"""
Tests for Portfolio Attribution endpoints.
"""

import pytest
from uuid import UUID
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.middleware.auth import get_current_user
from app.database import get_db

TEST_PID = "11111111-1111-1111-1111-111111111111"

_SAMPLE_POSITIONS = [
    {
        "id": UUID("11111111-1111-1111-1111-111111111111"),
        "ticker": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "instrument_type": "stock",
        "quantity": 100,
        "average_price": 120.0,
        "market_value": 15000.0,
        "cost_basis": 12000.0,
        "unrealized_pnl": 3000.0,
        "realized_pnl": 0.0,
    },
    {
        "id": UUID("22222222-2222-2222-2222-222222222222"),
        "ticker": "MSFT",
        "name": "Microsoft Corp.",
        "sector": "Technology",
        "instrument_type": "stock",
        "quantity": 50,
        "average_price": 160.0,
        "market_value": 9000.0,
        "cost_basis": 8000.0,
        "unrealized_pnl": 1000.0,
        "realized_pnl": 0.0,
    },
    {
        "id": UUID("33333333-3333-3333-3333-333333333333"),
        "ticker": "JPM",
        "name": "JPMorgan Chase",
        "sector": "Financial Services",
        "instrument_type": "stock",
        "quantity": 30,
        "average_price": 140.0,
        "market_value": 4500.0,
        "cost_basis": 4200.0,
        "unrealized_pnl": 300.0,
        "realized_pnl": 0.0,
    },
]

_SAMPLE_SECURITY_ATTRIBUTION = {
    "portfolio_id": "test-portfolio-uuid",
    "period": "1y",
    "total_market_value": 28500.0,
    "portfolio_return_pct": 5.26,
    "securities": [
        {
            "ticker": "AAPL",
            "name": "Apple Inc.",
            "sector": "Technology",
            "instrument_type": "stock",
            "quantity": 100,
            "weight_pct": 52.63,
            "cost_basis": 12000.0,
            "market_value": 15000.0,
            "return_pct": 25.0,
            "contribution_pct": 13.16,
        },
        {
            "ticker": "MSFT",
            "name": "Microsoft Corp.",
            "sector": "Technology",
            "instrument_type": "stock",
            "quantity": 50,
            "weight_pct": 31.58,
            "cost_basis": 8000.0,
            "market_value": 9000.0,
            "return_pct": 12.5,
            "contribution_pct": 3.95,
        },
        {
            "ticker": "JPM",
            "name": "JPMorgan Chase",
            "sector": "Financial Services",
            "instrument_type": "stock",
            "quantity": 30,
            "weight_pct": 15.79,
            "cost_basis": 4200.0,
            "market_value": 4500.0,
            "return_pct": 7.14,
            "contribution_pct": 1.13,
        },
    ],
    "as_of": "2026-05-18T12:00:00",
}

_SAMPLE_SECTOR_ATTRIBUTION = {
    "portfolio_id": "test-portfolio-uuid",
    "benchmark": "SPY",
    "period": "1y",
    "total_portfolio_return": 8.25,
    "total_allocation_effect": 0.42,
    "total_selection_effect": 0.85,
    "total_attribution": 1.27,
    "sectors": [
        {
            "sector": "Technology",
            "portfolio_weight": 84.21,
            "benchmark_weight": 29.5,
            "portfolio_return": 20.83,
            "benchmark_return": 15.2,
            "allocation_effect": 8.36,
            "selection_effect": 1.66,
            "interaction_effect": 0.74,
            "total_effect": 10.76,
        },
        {
            "sector": "Financial Services",
            "portfolio_weight": 15.79,
            "benchmark_weight": 13.0,
            "portfolio_return": 7.14,
            "benchmark_return": 5.8,
            "allocation_effect": 0.16,
            "selection_effect": 0.17,
            "interaction_effect": 0.02,
            "total_effect": 0.35,
        },
    ],
    "as_of": "2026-05-18T12:00:00",
}

_SAMPLE_FACTOR_ATTRIBUTION = {
    "portfolio_id": "test-portfolio-uuid",
    "model": "3-factor",
    "period": "1y",
    "n_observations": 252,
    "alpha_daily": 0.0005,
    "alpha_annualized": 0.126,
    "alpha_t_stat": 1.85,
    "r_squared": 0.72,
    "adjusted_r_squared": 0.71,
    "factor_loadings": {
        "Mkt-RF": {"coefficient": 1.05, "std_error": 0.08, "t_stat": 13.12},
        "SMB": {"coefficient": -0.15, "std_error": 0.10, "t_stat": -1.50},
        "HML": {"coefficient": 0.08, "std_error": 0.11, "t_stat": 0.73},
    },
    "mean_factor_returns": {
        "Mkt-RF": 0.0006,
        "SMB": 0.0001,
        "HML": 0.0000,
    },
    "factor_contributions": {
        "Mkt-RF": 0.00063,
        "SMB": -0.000015,
        "HML": 0.0,
    },
    "as_of": "2026-05-18T12:00:00",
}

_SAMPLE_FULL_REPORT = {
    "portfolio_id": "test-portfolio-uuid",
    "benchmark": "SPY",
    "period": "1y",
    "sector_attribution": _SAMPLE_SECTOR_ATTRIBUTION,
    "security_attribution": _SAMPLE_SECURITY_ATTRIBUTION,
    "factor_attribution": _SAMPLE_FACTOR_ATTRIBUTION,
    "as_of": "2026-05-18T12:00:00",
}


@pytest.fixture
def mock_db():
    """Mock database session with sample positions."""
    mock_session = MagicMock()
    mock_result = MagicMock()
    mock_result.mappings().all.return_value = _SAMPLE_POSITIONS
    mock_session.execute = AsyncMock(return_value=mock_result)
    return mock_session


@pytest.fixture
def client(mock_db):
    """Test client with mocked auth and database."""
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin"}
    transport = ASGITransport(app=app)
    yield AsyncClient(transport=transport, base_url="http://test")
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_sector_attribution(client):
    with patch("app.services.analytics.attribution.get_history") as mock_history:
        mock_history.return_value = [
            {"close": 100, "date": "2025-01-02"},
            {"close": 110, "date": "2025-06-02"},
            {"close": 115, "date": "2025-12-31"},
        ]
        resp = await client.get(f"/api/v1/attribution/{TEST_PID}/sector?benchmark=SPY&period=1y")
        assert resp.status_code == 200
        data = resp.json()
        assert "sectors" in data
        assert data["benchmark"] == "SPY"
        assert len(data["sectors"]) > 0
        for s in data["sectors"]:
            assert "sector" in s
            assert "allocation_effect" in s
            assert "selection_effect" in s


@pytest.mark.anyio
async def test_security_attribution(client):
    resp = await client.get(f"/api/v1/attribution/{TEST_PID}/security?period=1y")
    assert resp.status_code == 200
    data = resp.json()
    assert "securities" in data
    assert len(data["securities"]) > 0
    for s in data["securities"]:
        assert "ticker" in s
        assert "weight_pct" in s
        assert "contribution_pct" in s


@pytest.mark.anyio
async def test_security_attribution_empty():
    """Test security attribution with empty portfolio."""
    mock_empty = MagicMock()
    mock_empty_result = MagicMock()
    mock_empty_result.mappings().all.return_value = []
    mock_empty.execute = AsyncMock(return_value=mock_empty_result)

    app.dependency_overrides[get_db] = lambda: mock_empty
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin"}
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as c:
        resp = await c.get("/api/v1/attribution/22222222-2222-2222-2222-222222222222/security")
        assert resp.status_code == 200
        data = resp.json()
        assert "error" in data

    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_full_attribution_report(client):
    with patch("app.services.analytics.attribution.get_history") as mock_history, \
         patch("app.services.analytics.attribution.fetch_factors") as mock_factors:
        mock_history.return_value = [
            {"close": 100, "date": "2025-01-02"},
            {"close": 115, "date": "2025-12-31"},
        ]
        mock_factors.return_value = {
            "dates": ["20250101", "20251231"],
            "factors": {
                "Mkt-RF": MagicMock(shape=(2,)), "SMB": MagicMock(shape=(2,)),
                "HML": MagicMock(shape=(2,)),
            },
            "rf": MagicMock(shape=(2,)),
            "model": "3-factor",
        }

        resp = await client.get(f"/api/v1/attribution/{TEST_PID}?benchmark=SPY&period=1y")
        assert resp.status_code == 200
        data = resp.json()
        assert "sector_attribution" in data
        assert "security_attribution" in data
        assert "factor_attribution" in data


@pytest.mark.anyio
async def test_attribution_not_found():
    """Test attribution with non-existent portfolio."""
    mock_none = MagicMock()
    mock_none_result = MagicMock()
    mock_none_result.mappings().all.return_value = []
    mock_none.execute = AsyncMock(return_value=mock_none_result)

    app.dependency_overrides[get_db] = lambda: mock_none
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin"}
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as c:
        resp = await c.get("/api/v1/attribution/33333333-3333-3333-3333-333333333333/sector")
        assert resp.status_code == 200
        data = resp.json()
        assert "error" in data

    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_factor_attribution_not_found():
    """Test factor attribution on empty portfolio."""
    mock_empty = MagicMock()
    mock_result = MagicMock()
    mock_result.mappings().all.return_value = []
    mock_empty.execute = AsyncMock(return_value=mock_result)

    app.dependency_overrides[get_db] = lambda: mock_empty
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin"}
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as c:
        resp = await c.get("/api/v1/attribution/22222222-2222-2222-2222-222222222222/factor?model=3&period=1y")
        assert resp.status_code == 200
        data = resp.json()
        assert "error" in data

    app.dependency_overrides.clear()
