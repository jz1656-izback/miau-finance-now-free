from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.activity_service import get_activity

router = APIRouter()


@router.get("")
async def list_activity(
    workspace_id: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    username = current_user.get("sub")
    user_row = await db.execute(
        text("SELECT id FROM users WHERE username = :username"),
        {"username": username},
    )
    user = user_row.mappings().first()
    if not user:
        raise HTTPException(401, "User not found")

    items = await get_activity(
        db=db,
        workspace_id=workspace_id,
        limit=limit,
        offset=offset,
    )

    count_result = await db.execute(
        text("""
            SELECT COUNT(*) FROM activity_logs al
            WHERE al.user_id = :user_id
        """),
        {"user_id": user["id"]},
    )
    total = count_result.scalar()

    return {"items": items, "total": total, "limit": limit, "offset": offset}
