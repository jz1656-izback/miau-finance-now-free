"""DeFiLlama API — TVL, yields, DEX volumes, stablecoins, fees, bridges."""
import logging
import time
import httpx
from typing import Optional
from app.services.data.base import DataSource
from app.services.data.models import DefiProtocol, YieldPool

logger = logging.getLogger(__name__)


class DefiLlamaProvider(DataSource):
    """Free DeFi data from DeFiLlama. No key needed."""

    @property
    def name(self) -> str:
        return "defillama"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 300

    @property
    def base_url(self) -> str:
        return "https://api.llama.fi"

    @property
    def capabilities(self) -> list[str]:
        return ["defi"]

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self.base_url}/overview/ethereum")
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_tvl_overview(self) -> dict:
        start = time.monotonic()
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/chains")
            elapsed = round((time.monotonic() - start) * 1000, 1)
            if r.status_code != 200:
                logger.warning("DeFiLlama chains returned %d (%sms)", r.status_code, elapsed)
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"DeFiLlama chains returned {r.status_code}")
            logger.debug("DeFiLlama chains OK (%sms)", elapsed)
            chains = r.json()
            total_tvl = sum(float(c.get("tvl", 0)) for c in chains if c.get("tvl"))
            top = sorted(chains, key=lambda c: float(c.get("tvl", 0) or 0), reverse=True)[:10]
            return {
                "total_tvl": round(total_tvl, 1),
                "chains_count": len(chains),
                "top_chains": [{"name": c["name"], "tvl": round(float(c.get("tvl", 0)), 1)} for c in top],
            }

    async def fetch_protocols(self) -> list[DefiProtocol]:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/protocols")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"DeFiLlama protocols returned {r.status_code}")
            data = r.json()
            return [
                DefiProtocol(name=p.get("name", ""), chain=p.get("chain", "unknown"), tvl=float(p.get("tvl", 0) or 0), category=p.get("category", ""), change_24h=float(p.get("change_1h", 0)) if p.get("change_1h") else None)
                for p in (data or [])[:50]
            ]

    async def fetch_yields(self, min_apy: float = 0) -> list[YieldPool]:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get("https://yields.llama.fi/pools")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"DeFiLlama yields returned {r.status_code}")
            data = r.json()
            return [
                YieldPool(pool=p.get("pool", ""), chain=p.get("chain", ""), project=p.get("project", ""), apy=float(p.get("apy", 0)), tvl=float(p.get("tvlUsd", 0)), reward_tokens=p.get("rewardTokens"))
                for p in (data.get("data", []) or []) if float(p.get("apy", 0)) >= min_apy
            ][:50]

    async def fetch_stablecoins(self) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get("https://stablecoins.llama.fi/stablecoins")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"DeFiLlama stablecoins returned {r.status_code}")
            data = r.json()
            return data.get("peggedAssets", [])

    async def fetch_dex_volumes(self) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get("https://api.llama.fi/overview/dexs?excludeTotalDataChart=true")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"DeFiLlama dexs returned {r.status_code}")
            return r.json()

    async def fetch_fees(self) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get("https://api.llama.fi/overview/fees")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"DeFiLlama fees returned {r.status_code}")
            return r.json()
