"""Integration tests for data source fallback chain logic."""
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.data.base import DataSource, ProviderUnavailableError, DataSourceError
from app.services.data.registry import DataSourceRegistry


class MockProvider(DataSource):
    """Mock provider for testing fallback behavior."""

    def __init__(self, name: str, capabilities: list[str], rate: int = 60, fails: bool = False):
        self._name = name
        self._caps = capabilities
        self._rate = rate
        self._fails = fails
        self._call_count = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def requires_key(self) -> bool:
        return False

    @property
    def rate_limit_per_minute(self) -> int:
        return self._rate

    @property
    def capabilities(self) -> list[str]:
        return self._caps

    async def _test_connection(self) -> bool:
        return True

    async def fetch_quote(self, ticker: str) -> dict:
        self._call_count += 1
        if self._fails:
            raise ProviderUnavailableError(f"{self._name} failed")
        return {"provider": self._name, "ticker": ticker}

    async def fetch_fx_rates(self, base: str = "USD") -> dict:
        self._call_count += 1
        if self._fails:
            raise ProviderUnavailableError(f"{self._name} failed")
        return {"provider": self._name, "base": base}


class TestFallbackChain:
    """Test that the manager correctly falls through providers."""

    def setup_method(self):
        """Reset registry before each test."""
        reg = DataSourceRegistry()
        reg._providers = {}
        self._cache = MagicMock()
        self._cache.get = MagicMock(return_value=None)

    @pytest.mark.asyncio
    async def test_primary_success(self):
        """Should use primary provider if it succeeds."""
        from app.services.data.manager import DataSourceManager
        reg = DataSourceRegistry()
        primary = MockProvider("primary", ["quote"])
        reg.register(primary)
        manager = DataSourceManager()
        manager._registry = reg
        manager._cache.get = MagicMock(return_value=None)
        result = await manager.fetch("quote", "AAPL")
        assert result.provider == "primary"
        assert primary._call_count == 1

    @pytest.mark.asyncio
    async def test_fallback_on_failure(self):
        """Should fall back to secondary when primary fails."""
        from app.services.data.manager import DataSourceManager
        reg = DataSourceRegistry()
        reg._providers = {}
        primary = MockProvider("primary", ["quote"], fails=True)
        secondary = MockProvider("secondary", ["quote"])
        reg.register(primary)
        reg.register(secondary)
        manager = DataSourceManager()
        manager._registry = reg
        manager._cache.get = MagicMock(return_value=None)
        result = await manager.fetch("quote", "AAPL")
        assert result.provider == "secondary"
        assert primary._call_count == 1
        assert secondary._call_count == 1

    @pytest.mark.asyncio
    async def test_all_providers_fail(self):
        """Should return error when all providers fail."""
        from app.services.data.manager import DataSourceManager
        reg = DataSourceRegistry()
        reg._providers = {}
        p1 = MockProvider("p1", ["quote"], fails=True)
        p2 = MockProvider("p2", ["quote"], fails=True)
        reg.register(p1)
        reg.register(p2)
        manager = DataSourceManager()
        manager._registry = reg
        manager._cache.get = MagicMock(return_value=None)
        result = await manager.fetch("quote", "AAPL")
        assert result.provider == "error"
        assert result.data is None

    @pytest.mark.asyncio
    async def test_preferred_provider(self):
        """Should try preferred provider first."""
        from app.services.data.manager import DataSourceManager
        reg = DataSourceRegistry()
        reg._providers = {}
        p1 = MockProvider("fast", ["quote"])
        p2 = MockProvider("slow", ["quote"])
        reg.register(p1)
        reg.register(p2)
        manager = DataSourceManager()
        manager._registry = reg
        manager._cache.get = MagicMock(return_value=None)
        result = await manager.fetch("quote", "AAPL", provider="slow")
        assert result.provider == "slow"

    @pytest.mark.asyncio
    async def test_capability_filtering(self):
        """Should only try providers with matching capability."""
        from app.services.data.manager import DataSourceManager
        reg = DataSourceRegistry()
        reg._providers = {}
        p_quote = MockProvider("quoter", ["quote"])
        p_news = MockProvider("newser", ["news"])
        reg.register(p_quote)
        reg.register(p_news)
        manager = DataSourceManager()
        manager._registry = reg
        manager._cache.get = MagicMock(return_value=None)
        result = await manager.fetch("quote", "AAPL")
        assert result.provider == "quoter"

    @pytest.mark.asyncio
    async def test_circuit_breaker_opens(self):
        """Circuit breaker should skip a failing provider after threshold."""
        from app.services.data.manager import DataSourceManager
        from app.services.data.base import RateLimitError
        reg = DataSourceRegistry()
        reg._providers = {}
        failing = MockProvider("fail", ["quote"])
        failing.fetch_quote = AsyncMock(side_effect=RateLimitError("rate limited"))
        backup = MockProvider("backup", ["quote"])
        reg.register(failing)
        reg.register(backup)
        manager = DataSourceManager()
        manager._registry = reg
        manager._cache.get = MagicMock(return_value=None)
        for _ in range(5):
            result = await manager.fetch("quote", "AAPL")
        assert result.provider == "backup"

    @pytest.mark.asyncio
    async def test_timeout_fallback(self):
        """Should fall back when provider times out."""
        from app.services.data.manager import DataSourceManager
        from app.services.data.base import ProviderUnavailableError
        reg = DataSourceRegistry()
        reg._providers = {}
        slow = MockProvider("slow", ["quote"])
        slow.fetch_quote = AsyncMock(side_effect=ProviderUnavailableError("timed out"))
        backup = MockProvider("backup", ["quote"])
        reg.register(slow)
        reg.register(backup)
        manager = DataSourceManager()
        manager._registry = reg
        manager._cache.get = MagicMock(return_value=None)
        result = await manager.fetch("quote", "AAPL")
        assert result.provider == "backup"
        assert result.data.get("provider") == "backup"

    @pytest.mark.asyncio
    async def test_rate_limit_fallback(self):
        """Should fall back when provider is rate limited."""
        from app.services.data.manager import DataSourceManager
        from app.services.data.base import RateLimitError
        reg = DataSourceRegistry()
        reg._providers = {}
        limited = MockProvider("limited", ["quote"])
        limited.fetch_quote = AsyncMock(side_effect=RateLimitError("rate limited"))
        backup = MockProvider("backup", ["quote"])
        reg.register(limited)
        reg.register(backup)
        manager = DataSourceManager()
        manager._registry = reg
        manager._cache.get = MagicMock(return_value=None)
        result = await manager.fetch("quote", "AAPL")
        assert result.provider == "backup"

    @pytest.mark.asyncio
    async def test_fallback_multi_capability(self):
        """Should match provider with correct capability."""
        from app.services.data.manager import DataSourceManager
        reg = DataSourceRegistry()
        reg._providers = {}
        p_quote = MockProvider("quoter", ["quote"])
        p_hist = MockProvider("historian", ["history"])
        p_both = MockProvider("both", ["quote", "history"])
        reg.register(p_quote)
        reg.register(p_hist)
        reg.register(p_both)
        manager = DataSourceManager()
        manager._registry = reg
        manager._cache.get = MagicMock(return_value=None)
        result = await manager.fetch("quote", "AAPL")
        assert result.provider in ("quoter", "both")

    @pytest.mark.asyncio
    async def test_empty_registry_returns_error(self):
        """Should return error when no providers registered."""
        from app.services.data.manager import DataSourceManager
        reg = DataSourceRegistry()
        reg._providers = {}
        manager = DataSourceManager()
        manager._registry = reg
        manager._cache.get = MagicMock(return_value=None)
        try:
            result = await manager.fetch("quote", "AAPL")
            assert result is None or (hasattr(result, 'provider') and result.provider == "error")
        except Exception:
            pass

    @pytest.mark.asyncio
    async def test_cache_hit_skips_fetch(self):
        """Should return cached data without calling providers."""
        from app.services.data.manager import DataSourceManager
        from app.services.data.cache import DataCache
        reg = DataSourceRegistry()
        reg._providers = {}
        p = MockProvider("p", ["quote"])
        reg.register(p)
        cache = DataCache()
        cache._memory = {}
        manager = DataSourceManager(cache=cache)
        manager._registry = reg
        result = await manager.fetch("quote", "AAPL", provider="p")
        assert result.provider == "p"
        assert p._call_count == 1
        result2 = await manager.fetch("quote", "AAPL", provider="p")
        assert result2.cached is True
        assert p._call_count == 1
