"""Jobs API — search FinTech jobs matching Jevgeni's profile."""
import logging
from fastapi import APIRouter, Depends, Query

from app.middleware.auth import get_current_user
from app.services.jobs_service import search_jobs, get_job_summary, search_github_jobs

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs"])


@router.get("/search")
async def search_fintech_jobs(
    skill: str = Query("", description="Filter by skill (Python, React, etc.)"),
    location: str = Query("Germany"),
    remote: bool = Query(True),
    user: dict = Depends(get_current_user),
):
    results = await search_jobs(skill, location, remote)
    return {"jobs": results, "count": len(results)}


@router.get("/summary")
async def jobs_summary(user: dict = Depends(get_current_user)):
    return await get_job_summary()


@router.get("/github")
async def github_jobs(
    query: str = Query("fintech python react"),
    user: dict = Depends(get_current_user),
):
    results = await search_github_jobs(query)
    return {"jobs": results, "count": len(results)}
