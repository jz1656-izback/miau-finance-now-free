import pytest
from httpx import AsyncClient
from unittest.mock import patch


@pytest.mark.anyio
async def test_list_brokers(client: AsyncClient):
    resp = await client.get("/api/v1/brokers")
    assert resp.status_code == 200
    data = resp.json()
    assert "brokers" in data


@pytest.mark.anyio
async def test_broker_account_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/brokers/nonexistent/account")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_broker_positions_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/brokers/nonexistent/positions")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_broker_submit_order_not_found(client: AsyncClient):
    resp = await client.post(
        "/api/v1/brokers/nonexistent/orders",
        json={"symbol": "AAPL", "qty": 1, "side": "buy"},
    )
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_broker_orders_not_found(client: AsyncClient):
    resp = await client.get("/api/v1/brokers/nonexistent/orders")
    assert resp.status_code == 404



