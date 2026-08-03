"""
Data quality checks and parallel fetching utilities.
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)

STALE_THRESHOLD_HOURS = {
    "price": 1,
    "crypto": 1,
    "forex": 2,
    "fundamentals": 24,
    "filings": 168,
}


class DataQualityError(ValueError):
    pass


def check_price_quality(data: dict, source: str = "unknown") -> Optional[str]:
    price = data.get("price") or data.get("close")
    if price is not None:
        try:
            p = float(price)
            if p <= 0:
                return f"Non-positive price {p} from {source}"
            if p > 100_000_000:
                return f"Suspiciously high price {p} from {source}"
        except (TypeError, ValueError):
            return f"Invalid price value {price} from {source}"

    change = data.get("change_pct") or data.get("change_24h_pct")
    if change is not None:
        try:
            c = float(change)
            if abs(c) > 100:
                return f"Extreme change {c}% from {source}"
        except (TypeError, ValueError):
            pass

    return None


def check_timestamp_freshness(
    timestamp: Optional[str],
    source: str = "unknown",
    max_age_hours: int = 24,
) -> Optional[str]:
    if not timestamp:
        return None
    try:
        ts = datetime.fromisoformat(timestamp)
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        age = (datetime.now(timezone.utc) - ts).total_seconds() / 3600
        if age > max_age_hours:
            return f"Stale data from {source}: {age:.1f}h old (max {max_age_hours}h)"
    except (ValueError, TypeError):
        return f"Invalid timestamp {timestamp} from {source}"
    return None


async def parallel_fetch(
    items: list[Any],
    fetcher: Callable,
    semaphore_limit: int = 5,
    label: str = "fetch",
) -> list[Any]:
    sem = asyncio.Semaphore(semaphore_limit)

    async def bounded(item: Any) -> Any:
        async with sem:
            try:
                return await fetcher(item)
            except Exception as e:
                logger.warning(f"[{label}] Failed for {item}: {e}")
                return None

    results = await asyncio.gather(*[bounded(item) for item in items])
    successes = [r for r in results if r is not None]
    failures = len(results) - len(successes)
    if failures:
        logger.warning(f"[{label}] {failures}/{len(results)} fetches failed")
    return successes