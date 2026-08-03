import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.brokers.registry import discover_brokers, get_broker, list_brokers

logger = logging.getLogger(__name__)


async def sync_broker_orders(
    db: AsyncSession,
    broker_name: str,
) -> dict:
    discover_brokers()
    cls = get_broker(broker_name)
    if not cls:
        return {"broker": broker_name, "status": "error", "message": f"Unknown broker: {broker_name}"}

    broker = cls()
    try:
        await broker.connect() if hasattr(broker, "connect") else None
        remote_orders = await broker.get_orders()

        local = await db.execute(
            text("SELECT id, broker_order_id, status FROM orders WHERE broker_order_id IS NOT NULL"),
        )
        local_orders = {r.broker_order_id: r for r in local.mappings().all()}

        synced = 0
        for remote in remote_orders:
            remote_id = remote.get("id")
            remote_status = remote.get("status", "").upper()
            if remote_id in local_orders:
                local_status = local_orders[remote_id].status
                if local_status != remote_status:
                    await db.execute(
                        text("UPDATE orders SET status = :status, updated_at = NOW() WHERE broker_order_id = :oid"),
                        {"status": remote_status, "oid": remote_id},
                    )
                    synced += 1

        await db.commit()
        return {
            "broker": broker_name,
            "status": "ok",
            "remote_orders": len(remote_orders),
            "local_orders": len(local_orders),
            "synced": synced,
        }
    except Exception as e:
        logger.error(f"Sync failed for {broker_name}: {e}")
        return {"broker": broker_name, "status": "error", "message": str(e)}
    finally:
        await broker.close()


async def sync_all_brokers(db: AsyncSession) -> list[dict]:
    discover_brokers()
    results = []
    for info in list_brokers():
        result = await sync_broker_orders(db, info["name"])
        results.append(result)
    return results


async def sync_positions(
    db: AsyncSession,
    broker_name: str,
    portfolio_id: str,
) -> dict:
    discover_brokers()
    cls = get_broker(broker_name)
    if not cls:
        return {"broker": broker_name, "status": "error", "message": f"Unknown broker: {broker_name}"}

    broker = cls()
    try:
        await broker.connect() if hasattr(broker, "connect") else None
        positions = await broker.get_positions()

        for pos in positions:
            ticker = pos.get("symbol")
            qty = pos.get("qty", 0)
            market_value = pos.get("market_value", 0)

            inst = await db.execute(
                text("SELECT id FROM instruments WHERE ticker = :ticker"),
                {"ticker": ticker},
            )
            instrument = inst.mappings().first()
            if not instrument:
                continue

            existing = await db.execute(
                text("""
                    SELECT id FROM positions
                    WHERE portfolio_id = :pid AND instrument_id = :iid
                """),
                {"pid": portfolio_id, "iid": instrument["id"]},
            )
            if existing.mappings().first():
                await db.execute(
                    text("""
                        UPDATE positions
                        SET quantity = :qty, market_value = :mv, updated_at = NOW()
                        WHERE portfolio_id = :pid AND instrument_id = :iid
                    """),
                    {"qty": qty, "mv": market_value, "pid": portfolio_id, "iid": instrument["id"]},
                )
            else:
                await db.execute(
                    text("""
                        INSERT INTO positions (id, portfolio_id, instrument_id, quantity, market_value, as_of_date)
                        VALUES (gen_random_uuid(), :pid, :iid, :qty, :mv, NOW())
                    """),
                    {"pid": portfolio_id, "iid": instrument["id"], "qty": qty, "mv": market_value},
                )

        await db.commit()
        return {"broker": broker_name, "status": "ok", "positions_synced": len(positions)}
    except Exception as e:
        logger.error(f"Position sync failed for {broker_name}: {e}")
        return {"broker": broker_name, "status": "error", "message": str(e)}
    finally:
        await broker.close()
