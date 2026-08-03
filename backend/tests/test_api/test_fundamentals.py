import pytest
from httpx import AsyncClient
from unittest.mock import patch


@pytest.mark.anyio
async def test_company_overview_happy_path(
    client: AsyncClient, mock_yf_get_info
):
    resp = await client.get("/api/v1/fundamentals/AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert data["sector"] == "Technology"
    assert "valuation" in data
    assert "price_targets" in data


@pytest.mark.anyio
async def test_company_overview_no_data(client: AsyncClient):
    with patch("app.services.analytics.fundamentals.get_info", return_value={}):
        resp = await client.get("/api/v1/fundamentals/FAKE")
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_company_overview_valuation_fields(
    client: AsyncClient, mock_yf_get_info
):
    resp = await client.get("/api/v1/fundamentals/AAPL")
    data = resp.json()
    valuation = data.get("valuation", {})
    assert "marketCap" in valuation
    assert "trailingPE" in valuation
    assert "forwardPE" in valuation


@pytest.mark.anyio
async def test_company_overview_price_targets(
    client: AsyncClient, mock_yf_get_info
):
    resp = await client.get("/api/v1/fundamentals/AAPL")
    data = resp.json()
    targets = data.get("price_targets", {})
    assert "targetMeanPrice" in targets
    assert "targetHighPrice" in targets
    assert "targetLowPrice" in targets


@pytest.mark.anyio
async def test_company_overview_employee_count(
    client: AsyncClient, mock_yf_get_info
):
    resp = await client.get("/api/v1/fundamentals/AAPL")
    data = resp.json()
    assert data["employees"] == 150000


@pytest.mark.anyio
async def test_earnings_happy_path(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get("/api/v1/fundamentals/AAPL/earnings")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "records" in data


@pytest.mark.anyio
async def test_earnings_no_data(client: AsyncClient):
    with patch("app.services.analytics.fundamentals.get_history", return_value=[]):
        resp = await client.get("/api/v1/fundamentals/FAKE/earnings")
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data
