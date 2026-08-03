"""Abstract base class for all data source providers."""
from abc import ABC, abstractmethod
from typing import Any, Optional
from app.services.data.models import Quote, OHLCV, Fundamentals, HealthStatus


class DataSourceError(Exception):
    """Raised when a data source fails to fetch data."""


class RateLimitError(DataSourceError):
    """Raised when the upstream API rate limit is exceeded."""


class ProviderUnavailableError(DataSourceError):
    """Raised when the upstream API is unreachable or returns 5xx."""


class DataSource(ABC):
    """Abstract base for every data source provider in Miau Finance.

    Each provider wraps one upstream API (Finnhub, SecuritiesDB, etc.)
    and implements the methods below. Providers are auto-registered in
    the DataSourceRegistry.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique slug identifier, e.g. 'finnhub', 'securitiesdb', 'frankfurter'."""

    @property
    @abstractmethod
    def requires_key(self) -> bool:
        """True if this provider needs an API key configured in Settings."""

    @property
    @abstractmethod
    def rate_limit_per_minute(self) -> int:
        """Maximum requests per minute for the free tier."""

    def _ensure_tracking(self) -> None:
        if not hasattr(self, '_request_count'):
            self._request_count = 0
            self._last_request_time = 0.0
            self._error_count = 0
            self._success_count = 0
            self._total_latency_ms = 0.0

    def _track_request(self, latency_ms: float, success: bool = True) -> None:
        """Track a request for rate limit and health monitoring."""
        self._ensure_tracking()
        import time
        now = time.time()
        if now - self._last_request_time > 60:
            self._request_count = 0
        self._request_count += 1
        self._last_request_time = now
        self._total_latency_ms += latency_ms
        if success:
            self._success_count += 1
        else:
            self._error_count += 1

    @property
    def remaining_quota(self) -> int:
        """Estimated remaining requests in the current window."""
        self._ensure_tracking()
        return max(0, self.rate_limit_per_minute - self._request_count)

    @property
    def stats(self) -> dict:
        self._ensure_tracking()
        return {
            "name": self.name,
            "requires_key": self.requires_key,
            "rate_limit": self.rate_limit_per_minute,
            "remaining_quota": self.remaining_quota,
            "success_count": self._success_count,
            "error_count": self._error_count,
            "avg_latency_ms": round(self._total_latency_ms / max(self._success_count + self._error_count, 1), 1),
        }

    @property
    def base_url(self) -> str:
        """Override in subclass with the upstream API base URL."""
        return ""

    @property
    def capabilities(self) -> list[str]:
        """List of capabilities this provider supports.

        Standard capability tags:
        - 'quote' — real-time stock/asset price
        - 'history' — historical OHLCV data
        - 'fundamentals' — company financials
        - 'news' — company/market news
        - 'screener' — stock screening/filters
        - 'insider' — insider transactions
        - 'short' — short interest data
        - 'ipo' — IPO calendar
        - 'ownership' — institutional ownership
        - 'etf_analysis' — ETF holdings/overlap
        - 'quant_health' — Piotroski/Altman Z scores
        - 'dcf_valuation' — DCF fair value
        - 'fx' — forex exchange rates
        - 'macro' — economic indicators
        - 'crypto' — cryptocurrency data
        - 'defi' — DeFi protocol data (TVL, yields)
        - 'gas' — blockchain gas prices
        - 'technical' — technical indicators
        - 'sector' — sector performance
        - 'options' — options chain data
        """
        return []

    async def health(self) -> HealthStatus:
        """Check if the upstream API is reachable.

        Returns a HealthStatus with latency, status, and optional error.
        Default implementation returns Healthy if self._test_connection succeeds.
        """
        try:
            start = __import__('time').time()
            ok = await self._test_connection()
            elapsed = __import__('time').time() - start
            if ok:
                return HealthStatus(provider=self.name, healthy=True, latency_ms=round(elapsed * 1000))
            return HealthStatus(provider=self.name, healthy=False, error="Connection test returned False")
        except Exception as e:
            return HealthStatus(provider=self.name, healthy=False, error=str(e))

    @abstractmethod
    async def _test_connection(self) -> bool:
        """Quick connectivity check. Called by health()."""

    async def fetch_quote(self, ticker: str) -> Quote:
        """Fetch real-time quote for a ticker. Raise DataSourceError on failure."""
        raise NotImplementedError(f"{self.name} does not support quote")

    async def fetch_history(self, ticker: str, period: str = "1mo", interval: str = "1d") -> list[OHLCV]:
        """Fetch historical OHLCV data."""
        raise NotImplementedError(f"{self.name} does not support history")

    async def fetch_fundamentals(self, ticker: str) -> Fundamentals:
        """Fetch company fundamentals."""
        raise NotImplementedError(f"{self.name} does not support fundamentals")
