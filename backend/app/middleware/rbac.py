import logging
from fastapi import Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID

from app.database import get_db
from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)


async def get_current_user_db(
    db: AsyncSession = Depends(get_db),
    token_user: dict = Depends(get_current_user),
) -> dict:
    """Fetch full user record (including role) from DB using JWT sub claim."""
    username = token_user.get("sub")
    if not username:
        raise HTTPException(401, "Invalid token: missing subject")
    result = await db.execute(
        text("SELECT id, username, email, role FROM users WHERE username = :username"),
        {"username": username},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(401, "User not found")
    return dict(row)


def require_role(*roles: str):
    """Dependency factory: require the current user to have one of the given roles.

    Usage:
        @router.get("/admin-only")
        async def admin_endpoint(
            user: dict = Depends(get_current_user_db),
            _=Depends(require_role("admin")),
        ):
            ...
    """
    async def _require_role(user: dict = Depends(get_current_user_db)) -> None:
        if user.get("role") not in roles:
            logger.warning("Access denied for user %s (role=%s) — requires one of %s", user.get("username", "unknown"), user.get("role"), roles)
            raise HTTPException(
                status_code=403,
                detail=f"Requires one of roles: {', '.join(roles)}",
            )
    return _require_role


async def require_workspace_access(
    workspace_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
) -> None:
    """Verify the current user is a member of the given workspace.

    Usage:
        @router.get("/workspace/{workspace_id}")
        async def workspace_endpoint(
            workspace_id: UUID,
            db: AsyncSession = Depends(get_db),
            _: None = Depends(lambda w=workspace_id: require_workspace_access(w)),
        ):
            ...
    """
    result = await db.execute(
        text("""
            SELECT 1 FROM workspace_members
            WHERE workspace_id = :workspace_id AND user_id = :user_id
        """),
        {"workspace_id": workspace_id, "user_id": user["id"]},
    )
    if not result.scalar():
        logger.warning("Workspace access denied: user %s not in workspace %s", user.get("id"), workspace_id)
        raise HTTPException(
            status_code=403,
            detail="Not a member of this workspace",
        )
