import pytest
from httpx import AsyncClient, ASGITransport
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
    "revenueGrowth": 0.08,
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "dividendYield": 0.005,
    "dividendRate": 0.96,
    "payoutRatio": 0.15,
    "exDividendDate": "2025-02-10",
    "fiveYearAvgDividendYield": 0.006,
    "trailingAnnualDividendYield": 0.005,
    "priceToBook": 8.0,
    "priceToSalesTrailingMonths": 6.25,
    "enterpriseToEbitda": 20.0,
    "trailingEbitda": 120_000_000_000,
    "totalRevenueTrailingMonths": 400_000_000_000,
}


@pytest.mark.anyio
async def test_wacc_happy_path(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.get("/api/v1/analytics/valuation/wacc/AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "wacc" in data
    assert "cost_of_equity" in data
    assert "cost_of_debt" in data
    assert data["beta"] == 1.2
    assert 0 < data["wacc"] < 1


@pytest.mark.anyio
async def test_wacc_defaults_on_empty(client: AsyncClient):
    with patch("app.services.analytics.valuation.get_financials", return_value={}):
        resp = await client.get("/api/v1/analytics/valuation/wacc/EMPTY3")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "EMPTY3"
    assert 0 < data["wacc"] < 1
    assert data["beta"] == 1.0


@pytest.mark.anyio
async def test_dcf_happy_path(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.get("/api/v1/analytics/valuation/dcf/AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["model"] == "DCF"
    assert data["ticker"] == "AAPL"
    assert "fair_price" in data
    assert "recommendation" in data
    assert "projections" in data
    assert len(data["projections"]) == 5


@pytest.mark.anyio
async def test_dcf_custom_params(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.get(
            "/api/v1/analytics/valuation/dcf/AAPL?growth=0.07&terminal_growth=0.03&years=7"
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["growth_rate"] == 0.07
    assert data["terminal_growth"] == 0.03
    assert data["projection_years"] == 7
    assert len(data["projections"]) == 7


@pytest.mark.anyio
async def test_dcf_with_exit_multiple(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.get("/api/v1/analytics/valuation/dcf/AAPL?exit_multiple=15")
    assert resp.status_code == 200
    data = resp.json()
    assert "fair_price" in data
    assert "recommendation" in data


@pytest.mark.anyio
async def test_dcf_defaults_on_empty(client: AsyncClient):
    with patch("app.services.analytics.valuation.get_financials", return_value={}):
        resp = await client.get("/api/v1/analytics/valuation/dcf/EMPTY1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["model"] == "DCF"
    assert "fair_price" in data


@pytest.mark.anyio
async def test_comps_happy_path(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.get("/api/v1/analytics/valuation/comps/AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "sector" in data
    assert "pe_ratio" in data
    assert "peers" in data
    assert len(data["peers"]) > 0


@pytest.mark.anyio
async def test_comps_defaults_on_empty(client: AsyncClient):
    with patch("app.services.analytics.valuation.get_financials", return_value={}):
        resp = await client.get("/api/v1/analytics/valuation/comps/NODATA2")
    assert resp.status_code == 200
    data = resp.json()
    assert data["sector"] == "Technology"


@pytest.mark.anyio
async def test_lbo_happy_path(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.get("/api/v1/analytics/valuation/lbo/AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["model"] == "LBO"
    assert "moic" in data
    assert "irr_pct" in data
    assert "verdict" in data
    assert "cash_flows" in data
    assert len(data["cash_flows"]) == 5


@pytest.mark.anyio
async def test_lbo_custom_params(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.get(
            "/api/v1/analytics/valuation/lbo/AAPL?debt=0.80&exit_year=7&exit_multiple=12"
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["debt_pct"] == 0.80
    assert data["exit_year"] == 7


@pytest.mark.anyio
async def test_lbo_defaults_on_empty(client: AsyncClient):
    with patch("app.services.analytics.valuation.get_financials", return_value={}):
        resp = await client.get("/api/v1/analytics/valuation/lbo/EMPTY2")
    assert resp.status_code == 200
    data = resp.json()
    assert data["model"] == "LBO"
    assert "moic" in data
    assert "verdict" in data


@pytest.mark.anyio
async def test_dcf_invalid_growth_raises(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.get("/api/v1/analytics/valuation/dcf/AAPL?growth=0.99")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_lbo_invalid_debt_raises(client: AsyncClient):
    with patch("app.services.analytics._yf.get_info", return_value=_MOCK_FINANCIALS):
        resp = await client.get("/api/v1/analytics/valuation/lbo/AAPL?debt=1.5")
    assert resp.status_code == 422
