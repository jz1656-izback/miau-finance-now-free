"""CoinGecko — crypto prices, market data, top coins, categories, trends. No key needed for basic tier."""
import httpx
from datetime import datetime
from typing import Optional
from app.services.data.base import DataSource


class CoinGeckoProvider(DataSource):
    """Crypto data from CoinGecko. Free tier: 10-30 req/min, no key needed."""

    @property
    def name(self) -> str:
        return "coingecko"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 30

    @property
    def base_url(self) -> str:
        return "https://api.coingecko.com/api/v3"

    @property
    def capabilities(self) -> list[str]:
        return ["crypto", "price", "market"]

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{self.base_url}/ping")
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_price(self, coin_id: str = "bitcoin", currency: str = "usd") -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/simple/price?ids={coin_id}&vs_currencies={currency}&include_24hr_change=true&include_market_cap=true&include_24hr_vol=true")
            if r.status_code != 200:
                return {"coin": coin_id, "error": f"HTTP {r.status_code}"}
            data = r.json().get(coin_id, {})
            return {
                "coin": coin_id, "price": data.get(currency),
                "change_24h_pct": data.get(f"{currency}_24h_change"),
                "market_cap": data.get(f"{currency}_market_cap"),
                "volume_24h": data.get(f"{currency}_24h_vol"),
                "currency": currency.upper(),
            }

    async def fetch_market_overview(self, currency: str = "usd") -> dict:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/global")
            if r.status_code != 200:
                return {"error": f"HTTP {r.status_code}"}
            data = r.json().get("data", {})
            return {
                "total_market_cap": data.get("total_market_cap", {}).get(currency),
                "total_volume_24h": data.get("total_volume", {}).get(currency),
                "btc_dominance_pct": round(data.get("market_cap_percentage", {}).get("btc", 0), 2),
                "active_cryptos": data.get("active_cryptocurrencies", 0),
                "markets": data.get("markets", 0),
            }

    async def fetch_top_coins(self, limit: int = 20, currency: str = "usd") -> list[dict]:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/coins/markets?vs_currency={currency}&order=market_cap_desc&per_page={limit}&page=1&sparkline=false&price_change_percentage=24h")
            if r.status_code != 200:
                return []
            coins = r.json()
            return [
                {"rank": c.get("market_cap_rank"), "name": c.get("name"),
                 "symbol": c.get("symbol", "").upper(), "price": c.get("current_price"),
                 "market_cap": c.get("market_cap"), "volume_24h": c.get("total_volume"),
                 "change_24h_pct": c.get("price_change_percentage_24h"),
                 "high_24h": c.get("high_24h"), "low_24h": c.get("low_24h")}
                for c in coins
            ]

    async def fetch_trending(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/search/trending")
            if r.status_code != 200:
                return []
            coins = r.json().get("coins", [])
            return [
                {"rank": i + 1, "name": c["item"].get("name"), "symbol": c["item"].get("symbol"),
                 "price_btc": c["item"].get("price_btc"), "market_cap_rank": c["item"].get("market_cap_rank")}
                for i, c in enumerate(coins[:10])
            ]

    async def fetch_categories(self) -> list[dict]:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}/coins/categories")
            if r.status_code != 200:
                return []
            return [
                {"id": c.get("id"), "name": c.get("name"), "market_cap": c.get("market_cap"),
                 "volume_24h": c.get("volume_24h"), "change_24h_pct": c.get("market_cap_change_percentage_24h")}
                for c in r.json()[:30]
            ]
