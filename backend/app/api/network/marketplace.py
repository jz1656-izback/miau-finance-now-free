import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from app.middleware.auth import get_current_user
from app.services.network.strategy_nft import mint_strategy, get_strategy, list_strategies, list_my_strategies
from app.services.network.licensing import purchase_license, get_license, list_licenses, LICENSE_TIERS
from app.services.network.reputation import rate_strategy, get_strategy_reputation
from app.services.network.audit import validate_strategy

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/network", tags=["Network"])


@router.post("/strategies/mint")
async def api_mint_strategy(name: str, description: str, code: str, backtest_return: float = 0, backtest_sharpe: float = 0, user=Depends(get_current_user)):
    audit = await validate_strategy(code)
    if not audit["passed"]:
        raise HTTPException(400, f"Strategy validation failed: {audit['audit']['risk_level']} risk")
    result = await mint_strategy(name, user.get("sub", "anonymous"), description, hash(code), {"total_return_pct": backtest_return, "sharpe_ratio": backtest_sharpe})
    result["audit"] = audit["audit"]
    return result


@router.get("/strategies")
async def api_list_strategies(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
    items, total = await list_strategies(limit, offset)
    return {"items": items, "total": total}


@router.get("/strategies/{strategy_id}")
async def api_get_strategy(strategy_id: str):
    s = await get_strategy(strategy_id)
    if not s:
        raise HTTPException(404, "Strategy not found")
    rep = await get_strategy_reputation(strategy_id)
    s["reputation"] = rep
    return s


@router.get("/strategies/{strategy_id}/reputation")
async def api_strategy_reputation(strategy_id: str):
    return await get_strategy_reputation(strategy_id)


@router.post("/strategies/{strategy_id}/rate")
async def api_rate_strategy(strategy_id: str, rating: int = Query(..., ge=1, le=5), review: str = "", user=Depends(get_current_user)):
    return await rate_strategy(strategy_id, user.get("sub", "anonymous"), rating, review)


@router.post("/strategies/{strategy_id}/purchase")
async def api_purchase_license(strategy_id: str, tier: str = "standard", user=Depends(get_current_user)):
    if tier not in LICENSE_TIERS:
        raise HTTPException(400, f"Invalid tier. Choose from: {list(LICENSE_TIERS.keys())}")
    result = await purchase_license(user.get("sub", "anonymous"), strategy_id, tier)
    if not result:
        raise HTTPException(400, "Purchase failed")
    return result


@router.get("/licenses")
async def api_list_licenses(user=Depends(get_current_user)):
    return await list_licenses(user.get("sub", "anonymous"))


@router.get("/licenses/{license_id}")
async def api_get_license(license_id: str):
    l = await get_license(license_id)
    if not l:
        raise HTTPException(404, "License not found")
    return l
