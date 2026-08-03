import logging
import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.middleware.auth import get_current_user
from app.middleware.rbac import get_current_user_db
from app.middleware.tier import get_user_tier, require_tier
from app.schemas.api_keys import (
    ApiKeyCreate, ApiKeyResponse, ApiKeyCreatedResponse,
    WebhookEndpointCreate, WebhookEndpointResponse, DeveloperDashboardResponse,
)
from app.middleware.api_key_auth import generate_api_key

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/developer", tags=["Developer"])


@router.get("/dashboard")
async def developer_dashboard(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    uid = user["id"]
    tier = await get_user_tier(db=db, current_user={"sub": user["username"]})

    keys_result = await db.execute(
        text("SELECT id, name, key_prefix, scopes, last_used_at, expires_at, is_active, created_at FROM api_keys WHERE user_id = :uid ORDER BY created_at DESC"),
        {"uid": uid},
    )
    api_keys = [dict(r) for r in keys_result.mappings().all()]

    webhooks_result = await db.execute(
        text("SELECT id, url, events, is_active, created_at FROM webhook_endpoints WHERE user_id = :uid ORDER BY created_at DESC"),
        {"uid": uid},
    )
    webhooks = [dict(r) for r in webhooks_result.mappings().all()]

    today_result = await db.execute(
        text("SELECT COUNT(*) FROM api_usage_log WHERE user_id = :uid AND logged_at >= NOW() - INTERVAL '1 day'"),
        {"uid": uid},
    )
    today_count = today_result.scalar() or 0

    month_result = await db.execute(
        text("SELECT COUNT(*) FROM api_usage_log WHERE user_id = :uid AND logged_at >= NOW() - INTERVAL '30 days'"),
        {"uid": uid},
    )
    month_count = month_result.scalar() or 0

    return DeveloperDashboardResponse(
        tier=tier,
        tier_key_limit=TIER_KEY_LIMITS.get(tier, 0),
        tier_webhook_limit=TIER_WEBHOOK_LIMITS.get(tier, 0),
        total_api_keys=len(api_keys),
        active_webhooks=len(webhooks),
        requests_today=today_count,
        requests_this_month=month_count,
        api_keys=[ApiKeyResponse(
            id=str(k["id"]), name=k["name"], key_prefix=k["key_prefix"],
            scopes=k["scopes"] or {}, last_used_at=k["last_used_at"],
            expires_at=k["expires_at"], is_active=k["is_active"],
            created_at=k["created_at"],
        ) for k in api_keys],
        webhooks=[WebhookEndpointResponse(
            id=str(w["id"]), url=w["url"], events=w["events"] or [],
            is_active=w["is_active"], created_at=w["created_at"],
        ) for w in webhooks],
    )


TIER_KEY_LIMITS: dict[str, int] = {
    "free": 2,
    "pro": 10,
    "enterprise": 999999,
}


@router.post("/api-keys", response_model=ApiKeyCreatedResponse)
async def create_api_key(
    req: ApiKeyCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    tier = await get_user_tier(db=db, current_user={"sub": user["username"]})
    key_limit = TIER_KEY_LIMITS.get(tier, 0)

    count_result = await db.execute(
        text("SELECT COUNT(*) FROM api_keys WHERE user_id = :uid AND is_active = TRUE"),
        {"uid": user["id"]},
    )
    existing_count = count_result.scalar() or 0

    if existing_count >= key_limit:
        raise HTTPException(
            status_code=402,
            detail=f"API key limit reached ({key_limit}) for tier '{tier}'. Upgrade to create more keys.",
        )

    raw, prefix, key_hash = generate_api_key()
    scopes = req.scopes or {"read": True}

    result = await db.execute(
        text("""
            INSERT INTO api_keys (id, user_id, name, key_prefix, key_hash, scopes)
            VALUES (gen_random_uuid(), :uid, :name, :prefix, :hash, :scopes)
            RETURNING id, name, key_prefix, scopes, last_used_at, expires_at, is_active, created_at
        """),
        {"uid": user["id"], "name": req.name, "prefix": prefix, "hash": key_hash, "scopes": scopes},
    )
    await db.commit()
    row = dict(result.mappings().first())

    logger.info(f"API key created for user {user['id']} ({tier}): {req.name}")
    return ApiKeyCreatedResponse(
        id=str(row["id"]), name=row["name"], key_prefix=row["key_prefix"],
        scopes=row["scopes"] or {}, raw_key=raw,
        last_used_at=row["last_used_at"], expires_at=row["expires_at"],
        is_active=row["is_active"], created_at=row["created_at"],
    )


@router.get("/api-keys")
async def list_api_keys(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("SELECT id, name, key_prefix, scopes, last_used_at, expires_at, is_active, created_at FROM api_keys WHERE user_id = :uid ORDER BY created_at DESC"),
        {"uid": user["id"]},
    )
    return {"api_keys": [dict(r) for r in result.mappings().all()]}


@router.delete("/api-keys/{key_id}")
async def revoke_api_key(
    key_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("UPDATE api_keys SET is_active = FALSE WHERE id = :id AND user_id = :uid RETURNING id"),
        {"id": key_id, "uid": user["id"]},
    )
    await db.commit()
    if not result.rowcount:
        raise HTTPException(404, "API key not found")
    return {"revoked": str(key_id)}


TIER_WEBHOOK_LIMITS: dict[str, int] = {
    "free": 1,
    "pro": 5,
    "enterprise": 100,
}


@router.post("/webhooks")
async def create_webhook(
    req: WebhookEndpointCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    tier = await get_user_tier(db=db, current_user={"sub": user["username"]})
    wh_limit = TIER_WEBHOOK_LIMITS.get(tier, 0)

    count_result = await db.execute(
        text("SELECT COUNT(*) FROM webhook_endpoints WHERE user_id = :uid AND is_active = TRUE"),
        {"uid": user["id"]},
    )
    existing_count = count_result.scalar() or 0

    if existing_count >= wh_limit:
        raise HTTPException(
            status_code=402,
            detail=f"Webhook limit reached ({wh_limit}) for tier '{tier}'. Upgrade to create more.",
        )

    secret = secrets.token_hex(32)
    result = await db.execute(
        text("""
            INSERT INTO webhook_endpoints (id, user_id, url, events, secret)
            VALUES (gen_random_uuid(), :uid, :url, :events, :secret)
            RETURNING id, url, events, is_active, created_at
        """),
        {"uid": user["id"], "url": req.url, "events": req.events, "secret": secret},
    )
    await db.commit()
    row = dict(result.mappings().first())
    return {**row, "id": str(row["id"]), "secret": secret}


@router.get("/webhooks")
async def list_webhooks(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("SELECT id, url, events, is_active, created_at FROM webhook_endpoints WHERE user_id = :uid ORDER BY created_at DESC"),
        {"uid": user["id"]},
    )
    return {"webhooks": [dict(r) for r in result.mappings().all()]}


@router.delete("/webhooks/{webhook_id}")
async def delete_webhook(
    webhook_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("DELETE FROM webhook_endpoints WHERE id = :id AND user_id = :uid RETURNING id"),
        {"id": webhook_id, "uid": user["id"]},
    )
    await db.commit()
    if not result.rowcount:
        raise HTTPException(404, "Webhook not found")
    return {"deleted": str(webhook_id)}
