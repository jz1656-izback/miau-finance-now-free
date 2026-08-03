"""Unit tests for data source layer: base, registry, cache, circuit breaker, manager."""
import pytest
import time
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.data.base import DataSource, DataSourceError, RateLimitError, ProviderUnavailableError
from app.services.data.registry import DataSourceRegistry
from app.services.data.cache import DataCache
from app.services.data.manager import CircuitBreaker, DataSourceManager
from app.services.data.models import DataSourceResponse


# ── Helpers ─────────────────────────────────────────────────────

class MockDataSource(DataSource):
    """Minimal concrete DataSource for testing the base class."""

    def __init__(self, name: str = "mock", requires_key: bool = False,
                 rate_limit: int = 60, capabilities: list[str] | None = None):
        self._name = name
        self._req_key = requires_key
        self._rate = rate_limit
        self._caps = capabilities or []
        self.call_count = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def requires_key(self) -> bool:
        return self._req_key

    @property
    def rate_limit_per_minute(self) -> int:
        return self._rate

    @property
    def capabilities(self) -> list[str]:
        return self._caps

    async def _test_connection(self) -> bool:
        return True

    async def fetch_quote(self, ticker: str) -> dict:
        self.call_count += 1
        return {"provider": self._name, "ticker": ticker}


# ── 1. DataSource Base Class ───────────────────────────────────

class TestDataSourceBase:

    def test_cannot_instantiate_abstract(self):
        """Should raise TypeError when instantiating DataSource directly."""
        with pytest.raises(TypeError):
            DataSource()

    def test_concrete_subclass(self):
        """A concrete subclass with all abstract methods works."""
        ds = MockDataSource()
        assert ds.name == "mock"
        assert ds.base_url == ""
        assert ds.capabilities == []

    def test_stats_tracking(self):
        ds = MockDataSource()
        assert ds.stats["name"] == "mock"
        assert ds.stats["remaining_quota"] == 60
        assert ds.stats["success_count"] == 0
        assert ds.stats["error_count"] == 0
        ds._track_request(50.0, success=True)
        assert ds.stats["success_count"] == 1
        assert ds.stats["avg_latency_ms"] == 50.0
        ds._track_request(100.0, success=False)
        assert ds.stats["error_count"] == 1
        assert ds.stats["avg_latency_ms"] == 75.0

    def test_remaining_quota(self):
        ds = MockDataSource(rate_limit=10)
        assert ds.remaining_quota == 10
        for _ in range(7):
            ds._track_request(5, success=True)
        assert ds.remaining_quota == 3

    @pytest.mark.asyncio
    async def test_health_default(self):
        ds = MockDataSource()
        status = await ds.health()
        assert status.healthy is True
        assert status.provider == "mock"
        assert status.latency_ms is not None

    @pytest.mark.asyncio
    async def test_abstract_methods_raise(self):
        ds = MockDataSource()
        with pytest.raises(NotImplementedError):
            await ds.fetch_history("AAPL")


# ── 2. DataSourceRegistry ──────────────────────────────────────

class TestDataSourceRegistry:

    def setup_method(self):
        self.reg = DataSourceRegistry()
        self.reg._providers = {}

    def test_singleton(self):
        r1 = DataSourceRegistry()
        r2 = DataSourceRegistry()
        assert r1 is r2

    def test_register_and_get(self):
        p = MockDataSource("alpha")
        self.reg.register(p)
        assert self.reg.get("alpha") is p
        assert self.reg.get("nonexistent") is None

    def test_list(self):
        p1 = MockDataSource("a")
        p2 = MockDataSource("b")
        self.reg.register(p1)
        self.reg.register(p2)
        providers = self.reg.list()
        assert len(providers) == 2
        assert {p.name for p in providers} == {"a", "b"}

    def test_get_by_capability(self):
        p1 = MockDataSource("quoter", capabilities=["quote", "history"])
        p2 = MockDataSource("newser", capabilities=["news"])
        p3 = MockDataSource("full", capabilities=["quote", "fundamentals"])
        self.reg.register(p1)
        self.reg.register(p2)
        self.reg.register(p3)
        quotes = self.reg.get_by_capability("quote")
        assert len(quotes) == 2
        assert {p.name for p in quotes} == {"quoter", "full"}
        news = self.reg.get_by_capability("news")
        assert len(news) == 1
        assert news[0].name == "newser"

    def test_count(self):
        assert self.reg.count() == 0
        self.reg.register(MockDataSource("a"))
        assert self.reg.count() == 1
        self.reg.register(MockDataSource("b"))
        assert self.reg.count() == 2

    def test_overwrite_on_register(self):
        p1 = MockDataSource("dup")
        p2 = MockDataSource("dup")
        self.reg.register(p1)
        self.reg.register(p2)
        assert self.reg.get("dup") is p2
        assert self.reg.count() == 1


# ── 3. DataCache ───────────────────────────────────────────────

class TestDataCache:

    def setup_method(self):
        self.cache = DataCache()
        self.cache._memory = {}
        self.cache.hits = 0
        self.cache.misses = 0

    def test_set_and_get(self):
        self.cache.set("test", "key1", value={"price": 100})
        result = self.cache.get("test", "key1")
        assert result == {"price": 100}

    def test_get_missing(self):
        assert self.cache.get("nonexistent", "key") is None

    def test_delete(self):
        self.cache.set("p", "k", value="v")
        assert self.cache.get("p", "k") == "v"
        self.cache.delete("p", "k")
        assert self.cache.get("p", "k") is None

    def test_multiple_parts_key(self):
        self.cache.set("provider", "tier1", "AAPL", value={"close": 150})
        assert self.cache.get("provider", "tier1", "AAPL") == {"close": 150}

    def test_hit_and_miss_tracking(self):
        assert self.cache.stats()["hits"] == 0
        assert self.cache.stats()["misses"] == 0
        self.cache.get("p", "x")
        assert self.cache.stats()["misses"] == 1
        self.cache.set("p", "x", value=42)
        self.cache.get("p", "x")
        assert self.cache.stats()["hits"] >= 1

    def test_stats_format(self):
        stats = self.cache.stats()
        assert "memory_entries" in stats
        assert "hit_rate_pct" in stats
        assert "tiers" in stats
        assert stats["hit_rate_pct"] == 0.0

    def test_ttl_expiry(self, monkeypatch):
        fake_now = 1000000.0

        class FakeDatetime:
            @staticmethod
            def now():
                class FakeNow:
                    @staticmethod
                    def timestamp():
                        return fake_now
                return FakeNow()

        monkeypatch.setattr("app.services.data.cache.datetime", FakeDatetime)
        cache = DataCache()
        cache.set("p", "k", value="fresh", ttl=60)
        assert cache.get("p", "k") == "fresh"
        fake_now += 61
        assert cache.get("p", "k") is None

    def test_redis_fallback(self):
        """When redis is unavailable, in-memory cache still works."""
        cache = DataCache()
        cache.set("p", "k", value="mem")
        assert cache.get("p", "k") == "mem"


# ── 4. CircuitBreaker ──────────────────────────────────────────

class TestCircuitBreaker:

    def setup_method(self):
        self.cb = CircuitBreaker(failure_threshold=3, reset_timeout=60.0)

    def test_initial_state_closed(self):
        assert not self.cb.is_open("yahoo")

    def test_opens_after_threshold(self):
        for _ in range(3):
            self.cb.record_failure("yahoo")
        assert self.cb.is_open("yahoo")

    def test_stays_closed_below_threshold(self):
        for _ in range(2):
            self.cb.record_failure("yahoo")
        assert not self.cb.is_open("yahoo")

    def test_success_resets_failures(self):
        for _ in range(3):
            self.cb.record_failure("yahoo")
        assert self.cb.is_open("yahoo")
        self.cb.record_success("yahoo")
        assert not self.cb.is_open("yahoo")

    def test_half_open_after_timeout(self, monkeypatch):
        for _ in range(3):
            self.cb.record_failure("yahoo")
        assert self.cb.is_open("yahoo")

        monkeypatch.setattr("time.time", lambda: 9999999999)
        assert not self.cb.is_open("yahoo")

    def test_independent_per_provider(self):
        for _ in range(3):
            self.cb.record_failure("provider_a")
        assert self.cb.is_open("provider_a")
        assert not self.cb.is_open("provider_b")

    def test_custom_threshold(self):
        cb = CircuitBreaker(failure_threshold=1, reset_timeout=30)
        cb.record_failure("x")
        assert cb.is_open("x")


# ── 5. DataSourceManager ───────────────────────────────────────

class TestDataSourceManager:

    def setup_method(self):
        self.reg = DataSourceRegistry()
        self.reg._providers = {}
        self.cache = DataCache()
        self.cache._memory = {}
        self.manager = DataSourceManager(cache=self.cache, registry=self.reg)

    @pytest.mark.asyncio
    async def test_fallback_chain_primary_fails_fallback_succeeds(self):
        primary = MockDataSource("primary", capabilities=["quote"])
        async def fail(_ticker):
            raise ProviderUnavailableError("down")
        primary.fetch_quote = fail
        fallback = MockDataSource("fallback", capabilities=["quote"])
        self.reg.register(primary)
        self.reg.register(fallback)
        result = await self.manager.fetch("quote", "AAPL")
        assert result.provider == "fallback"
        assert result.data["ticker"] == "AAPL"

    @pytest.mark.asyncio
    async def test_all_providers_fail(self):
        for i in range(3):
            p = MockDataSource(f"p{i}", capabilities=["quote"])
            async def fail(_t, prov=p):
                raise ProviderUnavailableError(f"{prov.name} down")
            p.fetch_quote = fail
            self.reg.register(p)
        result = await self.manager.fetch("quote", "AAPL")
        assert result.provider == "error"
        assert result.data is None

    @pytest.mark.asyncio
    async def test_circuit_breaker_trips_after_n_failures(self):
        failing = MockDataSource("failing", capabilities=["quote"])
        async def always_fail(_t):
            raise RateLimitError("rate limited")
        failing.fetch_quote = always_fail
        backup = MockDataSource("backup", capabilities=["quote"])
        self.reg.register(failing)
        self.reg.register(backup)
        results = []
        for _ in range(5):
            self.manager._cache.delete("quote", "AAPL")
            result = await self.manager.fetch("quote", "AAPL")
            results.append(result.provider)
        assert "backup" in results
        assert backup.call_count >= 1

    @pytest.mark.asyncio
    async def test_primary_success_no_fallback(self):
        primary = MockDataSource("primary", capabilities=["quote"])
        fallback = MockDataSource("fallback", capabilities=["quote"])
        self.reg.register(primary)
        self.reg.register(fallback)
        result = await self.manager.fetch("quote", "AAPL")
        assert result.provider == "primary"
        assert primary.call_count == 1
        assert fallback.call_count == 0

    @pytest.mark.asyncio
    async def test_preferred_provider_used_first(self):
        a = MockDataSource("a", capabilities=["quote"])
        b = MockDataSource("b", capabilities=["quote"])
        self.reg.register(a)
        self.reg.register(b)
        result = await self.manager.fetch("quote", "AAPL", provider="b")
        assert result.provider == "b"

    @pytest.mark.asyncio
    async def test_cache_hit_skips_fetch(self):
        p = MockDataSource("p", capabilities=["quote"])
        self.reg.register(p)
        self.manager._cache.set("quote", "AAPL", value={"cached": True})
        result = await self.manager.fetch("quote", "AAPL")
        assert result.cached is True
        assert p.call_count == 0

    @pytest.mark.asyncio
    async def test_capability_filtering(self):
        p_quote = MockDataSource("quoter", capabilities=["quote"])
        p_news = MockDataSource("newser", capabilities=["news"])
        self.reg.register(p_quote)
        self.reg.register(p_news)
        result = await self.manager.fetch("quote", "AAPL")
        assert result.provider == "quoter"
        result = await self.manager.fetch("news", "AAPL")
        assert result.provider == "error"
