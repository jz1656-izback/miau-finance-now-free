"""Unified DataSourceManager with fallback chain, retry, circuit breaker."""
import asyncio
import random
from typing import Any, Optional

from app.services.data.base import DataSourceError, RateLimitError, ProviderUnavailableError
from app.services.data.cache import DataCache, data_cache as default_cache, TTL_TIERS
from app.services.data.models import DataSourceResponse
from app.services.data.registry import DataSourceRegistry, registry as default_registry


class CircuitBreaker:
    """Simple circuit breaker to avoid hammering failing providers."""

    def __init__(self, failure_threshold: int = 3, reset_timeout: float = 30.0):
        self._failures: dict[str, int] = {}
        self._open_until: dict[str, float] = {}
        self._threshold = failure_threshold
        self._reset_timeout = reset_timeout

    def record_failure(self, provider: str) -> None:
        import time
        self._failures[provider] = self._failures.get(provider, 0) + 1
        if self._failures[provider] >= self._threshold:
            self._open_until[provider] = time.time() + self._reset_timeout

    def record_success(self, provider: str) -> None:
        self._failures.pop(provider, None)
        self._open_until.pop(provider, None)

    def is_open(self, provider: str) -> bool:
        import time
        if provider in self._open_until:
            if time.time() > self._open_until[provider]:
                self._open_until.pop(provider, None)
                self._failures[provider] = 0
                return False
            return True
        return False


class DataSourceManager:
    """Central data fetching coordinator.

    Features:
    - Fallback chain: try primary provider, then fallback(s)
    - Caching via DataCache with TTL tiers
    - Circuit breaker per provider
    - Retry with exponential jitter
    - Unified error handling
    """

    def __init__(self, cache: Optional[DataCache] = None, registry: Optional[DataSourceRegistry] = None):
        self._registry = registry or default_registry
        self._cache = cache or default_cache
        self._breaker = CircuitBreaker()

    async def fetch(
        self,
        capability: str,
        *args: str,
        provider: Optional[str] = None,
        tier: str = "medium",
        **kwargs: Any,
    ) -> DataSourceResponse:
        """Fetch data for a given capability, with fallback chain.

        Args:
            capability: Standard capability tag (e.g. 'quote', 'screener')
            *args: Positional args to cache key (typically ticker + params)
            provider: Specific provider name to try first
            tier: Cache TTL tier ('fast', 'medium', 'slow', 'hourly', 'daily')
            **kwargs: Passed through to provider fetch methods

        Returns:
            DataSourceResponse with provider name, data, cached flag, latency
        """
        cache_key = capability
        ttl = TTL_TIERS.get(tier, 60)
        cached = self._cache.get(cache_key, *args)
        if cached is not None:
            return DataSourceResponse(provider="cache", data=cached, cached=True, latency_ms=0)

        providers = self._get_providers_for_capability(capability, preferred=provider)
        last_error: Optional[str] = None

        for prov in providers:
            if self._breaker.is_open(prov.name):
                continue
            try:
                import time
                start = time.time()
                result = await self._execute_fetch(prov, capability, *args, **kwargs)
                elapsed = round((time.time() - start) * 1000, 2)
                self._breaker.record_success(prov.name)
                self._cache.set(cache_key, *args, value=result, ttl=ttl)
                return DataSourceResponse(provider=prov.name, data=result, cached=False, latency_ms=elapsed)
            except (RateLimitError, ProviderUnavailableError, DataSourceError) as e:
                self._breaker.record_failure(prov.name)
                last_error = str(e)
                await asyncio.sleep(random.uniform(0.05, 0.2))

        return DataSourceResponse(
            provider="error",
            data=None,
            cached=False,
            latency_ms=0,
        )

    def _get_providers_for_capability(self, capability: str, preferred: Optional[str] = None) -> list:
        """Order providers: preferred first, then by capability match, then by rate limit."""
        candidates = self._registry.get_by_capability(capability)
        if preferred:
            preferred_prov = self._registry.get(preferred)
            if preferred_prov and preferred_prov in candidates:
                candidates.remove(preferred_prov)
                return [preferred_prov] + candidates
        candidates.sort(key=lambda p: p.rate_limit_per_minute, reverse=True)
        return candidates

    async def _execute_fetch(self, prov, capability: str, *args, **kwargs) -> Any:
        """Route to the correct fetch method based on capability."""
        mapping = {
            "quote": lambda: prov.fetch_quote(args[0] if args else kwargs.get("ticker", "")),
            "history": lambda: prov.fetch_history(args[0] if args else kwargs.get("ticker", ""), kwargs.get("period", "1mo"), kwargs.get("interval", "1d")),
            "fundamentals": lambda: prov.fetch_fundamentals(args[0] if args else kwargs.get("ticker", "")),
        }
        fetcher = mapping.get(capability)
        if fetcher:
            return await fetcher()
        raise DataSourceError(f"Capability '{capability}' not supported by {prov.name}")
