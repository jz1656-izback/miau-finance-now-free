from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from decimal import Decimal
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.paper_trading import (
    simulate_market_fill,
    simulate_limit_fill,
    simulate_stop_fill,
    simulate_trailing_stop_fill,
)

router = APIRouter()


async def get_current_user_db(db: AsyncSession = Depends(get_db), token_user: dict = Depends(get_current_user)) -> dict:
    username = token_user.get("sub")
    result = await db.execute(
        text("SELECT id, username, email, role FROM users WHERE username = :username"),
        {"username": username},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(401, "User not found")
    return dict(row)


@router.post("/paper/portfolios")
async def create_paper_portfolio(
    name: str,
    initial_cash: float = 100000.0,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            INSERT INTO paper_portfolios (id, user_id, name, initial_cash, current_cash)
            VALUES (gen_random_uuid(), :uid, :name, :cash, :cash)
            RETURNING id, user_id, name, initial_cash, current_cash, created_at
        """),
        {"uid": current_user["id"], "name": name, "cash": initial_cash},
    )
    await db.commit()
    return dict(result.mappings().first())


@router.get("/paper/portfolios")
async def list_paper_portfolios(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            SELECT pp.*, COUNT(pt.id) as trade_count
            FROM paper_portfolios pp
            LEFT JOIN paper_trades pt ON pt.paper_portfolio_id = pp.id
            WHERE pp.user_id = :uid
            GROUP BY pp.id
            ORDER BY pp.created_at DESC
        """),
        {"uid": current_user["id"]},
    )
    return [dict(row) for row in result.mappings().all()]


@router.get("/paper/portfolios/{portfolio_id}")
async def get_paper_portfolio(
    portfolio_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            SELECT pp.*, COUNT(pt.id) as trade_count,
                   COALESCE(SUM(CASE WHEN pt.side = 'BUY' THEN pt.quantity * pt.price ELSE 0 END), 0) as total_bought,
                   COALESCE(SUM(CASE WHEN pt.side = 'SELL' THEN pt.quantity * pt.price ELSE 0 END), 0) as total_sold
            FROM paper_portfolios pp
            LEFT JOIN paper_trades pt ON pt.paper_portfolio_id = pp.id
            WHERE pp.id = :id AND pp.user_id = :uid
            GROUP BY pp.id
        """),
        {"id": portfolio_id, "uid": current_user["id"]},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, "Paper portfolio not found")
    return dict(row)


@router.post("/paper/execute/{portfolio_id}")
async def execute_paper_trade(
    portfolio_id: str,
    instrument_id: str,
    side: str,
    quantity: float,
    order_type: str = "market",
    limit_price: Optional[float] = None,
    stop_price: Optional[float] = None,
    trail_pct: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    portfolio = await db.execute(
        text("SELECT id, current_cash FROM paper_portfolios WHERE id = :id AND user_id = :uid"),
        {"id": portfolio_id, "uid": current_user["id"]},
    )
    port = portfolio.mappings().first()
    if not port:
        raise HTTPException(404, "Paper portfolio not found")

    qty = Decimal(str(quantity))

    if order_type == "market":
        trade = await simulate_market_fill(db, portfolio_id, instrument_id, side, qty)
    elif order_type == "limit":
        if limit_price is None:
            raise HTTPException(400, "limit_price required for limit orders")
        trade = await simulate_limit_fill(db, portfolio_id, instrument_id, side, qty, Decimal(str(limit_price)))
    elif order_type == "stop":
        if stop_price is None:
            raise HTTPException(400, "stop_price required for stop orders")
        trade = await simulate_stop_fill(db, portfolio_id, instrument_id, side, qty, Decimal(str(stop_price)))
    elif order_type == "trailing_stop":
        if trail_pct is None:
            raise HTTPException(400, "trail_pct required for trailing_stop orders")
        trade = await simulate_trailing_stop_fill(db, portfolio_id, instrument_id, side, qty, Decimal(str(trail_pct)))
    else:
        raise HTTPException(400, f"Unknown order type: {order_type}")

    if trade is None:
        raise HTTPException(400, "Order conditions not met — no fill")

    cost = Decimal(str(trade["price"])) * qty + Decimal(str(trade["commission"]))
    if side.upper() == "SELL":
        cost = -cost

    await db.execute(
        text("UPDATE paper_portfolios SET current_cash = current_cash - :cost WHERE id = :id"),
        {"cost": cost, "id": portfolio_id},
    )
    await db.commit()

    return trade


@router.get("/paper/trades/{portfolio_id}")
async def get_paper_trade_history(
    portfolio_id: str,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    portfolio = await db.execute(
        text("SELECT id FROM paper_portfolios WHERE id = :id AND user_id = :uid"),
        {"id": portfolio_id, "uid": current_user["id"]},
    )
    if not portfolio.mappings().first():
        raise HTTPException(404, "Paper portfolio not found")

    result = await db.execute(
        text("""
            SELECT pt.*, i.ticker, i.name as instrument_name
            FROM paper_trades pt
            JOIN instruments i ON i.id = pt.instrument_id
            WHERE pt.paper_portfolio_id = :ppid
            ORDER BY pt.executed_at DESC
            LIMIT :limit OFFSET :offset
        """),
        {"ppid": portfolio_id, "limit": limit, "offset": offset},
    )
    return [dict(row) for row in result.mappings().all()]
