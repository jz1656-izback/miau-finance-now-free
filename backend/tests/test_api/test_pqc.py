"""Tests for PQC API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_pqc_kyber():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/security/pqc/kyber/keygen")
    assert resp.status_code in (200, 401)


@pytest.mark.anyio
async def test_pqc_dilithium():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/security/pqc/dilithium/keygen")
    assert resp.status_code in (200, 401)


@pytest.mark.anyio
async def test_pqc_info():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/security/pqc/info")
    assert resp.status_code in (200, 401)
