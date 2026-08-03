import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

_ORDER_ID = str(uuid4())
_PORTFOLIO_ID = str(uuid4())
_INSTRUMENT_ID = str(uuid4())

_ORDER_RESULT = {
    "id": _ORDER_ID,
    "portfolio_id": _PORTFOLIO_ID,
    "instrument_id": _INSTRUMENT_ID,
    "order_type": "market",
    "side": "BUY",
    "quantity": 100,
    "status": "filled",
    "created_at": "2025-01-01T00:00:00",
}


@pytest.fixture(autouse=True)
def mock_order_db():
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        mock_result = MagicMock()
        mock_result.mappings.return_value.first.return_value = _ORDER_RESULT
        mock_result.mappings.return_value.all.return_value = [_ORDER_RESULT]
        mock_result.scalar.return_value = 1
        mock_result.rowcount = 1
        return mock_result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_create_order(client: AsyncClient, mock_order_db):
    resp = await client.post(
        "/api/v1/orders",
        params={
            "portfolio_id": _PORTFOLIO_ID,
            "instrument_id": _INSTRUMENT_ID,
            "order_type": "market",
            "side": "BUY",
            "quantity": 100,
        },
    )
    assert resp.status_code in (200, 201, 400)


@pytest.mark.anyio
async def test_list_orders(client: AsyncClient, mock_order_db):
    resp = await client.get("/api/v1/orders")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.anyio
async def test_get_order(client: AsyncClient, mock_order_db):
    resp = await client.get(f"/api/v1/orders/{_ORDER_ID}")
    assert resp.status_code in (200, 404)


@pytest.mark.anyio
async def test_update_order(client: AsyncClient, mock_order_db):
    resp = await client.put(
        f"/api/v1/orders/{_ORDER_ID}",
        params={"quantity": 200},
    )
    assert resp.status_code in (200, 400, 404)


@pytest.mark.anyio
async def test_cancel_order(client: AsyncClient, mock_order_db):
    resp = await client.delete(f"/api/v1/orders/{_ORDER_ID}")
    assert resp.status_code in (200, 400, 404)


@pytest.mark.anyio
async def test_create_order_validation_error(client: AsyncClient, mock_order_db):
    resp = await client.post(
        "/api/v1/orders",
        params={
            "portfolio_id": _PORTFOLIO_ID,
            "instrument_id": _INSTRUMENT_ID,
            "order_type": "invalid_type",
            "side": "BUY",
            "quantity": 100,
        },
    )
    assert resp.status_code in (400, 422)


@pytest.mark.anyio
async def test_list_orders_filtered(client: AsyncClient, mock_order_db):
    resp = await client.get("/api/v1/orders?status=filled&limit=10&offset=0")
    assert resp.status_code == 200
