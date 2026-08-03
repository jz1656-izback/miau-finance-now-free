"""Tests for global markets endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_global_markets():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/markets/global")
    assert resp.status_code in (200, 401)


@pytest.mark.anyio
async def test_exchange_detail():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/markets/global/NYSE")
    assert resp.status_code in (200, 401, 404)
