"""DumbStockAPI — ticker metadata across all global exchanges. No key needed."""
import httpx
from app.services.data.base import DataSource


class DumbStockProvider(DataSource):
    """Free ticker search from DumbStockAPI. No key needed."""

    @property
    def name(self) -> str:
        return "dumbstock"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 9999

    @property
    def base_url(self) -> str:
        return "https://dumbstockapi.com/stock"

    @property
    def capabilities(self) -> list[str]:
        return ["screener"]

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self.base_url}/ticker/AAPL")
                return r.status_code < 500
        except Exception:
            return False

    async def search_ticker(self, query: str) -> list[dict]:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}?search={query}&limit=20")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"DumbStockAPI returned {r.status_code}")
            return r.json()

    async def get_ticker_info(self, ticker: str) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/ticker/{ticker.upper()}")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"DumbStockAPI returned {r.status_code}")
            data = r.json()
            if isinstance(data, list) and data:
                return data[0]
            return {}
