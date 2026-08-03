import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_health_endpoint(client: AsyncClient):
    resp = await client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["app"] == "Miau Finance"


@pytest.mark.anyio
async def test_api_map_endpoint(client: AsyncClient):
    resp = await client.get("/api/v1")
    assert resp.status_code == 200
    data = resp.json()
    assert data["app"] == "Miau Finance"
    assert "version" in data
    assert "endpoints" in data
    assert "health" in data["endpoints"]
    assert data["endpoints"]["health"] == "GET /api/v1/health"
    assert "market_live" in data["endpoints"]


@pytest.mark.anyio
async def test_health_returns_valid_json(client: AsyncClient):
    resp = await client.get("/api/v1/health")
    assert resp.headers["content-type"] == "application/json"
    data = resp.json()
    assert isinstance(data, dict)


@pytest.mark.anyio
async def test_api_map_contains_platform_endpoints(client: AsyncClient):
    resp = await client.get("/api/v1")
    data = resp.json()
    endpoints = data["endpoints"]
    core_keys = [
        "health", "api_map",
        "instruments_list", "portfolios_list",
        "search", "analytics_summary",
    ]
    for key in core_keys:
        assert key in endpoints, f"Missing endpoint: {key}"


@pytest.mark.anyio
async def test_nonexistent_route_returns_404(client: AsyncClient):
    resp = await client.get("/api/v1/nonexistent")
    assert resp.status_code == 404
