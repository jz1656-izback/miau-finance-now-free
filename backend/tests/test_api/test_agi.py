"""Tests for AGI API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_agi_status():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/agi/status")
    assert resp.status_code in (200, 401)


@pytest.mark.anyio
async def test_agi_hypotheses():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/agi/hypotheses")
    assert resp.status_code in (200, 401)


@pytest.mark.anyio
async def test_agi_hypotheses_ticker():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/agi/hypotheses?ticker=AAPL")
    assert resp.status_code in (200, 401)
