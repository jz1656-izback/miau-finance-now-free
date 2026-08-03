import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4


@pytest.fixture(autouse=True)
def mock_social_db():
    from app.main import app
    from app.database import get_db
    from app.middleware.rbac import get_current_user_db

    mock_sesh = MagicMock()
    mock_sesh.execute = AsyncMock()
    mock_sesh.commit = AsyncMock()

    async def mock_exec(*args, **kwargs):
        result = MagicMock()
        sql = str(args[0]) if args else ""
        if "INSERT INTO shared_portfolio_views" in sql:
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()),
                "portfolio_id": str(uuid4()),
                "share_token": "test-token",
                "is_public": True,
                "expires_at": None,
                "created_at": "2025-01-01T00:00:00",
            }
        elif "INSERT INTO social_activities" in sql:
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()),
                "user_id": str(uuid4()),
                "action_type": "trade_executed",
                "resource_type": "trade",
                "resource_id": str(uuid4()),
                "details": {},
                "visibility": "public",
                "created_at": "2025-01-01T00:00:00",
            }
        elif "INSERT INTO comments" in sql:
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()),
                "activity_id": str(uuid4()),
                "user_id": str(uuid4()),
                "text": "test comment",
                "parent_id": None,
                "created_at": "2025-01-01T00:00:00",
            }
        elif "INSERT INTO follows" in sql:
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()),
                "follower_id": str(uuid4()),
                "followed_id": str(uuid4()),
                "created_at": "2025-01-01T00:00:00",
            }
        elif "spv.id" in sql or "shared_portfolio_views" in sql:
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()),
                "portfolio_id": str(uuid4()),
                "share_token": "test-token",
                "is_public": True,
                "expires_at": None,
                "created_at": "2025-01-01T00:00:00",
                "portfolio_name": "Test Portfolio",
                "owner_name": "testuser",
            }
        elif "FROM positions" in sql or "pos.market_value" in sql:
            result.mappings.return_value.all.return_value = [
                {"ticker": "AAPL", "name": "Apple Inc.", "quantity": 100, "market_value": 15000.0},
            ]
        elif "COUNT" in sql or (args and "scalar" in str(args[0]).lower()):
            result.scalar.return_value = 5
        else:
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()),
                "username": "testuser",
                "email": "test@test.com",
                "role": "user",
            }
        result.mappings.return_value.all.return_value = []
        result.scalar.return_value = 0
        result.rowcount = 1
        return result

    mock_sesh.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_sesh
    app.dependency_overrides[get_current_user_db] = lambda: {
        "id": str(uuid4()),
        "username": "testuser",
        "email": "test@test.com",
        "role": "user",
    }
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_create_share_link(mock_social_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/social/share",
            json={"portfolio_id": str(uuid4()), "is_public": True},
        )
        assert resp.status_code in (200, 201, 422)


@pytest.mark.anyio
async def test_get_leaderboard(mock_social_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/social/leaderboard")
        assert resp.status_code == 200
        assert "leaderboard" in resp.json()


@pytest.mark.anyio
async def test_get_leaderboard_defaults(mock_social_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/social/leaderboard")
        assert resp.status_code == 200


@pytest.mark.anyio
async def test_create_activity(mock_social_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            "/api/v1/social/activity",
            json={
                "action_type": "trade_executed",
                "resource_type": "trade",
                "resource_id": str(uuid4()),
                "details": {"ticker": "AAPL"},
            },
        )
        assert resp.status_code in (200, 201, 422)


@pytest.mark.anyio
async def test_get_feed(mock_social_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/social/feed?limit=10")
        assert resp.status_code == 200
        assert "activities" in resp.json()


@pytest.mark.anyio
async def test_follow_user(mock_social_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(f"/api/v1/social/follow/{uuid4()}")
        assert resp.status_code in (200, 201, 400, 404, 409)


@pytest.mark.anyio
async def test_unfollow_user(mock_social_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.delete(f"/api/v1/social/follow/{uuid4()}")
        assert resp.status_code in (200, 404)


@pytest.mark.anyio
async def test_get_reputation(mock_social_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/social/reputation")
        assert resp.status_code == 200


@pytest.mark.anyio
async def test_get_badges(mock_social_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/social/badges")
        assert resp.status_code == 200
        assert "badges" in resp.json()


@pytest.mark.anyio
async def test_get_public_portfolio(mock_social_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get(f"/api/v1/public/portfolio/{uuid4()}")
        assert resp.status_code in (200, 404)


@pytest.mark.anyio
async def test_create_comment(mock_social_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post(
            f"/api/v1/social/feed/{uuid4()}/comment",
            json={"text": "Great trade!"},
        )
        assert resp.status_code in (200, 201, 404, 422)
