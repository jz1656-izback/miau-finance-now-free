"""Portfolio module for Miau Finance SDK."""

from __future__ import annotations

from typing import Any, Optional


class PortfolioModule:
    def __init__(self, client):
        self._client = client

    def list(self) -> list[dict[str, Any]]:
        return self._client._request("GET", "portfolios")

    def get(self, portfolio_id: str) -> dict[str, Any]:
        return self._client._request("GET", f"portfolios/{portfolio_id}")

    def get_positions(self, portfolio_id: str) -> list[dict[str, Any]]:
        return self._client._request("GET", f"portfolios/{portfolio_id}/positions")

    def set_currency(self, portfolio_id: str, currency: str) -> dict[str, Any]:
        return self._client._request("PUT", f"portfolios/{portfolio_id}/currency", params={"currency": currency})

    def get_pnl(self, portfolio_id: str, days: int = 30) -> dict[str, Any]:
        return self._client._request("GET", f"analytics/portfolios/{portfolio_id}/fx-pnl", params={"days": days})

    def get_summary(self) -> dict[str, Any]:
        return self._client._request("GET", "analytics/summary")

    def get_analytics(self, portfolio_id: str) -> dict[str, Any]:
        return self._client._request("GET", f"analytics/portfolios/{portfolio_id}")

    def get_risk(self, portfolio_id: str) -> list[dict[str, Any]]:
        return self._client._request("GET", f"analytics/portfolios/{portfolio_id}/risk")
