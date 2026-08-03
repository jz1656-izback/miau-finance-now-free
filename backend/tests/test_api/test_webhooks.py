import hmac
import hashlib
import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

_WEBHOOK_ID = str(uuid4())
_USER_ID = str(uuid4())


@pytest.fixture(autouse=True)
def register_router():
    from app.main import app
    from app.api.webhooks import router
    app.include_router(router, prefix="/api/v1")


@pytest.fixture(autouse=True)
def mock_webhook_db():
    from app.main import app
    from app.database import get_db
    from app.middleware.rbac import get_current_user_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    state = {"webhook_found": True}

    async def mock_exec(*args, **kwargs):
        sql = str(args[0]) if args else ""
        result = MagicMock()
        result.rowcount = 1

        if "SELECT id, username, email, role FROM users" in sql:
            result.mappings.return_value.first.return_value = {
                "id": _USER_ID, "username": "testuser", "email": "test@test.com", "role": "user",
            }
        elif "INSERT INTO webhook_endpoints" in sql:
            result.mappings.return_value.first.return_value = {
                "id": _WEBHOOK_ID,
                "user_id": _USER_ID,
                "url": "https://example.com/hook",
                "events": ["price_alert"],
                "is_active": True,
                "created_at": "2025-01-01T00:00:00",
            }
        elif "FROM webhook_endpoints WHERE user_id" in sql:
            if state["webhook_found"]:
                result.mappings.return_value.all.return_value = [
                    {
                        "id": _WEBHOOK_ID,
                        "url": "https://example.com/hook",
                        "events": ["price_alert"],
                        "is_active": True,
                        "created_at": "2025-01-01T00:00:00",
                    }
                ]
            else:
                result.mappings.return_value.all.return_value = []
        elif "DELETE FROM webhook_endpoints" in sql:
            result.rowcount = 1 if state["webhook_found"] else 0
        else:
            result.mappings.return_value.first.return_value = None
            result.mappings.return_value.all.return_value = []

        return result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    app.dependency_overrides[get_current_user_db] = lambda: {
        "id": _USER_ID, "username": "testuser", "email": "test@test.com", "role": "user",
    }
    yield state
    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_current_user_db, None)


@pytest.mark.anyio
async def test_create_webhook(mock_webhook_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/webhooks",
            params={"url": "https://example.com/hook", "events": ["price_alert", "trade"]},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["url"] == "https://example.com/hook"
        assert "signing_secret" in data


@pytest.mark.anyio
async def test_list_webhooks(mock_webhook_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/webhooks")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 1


@pytest.mark.anyio
async def test_list_webhooks_empty(mock_webhook_db):
    mock_webhook_db["webhook_found"] = False
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/webhooks")
        assert resp.status_code == 200
        assert resp.json() == []


@pytest.mark.anyio
async def test_delete_webhook(mock_webhook_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.delete(f"/api/v1/webhooks/{_WEBHOOK_ID}")
        assert resp.status_code == 200
        assert resp.json()["deleted"] == _WEBHOOK_ID


@pytest.mark.anyio
async def test_delete_webhook_not_found(mock_webhook_db):
    mock_webhook_db["webhook_found"] = False
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.delete(f"/api/v1/webhooks/{uuid4()}")
        assert resp.status_code == 404


@pytest.mark.anyio
async def test_webhook_deliveries(mock_webhook_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get(f"/api/v1/webhooks/{_WEBHOOK_ID}/deliveries")
        assert resp.status_code == 200
        data = resp.json()
        assert data["webhook_id"] == _WEBHOOK_ID
        assert "deliveries" in data


@pytest.mark.anyio
async def test_create_webhook_missing_url(mock_webhook_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/v1/webhooks")
        assert resp.status_code == 422


@pytest.mark.anyio
async def test_delete_webhook_other_user():
    from app.main import app
    from app.database import get_db
    from app.middleware.rbac import get_current_user_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    async def noop_exec(*args, **kwargs):
        r = MagicMock()
        r.rowcount = 0
        return r

    mock_session.execute.side_effect = noop_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    app.dependency_overrides[get_current_user_db] = lambda: {
        "id": str(uuid4()), "username": "other", "email": "o@t.com", "role": "user",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.delete(f"/api/v1/webhooks/{uuid4()}")
        assert resp.status_code == 404
    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_current_user_db, None)


def test_verify_signature():
    from app.api.webhooks import verify_signature
    secret = "test-secret-123"
    payload = b'{"event": "price_alert"}'
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    assert verify_signature(payload, expected, secret) is True
    assert verify_signature(payload, "bad-signature", secret) is False
    assert verify_signature(payload, expected, "wrong-secret") is False
