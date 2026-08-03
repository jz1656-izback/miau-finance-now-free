import pytest
from httpx import AsyncClient
from unittest.mock import patch

_MOCK_DIVIDENDS = {
    "dividendYield": 0.005,
    "dividendRate": 0.96,
    "payoutRatio": 0.15,
    "exDividendDate": "2025-02-10",
    "lastDividendDate": "2025-01-15",
    "fiveYearAvgDividendYield": 0.006,
    "trailingAnnualDividendYield": 0.005,
    "currentPrice": 150.0,
    "beta": 1.2,
    "marketCap": 2_500_000_000_000,
    "sector": "Technology",
    "shortName": "Apple Inc.",
}

_MOCK_MULTI_DIVIDENDS = {
    "AAPL": {
        "dividendYield": 0.005, "dividendRate": 0.96, "payoutRatio": 0.15,
        "exDividendDate": "2025-02-10", "currentPrice": 150.0,
        "shortName": "Apple Inc.",
    },
    "MSFT": {
        "dividendYield": 0.008, "dividendRate": 3.0, "payoutRatio": 0.30,
        "exDividendDate": "2025-02-15", "currentPrice": 400.0,
        "shortName": "Microsoft Corp.",
    },
}


@pytest.mark.anyio
async def test_dividend_info_happy_path(client: AsyncClient):
    with patch("app.api.analytics.dividends.yf_info", return_value=_MOCK_DIVIDENDS):
        resp = await client.get("/api/v1/analytics/dividends/AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "dividend_yield" in data
    assert "dividend_rate" in data
    assert "payout_ratio" in data
    assert data["dividend_yield"] == 0.5
    assert data["dividend_rate"] == 0.96


@pytest.mark.anyio
async def test_dividend_info_empty(client: AsyncClient):
    with patch("app.api.analytics.dividends.yf_info", return_value={}):
        resp = await client.get("/api/v1/analytics/dividends/EMPTYDIV")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "EMPTYDIV"
    assert data["dividend_yield"] == 0
    assert data["dividend_rate"] == 0


@pytest.mark.anyio
async def test_dividend_calendar(client: AsyncClient):
    async def mock_yf_info(ticker):
        return _MOCK_MULTI_DIVIDENDS.get(ticker.upper(), {})

    with patch("app.api.analytics.dividends.yf_info", side_effect=mock_yf_info):
        resp = await client.get(
            "/api/v1/analytics/dividends/calendar?tickers=AAPL,MSFT"
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["tickers"] == 2
    assert "holdings" in data
    assert len(data["holdings"]) == 2


@pytest.mark.anyio
async def test_dividend_calendar_defaults(client: AsyncClient):
    async def mock_yf_info(ticker):
        return _MOCK_MULTI_DIVIDENDS.get(ticker.upper(), {})

    with patch("app.api.analytics.dividends.yf_info", side_effect=mock_yf_info):
        resp = await client.get("/api/v1/analytics/dividends/calendar")
    assert resp.status_code == 200
    data = resp.json()
    assert "holdings" in data
