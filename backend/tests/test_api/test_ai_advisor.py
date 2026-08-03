import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock


@pytest.fixture
def app_client():
    from app.main import app
    from app.middleware.auth import get_current_user

    app.dependency_overrides[get_current_user] = lambda: {"sub": "testuser", "role": "user"}
    transport = ASGITransport(app=app)
    client = AsyncClient(transport=transport, base_url="http://test")
    yield client
    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.anyio
async def test_advisor_portfolio_success(app_client):
    with patch("app.api.analytics.ai_advisor.analyze_portfolio") as mock:
        mock.return_value = {"summary": "test", "risk_level": "low"}
        resp = await app_client.post(
            "/api/v1/ai/advisor/portfolio",
            json={"portfolio_id": "550e8400-e29b-41d4-a716-446655440000"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary"] == "test"
        assert data["risk_level"] == "low"


@pytest.mark.anyio
async def test_advisor_market_success(app_client):
    with patch("app.api.analytics.ai_advisor.analyze_market") as mock:
        mock.return_value = {"market_sentiment": "bullish", "hot_sectors": ["Tech"]}
        resp = await app_client.post("/api/v1/ai/advisor/market", json={})
        assert resp.status_code == 200
        data = resp.json()
        assert data["market_sentiment"] == "bullish"


@pytest.mark.anyio
async def test_advisor_risk_success(app_client):
    with patch("app.api.analytics.ai_advisor.assess_risk") as mock:
        mock.return_value = {"risk_score": 45, "risk_factors": ["volatility"]}
        resp = await app_client.post(
            "/api/v1/ai/advisor/risk",
            json={"portfolio_id": "550e8400-e29b-41d4-a716-446655440000"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["risk_score"] == 45


@pytest.mark.anyio
async def test_ai_query_success(app_client):
    mock_instance = AsyncMock()
    mock_instance.chat.return_value = {"content": "AAPL is trading at $150", "role": "assistant"}

    with patch("app.services.ai.client.AIClient") as mock_cls:
        mock_cls.return_value = mock_instance
        with patch("app.config.settings.ai_api_key", "test-key"):
            resp = await app_client.post(
                "/api/v1/ai/query",
                json={"query": "What is AAPL price?"},
            )
    assert resp.status_code == 200
    data = resp.json()
    assert "response" in data
    assert "AAPL" in data["response"]


@pytest.mark.anyio
async def test_advisor_portfolio_no_auth():
    from app.main import app
    from app.middleware.auth import get_current_user

    app.dependency_overrides.pop(get_current_user, None)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/v1/ai/advisor/portfolio", json={"portfolio_id": "test"})
        assert resp.status_code in (401, 403)
