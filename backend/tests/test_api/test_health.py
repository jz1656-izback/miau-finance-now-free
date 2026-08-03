"""Tests for the health check endpoints."""
import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock


@pytest.mark.anyio
async def test_health_endpoint_returns_200(client: AsyncClient):
    resp = await client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "uptime_seconds" in data
    assert "services" in data
    assert "provider_health" in data
    assert data["services"]["api"] is True
    assert data["services"]["data_providers"] >= 0
    assert data["services"]["providers_healthy"] >= 0
    assert data["services"]["providers_unhealthy"] >= 0


@pytest.mark.anyio
async def test_health_returns_provider_details(client: AsyncClient):
    resp = await client.get("/api/v1/health")
    data = resp.json()
    for provider, healthy in data["provider_health"].items():
        assert isinstance(provider, str)
        assert isinstance(healthy, bool)


@pytest.mark.anyio
async def test_health_returns_log_files(client: AsyncClient):
    resp = await client.get("/api/v1/health")
    data = resp.json()
    assert "log_files" in data
    assert isinstance(data["log_files"], dict)


@pytest.mark.anyio
async def test_health_services_endpoint(client: AsyncClient):
    resp = await client.get("/api/v1/health/services")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data
    assert "total" in data
    assert "up" in data
    assert "down" in data
    assert "services" in data
    assert data["total"] >= 5
    assert data["up"] + data["down"] + data.get("unknown", 0) == data["total"]


@pytest.mark.anyio
async def test_health_history_endpoint(client: AsyncClient):
    resp = await client.get("/api/v1/health/history?hours=1")
    assert resp.status_code == 200
    data = resp.json()
    assert "history" in data
    assert isinstance(data["history"], list)


@pytest.mark.anyio
async def test_health_history_default_hours(client: AsyncClient):
    resp = await client.get("/api/v1/health/history")
    assert resp.status_code == 200
    data = resp.json()
    assert "history" in data


@pytest.mark.anyio
async def test_metrics_endpoint_returns_prometheus(client: AsyncClient):
    resp = await client.get("/metrics")
    assert resp.status_code == 200
    text = resp.text
    assert "miau_requests_total" in text or "metrics not available" in text


@pytest.mark.anyio
async def test_health_timestamp_format(client: AsyncClient):
    resp = await client.get("/api/v1/health")
    ts = resp.json()["timestamp"]
    assert ts.endswith("Z") or "+" in ts


@pytest.mark.anyio
async def test_health_version_string(client: AsyncClient):
    resp = await client.get("/api/v1/health")
    version = resp.json()["version"]
    assert version.startswith("v")
