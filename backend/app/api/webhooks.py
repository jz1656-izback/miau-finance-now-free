import hashlib
import hmac
import secrets
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database import get_db
from app.middleware.auth import get_current_user
from app.middleware.rbac import get_current_user_db

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("")
async def create_webhook(
    url: str,
    events: list[str],
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    secret = secrets.token_hex(16)
    result = await db.execute(
        text("""
            INSERT INTO webhook_endpoints (id, user_id, url, events, secret, is_active)
            VALUES (gen_random_uuid(), :uid, :url, :events, :secret, TRUE)
            RETURNING id, user_id, url, events, is_active, created_at
        """),
        {"uid": user["id"], "url": url, "events": events, "secret": secret},
    )
    await db.commit()
    row = dict(result.mappings().first())
    row["id"] = str(row["id"])
    row["user_id"] = str(row["user_id"])
    row["signing_secret"] = secret
    return row


@router.get("")
async def list_webhooks(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            SELECT id, url, events, is_active, created_at
            FROM webhook_endpoints WHERE user_id = :uid
            ORDER BY created_at DESC
        """),
        {"uid": user["id"]},
    )
    return [dict(row) for row in result.mappings().all()]


@router.delete("/{webhook_id}")
async def delete_webhook(
    webhook_id: str,
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
    return {"deleted": webhook_id}


@router.get("/{webhook_id}/deliveries")
async def webhook_deliveries(
    webhook_id: str,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    return {"webhook_id": webhook_id, "deliveries": [], "note": "Delivery history coming soon"}


@router.post("/{webhook_id}/ping")
async def ping_webhook(
    webhook_id: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    row = await db.execute(
        text("SELECT id, url, secret FROM webhook_endpoints WHERE id = :id AND user_id = :uid"),
        {"id": webhook_id, "uid": user["id"]},
    )
    wh = row.mappings().first()
    if not wh:
        raise HTTPException(404, "Webhook not found")

    payload = b'{"event":"test.ping","timestamp":"' + __import__("datetime").datetime.now(timezone.utc).isoformat().encode() + b'","message":"Miau Finance webhook test"}'
    signature = hmac.new(str(wh["secret"]).encode(), payload, hashlib.sha256).hexdigest()

    try:
        import httpx
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.post(
                str(wh["url"]),
                content=payload,
                headers={
                    "Content-Type": "application/json",
                    "X-Miau-Signature": signature,
                    "X-Miau-Event": "test.ping",
                },
            )
            return {
                "webhook_id": webhook_id,
                "status_code": resp.status_code,
                "signature": signature[:16] + "...",
                "payload_preview": payload[:80].decode() + "...",
            }
    except Exception as e:
        return {
            "webhook_id": webhook_id,
            "error": str(e),
            "signature": signature[:16] + "...",
            "note": "Webhook endpoint unreachable. Verify URL and connectivity.",
        }
