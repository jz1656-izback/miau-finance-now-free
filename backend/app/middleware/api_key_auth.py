import hashlib
import hmac
import logging
import secrets
from typing import Optional
from fastapi import Request, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session

logger = logging.getLogger(__name__)

KEY_PREFIX_LEN = 8
KEY_TOTAL_LEN = 48


def generate_api_key() -> tuple[str, str, str]:
    """Generate a new API key. Returns (raw_key, prefix, hash)."""
    raw = f"miau_{secrets.token_urlsafe(30)}"
    prefix = raw[:KEY_PREFIX_LEN]
    key_hash = hashlib.sha256(raw.encode()).hexdigest()
    return raw, prefix, key_hash


def hash_api_key(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode()).hexdigest()


async def authenticate_api_key(request: Request) -> Optional[dict]:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer miau_"):
        return None

    raw_key = auth_header.replace("Bearer ", "")
    key_hash = hash_api_key(raw_key)
    prefix = raw_key[:KEY_PREFIX_LEN]

    async with async_session() as db:
        try:
            result = await db.execute(
                text("""
                    SELECT ak.id, ak.user_id, ak.name, ak.scopes, ak.rate_limit_multiplier,
                           u.username, u.role
                    FROM api_keys ak
                    JOIN users u ON u.id = ak.user_id
                    WHERE ak.key_hash = :hash AND ak.key_prefix = :prefix AND ak.is_active = TRUE
                      AND (ak.expires_at IS NULL OR ak.expires_at > NOW())
                """),
                {"hash": key_hash, "prefix": prefix},
            )
            row = result.mappings().first()
            if not row:
                return None

            await db.execute(
                text("UPDATE api_keys SET last_used_at = NOW() WHERE id = :id"),
                {"id": row["id"]},
            )
            await db.commit()

            return {
                "sub": row["username"],
                "role": row["role"],
                "user_id": str(row["user_id"]),
                "api_key_id": str(row["id"]),
                "auth_type": "api_key",
                "scopes": row["scopes"],
            }
        except Exception as e:
            logger.warning(f"API key auth failed: {e}")
            return None
