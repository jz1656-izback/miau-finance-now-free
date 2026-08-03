import logging
from typing import Any, Optional

import httpx

from app.config import settings
from app.services.brokers.base import BrokerBase
from app.services.brokers.registry import register

logger = logging.getLogger(__name__)


@register("ibkr")
class IBBroker(BrokerBase):
    display_name = "Interactive Brokers (Client Portal)"

    def __init__(self):
        self._gateway_url = settings.ib_gateway_url or "https://localhost:5000"
        self._account_id = settings.ib_account_id or ""
        self._client: Optional[httpx.AsyncClient] = None
        self._auth_token: Optional[str] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self._gateway_url,
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
                logger.info("IBKR: authenticated with gateway at %s", self._gateway_url)
            else:
                logger.warning("IBKR: auth failed — %s %s", resp.status_code, resp.text)
        except httpx.ConnectError:
            logger.warning("IBKR: cannot connect to gateway at %s", self._gateway_url)
        except Exception as e:
            logger.warning("IBKR: auth error — %s", e)

    async def get_account(self) -> dict[str, Any]:
        client = await self._get_client()
        url = f"/v1/api/portfolio/{self._account_id}/account/meta"
        try:
            resp = await client.get(url)
            if resp.status_code != 200:
                return {
                    "broker": "ibkr",
                    "error": f"gateway returned {resp.status_code}",
                    "note": "Ensure IB Gateway/TWS is running and authenticated",
                }
            data = resp.json()
            return {
                "broker": "ibkr",
                "account_id": data.get("accountId", self._account_id),
                "currency": data.get("currency", "USD"),
                "account_type": data.get("accountType", ""),
                "status": "active",
            }
        except httpx.ConnectError:
            return {
                "broker": "ibkr",
                "error": f"Cannot connect to IB Gateway at {self._gateway_url}",
                "note": "Ensure IB Gateway/TWS is running on port 5000",
            }

    async def get_positions(self) -> list[dict[str, Any]]:
        client = await self._get_client()
        url = f"/v1/api/portfolio/{self._account_id}/positions/0"
        try:
            resp = await client.get(url)
            if resp.status_code != 200:
                return []
            data = resp.json()
            positions = []
            for p in data if isinstance(data, list) else [data]:
                mkt_price = float(p.get("marketPrice", 0))
                qty = float(p.get("position", 0))
                positions.append({
                    "symbol": p.get("contractDesc", ""),
                    "asset_class": p.get("assetClass", ""),
                    "qty": qty,
                    "market_value": mkt_price * qty,
                    "cost_basis": float(p.get("costBasisMoney", {}).get("amount", 0)),
                    "unrealized_pl": float(p.get("unrealizedPnl", {}).get("amount", 0)),
                    "current_price": mkt_price,
                    "currency": p.get("currency", "USD"),
                })
            return positions
        except httpx.ConnectError:
            logger.warning("IBKR: cannot connect to gateway for positions")
            return []

    async def submit_order(self, order: dict[str, Any]) -> dict[str, Any]:
        client = await self._get_client()
        payload = {
            "acctId": self._account_id,
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

        url = f"/v1/api/iserver/account/{self._account_id}/orders"
        try:
            resp = await client.post(url, json=[payload])
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
        except httpx.ConnectError:
            return {"error": f"Cannot connect to IB Gateway at {self._gateway_url}"}

    async def cancel_order(self, order_id: str) -> dict[str, Any]:
        client = await self._get_client()
        url = f"/v1/api/iserver/account/{self._account_id}/order/{order_id}"
        try:
            resp = await client.delete(url)
            if resp.status_code != 200:
                return {"error": f"IBKR cancel failed: {resp.text}"}
            return {"id": order_id, "status": "cancelled"}
        except httpx.ConnectError:
            return {"error": f"Cannot connect to IB Gateway at {self._gateway_url}"}

    async def get_orders(self, status: Optional[str] = None) -> list[dict[str, Any]]:
        client = await self._get_client()
        params = {}
        if status:
            params["status"] = status
        url = f"/v1/api/iserver/account/{self._account_id}/orders"
        try:
            resp = await client.get(url, params=params)
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
        except httpx.ConnectError:
            logger.warning("IBKR: cannot connect to gateway for orders")
            return []

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
