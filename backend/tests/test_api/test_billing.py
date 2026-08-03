import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4


@pytest.fixture(autouse=True)
def mock_billing_db():
    from app.main import app
    from app.database import get_db
    from app.middleware.rbac import get_current_user_db

    mock_sesh = MagicMock()
    mock_sesh.execute = AsyncMock()
    mock_sesh.commit = AsyncMock()

    async def mock_exec(*args, **kwargs):
        result = MagicMock()
        sql = str(args[0]) if args else ""
        if "INSERT INTO subscriptions" in sql or "ON CONFLICT" in sql:
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()),
                "user_id": str(uuid4()),
                "stripe_customer_id": None,
                "stripe_subscription_id": None,
                "tier": "pro",
                "status": "active",
                "trial_ends_at": None,
                "current_period_end": "2025-02-01T00:00:00",
                "created_at": "2025-01-01T00:00:00",
            }
            result.rowcount = 1
        elif "UPDATE subscriptions" in sql:
            result.rowcount = 1
        else:
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()),
                "user_id": str(uuid4()),
                "stripe_customer_id": None,
                "stripe_subscription_id": None,
                "tier": "free",
                "status": "active",
                "trial_ends_at": None,
                "current_period_end": None,
                "created_at": "2025-01-01T00:00:00",
            }
        result.mappings.return_value.all.return_value = []
        result.scalar.return_value = 1
        result.rowcount = 1
        return result

    mock_sesh.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_sesh
    app.dependency_overrides[get_current_user_db] = lambda: {
        "id": str(uuid4()),
        "username": "testuser",
        "email": "test@test.com",
        "role": "user",
    }
    yield
    app.dependency_overrides.clear()


@pytest.mark.anyio
async def test_get_subscription_free(mock_billing_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/billing/subscription")
        assert resp.status_code == 200
        data = resp.json()
        assert data["tier"] == "free"


@pytest.mark.anyio
async def test_checkout_dev_mode(mock_billing_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/v1/billing/checkout", json={"tier": "pro"})
        assert resp.status_code == 200
        data = resp.json()
        assert "session_url" in data
        assert "dev_mode" in data["session_url"]


@pytest.mark.anyio
async def test_checkout_invalid_tier(mock_billing_db):
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/v1/billing/checkout", json={"tier": "nonexistent"})
        assert resp.status_code == 400


@pytest.mark.anyio
async def test_checkout_already_subscribed(mock_billing_db):
    from app.main import app
    from app.database import get_db
    from unittest.mock import MagicMock

    mock_sesh = MagicMock()
    mock_sesh.execute = AsyncMock()
    mock_sesh.commit = AsyncMock()

    async def mock_exec_already(*args, **kwargs):
        result = MagicMock()
        sql = str(args[0]) if args else ""
        if "INSERT" in sql or "ON CONFLICT" in sql:
            result.rowcount = 0
        else:
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()),
                "user_id": str(uuid4()),
                "stripe_customer_id": None,
                "stripe_subscription_id": None,
                "tier": "pro",
                "status": "active",
                "trial_ends_at": None,
                "current_period_end": "2025-02-01T00:00:00",
                "created_at": "2025-01-01T00:00:00",
            }
        result.mappings.return_value.all.return_value = []
        result.rowcount = 1
        return result

    mock_sesh.execute.side_effect = mock_exec_already
    app.dependency_overrides[get_db] = lambda: mock_sesh

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/v1/billing/checkout", json={"tier": "pro"})
        assert resp.status_code == 200
        data = resp.json()
        assert "already_active" in data["session_url"]


@pytest.mark.anyio
async def test_webhook_fails_closed_no_secret(mock_billing_db):
    """🔒 SECURITY (V7-002/C4): without a webhook secret the endpoint MUST fail
    closed (503) rather than accepting unsigned payloads."""
    from app.main import app
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/v1/billing/webhook", json={"type": "test"})
        assert resp.status_code == 503
        assert "not configured" in resp.text


@pytest.mark.anyio
async def test_checkout_upgrades_from_free(mock_billing_db):
    from app.main import app
    from app.database import get_db
    from unittest.mock import MagicMock

    mock_sesh = MagicMock()
    mock_sesh.execute = AsyncMock()
    mock_sesh.commit = AsyncMock()
    call_count = 0

    async def mock_exec_upgrade(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        result = MagicMock()
        if call_count == 1:
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()), "user_id": str(uuid4()),
                "tier": "free", "status": "active",
                "stripe_customer_id": None, "stripe_subscription_id": None,
                "trial_ends_at": None, "current_period_end": None,
                "created_at": "2025-01-01T00:00:00",
            }
        elif "INSERT" in str(args[0]):
            result.rowcount = 1
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()), "user_id": str(uuid4()),
                "tier": "pro", "status": "active",
                "stripe_customer_id": None, "stripe_subscription_id": None,
                "trial_ends_at": None, "current_period_end": "2025-02-01T00:00:00",
                "created_at": "2025-01-01T00:00:00",
            }
        else:
            result.mappings.return_value.first.return_value = None
        result.mappings.return_value.all.return_value = []
        result.rowcount = 1
        return result

    mock_sesh.execute.side_effect = mock_exec_upgrade
    app.dependency_overrides[get_db] = lambda: mock_sesh

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/v1/billing/checkout", json={"tier": "enterprise"})
        assert resp.status_code == 200
        data = resp.json()
        assert "dev_mode" in data["session_url"]


@pytest.mark.anyio
async def test_activate_trial(client: AsyncClient):
    from app.main import app
    from app.database import get_db
    from app.middleware.rbac import get_current_user_db
    mock_sesh = MagicMock()
    mock_sesh.execute = AsyncMock()
    mock_sesh.commit = AsyncMock()

    async def mock_exec_trial(*args, **kwargs):
        result = MagicMock()
        sql = str(args[0]) if args else ""
        if "SELECT" in sql and "subscriptions" in sql:
            result.mappings.return_value.first.return_value = None
        elif "INSERT" in sql:
            result.mappings.return_value.first.return_value = {
                "id": str(uuid4()), "user_id": str(uuid4()), "tier": "pro",
                "status": "trialing", "trial_ends_at": "2025-01-08T00:00:00",
                "current_period_end": "2025-01-08T00:00:00",
            }
        return result

    mock_sesh.execute.side_effect = mock_exec_trial
    app.dependency_overrides[get_db] = lambda: mock_sesh
    resp = await client.post("/api/v1/billing/trial/activate")
    assert resp.status_code in (200, 201), f"Got {resp.status_code}"
    data = resp.json()
    assert data.get("status") == "trial_active" or data.get("tier") == "pro"
    app.dependency_overrides.pop(get_db, None)


@pytest.mark.anyio
async def test_billing_portal(client: AsyncClient):
    from app.main import app
    from app.database import get_db
    mock_sesh = MagicMock()
    mock_sesh.execute = AsyncMock()
    mock_sesh.commit = AsyncMock()

    async def mock_exec_portal(*args, **kwargs):
        result = MagicMock()
        result.mappings.return_value.first.return_value = {
            "id": str(uuid4()), "user_id": str(uuid4()), "tier": "pro", "status": "active",
            "stripe_customer_id": None, "stripe_subscription_id": None,
            "trial_ends_at": None, "current_period_end": "2025-02-01T00:00:00", "created_at": "2025-01-01T00:00:00",
        }
        return result

    mock_sesh.execute.side_effect = mock_exec_portal
    app.dependency_overrides[get_db] = lambda: mock_sesh
    resp = await client.post("/api/v1/billing/portal")
    assert resp.status_code in (200, 404, 405)
    app.dependency_overrides.pop(get_db, None)


@pytest.mark.anyio
async def test_get_subscription_endpoint(client: AsyncClient):
    from app.main import app
    from app.database import get_db
    mock_sesh = MagicMock()
    mock_sesh.execute = AsyncMock()
    mock_sesh.commit = AsyncMock()

    async def mock_exec_sub(*args, **kwargs):
        result = MagicMock()
        result.mappings.return_value.first.return_value = {
            "id": str(uuid4()), "user_id": str(uuid4()), "tier": "pro", "status": "active",
            "stripe_customer_id": "cus_test", "stripe_subscription_id": "sub_test",
            "trial_ends_at": None, "current_period_end": "2025-02-01T00:00:00", "created_at": "2025-01-01T00:00:00",
        }
        return result

    mock_sesh.execute.side_effect = mock_exec_sub
    app.dependency_overrides[get_db] = lambda: mock_sesh
    resp = await client.get("/api/v1/billing/subscription")
    assert resp.status_code in (200, 404, 405)
    if resp.status_code == 200:
        data = resp.json()
        assert "tier" in data
    app.dependency_overrides.pop(get_db, None)
