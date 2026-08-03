"""Wealth cron — weekly allocation + rebalance + valuation updates."""
import logging
from datetime import datetime, timezone

from app.services.wealth_engine import run_allocation_cycle
from app.services.auto_investor import auto_buy_stocks, auto_buy_crypto

logger = logging.getLogger(__name__)


async def run_weekly_allocation(db=None) -> dict:
    """Weekly wealth allocation: distribute profits across 3 tiers."""
    if not db:
        return {"status": "skipped", "reason": "No database session"}
    logger.info("Running weekly wealth allocation...")
    result = await run_allocation_cycle(db)
    logger.info("Weekly allocation complete: %s", result.get("status", "?"))
    return result


async def run_daily_investment_check(db=None) -> dict:
    """Daily check: invest cat eco balance if above threshold."""
    from app.services.revenue import get_cat_eco_balance
    if not db:
        return {"status": "skipped"}
    balance = await get_cat_eco_balance(db)
    cat_eco = balance.get("cat_eco_balance", 0)
    if cat_eco >= 100:
        logger.info("Cat eco balance €%s above €100 threshold — triggering investment", cat_eco)
        await auto_buy_stocks(cat_eco * 0.6, dry_run=True)  # 60% stocks
        await auto_buy_crypto(cat_eco * 0.4, dry_run=True)  # 40% crypto
        return {"status": "investment_triggered", "amount": cat_eco}
    return {"status": "below_threshold", "balance": cat_eco}
