"""Tests for NFT API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_nft_portfolio():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/defi/nft/portfolio")
    assert resp.status_code in (200, 401)


@pytest.mark.anyio
async def test_nft_floor():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/defi/nft/floor?collection=bayc")
    assert resp.status_code in (200, 401)
