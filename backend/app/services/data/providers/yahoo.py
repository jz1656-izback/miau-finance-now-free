"""Yahoo Finance provider — wraps existing _yf.py in the DataSource pattern."""
import logging
import time
from datetime import datetime, timezone
from app.services.data.base import DataSource, DataSourceError
from app.services.data.models import Quote
from app.services.analytics._yf import get_price, get_info, get_history

logger = logging.getLogger(__name__)


class YahooProvider(DataSource):
    @property
    def name(self) -> str:
        return "yahoo"

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return 30

    @property
    def capabilities(self) -> list[str]:
        return ["quote", "history", "fundamentals"]

    async def _test_connection(self) -> bool:
        try:
            result = await get_price("AAPL")
            return result is not None and result.get("price") is not None
        except Exception:
            return False

    async def fetch_quote(self, ticker: str) -> Quote:
        start = time.monotonic()
        data = await get_price(ticker.upper())
        elapsed = round((time.monotonic() - start) * 1000, 1)
        if not data or data.get("error"):
            logger.warning("Yahoo no data for %s (%sms): %s", ticker, elapsed, (data or {}).get("error", "empty"))
            raise DataSourceError(f"No data for {ticker}")
        logger.debug("Yahoo quote %s OK (%sms)", ticker, elapsed)
        # get_price() returns a flat schema: price / prev_close / change / change_pct
        price = float(data.get("price") or 0)
        prev_close = float(data.get("prev_close") or 0)
        change = float(data.get("change") or 0)
        change_pct = float(data.get("change_pct") or 0)
        return Quote(
            ticker=ticker.upper(),
            price=price,
            change=change,
            change_pct=change_pct,
            open=float(data.get("open") or 0) or None,
            high=float(data.get("high") or 0) or None,
            low=float(data.get("low") or 0) or None,
            volume=int(data.get("volume") or 0) or None,
            previous_close=prev_close or None,
            timestamp=datetime.now(timezone.utc),
        )

    async def fetch_history(self, ticker: str, period: str = "1mo", interval: str = "1d") -> list:
        data = await get_history(ticker.upper(), period, interval)
        if not data:
            raise DataSourceError(f"No history for {ticker}")
        return data

    async def fetch_fundamentals(self, ticker: str) -> dict:
        data = await get_info(ticker.upper())
        if not data:
            raise DataSourceError(f"No fundamentals for {ticker}")
        return data
