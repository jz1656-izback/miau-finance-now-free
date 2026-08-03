from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.services import ontology_service

router = APIRouter()


@router.get("")
async def search(
    q: str = Query(..., min_length=1, max_length=200, pattern=r"^[\w\s\-_.]{1,200}$"),
    type: Optional[str] = Query(None, pattern=r"^[\w\-]{0,50}$", max_length=50),
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_db),
):
    results = await ontology_service.search_objects(db, q, type, limit)
    return {
        "query": q,
        "total": len(results),
        "results": results,
    }
