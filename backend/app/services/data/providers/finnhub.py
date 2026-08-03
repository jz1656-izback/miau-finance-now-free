"""Finnhub API — market data: quotes, candles, financials, news, SEC, insider, IPO, etc.

Free key (60 req/min) at https://finnhub.io
"""
import logging
import time
import httpx
from datetime import timezone, datetime
from typing import Optional
from app.config import settings
from app.services.data.base import DataSource
from app.services.data.models import Quote, OHLCV, Fundamentals

logger = logging.getLogger(__name__)


class FinnhubProvider(DataSource):
    """Market data from Finnhub.io. Requires API key."""

    @property
    def name(self) -> str:
        return "finnhub"

    @property
    def requires_key(self) -> bool:
        return True

    @property
    def rate_limit_per_minute(self) -> int:
        return 60

    @property
    def base_url(self) -> str:
        return "https://finnhub.io/api/v1"

    @property
    def capabilities(self) -> list[str]:
        return ["quote", "history", "fundamentals", "news", "insider", "short", "ipo", "ownership"]

    def _headers(self) -> dict:
        key = settings.finnhub_api_key
        if not key:
            from app.services.data.vault import get_key
            key = get_key("finnhub_api_key") or ""
        return {"X-Finnhub-Token": key}

    async def _test_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get(f"{self.base_url}/quote?symbol=AAPL", headers=self._headers())
                return r.status_code == 200
        except Exception:
            return False

    async def _get(self, path: str, params: dict = None) -> dict:
        start = time.monotonic()
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{self.base_url}{path}", params=params or {}, headers=self._headers())
            elapsed = round((time.monotonic() - start) * 1000, 1)
            if r.status_code == 429:
                logger.warning("Finnhub rate limit exceeded on %s", path)
                from app.services.data.base import RateLimitError
                raise RateLimitError("Finnhub rate limit exceeded")
            if r.status_code != 200:
                logger.warning("Finnhub %s returned %d (%sms)", path, r.status_code, elapsed)
                from app.services.data.base import ProviderUnavailableError
                raise ProviderUnavailableError(f"Finnhub {path} returned {r.status_code}")
            logger.debug("Finnhub %s OK (%sms)", path, elapsed)
            return r.json()

    async def fetch_quote(self, ticker: str) -> Quote:
        data = await self._get("/quote", {"symbol": ticker.upper()})
        return Quote(ticker=ticker.upper(), price=float(data.get("c", 0)), change=float(data.get("d", 0)), change_pct=float(data.get("dp", 0)), open=float(data["o"]) if data.get("o") else None, high=float(data["h"]) if data.get("h") else None, low=float(data["l"]) if data.get("l") else None, previous_close=float(data["pc"]) if data.get("pc") else None, volume=None, timestamp=datetime.now(timezone.utc))

    async def fetch_profile(self, ticker: str) -> dict:
        return await self._get("/stock/profile2", {"symbol": ticker.upper()})

    async def fetch_news(self, ticker: str, from_date: str = None, to_date: str = None) -> list[dict]:
        params = {"symbol": ticker.upper()}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return await self._get("/company-news", params)

    async def fetch_insider(self, ticker: str) -> list[dict]:
        data = await self._get("/stock/insider-transactions", {"symbol": ticker.upper(), "limit": 20})
        return data.get("data", [])

    async def fetch_short_interest(self, ticker: str) -> list[dict]:
        return await self._get("/stock/short-interest", {"symbol": ticker.upper()})

    async def fetch_ipo_calendar(self, from_date: str = None, to_date: str = None) -> list[dict]:
        params = {}
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        data = await self._get("/calendar/ipo", params)
        return data.get("ipoCalendar", [])

    async def fetch_ownership(self, ticker: str) -> list[dict]:
        data = await self._get("/stock/institutional-ownership", {"symbol": ticker.upper(), "limit": 20})
        return data.get("data", [])

    async def fetch_earnings(self, ticker: str) -> list[dict]:
        data = await self._get("/stock/earnings", {"symbol": ticker.upper(), "limit": 10})
        return data if isinstance(data, list) else []

    async def fetch_recommendations(self, ticker: str) -> list[dict]:
        data = await self._get("/stock/recommendation", {"symbol": ticker.upper()})
        return data if isinstance(data, list) else []

    async def fetch_price_target(self, ticker: str) -> dict:
        return await self._get("/stock/price-target", {"symbol": ticker.upper()})

    async def fetch_sec_filings(self, ticker: str) -> list[dict]:
        data = await self._get("/stock/filings", {"symbol": ticker.upper(), "limit": 10})
        return data if isinstance(data, list) else []

    async def fetch_market_news(self, category: str = "general") -> list[dict]:
        data = await self._get("/news", {"category": category})
        return data if isinstance(data, list) else []

    async def fetch_fundamentals(self, ticker: str) -> Fundamentals:
        data = await self._get("/stock/metric", {"symbol": ticker.upper(), "metric": "all"})
        metric = data.get("metric", {})
        return Fundamentals(ticker=ticker.upper(), company_name=None, market_cap=metric.get("marketCapitalization"), pe_ratio=metric.get("peAnnual"), eps=metric.get("epsAnnual"), dividend_yield=metric.get("dividendYieldIndicatedAnnual"), beta=metric.get("beta"), revenue=metric.get("revenueAnnual"), revenue_growth=metric.get("revenueGrowthAnnual"), profit_margin=metric.get("profitMargin"), debt_to_equity=metric.get("totalDebt/equity"), free_cash_flow=metric.get("freeCashFlowAnnual"))

    async def fetch_history(self, ticker: str, period: str = "1mo", interval: str = "D") -> list[OHLCV]:
        import time
        res_map = {"1d": "D", "1wk": "W", "1mo": "M", "1m": "1", "5m": "5", "15m": "15"}
        resolution = res_map.get(interval, "D")
        to_t = int(time.time())
        from_t = to_t - {"1d": 86400, "5d": 432000, "1mo": 2592000, "3mo": 7776000, "6mo": 15552000, "1y": 31536000}.get(period, 2592000)
        data = await self._get("/stock/candle", {"symbol": ticker.upper(), "resolution": resolution, "from": str(from_t), "to": str(to_t)})
        if data.get("s") != "ok":
            return []
        return [OHLCV(timestamp=datetime.fromtimestamp(data["t"][i]), open=float(data["o"][i]), high=float(data["h"][i]), low=float(data["l"][i]), close=float(data["c"][i]), volume=int(data["v"][i])) for i in range(len(data.get("t", [])))]
