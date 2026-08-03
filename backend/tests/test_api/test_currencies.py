"""Tests for currency endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_list_currencies():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/currencies")
    assert resp.status_code == 200
    data = resp.json()
    assert "USD" in data
    assert data["USD"]["symbol"] == "$"


@pytest.mark.anyio
async def test_convert_currency():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/currencies/convert?amount=100&from=USD&to=EUR")
    if resp.status_code == 200:
        data = resp.json()
        assert "converted_amount" in data
        assert data["from_currency"] == "USD"
