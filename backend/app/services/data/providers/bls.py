"""Bureau of Labor Statistics API — CPI, PPI, employment, unemployment, wages.

Free key at https://data.bls.gov/registrationEngine
"""
import httpx
from typing import Optional
from app.config import settings
from app.services.data.base import DataSource
from app.services.data.models import MacroIndicator


class BLSProvider(DataSource):
    """Macroeconomic data from the US Bureau of Labor Statistics."""

    @property
    def name(self) -> str:
        return "bls"

    @property
    def requires_key(self) -> bool:
        return True

    @property
    def rate_limit_per_minute(self) -> int:
        return 30

    @property
    def base_url(self) -> str:
        return "https://api.bls.gov/publicAPI/v2"

    @property
    def capabilities(self) -> list[str]:
        return ["macro"]

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.post(f"{self.base_url}/timeseries/data/CUSR0000SA0", json={"registrationkey": __import__('app.services.data.vault', fromlist=['get_key']).get_key('bls_api_key') or settings.bls_api_key or "", "startyear": 2024, "endyear": 2024})
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_series(self, series_id: str, start_year: int = 2024, end_year: int = 2025) -> list[MacroIndicator]:
        payload = {
            "seriesid": [series_id],
            "startyear": str(start_year),
            "endyear": str(end_year),
            "registrationkey": __import__('app.services.data.vault', fromlist=['get_key']).get_key('bls_api_key') or settings.bls_api_key or "",
        }
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"{self.base_url}/timeseries/data", json=payload)
            if r.status_code != 200:
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"BLS returned {r.status_code}")
            data = r.json()
            results = []
            for series in data.get("Results", {}).get("series", []):
                for item in series.get("data", []):
                    results.append(MacroIndicator(
                        country="US",
                        indicator=series_id,
                        value=float(item.get("value", 0)),
                        change_yoy=None,
                        date=f"{item.get('year', '')}-{item.get('period', '').replace('M', '')}",
                    ))
            return results
