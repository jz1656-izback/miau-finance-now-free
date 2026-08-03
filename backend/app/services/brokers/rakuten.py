import logging
import hashlib
from typing import Any, Optional

import httpx

from app.config import settings
from app.services.brokers.base import BrokerBase
from app.services.brokers.registry import register

logger = logging.getLogger(__name__)

RAKUTEN_BASE = getattr(settings, "rakuten_base_url", "https://api.rakuten-sec.co.jp")
RAKUTEN_API_KEY = getattr(settings, "rakuten_api_key", "")
RAKUTEN_API_SECRET = getattr(settings, "rakuten_api_secret", "")


@register("rakuten")
class RakutenBroker(BrokerBase):
    display_name = "Rakuten Securities"

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
        self._access_token: Optional[str] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(base_url=RAKUTEN_BASE, timeout=30.0)
            if RAKUTEN_API_KEY and RAKUTEN_API_SECRET:
                self._client.headers["X-API-KEY"] = RAKUTEN_API_KEY
                self._client.headers["X-API-SECRET"] = RAKUTEN_API_SECRET
        return self._client

    async def connect(self) -> bool:
        try:
            client = await self._get_client()
            resp = await client.get("/v1/member/status")
            if resp.status_code == 200:
                self._access_token = resp.headers.get("X-ACCESS-TOKEN")
                logger.info("Rakuten: connected")
                return True
            logger.warning("Rakuten: connection failed: %s", resp.status_code)
            return False
        except Exception as e:
            logger.error("Rakuten: connect error: %s", e)
            return False

    async def disconnect(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
        self._access_token = None

    async def get_account(self) -> dict[str, Any]:
        try:
            client = await self._get_client()
            resp = await client.get("/v1/accounts/balance")
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "broker": "rakuten",
                    "account_id": data.get("accountId", ""),
                    "cash": float(data.get("cashBalance", 0)),
                    "currency": "JPY",
                    "status": "active",
                    "buying_power": float(data.get("buyingPower", 0)),
                }
            return {"broker": "rakuten", "status": "unavailable"}
        except Exception as e:
            logger.error("Rakuten: get_account failed: %s", e)
            return {"broker": "rakuten", "status": "error", "error": str(e)}

    async def get_positions(self) -> list[dict[str, Any]]:
        try:
            client = await self._get_client()
            resp = await client.get("/v1/accounts/positions")
            if resp.status_code == 200:
                data = resp.json()
                return [
                    {
                        "symbol": p.get("symbol", ""),
                        "qty": float(p.get("quantity", 0)),
                        "market_value": float(p.get("marketValue", 0)),
                        "unrealized_pnl": float(p.get("unrealizedPnl", 0)),
                        "currency": "JPY",
                    }
                    for p in (data.get("positions", []) or [])
                ]
            return []
        except Exception as e:
            logger.error("Rakuten: get_positions failed: %s", e)
            return []

    async def submit_order(self, order: dict[str, Any]) -> dict[str, Any]:
        try:
            client = await self._get_client()
            payload = {
                "symbol": order["symbol"],
                "side": order["side"].upper(),
                "orderType": order.get("type", "market").upper(),
                "quantity": order["qty"],
                "timeInForce": order.get("time_in_force", "DAY"),
            }
            if "limit_price" in order:
                payload["price"] = order["limit_price"]
            resp = await client.post("/v1/orders", json=payload)
            if resp.status_code == 200:
                data = resp.json()
                return {"id": str(data.get("orderId", "")), "status": "submitted"}
            return {"id": "", "status": "rejected", "error": f"HTTP {resp.status_code}"}
        except Exception as e:
            logger.error("Rakuten: order failed: %s", e)
            return {"id": "", "status": "error", "error": str(e)}

    async def cancel_order(self, order_id: str) -> dict[str, Any]:
        try:
            client = await self._get_client()
            resp = await client.delete(f"/v1/orders/{order_id}")
            return {"id": order_id, "status": "cancelled" if resp.status_code == 200 else "error"}
        except Exception as e:
            return {"id": order_id, "status": "error", "error": str(e)}

    async def get_orders(self, status: Optional[str] = None) -> list[dict[str, Any]]:
        try:
            client = await self._get_client()
            params = {}
            if status:
                params["status"] = status
            resp = await client.get("/v1/orders", params=params)
            if resp.status_code == 200:
                data = resp.json()
                return [
                    {
                        "id": str(o.get("orderId", "")),
                        "symbol": o.get("symbol", ""),
                        "qty": float(o.get("quantity", 0)),
                        "side": o.get("side", "").upper(),
                        "type": o.get("orderType", "").lower(),
                        "status": o.get("status", "").lower(),
                        "created_at": o.get("createdAt", ""),
                    }
                    for o in (data.get("orders", []) or [])
                ]
            return []
        except Exception as e:
            logger.error("Rakuten: get_orders failed: %s", e)
            return []

    async def close(self) -> None:
        await self.disconnect()
