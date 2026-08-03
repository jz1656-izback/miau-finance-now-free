import pytest
from datetime import datetime, timezone
from httpx import AsyncClient
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.database import get_db


def _make_mock_exec(results):
    """Create an async execute function that returns sequential mock results."""
    result_mocks = []
    for r in results:
        m = MagicMock()
        if r is None:
            m.fetchone.return_value = None
            m.fetchall.return_value = []
            m.scalar.return_value = 0
        elif isinstance(r, list):
            m.fetchone.return_value = r[0] if r else None
            m.fetchall.return_value = r
            m.scalar.return_value = len(r)
        else:
            m.fetchone.return_value = r
            m.fetchall.return_value = [r]
            m.scalar.return_value = 1
        result_mocks.append(m)

    async def execute(*args, **kwargs):
        if result_mocks:
            return result_mocks.pop(0)
        m = MagicMock()
        m.fetchone.return_value = None
        m.fetchall.return_value = []
        return m

    return execute


@pytest.fixture
def mock_watchlist_db():
    """Mock DB for watchlist tests."""
    mock_session = MagicMock(spec=AsyncSession)
    app.dependency_overrides[get_db] = lambda: mock_session
    yield mock_session
    app.dependency_overrides.pop(get_db, None)


@pytest.mark.anyio
async def test_list_watchlists_empty(client: AsyncClient, mock_watchlist_db):
    mock_watchlist_db.execute = AsyncMock()
    mock_watchlist_db.execute.side_effect = _make_mock_exec([[]])
    resp = await client.get("/api/v1/watchlist")
    assert resp.status_code == 200
    data = resp.json()
    assert data["watchlists"] == []


@pytest.mark.anyio
async def test_list_watchlist_items_empty(client: AsyncClient, mock_watchlist_db):
    mock_watchlist_db.execute = AsyncMock()
    mock_watchlist_db.execute.side_effect = _make_mock_exec([[]])
    resp = await client.get("/api/v1/watchlist/items")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []


@pytest.mark.anyio
async def test_add_watchlist_item_no_watchlist(client: AsyncClient, mock_watchlist_db):
    from uuid import uuid4
    wl_id = str(uuid4())

    mock_watchlist_db.execute = AsyncMock()
    now = datetime.now(timezone.utc)
    mock_watchlist_db.execute.side_effect = _make_mock_exec([
        None,                              # find existing watchlist → None
        (wl_id,),                          # create watchlist → returns ID
        None,                              # check existing ticker → None
        (str(uuid4()), "AAPL", now),       # insert item
    ])

    resp = await client.post("/api/v1/watchlist/items?ticker=AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert "AAPL" in data["message"]


@pytest.mark.anyio
async def test_add_watchlist_item_duplicate(client: AsyncClient, mock_watchlist_db):
    from uuid import uuid4
    wl_id = str(uuid4())

    mock_watchlist_db.execute = AsyncMock()
    mock_watchlist_db.execute.side_effect = _make_mock_exec([
        None,                              # find existing watchlist
        (wl_id,),                          # create watchlist
        (wl_id,),                          # already exists
    ])

    resp = await client.post("/api/v1/watchlist/items?ticker=AAPL")
    assert resp.status_code == 409
    assert "already in watchlist" in resp.json()["detail"]


@pytest.mark.anyio
async def test_remove_watchlist_item(client: AsyncClient, mock_watchlist_db):
    mock_watchlist_db.execute = AsyncMock()
    mock_watchlist_db.execute.side_effect = _make_mock_exec([
        ("AAPL",),  # DELETE RETURNING ticker
    ])

    resp = await client.delete("/api/v1/watchlist/items?ticker=AAPL")
    assert resp.status_code == 200
    data = resp.json()
    assert "Removed AAPL" in data["message"]


@pytest.mark.anyio
async def test_remove_watchlist_item_not_found(client: AsyncClient, mock_watchlist_db):
    mock_watchlist_db.execute = AsyncMock()
    mock_watchlist_db.execute.side_effect = _make_mock_exec([
        None,  # DELETE RETURNING → no rows
    ])

    resp = await client.delete("/api/v1/watchlist/items?ticker=INVALID")
    assert resp.status_code == 404
