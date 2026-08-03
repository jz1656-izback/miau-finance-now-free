from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
import secrets

from app.database import get_db
from app.middleware.auth import get_current_user
from app.middleware.rbac import get_current_user_db
from app.schemas.social import ShareCreate, ShareResponse, ActivityCreate, ActivityResponse, CommentCreate, CommentResponse, FollowResponse
from app.services.leaderboard import calculate_leaderboard
from app.services.social_service import log_activity, get_activity_feed, ACTIVITY_TYPES
from app.services.reputation import calculate_reputation, check_badges, POINTS

router = APIRouter(prefix="/social", tags=["Social"])


@router.post("/share")
async def create_share_link(
    req: ShareCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    share_token = secrets.token_urlsafe(32)
    result = await db.execute(
        text("""
            INSERT INTO shared_portfolio_views (id, portfolio_id, share_token, is_public, expires_at)
            VALUES (gen_random_uuid(), :pid, :token, :is_public, :expires)
            RETURNING id, portfolio_id, share_token, is_public, expires_at, created_at
        """),
        {"pid": req.portfolio_id, "token": share_token, "is_public": req.is_public, "expires": req.expires_at},
    )
    await db.commit()
    row = dict(result.mappings().first())
    return ShareResponse(
        id=str(row["id"]),
        portfolio_id=str(row["portfolio_id"]),
        share_token=row["share_token"],
        is_public=row["is_public"],
        share_url=f"/api/v1/public/portfolio/{row['share_token']}",
        expires_at=row["expires_at"],
        created_at=row["created_at"],
    )


@router.get("/leaderboard")
async def get_leaderboard(
    period: str = Query("all_time"),
    metric: str = Query("total_return"),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    results = await calculate_leaderboard(db, metric=metric, period=period, limit=limit)
    return {"period": period, "metric": metric, "leaderboard": results}


@router.post("/activity")
async def create_activity(
    req: ActivityCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await log_activity(
        db=db, user_id=user["id"], action_type=req.action_type,
        resource_type=req.resource_type, resource_id=req.resource_id,
        details=req.details, visibility=req.visibility,
    )
    return {"activity": {**result, "id": str(result["id"]), "user_id": str(result["user_id"])}}


@router.get("/feed")
async def get_feed(
    limit: int = Query(20, ge=1, le=100),
    cursor: str = Query(None),
    filter: str = Query("global", alias="filter"),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    activities, next_cursor = await get_activity_feed(
        db, user_id=user["id"], filter_type=filter, limit=limit, cursor=cursor,
    )
    return {"activities": activities, "next_cursor": next_cursor}


@router.post("/feed/{activity_id}/comment")
async def create_comment(
    activity_id: UUID,
    req: CommentCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            INSERT INTO comments (id, activity_id, user_id, parent_id, text)
            VALUES (gen_random_uuid(), :aid, :uid, :parent, :text)
            RETURNING id, activity_id, user_id, parent_id, text, created_at
        """),
        {"aid": activity_id, "uid": user["id"], "parent": req.parent_id, "text": req.text},
    )
    await db.commit()
    row = dict(result.mappings().first())
    return CommentResponse(
        id=str(row["id"]), activity_id=str(row["activity_id"]),
        user_id=str(row["user_id"]), text=row["text"],
        parent_id=str(row["parent_id"]) if row["parent_id"] else None,
        created_at=str(row["created_at"]) if row["created_at"] else None,
    )


@router.get("/feed/{activity_id}/comments")
async def get_comments(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            SELECT c.id, c.activity_id, c.user_id, u.username, c.text, c.parent_id, c.created_at
            FROM comments c
            JOIN users u ON u.id = c.user_id
            WHERE c.activity_id = :aid
            ORDER BY c.created_at ASC
        """),
        {"aid": activity_id},
    )
    rows = result.mappings().all()
    return {"comments": [
        CommentResponse(
            id=str(r["id"]), activity_id=str(r["activity_id"]),
            user_id=str(r["user_id"]), username=r["username"], text=r["text"],
            parent_id=str(r["parent_id"]) if r["parent_id"] else None,
            created_at=str(r["created_at"]) if r["created_at"] else None,
        ) for r in rows
    ]}


@router.delete("/comment/{comment_id}")
async def delete_comment(
    comment_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("DELETE FROM comments WHERE id = :cid AND user_id = :uid RETURNING id"),
        {"cid": comment_id, "uid": user["id"]},
    )
    await db.commit()
    if not result.rowcount:
        raise HTTPException(404, "Comment not found or not owned by user")
    return {"deleted": str(comment_id)}


@router.post("/follow/{target_user_id}")
async def follow_user(
    target_user_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    if str(user["id"]) == str(target_user_id):
        raise HTTPException(400, "Cannot follow yourself")
    try:
        result = await db.execute(
            text("""
                INSERT INTO follows (id, follower_id, followed_id)
                VALUES (gen_random_uuid(), :follower, :followed)
                ON CONFLICT ON CONSTRAINT uq_follows_pair DO NOTHING
                RETURNING id, follower_id, followed_id, created_at
            """),
            {"follower": user["id"], "followed": target_user_id},
        )
        await db.commit()
        row = result.mappings().first()
        if not row:
            raise HTTPException(409, "Already following this user")
        return FollowResponse(
            follower_id=str(row["follower_id"]), followed_id=str(row["followed_id"]),
            created_at=str(row["created_at"]) if row["created_at"] else None,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, str(e))


@router.delete("/follow/{target_user_id}")
async def unfollow_user(
    target_user_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("DELETE FROM follows WHERE follower_id = :follower AND followed_id = :followed RETURNING id"),
        {"follower": user["id"], "followed": target_user_id},
    )
    await db.commit()
    if not result.rowcount:
        raise HTTPException(404, "Not following this user")
    return {"unfollowed": str(target_user_id)}


@router.post("/feed/{activity_id}/like")
async def like_activity(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    await db.execute(text("""
        INSERT INTO activity_likes (activity_id, user_id) VALUES (:aid, :uid)
        ON CONFLICT ON CONSTRAINT uq_activity_like DO NOTHING
    """), {"aid": activity_id, "uid": user["id"]})
    await db.commit()
    count = await db.execute(text("SELECT COUNT(*) FROM activity_likes WHERE activity_id = :aid"), {"aid": activity_id})
    return {"liked": True, "likes": count.scalar() or 0}


@router.delete("/feed/{activity_id}/like")
async def unlike_activity(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    await db.execute(text("DELETE FROM activity_likes WHERE activity_id = :aid AND user_id = :uid"), {"aid": activity_id, "uid": user["id"]})
    await db.commit()
    count = await db.execute(text("SELECT COUNT(*) FROM activity_likes WHERE activity_id = :aid"), {"aid": activity_id})
    return {"liked": False, "likes": count.scalar() or 0}


@router.get("/users/search")
async def search_users(
    q: str,
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    rows = await db.execute(text("""
        SELECT id, username, created_at FROM users
        WHERE username ILIKE :q OR id::text ILIKE :q
        LIMIT :lim
    """), {"q": f"%{q}%", "lim": limit})
    return [dict(r._mapping) for r in rows]


@router.get("/notifications")
async def get_notifications(
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    rows = await db.execute(text("""
        SELECT id, type, title, body, related_user_id, related_activity_id, read, created_at
        FROM notifications WHERE user_id = :uid
        ORDER BY created_at DESC LIMIT :lim
    """), {"uid": user["id"], "lim": limit})
    return [dict(r._mapping) for r in rows]


@router.post("/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    await db.execute(text("UPDATE notifications SET read = true WHERE id = :nid AND user_id = :uid"), {"nid": notification_id, "uid": user["id"]})
    await db.commit()
    return {"read": True}


@router.get("/reputation")
async def get_reputation(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("SELECT COUNT(*) as trades FROM trades WHERE portfolio_id IN (SELECT id FROM portfolios)")
    )
    count = result.scalar() or 0
    points = count * POINTS.get("trade", 1)
    return calculate_reputation(points)


@router.get("/badges")
async def get_badges(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(text("SELECT COUNT(*) as trades FROM trades"))
    trade_count = result.scalar() or 0
    completed = []
    if trade_count > 0: completed.append("first_trade")
    if trade_count >= 10: completed.append("ai_master")
    return {"badges": check_badges(completed)}


@router.post("/feed/{activity_id}/like")
async def like_activity(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    await db.execute(text("""
        INSERT INTO activity_likes (activity_id, user_id)
        VALUES (:aid, :uid)
        ON CONFLICT DO NOTHING
    """), {"aid": activity_id, "uid": user["id"]})
    await db.commit()
    return {"liked": str(activity_id)}


@router.delete("/feed/{activity_id}/like")
async def unlike_activity(
    activity_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    await db.execute(text("DELETE FROM activity_likes WHERE activity_id = :aid AND user_id = :uid"),
                     {"aid": activity_id, "uid": user["id"]})
    await db.commit()
    return {"unliked": str(activity_id)}


@router.get("/notifications")
async def get_notifications(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    rows = await db.execute(text("""
        SELECT id, type, message, link, is_read, created_at
        FROM notifications WHERE user_id = :uid
        ORDER BY created_at DESC LIMIT 50
    """), {"uid": user["id"]})
    return [dict(r._mapping) for r in rows]


@router.post("/notifications/{notif_id}/read")
async def mark_notification_read(
    notif_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    await db.execute(text("UPDATE notifications SET is_read = true WHERE id = :nid AND user_id = :uid"),
                     {"nid": notif_id, "uid": user["id"]})
    await db.commit()
    return {"read": str(notif_id)}


@router.get("/users/search")
async def search_users(
    q: str = Query("", min_length=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    rows = await db.execute(text("""
        SELECT id, username, role, created_at
        FROM users
        WHERE username ILIKE :q
        ORDER BY username LIMIT :lim
    """), {"q": f"%{q}%", "lim": limit})
    return [dict(r._mapping) for r in rows]
