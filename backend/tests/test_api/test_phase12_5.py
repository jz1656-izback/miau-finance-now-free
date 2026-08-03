import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock, MagicMock


@pytest.mark.anyio
async def test_scenario_happy_path(client: AsyncClient):
    resp = await client.get("/api/v1/analytics/scenario/AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "scenarios" in data
    assert len(data["scenarios"]) == 6
    assert "worst_case" in data
    assert "best_case" in data
    assert "drawdown_risk" in data


@pytest.mark.anyio
async def test_scenario_custom_shocks(client: AsyncClient):
    resp = await client.get("/api/v1/analytics/scenario/shocks/AAPL?shocks=-0.30,-0.15,0,0.15,0.30")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["scenarios"]) == 5
    labels = [s["label"] for s in data["scenarios"]]
    assert "Shock -30%" in labels
    assert "Shock +0%" in labels
    assert "Shock +30%" in labels


@pytest.mark.anyio
async def test_scenario_no_yf_info(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value={}):
        resp = await client.get("/api/v1/analytics/scenario/UNKNOWN")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "UNKNOWN"
    assert len(data["scenarios"]) == 6


@pytest.mark.anyio
async def test_portfolio_scenario(client: AsyncClient):
    resp = await client.post(
        "/api/v1/analytics/scenario/portfolio?tickers=AAPL&tickers=MSFT&market_shock=-0.10"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "holdings" in data
    assert len(data["holdings"]) == 2
    assert "portfolio_change_pct" in data
    assert "market_shock_pct" in data
    assert data["market_shock_pct"] == -10.0


@pytest.mark.anyio
async def test_portfolio_scenario_with_weights(client: AsyncClient):
    resp = await client.post(
        "/api/v1/analytics/scenario/portfolio?tickers=AAPL&tickers=MSFT&weights=0.6,0.4&market_shock=-0.20"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["holdings"]) == 2
    assert data["market_shock_pct"] == -20.0


@pytest.mark.anyio
async def test_portfolio_scenario_invalid_shock_clamped(client: AsyncClient):
    resp = await client.post(
        "/api/v1/analytics/scenario/portfolio?tickers=AAPL&market_shock=-0.60"
    )
    assert resp.status_code in (200, 422)


@pytest.mark.anyio
async def test_dividend_info(client: AsyncClient, mock_yf_get_info):
    resp = await client.get("/api/v1/analytics/dividends/AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "dividend_yield" in data
    assert "dividend_rate" in data
    assert "payout_ratio" in data


@pytest.mark.anyio
async def test_dividend_info_unknown(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value={}):
        resp = await client.get("/api/v1/analytics/dividends/UNKNOWN")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "UNKNOWN"
    assert data["dividend_yield"] == 0.0


@pytest.mark.anyio
async def test_dividend_calendar_default(client: AsyncClient, mock_yf_get_info):
    resp = await client.get("/api/v1/analytics/dividends/calendar")
    assert resp.status_code == 200
    data = resp.json()
    assert "holdings" in data
    assert data["tickers"] >= 1
    assert "total_annual_income" in data


@pytest.mark.anyio
async def test_dividend_calendar_custom_tickers(client: AsyncClient):
    resp = await client.get("/api/v1/analytics/dividends/calendar?tickers=AAPL,MSFT,GOOGL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["tickers"] == 3
    assert len(data["holdings"]) == 3


@pytest.mark.anyio
async def test_rolling_risk_happy_path(client: AsyncClient):
    with patch("yfinance.Ticker") as mock_ticker:
        instance = MagicMock()
        import pandas as pd
        dates = pd.date_range("2023-01-01", periods=500, freq="B")
        instance.history.return_value = pd.DataFrame({
            "Close": [150 + i * 0.1 for i in range(500)],
        }, index=dates)
        mock_ticker.return_value = instance

        resp = await client.get("/api/v1/risk/rolling?ticker=AAPL&benchmark=SPY&window=12mo&period=3y")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert data["benchmark"] == "SPY"
    assert "current_sharpe" in data
    assert "current_volatility_pct" in data
    assert "current_beta" in data
    assert "rolling_sharpe" in data
    assert "rolling_beta" in data


@pytest.mark.anyio
async def test_rolling_risk_no_data(client: AsyncClient):
    import pandas as pd
    with patch("yfinance.Ticker") as mock_ticker:
        instance = MagicMock()
        instance.history.return_value = pd.DataFrame()
        mock_ticker.return_value = instance

        resp = await client.get("/api/v1/risk/rolling?ticker=FAKE")
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_rolling_risk_custom_window(client: AsyncClient):
    with patch("yfinance.Ticker") as mock_ticker:
        instance = MagicMock()
        import pandas as pd
        dates = pd.date_range("2023-01-01", periods=800, freq="B")
        instance.history.return_value = pd.DataFrame({
            "Close": [200 + i * 0.05 for i in range(800)],
        }, index=dates)
        mock_ticker.return_value = instance

        resp = await client.get("/api/v1/risk/rolling?ticker=MSFT&benchmark=SPY&window=6mo&period=1y")
    assert resp.status_code == 200
    data = resp.json()
    assert data["window"] == "6mo"
    assert data["period"] == "1y"
