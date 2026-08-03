"""Tests for the Alerts API endpoints."""
import pytest
from unittest.mock import patch, MagicMock
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_alert(client: AsyncClient):
    with patch("app.services.alerts_service.alerts_service.create_alert") as mock_create:
        mock_create.return_value = MagicMock(to_dict=lambda: {
            "alert_id": "alert_001", "user_id": "test_user",
            "alert_type": "price_threshold", "portfolio_id": None,
            "ticker": "AAPL", "condition": "above", "threshold": 200.0,
            "current_value": 0, "severity": "warning", "enabled": True,
            "status": "active", "created_at": "2025-01-15T12:00:00",
            "last_triggered": None,
        })
        res = await client.post("/api/v1/alerts", json={
            "alert_type": "price_threshold", "ticker": "AAPL",
            "condition": "above", "threshold": 200.0, "severity": "warning",
        })
        assert res.status_code == 200
        data = res.json()
        assert data["alert_id"] == "alert_001"
        assert data["ticker"] == "AAPL"


@pytest.mark.anyio
async def test_create_alert_invalid_type(client: AsyncClient):
    res = await client.post("/api/v1/alerts", json={
        "alert_type": "invalid_type", "ticker": "AAPL",
        "condition": "above", "threshold": 200.0,
    })
    assert res.status_code == 400


@pytest.mark.anyio
async def test_create_alert_missing_ticker_and_portfolio(client: AsyncClient):
    res = await client.post("/api/v1/alerts", json={
        "alert_type": "price_threshold", "condition": "above",
        "threshold": 200.0,
    })
    assert res.status_code == 400


@pytest.mark.anyio
async def test_get_alerts_empty(client: AsyncClient):
    with patch("app.services.alerts_service.alerts_service.get_user_alerts") as mock_get:
        mock_get.return_value = []
        res = await client.get("/api/v1/alerts")
        assert res.status_code == 200
        assert res.json() == []


@pytest.mark.anyio
async def test_get_alerts(client: AsyncClient):
    with patch("app.services.alerts_service.alerts_service.get_user_alerts") as mock_get:
        mock_get.return_value = [MagicMock(to_dict=lambda: {
            "alert_id": "alert_001", "user_id": "test_user",
            "alert_type": "price_threshold", "portfolio_id": None,
            "ticker": "AAPL", "condition": "above", "threshold": 200.0,
            "current_value": 185.0, "severity": "warning", "enabled": True,
            "status": "active", "created_at": "2025-01-15T12:00:00",
            "last_triggered": None,
        })]
        res = await client.get("/api/v1/alerts")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 1
        assert data[0]["ticker"] == "AAPL"


@pytest.mark.anyio
async def test_enable_alert(client: AsyncClient):
    with patch("app.services.alerts_service.alerts_service.enable_alert") as mock_enable, \
         patch("app.services.alerts_service.alerts_service.get_alert") as mock_get:
        mock_enable.return_value = True
        mock_get.return_value = MagicMock(user_id="admin")
        res = await client.put("/api/v1/alerts/alert_admin_001/enable")
        assert res.status_code == 200
        assert res.json() == {"status": "enabled"}


@pytest.mark.anyio
async def test_enable_alert_not_found(client: AsyncClient):
    with patch("app.services.alerts_service.alerts_service.enable_alert") as mock_enable, \
         patch("app.services.alerts_service.alerts_service.get_alert") as mock_get:
        mock_enable.return_value = False
        mock_get.return_value = None
        res = await client.put("/api/v1/alerts/nonexistent/enable")
        assert res.status_code == 404


@pytest.mark.anyio
async def test_disable_alert(client: AsyncClient):
    with patch("app.services.alerts_service.alerts_service.disable_alert") as mock_disable, \
         patch("app.services.alerts_service.alerts_service.get_alert") as mock_get:
        mock_disable.return_value = True
        mock_get.return_value = MagicMock(user_id="admin")
        res = await client.put("/api/v1/alerts/alert_admin_001/disable")
        assert res.status_code == 200
        assert res.json() == {"status": "disabled"}


@pytest.mark.anyio
async def test_delete_alert(client: AsyncClient):
    with patch("app.services.alerts_service.alerts_service.delete_alert") as mock_delete, \
         patch("app.services.alerts_service.alerts_service.get_alert") as mock_get:
        mock_delete.return_value = True
        mock_get.return_value = MagicMock(user_id="admin")
        res = await client.delete("/api/v1/alerts/alert_admin_001")
        assert res.status_code == 200
        assert res.json() == {"status": "deleted"}


@pytest.mark.anyio
async def test_delete_alert_not_found(client: AsyncClient):
    with patch("app.services.alerts_service.alerts_service.delete_alert") as mock_delete, \
         patch("app.services.alerts_service.alerts_service.get_alert") as mock_get:
        mock_delete.return_value = False
        mock_get.return_value = None
        res = await client.delete("/api/v1/alerts/nonexistent")
        assert res.status_code == 404


@pytest.mark.anyio
async def test_get_alert_history(client: AsyncClient):
    with patch("app.services.alerts_service.alerts_service.get_alert_history") as mock_hist:
        mock_hist.return_value = [
            {"timestamp": "2025-01-15T12:00:00", "alert_id": "alert_001",
             "alert_type": "price_threshold", "ticker": "AAPL",
             "price": 201.5, "threshold": 200.0},
        ]
        res = await client.get("/api/v1/alerts/history?days=7")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 1
        assert data[0]["ticker"] == "AAPL"


@pytest.mark.anyio
async def test_create_example_alerts(client: AsyncClient):
    with patch("app.services.alerts_service.alerts_service.create_alert") as mock_create:
        mock_create.return_value = MagicMock(to_dict=lambda: {
            "alert_id": "alert_ex", "user_id": "test_user",
            "alert_type": "price_threshold", "portfolio_id": None,
            "ticker": "AAPL", "condition": "above", "threshold": 180.0,
            "current_value": 0, "severity": "warning", "enabled": True,
            "status": "active", "created_at": "2025-01-15T12:00:00",
            "last_triggered": None,
        })
        res = await client.post("/api/v1/alerts/examples")
        assert res.status_code == 200
        data = res.json()
        assert "message" in data
        assert "alerts" in data


@pytest.mark.anyio
async def test_alerts_require_auth():
    """Test that unauthenticated requests are rejected."""
    from httpx import ASGITransport, AsyncClient
    from app.main import app
    # Remove the dependency override to test auth
    app.dependency_overrides.clear()
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            res = await ac.get("/api/v1/alerts")
            assert res.status_code == 401
    finally:
        from app.middleware.auth import get_current_user
        app.dependency_overrides[get_current_user] = lambda: {"sub": "admin"}
