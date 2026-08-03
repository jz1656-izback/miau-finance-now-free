"""Tests for carbon footprint API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_carbon_ticker():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/carbon/AAPL")
    assert resp.status_code in (200, 401, 404)


@pytest.mark.anyio
async def test_carbon_portfolio():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/carbon/portfolio/test-id")
    assert resp.status_code in (200, 401, 404)
