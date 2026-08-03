import pytest
from httpx import AsyncClient
from unittest.mock import patch

_MOCK_FINANCIALS = {
    "currentPrice": 150.0,
    "beta": 1.2,
    "marketCap": 2_500_000_000_000,
    "totalDebt": 100_000_000_000,
    "totalCash": 50_000_000_000,
    "freeCashflow": 100_000_000_000,
    "ebitda": 120_000_000_000,
    "totalRevenue": 400_000_000_000,
    "profitMargins": 0.25,
    "trailingEps": 6.0,
    "bookValue": 40.0,
    "sharesOutstanding": 16_000_000_000,
    "sector": "Technology",
    "industry": "Consumer Electronics",
}


@pytest.mark.anyio
async def test_scenario_happy_path(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.get("/api/v1/analytics/scenario/AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "scenarios" in data
    assert len(data["scenarios"]) == 6
    assert "current_price" in data
    assert "worst_case" in data
    assert "best_case" in data
    assert any("Bear" in s["label"] for s in data["scenarios"])


@pytest.mark.anyio
async def test_scenario_shocks_custom(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.get("/api/v1/analytics/scenario/shocks/AAPL?shocks=-0.30,-0.15,0,0.15,0.30")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert len(data["scenarios"]) == 5


@pytest.mark.anyio
async def test_scenario_empty_financials(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value={}):
        resp = await client.get("/api/v1/analytics/scenario/EMPTYSC")
    assert resp.status_code == 200
    data = resp.json()
    assert "scenarios" in data
    assert len(data["scenarios"]) == 6
    assert data["current_price"] == 100.0


@pytest.mark.anyio
async def test_portfolio_scenario(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.post(
            "/api/v1/analytics/scenario/portfolio?tickers=AAPL&tickers=MSFT&market_shock=-0.10"
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["market_shock_pct"] == -10.0
    assert "portfolio_change_pct" in data
    assert "holdings" in data
    assert len(data["holdings"]) == 2


@pytest.mark.anyio
async def test_portfolio_scenario_with_weights(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.post(
            "/api/v1/analytics/scenario/portfolio?tickers=AAPL&tickers=MSFT&tickers=GOOGL&weights=0.5,0.3,0.2"
        )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["holdings"]) == 3
