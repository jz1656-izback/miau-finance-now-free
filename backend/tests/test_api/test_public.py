import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4


@pytest.fixture(autouse=True)
def mock_public_db():
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    state = {
        "share_found": True,
        "is_public": True,
        "expires_at": None,
    }

    async def mock_exec(*args, **kwargs):
        sql = str(args[0]) if args else ""
        result = MagicMock()

        if "FROM shared_portfolio_views spv" in sql and "WHERE spv.share_token" in sql:
            if not state["share_found"]:
                result.mappings.return_value.first.return_value = None
            else:
                result.mappings.return_value.first.return_value = {
                    "id": str(uuid4()),
                    "portfolio_id": str(uuid4()),
                    "is_public": state["is_public"],
                    "expires_at": state["expires_at"],
                    "created_at": "2025-01-01T00:00:00",
                    "portfolio_name": "Test Portfolio",
                    "owner_name": "testuser",
                }
        elif "FROM positions pos" in sql or "pos.market_value" in sql:
            result.mappings.return_value.all.return_value = [
                {"ticker": "AAPL", "name": "Apple Inc.", "quantity": 100, "market_value": 15000.0},
                {"ticker": "GOOGL", "name": "Alphabet Inc.", "quantity": 50, "market_value": 7500.0},
            ]
        else:
            result.mappings.return_value.first.return_value = None
            result.mappings.return_value.all.return_value = []

        return result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    yield state
    app.dependency_overrides.pop(get_db, None)


@pytest.mark.anyio
async def test_view_shared_portfolio(client: AsyncClient, mock_public_db):
    resp = await client.get(f"/api/v1/public/portfolio/{uuid4()}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["portfolio_name"] == "Test Portfolio"
    assert data["owner"] == "testuser"
    assert len(data["holdings"]) == 2
    assert data["holdings"][0]["ticker"] == "AAPL"


@pytest.mark.anyio
async def test_view_shared_portfolio_not_found(client: AsyncClient, mock_public_db):
    mock_public_db["share_found"] = False
    resp = await client.get(f"/api/v1/public/portfolio/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Share not found"


@pytest.mark.anyio
async def test_view_shared_portfolio_not_public(client: AsyncClient, mock_public_db):
    mock_public_db["is_public"] = False
    resp = await client.get(f"/api/v1/public/portfolio/{uuid4()}")
    assert resp.status_code == 403
    assert resp.json()["detail"] == "This portfolio is not public"


@pytest.mark.anyio
async def test_view_shared_portfolio_expired(client: AsyncClient, mock_public_db):
    from datetime import datetime, timezone, timedelta
    mock_public_db["expires_at"] = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    resp = await client.get(f"/api/v1/public/portfolio/{uuid4()}")
    assert resp.status_code == 410
    assert "expired" in resp.json()["detail"].lower()


@pytest.mark.anyio
async def test_view_shared_portfolio_not_expired(client: AsyncClient, mock_public_db):
    from datetime import datetime, timezone, timedelta
    mock_public_db["expires_at"] = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    resp = await client.get(f"/api/v1/public/portfolio/{uuid4()}")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_view_shared_portfolio_empty_holdings(client: AsyncClient, mock_public_db):
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    async def empty_holdings_exec(*args, **kwargs):
        sql = str(args[0]) if args else ""
        r = MagicMock()
        if "FROM shared_portfolio_views spv" in sql:
            r.mappings.return_value.first.return_value = {
                "id": str(uuid4()),
                "portfolio_id": str(uuid4()),
                "is_public": True,
                "expires_at": None,
                "created_at": "2025-01-01T00:00:00",
                "portfolio_name": "Empty",
                "owner_name": "user",
            }
        else:
            r.mappings.return_value.all.return_value = []
        return r

    mock_session.execute.side_effect = empty_holdings_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    resp = await client.get(f"/api/v1/public/portfolio/{uuid4()}")
    assert resp.status_code == 200
    assert resp.json()["holdings"] == []
    app.dependency_overrides[get_db] = lambda: mock_session
