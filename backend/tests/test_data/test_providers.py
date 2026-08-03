"""Unit tests for all data source providers (mock HTTP responses)."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.data.base import DataSource, RateLimitError, ProviderUnavailableError
from app.services.data.models import Quote, OHLCV, GasPrices, YieldPool, DefiProtocol
from app.services.data.registry import DataSourceRegistry


# ── DataSource Base Tests ─────────────────────────────────────

class TestDataSourceBase:

    def test_stats_tracking(self):
        class TestProvider(DataSource):
            @property
            def name(self): return "test"
            @property
            def requires_key(self): return False
            @property
            def rate_limit_per_minute(self): return 60
            async def _test_connection(self): return True

        p = TestProvider()
        assert p.stats["name"] == "test"
        assert p.stats["remaining_quota"] == 60
        p._track_request(50, success=True)
        assert p.stats["success_count"] == 1
        assert p.stats["avg_latency_ms"] == 50.0
        assert p.stats["remaining_quota"] == 59
        p._track_request(100, success=False)
        assert p.stats["error_count"] == 1
        assert p.stats["avg_latency_ms"] == 75.0

    def test_remaining_quota_decreases(self):
        class TestProvider(DataSource):
            @property
            def name(self): return "test2"
            @property
            def requires_key(self): return False
            @property
            def rate_limit_per_minute(self): return 10
            async def _test_connection(self): return True

        p = TestProvider()
        assert p.remaining_quota == 10
        for _ in range(5):
            p._track_request(10, success=True)
        assert p.remaining_quota == 5
        for _ in range(5):
            p._track_request(10, success=True)
        assert p.remaining_quota == 0


# ── Registry Tests ─────────────────────────────────────────────

class TestDataSourceRegistry:

    def test_singleton(self):
        r1 = DataSourceRegistry()
        r2 = DataSourceRegistry()
        assert r1 is r2

    def test_register_and_get(self):
        reg = DataSourceRegistry()
        mock_provider = MagicMock(spec=DataSource)
        mock_provider.name = "mock"
        reg.register(mock_provider)
        assert reg.get("mock") is mock_provider
        assert reg.get("nonexistent") is None

    def test_get_by_capability(self):
        reg = DataSourceRegistry()
        reg._providers = {}
        p1 = MagicMock(spec=DataSource)
        p1.name = "a"; p1.capabilities = ["quote", "history"]
        p2 = MagicMock(spec=DataSource)
        p2.name = "b"; p2.capabilities = ["quote"]
        p3 = MagicMock(spec=DataSource)
        p3.name = "c"; p3.capabilities = ["defi"]
        reg.register(p1); reg.register(p2); reg.register(p3)
        quotes = reg.get_by_capability("quote")
        assert len(quotes) == 2
        defi = reg.get_by_capability("defi")
        assert len(defi) == 1
        assert defi[0].name == "c"


# ── HTTP Provider Tests (mocked) ───────────────────────────────

class TestFrankfurterProvider:

    @pytest.mark.asyncio
    async def test_fetch_fx_rates(self):
        from app.services.data.providers.frankfurter import FrankfurterProvider
        provider = FrankfurterProvider()
        mock_resp = MagicMock(status_code=200)
        mock_resp.json = MagicMock(return_value={"amount": 1.0, "base": "USD", "date": "2024-01-01", "rates": {"EUR": 0.92, "GBP": 0.79, "JPY": 148.5}})
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_resp):
            result = await provider.fetch_fx_rates("USD")
            assert isinstance(result, dict)
            assert "EUR" in result
            assert result["USD"] == 1.0

    @pytest.mark.asyncio
    async def test_fetch_fx_convert(self):
        from app.services.data.providers.frankfurter import FrankfurterProvider
        provider = FrankfurterProvider()
        mock_resp = MagicMock(status_code=200)
        mock_resp.json = MagicMock(return_value={"amount": 1.0, "base": "USD", "date": "2024-01-01", "rates": {"EUR": 0.92}})
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_resp):
            result = await provider.fetch_fx_convert(100, "USD", "EUR")
            assert result["amount"] == 100
            assert result["rate"] == 0.92


class TestDefiLlamaProvider:

    @pytest.mark.asyncio
    async def test_tvl_overview(self):
        from app.services.data.providers.defillama import DefiLlamaProvider
        provider = DefiLlamaProvider()
        mock_resp = MagicMock(status_code=200)
        mock_resp.json = MagicMock(return_value=[{"name": "Ethereum", "tvl": 50000000000}, {"name": "Solana", "tvl": 10000000000}])
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_resp):
            overview = await provider.fetch_tvl_overview()
            assert "total_tvl" in overview
            assert "chains_count" in overview

    @pytest.mark.asyncio
    async def test_protocols(self):
        from app.services.data.providers.defillama import DefiLlamaProvider
        provider = DefiLlamaProvider()
        mock_resp = MagicMock(status_code=200)
        mock_resp.json = MagicMock(return_value=[{"name": "Lido", "chain": "ethereum", "tvl": 20000000000, "category": "Liquid Staking"}])
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_resp):
            protocols = await provider.fetch_protocols()
            assert isinstance(protocols, list)
            assert len(protocols) > 0


class TestDumbStockProvider:

    @pytest.mark.asyncio
    async def test_search(self):
        from app.services.data.providers.dumbstock import DumbStockProvider
        provider = DumbStockProvider()
        mock_resp = MagicMock(status_code=200)
        mock_resp.json = MagicMock(return_value=[{"symbol": "AAPL", "name": "Apple Inc.", "exchange": "NASDAQ"}])
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_resp):
            result = await provider.search_ticker("AAPL")
            assert isinstance(result, list)
            assert len(result) > 0


# ── Cache Tests ────────────────────────────────────────────────

class TestDataCache:

    def test_set_and_get(self):
        from app.services.data.cache import DataCache
        cache = DataCache()
        assert cache.set("test_provider", "key1", value={"price": 100})
        result = cache.get("test_provider", "key1")
        assert result == {"price": 100}

    def test_missing_key(self):
        from app.services.data.cache import DataCache
        cache = DataCache()
        assert cache.get("nonexistent", "key") is None

    def test_delete(self):
        from app.services.data.cache import DataCache
        cache = DataCache()
        cache.set("p", "k", value="v")
        assert cache.get("p", "k") == "v"
        assert cache.delete("p", "k")
        assert cache.get("p", "k") is None

    def test_stats(self):
        from app.services.data.cache import DataCache
        cache = DataCache()
        stats = cache.stats()
        assert "memory_entries" in stats


# ── Model Validation Tests ────────────────────────────────────

class TestModels:

    def test_quote(self):
        from datetime import datetime
        q = Quote(ticker="AAPL", price=150.0, change=1.5, change_pct=1.0, timestamp=datetime.utcnow())
        assert q.ticker == "AAPL"
        assert q.price == 150.0

    def test_ohlcv(self):
        from datetime import datetime
        o = OHLCV(timestamp=datetime.utcnow(), open=100.0, high=110.0, low=99.0, close=105.0, volume=10000)
        assert o.open == 100.0
        assert o.volume == 10000

    def test_gas_prices(self):
        g = GasPrices(chain="ethereum", safe_gwei=10.0, propose_gwei=15.0, fast_gwei=20.0)
        assert g.fast_gwei == 20.0

    def test_yield_pool(self):
        y = YieldPool(pool="aave-usdc", chain="ethereum", project="aave", apy=5.5, tvl=1000000)
        assert y.apy == 5.5

    def test_defi_protocol(self):
        d = DefiProtocol(name="Uniswap", chain="ethereum", tvl=5000000000, category="DEX")
        assert d.name == "Uniswap"


class TestOpenSkyProvider:

    def test_capabilities(self):
        from app.services.data.providers.opensky import OpenSkyProvider
        p = OpenSkyProvider()
        assert "globe_aircraft" in p.capabilities
        assert p.name == "opensky"

    @pytest.mark.asyncio
    async def test_fetch_globe_aircraft(self):
        from unittest.mock import patch, MagicMock
        from app.services.data.providers.opensky import OpenSkyProvider
        p = OpenSkyProvider()

        mock_data = {
            "states": [
                ["abc123", "SWA123", "United States", 1700000000, 1700000000,
                 -122.37, 37.62, 35000, 480.2, 270, 0, False, 0]
            ]
        }

        # Mock httpx at the transport level — patch the client.get method directly
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = mock_data

        # Patch client.get to return an awaitable that returns mock_resp
        class MockClient:
            async def get(self, *args, **kwargs):
                return mock_resp

        class MockAsyncClient:
            async def __aenter__(self):
                return MockClient()
            async def __aexit__(self, *args):
                pass

        with patch("httpx.AsyncClient", return_value=MockAsyncClient()):
            result = await p.fetch_globe_aircraft()
            assert isinstance(result, list)
            assert len(result) > 0
            assert result[0]["lat"] == 37.62
            assert result[0]["lng"] == -122.37
            assert result[0]["callsign"] == "SWA123"


class TestMaritimeProvider:

    def test_capabilities(self):
        from app.services.data.providers.maritime import MaritimeProvider
        p = MaritimeProvider()
        assert "globe_maritime" in p.capabilities
        assert p.name == "maritime"

    @pytest.mark.asyncio
    async def test_fetch_globe_maritime(self):
        from app.services.data.providers.maritime import MaritimeProvider
        p = MaritimeProvider()
        result = await p.fetch_globe_maritime()
        assert isinstance(result, dict)
        assert "ships" in result
        assert "ports" in result
        assert "lanes" in result
        assert len(result["ships"]) > 0
        assert "lat" in result["ships"][0]
        assert "lng" in result["ships"][0]

    @pytest.mark.asyncio
    async def test_ports_have_teu(self):
        from app.services.data.providers.maritime import MaritimeProvider
        p = MaritimeProvider()
        result = await p.fetch_globe_maritime()
        for port in result["ports"]:
            assert "teu" in port
            assert port["teu"] > 0


class TestSatelliteProvider:

    def test_capabilities(self):
        from app.services.data.providers.satellite import SatelliteDataSource
        p = SatelliteDataSource()
        assert "satellites" in p.capabilities
        assert p.name == "celestrak"

    def test_fetch_globe_satellites(self):
        from app.services.data.providers.satellite import SatelliteDataSource
        p = SatelliteDataSource()
        result = p.fetch_globe_satellites()
        assert isinstance(result, list)
        assert len(result) > 0
        assert "name" in result[0]
        assert "lat" in result[0]
        assert "lng" in result[0]
        assert -90 <= result[0]["lat"] <= 90
        assert -180 <= result[0]["lng"] <= 180

    def test_iss_position(self):
        from app.services.data.providers.satellite import SatelliteDataSource
        p = SatelliteDataSource()
        iss = p.fetch_iss_position()
        assert iss["name"] == "ISS"
        assert "lat" in iss
        assert "lng" in iss


class TestConflictProvider:

    def test_capabilities(self):
        from app.services.data.providers.conflict import ConflictDataSource
        p = ConflictDataSource()
        assert "conflict_zones" in p.capabilities
        assert p.name == "conflict"

    def test_fetch_conflict_zones(self):
        from app.services.data.providers.conflict import ConflictDataSource
        p = ConflictDataSource()
        zones = p.fetch_conflict_zones()
        assert isinstance(zones, list)
        assert len(zones) > 0
        assert "name" in zones[0]
        assert "lat" in zones[0]
        assert "lng" in zones[0]
        assert -90 <= zones[0]["lat"] <= 90

    def test_conflict_types(self):
        from app.services.data.providers.conflict import ConflictDataSource
        p = ConflictDataSource()
        zones = p.fetch_conflict_zones()
        types = {z["type"] for z in zones}
        assert len(types) >= 3  # At least 3 different conflict types
        assert all("lat" in z and "lng" in z for z in zones)
