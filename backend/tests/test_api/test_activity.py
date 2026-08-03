import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

_USER_ID = str(uuid4())


@pytest.fixture(autouse=True)
def mock_activity_db():
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        sql = str(args[0]) if args else ""
        result = MagicMock()

        if "SELECT id FROM users WHERE username" in sql:
            result.mappings.return_value.first.return_value = {
                "id": _USER_ID,
            }
        elif "SELECT COUNT(*) FROM activity_logs" in sql:
            result.scalar.return_value = 10
        else:
            result.mappings.return_value.first.return_value = None
            result.mappings.return_value.all.return_value = []

        return result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.mark.anyio
async def test_list_activity(client: AsyncClient, mock_activity_db):
    with patch("app.api.activity.get_activity") as mock_get:
        mock_get.return_value = [
            {
                "id": str(uuid4()),
                "action": "trade_executed",
                "resource_type": "trade",
                "resource_id": str(uuid4()),
                "details": {"ticker": "AAPL"},
                "created_at": "2025-01-01T00:00:00",
            }
        ]
        resp = await client.get("/api/v1/activity")
        assert resp.status_code == 200
        data = resp.json()
        assert "items" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data
        assert data["total"] == 10
        assert len(data["items"]) == 1


@pytest.mark.anyio
async def test_list_activity_empty(client: AsyncClient, mock_activity_db):
    with patch("app.api.activity.get_activity") as mock_get:
        mock_get.return_value = []
        resp = await client.get("/api/v1/activity")
        assert resp.status_code == 200
        assert resp.json()["items"] == []


@pytest.mark.anyio
async def test_list_activity_pagination(client: AsyncClient, mock_activity_db):
    with patch("app.api.activity.get_activity") as mock_get:
        mock_get.return_value = []
        resp = await client.get("/api/v1/activity?limit=10&offset=20")
        assert resp.status_code == 200
        assert resp.json()["limit"] == 10
        assert resp.json()["offset"] == 20


@pytest.mark.anyio
async def test_list_activity_invalid_limit(client: AsyncClient, mock_activity_db):
    resp = await client.get("/api/v1/activity?limit=300")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_list_activity_invalid_offset(client: AsyncClient, mock_activity_db):
    resp = await client.get("/api/v1/activity?offset=-1")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_list_activity_with_workspace_filter(client: AsyncClient, mock_activity_db):
    with patch("app.api.activity.get_activity") as mock_get:
        mock_get.return_value = [
            {
                "id": str(uuid4()),
                "workspace_id": str(uuid4()),
                "action": "portfolio_updated",
                "resource_type": "portfolio",
                "created_at": "2025-01-01T00:00:00",
            }
        ]
        resp = await client.get("/api/v1/activity", params={"workspace_id": str(uuid4())})
        assert resp.status_code == 200
        assert mock_get.call_count == 1
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["workspace_id"] is not None


@pytest.mark.anyio
async def test_list_activity_default_limit(client: AsyncClient, mock_activity_db):
    with patch("app.api.activity.get_activity") as mock_get:
        mock_get.return_value = []
        resp = await client.get("/api/v1/activity")
        assert resp.status_code == 200
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs["limit"] == 50
        assert call_kwargs["offset"] == 0


@pytest.mark.anyio
async def test_list_activity_unauthorized_no_user(client: AsyncClient, mock_activity_db):
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    async def no_user_exec(*args, **kwargs):
        r = MagicMock()
        r.mappings.return_value.first.return_value = None
        return r

    mock_session.execute.side_effect = no_user_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    resp = await client.get("/api/v1/activity")
    assert resp.status_code == 401
    app.dependency_overrides[get_db] = lambda: mock_session
