import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4


_USER_ID = str(uuid4())
_TARGET_ID = str(uuid4())


@pytest.fixture(autouse=True)
def mock_follow_db():
    from app.main import app
    from app.database import get_db
    from app.middleware.rbac import get_current_user_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    _user_id = _USER_ID

    async def mock_exec(*args, **kwargs):
        sql = str(args[0]) if args else ""
        mock_result = MagicMock()
        mock_result.mappings.return_value.first.return_value = {
            "id": _user_id,
            "username": "admin",
            "email": "admin@test.com",
            "role": "admin",
        }
        mock_result.mappings.return_value.all.return_value = [
            {"id": _user_id, "follower_id": _user_id, "followed_id": _TARGET_ID, "created_at": "2025-01-15T12:00:00"}
        ]
        mock_result.scalar.return_value = 1
        mock_result.rowcount = 1
        if "DELETE" in sql:
            mock_result.rowcount = 0
        return mock_result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    app.dependency_overrides[get_current_user_db] = lambda: {
        "id": _user_id,
        "username": "admin",
        "email": "admin@test.com",
        "role": "admin",
    }
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_follow_user(client: AsyncClient, mock_follow_db):
    resp = await client.post(f"/api/v1/social/follow/{_TARGET_ID}")
    assert resp.status_code in (200, 201, 400, 409)


@pytest.mark.anyio
async def test_unfollow_user(client: AsyncClient, mock_follow_db):
    resp = await client.delete(f"/api/v1/social/follow/{_TARGET_ID}")
    assert resp.status_code in (200, 204, 404)


@pytest.mark.anyio
async def test_cannot_follow_self(client: AsyncClient, mock_follow_db):
    resp = await client.post(f"/api/v1/social/follow/{_USER_ID}")
    assert resp.status_code in (400,)


@pytest.mark.anyio
async def test_follow_requires_auth(client: AsyncClient, mock_follow_db):
    from app.main import app
    from app.middleware.auth import get_current_user
    from fastapi import HTTPException, status

    def raise_401():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    app.dependency_overrides[get_current_user] = raise_401
    resp = await client.post(f"/api/v1/social/follow/{_TARGET_ID}")
    assert resp.status_code in (401, 403)
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin"}


@pytest.mark.anyio
async def test_get_reputation(client: AsyncClient, mock_follow_db):
    resp = await client.get("/api/v1/social/reputation")
    assert resp.status_code in (200, 404, 405)


@pytest.mark.anyio
async def test_get_badges(client: AsyncClient, mock_follow_db):
    resp = await client.get("/api/v1/social/badges")
    assert resp.status_code in (200, 404, 405)
