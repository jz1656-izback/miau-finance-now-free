import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
def mock_auth():
    from app.middleware.auth import get_current_user
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin"}
    yield
    app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture(autouse=True)
def disable_rate_limit():
    from app.config import settings
    orig_min = settings.rate_limit_per_minute
    orig_hour = settings.rate_limit_per_hour
    settings.rate_limit_per_minute = 100000
    settings.rate_limit_per_hour = 1000000
    yield
    settings.rate_limit_per_minute = orig_min
    settings.rate_limit_per_hour = orig_hour


@pytest.fixture(autouse=True)
def disable_csrf():
    """Disable CSRF middleware for tests."""
    app.user_middleware = [m for m in app.user_middleware if m.cls.__name__ != 'CSRFMiddleware']
    # Force rebuild of middleware stack
    app.middleware_stack = None
    yield
    # Restore middleware stack for next test
    app.middleware_stack = None


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


_YF_HISTORY_MODULES = [
    "app.services.analytics.market_data",
    "app.services.analytics.risk",
    "app.services.analytics.signals",
    "app.services.analytics.fundamentals",
    "app.services.analytics.portfolio_optimizer",
]
_YF_PRICE_MODULES = ["app.services.analytics.market_data"]
_YF_INFO_MODULES = ["app.services.analytics.fundamentals"]

_PRICE = {"ticker": "AAPL", "price": 150.25, "prev_close": 148.50, "change": 1.75,
          "change_pct": 1.18, "high": 151.00, "low": 149.00, "volume": 50000000,
          "as_of": "2025-01-15T12:00:00"}

_HISTORY = [
    {"date": "2025-01-15T12:00:00", "open": 149.0, "high": 151.0, "low": 148.5,
     "close": 150.25, "volume": 50000000},
    {"date": "2025-01-14T12:00:00", "open": 148.0, "high": 149.5, "low": 147.0,
     "close": 148.50, "volume": 45000000},
    {"date": "2025-01-13T12:00:00", "open": 147.0, "high": 148.5, "low": 146.0,
     "close": 147.80, "volume": 42000000},
]

_LONG_HISTORY = []
for i in range(252):
    _LONG_HISTORY.append({
        "date": f"2024-{(i // 30) + 1:02d}-{(i % 28) + 1:02d}T12:00:00",
        "open": 148.0, "high": 149.5, "low": 147.0,
        "close": 150.0 + (i % 50) * 0.5, "volume": 45000000,
    })

_INFO = {
    "assetProfile": {"sector": "Technology", "industry": "Consumer Electronics",
                     "fullTimeEmployees": 150000,
                     "longBusinessSummary": "Apple Inc.",
                     "website": "https://apple.com"},
    "financialData": {"shortName": {"raw": "Apple Inc."}, "recommendationKey": "buy",
                      "targetMeanPrice": {"raw": 180.0}, "targetHighPrice": {"raw": 220.0},
                      "targetLowPrice": {"raw": 140.0}, "numberOfAnalystOpinions": {"raw": 40}},
    "defaultKeyStatistics": {"marketCap": {"raw": 2500000000000}, "trailingPE": {"raw": 28.5},
                             "forwardPE": {"raw": 25.0}, "priceToBook": {"raw": 45.0},
                             "enterpriseToEbitda": {"raw": 22.0}},
    "summaryDetail": {}, "price": {},
}


def _make_patches(modules, func_name, target_modules):
    ps = []
    for mod in modules:
        ps.append(patch(f"{mod}.{func_name}", new_callable=AsyncMock))
    if target_modules:
        ps.append(patch(f"app.services.analytics._yf.{func_name}", new_callable=AsyncMock))
    return ps


@pytest.fixture
def mock_yf_price():
    ps = _make_patches(_YF_PRICE_MODULES, "get_price", True)
    mocks = [p.start() for p in ps]
    for m in mocks:
        m.return_value = _PRICE
    yield mocks
    for p in reversed(ps):
        p.stop()


@pytest.fixture
def mock_yf_history():
    ps = _make_patches(_YF_HISTORY_MODULES, "get_history", True)
    mocks = [p.start() for p in ps]
    for m in mocks:
        m.return_value = _HISTORY
    yield mocks
    for p in reversed(ps):
        p.stop()


@pytest.fixture
def mock_yf_history_many():
    ps = _make_patches(_YF_HISTORY_MODULES, "get_history", True)
    mocks = [p.start() for p in ps]
    for m in mocks:
        m.return_value = _LONG_HISTORY
    yield mocks
    for p in reversed(ps):
        p.stop()


@pytest.fixture
def mock_yf_get_info():
    ps = _make_patches(_YF_INFO_MODULES, "get_info", True)
    mocks = [p.start() for p in ps]
    for m in mocks:
        m.return_value = _INFO
    yield mocks
    for p in reversed(ps):
        p.stop()


@pytest.fixture
def mock_yahoo_news():
    with patch("yfinance.Ticker") as m:
        instance = MagicMock()
        instance.news = [
            {"title": "Apple Reports Strong Earnings", "publisher": "Reuters",
             "link": "https://reuters.com/apple", "type": "STORY",
             "relatedTickers": ["AAPL"], "summary": "Apple beat expectations.",
             "providerPublishTime": 1700000000},
        ]
        m.return_value = instance
        yield m


@pytest.fixture
def mock_coingecko():
    with patch("app.services.analytics.data_sources.httpx.AsyncClient") as mock:
        client_instance = MagicMock()
        mock.return_value.__aenter__.return_value = client_instance
        yield client_instance
