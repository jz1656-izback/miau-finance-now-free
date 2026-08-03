"""SecuritiesDB API — quant data: Piotroski F-Score, Altman Z, DCF, ETF overlap, etc.

No key required. 100 req/min. Covers US equities.
"""
import logging
import time
import httpx
from typing import Optional
from app.services.data.base import DataSource
from app.services.data.models import QuantHealthScore, FairValue

logger = logging.getLogger(__name__)


class SecuritiesDBProvider(DataSource):
    """Free quant data from SecuritiesDB. No key needed."""

    @property
    def name(self) -> str:
        return "securitiesdb"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 100

    @property
    def base_url(self) -> str:
        return "https://securitiesdb.com/api/v1"

    @property
    def capabilities(self) -> list[str]:
        return [
            "quant_health", "dcf_valuation", "etf_analysis",
            "insider", "risk_factors", "fama_french",
            "passive_float", "earnings_transparency",
        ]

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self.base_url}/health")
                return r.status_code < 500
        except Exception:
            return False

    async def _get(self, path: str) -> dict:
        start = time.monotonic()
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}{path}", timeout=10)
            elapsed = round((time.monotonic() - start) * 1000, 1)
            if r.status_code != 200:
                logger.warning("SecuritiesDB %s returned %d (%sms)", path, r.status_code, elapsed)
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"SecuritiesDB HTTP {r.status_code} on {path}")
            logger.debug("SecuritiesDB %s OK (%sms)", path, elapsed)
            return r.json()

    async def fetch_quant_health(self, ticker: str) -> QuantHealthScore:
        data = await self._get(f"/stocks/{ticker.upper()}/quant-health")
        scores = data.get("data", {}).get("scores", {})
        return QuantHealthScore(
            ticker=ticker.upper(),
            piotroski_f_score=scores.get("piotroski_f"),
            altman_z_score=scores.get("altman_z"),
            beneish_m_score=scores.get("beneish_m"),
            roic_wacc_spread=scores.get("roic_wacc_spread"),
        )

    async def fetch_fair_value(self, ticker: str) -> FairValue:
        data = await self._get(f"/stocks/{ticker.upper()}/dcf")
        d = data.get("data", {})
        dcf = d.get("dcf", {})
        matrix = d.get("sensitivity_matrix")
        sm = matrix.get("fair_values") if matrix and "fair_values" in matrix else None
        return FairValue(
            ticker=ticker.upper(),
            fair_price=dcf.get("fair_value"),
            current_price=d.get("current_price"),
            upside_pct=dcf.get("upside_pct"),
            wacc=dcf.get("wacc"),
            sensitivity_matrix=sm,
        )

    async def fetch_etf_overlap(self, ticker: str) -> dict:
        return await self._get(f"/etf/{ticker.upper()}/overlap")

    async def fetch_etf_xray(self, ticker: str) -> dict:
        return await self._get(f"/etfs/{ticker.upper()}/xray")

    async def fetch_insider_activity(self, ticker: str) -> dict:
        return await self._get(f"/stocks/{ticker.upper()}/insider-activity")

    async def fetch_risk_factors(self, ticker: str) -> dict:
        return await self._get(f"/stocks/{ticker.upper()}/risk-factors")

    async def fetch_passive_float(self, ticker: str) -> dict:
        return await self._get(f"/stocks/{ticker.upper()}/passive-float")

    async def fetch_fama_french(self, ticker: str) -> dict:
        return await self._get(f"/stocks/{ticker.upper()}/fama-french")

    async def fetch_earnings_transparency(self, ticker: str) -> dict:
        return await self._get(f"/stocks/{ticker.upper()}/earnings-transparency")
