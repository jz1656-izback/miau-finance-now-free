import logging
from typing import Any, Optional

import httpx

from app.config import settings
from app.services.brokers.base import BrokerBase
from app.services.brokers.registry import register

logger = logging.getLogger(__name__)

SAXO_BASE_URL = getattr(settings, "saxo_base_url", "https://gateway.saxobank.com/sim/openapi")
SAXO_CLIENT_KEY = getattr(settings, "saxo_client_key", "")
SAXO_CLIENT_SECRET = getattr(settings, "saxo_client_secret", "")
SAXO_TOKEN_URL = getattr(settings, "saxo_token_url", "https://gateway.saxobank.com/sim/openapi/oauth2/token")


@register("saxo")
class SaxoBroker(BrokerBase):
    display_name = "Saxo Bank"

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
        self._access_token: Optional[str] = None
        self._token_expiry: float = 0

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=SAXO_BASE_URL,
                timeout=30.0,
            )
            await self._authenticate()
        return self._client

    async def _authenticate(self) -> None:
        if not SAXO_CLIENT_KEY or not SAXO_CLIENT_SECRET:
            logger.warning("Saxo: missing credentials — set SAXO_CLIENT_KEY and SAXO_CLIENT_SECRET")
            return
        try:
            resp = await httpx.AsyncClient().post(
                SAXO_TOKEN_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": SAXO_CLIENT_KEY,
                    "client_secret": SAXO_CLIENT_SECRET,
                },
            )
            if resp.status_code == 200:
                data = resp.json()
                self._access_token = data.get("access_token", "")
                logger.info("Saxo: authenticated")
            else:
                logger.warning("Saxo: auth failed — %s", resp.text)
        except Exception as e:
            logger.warning("Saxo: auth error — %s", e)

    async def _headers(self) -> dict[str, str]:
        h = {"Content-Type": "application/json"}
        if self._access_token:
            h["Authorization"] = f"Bearer {self._access_token}"
        return h

    async def get_account(self) -> dict[str, Any]:
        client = await self._get_client()
        resp = await client.get("/port/v1/accounts/me", headers=await self._headers())
        if resp.status_code != 200:
            return {"broker": "saxo", "error": f"gateway returned {resp.status_code}"}
        data = resp.json()
        return {
            "broker": "saxo",
            "account_id": data.get("AccountId", ""),
            "account_type": data.get("AccountType", ""),
            "currency": data.get("Currency", "USD"),
            "status": "active",
        }

    async def get_positions(self) -> list[dict[str, Any]]:
        client = await self._get_client()
        resp = await client.get("/port/v1/positions/me", headers=await self._headers())
        if resp.status_code != 200:
            return []
        data = resp.json()
        positions = []
        for p in data.get("Data", []):
            positions.append({
                "symbol": p.get("Symbol", ""),
                "asset_class": p.get("AssetType", ""),
                "qty": float(p.get("Amount", 0)),
                "market_value": float(p.get("MarketValue", {}).get("Amount", 0)),
                "cost_basis": float(p.get("CostPrice", {}).get("Amount", 0)) * float(p.get("Amount", 0)),
                "unrealized_pnl": float(p.get("ProfitLossForPeriod", {}).get("Amount", 0)),
                "current_price": float(p.get("CurrentPrice", {}).get("Amount", 0)),
                "currency": p.get("MarketValue", {}).get("Currency", "USD"),
            })
        return positions

    async def submit_order(self, order: dict[str, Any]) -> dict[str, Any]:
        client = await self._get_client()
        payload = {
            "AccountKey": order.get("account_key", ""),
            "BuySell": order.get("side", "Buy").lower(),
            "Amount": order.get("qty", 0),
            "AssetType": order.get("asset_type", "Stock"),
            "OrderType": order.get("type", "Market").lower(),
            "OrderDuration": {"DurationType": "DayOrder"},
        }
        if order.get("symbol"):
            payload["Symbol"] = order["symbol"].upper()

        if "limit_price" in order:
            payload["OrderPrice"] = {"Amount": order["limit_price"], "Currency": order.get("currency", "USD")}
        if "stop_price" in order:
            payload["OrderTrigger"] = {"TriggerPrice": {"Amount": order["stop_price"], "Currency": order.get("currency", "USD")}}

        resp = await client.post("/trade/v1/orders", json=payload, headers=await self._headers())
        if resp.status_code != 201:
            return {"error": f"Saxo order failed: {resp.text}"}
        data = resp.json()
        return {
            "id": data.get("OrderId", ""),
            "symbol": order.get("symbol"),
            "qty": order.get("qty"),
            "side": order.get("side"),
            "type": order.get("type", "market"),
            "status": data.get("Status", "submitted"),
        }

    async def cancel_order(self, order_id: str) -> dict[str, Any]:
        client = await self._get_client()
        resp = await client.delete(f"/trade/v1/orders/{order_id}", headers=await self._headers())
        if resp.status_code != 204:
            return {"error": f"Saxo cancel failed: {resp.text}"}
        return {"id": order_id, "status": "cancelled"}

    async def get_orders(self, status: Optional[str] = None) -> list[dict[str, Any]]:
        client = await self._get_client()
        params = {}
        if status:
            params["status"] = status
        resp = await client.get("/trade/v1/orders", params=params, headers=await self._headers())
        if resp.status_code != 200:
            return []
        data = resp.json()
        orders = []
        for o in data.get("Data", []):
            orders.append({
                "id": o.get("OrderId", ""),
                "symbol": o.get("Symbol", ""),
                "qty": float(o.get("Amount", 0)),
                "side": o.get("BuySell", "Buy"),
                "type": o.get("OrderType", "Market"),
                "status": o.get("Status", ""),
                "filled_qty": float(o.get("FilledAmount", 0)),
                "avg_price": float(o.get("Price", {}).get("Amount", 0)),
            })
        return orders

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
