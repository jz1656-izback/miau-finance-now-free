"""Corporate bonds — IG/HY yields, spreads, ratings via FRED."""
import httpx
from datetime import datetime
from app.services.data.base import DataSource, ProviderUnavailableError


class CorporateBondsProvider(DataSource):
    """Corporate bond yields and spreads by rating (AAA through CCC).

    Powered by FRED API — ICE BofA US Corporate Bond Indices.
    """

    @property
    def name(self) -> str:
        return "corporate_bonds"

    @property
    def requires_key(self) -> bool:
        return True

    @property
    def rate_limit_per_minute(self) -> int:
        return 60

    @property
    def base_url(self) -> str:
        return "https://api.stlouisfed.org/fred"

    @property
    def capabilities(self) -> list[str]:
        return ["corporate_bond_yields", "bond_spreads"]

    # ICE BofA US Corporate Bond Yield series IDs
    BOND_SERIES = {
        "AAA": "BAMLC0A0CM",
        "AA": "BAMLCC0A0CM",
        "A": "BAMLC0A1CAA",
        "BBB": "BAMLC0A4YBBB",
        "BB": "BAMLH0A0HYM2",
        "B": "BAMLH0A1HYM2",
        "CCC": "BAMLH0A3HYM",
        "IG_OAS": "BAMLC0A0CM",      # Investment Grade OAS
        "HY_OAS": "BAMLH0A0HYM2",    # High Yield OAS
    }

    TREASURY_SERIES = {
        "10Y": "DGS10",
        "2Y": "DGS2",
    }

    async def _fetch_fred_series(self, series_id: str) -> dict | None:
        api_key = self._get_key()
        if not api_key:
            return None
        url = f"{self.base_url}/series/observations"
        params = {
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": 2,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            raise ProviderUnavailableError(f"FRED returned {resp.status_code} for {series_id}")
        data = resp.json()
        obs = data.get("observations", [])
        if not obs:
            return None
        latest = obs[0]
        return {
            "series_id": series_id,
            "date": latest.get("date"),
            "value": latest.get("value"),
        }

    async def _test_connection(self) -> bool:
        """Test by fetching AAA yield."""
        try:
            data = await self._fetch_fred_series(self.BOND_SERIES["AAA"])
            return data is not None and data.get("value") != "."
        except Exception:
            return False

    async def fetch_bond_yields(self) -> list[dict]:
        """Fetch latest yields for all corporate bond ratings."""
        results = []
        for rating, series_id in self.BOND_SERIES.items():
            data = await self._fetch_fred_series(series_id)
            if data and data.get("value") and data["value"] != ".":
                results.append({
                    "rating": rating,
                    "yield": float(data["value"]),
                    "date": data["date"],
                    "series_id": series_id,
                })
        return results

    async def fetch_spreads(self) -> list[dict]:
        """Calculate credit spreads over Treasuries."""
        yields = await self.fetch_bond_yields()
        treasury_10y = await self._fetch_fred_series(self.TREASURY_SERIES["10Y"])
        treasury_2y = await self._fetch_fred_series(self.TREASURY_SERIES["2Y"])
        treasury_10y_val = float(treasury_10y["value"]) if treasury_10y and treasury_10y.get("value") != "." else 0
        treasury_2y_val = float(treasury_2y["value"]) if treasury_2y and treasury_2y.get("value") != "." else 0

        spreads = []
        for item in yields:
            spread_10y = item["yield"] - treasury_10y_val if treasury_10y_val > 0 else 0
            spread_2y = item["yield"] - treasury_2y_val if treasury_2y_val > 0 else 0
            spreads.append({
                "rating": item["rating"],
                "yield": item["yield"],
                "spread_10y": round(spread_10y, 2),
                "spread_2y": round(spread_2y, 2),
            })
        return spreads

    async def fetch(self, query: str | None = None, **kwargs) -> dict:
        """Fetch all bond data."""
        try:
            yields = await self.fetch_bond_yields()
            spreads = await self.fetch_spreads()
            return {
                "bond_yields": yields,
                "credit_spreads": spreads,
                "updated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            raise ProviderUnavailableError(f"Corporate bonds fetch failed: {e}")
