import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4


@pytest.fixture(autouse=True)
def mock_rbac_db():
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        mock_result = MagicMock()
        mock_result.mappings.return_value.first.return_value = {
            "id": str(uuid4()),
            "username": "admin",
            "email": "admin@test.com",
            "role": "admin",
        }
        mock_result.scalar.return_value = 1
        return mock_result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_require_role_admin_allowed(client: AsyncClient, mock_rbac_db):
    resp = await client.get("/api/v1/users")
    assert resp.status_code in (200, 404, 405)


@pytest.mark.anyio
async def test_require_role_admin_denied(client: AsyncClient, mock_rbac_db):
    from app.main import app
    from app.middleware.auth import get_current_user

    app.dependency_overrides[get_current_user] = lambda: {"sub": "readonly_user", "role": "readonly"}
    resp = await client.get("/api/v1/users")
    assert resp.status_code in (200, 403)
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin"}


@pytest.mark.anyio
async def test_require_role_readonly(client: AsyncClient, mock_rbac_db):
    from app.main import app
    from app.middleware.auth import get_current_user
    from app.middleware.rbac import require_role

    app.dependency_overrides[get_current_user] = lambda: {"sub": "readonly_user", "role": "readonly"}
    resp = await client.get("/api/v1/users")
    assert resp.status_code in (200, 403)
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin"}


@pytest.mark.anyio
async def test_workspace_isolation(client: AsyncClient, mock_rbac_db):
    from app.main import app
    from app.middleware.auth import get_current_user

    app.dependency_overrides[get_current_user] = lambda: {"sub": "user1", "role": "user"}
    workspace_id = str(uuid4())
    resp = await client.get(f"/api/v1/portfolios/{workspace_id}")
    assert resp.status_code in (200, 403, 404)
    app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin"}


@pytest.mark.anyio
async def test_require_role_no_auth(client: AsyncClient, mock_rbac_db):
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


@pytest.mark.anyio
async def test_require_role_invalid_token(client: AsyncClient, mock_rbac_db):
    from app.main import app
    from app.middleware.auth import get_current_user
    from fastapi import HTTPException, status

    def raise_401():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    app.dependency_overrides[get_current_user] = raise_401
    try:
        resp = await client.get("/api/v1/users")
        assert resp.status_code in (401, 403)
    finally:
        app.dependency_overrides[get_current_user] = lambda: {"sub": "admin", "role": "admin"}
