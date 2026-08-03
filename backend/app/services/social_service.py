from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

ACTIVITY_TYPES = {
    "trade_executed": "{user} executed a {details} trade",
    "achievement_unlocked": "{user} unlocked the {details} achievement",
    "ai_insight": "{user} received an AI insight",
    "portfolio_shared": "{user} shared their portfolio",
    "new_follower": "{user} gained a new follower",
    "leaderboard_rank": "{user} reached #{details} on the leaderboard",
}


def format_message(action_type: str, username: str, details: Optional[str] = None) -> str:
    template = ACTIVITY_TYPES.get(action_type, "{user} performed {action}")
    return template.format(user=username, action=action_type, details=details or "")


async def log_activity(
    db: AsyncSession,
    user_id: str,
    action_type: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    details: Optional[dict] = None,
    visibility: str = "public",
) -> dict:
    result = await db.execute(
        text("""
            INSERT INTO social_activities (id, user_id, action_type, resource_type, resource_id, details, visibility)
            VALUES (gen_random_uuid(), :user_id, :action_type, :resource_type, :resource_id, :details, :visibility)
            RETURNING id, user_id, action_type, resource_type, resource_id, details, visibility, created_at
        """),
        {
            "user_id": user_id,
            "action_type": action_type,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "visibility": visibility,
        },
    )
    await db.commit()
    return dict(result.mappings().first())


async def get_activity_feed(
    db: AsyncSession,
    user_id: Optional[str] = None,
    filter_type: str = "global",
    limit: int = 20,
    cursor: Optional[str] = None,
) -> tuple[list[dict], Optional[str]]:
    conditions = []
    params: dict = {"limit": limit + 1}

    if filter_type == "following" and user_id:
        conditions.append("sa.user_id IN (SELECT followed_id FROM follows WHERE follower_id = :uid)")
        params["uid"] = user_id
    elif filter_type == "own" and user_id:
        conditions.append("sa.user_id = :uid")
        params["uid"] = user_id

    if cursor:
        conditions.append("sa.created_at < :cursor")
        params["cursor"] = cursor

    where = " AND ".join(conditions) if conditions else "TRUE"
    query = text(f"""
        SELECT sa.id, sa.user_id, u.username, sa.action_type, sa.resource_type,
               sa.resource_id, sa.details, sa.visibility, sa.created_at,
               (SELECT COUNT(*) FROM comments c WHERE c.activity_id = sa.id) as comment_count
        FROM social_activities sa
        JOIN users u ON u.id = sa.user_id
        WHERE {where}
        ORDER BY sa.created_at DESC
        LIMIT :limit
    """)
    result = await db.execute(query, params)
    rows = [dict(r) for r in result.mappings().all()]
    has_more = len(rows) > limit
    if has_more:
        rows = rows[:limit]
    next_cursor = str(rows[-1]["created_at"]) if rows and has_more else None
    activities = []
    for r in rows:
        activities.append({
            "id": str(r["id"]),
            "user_id": str(r["user_id"]),
            "username": r["username"],
            "action_type": r["action_type"],
            "resource_type": r["resource_type"],
            "resource_id": str(r["resource_id"]) if r["resource_id"] else None,
            "details": r["details"],
            "message": format_message(r["action_type"], r["username"], str(r.get("details", {}))),
            "comment_count": r["comment_count"],
            "created_at": str(r["created_at"]) if r["created_at"] else None,
        })
    return activities, next_cursor
