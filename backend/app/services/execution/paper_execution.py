from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from datetime import datetime
from typing import Optional


async def execute_paper_trade(
    db: AsyncSession,
    paper_portfolio_id: str,
    instrument_id: str,
    side: str,
    quantity: Decimal,
    price: Decimal,
    commission: Decimal = Decimal("0"),
    slippage: Decimal = Decimal("0"),
    tca_cost: Decimal = Decimal("0"),
) -> dict:
    result = await db.execute(
        text("""
            INSERT INTO paper_trades (id, paper_portfolio_id, instrument_id, side, quantity, price, commission, slippage, tca_cost)
            VALUES (gen_random_uuid(), :ppid, :iid, :side, :qty, :price, :comm, :slip, :tca)
            RETURNING id, paper_portfolio_id, instrument_id, side, quantity, price, commission, slippage, tca_cost, executed_at
        """),
        {
            "ppid": paper_portfolio_id, "iid": instrument_id, "side": side,
            "qty": quantity, "price": price, "comm": commission,
            "slip": slippage, "tca": tca_cost,
        },
    )
    await db.commit()
    return dict(result.mappings().first())


async def get_paper_portfolio_value(db: AsyncSession, paper_portfolio_id: str) -> dict:
    result = await db.execute(
        text("""
            SELECT pp.id, pp.name, pp.initial_cash, pp.current_cash,
                   COALESCE(SUM(pt.quantity * pt.price * CASE WHEN pt.side = 'BUY' THEN 1 ELSE -1 END), 0) as position_value
            FROM paper_portfolios pp
            LEFT JOIN paper_trades pt ON pt.paper_portfolio_id = pp.id
            WHERE pp.id = :ppid
            GROUP BY pp.id, pp.name, pp.initial_cash, pp.current_cash
        """),
        {"ppid": paper_portfolio_id},
    )
    row = result.mappings().first()
    if not row:
        return {}
    pos_value = float(row["position_value"]) if row["position_value"] else 0
    cash = float(row["current_cash"])
    return {
        "id": str(row["id"]),
        "name": row["name"],
        "initial_cash": float(row["initial_cash"]),
        "current_cash": cash,
        "position_value": pos_value,
        "total_equity": cash + pos_value,
    }
