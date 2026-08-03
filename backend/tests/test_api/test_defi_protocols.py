"""Tests for DeFi protocol endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_defi_protocols():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/defi/protocols")
    assert resp.status_code in (200, 401)


@pytest.mark.anyio
async def test_defi_positions():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/defi/positions")
    assert resp.status_code in (200, 401)
