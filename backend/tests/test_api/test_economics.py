import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock


def _make_yf_chart_response(price: float, prev: float):
    return {
        "chart": {
            "result": [{
                "meta": {
                    "regularMarketPrice": price,
                    "previousClose": prev,
                },
            }],
        },
    }


@pytest.mark.anyio
async def test_commodities_happy_path(client: AsyncClient):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = _make_yf_chart_response(2030.0, 2020.0)

    mock_client = MagicMock()
    mock_client.get.return_value = mock_resp

    with patch("httpx.AsyncClient") as mock:
        mock.return_value.__aenter__.return_value = mock_client
        resp = await client.get("/api/v1/economics/commodities", )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)


@pytest.mark.anyio
async def test_commodities_partial_failure(client: AsyncClient):
    mock_success = MagicMock()
    mock_success.status_code = 200
    mock_success.json.return_value = _make_yf_chart_response(2030.0, 2020.0)

    mock_fail = MagicMock()
    mock_fail.status_code = 404

    mock_client = MagicMock()
    mock_client.get.side_effect = [mock_success] + [mock_fail] * 6

    with patch("httpx.AsyncClient") as mock:
        mock.return_value.__aenter__.return_value = mock_client
        resp = await client.get("/api/v1/economics/commodities", )
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_commodities_all_failures(client: AsyncClient):
    mock_resp = MagicMock()
    mock_resp.status_code = 404

    mock_client = MagicMock()
    mock_client.get.return_value = mock_resp

    with patch("httpx.AsyncClient") as mock:
        mock.return_value.__aenter__.return_value = mock_client
        resp = await client.get("/api/v1/economics/commodities", )
    assert resp.status_code == 200
    assert resp.json() == {}


@pytest.mark.anyio
async def test_treasury_yield_happy_path(client: AsyncClient):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = _make_yf_chart_response(4.25, 4.23)

    mock_client = MagicMock()
    mock_client.get.return_value = mock_resp

    with patch("httpx.AsyncClient") as mock:
        mock.return_value.__aenter__.return_value = mock_client
        resp = await client.get("/api/v1/economics/treasury-yield", )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)


@pytest.mark.anyio
async def test_treasury_yield_all_failures(client: AsyncClient):
    mock_resp = MagicMock()
    mock_resp.status_code = 404

    mock_client = MagicMock()
    mock_client.get.return_value = mock_resp

    with patch("httpx.AsyncClient") as mock:
        mock.return_value.__aenter__.return_value = mock_client
        resp = await client.get("/api/v1/economics/treasury-yield", )
    assert resp.status_code == 200
    assert resp.json() == {}


@pytest.mark.anyio
async def test_market_breadth_happy_path(client: AsyncClient):
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = _make_yf_chart_response(4800.0, 4775.0)

    mock_client = MagicMock()
    mock_client.get.return_value = mock_resp

    with patch("httpx.AsyncClient") as mock:
        mock.return_value.__aenter__.return_value = mock_client
        resp = await client.get("/api/v1/economics/market-breadth", )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)


@pytest.mark.anyio
async def test_market_breadth_partial_data(client: AsyncClient):
    mock_success = MagicMock()
    mock_success.status_code = 200
    mock_success.json.return_value = _make_yf_chart_response(4800.0, 4775.0)

    mock_fail = MagicMock()
    mock_fail.status_code = 404

    mock_client = MagicMock()
    mock_client.get.side_effect = [mock_success] + [mock_fail] * 4

    with patch("httpx.AsyncClient") as mock:
        mock.return_value.__aenter__.return_value = mock_client
        resp = await client.get("/api/v1/economics/market-breadth", )
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_correlation_happy_path(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get(
        "/api/v1/economics/correlation?tickers=AAPL,MSFT,GOOGL",
        
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "tickers" in data
    assert "correlation_matrix" in data


@pytest.mark.anyio
async def test_correlation_single_ticker(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get(
        "/api/v1/economics/correlation?tickers=AAPL", 
    )
    assert resp.status_code == 200
    data = resp.json()
    if "error" in data:
        assert data["error"] == "Need at least 2 tickers"


@pytest.mark.anyio
async def test_correlation_default_tickers(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get("/api/v1/economics/correlation", )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data.get("tickers", [])) >= 2


@pytest.mark.anyio
async def test_gainers_losers_happy_path(
    client: AsyncClient, mock_yf_price
):
    resp = await client.get("/api/v1/economics/gainers-losers", )
    assert resp.status_code == 200
    data = resp.json()
    assert "top_gainers" in data
    assert "top_losers" in data


@pytest.mark.anyio
async def test_fred_indicators_happy_path(client: AsyncClient):
    resp = await client.get("/api/v1/economics/fred?series_ids=GDP,UNRATE&limit=5")
    assert resp.status_code == 200
    data = resp.json()
    assert "series" in data
    assert len(data["series"]) == 2
    for s in data["series"]:
        assert "series_id" in s
        assert "series_name" in s
        assert "observations" in s
        assert len(s["observations"]) <= 5


@pytest.mark.anyio
async def test_fred_indicators_unsupported_series(client: AsyncClient):
    resp = await client.get("/api/v1/economics/fred?series_ids=INVALID&limit=5")
    assert resp.status_code == 200
    data = resp.json()
    assert "series" in data
    assert data["series"][0]["series_id"] == "INVALID"
    assert "error" in data["series"][0]


@pytest.mark.anyio
async def test_fred_indicators_default_series(client: AsyncClient):
    resp = await client.get("/api/v1/economics/fred?limit=3")
    assert resp.status_code == 200
    data = resp.json()
    assert "series" in data
    assert len(data["series"]) >= 1
