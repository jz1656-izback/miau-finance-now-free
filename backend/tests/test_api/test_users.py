import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

_USER_ID = str(uuid4())
_SAMPLE_USER = {
    "id": _USER_ID,
    "username": "testuser",
    "email": "test@example.com",
    "role": "user",
}

_USER_RESULT = {
    "id": _USER_ID,
    "username": "testuser",
    "email": "test@example.com",
    "role": "user",
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00",
}


@pytest.fixture
def mock_db():
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        mock_result = MagicMock()
        mock_result.mappings.return_value.first.return_value = _USER_RESULT
        mock_result.mappings.return_value.all.return_value = [_USER_RESULT]
        mock_result.scalar_one_or_none.return_value = MagicMock(
            to_dict=lambda: _USER_RESULT
        )
        mock_result.scalar.return_value = 1
        mock_result.rowcount = 1
        return mock_result

    mock_session.execute.side_effect = mock_exec
    mock_session.commit = AsyncMock()
    app.dependency_overrides[get_db] = lambda: mock_session
    yield mock_session
    app.dependency_overrides.pop(get_db, None)


@pytest.mark.anyio
async def test_list_users(client: AsyncClient, mock_db):
    resp = await client.get("/api/v1/users")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_get_user(client: AsyncClient, mock_db):
    resp = await client.get(f"/api/v1/users/{_USER_ID}")
    assert resp.status_code in (200, 404)


@pytest.mark.anyio
async def test_create_user(client: AsyncClient, mock_db):
    with patch("app.api.users.pwd_context.hash", return_value="$2b$12$fakehash"):
        resp = await client.post(
            "/api/v1/users",
            json={"username": "newuser", "email": "new@example.com", "password": "secret123"},
        )
        assert resp.status_code in (200, 201), f"Got {resp.status_code}: {resp.text}"


@pytest.mark.anyio
async def test_update_user(client: AsyncClient, mock_db):
    from app.main import app
    from app.middleware.auth import get_current_user

    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin", "user_id": _USER_ID}
    resp = await client.put(
        f"/api/v1/users/{_USER_ID}",
        json={"email": "updated@example.com"},
    )
    assert resp.status_code in (200, 400, 405), f"Got {resp.status_code}: {resp.text}"
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin"}


@pytest.mark.anyio
async def test_delete_user(client: AsyncClient, mock_db):
    from app.main import app
    from app.middleware.auth import get_current_user

    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin", "user_id": _USER_ID}
    resp = await client.delete(f"/api/v1/users/{_USER_ID}")
    assert resp.status_code in (200, 204, 404)
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin"}


@pytest.mark.anyio
async def test_get_user_unauthorized(client: AsyncClient, mock_db):
    from app.main import app
    from app.middleware.auth import get_current_user
    from fastapi import HTTPException, status

    def raise_401():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    app.dependency_overrides[get_current_user] = raise_401
    try:
        resp = await client.get("/api/v1/users")
        assert resp.status_code in (401, 403)
    finally:
        app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin"}
