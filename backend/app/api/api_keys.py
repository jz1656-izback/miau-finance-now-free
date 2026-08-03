from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import uuid4
from app.database import get_db
from app.middleware.auth import get_current_user
from app.schemas.api_keys import ApiKeyCreate, ApiKeyResponse, ApiKeyCreatedResponse

router = APIRouter()


@router.post("/api-keys", response_model=ApiKeyCreatedResponse)
async def create_api_key(
    req: ApiKeyCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    user_id = user.get("sub", "")
    raw_key = f"miau_{uuid4().hex}"
    key_prefix = raw_key[:8]
    result = await db.execute(
        text("""
            INSERT INTO api_keys (id, user_id, name, key_hash, key_prefix, scopes, expires_at)
            VALUES (gen_random_uuid(), :uid, :name, :kh, :kp, :scopes,
                    NOW() + CAST(:days AS INTEGER) * INTERVAL '1 day')
            RETURNING id, name, key_prefix, scopes, expires_at, created_at
        """),
        {
            "uid": user_id,
            "name": req.name,
            "kh": raw_key,
            "kp": key_prefix,
            "scopes": req.scopes,
            "days": req.expires_in_days or 365,
        },
    )
    await db.commit()
    row = result.mappings().first()
    return ApiKeyCreatedResponse(
        id=str(row["id"]),
        name=row["name"],
        key=raw_key,
        key_prefix=row["key_prefix"],
        scopes=row["scopes"],
        expires_at=str(row["expires_at"]) if row["expires_at"] else None,
        created_at=str(row["created_at"]) if row["created_at"] else None,
        raw_key=raw_key,
    )


@router.get("/api-keys", response_model=list[ApiKeyResponse])
async def list_api_keys(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    user_id = user.get("sub", "")
    result = await db.execute(
        text("SELECT id, name, key_prefix, scopes, expires_at, created_at FROM api_keys WHERE user_id = :uid ORDER BY created_at DESC"),
        {"uid": user_id},
    )
    return [ApiKeyResponse(
        id=str(r["id"]),
        name=r["name"],
        key="",
        key_prefix=r["key_prefix"],
        scopes=r["scopes"],
        expires_at=str(r["expires_at"]) if r["expires_at"] else None,
        created_at=str(r["created_at"]) if r["created_at"] else None,
    ) for r in result.mappings().all()]


@router.delete("/api-keys/{key_id}")
async def delete_api_key(
    key_id: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    user_id = user.get("sub", "")
    result = await db.execute(
        text("DELETE FROM api_keys WHERE id = :id AND user_id = :uid RETURNING id"),
        {"id": key_id, "uid": user_id},
    )
    await db.commit()
    if not result.rowcount:
        raise HTTPException(404, "API key not found")
    return {"message": "API key deleted"}
