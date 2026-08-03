import logging
from typing import Any, Optional

import httpx

from app.config import settings
from app.services.brokers.base import BrokerBase
from app.services.brokers.registry import register

logger = logging.getLogger(__name__)


@register("alpaca")
class AlpacaBroker(BrokerBase):
    display_name = "Alpaca Markets"

    def __init__(self):
        self._api_key = settings.alpaca_api_key or ""
        self._secret_key = settings.alpaca_secret_key or ""
        base = "https://paper-api.alpaca.markets" if settings.alpaca_paper else "https://api.alpaca.markets"
        self._base_url = base
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                headers={
                    "APCA-API-KEY-ID": self._api_key,
                    "APCA-API-SECRET-KEY": self._secret_key,
                },
                timeout=30.0,
            )
        return self._client

    async def get_account(self) -> dict[str, Any]:
        client = await self._get_client()
        resp = await client.get("/v2/account")
        resp.raise_for_status()
        data = resp.json()
        return {
            "id": data.get("id"),
            "status": data.get("status"),
            "currency": data.get("currency"),
            "cash": float(data.get("cash", 0)),
            "portfolio_value": float(data.get("portfolio_value", 0)),
            "buying_power": float(data.get("buying_power", 0)),
            "daytrade_count": data.get("daytrade_count", 0),
        }

    async def get_positions(self) -> list[dict[str, Any]]:
        client = await self._get_client()
        resp = await client.get("/v2/positions")
        resp.raise_for_status()
        return [
            {
                "symbol": p.get("symbol"),
                "qty": float(p.get("qty", 0)),
                "market_value": float(p.get("market_value", 0)),
                "cost_basis": float(p.get("cost_basis", 0)),
                "unrealized_pl": float(p.get("unrealized_pl", 0)),
                "unrealized_plpc": float(p.get("unrealized_plpc", 0)),
                "current_price": float(p.get("current_price", 0)),
                "avg_entry_price": float(p.get("avg_entry_price", 0)),
            }
            for p in (resp.json() or [])
        ]

    async def submit_order(self, order: dict[str, Any]) -> dict[str, Any]:
        client = await self._get_client()
        payload = {
            "symbol": order["symbol"],
            "qty": str(order["qty"]),
            "side": order["side"],
            "type": order.get("type", "market"),
            "time_in_force": order.get("time_in_force", "day"),
        }
        if "limit_price" in order:
            payload["limit_price"] = str(order["limit_price"])
        if "stop_price" in order:
            payload["stop_price"] = str(order["stop_price"])
        resp = await client.post("/v2/orders", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return {
            "id": data.get("id"),
            "symbol": data.get("symbol"),
            "qty": data.get("qty"),
            "side": data.get("side"),
            "type": data.get("type"),
            "status": data.get("status"),
            "filled_qty": data.get("filled_qty"),
            "filled_avg_price": data.get("filled_avg_price"),
            "created_at": data.get("created_at"),
        }

    async def cancel_order(self, order_id: str) -> dict[str, Any]:
        client = await self._get_client()
        resp = await client.delete(f"/v2/orders/{order_id}")
        resp.raise_for_status()
        return {"id": order_id, "status": "cancelled"}

    async def get_orders(self, status: Optional[str] = None) -> list[dict[str, Any]]:
        client = await self._get_client()
        params = {"limit": 50}
        if status:
            params["status"] = status
        resp = await client.get("/v2/orders", params=params)
        resp.raise_for_status()
        return [
            {
                "id": o.get("id"),
                "symbol": o.get("symbol"),
                "qty": o.get("qty"),
                "side": o.get("side"),
                "type": o.get("type"),
                "status": o.get("status"),
                "filled_qty": o.get("filled_qty"),
                "filled_avg_price": o.get("filled_avg_price"),
                "created_at": o.get("created_at"),
            }
            for o in (resp.json() or [])
        ]

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None
