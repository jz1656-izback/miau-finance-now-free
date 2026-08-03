import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4


_SHARE_TOKEN = str(uuid4())


@pytest.fixture(autouse=True)
def mock_social_db():
    from app.main import app
    from app.database import get_db
    from app.middleware.rbac import get_current_user_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    async def mock_exec(*args, **kwargs):
        mock_result = MagicMock()
        mock_result.mappings.return_value.first.return_value = {
            "id": str(uuid4()),
            "portfolio_id": str(uuid4()),
            "share_token": _SHARE_TOKEN,
            "is_public": True,
            "share_url": f"/api/v1/public/portfolio/{_SHARE_TOKEN}",
            "expires_at": None,
            "created_at": "2025-01-15T12:00:00",
        }
        mock_result.mappings.return_value.all.return_value = [
            {"id": str(uuid4()), "share_token": _SHARE_TOKEN, "is_public": True}
        ]
        mock_result.scalar.return_value = 1
        mock_result.rowcount = 1
        return mock_result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    app.dependency_overrides[get_current_user_db] = lambda: {
        "id": str(uuid4()),
        "username": "testuser",
        "email": "test@test.com",
        "role": "user",
    }
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_create_share_link(client: AsyncClient, mock_social_db):
    resp = await client.post(
        "/api/v1/social/share",
        json={"portfolio_id": str(uuid4()), "is_public": True},
    )
    assert resp.status_code in (200, 201), f"Got {resp.status_code}"
    data = resp.json()
    assert "share_url" in data or "share_token" in str(data)


@pytest.mark.anyio
async def test_share_link_returns_url(client: AsyncClient, mock_social_db):
    resp = await client.post(
        "/api/v1/social/share",
        json={"portfolio_id": str(uuid4()), "is_public": True},
    )
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert "share_url" in str(data) or "token" in str(data).lower()


@pytest.mark.anyio
async def test_share_requires_auth(client: AsyncClient, mock_social_db):
    from app.main import app
    from app.middleware.auth import get_current_user
    from fastapi import HTTPException, status

    def raise_401():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    app.dependency_overrides[get_current_user] = raise_401
    resp = await client.post(
        "/api/v1/social/share",
        json={"portfolio_id": str(uuid4())},
    )
    assert resp.status_code in (401, 403)
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin"}
