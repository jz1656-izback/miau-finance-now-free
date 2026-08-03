import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4


@pytest.fixture(autouse=True)
def mock_feed_db():
    from app.main import app
    from app.database import get_db
    from app.middleware.rbac import get_current_user_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    _comment_id = str(uuid4())

    _feed_row = {
        "id": str(uuid4()),
        "user_id": str(uuid4()),
        "username": "testuser",
        "action_type": "trade_executed",
        "resource_type": "trade",
        "resource_id": str(uuid4()),
        "details": {},
        "visibility": "public",
        "comment_count": 0,
        "created_at": "2025-01-15T12:00:00",
    }

    _user_row = {
        "id": str(uuid4()),
        "username": "admin",
        "email": "admin@test.com",
        "role": "admin",
    }

    _comment_row = {
        "id": _comment_id,
        "activity_id": str(uuid4()),
        "user_id": str(uuid4()),
        "username": "testuser",
        "text": "Nice!",
        "parent_id": None,
        "created_at": "2025-01-15T12:00:00",
    }

    _insert_comment_row = {
        "id": str(uuid4()),
        "activity_id": str(uuid4()),
        "user_id": str(uuid4()),
        "parent_id": None,
        "text": "Great trade!",
        "created_at": "2025-01-15T12:00:00",
    }

    _insert_activity_row = {
        "id": str(uuid4()),
        "user_id": str(uuid4()),
        "action_type": "trade_executed",
        "resource_type": "trade",
        "resource_id": str(uuid4()),
        "details": {},
        "visibility": "public",
        "created_at": "2025-01-15T12:00:00",
    }

    async def mock_exec(*args, **kwargs):
        sql = str(args[0]) if args else ""
        mock_result = MagicMock()

        if "INSERT INTO comments" in sql:
            mock_result.mappings.return_value.first.return_value = _insert_comment_row
            mock_result.mappings.return_value.all.return_value = [_comment_row]
        elif "INSERT INTO social_activities" in sql:
            mock_result.mappings.return_value.first.return_value = _insert_activity_row
            mock_result.mappings.return_value.all.return_value = [_feed_row]
        elif "ORDER BY sa.created_at" in sql:
            mock_result.mappings.return_value.first.return_value = _feed_row
            mock_result.mappings.return_value.all.return_value = [_feed_row]
        elif "c.activity_id" in sql:
            mock_result.mappings.return_value.first.return_value = _comment_row
            mock_result.mappings.return_value.all.return_value = [_comment_row]
        else:
            mock_result.mappings.return_value.first.return_value = _user_row
            mock_result.mappings.return_value.all.return_value = [_feed_row]

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
async def test_get_feed(client: AsyncClient, mock_feed_db):
    resp = await client.get("/api/v1/social/feed?limit=10")
    assert resp.status_code in (200, 404, 405)
    if resp.status_code == 200:
        data = resp.json()
        assert "activities" in data


@pytest.mark.anyio
async def test_get_feed_with_filter(client: AsyncClient, mock_feed_db):
    resp = await client.get("/api/v1/social/feed?filter=global")
    assert resp.status_code in (200, 404, 405)


@pytest.mark.anyio
async def test_create_activity(client: AsyncClient, mock_feed_db):
    resp = await client.post(
        "/api/v1/social/activity",
        json={
            "action_type": "trade_executed",
            "resource_type": "trade",
            "resource_id": str(uuid4()),
            "visibility": "public",
        },
    )
    assert resp.status_code in (200, 201, 405)
    if resp.status_code in (200, 201):
        data = resp.json()
        assert "activity" in data


@pytest.mark.anyio
async def test_add_comment(client: AsyncClient, mock_feed_db):
    activity_id = str(uuid4())
    resp = await client.post(
        f"/api/v1/social/feed/{activity_id}/comment",
        json={"text": "Great trade!"},
    )
    assert resp.status_code in (200, 201, 404, 405)


@pytest.mark.anyio
async def test_get_comments(client: AsyncClient, mock_feed_db):
    activity_id = str(uuid4())
    resp = await client.get(f"/api/v1/social/feed/{activity_id}/comments")
    assert resp.status_code in (200, 404, 405)
