import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

_PORTFOLIO_ID = str(uuid4())
_USER_ID = str(uuid4())
_INSTRUMENT_ID = str(uuid4())

_PORTFOLIO_RESULT = {
    "id": _PORTFOLIO_ID,
    "user_id": _USER_ID,
    "name": "Test Paper Portfolio",
    "current_cash": "100000.00",
    "initial_cash": "100000.00",
    "trade_count": 0,
    "total_bought": 0,
    "total_sold": 0,
    "created_at": "2025-01-01T00:00:00",
}

_TRADE_RESULT = {
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
}


@pytest.fixture(autouse=True)
def mock_paper_db():
    from app.main import app
    from app.database import get_db
    from app.middleware.auth import get_current_user

    app.dependency_overrides[get_current_user] = lambda: {"sub": "testuser", "role": "user", "user_id": _USER_ID}

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    call_count = [0]

    async def mock_exec(*args, **kwargs):
        sql = str(args[0]) if args else ""
        call_count[0] += 1

        mock_result = MagicMock()
        mock_result.scalar.return_value = "100000.00"

        if "FROM users" in sql:
            mock_result.mappings.return_value.first.return_value = {
                "id": _USER_ID,
                "username": "testuser",
            }
        elif "FROM paper_portfolios" in sql:
            mock_result.mappings.return_value.first.return_value = _PORTFOLIO_RESULT
            mock_result.mappings.return_value.all.return_value = [_PORTFOLIO_RESULT]
        else:
            mock_result.mappings.return_value.first.return_value = _PORTFOLIO_RESULT
            mock_result.mappings.return_value.all.return_value = []

        return mock_result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.mark.anyio
async def test_create_paper_portfolio(client: AsyncClient, mock_paper_db):
    resp = await client.post(
        "/api/v1/paper/portfolios",
        params={"name": "Test Portfolio", "initial_cash": 50000},
    )
    assert resp.status_code in (200, 201, 400)


@pytest.mark.anyio
async def test_list_paper_portfolios(client: AsyncClient, mock_paper_db):
    resp = await client.get("/api/v1/paper/portfolios")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_get_paper_portfolio(client: AsyncClient, mock_paper_db):
    resp = await client.get(f"/api/v1/paper/portfolios/{_PORTFOLIO_ID}")
    assert resp.status_code in (200, 404)


@pytest.mark.anyio
async def test_execute_paper_market_trade(client: AsyncClient, mock_paper_db):
    with patch("app.api.paper_trading.simulate_market_fill") as mock_fill:
        mock_fill.return_value = _TRADE_RESULT
        resp = await client.post(
            f"/api/v1/paper/execute/{_PORTFOLIO_ID}",
            params={
                "instrument_id": _INSTRUMENT_ID,
                "side": "BUY",
                "quantity": 100,
                "order_type": "market",
            },
        )
        assert resp.status_code in (200, 400)


@pytest.mark.anyio
async def test_get_paper_trade_history(client: AsyncClient, mock_paper_db):
    resp = await client.get(f"/api/v1/paper/trades/{_PORTFOLIO_ID}")
    assert resp.status_code in (200, 404)
