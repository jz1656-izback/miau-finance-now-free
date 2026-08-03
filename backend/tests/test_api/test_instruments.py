import pytest
from httpx import AsyncClient
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

_SAMPLE_INSTRUMENT = {
    "id": str(uuid.uuid4()),
    "ticker": "AAPL",
    "name": "Apple Inc.",
    "instrument_type": "stock",
    "currency": "USD"
}

@pytest.fixture
def mock_db():
    mock = MagicMock(spec=AsyncSession)
    return mock

@pytest.mark.anyio
async def test_list_instruments(client: AsyncClient):
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        mock_result = MagicMock()
        mock_instrument = MagicMock()
        mock_instrument.Instrument.to_dict.return_value = _SAMPLE_INSTRUMENT
        mock_result.unique.return_value.all.return_value = [mock_instrument]
        return mock_result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session

    try:
        resp = await client.get("/api/v1/instruments")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["ticker"] == "AAPL"
    finally:
        app.dependency_overrides.clear()

@pytest.mark.anyio
async def test_get_instrument(client: AsyncClient):
    from app.main import app
    from app.database import get_db

    mock_session = MagicMock(spec=AsyncSession)
    mock_session.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        mock_result = MagicMock()
        mock_instrument = MagicMock()
        mock_instrument.to_dict.return_value = _SAMPLE_INSTRUMENT
        mock_result.scalar_one_or_none.return_value = mock_instrument
        return mock_result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session

    try:
        resp = await client.get(f"/api/v1/instruments/{_SAMPLE_INSTRUMENT['id']}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["ticker"] == "AAPL"
    finally:
        app.dependency_overrides.clear()
