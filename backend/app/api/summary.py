from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.summary import get_daily_summary

router = APIRouter(prefix="/summary", tags=["Summary"])


@router.get("")
async def daily_summary(
    date: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    uid = user.get("sub") or user.get("user_id")
    return await get_daily_summary(db, uid, date)
