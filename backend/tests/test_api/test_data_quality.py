"""
Tests for Data Quality Middleware and endpoints.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_data_quality_headers_present(client: AsyncClient):
    """Data quality headers should be present on responses."""
    resp = await client.get("/api/v1/health")
    assert "X-Data-Quality" in resp.headers
    assert resp.headers["X-Data-Quality"] in ("fresh", "error", "redirect")


@pytest.mark.anyio
async def test_data_domain_header_price(client: AsyncClient):
    """Price endpoints should include data domain headers."""
    resp = await client.get("/api/v1/market/live?tickers=AAPL")
    if resp.status_code < 500:
        # Headers may be present even on 401/404
        assert "X-Data-Domain" in resp.headers or "X-Data-Quality" in resp.headers


@pytest.mark.anyio
async def test_data_quality_health_endpoint(client: AsyncClient):
    """Data quality health endpoint returns domain list."""
    resp = await client.get("/api/v1/data-quality/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["domains_monitored"] > 0
    assert len(data["domains"]) > 0


@pytest.mark.anyio
async def test_data_quality_domains_endpoint(client: AsyncClient):
    """Data quality domains endpoint lists all monitored domains."""
    resp = await client.get("/api/v1/data-quality/domains")
    assert resp.status_code == 200
    data = resp.json()
    assert "domains" in data
    assert data["total"] > 0
    # Verify specific domains exist
    for domain in ("price", "historical", "news"):
        assert domain in data["domains"], f"Missing domain: {domain}"


@pytest.mark.anyio
async def test_data_freshness_headers(client: AsyncClient):
    """Freshness headers should contain TTL and timestamp info."""
    resp = await client.get("/api/v1/health")
    if "X-Data-TTL" in resp.headers:
        ttl = resp.headers["X-Data-TTL"]
        assert ttl.isdigit(), f"TTL should be numeric: {ttl}"
        assert int(ttl) > 0
    if "X-Data-Timestamp" in resp.headers:
        ts = resp.headers["X-Data-Timestamp"]
        assert ts.isdigit(), f"Timestamp should be numeric: {ts}"
    assert "X-Data-Origin" in resp.headers
    assert resp.headers["X-Data-Origin"] == "miau-finance"


@pytest.mark.anyio
async def test_error_responses_have_quality_headers(client: AsyncClient):
    """Error responses should still have data quality headers."""
    resp = await client.get("/api/v1/nonexistent-route")
    assert resp.status_code == 404
    assert "X-Data-Quality" in resp.headers
