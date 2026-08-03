"""Etherscan Gas Tracker — SafeGasPrice, ProposeGasPrice, FastGasPrice.

Free key at https://etherscan.io/register
"""
import httpx
from app.config import settings
from app.services.data.base import DataSource
from app.services.data.models import GasPrices


class EtherscanProvider(DataSource):
    """Gas price data from Etherscan. Requires free API key."""

    @property
    def name(self) -> str:
        return "etherscan"

    @property
    def requires_key(self) -> bool:
        return True

    @property
    def rate_limit_per_minute(self) -> int:
        return 5

    @property
    def base_url(self) -> str:
        return "https://api.etherscan.io/api"

    @property
    def capabilities(self) -> list[str]:
        return ["gas"]

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self.base_url}?module=gastracker&action=gasoracle&apikey={'test'}")
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_gas_oracle(self) -> GasPrices:
        key = __import__('app.services.data.vault', fromlist=['get_key']).get_key('etherscan_api_key') or settings.etherscan_api_key or ""
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}?module=gastracker&action=gasoracle&apikey={key}")
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"Etherscan returned {r.status_code}")
            data = r.json()
            result = data.get("result", {})
            return GasPrices(
                chain="ethereum-mainnet",
                safe_gwei=float(result.get("SafeGasPrice", 0)),
                propose_gwei=float(result.get("ProposeGasPrice", 0)),
                fast_gwei=float(result.get("FastGasPrice", 0)),
                base_fee=None,
            )
