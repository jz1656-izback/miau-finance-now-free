"""Tests for DeFi wallet endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_connect_wallet():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.post("/api/v1/defi/wallet/connect", json={"wallet": "metamask"})
    assert resp.status_code in (200, 401)


@pytest.mark.anyio
async def test_wallet_balance():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/defi/wallet/balance")
    assert resp.status_code in (200, 401)
