"""HF Data Library — 1-min OHLCV bars for 1,391 US equities, 23+ years of history."""
import httpx
from datetime import datetime
from typing import Optional
from app.services.data.base import DataSource, ProviderUnavailableError
from app.services.data.models import OHLCV


class HFDataProvider(DataSource):
    """High-frequency data from HF Data Library. Free key at https://hfdata.io."""

    @property
    def name(self) -> str:
        return "hfdata"

    @property
    def requires_key(self) -> bool:
        return True

    @property
    def rate_limit_per_minute(self) -> int:
        return 300

    @property
    def base_url(self) -> str:
        return "https://api.hfdata.io/v1"

    @property
    def capabilities(self) -> list[str]:
        return ["intraday", "ohlcv", "us_equities"]

    async def _get_key(self) -> str:
        from os import environ
        key = environ.get("HFDATA_API_KEY", "")
        if not key:
            from app.services.data.base import ConfigError
            raise ConfigError("HFDATA_API_KEY not set in environment")
        return key

    async def _test_connection(self) -> bool:
        try:
            key = await self._get_key()
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{self.base_url}/stocks?api_key={key}&limit=1")
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_intraday(self, ticker: str, interval: str = "1min", limit: int = 390) -> list[OHLCV]:
        """Fetch intraday OHLCV bars.
        
        Args:
            ticker: Stock symbol
            interval: 1min, 5min, 15min, 30min, 60min
            limit: Number of bars (default 390 = 1 trading day of 1-min bars)
        """
        key = await self._get_key()
        params = {"api_key": key, "ticker": ticker.upper(), "interval": interval, "limit": min(limit, 5000)}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/intraday", params=params)
            if r.status_code == 429:
                raise ProviderUnavailableError("HF Data rate limit exceeded")
            if r.status_code != 200:
                raise ProviderUnavailableError(f"HF Data returned {r.status_code}")
            data = r.json()
            if isinstance(data, dict) and "data" in data:
                data = data["data"]
            return [
                OHLCV(
                    timestamp=d.get("timestamp", d.get("t", "")),
                    open=float(d.get("open", d.get("o", 0))),
                    high=float(d.get("high", d.get("h", 0))),
                    low=float(d.get("low", d.get("l", 0))),
                    close=float(d.get("close", d.get("c", 0))),
                    volume=int(d.get("volume", d.get("v", 0))),
                )
                for d in data if d.get("close") or d.get("c")
            ]

    async def fetch_daily(self, ticker: str, limit: int = 252) -> list[OHLCV]:
        """Fetch daily OHLCV bars (1 year = ~252 trading days)."""
        key = await self._get_key()
        params = {"api_key": key, "ticker": ticker.upper(), "interval": "daily", "limit": min(limit, 5000)}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/intraday", params=params)
            if r.status_code != 200:
                raise ProviderUnavailableError(f"HF Data daily returned {r.status_code}")
            data = r.json()
            if isinstance(data, dict) and "data" in data:
                data = data["data"]
            return [
                OHLCV(
                    timestamp=d.get("timestamp", d.get("t", "")),
                    open=float(d.get("open", d.get("o", 0))),
                    high=float(d.get("high", d.get("h", 0))),
                    low=float(d.get("low", d.get("l", 0))),
                    close=float(d.get("close", d.get("c", 0))),
                    volume=int(d.get("volume", d.get("v", 0))),
                )
                for d in data if d.get("close") or d.get("c")
            ]

    async def search_stocks(self, query: str) -> list[dict]:
        """Search available stocks by ticker or name."""
        key = await self._get_key()
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/stocks?api_key={key}&search={query}")
            if r.status_code != 200:
                return []
            data = r.json()
            if isinstance(data, dict) and "data" in data:
                data = data["data"]
            return [
                {"ticker": d.get("ticker", ""), "name": d.get("name", ""), "sector": d.get("sector", "")}
                for d in data if d.get("ticker")
            ]
