"""FRED — Federal Reserve Economic Data: GDP, CPI, unemployment, interest rates, treasury yields."""
import httpx
from datetime import datetime
from typing import Optional
from app.services.data.base import DataSource, ProviderUnavailableError


class FREDProvider(DataSource):
    """Economic data from FRED (St. Louis Fed). Free key at https://fred.stlouisfed.org/docs/api/api_key.html."""

    @property
    def name(self) -> str:
        return "fred"

    @property
    def requires_key(self) -> bool:
        return True

    @property
    def rate_limit_per_minute(self) -> int:
        return 120

    @property
    def base_url(self) -> str:
        return "https://api.stlouisfed.org/fred"

    @property
    def capabilities(self) -> list[str]:
        return ["macro", "gdp", "cpi", "unemployment", "interest_rates", "treasury"]

    SERIES = {
        "GDP": "Gross Domestic Product", "CPIAUCSL": "Consumer Price Index",
        "UNRATE": "Unemployment Rate", "FEDFUNDS": "Federal Funds Rate",
        "DGS10": "10-Year Treasury", "DGS2": "2-Year Treasury",
        "DGS30": "30-Year Treasury", "T5YIE": "5-Year Breakeven Inflation",
        "M2SL": "M2 Money Supply", "PCE": "Personal Consumption Expenditures",
        "INDPRO": "Industrial Production", "HOUST": "Housing Starts",
        "UMCSENT": "Consumer Sentiment (UoM)", "PAYEMS": "Nonfarm Payrolls",
        "PPIACO": "Producer Price Index",
    }

    async def _get_key(self) -> str:
        from os import environ
        key = environ.get("FRED_API_KEY", "")
        if not key:
            from app.services.data.base import ConfigError
            raise ConfigError("FRED_API_KEY not set in environment")
        return key

    async def _test_connection(self) -> bool:
        try:
            key = await self._get_key()
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{self.base_url}/series/observations", params={"series_id": "GDP", "api_key": key, "file_type": "json", "limit": 1})
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_series(self, series_id: str, limit: int = 100) -> list[dict]:
        key = await self._get_key()
        params = {"series_id": series_id.upper(), "api_key": key, "file_type": "json", "sort_order": "desc", "limit": limit}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/series/observations", params=params)
            if r.status_code != 200:
                raise ProviderUnavailableError(f"FRED returned {r.status_code}")
            data = r.json().get("observations", [])
            return [
                {"date": o["date"], "value": float(o["value"]), "series_id": series_id.upper(),
                 "name": self.SERIES.get(series_id.upper(), series_id.upper())}
                for o in data if o.get("value") and o["value"] != "."
            ]

    async def list_series(self) -> list[dict]:
        return [{"id": k, "name": v} for k, v in self.SERIES.items()]

    async def fetch_gdp(self, limit: int = 80) -> list[dict]:
        return await self.fetch_series("GDP", limit)

    async def fetch_cpi(self, limit: int = 60) -> list[dict]:
        return await self.fetch_series("CPIAUCSL", limit)

    async def fetch_unemployment(self, limit: int = 60) -> list[dict]:
        return await self.fetch_series("UNRATE", limit)

    async def fetch_fed_rate(self, limit: int = 60) -> list[dict]:
        return await self.fetch_series("FEDFUNDS", limit)

    async def fetch_treasury_yield(self, maturity: str = "DGS10", limit: int = 60) -> list[dict]:
        return await self.fetch_series(maturity, limit)

    async def fetch_nonfarm_payrolls(self, limit: int = 60) -> list[dict]:
        return await self.fetch_series("PAYEMS", limit)
