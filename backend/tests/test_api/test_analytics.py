import pytest
from httpx import AsyncClient
from unittest.mock import MagicMock, AsyncMock


_SAMPLE_SUMMARY = {
    "total_portfolios": 5,
    "total_instruments": 150,
    "total_trades": 500,
    "total_aum": 5000000.0,
    "total_unrealized_pnl": 250000.0,
}

_SAMPLE_PORTFOLIO_ANALYTICS = {
    "summary": {
        "name": "Tech Growth",
        "total_value": 500000.0,
        "total_pnl": 25000.0,
    },
    "pnl_timeseries": [
        {"date": "2025-01-15", "pnl": 1000.0, "pnl_pct": 0.2},
    ],
    "risk_metrics": {
        "var_95": -0.025,
        "sharpe_ratio": 1.2,
    },
}

_SAMPLE_PERFORMANCE = [
    {"date": "2025-01-15", "return_pct": 0.5},
    {"date": "2025-01-14", "return_pct": -0.2},
]

_SAMPLE_PNL_TIMESERIES = [
    {"date": "2025-01-15", "pnl": 1000.0, "pnl_pct": 0.2},
    {"date": "2025-01-14", "pnl": -500.0, "pnl_pct": -0.1},
]


@pytest.mark.anyio
async def test_analytics_summary(client: AsyncClient):
    from app.main import app
    from app.database import get_db
    from app.services import analytics_service

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    with pytest.MonkeyPatch.context() as mp:
        async def mock_summary(*args):
            return _SAMPLE_SUMMARY

        mp.setattr(analytics_service, "get_summary_dashboard", mock_summary)
        app.dependency_overrides[get_db] = lambda: mock_session
        try:
            resp = await client.get("/api/v1/analytics/summary")
            assert resp.status_code == 200
            data = resp.json()
            assert "total_portfolios" in data
            assert "total_instruments" in data
            assert "total_aum" in data
        finally:
            app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_portfolio_analytics(client: AsyncClient):
    from app.main import app
    from app.database import get_db
    from app.services import analytics_service

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    with pytest.MonkeyPatch.context() as mp:
        async def mock_summary(*args):
            return {"name": "Tech Growth", "total_value": 500000.0}
        async def mock_pnl(*args, **kwargs):
            return _SAMPLE_PNL_TIMESERIES
        async def mock_risk(*args):
            return {"var_95": -0.025, "sharpe_ratio": 1.2}

        mp.setattr(analytics_service, "get_portfolio_summary", mock_summary)
        mp.setattr(analytics_service, "get_pnl_timeseries", mock_pnl)
        mp.setattr(analytics_service, "get_portfolio_risk_metrics", mock_risk)

        app.dependency_overrides[get_db] = lambda: mock_session
        try:
            resp = await client.get("/api/v1/analytics/portfolios/550e8400-e29b-41d4-a716-446655440000")
            assert resp.status_code == 200
            data = resp.json()
            assert "summary" in data
            assert "pnl_timeseries" in data
            assert "risk_metrics" in data
        finally:
            app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_portfolio_analytics_not_found(client: AsyncClient):
    from app.main import app
    from app.database import get_db
    from app.services import analytics_service

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    with pytest.MonkeyPatch.context() as mp:
        async def mock_summary(*args):
            return None

        mp.setattr(analytics_service, "get_portfolio_summary", mock_summary)

        app.dependency_overrides[get_db] = lambda: mock_session
        try:
            resp = await client.get("/api/v1/analytics/portfolios/550e8400-e29b-41d4-a716-446655449999")
            assert resp.status_code == 404
        finally:
            app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_instrument_performance(client: AsyncClient):
    from app.main import app
    from app.database import get_db
    from app.services import analytics_service

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    with pytest.MonkeyPatch.context() as mp:
        async def mock_perf(*args):
            return _SAMPLE_PERFORMANCE

        mp.setattr(analytics_service, "get_instrument_performance", mock_perf)
        app.dependency_overrides[get_db] = lambda: mock_session
        try:
            resp = await client.get("/api/v1/analytics/instruments/550e8400-e29b-41d4-a716-446655440000/performance")
            assert resp.status_code == 200
        finally:
            app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_pnl_timeseries(client: AsyncClient):
    from app.main import app
    from app.database import get_db
    from app.services import analytics_service

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    with pytest.MonkeyPatch.context() as mp:
        async def mock_pnl(*args, **kwargs):
            return _SAMPLE_PNL_TIMESERIES

        mp.setattr(analytics_service, "get_pnl_timeseries", mock_pnl)
        app.dependency_overrides[get_db] = lambda: mock_session
        try:
            resp = await client.get("/api/v1/analytics/pnl/timeseries?days=30")
            assert resp.status_code == 200
            data = resp.json()
            assert isinstance(data, list)
        finally:
            app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_pnl_timeseries_empty(client: AsyncClient):
    from app.main import app
    from app.database import get_db
    from app.services import analytics_service

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    with pytest.MonkeyPatch.context() as mp:
        async def mock_pnl(*args, **kwargs):
            return []

        mp.setattr(analytics_service, "get_pnl_timeseries", mock_pnl)
        app.dependency_overrides[get_db] = lambda: mock_session
        try:
            resp = await client.get("/api/v1/analytics/pnl/timeseries?days=7")
            assert resp.status_code == 200
            assert resp.json() == []
        finally:
            app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_portfolio_risk(client: AsyncClient):
    from app.main import app
    from app.database import get_db
    from app.services import analytics_service

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    with pytest.MonkeyPatch.context() as mp:
        async def mock_risk(*args):
            return {"var_95": -0.025, "sharpe_ratio": 1.2}

        mp.setattr(analytics_service, "get_portfolio_risk_metrics", mock_risk)
        app.dependency_overrides[get_db] = lambda: mock_session
        try:
            resp = await client.get("/api/v1/analytics/portfolios/550e8400-e29b-41d4-a716-446655440000/risk")
            assert resp.status_code == 200
            data = resp.json()
            assert "var_95" in data
        finally:
            app.dependency_overrides.clear()
