import pytest
from httpx import AsyncClient
from unittest.mock import patch


@pytest.mark.anyio
async def test_var_happy_path(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get(
        "/api/v1/risk/var?ticker=AAPL&confidence=0.95", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "var" in data
    assert "cvar" in data
    assert data["confidence"] == 0.95


@pytest.mark.anyio
async def test_var_with_different_confidence(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get(
        "/api/v1/risk/var?ticker=AAPL&confidence=0.99", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["confidence"] == 0.99


@pytest.mark.anyio
async def test_var_parametric_method(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get(
        "/api/v1/risk/var?ticker=AAPL&method=parametric", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["method"] == "parametric"


@pytest.mark.anyio
async def test_var_empty_returns(client: AsyncClient):
    with patch("app.services.analytics.risk.get_history", return_value=[]):
        resp = await client.get(
            "/api/v1/risk/var?ticker=EMPTY", 
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_beta_happy_path(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get(
        "/api/v1/risk/beta?ticker=AAPL&benchmark=SPY", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "beta" in data
    assert "alpha" in data
    assert "correlation" in data
    assert "r_squared" in data


@pytest.mark.anyio
async def test_beta_with_custom_benchmark(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get(
        "/api/v1/risk/beta?ticker=TSLA&benchmark=QQQ", 
    )
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_beta_insufficient_data(client: AsyncClient):
    with patch("app.services.analytics.risk.get_history", return_value=[]):
        resp = await client.get(
            "/api/v1/risk/beta?ticker=EMPTY", 
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_stress_test_happy_path(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get(
        "/api/v1/risk/stress-test?ticker=SPY", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "2008_financial_crisis" in data
    assert "2020_covid" in data
    for scenario in data.values():
        assert "description" in scenario
        assert "shock_pct" in scenario
        assert "impact_label" in scenario


@pytest.mark.anyio
async def test_stress_test_empty_data(client: AsyncClient):
    with patch("app.services.analytics.risk.get_history", return_value=[]):
        resp = await client.get(
            "/api/v1/risk/stress-test?ticker=EMPTY", 
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_greeks_call_option(client: AsyncClient):
    resp = await client.get(
        "/api/v1/risk/greeks?spot=100&strike=105&days_to_expiry=30&option_type=call",
        
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["option_type"] == "call"
    assert "delta" in data
    assert "gamma" in data
    assert "theta" in data
    assert "vega" in data
    assert "rho" in data


@pytest.mark.anyio
async def test_greeks_put_option(client: AsyncClient):
    resp = await client.get(
        "/api/v1/risk/greeks?spot=100&strike=105&days_to_expiry=30&option_type=put",
        
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["option_type"] == "put"


@pytest.mark.anyio
async def test_greeks_invalid_parameters(client: AsyncClient):
    resp = await client.get(
        "/api/v1/risk/greeks?spot=-1&strike=105", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_greeks_default_values(client: AsyncClient):
    resp = await client.get("/api/v1/risk/greeks", )
    assert resp.status_code == 200
    data = resp.json()
    assert data["spot"] == 100.0
    assert data["strike"] == 105.0


@pytest.mark.anyio
async def test_comprehensive_risk_happy_path(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get(
        "/api/v1/risk/comprehensive?ticker=AAPL", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "var_95" in data
    assert "var_99" in data
    assert "beta" in data
    assert "stress_test" in data


@pytest.mark.anyio
async def test_comprehensive_risk_no_data(client: AsyncClient):
    with patch("app.services.analytics.risk.get_history", return_value=[]):
        resp = await client.get(
            "/api/v1/risk/comprehensive?ticker=FAKE", 
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


def _make_rolling_mock_df():
    import pandas as pd
    import numpy as np
    dates = pd.date_range(end="2025-01-15", periods=504, freq="D")
    prices = 100 + np.cumsum(np.random.default_rng(42).normal(0, 1, 504))
    df = pd.DataFrame({
        "Open": prices, "High": prices * 1.01, "Low": prices * 0.99,
        "Close": prices, "Volume": 50_000_000,
    }, index=dates)
    df.index.name = "Date"
    return df


@pytest.mark.anyio
async def test_rolling_risk_happy_path(client: AsyncClient, mock_yf_history):
    df = _make_rolling_mock_df()
    with patch("yfinance.Ticker") as mock_ticker:
        mock_ticker.return_value.history.return_value = df
        resp = await client.get(
            "/api/v1/risk/rolling?ticker=AAPL&benchmark=SPY&window=12mo&period=3y"
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "current_sharpe" in data
    assert "current_volatility_pct" in data
    assert "current_beta" in data
    assert "rolling_sharpe" in data
    assert "rolling_beta" in data
    assert len(data["rolling_sharpe"]["dates"]) > 0


@pytest.mark.anyio
async def test_rolling_risk_default_params(client: AsyncClient, mock_yf_history):
    df = _make_rolling_mock_df()
    with patch("yfinance.Ticker") as mock_ticker:
        mock_ticker.return_value.history.return_value = df
        resp = await client.get("/api/v1/risk/rolling")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert data["benchmark"] == "SPY"


@pytest.mark.anyio
async def test_rolling_risk_no_data(client: AsyncClient):
    with patch("yfinance.Ticker") as mock_ticker:
        mock_ticker.return_value.history.return_value = None
        resp = await client.get("/api/v1/risk/rolling?ticker=FAKE")
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data
