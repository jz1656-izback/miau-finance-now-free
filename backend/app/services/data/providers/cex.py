"""CEX public APIs — Binance, Coinbase, Kraken public ticker/orderbook data.

No key needed — these are public endpoints.
"""
import httpx
from app.services.data.base import DataSource


class CEXProvider(DataSource):
    """Public CEX data from Binance, Coinbase, Kraken. No key needed."""

    @property
    def name(self) -> str:
        return "cex"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 120

    @property
    def base_url(self) -> str:
        return ""

    @property
    def capabilities(self) -> list[str]:
        return ["crypto"]

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get("https://api.binance.com/api/v3/ping")
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_binance_ticker(self, symbol: str = "BTCUSDT") -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol.upper()}")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"Binance returned {r.status_code}")
            return r.json()

    async def fetch_coinbase_ticker(self, product_id: str = "BTC-USD") -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"https://api.exchange.coinbase.com/products/{product_id}/ticker")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"Coinbase returned {r.status_code}")
            return r.json()

    async def fetch_orderbook(self, exchange: str, symbol: str, limit: int = 10) -> dict:
        urls = {
            "binance": f"https://api.binance.com/api/v3/depth?symbol={symbol.upper()}&limit={limit}",
            "coinbase": f"https://api.exchange.coinbase.com/products/{symbol}/book?level=2",
            "kraken": f"https://api.kraken.com/0/public/Depth?pair={symbol}&count={limit}",
        }
        url = urls.get(exchange)
        if not url:
            raise ValueError(f"Unsupported exchange: {exchange}")
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"{exchange} orderbook returned {r.status_code}")
            return r.json()

    async def fetch_listings(self, exchange: str) -> list[dict]:
        urls = {
            "binance": "https://api.binance.com/api/v3/exchangeInfo",
            "coinbase": "https://api.exchange.coinbase.com/products",
            "kraken": "https://api.kraken.com/0/public/AssetPairs",
        }
        url = urls.get(exchange)
        if not url:
            raise ValueError(f"Unsupported exchange: {exchange}")
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(url)
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"{exchange} listings returned {r.status_code}")
            return r.json()
