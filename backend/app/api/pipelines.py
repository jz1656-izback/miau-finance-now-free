from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db

router = APIRouter()


@router.get("/runs")
async def list_pipeline_runs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("SELECT * FROM pipeline_runs ORDER BY created_at DESC LIMIT 50")
    )
    return [dict(row) for row in result.mappings().all()]


@router.post("/runs")
async def create_pipeline_run(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            INSERT INTO pipeline_runs (pipeline_name, status, started_at)
            VALUES ('manual_run', 'running', NOW())
            RETURNING *
        """)
    )
    await db.commit()
    return dict(result.mappings().first())


@router.post("/calculate/pnl")
async def calculate_pnl(db: AsyncSession = Depends(get_db)):
    await db.execute(text("""
        INSERT INTO pnl (portfolio_id, instrument_id, pnl_type, pnl_amount, currency, source, from_date, to_date)
        SELECT
            pos.portfolio_id,
            pos.instrument_id,
            'unrealized' as pnl_type,
            pos.unrealized_pnl as pnl_amount,
            pos.currency,
            'mark_to_market' as source,
            DATE(NOW()) - INTERVAL '30 days' as from_date,
            NOW() as to_date
        FROM positions pos
        WHERE pos.unrealized_pnl != 0
        ON CONFLICT DO NOTHING
    """))
    await db.commit()
    return {"status": "ok", "message": "P&L calculated"}
