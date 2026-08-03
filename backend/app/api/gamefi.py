import logging
from fastapi import APIRouter, Depends, Query
from app.middleware.auth import get_current_user
from app.services.gamefi import tokens, p2e_earnings, guilds, virtual_land, asset_valuation, yield_compare
from app.services.gamefi import nft_portfolio, nft_rental, scholarship_roi

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/gamefi", tags=["GameFi"])


@router.get("/tokens")
async def list_tokens(user: dict = Depends(get_current_user)):
    return await tokens.list_tokens()


@router.get("/tokens/{symbol}")
async def get_token(symbol: str, user: dict = Depends(get_current_user)):
    return await tokens.get_token(symbol)


@router.get("/p2e/games")
async def p2e_games(user: dict = Depends(get_current_user)):
    return await p2e_earnings.list_games()


@router.get("/p2e/{game_id}")
async def p2e_game(game_id: str, user: dict = Depends(get_current_user)):
    return await p2e_earnings.get_game(game_id)


@router.get("/p2e/{game_id}/simulate")
async def p2e_simulate(game_id: str, hours: float = Query(4), user: dict = Depends(get_current_user)):
    return await p2e_earnings.simulate_earnings(game_id, hours)


@router.get("/p2e/leaderboard")
async def p2e_leaderboard(user: dict = Depends(get_current_user)):
    return await p2e_earnings.leaderboard()


@router.get("/guilds")
async def list_guilds(user: dict = Depends(get_current_user)):
    return await guilds.list_guilds()


@router.get("/guilds/{guild_id}")
async def get_guild(guild_id: str, user: dict = Depends(get_current_user)):
    return await guilds.get_guild(guild_id)


@router.get("/guilds/compare")
async def guild_compare(user: dict = Depends(get_current_user)):
    return await guilds.guild_comparison()


@router.get("/virtual-land/worlds")
async def land_worlds(user: dict = Depends(get_current_user)):
    return await virtual_land.list_worlds()


@router.get("/virtual-land/{world_id}")
async def land_world(world_id: str, user: dict = Depends(get_current_user)):
    return await virtual_land.get_world(world_id)


@router.get("/virtual-land/{world_id}/history")
async def land_history(world_id: str, user: dict = Depends(get_current_user)):
    return await virtual_land.price_history(world_id)


@router.post("/assets/estimate")
async def estimate_value(parcels: list[dict], user: dict = Depends(get_current_user)):
    return await virtual_land.portfolio_estimate(parcels)


@router.get("/valuations/types")
async def valuation_types(user: dict = Depends(get_current_user)):
    return await asset_valuation.list_assets()


@router.get("/valuations/estimate")
async def valuation_estimate(
    asset: str = Query("axie"), category: str = Query("common"), quantity: int = Query(1),
    user: dict = Depends(get_current_user),
):
    return await asset_valuation.estimate_value(asset, category, quantity)


@router.get("/yields")
async def yields_all(max_risk: str = Query("high"), user: dict = Depends(get_current_user)):
    return await yield_compare.by_risk(max_risk)


@router.get("/nft/portfolio")
async def nft_portfolio_list(user: dict = Depends(get_current_user)):
    return await nft_portfolio.get_portfolio()


@router.get("/nft/rental/yields")
async def nft_rental_yields(user: dict = Depends(get_current_user)):
    return await nft_rental.list_opportunities()


@router.get("/scholarship/roi")
async def scholarship_roi_calc(
    cost: float = Query(500), monthly: float = Query(150), split: float = Query(30),
    user: dict = Depends(get_current_user),
):
    return await scholarship_roi.calculate(cost, monthly, split)
