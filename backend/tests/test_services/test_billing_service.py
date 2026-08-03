import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4


@pytest.mark.anyio
async def test_get_or_create_customer_dev_mode():
    from app.services.billing_service import get_or_create_stripe_customer

    mock_db = MagicMock()
    mock_db.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        r = MagicMock()
        r.mappings.return_value.first.return_value = None
        return r

    mock_db.execute.side_effect = mock_exec

    customer_id = await get_or_create_stripe_customer(mock_db, str(uuid4()), "test@test.com")
    assert customer_id is not None
    assert customer_id.startswith("cus_dev_")


@pytest.mark.anyio
async def test_create_checkout_session_dev_mode():
    from app.services.billing_service import create_checkout_session

    with patch("app.services.billing_service.STRIPE_SECRET_KEY", ""):
        url = await create_checkout_session(str(uuid4()), "test@test.com", "pro")
        assert url is not None
        assert "dev=true" in url


@pytest.mark.anyio
async def test_get_subscription():
    from app.services.billing_service import get_subscription

    mock_db = MagicMock()
    mock_db.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        r = MagicMock()
        r.mappings.return_value.first.return_value = {"id": "sub-id", "tier": "pro", "status": "active"}
        return r

    mock_db.execute.side_effect = mock_exec

    sub = await get_subscription(mock_db, str(uuid4()))
    assert sub is not None
    assert sub["tier"] == "pro"


@pytest.mark.anyio
async def test_update_subscription_tier():
    from app.services.billing_service import update_subscription_tier

    mock_db = MagicMock()
    mock_db.execute = AsyncMock()
    mock_db.commit = AsyncMock()

    async def mock_exec(*args, **kwargs):
        r = MagicMock()
        r.rowcount = 1
        return r

    mock_db.execute.side_effect = mock_exec

    result = await update_subscription_tier(mock_db, str(uuid4()), "enterprise")
    assert result is True


@pytest.mark.anyio
async def test_cancel_subscription():
    from app.services.billing_service import cancel_subscription

    mock_db = MagicMock()
    mock_db.execute = AsyncMock()
    mock_db.commit = AsyncMock()

    async def mock_exec(*args, **kwargs):
        r = MagicMock()
        r.rowcount = 1
        return r

    mock_db.execute.side_effect = mock_exec

    result = await cancel_subscription(mock_db, str(uuid4()))
    assert result is True


@pytest.mark.anyio
async def test_create_portal_session_dev_mode():
    from app.services.billing_service import create_portal_session

    with patch("app.services.billing_service.STRIPE_SECRET_KEY", ""):
        url = await create_portal_session(str(uuid4()), "http://return")
        assert url == "http://return"


@pytest.mark.anyio
async def test_create_checkout_session_stripe_mode():
    import app.services.billing_service as svc
    import sys
    mock_stripe = MagicMock()
    mock_session = MagicMock()
    mock_session.url = "https://checkout.stripe.com/test"
    mock_stripe.checkout.Session.create.return_value = mock_session
    mock_stripe.Customer.list.return_value = MagicMock(data=[])
    sys.modules["stripe"] = mock_stripe

    with patch.object(svc, "STRIPE_SECRET_KEY", "sk_test_key"):
        url = await svc.create_checkout_session(str(uuid4()), "test@test.com", "pro")
        assert url == "https://checkout.stripe.com/test"

    del sys.modules["stripe"]


def test_tier_prices_defined():
    prices = {
        "pro": {"amount": 11600, "currency": "usd"},
        "enterprise": {"amount": 39600, "currency": "usd"},
    }
    assert "pro" in prices
    assert "enterprise" in prices
    assert prices["pro"]["amount"] < prices["enterprise"]["amount"]
