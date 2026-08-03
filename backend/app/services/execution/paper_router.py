from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal
from app.models import OrderType, OrderStatus
from app.services.execution.fill_simulator import FillSimulator


async def route_paper_order(
    db: AsyncSession,
    order_id: str,
    order_type: OrderType,
    side: str,
    quantity: Decimal,
    price: Decimal | None,
    stop_price: Decimal | None,
    current_price: Decimal,
    simulator: FillSimulator | None = None,
) -> dict:
    if simulator is None:
        simulator = FillSimulator()

    exec_price = current_price
    if order_type == OrderType.LIMIT and price:
        exec_price = price
    elif order_type == OrderType.STOP and stop_price:
        exec_price = stop_price
    elif order_type == OrderType.STOP_LIMIT and stop_price:
        exec_price = stop_price

    fill = simulator.simulate_fill(side, quantity, exec_price, current_price)
    new_status = OrderStatus.FILLED

    result = await db.execute(
        text("""
            UPDATE orders
            SET status = :status, filled_qty = :qty, filled_avg_price = :price,
                filled_at = NOW(), updated_at = NOW()
            WHERE id = :oid
            RETURNING id, status, filled_qty, filled_avg_price, filled_at
        """),
        {
            "oid": order_id, "status": new_status.value,
            "qty": fill.filled_qty, "price": fill.fill_price,
        },
    )
    await db.commit()
    return dict(result.mappings().first())
