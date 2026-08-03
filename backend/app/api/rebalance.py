import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.middleware.rbac import get_current_user_db
from app.services.analytics.rebalance import (
    detect_drift,
    generate_rebalance_plan,
    set_target_allocations,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/portfolios", tags=["Rebalance"])


@router.post("/{portfolio_id}/rebalance/drift")
async def portfolio_drift(
    portfolio_id: str,
    threshold: float = 0.05,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await detect_drift(portfolio_id, db, threshold)
    if result.get("error"):
        raise HTTPException(400, result["error"])
    return result


@router.post("/{portfolio_id}/rebalance/plan")
async def rebalance_plan(
    portfolio_id: str,
    targets: Optional[dict[str, float]] = None,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    if targets:
        result = await set_target_allocations(portfolio_id, targets, db)
    else:
        result = await generate_rebalance_plan(portfolio_id, db)
    if result.get("error"):
        raise HTTPException(400, result["error"])
    return result
