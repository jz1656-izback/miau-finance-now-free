from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models import OrderStatus
from app.config import settings


class OrderStateMachine:
    TRANSITIONS = {
        OrderStatus.PENDING: {OrderStatus.SUBMITTED, OrderStatus.CANCELLED, OrderStatus.REJECTED},
        OrderStatus.SUBMITTED: {OrderStatus.PARTIALLY_FILLED, OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED},
        OrderStatus.PARTIALLY_FILLED: {OrderStatus.FILLED, OrderStatus.CANCELLED},
        OrderStatus.FILLED: set(),
        OrderStatus.CANCELLED: set(),
        OrderStatus.REJECTED: set(),
        OrderStatus.EXPIRED: set(),
    }

    @classmethod
    def can_transition(cls, current: OrderStatus, target: OrderStatus) -> bool:
        return target in cls.TRANSITIONS.get(current, set())

    @classmethod
    def valid_transitions(cls, current: OrderStatus) -> set[OrderStatus]:
        return cls.TRANSITIONS.get(current, set())


RISK_CONFIG = {
    "max_position_per_instrument": 100000,
    "max_position_per_portfolio": 1000000,
    "max_concentration_pct": 25.0,
    "daily_loss_limit": 50000,
}


async def check_position_limits(
    db: AsyncSession,
    portfolio_id: str,
    instrument_id: str,
    side: str,
    quantity: float,
    price: float,
) -> list[str]:
    errors = []
    order_value = quantity * price

    port_result = await db.execute(
        text("SELECT current_cash, initial_cash FROM paper_portfolios WHERE id = :id"),
        {"id": portfolio_id},
    )
    port = port_result.mappings().first()
    portfolio_value = float(port["current_cash"]) if port else 0.0
    if not port:
        portfolio_value = 1000000.0

    if side.upper() == "BUY" and order_value > portfolio_value:
        errors.append("Insufficient buying power")

    position_result = await db.execute(
        text("""
            SELECT COALESCE(SUM(CASE WHEN side = 'BUY' THEN quantity ELSE -quantity END), 0) as net_position
            FROM paper_trades WHERE paper_portfolio_id = :ppid AND instrument_id = :iid
        """),
        {"ppid": portfolio_id, "iid": instrument_id},
    )
    current_position = float(position_result.scalar() or 0)
    new_position = current_position + (quantity if side.upper() == "BUY" else -quantity)

    if abs(new_position * price) > RISK_CONFIG["max_position_per_instrument"]:
        errors.append(f"Position limit exceeded: max {RISK_CONFIG['max_position_per_instrument']} per instrument")

    total_exposure = await db.execute(
        text("""
            SELECT COALESCE(SUM(ABS(quantity * price)), 0) FROM paper_trades WHERE paper_portfolio_id = :ppid
        """),
        {"ppid": portfolio_id},
    )
    total = float(total_exposure.scalar() or 0)
    concentration = (abs(new_position * price) / max(portfolio_value, 1)) * 100
    if concentration > RISK_CONFIG["max_concentration_pct"]:
        errors.append(f"Concentration limit exceeded: max {RISK_CONFIG['max_concentration_pct']}%")

    return errors


async def check_daily_loss_limit(
    db: AsyncSession,
    portfolio_id: str,
) -> list[str]:
    errors = []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Check paper_trades for daily loss
    daily_result = await db.execute(
        text("""
            SELECT COALESCE(SUM(
                CASE WHEN side = 'SELL' THEN quantity * price
                ELSE -quantity * price END
            ), 0) as daily_pnl
            FROM paper_trades
            WHERE paper_portfolio_id = :ppid
            AND DATE(executed_at) = :today
        """),
        {"ppid": portfolio_id, "today": today},
    )
    daily_pnl = float(daily_result.scalar() or 0)

    if daily_pnl < -RISK_CONFIG["daily_loss_limit"]:
        errors.append(f"Daily loss limit exceeded: ${abs(daily_pnl):.2f} loss exceeds ${RISK_CONFIG['daily_loss_limit']} limit")

    return errors


async def pre_trade_risk_check(
    db: AsyncSession,
    portfolio_id: str,
    instrument_id: str,
    side: str,
    quantity: float,
    price: float,
) -> dict:
    errors = []
    errors.extend(await check_position_limits(db, portfolio_id, instrument_id, side, quantity, price))
    errors.extend(await check_daily_loss_limit(db, portfolio_id))

    if errors:
        return {"passed": False, "errors": errors}
    return {"passed": True, "errors": []}


async def validate_order(
    db: AsyncSession,
    portfolio_id: str,
    instrument_id: str,
    order_type: str,
    side: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
) -> list[str]:
    errors = []

    if quantity <= 0:
        errors.append("Quantity must be positive")

    if side.upper() not in ("BUY", "SELL"):
        errors.append("Side must be BUY or SELL")

    instrument = await db.execute(
        text("SELECT id, status FROM instruments WHERE id = :id"),
        {"id": instrument_id},
    )
    inst = instrument.mappings().first()
    if not inst:
        errors.append("Instrument not found")
    elif inst["status"] != "active":
        errors.append("Instrument is not active")

    portfolio = await db.execute(
        text("SELECT id, status FROM portfolios WHERE id = :id"),
        {"id": portfolio_id},
    )
    port = portfolio.mappings().first()
    if not port:
        errors.append("Portfolio not found")
    elif port["status"] != "active":
        errors.append("Portfolio is not active")

    if order_type in ("LIMIT", "STOP_LIMIT") and price is None:
        errors.append("Price is required for LIMIT and STOP_LIMIT orders")
    if order_type in ("STOP", "STOP_LIMIT", "TRAILING_STOP") and stop_price is None:
        errors.append("Stop price is required for STOP, STOP_LIMIT, and TRAILING_STOP orders")

    return errors


async def create_order(
    db: AsyncSession,
    portfolio_id: str,
    instrument_id: str,
    order_type: str,
    side: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
    user_id: Optional[str] = None,
) -> dict:
    result = await db.execute(
        text("""
            INSERT INTO orders (id, portfolio_id, instrument_id, order_type, side, quantity, price, stop_price, user_id, status)
            VALUES (gen_random_uuid(), :portfolio_id, :instrument_id, :order_type, :side, :quantity, :price, :stop_price, :user_id, 'PENDING')
            RETURNING *
        """),
        {
            "portfolio_id": portfolio_id,
            "instrument_id": instrument_id,
            "order_type": order_type,
            "side": side.upper(),
            "quantity": quantity,
            "price": price,
            "stop_price": stop_price,
            "user_id": user_id or "",
        },
    )
    await db.commit()
    return dict(result.mappings().first())


async def get_order(db: AsyncSession, order_id: str, user_id: Optional[str] = None) -> Optional[dict]:
    query = "SELECT * FROM orders WHERE id = :id"
    params = {"id": order_id}
    if user_id:
        query += " AND user_id = :uid"
        params["uid"] = user_id
    result = await db.execute(text(query), params)
    row = result.mappings().first()
    return dict(row) if row else None


async def list_orders(
    db: AsyncSession,
    portfolio_id: Optional[str] = None,
    instrument_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    user_id: Optional[str] = None,
) -> list[dict]:
    conditions = []
    params: dict = {"limit": limit, "offset": offset}

    if user_id:
        conditions.append("o.user_id = :user_id")
        params["user_id"] = user_id
    if portfolio_id:
        conditions.append("o.portfolio_id = :portfolio_id")
        params["portfolio_id"] = portfolio_id
    if instrument_id:
        conditions.append("o.instrument_id = :instrument_id")
        params["instrument_id"] = instrument_id
    if status:
        conditions.append("o.status = :status")
        params["status"] = status

    where = " AND ".join(conditions) if conditions else "TRUE"

    result = await db.execute(
        text(f"""
            SELECT o.*, i.ticker, i.name as instrument_name, p.name as portfolio_name
            FROM orders o
            JOIN instruments i ON i.id = o.instrument_id
            JOIN portfolios p ON p.id = o.portfolio_id
            WHERE {where}
            ORDER BY o.created_at DESC
            LIMIT :limit OFFSET :offset
        """),
        params,
    )
    return [dict(row) for row in result.mappings().all()]


async def update_order(
    db: AsyncSession,
    order_id: str,
    quantity: Optional[float] = None,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
    user_id: Optional[str] = None,
) -> Optional[dict]:
    order = await get_order(db, order_id, user_id=user_id)
    if not order:
        return None

    if order["status"] not in ("PENDING", "SUBMITTED"):
        raise ValueError("Only PENDING or SUBMITTED orders can be modified")

    sets = []
    params: dict = {"id": order_id}
    if quantity is not None:
        sets.append("quantity = :quantity")
        params["quantity"] = quantity
    if price is not None:
        sets.append("price = :price")
        params["price"] = price
    if stop_price is not None:
        sets.append("stop_price = :stop_price")
        params["stop_price"] = stop_price

    if not sets:
        return order

    sets.append("updated_at = NOW()")

    result = await db.execute(
        text(f"UPDATE orders SET {', '.join(sets)} WHERE id = :id RETURNING *"),
        params,
    )
    await db.commit()
    return dict(result.mappings().first())


async def cancel_order(db: AsyncSession, order_id: str, user_id: Optional[str] = None) -> Optional[dict]:
    order = await get_order(db, order_id, user_id=user_id)
    if not order:
        return None

    if order["status"] not in ("PENDING", "SUBMITTED"):
        raise ValueError("Only PENDING or SUBMITTED orders can be cancelled")

    result = await db.execute(
        text("""
            UPDATE orders SET status = 'CANCELLED', updated_at = NOW()
            WHERE id = :id RETURNING *
        """),
        {"id": order_id},
    )
    await db.commit()
    return dict(result.mappings().first())
