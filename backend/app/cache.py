import json
import logging
from typing import Optional

import redis.asyncio as aioredis

from app.config import settings
from app.metrics import redis_hits_total, redis_misses_total

logger = logging.getLogger(__name__)

_redis: Optional[aioredis.Redis] = None


async def get_redis() -> aioredis.Redis:
    global _redis
    if _redis is None:
        try:
            _redis = aioredis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=2,
                socket_timeout=2,
                max_connections=10,
                socket_keepalive=True,
                retry_on_timeout=True,
                health_check_interval=30,
            )
            await _redis.ping()
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}")
            return None
    return _redis


def _key_prefix(key: str) -> str:
    """Extract a prefix for metric labels, e.g. 'market:' from 'market:AAPL'."""
    if ":" in key:
        return key.split(":", 1)[0]
    return "default"


async def get_cache(key: str) -> Optional[dict]:
    try:
        r = await get_redis()
        if r is None:
            redis_misses_total.labels(key_prefix=_key_prefix(key)).inc()
            return None
        val = await r.get(key)
        if val is None:
            redis_misses_total.labels(key_prefix=_key_prefix(key)).inc()
            return None
        redis_hits_total.labels(key_prefix=_key_prefix(key)).inc()
        return json.loads(val)
    except Exception as e:
        logger.warning(f"Redis get_cache error: {e}")
        redis_misses_total.labels(key_prefix=_key_prefix(key)).inc()
        return None


async def set_cache(key: str, value: dict, ttl: int = 300) -> bool:
    try:
        r = await get_redis()
        if r is None:
            return False
        await r.setex(key, ttl, json.dumps(value))
        return True
    except Exception as e:
        logger.warning(f"Redis set_cache error: {e}")
        return False


async def delete_cache(key: str) -> bool:
    try:
        r = await get_redis()
        if r is None:
            return False
        await r.delete(key)
        return True
    except Exception as e:
        logger.warning(f"Redis delete_cache error: {e}")
        return False


async def clear_cache(pattern: str) -> bool:
    try:
        r = await get_redis()
        if r is None:
            return False
        cursor = 0
        while True:
            cursor, keys = await r.scan(cursor=cursor, match=pattern, count=100)
            if keys:
                await r.delete(*keys)
            if cursor == 0:
                break
        return True
    except Exception as e:
        logger.warning(f"Redis clear_cache error: {e}")
        return False
