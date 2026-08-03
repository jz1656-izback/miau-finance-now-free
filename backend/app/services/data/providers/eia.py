"""EIA API — oil, gas, coal, electricity, renewable energy data from the US Energy Information Administration."""
import httpx
from typing import Optional
from datetime import datetime
from app.services.data.base import DataSource, ProviderUnavailableError
from app.services.data.models import OHLCV


class EIAProvider(DataSource):
    """Energy data from EIA. Free key at https://www.eia.gov/opendata/register.php."""

    @property
    def name(self) -> str:
        return "eia"

    @property
    def requires_key(self) -> bool:
        return True

    @property
    def rate_limit_per_minute(self) -> int:
        return 30

    @property
    def base_url(self) -> str:
        return "https://api.eia.gov/v2"

    @property
    def capabilities(self) -> list[str]:
        return ["energy", "oil", "gas", "coal", "electricity", "renewable"]

    async def _get_key(self) -> str:
        from os import environ
        key = environ.get("EIA_API_KEY", "")
        if not key:
            from app.services.data.base import ConfigError
            raise ConfigError("EIA_API_KEY not set in environment")
        return key

    async def _test_connection(self) -> bool:
        try:
            key = await self._get_key()
            async with httpx.AsyncClient(timeout=10) as client:
                r = await client.get(f"{self.base_url}/petroleum/crd/crdpimp/data/?api_key={key}&length=1")
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_oil_prices(self, period: str = "1y") -> list[dict]:
        """Weekly Cushing, OK WTI spot price."""
        key = await self._get_key()
        params = {"api_key": key, "frequency": "weekly", "data[0]": "value", "sort[0][column]": "period", "sort[0][direction]": "desc"}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/petroleum/pri/spt/data/", params=params)
            if r.status_code != 200:
                raise ProviderUnavailableError(f"EIA oil prices returned {r.status_code}")
            data = r.json().get("response", {}).get("data", [])
            return [
                {"date": d["period"], "price": float(d.get("value", 0)), "unit": "USD/barrel"}
                for d in data if d.get("value")
            ]

    async def fetch_gas_prices(self, period: str = "1y") -> list[dict]:
        """Weekly US regular gasoline price."""
        key = await self._get_key()
        params = {"api_key": key, "frequency": "weekly", "data[0]": "value", "sort[0][column]": "period", "sort[0][direction]": "desc"}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/petroleum/pri/gnd/data/", params=params)
            if r.status_code != 200:
                raise ProviderUnavailableError(f"EIA gas prices returned {r.status_code}")
            data = r.json().get("response", {}).get("data", [])
            return [
                {"date": d["period"], "price": float(d.get("value", 0)), "unit": "USD/gallon"}
                for d in data if d.get("value")
            ]

    async def fetch_natural_gas(self, period: str = "1y") -> list[dict]:
        """Weekly US natural gas price."""
        key = await self._get_key()
        params = {"api_key": key, "frequency": "weekly", "data[0]": "value", "sort[0][column]": "period", "sort[0][direction]": "desc"}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/naturalgas/pri/fut/data/", params=params)
            if r.status_code != 200:
                raise ProviderUnavailableError(f"EIA natural gas returned {r.status_code}")
            data = r.json().get("response", {}).get("data", [])
            return [
                {"date": d["period"], "price": float(d.get("value", 0)), "unit": "USD/MMBtu"}
                for d in data if d.get("value")
            ]

    async def fetch_coal(self, period: str = "1y") -> list[dict]:
        """Weekly coal production and price."""
        key = await self._get_key()
        params = {"api_key": key, "frequency": "weekly", "data[0]": "value", "sort[0][column]": "period", "sort[0][direction]": "desc"}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/coal/prod/data/", params=params)
            if r.status_code != 200:
                raise ProviderUnavailableError(f"EIA coal returned {r.status_code}")
            data = r.json().get("response", {}).get("data", [])
            return [
                {"date": d["period"], "value": float(d.get("value", 0)), "unit": "short tons"}
                for d in data if d.get("value")
            ]

    async def fetch_electricity(self, period: str = "1y") -> list[dict]:
        """Weekly US electricity generation by source."""
        key = await self._get_key()
        params = {"api_key": key, "frequency": "weekly", "data[0]": "value", "sort[0][column]": "period", "sort[0][direction]": "desc"}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/electricity/rto/region-data/data/", params=params)
            if r.status_code != 200:
                raise ProviderUnavailableError(f"EIA electricity returned {r.status_code}")
            data = r.json().get("response", {}).get("data", [])
            return [
                {"date": d["period"], "value": float(d.get("value", 0)), "type": d.get("type-name", ""), "unit": "MWh"}
                for d in data if d.get("value")
            ]

    async def fetch_renewable(self, period: str = "1y") -> list[dict]:
        """Monthly renewable energy generation."""
        key = await self._get_key()
        params = {"api_key": key, "frequency": "monthly", "data[0]": "value", "sort[0][column]": "period", "sort[0][direction]": "desc"}
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/total/data/", params=params)
            if r.status_code != 200:
                raise ProviderUnavailableError(f"EIA renewable returned {r.status_code}")
            data = r.json().get("response", {}).get("data", [])
            return [
                {"date": d["period"], "value": float(d.get("value", 0)), "source": d.get("series-description", ""), "unit": "MWh"}
                for d in data if d.get("value")
            ]
