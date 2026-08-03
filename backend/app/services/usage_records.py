"""Usage records service — aggregator and query layer for UsageRecord model.

Provides cron-batchable aggregation from api_usage_log into the
usage_records table, plus user-facing query helpers.
"""
import logging
from datetime import date, timedelta
from typing import Optional

from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import UsageRecord

logger = logging.getLogger(__name__)

FREE_REQUEST_LIMIT = 10000
PRO_REQUEST_LIMIT = 500000


async def aggregate_daily_usage_records(db: AsyncSession) -> dict:
    """Aggregate yesterday's api_usage_log rows into usage_records.

    Runs as part of the daily cron cycle.  Uses upsert semantics so it
    is safe to run multiple times.
    """
    result = await db.execute(
        text("""
            INSERT INTO usage_records (id, user_id, api_key_id, date, request_count, data_transfer_bytes)
            SELECT
                gen_random_uuid(),
                user_id,
                api_key_id,
                DATE(logged_at) as date,
                COUNT(*) as request_count,
                0::bigint as data_transfer_bytes
            FROM api_usage_log
            WHERE logged_at >= NOW() - INTERVAL '1 day'
              AND logged_at < DATE(NOW())
            GROUP BY user_id, api_key_id, DATE(logged_at)
            ON CONFLICT (user_id, date) DO UPDATE
                SET request_count = usage_records.request_count + EXCLUDED.request_count,
                    data_transfer_bytes = usage_records.data_transfer_bytes + EXCLUDED.data_transfer_bytes
            RETURNING id
        """),
    )
    await db.commit()
    rows = result.mappings().all()
    logger.info("Aggregated %s daily usage records", len(rows))
    return {"period": "daily", "records_created": len(rows)}


async def get_user_usage(
    db: AsyncSession,
    user_id: str,
    days: int = 30,
) -> list[dict]:
    """Return usage records for a user over the last N days."""
    cutoff = date.today() - timedelta(days=days)
    stmt = (
        select(UsageRecord)
        .where(UsageRecord.user_id == user_id, UsageRecord.date >= cutoff)
        .order_by(UsageRecord.date.desc())
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": str(r.id),
            "date": r.date.isoformat(),
            "request_count": r.request_count or 0,
            "data_transfer_bytes": r.data_transfer_bytes or 0,
        }
        for r in rows
    ]


async def get_usage_summary(
    db: AsyncSession,
    user_id: str,
) -> dict:
    """Return a brief usage summary for the current billing period."""
    month_start = date.today().replace(day=1)

    result = await db.execute(
        select(func.coalesce(func.sum(UsageRecord.request_count), 0))
        .where(UsageRecord.user_id == user_id, UsageRecord.date >= month_start)
    )
    monthly_requests = result.scalar() or 0

    sub = await db.execute(
        text("SELECT tier, status FROM subscriptions WHERE user_id = :uid"),
        {"uid": user_id},
    )
    sub_row = sub.mappings().first()
    tier = sub_row["tier"] if sub_row else "free"

    tier_limits = {"free": FREE_REQUEST_LIMIT, "pro": PRO_REQUEST_LIMIT, "enterprise": 10_000_000}
    limit = tier_limits.get(tier, FREE_REQUEST_LIMIT)

    return {
        "tier": tier,
        "monthly_requests": monthly_requests,
        "limit": limit,
        "usage_pct": round(monthly_requests / limit * 100, 1) if limit > 0 else 0,
    }


async def prune_old_records(db: AsyncSession, days: int = 90) -> dict:
    """Archive/delete usage records older than *days*."""
    cutoff = date.today() - timedelta(days=days)
    result = await db.execute(
        text("DELETE FROM usage_records WHERE date < :cutoff"),
        {"cutoff": cutoff},
    )
    await db.commit()
    deleted = result.rowcount or 0
    logger.info("Pruned %s usage records older than %s days", deleted, days)
    return {"pruned": deleted}
