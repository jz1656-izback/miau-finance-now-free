import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal

from app.models import OrderType, OrderStatus


def _make_mock_db():
    session = MagicMock()
    session.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        result = MagicMock()
        sql = str(args[0]) if args else ""
        if "current_cash" in sql or "paper_portfolios" in sql:
            result.mappings.return_value.first.return_value = {
                "id": "pf-id",
                "current_cash": 100000.0,
                "initial_cash": 100000.0,
            }
        elif "sum(quantity)" in sql:
            result.scalar.return_value = 0
            return result
        else:
            result.mappings.return_value.first.return_value = {
                "id": "test-id",
                "portfolio_id": "pf-id",
                "instrument_id": "inst-id",
                "order_type": "MARKET",
                "side": "BUY",
                "quantity": 100,
                "price": None,
                "stop_price": None,
                "status": "PENDING",
                "filled_quantity": None,
                "average_fill_price": None,
                "created_at": "2025-01-01T00:00:00",
                "updated_at": None,
            }
            result.mappings.return_value.all.return_value = []
        result.scalar.return_value = 0
        result.rowcount = 1
        return result

    session.execute.side_effect = mock_exec
    return session


@pytest.mark.anyio
async def test_validate_order_valid():
    from app.services.order_service import validate_order

    mock_db = _make_mock_db()
    errors = await validate_order(mock_db, "pf-id", "inst-id", "market", "BUY", 100, None, None)
    assert isinstance(errors, list)


@pytest.mark.anyio
async def test_create_order():
    from app.services.order_service import create_order

    mock_db = _make_mock_db()
    mock_db.commit = AsyncMock()
    order = await create_order(mock_db, "pf-id", "inst-id", "market", "BUY", 100, None, None)
    assert order is not None
    assert order.get("side") == "BUY"


@pytest.mark.anyio
async def test_list_orders():
    from app.services.order_service import list_orders

    mock_db = _make_mock_db()
    orders = await list_orders(mock_db)
    assert isinstance(orders, list)


@pytest.mark.anyio
async def test_get_order():
    from app.services.order_service import get_order

    mock_db = _make_mock_db()
    order = await get_order(mock_db, "test-id")
    assert order is not None
    assert order["id"] == "test-id"


@pytest.mark.anyio
async def test_update_order():
    from app.services.order_service import update_order

    mock_db = _make_mock_db()
    mock_db.commit = AsyncMock()
    order = await update_order(mock_db, "test-id", quantity=Decimal("200"))
    assert order is not None


@pytest.mark.anyio
async def test_cancel_order():
    from app.services.order_service import cancel_order, get_order

    mock_db = _make_mock_db()
    mock_db.commit = AsyncMock()

    with patch("app.services.order_service.get_order") as mock_get:
        mock_get.return_value = {"id": "test-id",             "status": "PENDING", "quantity": 100}
        result = await cancel_order(mock_db, "test-id")
        assert result is not None


@pytest.mark.anyio
async def test_pre_trade_risk_check():
    from app.services.order_service import pre_trade_risk_check

    mock_db = _make_mock_db()
    result = await pre_trade_risk_check(mock_db, "pf-id", "inst-id", "BUY", 100, 150.0)
    assert "passed" in result
    assert "errors" in result
