"""Tests for the Factor Analysis API endpoints."""
import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient

_MOCK_FACTOR_RESULT = {
    "ticker": "AAPL",
    "model": "3-factor + Momentum",
    "period": "2y",
    "n_observations": 252,
    "date_range": {"start": "20240102", "end": "20250102"},
    "alpha": {
        "daily": 0.0003,
        "annualized": 0.0756,
        "std_error": 0.0002,
        "t_stat": 1.5,
    },
    "factor_loadings": {
        "Mkt-RF": {"coefficient": 1.2, "std_error": 0.05, "t_stat": 24.0},
        "SMB": {"coefficient": -0.3, "std_error": 0.08, "t_stat": -3.75},
        "HML": {"coefficient": -0.1, "std_error": 0.07, "t_stat": -1.43},
        "MOM": {"coefficient": 0.05, "std_error": 0.06, "t_stat": 0.83},
    },
    "r_squared": 0.45,
    "adjusted_r_squared": 0.44,
    "residual_std": 0.015,
    "as_of": "2025-01-15T12:00:00",
}


@pytest.mark.anyio
async def test_factor_regression_3factor(client: AsyncClient):
    with patch("app.services.analytics.factors.run_factor_regression", new_callable=AsyncMock) as mock:
        mock.return_value = _MOCK_FACTOR_RESULT
        res = await client.get("/api/v1/analytics/factors/AAPL?model=3&include_momentum=true")
        assert res.status_code == 200
        data = res.json()
        assert data["ticker"] == "AAPL"
        assert data["model"] == "3-factor + Momentum"
        assert "factor_loadings" in data
        assert "Mkt-RF" in data["factor_loadings"]


@pytest.mark.anyio
async def test_factor_regression_5factor(client: AsyncClient):
    with patch("app.services.analytics.factors.run_factor_regression", new_callable=AsyncMock) as mock:
        result = dict(_MOCK_FACTOR_RESULT, model="5-factor")
        result["factor_loadings"] = {
            "Mkt-RF": {"coefficient": 1.15, "std_error": 0.05, "t_stat": 23.0},
            "SMB": {"coefficient": -0.28, "std_error": 0.08, "t_stat": -3.5},
            "HML": {"coefficient": -0.1, "std_error": 0.07, "t_stat": -1.43},
            "RMW": {"coefficient": -0.05, "std_error": 0.06, "t_stat": -0.83},
            "CMA": {"coefficient": 0.02, "std_error": 0.05, "t_stat": 0.4},
        }
        mock.return_value = result
        res = await client.get("/api/v1/analytics/factors/AAPL?model=5")
        assert res.status_code == 200
        data = res.json()
        assert data["model"] == "5-factor"
        assert "RMW" in data["factor_loadings"]


@pytest.mark.anyio
async def test_factor_regression_insufficient_data(client: AsyncClient):
    with patch("app.services.analytics.factors.run_factor_regression", new_callable=AsyncMock) as mock:
        mock.return_value = {"error": "Insufficient price data for TEST"}
        res = await client.get("/api/v1/analytics/factors/TEST")
        assert res.status_code == 200
        assert "error" in res.json()


@pytest.mark.anyio
async def test_factor_regression_invalid_model(client: AsyncClient):
    res = await client.get("/api/v1/analytics/factors/AAPL?model=10")
    assert res.status_code == 422  # Pydantic validation: model must be 3-5


@pytest.mark.anyio
async def test_factor_regression_period(client: AsyncClient):
    with patch("app.services.analytics.factors.run_factor_regression", new_callable=AsyncMock) as mock:
        mock.return_value = dict(_MOCK_FACTOR_RESULT, period="5y")
        res = await client.get("/api/v1/analytics/factors/AAPL?period=5y")
        assert res.status_code == 200
        data = res.json()
        assert data["period"] == "5y"


@pytest.mark.anyio
async def test_factor_regression_default_params(client: AsyncClient):
    with patch("app.services.analytics.factors.run_factor_regression", new_callable=AsyncMock) as mock:
        mock.return_value = _MOCK_FACTOR_RESULT
        res = await client.get("/api/v1/analytics/factors/MSFT")
        assert res.status_code == 200
        mock.assert_called_once_with(
            ticker="MSFT", model=3, include_momentum=False, period="2y",
        )


@pytest.mark.anyio
async def test_factor_regression_with_momentum(client: AsyncClient):
    with patch("app.services.analytics.factors.run_factor_regression", new_callable=AsyncMock) as mock:
        mock.return_value = _MOCK_FACTOR_RESULT
        res = await client.get("/api/v1/analytics/factors/GOOGL?include_momentum=true")
        assert res.status_code == 200
        mock.assert_called_once()
        assert mock.call_args[1]["include_momentum"] is True
