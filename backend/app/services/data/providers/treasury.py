"""Treasury — US Treasury yields, TIPS, auctions, and central bank rates via FRED."""
import httpx
from datetime import datetime
from typing import Optional
from app.services.data.base import DataSource, ProviderUnavailableError


class TreasuryProvider(DataSource):
    """US Treasury data: yield curve, TIPS breakevens, SOFR, EFFR, IORB, auctions.

    Powered by FRED API (St. Louis Fed) + US Treasury auction feed.
    """

    @property
    def name(self) -> str:
        return "treasury"

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
        return ["fixed_income", "treasury", "rates", "yields", "central_bank", "tips"]

    YIELD_CURVE_SERIES: dict[str, str] = {
        "DGS1MO": "1-Month Treasury",
        "DGS3MO": "3-Month Treasury",
        "DGS6MO": "6-Month Treasury",
        "DGS1": "1-Year Treasury",
        "DGS2": "2-Year Treasury",
        "DGS3": "3-Year Treasury",
        "DGS5": "5-Year Treasury",
        "DGS7": "7-Year Treasury",
        "DGS10": "10-Year Treasury",
        "DGS20": "20-Year Treasury",
        "DGS30": "30-Year Treasury",
    }

    TIPS_SERIES: dict[str, str] = {
        "DFII5": "5-Year TIPS Yield",
        "DFII10": "10-Year TIPS Yield",
        "DFII30": "30-Year TIPS Yield",
    }

    RATE_SERIES: dict[str, str] = {
        "EFFR": "Effective Federal Funds Rate",
        "SOFR": "Secured Overnight Financing Rate",
        "IORB": "Interest on Reserve Balances",
        "DPCREDIT": "Discount Window Primary Credit",
        "T5YIE": "5-Year Breakeven Inflation Rate",
        "T10YIE": "10-Year Breakeven Inflation Rate",
        "T5YIFR": "5-Year Forward Inflation Expectation Rate",
        "TEDRATE": "TED Spread",
        "BAMLH0A0HYM2": "ICE BofA US High Yield Index Option-Adjusted Spread",
    }

    MORTGAGE_SERIES: dict[str, str] = {
        "MORTGAGE30US": "30-Year Fixed Rate Mortgage Average",
        "MORTGAGE15US": "15-Year Fixed Rate Mortgage Average",
        "MORTGAGE5US": "5/1-Year Adjustable Rate Mortgage Average",
        "OBMMIC30YF": "30-Year Fixed Rate Conforming Mortgage Index",
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
                r = await client.get(
                    f"{self.base_url}/series/observations",
                    params={"series_id": "DGS10", "api_key": key, "file_type": "json", "limit": 1},
                )
                return r.status_code == 200
        except Exception:
            return False

    async def fetch_series(self, series_id: str, limit: int = 30) -> list[dict]:
        key = await self._get_key()
        params = {
            "series_id": series_id.upper(), "api_key": key, "file_type": "json",
            "sort_order": "desc", "limit": limit,
        }
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base_url}/series/observations", params=params)
            if r.status_code != 200:
                raise ProviderUnavailableError(f"FRED returned {r.status_code}")
            data = r.json().get("observations", [])
            all_series = {**self.YIELD_CURVE_SERIES, **self.TIPS_SERIES, **self.RATE_SERIES, **self.MORTGAGE_SERIES}
            return [
                {"date": o["date"], "value": float(o["value"]), "series_id": series_id.upper(),
                 "name": all_series.get(series_id.upper(), series_id.upper())}
                for o in data if o.get("value") and o["value"] != "."
            ]

    async def fetch_yield_curve(self) -> list[dict]:
        results = []
        for sid in self.YIELD_CURVE_SERIES:
            try:
                points = await self.fetch_series(sid, limit=1)
                if points:
                    results.append(points[0])
            except Exception:
                continue
        return sorted(results, key=lambda x: float("inf") if x["value"] is None else float(x["value"]))

    async def fetch_treasury_yields(self, limit: int = 60) -> list[dict]:
        return await self.fetch_series("DGS10", limit)

    async def fetch_tips_yields(self, limit: int = 60) -> list[dict]:
        return await self.fetch_series("DFII10", limit)

    async def fetch_tips_breakevens(self, limit: int = 60) -> list[dict]:
        return await self.fetch_series("T10YIE", limit)

    async def fetch_yield_curve_history(self, maturity: str = "DGS10", days: int = 365) -> list[dict]:
        return await self.fetch_series(maturity, limit=days)

    async def fetch_effr(self, limit: int = 30) -> list[dict]:
        return await self.fetch_series("EFFR", limit)

    async def fetch_sofr(self, limit: int = 30) -> list[dict]:
        return await self.fetch_series("SOFR", limit)

    async def fetch_iorb(self, limit: int = 30) -> list[dict]:
        return await self.fetch_series("IORB", limit)

    async def fetch_mortgage_rates(self) -> list[dict]:
        results = []
        for sid in self.MORTGAGE_SERIES:
            try:
                points = await self.fetch_series(sid, limit=1)
                if points:
                    results.append(points[0])
            except Exception:
                continue
        return results
