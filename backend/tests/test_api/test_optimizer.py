import pytest
from httpx import AsyncClient
from unittest.mock import patch

from app.services.analytics import portfolio_optimizer


_SAMPLE_OPTIMIZE = {
    "tickers": ["AAPL", "MSFT"],
    "weights": {"AAPL": 0.6, "MSFT": 0.4},
    "expected_return": 0.15,
    "expected_volatility": 0.20,
    "sharpe_ratio": 0.75,
    "risk_free_rate": 0.05,
    "efficient_frontier": [],
    "assets": [],
}

_SAMPLE_MINVAR = {
    "tickers": ["AAPL", "MSFT"],
    "weights": {"AAPL": 0.5, "MSFT": 0.5},
    "expected_return": 0.10,
    "expected_volatility": 0.15,
    "method": "min_variance",
}

_SAMPLE_EQWEIGHT = {
    "tickers": ["AAPL", "MSFT", "GOOGL"],
    "weights": {"AAPL": 0.3333, "MSFT": 0.3333, "GOOGL": 0.3334},
    "expected_return": 0.11,
    "expected_volatility": 0.17,
    "method": "equal_weight",
}


@pytest.mark.anyio
async def test_optimize_max_sharpe_happy_path(
    client: AsyncClient
):
    with patch.object(portfolio_optimizer, "optimize_portfolio", return_value=_SAMPLE_OPTIMIZE):
        resp = await client.get(
            "/api/v1/optimizer/optimize?tickers=AAPL,MSFT&period=1y",
            
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "weights" in data
    assert "sharpe_ratio" in data
    assert data["sharpe_ratio"] == 0.75


@pytest.mark.anyio
async def test_optimize_default_tickers(client: AsyncClient):
    with patch.object(portfolio_optimizer, "optimize_portfolio", return_value=_SAMPLE_OPTIMIZE):
        resp = await client.get("/api/v1/optimizer/optimize", )
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_optimize_insufficient_data(client: AsyncClient):
    with patch.object(
        portfolio_optimizer, "optimize_portfolio",
        return_value={"error": "Insufficient data for optimization"},
    ):
        resp = await client.get(
            "/api/v1/optimizer/optimize?tickers=AAPL", 
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_min_variance_happy_path(client: AsyncClient):
    with patch.object(portfolio_optimizer, "min_variance_portfolio", return_value=_SAMPLE_MINVAR):
        resp = await client.get(
            "/api/v1/optimizer/min-variance?tickers=AAPL,MSFT", 
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["method"] == "min_variance"


@pytest.mark.anyio
async def test_min_variance_no_data(client: AsyncClient):
    with patch.object(
        portfolio_optimizer, "min_variance_portfolio",
        return_value={"error": "No data"},
    ):
        resp = await client.get(
            "/api/v1/optimizer/min-variance?tickers=FAKE,EMPTY", 
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_equal_weight_happy_path(client: AsyncClient):
    with patch.object(portfolio_optimizer, "equal_weight_portfolio", return_value=_SAMPLE_EQWEIGHT):
        resp = await client.get(
            "/api/v1/optimizer/equal-weight?tickers=AAPL,MSFT,GOOGL",
            
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["method"] == "equal_weight"
    assert len(data["weights"]) == 3


@pytest.mark.anyio
async def test_equal_weight_default_tickers(client: AsyncClient):
    with patch.object(portfolio_optimizer, "equal_weight_portfolio", return_value=_SAMPLE_EQWEIGHT):
        resp = await client.get(
            "/api/v1/optimizer/equal-weight", 
        )
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_performance_metrics_happy_path(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get(
        "/api/v1/optimizer/performance?tickers=AAPL,MSFT", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)


@pytest.mark.anyio
async def test_performance_metrics_custom_params(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get(
        "/api/v1/optimizer/performance?tickers=AAPL&period=1y&risk_free=0.03",
        
    )
    assert resp.status_code == 200
