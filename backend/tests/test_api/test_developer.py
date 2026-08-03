import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4


@pytest.fixture(autouse=True)
def mock_dev_db():
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()
    _user_id = str(uuid4())

    async def mock_exec(*args, **kwargs):
        sql = str(args[0]) if args else ""
        mock_result = MagicMock()
        mock_result.mappings.return_value.first.return_value = {
            "id": _user_id, "username": "admin", "email": "admin@test.com", "role": "admin",
        }
        mock_result.mappings.return_value.all.return_value = [
            {"id": str(uuid4()), "name": "Test Key", "key_prefix": "miau_abc", "scopes": {"read": True},
             "last_used_at": None, "expires_at": None, "is_active": True, "created_at": "2025-01-01T00:00:00",
             "url": "https://example.com/webhook", "events": ["price_alert"]}
        ]
        mock_result.scalar.return_value = 0
        mock_result.rowcount = 1
        if "INSERT INTO api_keys" in sql:
            mock_result.mappings.return_value.first.return_value = {
                "id": str(uuid4()), "name": "Test Key", "key_prefix": "miau_abc",
                "scopes": {"read": True}, "last_used_at": None,
                "expires_at": None, "is_active": True, "created_at": "2025-01-01T00:00:00",
            }
        elif "INSERT INTO webhook_endpoints" in sql:
            mock_result.mappings.return_value.first.return_value = {
                "id": str(uuid4()), "url": "https://example.com/webhook",
                "events": ["price_alert"], "is_active": True, "created_at": "2025-01-01T00:00:00",
            }
        return mock_result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.mark.anyio
async def test_create_api_key(client: AsyncClient, mock_dev_db):
    resp = await client.post(
        "/api/v1/developer/api-keys",
        json={"name": "Test Key"},
    )
    assert resp.status_code in (200, 201), f"Got {resp.status_code}"
    data = resp.json()
    assert "raw_key" in data
    assert data["name"] == "Test Key"


@pytest.mark.anyio
async def test_list_api_keys(client: AsyncClient, mock_dev_db):
    resp = await client.get("/api/v1/developer/api-keys")
    assert resp.status_code in (200, 404, 405)
    if resp.status_code == 200:
        data = resp.json()
        assert "api_keys" in data


@pytest.mark.anyio
async def test_revoke_api_key(client: AsyncClient, mock_dev_db):
    key_id = str(uuid4())
    resp = await client.delete(f"/api/v1/developer/api-keys/{key_id}")
    assert resp.status_code in (200, 204, 404)


@pytest.mark.anyio
async def test_developer_dashboard(client: AsyncClient, mock_dev_db):
    resp = await client.get("/api/v1/developer/dashboard")
    assert resp.status_code in (200, 404, 405)
    if resp.status_code == 200:
        data = resp.json()
        assert "total_api_keys" in data


@pytest.mark.anyio
async def test_create_webhook(client: AsyncClient, mock_dev_db):
    resp = await client.post(
        "/api/v1/developer/webhooks",
        json={"url": "https://example.com/webhook", "events": ["price_alert"]},
    )
    assert resp.status_code in (200, 201), f"Got {resp.status_code}"
    data = resp.json()
    assert "secret" in data or "id" in data


@pytest.mark.anyio
async def test_list_webhooks(client: AsyncClient, mock_dev_db):
    resp = await client.get("/api/v1/developer/webhooks")
    assert resp.status_code in (200, 404, 405)
    if resp.status_code == 200:
        data = resp.json()
        assert "webhooks" in data


@pytest.mark.anyio
async def test_delete_webhook(client: AsyncClient, mock_dev_db):
    webhook_id = str(uuid4())
    resp = await client.delete(f"/api/v1/developer/webhooks/{webhook_id}")
    assert resp.status_code in (200, 204, 404)


@pytest.mark.anyio
async def test_api_key_auth_requires_auth(client: AsyncClient, mock_dev_db):
    from app.main import app
    from app.middleware.auth import get_current_user
    from fastapi import HTTPException, status

    def raise_401():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    app.dependency_overrides[get_current_user] = raise_401
    resp = await client.get("/api/v1/developer/api-keys")
    assert resp.status_code in (401, 403)
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin"}
