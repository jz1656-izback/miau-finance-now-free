"""Tests for data feed endpoints: options, FRED, SEC filings, insider trades."""
import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch


# ── Options Chain ─────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_options_chain_happy_path(client: AsyncClient):
    sample = {
        "ticker": "AAPL",
        "underlying_price": 150.25,
        "expiration_dates": [1735689600],
        "calls": [{"strike": 155, "last_price": 2.5, "volume": 1000}],
        "puts": [{"strike": 145, "last_price": 1.8, "volume": 500}],
    }
    with patch("app.services.data_sources.options.get_options_chain", new_callable=AsyncMock) as mock:
        mock.return_value = sample
        resp = await client.get("/api/v1/options/AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "calls" in data
    assert "puts" in data


@pytest.mark.anyio
async def test_options_chain_with_expiration(client: AsyncClient):
    sample = {"ticker": "AAPL", "calls": [], "puts": []}
    with patch("app.services.data_sources.options.get_options_chain", new_callable=AsyncMock) as mock:
        mock.return_value = sample
        resp = await client.get("/api/v1/options/AAPL?expiration=1735689600")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_options_chain_error(client: AsyncClient):
    sample = {"ticker": "FAKE", "error": "No data", "calls": [], "puts": []}
    with patch("app.services.data_sources.options.get_options_chain", new_callable=AsyncMock) as mock:
        mock.return_value = sample
        resp = await client.get("/api/v1/options/FAKE")
    assert resp.status_code == 200
    assert "error" in resp.json()


# ── FRED Economic Data ───────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_fred_happy_path(client: AsyncClient):
    sample = {
        "series": [
            {"series_id": "GDP", "series_name": "Gross Domestic Product", "observations": [{"date": "2024-01-01", "value": 28000.0}]},
        ],
    }
    with patch("app.services.data_sources.fred.get_observations", new_callable=AsyncMock) as mock:
        mock.return_value = sample
        resp = await client.get("/api/v1/economics/fred?series_ids=GDP&limit=10")
    assert resp.status_code == 200
    data = resp.json()
    assert "series" in data
    assert data["series"][0]["series_id"] == "GDP"


@pytest.mark.anyio
async def test_fred_unsupported_series(client: AsyncClient):
    with patch("app.services.data_sources.fred.get_observations", new_callable=AsyncMock) as mock:
        mock.return_value = {
            "series": [{"series_id": "UNKNOWN", "error": "Unsupported series", "observations": []}],
        }
        resp = await client.get("/api/v1/economics/fred?series_ids=UNKNOWN")
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data["series"][0]


# ── SEC Filings ──────────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_sec_filings_happy_path(client: AsyncClient):
    sample = {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "filings": [{"filing_type": "10-K", "filing_date": "2024-10-25", "description": "Annual report"}],
        "source": "SEC EDGAR",
    }
    with patch("app.services.data_sources.sec_edgar.get_filings", new_callable=AsyncMock) as mock:
        mock.return_value = sample
        resp = await client.get("/api/v1/fundamentals/AAPL/filings")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert len(data["filings"]) > 0


@pytest.mark.anyio
async def test_sec_filings_with_types(client: AsyncClient):
    sample = {"ticker": "AAPL", "filings": [], "source": "SEC EDGAR"}
    with patch("app.services.data_sources.sec_edgar.get_filings", new_callable=AsyncMock) as mock:
        mock.return_value = sample
        resp = await client.get("/api/v1/fundamentals/AAPL/filings?filing_types=10-K,10-Q&limit=5")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_sec_filings_not_found(client: AsyncClient):
    sample = {"ticker": "FAKE", "filings": [], "note": "CIK not found"}
    with patch("app.services.data_sources.sec_edgar.get_filings", new_callable=AsyncMock) as mock:
        mock.return_value = sample
        resp = await client.get("/api/v1/fundamentals/FAKE/filings")
    assert resp.status_code == 200


# ── Insider Trades ───────────────────────────────────────────────────────────

@pytest.mark.anyio
async def test_insider_trades_happy_path(client: AsyncClient):
    sample = {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "trades": [{"filing_date": "2024-12-01", "transaction_type": "Buy", "shares": 1000}],
        "source": "SEC EDGAR",
    }
    with patch("app.services.data_sources.insider.get_insider_trades", new_callable=AsyncMock) as mock:
        mock.return_value = sample
        resp = await client.get("/api/v1/fundamentals/AAPL/insider-trades")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "trades" in data


@pytest.mark.anyio
async def test_insider_trades_not_found(client: AsyncClient):
    sample = {"ticker": "FAKE", "error": "CIK not found", "trades": []}
    with patch("app.services.data_sources.insider.get_insider_trades", new_callable=AsyncMock) as mock:
        mock.return_value = sample
        resp = await client.get("/api/v1/fundamentals/FAKE/insider-trades")
    assert resp.status_code == 200
    assert "error" in resp.json()
