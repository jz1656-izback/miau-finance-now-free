import random
from decimal import Decimal
from typing import Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings


def calc_slippage(quantity: Decimal, price: Decimal, side: str) -> Decimal:
    slippage_pct = Decimal(str(settings.paper_slippage_pct))
    direction = Decimal("1") if side.upper() == "BUY" else Decimal("-1")
    return quantity * price * slippage_pct * direction


def calc_commission(quantity: Decimal, price: Decimal) -> Decimal:
    rate = Decimal(str(settings.paper_commission_rate))
    return quantity * price * rate


def calc_tca_cost(quantity: Decimal, price: Decimal, market_impact: float = 0.0005) -> Decimal:
    return quantity * price * Decimal(str(market_impact))


async def simulate_market_fill(
    db: AsyncSession,
    paper_portfolio_id: str,
    instrument_id: str,
    side: str,
    quantity: Decimal,
) -> dict:
    price_result = await db.execute(
        text("SELECT close FROM market_data WHERE instrument_id = :id ORDER BY date DESC LIMIT 1"),
        {"id": instrument_id},
    )
    row = price_result.scalar()
    latest_price = Decimal(str(row)) if row else Decimal("100.0")

    slippage = calc_slippage(quantity, latest_price, side)
    commission = calc_commission(quantity, latest_price)
    tca_cost = calc_tca_cost(quantity, latest_price)

    fill_price = latest_price + slippage / quantity if quantity else latest_price

    result = await db.execute(
        text("""
            INSERT INTO paper_trades (id, paper_portfolio_id, instrument_id, side, quantity, price, commission, slippage, tca_cost)
            VALUES (gen_random_uuid(), :ppid, :iid, :side, :qty, :price, :comm, :slip, :tca)
            RETURNING *
        """),
        {
            "ppid": paper_portfolio_id,
            "iid": instrument_id,
            "side": side.upper(),
            "qty": quantity,
            "price": fill_price,
            "comm": commission,
            "slip": slippage,
            "tca": tca_cost,
        },
    )
    return dict(result.mappings().first())


async def simulate_limit_fill(
    db: AsyncSession,
    paper_portfolio_id: str,
    instrument_id: str,
    side: str,
    quantity: Decimal,
    limit_price: Decimal,
) -> Optional[dict]:
    price_result = await db.execute(
        text("SELECT close FROM market_data WHERE instrument_id = :id ORDER BY date DESC LIMIT 1"),
        {"id": instrument_id},
    )
    row = price_result.scalar()
    latest_price = Decimal(str(row)) if row else Decimal("100.0")

    if side.upper() == "BUY" and limit_price < latest_price:
        return None
    if side.upper() == "SELL" and limit_price > latest_price:
        return None

    slippage = calc_slippage(quantity, limit_price, side)
    commission = calc_commission(quantity, limit_price)
    tca_cost = calc_tca_cost(quantity, limit_price)

    result = await db.execute(
        text("""
            INSERT INTO paper_trades (id, paper_portfolio_id, instrument_id, side, quantity, price, commission, slippage, tca_cost)
            VALUES (gen_random_uuid(), :ppid, :iid, :side, :qty, :price, :comm, :slip, :tca)
            RETURNING *
        """),
        {
            "ppid": paper_portfolio_id,
            "iid": instrument_id,
            "side": side.upper(),
            "qty": quantity,
            "price": limit_price,
            "comm": commission,
            "slip": slippage,
            "tca": tca_cost,
        },
    )
    return dict(result.mappings().first())


async def simulate_stop_fill(
    db: AsyncSession,
    paper_portfolio_id: str,
    instrument_id: str,
    side: str,
    quantity: Decimal,
    stop_price: Decimal,
) -> Optional[dict]:
    price_result = await db.execute(
        text("SELECT close FROM market_data WHERE instrument_id = :id ORDER BY date DESC LIMIT 1"),
        {"id": instrument_id},
    )
    row = price_result.scalar()
    latest_price = Decimal(str(row)) if row else Decimal("100.0")

    if side.upper() == "BUY" and latest_price < stop_price:
        return None
    if side.upper() == "SELL" and latest_price > stop_price:
        return None

    return await simulate_market_fill(db, paper_portfolio_id, instrument_id, side, quantity)


async def simulate_trailing_stop_fill(
    db: AsyncSession,
    paper_portfolio_id: str,
    instrument_id: str,
    side: str,
    quantity: Decimal,
    trail_pct: Decimal,
) -> Optional[dict]:
    price_result = await db.execute(
        text("""
            SELECT MAX(high) as high, MIN(low) as low
            FROM market_data WHERE instrument_id = :id
            AND date >= NOW() - INTERVAL '7 days'
        """),
        {"id": instrument_id},
    )
    row = price_result.mappings().first()
    if not row:
        return None

    if side.upper() == "SELL":
        high = Decimal(str(row["high"])) if row["high"] else Decimal("100")
        stop_price = high * (Decimal("1") - trail_pct / Decimal("100"))
    else:
        low = Decimal(str(row["low"])) if row["low"] else Decimal("100")
        stop_price = low * (Decimal("1") + trail_pct / Decimal("100"))

    return await simulate_stop_fill(db, paper_portfolio_id, instrument_id, side, quantity, stop_price)
