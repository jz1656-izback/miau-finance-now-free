"""Alternative Assets — gold, crypto, collectibles, private equity tracking."""
import logging
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def track_alternative_asset(
    db: AsyncSession,
    name: str,
    asset_type: str,
    value: float,
    quantity: float = 1,
    notes: str = "",
) -> dict:
    """Track an alternative asset (gold, art, collectibles, private equity)."""
    await db.execute(
        text("""
            INSERT INTO alternative_assets (id, name, asset_type, quantity, current_value, notes, last_valuation, created_at)
            VALUES (gen_random_uuid(), :name, :type, :qty, :value, :notes, NOW(), NOW())
            ON CONFLICT (name, asset_type) DO UPDATE SET
                current_value = :value2, quantity = :qty2, notes = :notes2, last_valuation = NOW()
            RETURNING id
        """),
        {"name": name, "type": asset_type, "qty": quantity, "value": value, "notes": notes,
         "value2": value, "qty2": quantity, "notes2": notes},
    )
    await db.commit()
    return {"name": name, "type": asset_type, "value": value, "status": "tracked"}


async def get_alternative_summary(db: AsyncSession) -> dict:
    """Get alternative assets portfolio summary."""
    rows = await db.execute(
        text("""
            SELECT asset_type,
                   COALESCE(SUM(current_value), 0) as total_value,
                   COUNT(*) as count
            FROM alternative_assets
            GROUP BY asset_type
        """),
    )
    assets = [{"type": r["asset_type"], "value": float(r["total_value"]), "count": r["count"]}
              for r in rows.mappings()]
    total = sum(a["value"] for a in assets)
    return {
        "total_alternative_value": total,
        "by_type": assets,
        "count": len(assets),
    }
