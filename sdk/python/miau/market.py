"""Market data module for the Miau Finance Python SDK."""

from typing import Optional

from miau import MiauClient


class MarketModule:
    """Access market data endpoints."""

    def __init__(self, client: MiauClient):
        self._client = client

    def live(self, tickers: str) -> dict:
        return self._client.get("/api/v1/market/live", params={"tickers": tickers})

    def historical(self, ticker: str, period: str = "6mo") -> list[dict]:
        return self._client.get(f"/api/v1/market/historical/{ticker}", params={"period": period})

    def movers(self) -> list[dict]:
        return self._client.get("/api/v1/market/movers")

    def sectors(self) -> list[dict]:
        return self._client.get("/api/v1/market/sectors")

    def indicators(self) -> dict:
        return self._client.get("/api/v1/market/indicators")

    def forex(self, base: str = "USD") -> dict:
        return self._client.get("/api/v1/market/forex", params={"base": base})

    def crypto_price(self, coin: str = "bitcoin") -> dict:
        return self._client.get(f"/api/v1/market/crypto", params={"coin": coin})

    def crypto_top(self, limit: int = 20) -> list[dict]:
        return self._client.get("/api/v1/market/crypto/top", params={"limit": limit})

    def news(self, tickers: Optional[str] = None) -> list[dict]:
        params = {}
        if tickers:
            params["tickers"] = tickers
        return self._client.get("/api/v1/news/market", params=params)

    async def async_live(self, tickers: str) -> dict:
        return await self._client.async_get("/api/v1/market/live", params={"tickers": tickers})

    async def async_historical(self, ticker: str, period: str = "6mo") -> list[dict]:
        return await self._client.async_get(f"/api/v1/market/historical/{ticker}", params={"period": period})
