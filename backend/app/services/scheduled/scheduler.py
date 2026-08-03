import logging
import asyncio
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.auto_topup import check_and_topup
from app.services.scheduled.usage_cron import aggregate_daily_usage, prune_old_data
from app.async_utils import safe_task

logger = logging.getLogger(__name__)

_scheduler_running = False


async def run_daily_tasks(db: AsyncSession) -> None:
    now = datetime.now(timezone.utc)

    logger.info("Running daily billing tasks at %s", now.isoformat())

    topups = await check_and_topup(db)
    logger.info("Auto top-ups processed: %s", len(topups))

    usage = await aggregate_daily_usage(db)
    logger.info("Daily usage aggregated: %s", usage)

    pruned = await prune_old_data(db)
    logger.info("Old usage pruned: %s", pruned)

    expired = await db.execute(
        text("""
            UPDATE subscriptions
            SET status = 'expired', tier = 'free'
            WHERE status = 'trialing'
              AND trial_ends_at < NOW()
              AND trial_ends_at IS NOT NULL
            RETURNING id
        """),
    )
    await db.commit()
    expired_count = len(expired.mappings().all())
    logger.info("Trials expired: %s", expired_count)

    today = now.strftime("%Y-%m-%d")
    if now.day == 1:
        logger.info("First of month — generating invoices")
        await db.execute(
            text("""
                INSERT INTO invoices (id, user_id, amount, currency, status, period_start, period_end)
                SELECT gen_random_uuid(), s.user_id,
                       CASE s.tier WHEN 'pro' THEN 9900 WHEN 'enterprise' THEN 39600 ELSE 0 END,
                       'usd', 'open',
                       date_trunc('month', NOW()) - INTERVAL '1 month',
                       date_trunc('month', NOW())
                FROM subscriptions s
                WHERE s.status = 'active' AND s.tier != 'free'
                  AND NOT EXISTS (
                    SELECT 1 FROM invoices i
                    WHERE i.user_id = s.user_id AND i.period_start >= date_trunc('month', NOW()) - INTERVAL '1 month'
                  )
            """),
        )
        await db.commit()
        logger.info("Monthly invoices generated")

    # Log cleanup
    from app.services.log_cleanup import cleanup_logs
    removed = cleanup_logs()
    logger.info("Old log files cleaned: %s", removed)


def start_scheduler(interval_hours: int = 24) -> None:
    global _scheduler_running
    if _scheduler_running:
        return
    _scheduler_running = True

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        logger.warning("No running event loop — scheduler deferred")
        return

    async def _loop():
        while True:
            try:
                async for db in get_db():
                    await run_daily_tasks(db)
                    break
            except Exception as e:
                logger.error("Scheduler error: %s", e)
            await asyncio.sleep(interval_hours * 3600)

    safe_task(_loop(), name="billing-scheduler")
    logger.info("Billing scheduler started (interval=%sh)", interval_hours)
