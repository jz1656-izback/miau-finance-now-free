"""Billing cron job — runs daily to handle subscription lifecycle events.

Handles trial expiration, subscription renewals, and invoice generation.
"""
import logging
from datetime import datetime, timedelta
from sqlalchemy import text
from app.database import async_session

logger = logging.getLogger(__name__)


async def expire_trials():
    """Find and expire trials that have ended."""
    async with async_session() as db:
        result = await db.execute(
            text("""
                UPDATE subscriptions SET status = 'expired', tier = 'free'
                WHERE status = 'trialing' AND trial_ends_at < NOW()
                RETURNING id, user_id
            """)
        )
        rows = result.mappings().all()
        await db.commit()
        if rows:
            logger.info(f"Expired {len(rows)} trials: {[r['user_id'] for r in rows]}")
        return len(rows)


async def expire_subscriptions():
    """Find and mark subscriptions that have ended without renewal."""
    async with async_session() as db:
        result = await db.execute(
            text("""
                UPDATE subscriptions SET status = 'expired', tier = 'free'
                WHERE status = 'active' AND current_period_end < NOW()
                  AND stripe_subscription_id IS NULL
                RETURNING id, user_id
            """)
        )
        rows = result.mappings().all()
        await db.commit()
        if rows:
            logger.info(f"Expired {len(rows)} subscriptions: {[r['user_id'] for r in rows]}")
        return len(rows)


async def generate_monthly_invoices():
    """Generate invoice records for active paid subscriptions."""
    async with async_session() as db:
        result = await db.execute(
            text("""
                INSERT INTO invoices (id, user_id, amount, currency, status, period_start, period_end)
                SELECT
                    gen_random_uuid(), s.user_id,
                    CASE
                        WHEN s.tier = 'starter' THEN s.seats * 5000
                        WHEN s.tier = 'pro' THEN s.seats * 9900
                        WHEN s.tier = 'fund' THEN s.seats * 15000
                        WHEN s.tier = 'enterprise' THEN s.seats * 69967
                        ELSE 0
                    END,
                    'eur', 'open',
                    DATE_TRUNC('month', NOW()) - INTERVAL '1 month',
                    DATE_TRUNC('month', NOW())
                FROM subscriptions s
                WHERE s.status = 'active' AND s.tier IN ('starter', 'pro', 'fund', 'enterprise')
                  AND NOT EXISTS (
                    SELECT 1 FROM invoices i
                    WHERE i.user_id = s.user_id AND i.period_start >= DATE_TRUNC('month', NOW()) - INTERVAL '1 month'
                  )
                RETURNING id, user_id, amount
            """)
        )
        rows = result.mappings().all()
        await db.commit()
        if rows:
            logger.info(f"Generated {len(rows)} invoices")
        return len(rows)


async def run_billing_cycle():
    expired_trials = await expire_trials()
    expired_subs = await expire_subscriptions()
    invoices = await generate_monthly_invoices()
    logger.info(f"Billing cycle complete: {expired_trials} trials expired, "
                f"{expired_subs} subs expired, {invoices} invoices generated")
    return {"expired_trials": expired_trials, "expired_subs": expired_subs, "invoices_generated": invoices}
