import logging
from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user
from app.services.metaverse import gdp, real_estate, employment, arbitrage

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/metaverse", tags=["Metaverse"])


@router.get("/gdp")
async def gdp_overview(user: dict = Depends(get_current_user)):
    return await gdp.overview()


@router.get("/gdp/{world}")
async def gdp_world(world: str, user: dict = Depends(get_current_user)):
    return await gdp.world_gdp(world)


@router.get("/gdp/quarters")
async def gdp_quarters(user: dict = Depends(get_current_user)):
    return await gdp.total_gdp_by_quarter()


@router.get("/indices")
async def land_indices(user: dict = Depends(get_current_user)):
    return await real_estate.get_indices()


@router.get("/indices/{name}")
async def land_index(name: str, user: dict = Depends(get_current_user)):
    return await real_estate.get_index(name)


@router.get("/prime-locations")
async def prime_locations(user: dict = Depends(get_current_user)):
    return await real_estate.prime_locations()


@router.get("/employment")
async def employment_overview(user: dict = Depends(get_current_user)):
    return await employment.overview()


@router.get("/employment/{world}")
async def employment_world(world: str, user: dict = Depends(get_current_user)):
    return await employment.world_employment(world)


@router.get("/arbitrage")
async def arbitrage_opportunities(user: dict = Depends(get_current_user)):
    return await arbitrage.list_opportunities()
