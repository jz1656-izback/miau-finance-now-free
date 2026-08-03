import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")


async def get_or_create_stripe_customer(
    db: AsyncSession,
    user_id: str,
    email: str = "",
    username: str = "",
) -> Optional[str]:
    sub = await db.execute(
        text("SELECT stripe_customer_id FROM subscriptions WHERE user_id = :uid"),
        {"uid": user_id},
    )
    row = sub.mappings().first()
    if row and row["stripe_customer_id"]:
        return row["stripe_customer_id"]

    if not STRIPE_SECRET_KEY:
        return f"cus_dev_{user_id[:8]}"

    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY
        customer = stripe.Customer.create(
            email=email,
            metadata={"user_id": user_id, "username": username},
        )
        await db.execute(
            text("""
                INSERT INTO subscriptions (id, user_id, stripe_customer_id, tier, status)
                VALUES (gen_random_uuid(), :uid, :cid, 'free', 'active')
                ON CONFLICT (user_id) DO UPDATE SET stripe_customer_id = :cid2
            """),
            {"uid": user_id, "cid": customer.id, "cid2": customer.id},
        )
        await db.commit()
        return customer.id
    except Exception as e:
        logger.error(f"Failed to create Stripe customer: {e}")
        return None


async def create_checkout_session(
    user_id: str,
    email: str,
    tier: str,
    success_url: str = "http://localhost:5173/billing/success",
    cancel_url: str = "http://localhost:5173/billing/cancel",
) -> str:
    if not STRIPE_SECRET_KEY:
        return f"/billing/success?tier={tier}&dev=true"

    import stripe
    stripe.api_key = STRIPE_SECRET_KEY

    customer_id = None
    customer = stripe.Customer.list(email=email, limit=1)
    if customer.data:
        customer_id = customer.data[0].id

    price_ids = {
        "pro": os.getenv("STRIPE_PRO_PRICE_ID", "price_pro"),
        "enterprise": os.getenv("STRIPE_ENTERPRISE_PRICE_ID", "price_enterprise"),
    }

    session = stripe.checkout.Session.create(
        customer=customer_id,
        customer_email=email if not customer_id else None,
        metadata={"user_id": user_id, "tier": tier},
        line_items=[{
            "price": price_ids.get(tier, "price_pro"),
            "quantity": 1,
        }],
        mode="subscription",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url


async def create_portal_session(user_id: str, return_url: str) -> Optional[str]:
    if not STRIPE_SECRET_KEY:
        return return_url

    try:
        import stripe
        stripe.api_key = STRIPE_SECRET_KEY

        customer = stripe.Customer.list(
            metadata={"user_id": user_id}, limit=1,
        )
        if not customer.data:
            return None

        portal = stripe.billing_portal.Session.create(
            customer=customer.data[0].id,
            return_url=return_url,
        )
        return portal.url
    except Exception as e:
        logger.error(f"Failed to create portal session: {e}")
        return None


async def get_subscription(db: AsyncSession, user_id: str) -> Optional[dict]:
    result = await db.execute(
        text("SELECT * FROM subscriptions WHERE user_id = :uid"),
        {"uid": user_id},
    )
    row = result.mappings().first()
    return dict(row) if row else None


async def update_subscription_tier(db: AsyncSession, user_id: str, tier: str) -> bool:
    result = await db.execute(
        text("""
            UPDATE subscriptions SET tier = :tier, status = 'active',
            current_period_end = NOW() + INTERVAL '30 days'
            WHERE user_id = :uid
            RETURNING id
        """),
        {"tier": tier, "uid": user_id},
    )
    await db.commit()
    return result.rowcount > 0


async def cancel_subscription(db: AsyncSession, user_id: str) -> bool:
    result = await db.execute(
        text("UPDATE subscriptions SET status = 'cancelled' WHERE user_id = :uid"),
        {"uid": user_id},
    )
    await db.commit()
    return result.rowcount > 0
