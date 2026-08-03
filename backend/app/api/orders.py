from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.order_service import (
    validate_order,
    pre_trade_risk_check,
    create_order,
    get_order,
    list_orders,
    update_order,
    cancel_order,
)

router = APIRouter()


@router.post("/orders")
async def create_order_endpoint(
    portfolio_id: str,
    instrument_id: str,
    order_type: str,
    side: str,
    quantity: float,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    errors = await validate_order(
        db, portfolio_id, instrument_id, order_type, side, quantity, price, stop_price
    )
    if errors:
        raise HTTPException(400, detail=errors)

    if price is None:
        price_result = await db.execute(
            text("SELECT close FROM market_data WHERE instrument_id = :id ORDER BY date DESC LIMIT 1"),
            {"id": instrument_id},
        )
        trade_price = float(price_result.scalar() or 100.0)
    else:
        trade_price = price
    risk = await pre_trade_risk_check(db, portfolio_id, instrument_id, side, quantity, trade_price)
    if not risk["passed"]:
        raise HTTPException(400, detail=risk["errors"])

    order = await create_order(
        db, portfolio_id, instrument_id, order_type, side, quantity, price, stop_price,
        user_id=current_user.get("sub"),
    )
    return order


@router.get("/orders")
async def list_orders_endpoint(
    portfolio_id: Optional[str] = Query(None),
    instrument_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    items = await list_orders(db, portfolio_id, instrument_id, status, limit, offset, user_id=current_user.get("sub"))
    total_result = await db.execute(
        text("SELECT COUNT(*) FROM orders WHERE user_id = :uid"),
        {"uid": current_user.get("sub", "")},
    )
    total = total_result.scalar()
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/orders/{order_id}")
async def get_order_endpoint(
    order_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    order = await get_order(db, order_id, user_id=current_user.get("sub"))
    if not order:
        raise HTTPException(404, "Order not found")
    return order


@router.put("/orders/{order_id}")
async def update_order_endpoint(
    order_id: str,
    quantity: Optional[float] = None,
    price: Optional[float] = None,
    stop_price: Optional[float] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        order = await update_order(db, order_id, quantity, price, stop_price, user_id=current_user.get("sub"))
    except ValueError as e:
        raise HTTPException(400, str(e))
    if not order:
        raise HTTPException(404, "Order not found")
    return order


@router.delete("/orders/{order_id}")
async def cancel_order_endpoint(
    order_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        order = await cancel_order(db, order_id, user_id=current_user.get("sub"))
    except ValueError as e:
        raise HTTPException(400, str(e))
    if not order:
        raise HTTPException(404, "Order not found")
    return order
