"""Blocknative — gas prices for 40+ chains (Ethereum, L2s, L1s)."""
import httpx
from typing import Optional
from app.services.data.base import DataSource
from app.services.data.models import GasPrices


class BlocknativeProvider(DataSource):
    """Gas price data from Blocknative. Works without a key."""

    @property
    def name(self) -> str:
        return "blocknative"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 30

    @property
    def base_url(self) -> str:
        return "https://api.blocknative.com/gas"

    @property
    def capabilities(self) -> list[str]:
        return ["gas"]

    _chains: dict[int, str] = {
        1: "ethereum-mainnet",
        10: "optimism",
        56: "bsc",
        100: "gnosis",
        137: "polygon",
        250: "fantom",
        42161: "arbitrum",
        43114: "avalanche",
    }

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get("https://api.blocknative.com/gasprices/blockprices")
                return r.status_code in (200, 429)
        except Exception:
            return False

    async def fetch_gas(self, chain_id: int = 1) -> GasPrices:
        chain_name = self._chains.get(chain_id, "ethereum-mainnet")
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://api.blocknative.com/gasprices/blockprices")
            if r.status_code == 429:
                from app.services.data.base import RateLimitError
                raise RateLimitError("Blocknative rate limit")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"Blocknative returned {r.status_code}")
            data = r.json()
            bp = data.get("blockPrices", [{}])[0] if data.get("blockPrices") else {}
            prices = bp.get("estimatedPrices", [{}])[0] if bp.get("estimatedPrices") else {}
            return GasPrices(
                chain=chain_name,
                safe_gwei=float(prices.get(1, 0)),
                propose_gwei=float(prices.get(2, 0)),
                fast_gwei=float(prices.get(3, 0)),
                base_fee=float(bp.get("baseFee", 0)) if bp.get("baseFee") else None,
            )

    async def fetch_gas_all(self) -> list[GasPrices]:
        results = []
        for chain_id in self._chains:
            try:
                results.append(await self.fetch_gas(chain_id))
            except Exception:
                pass
        return results
