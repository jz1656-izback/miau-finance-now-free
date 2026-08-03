"""Tests for quantum computing API endpoints."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_quantum_info():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.get("/api/v1/quantum/info")
    assert resp.status_code in (200, 401)


@pytest.mark.anyio
async def test_quantum_qubo():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.post("/api/v1/quantum/qubo/solve", json={"Q": [[-1, 0.5], [0.5, -1]], "num_reads": 5})
    assert resp.status_code in (200, 401)


@pytest.mark.anyio
async def test_quantum_portfolio():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        resp = await c.post("/api/v1/quantum/portfolio",
            json={"expected_returns": [0.1, 0.2], "covariance": [[0.1, 0.02], [0.02, 0.08]]})
    assert resp.status_code in (200, 401)
