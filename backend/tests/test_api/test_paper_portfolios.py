import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from decimal import Decimal

_PORTFOLIO_ID = str(uuid4())
_USER_ID = str(uuid4())
_INSTRUMENT_ID = str(uuid4())

_PORTFOLIO_ROW = {
    "id": _PORTFOLIO_ID,
    "user_id": _USER_ID,
    "name": "Test Paper Portfolio",
    "initial_cash": "100000.00",
    "current_cash": "100000.00",
    "created_at": "2025-01-01T00:00:00",
    "trade_count": 0,
    "total_bought": 0,
    "total_sold": 0,
}

_TRADE_ROW = {
    "id": str(uuid4()),
    "paper_portfolio_id": _PORTFOLIO_ID,
    "instrument_id": _INSTRUMENT_ID,
    "side": "BUY",
    "quantity": "100",
    "price": "150.50",
    "commission": "7.50",
    "slippage": "1.50",
    "tca_cost": "0.75",
    "executed_at": "2025-01-01T00:00:00",
    "ticker": "AAPL",
    "instrument_name": "Apple Inc.",
}


@pytest.fixture(autouse=True)
def mock_paper_db():
    from app.main import app
    from app.database import get_db
    from app.api.paper_trading import get_current_user_db as pt_get_current_user_db

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    state = {"portfolio_found": True, "portfolio_has_cash": True, "trade_found": True}

    async def mock_exec(*args, **kwargs):
        sql = str(args[0]) if args else ""
        result = MagicMock()
        result.rowcount = 1

        if "SELECT id, username, email, role FROM users" in sql:
            result.mappings.return_value.first.return_value = {
                "id": _USER_ID, "username": "testuser", "email": "test@test.com", "role": "user",
            }
        elif "INSERT INTO paper_portfolios" in sql and "RETURNING" in sql:
            result.mappings.return_value.first.return_value = _PORTFOLIO_ROW
        elif "FROM paper_portfolios pp" in sql and "GROUP BY" in sql:
            if state["portfolio_found"]:
                result.mappings.return_value.first.return_value = _PORTFOLIO_ROW
                result.mappings.return_value.all.return_value = [_PORTFOLIO_ROW]
            else:
                result.mappings.return_value.first.return_value = None
                result.mappings.return_value.all.return_value = []
        elif "SELECT id, current_cash FROM paper_portfolios" in sql:
            if state["portfolio_found"]:
                result.mappings.return_value.first.return_value = {
                    "id": _PORTFOLIO_ID,
                    "current_cash": "100000.00" if state["portfolio_has_cash"] else "0",
                }
            else:
                result.mappings.return_value.first.return_value = None
        elif "SELECT pt.*, i.ticker" in sql or "FROM paper_trades pt" in sql:
            result.mappings.return_value.all.return_value = [_TRADE_ROW]
        elif "DELETE FROM paper_portfolios" in sql:
            result.rowcount = 1 if state["portfolio_found"] else 0
        elif "UPDATE paper_portfolios SET current_cash" in sql:
            result.rowcount = 1
        else:
            result.mappings.return_value.first.return_value = None
            result.mappings.return_value.all.return_value = []

        return result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    app.dependency_overrides[pt_get_current_user_db] = lambda: {
        "id": _USER_ID, "username": "testuser", "email": "test@test.com", "role": "user",
    }
    yield state, mock_session
    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(pt_get_current_user_db, None)


@pytest.mark.anyio
async def test_create_paper_portfolio(client: AsyncClient, mock_paper_db):
    resp = await client.post("/api/v1/paper/portfolios", params={"name": "Test Portfolio"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test Paper Portfolio"


@pytest.mark.anyio
async def test_create_paper_portfolio_custom_cash(client: AsyncClient, mock_paper_db):
    resp = await client.post(
        "/api/v1/paper/portfolios",
        params={"name": "Big Portfolio", "initial_cash": 500000},
    )
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_create_paper_portfolio_missing_name(client: AsyncClient, mock_paper_db):
    resp = await client.post("/api/v1/paper/portfolios")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_list_paper_portfolios(client: AsyncClient, mock_paper_db):
    resp = await client.get("/api/v1/paper/portfolios")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Test Paper Portfolio"


@pytest.mark.anyio
async def test_list_paper_portfolios_empty(client: AsyncClient, mock_paper_db):
    state, _ = mock_paper_db
    state["portfolio_found"] = False
    resp = await client.get("/api/v1/paper/portfolios")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.anyio
async def test_get_paper_portfolio(client: AsyncClient, mock_paper_db):
    resp = await client.get(f"/api/v1/paper/portfolios/{_PORTFOLIO_ID}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test Paper Portfolio"
    assert "trade_count" in data


@pytest.mark.anyio
async def test_get_paper_portfolio_not_found(client: AsyncClient, mock_paper_db):
    state, _ = mock_paper_db
    state["portfolio_found"] = False
    resp = await client.get(f"/api/v1/paper/portfolios/{uuid4()}")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_get_paper_portfolio_invalid_id(client: AsyncClient, mock_paper_db):
    resp = await client.get("/api/v1/paper/portfolios/not-a-uuid")
    assert resp.status_code in (404, 422)


@pytest.mark.anyio
async def test_delete_paper_portfolio(client: AsyncClient, mock_paper_db):
    resp = await client.delete(f"/api/v1/paper/portfolios/{_PORTFOLIO_ID}")
    assert resp.status_code == 200
    assert resp.json()["deleted"] == _PORTFOLIO_ID


@pytest.mark.anyio
async def test_delete_paper_portfolio_not_found(client: AsyncClient, mock_paper_db):
    state, _ = mock_paper_db
    state["portfolio_found"] = False
    resp = await client.delete(f"/api/v1/paper/portfolios/{uuid4()}")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Not found"


@pytest.mark.anyio
async def test_execute_market_trade(client: AsyncClient, mock_paper_db):
    with patch("app.api.paper_trading.simulate_market_fill") as mock_fill:
        mock_fill.return_value = _TRADE_ROW
        resp = await client.post(
            f"/api/v1/paper/execute/{_PORTFOLIO_ID}",
            params={
                "instrument_id": _INSTRUMENT_ID,
                "side": "BUY",
                "quantity": 100,
                "order_type": "market",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["side"] == "BUY"


@pytest.mark.anyio
async def test_execute_limit_trade(client: AsyncClient, mock_paper_db):
    with patch("app.api.paper_trading.simulate_limit_fill") as mock_fill:
        mock_fill.return_value = _TRADE_ROW
        resp = await client.post(
            f"/api/v1/paper/execute/{_PORTFOLIO_ID}",
            params={
                "instrument_id": _INSTRUMENT_ID,
                "side": "BUY",
                "quantity": 100,
                "order_type": "limit",
                "limit_price": 150.0,
            },
        )
        assert resp.status_code == 200


@pytest.mark.anyio
async def test_execute_limit_trade_missing_price(client: AsyncClient, mock_paper_db):
    resp = await client.post(
        f"/api/v1/paper/execute/{_PORTFOLIO_ID}",
        params={
            "instrument_id": _INSTRUMENT_ID,
            "side": "BUY",
            "quantity": 100,
            "order_type": "limit",
        },
    )
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_execute_stop_trade(client: AsyncClient, mock_paper_db):
    with patch("app.api.paper_trading.simulate_stop_fill") as mock_fill:
        mock_fill.return_value = _TRADE_ROW
        resp = await client.post(
            f"/api/v1/paper/execute/{_PORTFOLIO_ID}",
            params={
                "instrument_id": _INSTRUMENT_ID,
                "side": "BUY",
                "quantity": 100,
                "order_type": "stop",
                "stop_price": 140.0,
            },
        )
        assert resp.status_code == 200


@pytest.mark.anyio
async def test_execute_stop_trade_missing_price(client: AsyncClient, mock_paper_db):
    resp = await client.post(
        f"/api/v1/paper/execute/{_PORTFOLIO_ID}",
        params={
            "instrument_id": _INSTRUMENT_ID,
            "side": "BUY",
            "quantity": 100,
            "order_type": "stop",
        },
    )
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_execute_trailing_stop_trade(client: AsyncClient, mock_paper_db):
    with patch("app.api.paper_trading.simulate_trailing_stop_fill") as mock_fill:
        mock_fill.return_value = _TRADE_ROW
        resp = await client.post(
            f"/api/v1/paper/execute/{_PORTFOLIO_ID}",
            params={
                "instrument_id": _INSTRUMENT_ID,
                "side": "SELL",
                "quantity": 100,
                "order_type": "trailing_stop",
                "trail_pct": 5.0,
            },
        )
        assert resp.status_code == 200


@pytest.mark.anyio
async def test_execute_trailing_stop_missing_pct(client: AsyncClient, mock_paper_db):
    resp = await client.post(
        f"/api/v1/paper/execute/{_PORTFOLIO_ID}",
        params={
            "instrument_id": _INSTRUMENT_ID,
            "side": "SELL",
            "quantity": 100,
            "order_type": "trailing_stop",
        },
    )
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_execute_unknown_order_type(client: AsyncClient, mock_paper_db):
    resp = await client.post(
        f"/api/v1/paper/execute/{_PORTFOLIO_ID}",
        params={
            "instrument_id": _INSTRUMENT_ID,
            "side": "BUY",
            "quantity": 100,
            "order_type": "iceberg",
        },
    )
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_execute_trade_no_fill(client: AsyncClient, mock_paper_db):
    with patch("app.api.paper_trading.simulate_market_fill") as mock_fill:
        mock_fill.return_value = None
        resp = await client.post(
            f"/api/v1/paper/execute/{_PORTFOLIO_ID}",
            params={
                "instrument_id": _INSTRUMENT_ID,
                "side": "BUY",
                "quantity": 100,
            },
        )
        assert resp.status_code == 400
        assert "no fill" in resp.text.lower()


@pytest.mark.anyio
async def test_execute_trade_portfolio_not_found(client: AsyncClient, mock_paper_db):
    state, _ = mock_paper_db
    state["portfolio_found"] = False
    resp = await client.post(
        f"/api/v1/paper/execute/{uuid4()}",
        params={
            "instrument_id": _INSTRUMENT_ID,
            "side": "BUY",
            "quantity": 100,
        },
    )
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_get_trade_history(client: AsyncClient, mock_paper_db):
    resp = await client.get(f"/api/v1/paper/trades/{_PORTFOLIO_ID}")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.anyio
async def test_get_trade_history_not_found(client: AsyncClient, mock_paper_db):
    state, _ = mock_paper_db
    state["portfolio_found"] = False
    resp = await client.get(f"/api/v1/paper/trades/{uuid4()}")
    assert resp.status_code == 404
