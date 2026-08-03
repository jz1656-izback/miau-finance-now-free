import logging
from typing import Any, Optional

import httpx

from app.config import settings
from app.services.brokers.base import BrokerBase
from app.services.brokers.registry import register

logger = logging.getLogger(__name__)

IB_GATEWAY_URL = getattr(settings, "ib_gateway_url", "https://localhost:5000")
IB_ACCOUNT_ID = getattr(settings, "ib_account_id", "")


@register("ibkr")
class IBrokerConnector(BrokerBase):
    display_name = "Interactive Brokers"

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None
        self._auth_token: Optional[str] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=IB_GATEWAY_URL,
                verify=False,
                timeout=30.0,
            )
            await self._authenticate()
        return self._client

    async def _authenticate(self) -> None:
        try:
            resp = await self._client.post("/v1/api/iserver/auth/ssodh/authenticate")
            if resp.status_code == 200:
                data = resp.json()
                self._auth_token = data.get("token", "")
                logger.info("IBKR: authenticated with gateway")
            else:
                logger.warning("IBKR: auth failed — %s %s", resp.status_code, resp.text)
        except Exception as e:
            logger.warning("IBKR: auth error — %s", e)

    async def get_account(self) -> dict[str, Any]:
        client = await self._get_client()
        resp = await client.get("/v1/api/portfolio/{IB_ACCOUNT_ID}/account/meta")
        if resp.status_code != 200:
            return {
                "broker": "ibkr",
                "error": f"gateway returned {resp.status_code}",
                "note": "Ensure IB Gateway/TWS is running on port 5000",
            }
        data = resp.json()
        return {
            "broker": "ibkr",
            "account_id": data.get("accountId", IB_ACCOUNT_ID),
            "currency": data.get("currency", "USD"),
            "account_type": data.get("accountType", ""),
            "status": "active",
        }

    async def get_positions(self) -> list[dict[str, Any]]:
        client = await self._get_client()
        resp = await client.get(f"/v1/api/portfolio/{IB_ACCOUNT_ID}/positions/0")
        if resp.status_code != 200:
            return []
        data = resp.json()
        positions = []
        for p in data if isinstance(data, list) else [data]:
            positions.append({
                "symbol": p.get("contractDesc", ""),
                "asset_class": p.get("assetClass", ""),
                "qty": float(p.get("position", 0)),
                "market_value": float(p.get("marketPrice", 0)) * float(p.get("position", 0)),
                "cost_basis": float(p.get("costBasisMoney", {}).get("amount", 0)),
                "unrealized_pnl": float(p.get("unrealizedPnl", {}).get("amount", 0)),
                "current_price": float(p.get("marketPrice", 0)),
                "currency": p.get("currency", "USD"),
            })
        return positions

    async def submit_order(self, order: dict[str, Any]) -> dict[str, Any]:
        client = await self._get_client()
        payload = {
            "acctId": IB_ACCOUNT_ID,
            "conid": order.get("conid", 0),
            "orderType": order.get("type", "MKT").upper(),
            "side": order.get("side", "BUY").upper(),
            "quantity": order.get("qty", 0),
            "ticker": order.get("symbol", ""),
        }
        if "limit_price" in order:
            payload["price"] = order["limit_price"]
        if "stop_price" in order:
            payload["auxPrice"] = order["stop_price"]

        resp = await client.post("/v1/api/iserver/account/{IB_ACCOUNT_ID}/orders", json=[payload])
        if resp.status_code != 200:
            return {"error": f"IBKR order failed: {resp.text}"}
        data = resp.json()
        return {
            "id": data.get("id", ""),
            "symbol": order.get("symbol"),
            "qty": order.get("qty"),
            "side": order.get("side"),
            "type": order.get("type", "market"),
            "status": data.get("order_status", "submitted"),
        }

    async def cancel_order(self, order_id: str) -> dict[str, Any]:
        client = await self._get_client()
        resp = await client.delete(f"/v1/api/iserver/account/{IB_ACCOUNT_ID}/order/{order_id}")
        if resp.status_code != 200:
            return {"error": f"IBKR cancel failed: {resp.text}"}
        return {"id": order_id, "status": "cancelled"}

    async def get_orders(self, status: Optional[str] = None) -> list[dict[str, Any]]:
        client = await self._get_client()
        params = {}
        if status:
            params["status"] = status
        resp = await client.get(f"/v1/api/iserver/account/{IB_ACCOUNT_ID}/orders", params=params)
        if resp.status_code != 200:
            return []
        data = resp.json()
        orders = []
        for o in data.get("orders", []):
            orders.append({
                "id": o.get("orderId", ""),
                "symbol": o.get("ticker", ""),
                "qty": o.get("quantity", 0),
                "side": o.get("side", "BUY"),
                "type": o.get("orderType", "MKT"),
                "status": o.get("orderStatus", ""),
                "filled_qty": o.get("filledQuantity", 0),
                "avg_price": float(o.get("avgPrice", 0)),
            })
        return orders

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
