from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.web_push import send_web_push

router = APIRouter()


async def get_current_user_db(
    db: AsyncSession = Depends(get_db),
    token_user: dict = Depends(get_current_user),
) -> dict:
    username = token_user.get("sub")
    result = await db.execute(
        text("SELECT id, username FROM users WHERE username = :username"),
        {"username": username},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(401, "User not found")
    return dict(row)


@router.post("/push/subscribe")
async def subscribe_push(
    endpoint: str,
    p256dh_key: str = "",
    auth_key: str = "",
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            INSERT INTO push_subscriptions (id, user_id, endpoint, p256dh_key, auth_key)
            VALUES (gen_random_uuid(), :uid, :endpoint, :p256dh, :auth)
            ON CONFLICT (user_id, endpoint) DO UPDATE SET p256dh_key = :p256dh2, auth_key = :auth2
            RETURNING id, user_id, endpoint
        """),
        {"uid": current_user["id"], "endpoint": endpoint, "p256dh": p256dh_key, "auth": auth_key,
         "p256dh2": p256dh_key, "auth2": auth_key},
    )
    await db.commit()
    return {"status": "subscribed", "endpoint": endpoint[:50] + "..."}


@router.delete("/push/unsubscribe")
async def unsubscribe_push(
    endpoint: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    await db.execute(
        text("DELETE FROM push_subscriptions WHERE user_id = :uid AND endpoint = :endpoint"),
        {"uid": current_user["id"], "endpoint": endpoint},
    )
    await db.commit()
    return {"status": "unsubscribed"}


@router.post("/push/send")
async def send_push_notification(
    title: str,
    body: str,
    url: str = "/",
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("SELECT endpoint, p256dh_key, auth_key FROM push_subscriptions WHERE user_id = :uid"),
        {"uid": current_user["id"]},
    )
    subs = result.mappings().all()
    if not subs:
        raise HTTPException(404, "No push subscriptions found")
    results = []
    for sub in subs:
        ok = await send_web_push(dict(sub), title, body, url=url)
        results.append({"endpoint": sub.endpoint[:30] + "...", "sent": ok})
    return {"sent": len([r for r in results if r["sent"]]), "failed": len([r for r in results if not r["sent"]]), "results": results}


@router.post("/push/broadcast")
async def broadcast_push(
    title: str,
    body: str,
    url: str = "/",
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        text("SELECT endpoint, p256dh_key, auth_key FROM push_subscriptions"),
    )
    subs = result.mappings().all()
    sent = 0
    for sub in subs:
        ok = await send_web_push(dict(sub), title, body, url=url)
        if ok:
            sent += 1
    return {"sent": sent, "total": len(subs)}
