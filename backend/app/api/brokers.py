from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.middleware.auth import get_current_user
from app.services.brokers.registry import discover_brokers, get_broker, list_brokers
from app.services.brokers.sync import sync_broker_orders, sync_all_brokers, sync_positions

router = APIRouter()


@router.get("/brokers")
async def list_available_brokers(user=Depends(get_current_user)):
    discover_brokers()
    return {"brokers": list_brokers()}


@router.get("/brokers/{name}/account")
async def broker_account(name: str, user=Depends(get_current_user)):
    discover_brokers()
    cls = get_broker(name)
    if not cls:
        raise HTTPException(404, f"Unknown broker: {name}")
    broker = cls()
    try:
        return await broker.get_account()
    except Exception as e:
        raise HTTPException(502, f"Broker request failed: {e}")
    finally:
        await broker.close()


@router.delete("/brokers/{name}/orders/{order_id}")
async def broker_cancel_order(name: str, order_id: str, user=Depends(get_current_user)):
    discover_brokers()
    cls = get_broker(name)
    if not cls:
        raise HTTPException(404, f"Unknown broker: {name}")
    broker = cls()
    try:
        return await broker.cancel_order(order_id)
    except Exception as e:
        raise HTTPException(502, f"Broker cancel failed: {e}")
    finally:
        await broker.close()


@router.post("/brokers/sync/{name}")
async def broker_sync_orders(
    name: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    result = await sync_broker_orders(db, name)
    return result


@router.post("/brokers/sync")
async def broker_sync_all(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    results = await sync_all_brokers(db)
    return {"results": results}


@router.post("/brokers/sync/{name}/positions")
async def broker_sync_positions(
    name: str,
    portfolio_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    result = await sync_positions(db, name, portfolio_id)
    return result



@router.post("/brokers/{name}/orders")
async def broker_submit_order(name: str, order: dict, user=Depends(get_current_user)):
    discover_brokers()
    cls = get_broker(name)
    if not cls:
        raise HTTPException(404, f"Unknown broker: {name}")
    broker = cls()
    try:
        return await broker.submit_order(order)
    except Exception as e:
        raise HTTPException(502, f"Broker request failed: {e}")
    finally:
        await broker.close()


@router.get("/brokers/{name}/orders")
async def broker_orders(name: str, status: str = None, user=Depends(get_current_user)):
    discover_brokers()
    cls = get_broker(name)
    if not cls:
        raise HTTPException(404, f"Unknown broker: {name}")
    broker = cls()
    try:
        return await broker.get_orders(status=status)
    except Exception as e:
        raise HTTPException(502, f"Broker request failed: {e}")
    finally:
        await broker.close()
