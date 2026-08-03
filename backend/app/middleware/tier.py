import logging
from fastapi import Depends, HTTPException, Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, async_session
from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)

TIER_LIMITS: dict[str, dict[str, int]] = {
    "tamagotchi":   {"requests_per_minute": 0, "requests_per_hour": 0, "concurrent_connections": 1, "data_providers": 0},
    "trial":        {"requests_per_minute": 50, "requests_per_hour": 500, "concurrent_connections": 2, "data_providers": 5},
    "starter":      {"requests_per_minute": 500, "requests_per_hour": 10000, "concurrent_connections": 5, "data_providers": 15},
    "pro":          {"requests_per_minute": 3000, "requests_per_hour": 50000, "concurrent_connections": 10, "data_providers": 37},
    "fund":         {"requests_per_minute": 10000, "requests_per_hour": 100000, "concurrent_connections": 20, "data_providers": 37},
    "enterprise":   {"requests_per_minute": 1000000, "requests_per_hour": 10000000, "concurrent_connections": 1000, "data_providers": 37},
    # Admin / superadmin — effectively unlimited
    "admin":        {"requests_per_minute": 10000000, "requests_per_hour": 100000000, "concurrent_connections": 10000, "data_providers": 100},
    # Legacy aliases
    "free":         {"requests_per_minute": 2000, "requests_per_hour": 20000, "concurrent_connections": 2, "data_providers": 5},
    "tiny_catfund": {"requests_per_minute": 10000, "requests_per_hour": 100000, "concurrent_connections": 20, "data_providers": 37},
}


async def get_user_tier(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
) -> str:
    username = current_user.get("sub")
    if not username:
        return "free"

    try:
        user_row = await db.execute(
            text("SELECT id FROM users WHERE username = :username"),
            {"username": username},
        )
        user = user_row.mappings().first()
        if not user:
            return "free"

        sub_row = await db.execute(
            text("SELECT tier FROM subscriptions WHERE user_id = :uid AND status = 'active'"),
            {"uid": user["id"]},
        )
        sub = sub_row.mappings().first()
        if sub:
            return sub["tier"]
    except Exception as e:
        logger.warning("Failed to resolve user tier, defaulting to free: %s", e)

    return "free"


def require_tier(*tiers: str):
    async def tier_checker(
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user),
    ):
        tier = await get_user_tier(db=db, current_user=current_user)  # type: ignore[call-arg]
        if tier not in tiers:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"This feature requires one of: {', '.join(tiers)}. Your tier: {tier}",
            )
        return tier
    return tier_checker


def get_tier_limits(tier: str) -> dict[str, int]:
    return TIER_LIMITS.get(tier, TIER_LIMITS["tamagotchi"])


class TierMiddleware(BaseHTTPMiddleware):
    """Resolves and attaches the user's subscription tier to request.state.

    The tier is stored at ``request.state.tier`` so downstream middleware
    (rate limiting, audit logging) and route handlers can read it without
    re-querying the database.
    """

    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        request.state.tier = "free"
        request.state.user_id = None
        request.state.auth_type = None

        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            token = auth[7:]
            try:
                from app.middleware.api_key_auth import hash_api_key, KEY_PREFIX_LEN

                if token.startswith("miau_"):
                    request.state.auth_type = "api_key"
                    key_hash = hash_api_key(token)
                    prefix = token[:KEY_PREFIX_LEN]
                    async with async_session() as db:
                        try:
                            key_row = await db.execute(
                                text("""
                                    SELECT ak.user_id, u.username
                                    FROM api_keys ak
                                    JOIN users u ON u.id = ak.user_id
                                    WHERE ak.key_hash = :hash AND ak.key_prefix = :prefix AND ak.is_active = TRUE
                                      AND (ak.expires_at IS NULL OR ak.expires_at > NOW())
                                """),
                                {"hash": key_hash, "prefix": prefix},
                            )
                            key_data = key_row.mappings().first()
                            if key_data:
                                request.state.user_id = str(key_data["user_id"])
                                sub_row = await db.execute(
                                    text("SELECT tier FROM subscriptions WHERE user_id = :uid AND status = 'active'"),
                                    {"uid": key_data["user_id"]},
                                )
                                sub = sub_row.mappings().first()
                                if sub:
                                    request.state.tier = sub["tier"]
                        except Exception as e:
                            logger.warning("TierMiddleware: failed to resolve tier for API key: %s", e)
                else:
                    from jose import jwt
                    from app.config import settings
                    if not settings.secret_key:
                        raise RuntimeError("JWT secret_key is not configured — refusing to decode tokens")
                    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
                    username = payload.get("sub")
                    request.state.user_id = payload.get("user_id")
                    request.state.auth_type = "jwt"

                    if username:
                        # 🔒 SECURITY (V7-001/C1): pawdmin superadmin fast path removed.
                        # Tier is resolved from the DB user record only.
                        async with async_session() as db:
                            try:
                                user_row = await db.execute(
                                    text("SELECT id, role FROM users WHERE username = :username"),
                                    {"username": username},
                                )
                                user = user_row.mappings().first()
                                if user:
                                    request.state.user_id = str(user["id"])
                                    # Admin role bypasses subscription check
                                    if user["role"] == "admin":
                                        request.state.tier = "admin"
                                    else:
                                        sub_row = await db.execute(
                                            text("SELECT tier FROM subscriptions WHERE user_id = :uid AND status = 'active'"),
                                            {"uid": user["id"]},
                                        )
                                        sub = sub_row.mappings().first()
                                        if sub:
                                            request.state.tier = sub["tier"]
                            except Exception as e:
                                logger.warning("TierMiddleware: failed to resolve tier: %s", e)
            except Exception:
                pass

        response = await call_next(request)
        response.headers["X-Tier"] = request.state.tier
        return response
