"""Twelve Data — real-time/historical for 100k+ instruments, 50+ technical indicators.

Free key: 800 req/day. Get one at https://twelvedata.com/apikey
"""
import httpx
from datetime import timezone, datetime
from typing import Optional
from app.config import settings
from app.services.data.base import DataSource
from app.services.data.models import Quote, OHLCV


class TwelveDataProvider(DataSource):
    """Technical indicators and market data from Twelve Data."""

    @property
    def name(self) -> str:
        return "twelvedata"

    @property
    def requires_key(self) -> bool:
        return True

    @property
    def rate_limit_per_minute(self) -> int:
        return 8

    @property
    def base_url(self) -> str:
        return "https://api.twelvedata.com"

    @property
    def capabilities(self) -> list[str]:
        return ["quote", "history", "technical"]

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self.base_url}/quote?symbol=AAPL&apikey={__import__('app.services.data.vault', fromlist=['get_key']).get_key('twelvedata_api_key') or settings.twelvedata_api_key or ''}")
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_quote(self, ticker: str) -> Quote:
        params = {"symbol": ticker.upper(), "apikey": __import__('app.services.data.vault', fromlist=['get_key']).get_key('twelvedata_api_key') or settings.twelvedata_api_key or ""}
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/quote", params=params)
            if r.status_code == 429:
                from app.services.data.base import RateLimitError
                raise RateLimitError("Twelve Data rate limit exceeded")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"Twelve Data returned {r.status_code}")
            data = r.json()
            return Quote(
                ticker=ticker.upper(),
                price=float(data.get("close", 0)),
                change=float(data.get("change", 0)),
                change_pct=float(data.get("percent_change", 0)),
                open=float(data["open"]) if data.get("open") else None,
                high=float(data["high"]) if data.get("high") else None,
                low=float(data["low"]) if data.get("low") else None,
                volume=int(data["volume"]) if data.get("volume") else None,
                timestamp=datetime.now(timezone.utc),
            )

    async def fetch_history(self, ticker: str, period: str = "1mo", interval: str = "1d") -> list[OHLCV]:
        params = {
            "symbol": ticker.upper(),
            "interval": interval,
            "outputsize": {"1d": 1, "5d": 5, "1mo": 22, "3mo": 66, "6mo": 132, "1y": 264}.get(period, 22),
            "apikey": __import__('app.services.data.vault', fromlist=['get_key']).get_key('twelvedata_api_key') or settings.twelvedata_api_key or "",
        }
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/time_series", params=params)
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"Twelve Data history returned {r.status_code}")
            data = r.json()
            values = data.get("values", [])
            return [
                OHLCV(
                    timestamp=datetime.strptime(v["datetime"], "%Y-%m-%d %H:%M:%S") if " " in v.get("datetime", "") else datetime.strptime(v["datetime"], "%Y-%m-%d"),
                    open=float(v["open"]), high=float(v["high"]), low=float(v["low"]), close=float(v["close"]), volume=int(v["volume"]),
                )
                for v in values if all(k in v for k in ("open", "high", "low", "close", "volume", "datetime"))
            ]

    async def fetch_technicals(self, ticker: str, indicator: str = "rsi") -> dict:
        params = {
            "symbol": ticker.upper(),
            "interval": "1day",
            "indicator": indicator,
            "apikey": __import__('app.services.data.vault', fromlist=['get_key']).get_key('twelvedata_api_key') or settings.twelvedata_api_key or "",
        }
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/{indicator}", params=params)
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"Twelve Data {indicator} returned {r.status_code}")
            return r.json()
