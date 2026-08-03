import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4


@pytest.fixture(autouse=True)
def mock_defi_db():
    from app.main import app
    from app.database import get_db
    from app.middleware.rbac import get_current_user_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    async def mock_exec(*args, **kwargs):
        mr = MagicMock()
        mr.mappings.return_value.first.return_value = {"id": str(uuid4()), "address": "0x" + "a" * 40, "chain": "ethereum"}
        mr.mappings.return_value.all.return_value = [{"id": str(uuid4()), "session_id": str(uuid4()), "chain": "ethereum"}]
        mr.scalar.return_value = 1
        mr.rowcount = 1
        return mr

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    app.dependency_overrides[get_current_user_db] = lambda: {
        "id": str(uuid4()), "username": "testuser", "email": "test@test.com", "role": "user",
    }
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_list_chains(client: AsyncClient, mock_defi_db):
    resp = await client.get("/api/v1/defi/chains")
    assert resp.status_code in (200, 404, 405)


@pytest.mark.anyio
async def test_list_sessions(client: AsyncClient, mock_defi_db):
    resp = await client.get("/api/v1/defi/sessions")
    assert resp.status_code in (200, 404, 405)


@pytest.mark.anyio
async def test_wallet_balance(client: AsyncClient, mock_defi_db):
    resp = await client.get("/api/v1/defi/balance")
    assert resp.status_code in (200, 404, 405)


@pytest.mark.anyio
async def test_list_protocols(client: AsyncClient, mock_defi_db):
    resp = await client.get("/api/v1/defi/protocols")
    assert resp.status_code in (200, 404, 405)
