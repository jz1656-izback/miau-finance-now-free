"""StockPrice.dev — free real-time stock prices, no auth, no limits."""
import httpx
from typing import Optional
from datetime import timezone, datetime
from app.services.data.base import DataSource
from app.services.data.models import Quote, HealthStatus


class StockPriceDevProvider(DataSource):
    """Free real-time stock prices from stockprice.dev. No key needed."""

    @property
    def name(self) -> str:
        return "stockpricedev"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 9999  # no documented limit

    @property
    def base_url(self) -> str:
        return "https://stockprice.dev"

    @property
    def capabilities(self) -> list[str]:
        return ["quote"]

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self.base_url}/api/v1/quote/AAPL")
                return r.status_code < 500
        except Exception:
            return False

    async def fetch_quote(self, ticker: str) -> Quote:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/api/v1/quote/{ticker.upper()}")
            if r.status_code == 429:
                from app.services.data.base import RateLimitError
                raise RateLimitError(f"StockPrice.dev rate limited")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"StockPrice.dev returned {r.status_code}")
            data = r.json()
            return Quote(
                ticker=data.get("symbol", ticker.upper()),
                price=float(data.get("price", 0)),
                change=float(data.get("change", 0)),
                change_pct=float(data.get("changesPercentage", 0)),
                open=float(data["open"]) if data.get("open") else None,
                high=float(data["dayHigh"]) if data.get("dayHigh") else None,
                low=float(data["dayLow"]) if data.get("dayLow") else None,
                volume=int(data["volume"]) if data.get("volume") else None,
                previous_close=float(data["previousClose"]) if data.get("previousClose") else None,
                timestamp=datetime.now(timezone.utc),
            )
