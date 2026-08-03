"""Mobula API — on-chain wallet portfolio, token prices, DeFi positions. Free key at https://mobula.io."""
import httpx
from typing import Optional
from app.services.data.base import DataSource, ProviderUnavailableError


class MobulaProvider(DataSource):
    """On-chain data from Mobula. Free tier: 100 req/min with API key."""

    @property
    def name(self) -> str:
        return "mobula"

    @property
    def requires_key(self) -> bool:
        return True

    @property
    def rate_limit_per_minute(self) -> int:
        return 100

    @property
    def base_url(self) -> str:
        return "https://api.mobula.io/api/1"

    @property
    def capabilities(self) -> list[str]:
        return ["wallet", "defi", "token", "nft", "onchain"]

    async def _get_key(self) -> str:
        from os import environ
        key = environ.get("MOBULA_API_KEY", "")
        if not key:
            from app.services.data.base import ConfigError
            raise ConfigError("MOBULA_API_KEY not set in environment")
        return key

    async def _test_connection(self) -> bool:
        try:
            key = await self._get_key()
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{self.base_url}/metadata", params={"symbol": "Mobula"}, headers={"Authorization": key})
                return r.status_code == 200
        except Exception:
            return False

    async def _get(self, path: str, params: dict = None) -> dict:
        key = await self._get_key()
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}{path}", params=params or {}, headers={"Authorization": key})
            if r.status_code == 429:
                raise ProviderUnavailableError("Mobula rate limit exceeded")
            if r.status_code != 200:
                raise ProviderUnavailableError(f"Mobula returned {r.status_code}")
            return r.json()

    async def fetch_wallet_portfolio(self, wallet: str) -> dict:
        """Full wallet portfolio with token balances, values, and P&L."""
        data = await self._get("/wallet/portfolio", {"wallet": wallet})
        return {
            "wallet": wallet,
            "total_value_usd": data.get("totalValue", data.get("total_usd", 0)),
            "total_cost_usd": data.get("totalCost", data.get("total_cost", 0)),
            "pnl_usd": data.get("pnl", 0),
            "pnl_pct": data.get("pnlPercent", data.get("pnl_pct", 0)),
            "positions": data.get("assets", data.get("positions", [])),
            "chains": data.get("chains", []),
        }

    async def fetch_wallet_nfts(self, wallet: str) -> list[dict]:
        """NFT holdings for a wallet."""
        data = await self._get("/wallet/nfts", {"wallet": wallet})
        nfts = data.get("nfts", data.get("data", []))
        return [
            {"collection": n.get("collection", n.get("name", "")),
             "token_id": n.get("tokenId", n.get("token_id", "")),
             "name": n.get("name", ""), "floor_price": n.get("floorPrice", n.get("floor_price", 0)),
             "estimated_value": n.get("estimatedValue", n.get("estimated_value", 0)),
             "image": n.get("image", n.get("image_url", "")), "chain": n.get("chain", "")}
            for n in nfts
        ]

    async def fetch_token_price(self, symbol: str = "ETH") -> dict:
        """Current price and market data for a token."""
        data = await self._get("/metadata", {"symbol": symbol.upper()})
        return {
            "symbol": symbol.upper(),
            "name": data.get("name", ""),
            "price": data.get("price", data.get("current_price", 0)),
            "market_cap": data.get("marketCap", data.get("market_cap", 0)),
            "volume_24h": data.get("volume24h", data.get("volume_24h", 0)),
            "change_24h_pct": data.get("priceChange24h", data.get("change_24h", 0)),
            "supply": data.get("supply", data.get("circulating_supply", 0)),
        }

    async def fetch_defi_positions(self, wallet: str) -> list[dict]:
        """DeFi positions (lending, LP, staking) for a wallet."""
        data = await self._get("/wallet/defi", {"wallet": wallet})
        positions = data.get("positions", data.get("data", []))
        return [
            {"protocol": p.get("protocol", p.get("name", "")),
             "type": p.get("type", ""), "asset": p.get("asset", ""),
             "amount": p.get("amount", 0), "value_usd": p.get("valueUsd", p.get("value_usd", 0)),
             "apy": p.get("apy", 0), "chain": p.get("chain", "")}
            for p in positions
        ]

    async def fetch_historical_prices(self, symbol: str, days: int = 30) -> list[dict]:
        """Historical token prices."""
        data = await self._get("/historical", {"symbol": symbol.upper(), "period": f"{days}d"})
        points = data.get("prices", data.get("data", {}).get("prices", data.get("data", [])))
        if isinstance(points, dict):
            points = [{"timestamp": k, "price": v} for k, v in points.items()]
        return [
            {"date": str(p.get("timestamp", p.get("date", "")))[:10],
             "price": p.get("price", p.get("close", 0))}
            for p in (points or [])
        ]
