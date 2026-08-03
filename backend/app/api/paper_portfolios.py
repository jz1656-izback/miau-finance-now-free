from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from decimal import Decimal

from app.database import get_db
from app.middleware.auth import get_current_user
from app.middleware.rbac import get_current_user_db
from app.services.execution.paper_execution import get_paper_portfolio_value

router = APIRouter(prefix="/paper/portfolios", tags=["Paper Trading"])


@router.post("")
async def create_paper_portfolio(
    name: str,
    initial_cash: Decimal = Decimal("100000"),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            INSERT INTO paper_portfolios (id, user_id, name, initial_cash, current_cash)
            VALUES (gen_random_uuid(), :uid, :name, :cash, :cash)
            RETURNING id, name, initial_cash, current_cash, created_at
        """),
        {"uid": user["id"], "name": name, "cash": initial_cash},
    )
    await db.commit()
    return dict(result.mappings().first())


@router.get("")
async def list_paper_portfolios(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            SELECT id, name, initial_cash, current_cash, created_at
            FROM paper_portfolios WHERE user_id = :uid ORDER BY created_at DESC
        """),
        {"uid": user["id"]},
    )
    return {"portfolios": [dict(r) for r in result.mappings().all()]}


@router.get("/{portfolio_id}")
async def get_paper_portfolio(
    portfolio_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    value = await get_paper_portfolio_value(db, str(portfolio_id))
    if not value:
        raise HTTPException(404, "Paper portfolio not found")
    return value


@router.delete("/{portfolio_id}")
async def delete_paper_portfolio(
    portfolio_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("DELETE FROM paper_portfolios WHERE id = :pid AND user_id = :uid RETURNING id"),
        {"pid": portfolio_id, "uid": user["id"]},
    )
    await db.commit()
    if not result.rowcount:
        raise HTTPException(404, "Not found")
    return {"deleted": str(portfolio_id)}
