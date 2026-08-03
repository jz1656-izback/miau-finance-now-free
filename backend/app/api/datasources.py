"""Data source health and status dashboard API."""
import time
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from app.middleware.auth import get_current_user
from app.services.data.registry import registry
from app.services.data.cache import DataCache

router = APIRouter(prefix="/api/v1/datasources", tags=["Data Sources"])
cache = DataCache()


class KeySetRequest(BaseModel):
    provider: str
    key: str


@router.get("/status")
async def datasource_health(user: dict = Depends(get_current_user)):
    results = []
    for p in registry.list():
        try:
            start = time.time()
            health = await p.health()
            latency = round((time.time() - start) * 1000, 1)
            entry = health.model_dump()
            entry["latency_ms"] = latency
            entry["remaining_quota"] = p.remaining_quota
            entry["stats"] = p.stats
            results.append(entry)
        except Exception as e:
            results.append({"provider": p.name, "healthy": False, "error": str(e), "remaining_quota": 0})
    return {
        "providers": results,
        "total": len(results),
        "healthy": sum(1 for r in results if r.get("healthy")),
        "cache": cache.stats(),
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


@router.get("/providers")
async def list_providers(user: dict = Depends(get_current_user)):
    return {
        "providers": [
            {
                "name": p.name,
                "requires_key": p.requires_key,
                "rate_limit": p.rate_limit_per_minute,
                "capabilities": p.capabilities,
                "stats": p.stats,
            }
            for p in registry.list()
        ],
        "total": registry.count(),
    }


@router.get("/keys")
async def list_keys(user: dict = Depends(get_current_user)):
    from app.services.data.vault import list_keys
    return {"keys": list_keys()}


@router.put("/keys")
async def set_key(req: KeySetRequest, user: dict = Depends(get_current_user)):
    if not req.provider or not req.key:
        raise HTTPException(400, "Provider and key are required")
    if len(req.key) < 4:
        raise HTTPException(400, "Key must be at least 4 characters")
    from app.services.data.vault import set_key
    set_key(req.provider, req.key)
    return {"status": "ok", "provider": req.provider, "message": f"API key for {req.provider} configured"}


@router.delete("/keys/{provider}")
async def delete_key(provider: str, user: dict = Depends(get_current_user)):
    from app.services.data.vault import delete_key
    delete_key(provider)
    return {"status": "ok", "provider": provider}


@router.get("/fallback-chains")
async def fallback_chains(user: dict = Depends(get_current_user)):
    capability_map: dict[str, list[dict]] = {}
    for p in registry.list():
        for cap in p.capabilities:
            if cap not in capability_map:
                capability_map[cap] = []
            capability_map[cap].append({
                "name": p.name,
                "priority": len(capability_map[cap]) + 1,
                "requires_key": p.requires_key,
                "rate_limit": p.rate_limit_per_minute,
            })
    for cap in capability_map:
        capability_map[cap] = sorted(capability_map[cap], key=lambda x: (x["requires_key"], -x["rate_limit"]))
        for i, prov in enumerate(capability_map[cap]):
            prov["fallback_order"] = i + 1
    return {
        "capabilities": capability_map,
        "total_capabilities": len(capability_map),
    }


@router.post("/keys/test")
async def test_key(
    provider: str = Query(..., description="Provider name to test"),
    user: dict = Depends(get_current_user),
):
    from app.services.data.vault import get_key
    key = get_key(provider)
    if not key:
        raise HTTPException(404, f"No key configured for {provider}")
    prov = registry.get(provider)
    if not prov:
        raise HTTPException(404, f"Provider '{provider}' not found")
    try:
        result = await prov.health()
        return {"provider": provider, "healthy": result.healthy, "latency_ms": None, "message": "Key works" if result.healthy else "Key failed health check"}
    except Exception as e:
        return {"provider": provider, "healthy": False, "latency_ms": None, "message": str(e)}
