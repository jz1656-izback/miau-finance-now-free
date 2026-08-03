"""Daily usage aggregation cron.

Aggregates hourly api_usage_log into daily UsageRecord entries.
Prunes data older than 90 days. Runs via the background scheduler.
"""
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.usage_records import aggregate_daily_usage_records

logger = logging.getLogger(__name__)


async def aggregate_daily_usage(db: AsyncSession) -> dict:
    return await aggregate_daily_usage_records(db)


async def prune_old_data(db: AsyncSession) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=90)
    result = await db.execute(
        text("DELETE FROM api_usage_log WHERE logged_at < :cutoff"),
        {"cutoff": cutoff},
    )
    await db.commit()
    deleted = result.rowcount or 0
    logger.info("Pruned %s old usage records", deleted)
    return {"pruned": deleted}
