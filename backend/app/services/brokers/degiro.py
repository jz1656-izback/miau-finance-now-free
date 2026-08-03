import logging
import re
from typing import Any, Optional

import httpx

from app.config import settings
from app.services.brokers.base import BrokerBase
from app.services.brokers.registry import register

logger = logging.getLogger(__name__)

DEGIRO_BASE = getattr(settings, "degiro_base_url", "https://degiro.adaptable.app")
DEGIRO_USERNAME = getattr(settings, "degiro_username", "")
DEGIRO_PASSWORD = getattr(settings, "degiro_password", "")


@register("degiro")
class DegiroBroker(BrokerBase):
    display_name = "DEGIRO"

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
        self._session_id: Optional[str] = None
        self._account_id: Optional[int] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(base_url=DEGIRO_BASE, timeout=30.0)
            await self._login()
        return self._client

    async def _login(self) -> bool:
        if not DEGIRO_USERNAME or not DEGIRO_PASSWORD:
            logger.warning("DEGIRO: missing credentials")
            return False
        try:
            resp = await self._client.post("/login/secure", json={
                "username": DEGIRO_USERNAME,
                "password": DEGIRO_PASSWORD,
                "isPassCodeReset": False,
                "isRedirectToMobile": False,
            })
            if resp.status_code == 200:
                data = resp.json()
                self._session_id = data.get("sessionId")
                self._account_id = data.get("accountId")
                logger.info("DEGIRO: logged in as %s", DEGIRO_USERNAME)
                return True
            logger.warning("DEGIRO: login failed: %s", resp.status_code)
            return False
        except Exception as e:
            logger.error("DEGIRO: login error: %s", e)
            return False

    async def connect(self) -> bool:
        return await self._login()

    async def disconnect(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
        self._session_id = None

    async def get_account(self) -> dict[str, Any]:
        if not self._session_id:
            return {"broker": "degiro", "status": "disconnected"}
        try:
            client = await self._get_client()
            resp = await client.get(f"/v6/account/info/{self._account_id}")
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "broker": "degiro",
                    "account_id": str(self._account_id),
                    "cash": float(data.get("cashFunds", {}).get("value", 0)),
                    "portfolio_value": float(data.get("totalPortfolioValue", {}).get("value", 0)),
                    "currency": "EUR",
                    "status": "active",
                }
            return {"broker": "degiro", "status": "unavailable"}
        except Exception as e:
            logger.error("DEGIRO: get_account failed: %s", e)
            return {"broker": "degiro", "status": "error", "error": str(e)}

    async def get_positions(self) -> list[dict[str, Any]]:
        if not self._session_id:
            return []
        try:
            client = await self._get_client()
            resp = await client.get(f"/v6/portfolio/position?accountId={self._account_id}")
            if resp.status_code == 200:
                data = resp.json()
                return [
                    {
                        "symbol": p.get("symbol", ""),
                        "qty": float(p.get("position", {}).get("size", 0)),
                        "market_value": float(p.get("position", {}).get("marketValue", {}).get("value", 0)),
                        "unrealized_pnl": float(p.get("result", {}).get("unrealized", {}).get("value", 0)),
                        "current_price": float(p.get("price", {}).get("lastPrice", {}).get("value", 0)),
                    }
                    for p in (data.get("data", []) or [])
                ]
            return []
        except Exception as e:
            logger.error("DEGIRO: get_positions failed: %s", e)
            return []

    async def submit_order(self, order: dict[str, Any]) -> dict[str, Any]:
        if not self._session_id:
            return {"id": "", "status": "disconnected"}
        try:
            client = await self._get_client()
            payload = {
                "buySell": order["side"].upper(),
                "orderType": order.get("type", "market").upper(),
                "productId": order.get("product_id", 0),
                "timeType": "DAY",
                "size": str(order["qty"]),
            }
            if order.get("type") == "limit" and "limit_price" in order:
                payload["limitPrice"] = {"value": order["limit_price"], "decimals": 2}
            resp = await client.post(f"/v6/order/{self._account_id}", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return {"id": str(data.get("orderId", "")), "status": "submitted"}
            return {"id": "", "status": "rejected", "error": f"HTTP {resp.status_code}"}
        except Exception as e:
            logger.error("DEGIRO: order failed: %s", e)
            return {"id": "", "status": "error", "error": str(e)}

    async def cancel_order(self, order_id: str) -> dict[str, Any]:
        if not self._session_id:
            return {"id": order_id, "status": "disconnected"}
        try:
            client = await self._get_client()
            resp = await client.delete(f"/v6/order/{order_id}")
            return {"id": order_id, "status": "cancelled" if resp.status_code == 200 else "error"}
        except Exception as e:
            return {"id": order_id, "status": "error", "error": str(e)}

    async def get_orders(self, status: Optional[str] = None) -> list[dict[str, Any]]:
        if not self._session_id:
            return []
        try:
            client = await self._get_client()
            resp = await client.get(f"/v6/order?accountId={self._account_id}")
            if resp.status_code == 200:
                data = resp.json()
                return [
                    {
                        "id": str(o.get("orderId", "")),
                        "symbol": o.get("symbol", ""),
                        "qty": float(o.get("size", 0)),
                        "side": o.get("buySell", ""),
                        "type": o.get("orderType", "").lower(),
                        "status": o.get("status", "").lower(),
                        "created_at": o.get("created", ""),
                    }
                    for o in (data.get("data", []) or [])
                ]
            return []
        except Exception as e:
            logger.error("DEGIRO: get_orders failed: %s", e)
            return []

    async def close(self) -> None:
        await self.disconnect()
