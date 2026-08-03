import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

_KEY_ID = str(uuid4())


@pytest.fixture(autouse=True)
def register_router():
    from app.main import app
    from app.api.api_keys import router
    from app.api import api_keys_external as ext
    # Remove conflicting external routes so DB-backed api_keys tests work
    for route in list(app.routes):
        if hasattr(route, 'path') and route.path.startswith('/api/v1/api-keys'):
            app.routes.remove(route)
    app.include_router(router, prefix="/api/v1/dev")


@pytest.fixture(autouse=True)
def mock_api_key_db():
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    state = {"key_found": True}

    async def mock_exec(*args, **kwargs):
        sql = str(args[0]) if args else ""
        params = args[1] if len(args) > 1 else kwargs.get("parameters", {})
        result = MagicMock()
        result.rowcount = 1

        if "INSERT INTO api_keys" in sql and "RETURNING" in sql:
            name = params.get("name", "My API Key") if isinstance(params, dict) else "My API Key"
            result.mappings.return_value.first.return_value = {
                "id": _KEY_ID,
                "name": name,
                "key_prefix": "miau_abc",
                "scopes": ["read"],
                "expires_at": "2026-01-01T00:00:00",
                "created_at": "2025-01-01T00:00:00",
            }
        elif "FROM api_keys" in sql and "WHERE user_id" in sql:
            if state["key_found"]:
                result.mappings.return_value.all.return_value = [
                    {
                        "id": _KEY_ID,
                        "name": "My API Key",
                        "key_prefix": "miau_abc",
                        "scopes": ["read"],
                        "expires_at": "2026-01-01T00:00:00",
                        "created_at": "2025-01-01T00:00:00",
                    }
                ]
            else:
                result.mappings.return_value.all.return_value = []
        elif "DELETE FROM api_keys" in sql:
            result.rowcount = 1 if state["key_found"] else 0
        else:
            result.mappings.return_value.first.return_value = None
            result.mappings.return_value.all.return_value = []

        return result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    yield state
    app.dependency_overrides.pop(get_db, None)


@pytest.mark.anyio
async def test_create_api_key(mock_api_key_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/dev/api-keys",
            json={"name": "My API Key", "scopes": ["read"], "expires_in_days": 365},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "My API Key"
        assert data["key"].startswith("miau_")
        assert "raw_key" in data


@pytest.mark.anyio
async def test_create_api_key_default_scopes(mock_api_key_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/dev/api-keys",
            json={"name": "Minimal Key"},
        )
        assert resp.status_code == 200
        assert resp.json()["name"] == "Minimal Key"


@pytest.mark.anyio
async def test_create_api_key_missing_name(mock_api_key_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/dev/api-keys",
            json={},
        )
        assert resp.status_code == 422


@pytest.mark.anyio
async def test_create_api_key_format(mock_api_key_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/dev/api-keys",
            json={"name": "Format Check"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["key"].startswith("miau_")
        assert len(data["key"]) > 8


@pytest.mark.anyio
async def test_list_api_keys(mock_api_key_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/dev/api-keys")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "My API Key"


@pytest.mark.anyio
async def test_list_api_keys_empty(mock_api_key_db):
    mock_api_key_db["key_found"] = False
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/dev/api-keys")
        assert resp.status_code == 200
        assert resp.json() == []


@pytest.mark.anyio
async def test_revoke_api_key(mock_api_key_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.delete(f"/api/v1/dev/api-keys/{_KEY_ID}")
        assert resp.status_code == 200
        assert resp.json()["message"] == "API key deleted"


@pytest.mark.anyio
async def test_revoke_api_key_not_found(mock_api_key_db):
    mock_api_key_db["key_found"] = False
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.delete(f"/api/v1/dev/api-keys/{uuid4()}")
        assert resp.status_code == 404


@pytest.mark.anyio
async def test_revoke_api_key_other_user():
    from app.main import app
    from app.database import get_db
    from app.middleware.auth import get_current_user

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    async def noop_exec(*args, **kwargs):
        r = MagicMock()
        r.rowcount = 0
        return r

    mock_session.execute.side_effect = noop_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    app.dependency_overrides[get_current_user] = lambda: {"sub": "other", "role": "user"}
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.delete(f"/api/v1/dev/api-keys/{uuid4()}")
        assert resp.status_code == 404
    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_current_user, None)
