import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)

ALL_PLUGIN_SCOPES: dict[str, str] = {
    "market:read": "Read market data and prices",
    "market:write": "Submit market data requests",
    "portfolio:read": "View portfolio holdings and performance",
    "portfolio:write": "Modify portfolio positions",
    "orders:create": "Place trading orders",
    "orders:read": "View order history and status",
    "orders:cancel": "Cancel pending orders",
    "analytics:read": "View analytics and risk metrics",
    "analytics:write": "Run custom analytics computations",
    "alerts:read": "View alert configurations",
    "alerts:write": "Create and modify alerts",
    "watchlist:read": "View watchlists",
    "watchlist:write": "Modify watchlists",
    "account:read": "View account settings and profile",
    "webhooks:read": "View webhook configurations",
    "webhooks:write": "Create and modify webhooks",
}

DEFAULT_PLUGIN_SCOPES = ["market:read", "portfolio:read", "analytics:read"]


@dataclass
class PluginPermission:
    plugin_id: str
    user_id: str
    scopes: list[str] = field(default_factory=list)
    approved_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_revoked: bool = False
    id: str = ""


def validate_scopes(scopes: list[str]) -> tuple[bool, list[str]]:
    invalid = [s for s in scopes if s not in ALL_PLUGIN_SCOPES]
    if invalid:
        return False, invalid
    return True, []


async def approve_plugin_permissions(
    db: AsyncSession,
    plugin_id: str,
    user_id: str,
    scopes: list[str],
    expires_in_days: Optional[int] = None,
) -> dict:
    valid, invalid = validate_scopes(scopes)
    if not valid:
        raise HTTPException(400, f"Invalid scopes: {', '.join(invalid)}. Valid: {', '.join(ALL_PLUGIN_SCOPES)}")

    result = await db.execute(
        text("""
            INSERT INTO plugin_permissions (id, plugin_id, user_id, scopes, approved_at, expires_at)
            VALUES (gen_random_uuid(), :plugin_id, :user_id, :scopes, NOW(), :expires_at)
            ON CONFLICT (plugin_id, user_id) DO UPDATE SET
                scopes = :scopes2, approved_at = NOW(), is_revoked = FALSE,
                expires_at = :expires_at2
            RETURNING id, plugin_id, user_id, scopes, approved_at, expires_at, is_revoked
        """),
        {
            "plugin_id": plugin_id,
            "user_id": user_id,
            "scopes": scopes,
            "scopes2": scopes,
            "expires_at": (
                datetime.now(timezone.utc) + timedelta(days=expires_in_days)
                if expires_in_days else None
            ),
            "expires_at2": (
                datetime.now(timezone.utc) + timedelta(days=expires_in_days)
                if expires_in_days else None
            ),
        },
    )
    await db.commit()
    row = dict(result.mappings().first())
    logger.info("Plugin %s approved for user %s with scopes: %s", plugin_id, user_id, scopes)
    return row


async def revoke_plugin_permissions(db: AsyncSession, plugin_id: str, user_id: str) -> bool:
    result = await db.execute(
        text("""
            UPDATE plugin_permissions
            SET is_revoked = TRUE, expires_at = NOW()
            WHERE plugin_id = :plugin_id AND user_id = :user_id
            RETURNING id
        """),
        {"plugin_id": plugin_id, "user_id": user_id},
    )
    await db.commit()
    revoked = result.rowcount > 0
    if revoked:
        logger.info("Plugin %s permissions revoked for user %s", plugin_id, user_id)
    return revoked


async def get_plugin_permissions(db: AsyncSession, plugin_id: str, user_id: str) -> Optional[dict]:
    result = await db.execute(
        text("""
            SELECT id, plugin_id, user_id, scopes, approved_at, expires_at, is_revoked
            FROM plugin_permissions
            WHERE plugin_id = :plugin_id AND user_id = :user_id
        """),
        {"plugin_id": plugin_id, "user_id": user_id},
    )
    row = result.mappings().first()
    if not row:
        return None
    perm = dict(row)
    if perm["is_revoked"]:
        return None
    if perm["expires_at"] and perm["expires_at"] < datetime.now(timezone.utc):
        return None
    return perm


async def check_plugin_permission(
    db: AsyncSession,
    plugin_id: str,
    user_id: str,
    required_scope: str,
) -> bool:
    perm = await get_plugin_permissions(db, plugin_id, user_id)
    if not perm:
        return False
    return required_scope in perm.get("scopes", [])


async def list_approved_plugins(db: AsyncSession, user_id: str) -> list[dict]:
    result = await db.execute(
        text("""
            SELECT id, plugin_id, scopes, approved_at, expires_at
            FROM plugin_permissions
            WHERE user_id = :user_id AND is_revoked = FALSE
              AND (expires_at IS NULL OR expires_at > NOW())
            ORDER BY approved_at DESC
        """),
        {"user_id": user_id},
    )
    return [dict(r) for r in result.mappings().all()]


async def list_plugin_users(db: AsyncSession, plugin_id: str) -> list[dict]:
    result = await db.execute(
        text("""
            SELECT id, user_id, scopes, approved_at, expires_at
            FROM plugin_permissions
            WHERE plugin_id = :plugin_id AND is_revoked = FALSE
              AND (expires_at IS NULL OR expires_at > NOW())
        """),
        {"plugin_id": plugin_id},
    )
    return [dict(r) for r in result.mappings().all()]


class PluginPermissionMiddleware:
    async def check_request(
        self,
        request: Request,
        required_scope: str,
        db: AsyncSession,
        current_user: dict,
    ) -> None:
        plugin_id = request.headers.get("X-Plugin-ID", "")
        if not plugin_id:
            return
        user_id = current_user.get("user_id") or current_user.get("sub", "")
        if not user_id:
            raise HTTPException(401, "Not authenticated")
        has_perm = await check_plugin_permission(db, plugin_id, user_id, required_scope)
        if not has_perm:
            raise HTTPException(
                403,
                f"Plugin {plugin_id} lacks required scope '{required_scope}'. "
                f"Approved scopes: {ALL_PLUGIN_SCOPES}. "
                "Use POST /api/v1/plugins/{id}/approve to grant permissions.",
            )


plugin_permission_middleware = PluginPermissionMiddleware()
