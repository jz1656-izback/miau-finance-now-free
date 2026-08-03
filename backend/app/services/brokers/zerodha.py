import logging
from typing import Any, Optional

import httpx

from app.config import settings
from app.services.brokers.base import BrokerBase
from app.services.brokers.registry import register

logger = logging.getLogger(__name__)

ZERODHA_BASE = getattr(settings, "zerodha_base_url", "https://api.kite.trade")
ZERODHA_API_KEY = getattr(settings, "zerodha_api_key", "")
ZERODHA_ACCESS_TOKEN = getattr(settings, "zerodha_access_token", "")


@register("zerodha")
class ZerodhaBroker(BrokerBase):
    display_name = "Zerodha Kite"

    def __init__(self):
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            headers = {"X-Kite-Version": "3"}
            if ZERODHA_ACCESS_TOKEN:
                headers["Authorization"] = f"token {ZERODHA_API_KEY}:{ZERODHA_ACCESS_TOKEN}"
            self._client = httpx.AsyncClient(base_url=ZERODHA_BASE, headers=headers, timeout=30.0)
        return self._client

    async def connect(self) -> bool:
        try:
            client = await self._get_client()
            resp = await client.get("/user/profile")
            if resp.status_code == 200:
                logger.info("Zerodha: connected")
                return True
            logger.warning("Zerodha: connection failed: %s", resp.status_code)
            return False
        except Exception as e:
            logger.error("Zerodha: connect error: %s", e)
            return False

    async def disconnect(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get_account(self) -> dict[str, Any]:
        try:
            client = await self._get_client()
            resp = await client.get("/user/profile")
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                return {
                    "broker": "zerodha",
                    "account_id": data.get("user_id", ""),
                    "display_name": data.get("user_name", ""),
                    "email": data.get("email", ""),
                    "currency": "INR",
                    "status": "active",
                }
            return {"broker": "zerodha", "status": "unavailable"}
        except Exception as e:
            logger.error("Zerodha: get_account failed: %s", e)
            return {"broker": "zerodha", "status": "error", "error": str(e)}

    async def get_positions(self) -> list[dict[str, Any]]:
        try:
            client = await self._get_client()
            resp = await client.get("/portfolio/positions")
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                day = data.get("day", []) or []
                net = {p.get("trading_symbol", ""): p for p in (data.get("net", []) or [])}
                result = []
                for p in day:
                    sym = p.get("trading_symbol", "")
                    net_p = net.get(sym, {})
                    result.append({
                        "symbol": sym,
                        "qty": float(net_p.get("quantity", p.get("quantity", 0))),
                        "market_value": float(net_p.get("market_value", p.get("market_value", 0))),
                        "unrealized_pnl": float(net_p.get("unrealised", p.get("unrealised", 0))),
                        "current_price": float(p.get("last_price", 0)),
                        "avg_entry_price": float(net_p.get("average_price", 0)),
                        "currency": "INR",
                    })
                return result
            return []
        except Exception as e:
            logger.error("Zerodha: get_positions failed: %s", e)
            return []

    async def submit_order(self, order: dict[str, Any]) -> dict[str, Any]:
        try:
            client = await self._get_client()
            payload = {
                "tradingsymbol": order["symbol"],
                "exchange": order.get("exchange", "NSE"),
                "transaction_type": order["side"].upper(),
                "quantity": order["qty"],
                "order_type": order.get("type", "MARKET").upper(),
                "product": order.get("product", "CNC"),
                "validity": order.get("time_in_force", "DAY").upper(),
            }
            if "limit_price" in order:
                payload["price"] = str(order["limit_price"])
            if "stop_price" in order:
                payload["trigger_price"] = str(order["stop_price"])
            resp = await client.post("/orders/regular", json=payload)
            if resp.status_code == 200:
                data = resp.json().get("data", {})
                return {"id": str(data.get("order_id", "")), "status": "submitted"}
            error = resp.json().get("message", "Unknown error")
            return {"id": "", "status": "rejected", "error": error}
        except Exception as e:
            logger.error("Zerodha: order failed: %s", e)
            return {"id": "", "status": "error", "error": str(e)}

    async def cancel_order(self, order_id: str) -> dict[str, Any]:
        try:
            client = await self._get_client()
            resp = await client.delete(f"/orders/regular/{order_id}")
            return {"id": order_id, "status": "cancelled" if resp.status_code == 200 else "error"}
        except Exception as e:
            return {"id": order_id, "status": "error", "error": str(e)}

    async def get_orders(self, status: Optional[str] = None) -> list[dict[str, Any]]:
        try:
            client = await self._get_client()
            params = {}
            if status:
                params["status"] = status
            resp = await client.get("/orders", params=params)
            if resp.status_code == 200:
                data = resp.json().get("data", []) or []
                return [
                    {
                        "id": str(o.get("order_id", "")),
                        "symbol": o.get("tradingsymbol", ""),
                        "qty": float(o.get("quantity", 0)),
                        "side": o.get("transaction_type", ""),
                        "type": o.get("order_type", "").lower(),
                        "status": o.get("status", "").lower(),
                        "filled_qty": float(o.get("filled_quantity", 0)),
                        "filled_avg_price": float(o.get("average_price", 0)),
                        "created_at": o.get("order_timestamp", ""),
                    }
                    for o in data
                ]
            return []
        except Exception as e:
            logger.error("Zerodha: get_orders failed: %s", e)
            return []

    async def close(self) -> None:
        await self.disconnect()
