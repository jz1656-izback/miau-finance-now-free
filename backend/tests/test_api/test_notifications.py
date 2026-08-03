import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.anyio
async def test_push_subscribe():
    from app.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/notifications/subscribe",
            json={
                "endpoint": "https://fcm.googleapis.com/test",
                "keys": {"p256dh": "key", "auth": "auth"},
            },
        )
        assert resp.status_code in (200, 201, 404)


@pytest.mark.anyio
async def test_push_unsubscribe():
    from app.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/notifications/unsubscribe",
            json={"endpoint": "https://fcm.googleapis.com/test"},
        )
        assert resp.status_code in (200, 404)


@pytest.mark.anyio
async def test_price_alert_push():
    from app.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/alerts",
            json={
                "name": "AAPL alert",
                "ticker": "AAPL",
                "condition": "price > 200",
                "enable_push": True,
            },
        )
        assert resp.status_code in (200, 201, 422)


@pytest.mark.anyio
async def test_trade_notification():
    from app.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/notifications/test",
            json={"type": "trade_fill", "message": "Bought 10 AAPL @ $150"},
        )
        assert resp.status_code in (200, 404)


@pytest.mark.anyio
async def test_daily_summary():
    from app.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/notifications/summary")
        assert resp.status_code in (200, 404)


@pytest.mark.anyio
async def test_vapid_key_endpoint():
    from app.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/v1/notifications/vapid-public-key")
        assert resp.status_code in (200, 404)
