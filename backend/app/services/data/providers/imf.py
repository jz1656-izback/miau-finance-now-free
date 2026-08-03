"""IMF Data Explorer — GDP, inflation, trade, debt, unemployment by country (free key)."""
import httpx
from typing import Optional
from datetime import datetime
from app.services.data.base import DataSource, ProviderUnavailableError


class IMFProvider(DataSource):
    """IMF data via Data Explorer API. Free key at https://www.imf.org/en/Data."""

    @property
    def name(self) -> str:
        return "imf"

    @property
    def requires_key(self) -> bool:
        return True

    @property
    def rate_limit_per_minute(self) -> int:
        return 60

    @property
    def base_url(self) -> str:
        return "https://www.imf.org/external/datamapper/api/v1"

    @property
    def capabilities(self) -> list[str]:
        return ["macro", "gdp", "inflation", "trade", "debt", "unemployment"]

    async def _get_key(self) -> str:
        from os import environ
        key = environ.get("IMF_API_KEY", "")
        if not key:
            from app.services.data.base import ConfigError
            raise ConfigError("IMF_API_KEY not set in environment")
        return key

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{self.base_url}/NGDP_RPCH/WEOWORLD")
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_gdp(self, country: str = "WEOWORLD", years: int = 5) -> list[dict]:
        """Real GDP growth (% change) for a country or region."""
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/NGDP_RPCH/{country.upper()}")
            if r.status_code != 200:
                raise ProviderUnavailableError(f"IMF GDP returned {r.status_code}")
            data = r.json().get("values", r.json().get("data", {}))
            if isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], dict) and "values" in data[key]:
                        data = data[key]["values"]
                        break
            if isinstance(data, dict):
                values = data.get(country.upper(), data)
            else:
                values = data
            if isinstance(values, dict):
                values = values.get("values", values)
            now = datetime.now().year
            return [
                {"date": str(year), "value": round(float(val), 2), "unit": "% change"}
                for year, val in (values if isinstance(values, dict) else {}).items()
                if abs(now - int(year)) <= years and val is not None
            ]

    async def fetch_inflation(self, country: str = "WEOWORLD", years: int = 5) -> list[dict]:
        """Inflation rate (CPI % change) for a country or region."""
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/PCPIPCH/{country.upper()}")
            if r.status_code != 200:
                raise ProviderUnavailableError(f"IMF inflation returned {r.status_code}")
            data = r.json().get("values", r.json().get("data", {}))
            if isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], dict) and "values" in data[key]:
                        data = data[key]["values"]
                        break
            if isinstance(data, dict):
                values = data.get(country.upper(), data)
            else:
                values = data
            if isinstance(values, dict):
                values = values.get("values", values)
            now = datetime.now().year
            return [
                {"date": str(year), "value": round(float(val), 2), "unit": "% change"}
                for year, val in (values if isinstance(values, dict) else {}).items()
                if abs(now - int(year)) <= years and val is not None
            ]

    async def fetch_unemployment(self, country: str = "WEOWORLD", years: int = 5) -> list[dict]:
        """Unemployment rate (% of labor force) for a country or region."""
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/LUR/{country.upper()}")
            if r.status_code != 200:
                raise ProviderUnavailableError(f"IMF unemployment returned {r.status_code}")
            data = r.json().get("values", r.json().get("data", {}))
            if isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], dict) and "values" in data[key]:
                        data = data[key]["values"]
                        break
            if isinstance(data, dict):
                values = data.get(country.upper(), data)
            else:
                values = data
            if isinstance(values, dict):
                values = values.get("values", values)
            now = datetime.now().year
            return [
                {"date": str(year), "value": round(float(val), 2), "unit": "% of labor force"}
                for year, val in (values if isinstance(values, dict) else {}).items()
                if abs(now - int(year)) <= years and val is not None
            ]

    async def fetch_trade_balance(self, country: str = "WEOWORLD", years: int = 5) -> list[dict]:
        """Trade balance (exports - imports, % of GDP) for a country or region."""
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/BCA_NGDPD/{country.upper()}")
            if r.status_code != 200:
                raise ProviderUnavailableError(f"IMF trade balance returned {r.status_code}")
            data = r.json().get("values", r.json().get("data", {}))
            if isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], dict) and "values" in data[key]:
                        data = data[key]["values"]
                        break
            if isinstance(data, dict):
                values = data.get(country.upper(), data)
            else:
                values = data
            if isinstance(values, dict):
                values = values.get("values", values)
            now = datetime.now().year
            return [
                {"date": str(year), "value": round(float(val), 2), "unit": "% of GDP"}
                for year, val in (values if isinstance(values, dict) else {}).items()
                if abs(now - int(year)) <= years and val is not None
            ]

    async def fetch_government_debt(self, country: str = "WEOWORLD", years: int = 5) -> list[dict]:
        """Government debt as % of GDP for a country or region."""
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/GGXWDG_NGDP/{country.upper()}")
            if r.status_code != 200:
                raise ProviderUnavailableError(f"IMF debt returned {r.status_code}")
            data = r.json().get("values", r.json().get("data", {}))
            if isinstance(data, dict):
                for key in data:
                    if isinstance(data[key], dict) and "values" in data[key]:
                        data = data[key]["values"]
                        break
            if isinstance(data, dict):
                values = data.get(country.upper(), data)
            else:
                values = data
            if isinstance(values, dict):
                values = values.get("values", values)
            now = datetime.now().year
            return [
                {"date": str(year), "value": round(float(val), 2), "unit": "% of GDP"}
                for year, val in (values if isinstance(values, dict) else {}).items()
                if abs(now - int(year)) <= years and val is not None
            ]
