from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional


async def log_activity(
    db: AsyncSession,
    user_id: str,
    action: str,
    resource_type: str,
    resource_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    details: Optional[dict] = None,
) -> dict:
    result = await db.execute(
        text("""
            INSERT INTO activity_logs (id, user_id, workspace_id, action, resource_type, resource_id, details)
            VALUES (gen_random_uuid(), :user_id, :workspace_id, :action, :resource_type, :resource_id, :details)
            RETURNING id, user_id, workspace_id, action, resource_type, resource_id, details, created_at
        """),
        {
            "user_id": user_id,
            "workspace_id": workspace_id,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
        },
    )
    await db.commit()
    return dict(result.mappings().first())


async def get_activity(
    db: AsyncSession,
    user_id: Optional[str] = None,
    workspace_id: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> list:
    conditions = []
    params: dict = {"limit": limit, "offset": offset}

    if user_id:
        conditions.append("al.user_id = :user_id")
        params["user_id"] = user_id
    if workspace_id:
        conditions.append("al.workspace_id = :workspace_id")
        params["workspace_id"] = workspace_id

    where_clause = " AND ".join(conditions) if conditions else "TRUE"

    result = await db.execute(
        text(f"""
            SELECT al.*, u.username
            FROM activity_logs al
            JOIN users u ON u.id = al.user_id
            WHERE {where_clause}
            ORDER BY al.created_at DESC
            LIMIT :limit OFFSET :offset
        """),
        params,
    )
    return [dict(row) for row in result.mappings().all()]
