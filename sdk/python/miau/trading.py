"""Trading module for Miau Finance SDK."""

from __future__ import annotations

from typing import Any, Optional


class TradingModule:
    def __init__(self, client):
        self._client = client

    def place_order(self, ticker: str, quantity: float, side: str, order_type: str = "market", portfolio_id: Optional[str] = None, **kwargs) -> dict[str, Any]:
        body = {"ticker": ticker, "quantity": quantity, "side": side.upper(), "order_type": order_type, "portfolio_id": portfolio_id or "", **kwargs}
        return self._client._request("POST", "orders", json_body=body)

    def get_orders(self, portfolio_id: Optional[str] = None) -> list[dict[str, Any]]:
        params = {}
        if portfolio_id:
            params["portfolio_id"] = portfolio_id
        return self._client._request("GET", "orders", params=params)

    def cancel_order(self, order_id: str) -> dict[str, Any]:
        return self._client._request("DELETE", f"orders/{order_id}")

    def paper_account(self) -> dict[str, Any]:
        return self._client._request("GET", "paper/account")

    def paper_trade(self, ticker: str, quantity: float, side: str) -> dict[str, Any]:
        return self._client._request("POST", "paper/trade", json_body={"ticker": ticker, "quantity": quantity, "side": side.upper()})

    def paper_pnl(self) -> dict[str, Any]:
        return self._client._request("GET", "paper/pnl")

    def backtest(self, strategy: str, ticker: str, period: str = "1y", **params) -> dict[str, Any]:
        return self._client._request("GET", f"strategies/backtest/{strategy}/{ticker}", params={"period": period, **params})

    def list_brokers(self) -> list[dict[str, Any]]:
        return self._client._request("GET", "brokers")
