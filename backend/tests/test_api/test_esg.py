"""Tests for ESG API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_esg_ticker():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/esg/AAPL")
    assert resp.status_code in (200, 401, 404)


@pytest.mark.anyio
async def test_esg_portfolio():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/esg/portfolio/test-id")
    assert resp.status_code in (200, 401, 404)


@pytest.mark.anyio
async def test_esg_screen():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/esg/screen?min_score=50")
    assert resp.status_code in (200, 401)
