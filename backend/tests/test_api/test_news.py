import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock


@pytest.mark.anyio
async def test_market_news_happy_path(client: AsyncClient):
    sample = [
        {
            "title": "Market Update",
            "publisher": "Yahoo Finance",
            "link": "https://finance.yahoo.com",
            "type": "STORY",
            "summary": "Markets rallied today.",
            "published_at": "2025-01-15T12:00:00",
        },
    ]
    with patch("app.services.analytics.news.yahoo_finance_news") as mock:
        mock.return_value = sample
        resp = await client.get("/api/v1/news/market", )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == "Market Update"


@pytest.mark.anyio
async def test_market_news_empty(client: AsyncClient):
    with patch("app.services.analytics.news.yahoo_finance_news") as mock:
        mock.return_value = []
        resp = await client.get("/api/v1/news/market", )
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.anyio
async def test_company_news_happy_path(
    client: AsyncClient, mock_yahoo_news
):
    resp = await client.get("/api/v1/news/company/AAPL", )
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


@pytest.mark.anyio
async def test_company_news_not_found(client: AsyncClient):
    with patch("app.services.analytics.news.yf.Ticker") as mock:
        instance = MagicMock()
        instance.news = []
        mock.return_value = instance
        resp = await client.get(
            "/api/v1/news/company/FAKE", 
        )
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.anyio
async def test_company_news_with_limit(
    client: AsyncClient, mock_yahoo_news
):
    resp = await client.get(
        "/api/v1/news/company/AAPL?limit=3", 
    )
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_batch_news_happy_path(client: AsyncClient):
    sample = {
        "AAPL": [
            {"title": "Apple News", "publisher": "Reuters", "published_at": "2025-01-15T12:00:00"},
        ],
        "MSFT": [
            {"title": "Microsoft News", "publisher": "Bloomberg", "published_at": "2025-01-15T12:00:00"},
        ],
    }
    with patch("app.services.analytics.news.ticker_news_batch") as mock:
        mock.return_value = sample
        resp = await client.get(
            "/api/v1/news/batch?tickers=AAPL,MSFT", 
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "AAPL" in data
    assert "MSFT" in data


@pytest.mark.anyio
async def test_batch_news_default_tickers(client: AsyncClient):
    sample = {"AAPL": [], "MSFT": [], "GOOGL": []}
    with patch("app.services.analytics.news.ticker_news_batch") as mock:
        mock.return_value = sample
        resp = await client.get("/api/v1/news/batch", )
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_batch_news_empty(client: AsyncClient):
    sample = {}
    with patch("app.services.analytics.news.ticker_news_batch") as mock:
        mock.return_value = sample
        resp = await client.get(
            "/api/v1/news/batch?tickers=FAKE", 
        )
    assert resp.status_code == 200
