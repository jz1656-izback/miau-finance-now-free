"""CoinPaprika API — 2000+ coins, market data, ICOs, exchanges, global overview.

Free key: 20k req/month. Get one at https://coinpaprika.com/api
"""
import httpx
from typing import Optional
from app.config import settings
from app.services.data.base import DataSource
from app.services.data.models import Quote


class CoinPaprikaProvider(DataSource):
    """Crypto market data from CoinPaprika."""

    @property
    def name(self) -> str:
        return "coinpaprika"

    @property
    def requires_key(self) -> bool:
        return True

    @property
    def rate_limit_per_minute(self) -> int:
        return 30

    @property
    def base_url(self) -> str:
        return "https://api.coinpaprika.com/v1"

    @property
    def capabilities(self) -> list[str]:
        return ["crypto"]

    def _headers(self) -> dict:
        key = __import__('app.services.data.vault', fromlist=['get_key']).get_key('coinpaprika_api_key') or settings.coinpaprika_api_key or ""
        return {"Authorization": f"Bearer {key}"} if key else {}

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self.base_url}/global", headers=self._headers())
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_global(self) -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/global", headers=self._headers())
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"CoinPaprika returned {r.status_code}")
            return r.json()

    async def fetch_ticker(self, coin_id: str) -> Quote:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/tickers/{coin_id}", headers=self._headers())
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"CoinPaprika ticker returned {r.status_code}")
            data = r.json()
            quotes = data.get("quotes", {}).get("USD", {})
            return Quote(
                ticker=coin_id,
                price=float(quotes.get("price", 0)),
                change=float(quotes.get("percent_change_24h", 0)),
                change_pct=float(quotes.get("percent_change_24h", 0)),
                volume=int(quotes.get("volume_24h", 0)),
                high=float(quotes.get("ath_price", 0)) if quotes.get("ath_price") else None,
                low=None,
                open=None,
                previous_close=None,
                timestamp=__import__("datetime").datetime.now(timezone.utc),
            )

    async def fetch_coins(self, limit: int = 50) -> list[dict]:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/coins", headers=self._headers())
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"CoinPaprika coins returned {r.status_code}")
            return r.json()[:limit]

    async def search_coin(self, symbol: str) -> list[dict]:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/coins", headers=self._headers())
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"CoinPaprika coins returned {r.status_code}")
            coins = r.json()
            return [c for c in coins if symbol.upper() in c.get("symbol", "").upper() or symbol.lower() in c.get("name", "").lower()]
