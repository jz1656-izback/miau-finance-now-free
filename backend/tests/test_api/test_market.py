import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_live_prices_happy_path(
    client: AsyncClient, mock_yf_price
):
    resp = await client.get("/api/v1/market/live?tickers=AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert "data" in data
    assert "AAPL" in data["data"]
    assert data["data"]["AAPL"]["price"] == 150.25
    assert data["data"]["AAPL"]["change_pct"] == 1.18
    assert "as_of" in data


@pytest.mark.anyio
async def test_live_prices_multiple_tickers(
    client: AsyncClient, mock_yf_price
):
    resp = await client.get("/api/v1/market/live?tickers=AAPL,MSFT")
    assert resp.status_code == 200
    data = resp.json()
    assert "AAPL" in data["data"]
    assert "MSFT" in data["data"]


@pytest.mark.anyio
async def test_live_prices_default_tickers(
    client: AsyncClient, mock_yf_price
):
    resp = await client.get("/api/v1/market/live")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_historical_happy_path(
    client: AsyncClient, mock_yf_history
):
    resp = await client.get("/api/v1/market/historical/AAPL?period=1mo")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert len(data["records"]) == 3
    assert "close" in data["records"][0]


@pytest.mark.anyio
async def test_historical_empty_returns_error(
    client: AsyncClient,
):
    from unittest.mock import patch
    with patch("app.services.analytics.market_data.get_history", return_value=[]):
        resp = await client.get("/api/v1/market/historical/INVALID?period=1mo")
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data or len(data.get("records", [])) == 0


@pytest.mark.anyio
async def test_sectors_happy_path(client: AsyncClient):
    from unittest.mock import patch
    sample = [
        {"ticker": "XLK", "name": "Technology", "price": 200.0, "change_pct": 1.5},
    ]
    with patch("app.services.analytics.data_sources.sector_performance", return_value=sample):
        resp = await client.get("/api/v1/market/sectors")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["ticker"] == "XLK"


@pytest.mark.anyio
async def test_crypto_happy_path(client: AsyncClient):
    from unittest.mock import patch
    sample = {
        "coin": "bitcoin", "price": 45000, "change_24h_pct": 2.5,
        "market_cap": 880000000000, "volume_24h": 30000000000,
        "currency": "USD", "source": "CoinGecko",
    }
    with patch("app.services.analytics.data_sources.coingecko_coin_price", return_value=sample):
        resp = await client.get("/api/v1/market/crypto?coin=bitcoin")
    assert resp.status_code == 200
    data = resp.json()
    assert data["coin"] == "bitcoin"
    assert data["price"] == 45000
    assert data["change_24h_pct"] == 2.5


@pytest.mark.anyio
async def test_crypto_top_happy_path(client: AsyncClient):
    from unittest.mock import patch
    sample = [
        {"rank": 1, "name": "Bitcoin", "symbol": "BTC", "price": 45000,
         "market_cap": 880000000000, "volume_24h": 30000000000,
         "change_24h_pct": 2.5, "high_24h": 46000, "low_24h": 44000,
         "circulating_supply": 19000000},
    ]
    with patch("app.services.analytics.data_sources.coingecko_top_coins", return_value=sample):
        resp = await client.get("/api/v1/market/crypto/top?limit=5")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert data[0]["rank"] == 1


@pytest.mark.anyio
async def test_crypto_market_happy_path(client: AsyncClient):
    from unittest.mock import patch
    sample = {
        "total_market_cap_trillions": 2.5, "total_volume_24h_trillions": 0.15,
        "btc_dominance_pct": 45.0, "active_cryptos": 10000, "markets": 500,
    }
    with patch("app.services.analytics.data_sources.coingecko_market", return_value=sample):
        resp = await client.get("/api/v1/market/crypto/market")
    assert resp.status_code == 200
    data = resp.json()
    assert "btc_dominance_pct" in data


@pytest.mark.anyio
async def test_crypto_fear_greed_happy_path(client: AsyncClient):
    from unittest.mock import patch
    sample = {"value": 65, "classification": "Greed"}
    with patch("app.services.analytics.data_sources.bitcoin_fear_greed_index", return_value=sample):
        resp = await client.get("/api/v1/market/crypto/fear-greed")
    assert resp.status_code == 200
    data = resp.json()
    assert data["value"] == 65


@pytest.mark.anyio
async def test_crypto_historical_happy_path(client: AsyncClient):
    from unittest.mock import patch
    sample = {
        "coin": "bitcoin", "currency": "USD", "days": 7,
        "prices": [
            {"date": "2025-01-15T12:00:00", "price": 45000},
            {"date": "2025-01-14T12:00:00", "price": 44000},
        ],
    }
    with patch("app.services.analytics.data_sources.coingecko_historical", return_value=sample):
        resp = await client.get("/api/v1/market/crypto/historical?coin=bitcoin&days=7")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["prices"]) == 2


@pytest.mark.anyio
async def test_crypto_historical_empty_data(client: AsyncClient):
    from unittest.mock import patch
    sample = {"coin": "bitcoin", "error": "No data", "prices": []}
    with patch("app.services.analytics.data_sources.coingecko_historical", return_value=sample):
        resp = await client.get("/api/v1/market/crypto/historical?coin=invalidcoin")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_forex_happy_path(client: AsyncClient):
    from unittest.mock import patch
    sample = {"base": "USD", "date": "2025-01-15", "rates": {"EUR": 0.92, "GBP": 0.79}}
    with patch("app.services.analytics.data_sources.exchange_rate", return_value=sample):
        resp = await client.get("/api/v1/market/forex?base=USD")
    assert resp.status_code == 200
    data = resp.json()
    assert data["base"] == "USD"
    assert "EUR" in data["rates"]


@pytest.mark.anyio
async def test_forex_with_targets(client: AsyncClient):
    from unittest.mock import patch
    sample = {"base": "USD", "date": "2025-01-15", "rates": {"EUR": 0.92}}
    with patch("app.services.analytics.data_sources.exchange_rate", return_value=sample):
        resp = await client.get("/api/v1/market/forex?base=USD&targets=EUR,GBP")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_market_indicators_happy_path(client: AsyncClient):
    from unittest.mock import patch
    sample = {"sp500": {"value": 4800.0, "change": 20.0, "change_pct": 0.42}}
    with patch("app.services.analytics.data_sources.us_indicators", return_value=sample):
        resp = await client.get("/api/v1/market/indicators")
    assert resp.status_code == 200
    data = resp.json()
    assert "sp500" in data


@pytest.mark.anyio
async def test_market_indicators_empty(client: AsyncClient):
    from unittest.mock import patch
    with patch("app.services.analytics.data_sources.us_indicators", return_value={}):
        resp = await client.get("/api/v1/market/indicators")
    assert resp.status_code == 200
    assert resp.json() == {}


@pytest.mark.anyio
async def test_movers_happy_path(client: AsyncClient, mock_yf_price):
    resp = await client.get("/api/v1/market/movers")
    assert resp.status_code == 200
