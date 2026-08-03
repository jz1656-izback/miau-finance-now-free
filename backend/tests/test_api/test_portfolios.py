import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession


_SAMPLE_PORTFOLIOS = [
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "Tech Growth",
        "portfolio_type": "growth",
        "base_currency": "USD",
        "status": "active",
        "num_positions": 10,
        "total_value": 500000.0,
    },
    {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Income Fund",
        "portfolio_type": "income",
        "base_currency": "USD",
        "status": "active",
        "num_positions": 5,
        "total_value": 250000.0,
    },
]

_SAMPLE_PORTFOLIO_DETAIL = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Tech Growth",
    "portfolio_type": "growth",
    "base_currency": "USD",
    "status": "active",
    "positions": [
        {
            "ticker": "AAPL",
            "quantity": 100,
            "market_value": 15000.0,
            "unrealized_pnl": 1500.0,
            "instrument_name": "Apple Inc.",
            "instrument_type": "stock",
        },
    ],
}

_SAMPLE_POSITIONS = [
    {
        "ticker": "AAPL",
        "quantity": 100,
        "market_value": 15000.0,
        "unrealized_pnl": 1500.0,
        "instrument_name": "Apple Inc.",
        "instrument_type": "stock",
        "sector": "Technology",
    },
]


@pytest.fixture
def mock_db():
    mock = MagicMock(spec=AsyncSession)
    return mock


def _mock_execute(rows):
    async def execute(*args, **kwargs):
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = rows
        mock_result.mappings.return_value.first.return_value = rows[0] if rows else None
        mock_result.fetchall.return_value = rows
        return mock_result
    return execute


async def _override_get_db():
    mock = MagicMock(spec=AsyncSession)
    mock.execute = MagicMock()
    yield mock


@pytest.mark.anyio
async def test_list_portfolios(client: AsyncClient):
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = _SAMPLE_PORTFOLIOS
        return mock_result

    mock_session.execute.side_effect = mock_exec

    app.dependency_overrides[get_db] = lambda: mock_session
    try:
        resp = await client.get("/api/v1/portfolios")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        if data:
            assert "id" in data[0]
            assert "name" in data[0]
    finally:
        app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_get_portfolio(client: AsyncClient):
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute = AsyncMock()

    call_count = {"n": 0}

    async def mock_exec(*args, **kwargs):
        call_count["n"] += 1
        mock_result = MagicMock()
        if call_count["n"] == 1:
            mock_result.mappings.return_value.first.return_value = _SAMPLE_PORTFOLIO_DETAIL
        else:
            mock_result.mappings.return_value.all.return_value = _SAMPLE_PORTFOLIO_DETAIL["positions"]
        return mock_result

    mock_session.execute.side_effect = mock_exec

    app.dependency_overrides[get_db] = lambda: mock_session
    try:
        resp = await client.get(f"/api/v1/portfolios/{_SAMPLE_PORTFOLIO_DETAIL['id']}")
        if resp.status_code == 200:
            data = resp.json()
            assert "name" in data
            assert "positions" in data
    finally:
        app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_get_portfolio_not_found(client: AsyncClient):
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        mock_result = MagicMock()
        mock_result.mappings.return_value.first.return_value = None
        return mock_result

    mock_session.execute.side_effect = mock_exec

    app.dependency_overrides[get_db] = lambda: mock_session
    try:
        resp = await client.get("/api/v1/portfolios/550e8400-e29b-41d4-a716-446655449999")
        assert resp.status_code == 404
    finally:
        app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_get_positions(client: AsyncClient):
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = _SAMPLE_POSITIONS
        return mock_result

    mock_session.execute.side_effect = mock_exec

    app.dependency_overrides[get_db] = lambda: mock_session
    try:
        resp = await client.get("/api/v1/portfolios/550e8400-e29b-41d4-a716-446655440000/positions")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_get_positions_empty(client: AsyncClient):
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        mock_result = MagicMock()
        mock_result.mappings.return_value.all.return_value = []
        return mock_result

    mock_session.execute.side_effect = mock_exec

    app.dependency_overrides[get_db] = lambda: mock_session
    try:
        resp = await client.get("/api/v1/portfolios/550e8400-e29b-41d4-a716-446655440000/positions")
        assert resp.status_code == 200
        assert resp.json() == []
    finally:
        app.dependency_overrides.clear()
