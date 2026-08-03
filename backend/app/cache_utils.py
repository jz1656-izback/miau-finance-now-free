"""
Cache-aside decorator and helpers for data source functions.

Usage:
    from app.cache_utils import cached

    @cached(ttl=60)
    async def get_price(ticker: str):
        # ... fetch from external API
        return result
"""

import functools
import hashlib
import inspect
import logging
from typing import Any, Callable, Optional

logger = logging.getLogger(__name__)


async def _get_cache_safe(key: str) -> Optional[Any]:
    """Safe cache get with lazy import (redis may not be installed locally)."""
    try:
        from app.cache import get_cache as _get
        return await _get(key)
    except Exception:
        logger.debug(f"Cache unavailable, skipping GET for {key}")
        return None


async def _set_cache_safe(key: str, value: dict, ttl: int) -> bool:
    """Safe cache set with lazy import (redis may not be installed locally)."""
    try:
        from app.cache import set_cache as _set
        return await _set(key, value, ttl)
    except Exception:
        logger.debug(f"Cache unavailable, skipping SET for {key}")
        return False


def _make_cache_key(func: Callable, args: tuple, kwargs: dict, prefix: Optional[str] = None) -> str:
    """Build a deterministic cache key from function name + arguments."""
    func_name = prefix or func.__name__

    sig = inspect.signature(func)
    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()

    arg_parts = []
    for name, value in bound.arguments.items():
        if name == "self":
            continue
        if isinstance(value, (int, float, str, bool)):
            arg_parts.append(f"{name}={value}")
        elif value is None:
            arg_parts.append(f"{name}=None")
        else:
            arg_parts.append(f"{name}={hashlib.md5(str(value).encode()).hexdigest()[:8]}")

    key = f"{func_name}:{':'.join(arg_parts)}" if arg_parts else func_name
    if len(key) > 200:
        key = func_name + ":" + hashlib.md5(key.encode()).hexdigest()[:16]

    return key


async def get_cache_age(key: str) -> Optional[int]:
    """Return remaining TTL in seconds for a cached key.

    Uses Redis TTL command. Returns None if key doesn't exist
    or cache is unavailable.
    """
    try:
        from app.cache import get_redis
        r = await get_redis()
        if r is None:
            return None
        ttl = await r.ttl(key)
        return ttl if ttl >= 0 else None
    except Exception:
        logger.debug(f"Cache unavailable, skipping TTL check for {key}")
        return None


async def is_cache_fresh(key: str, max_age_seconds: int = 60) -> bool:
    """Check if a cached entry is fresh.

    An entry is considered fresh if it exists and its remaining TTL
    is at least max_age_seconds. Returns False if key doesn't exist
    or cache is unavailable.

    Args:
        key: Cache key to check.
        max_age_seconds: Minimum remaining TTL for freshness.
    """
    try:
        from app.cache import get_redis
        r = await get_redis()
        if r is None:
            return False
        ttl = await r.ttl(key)
        if ttl < 0:
            return False
        return ttl >= max_age_seconds
    except Exception:
        logger.debug(f"Cache unavailable, skipping freshness check for {key}")
        return False


def cached(
    ttl: int = 300,
    prefix: Optional[str] = None,
    key_builder: Optional[Callable] = None,
) -> Callable:
    """Cache-aside decorator for async data fetching functions.

    Checks Redis cache first. On hit: returns cached value. On miss: calls the
    function, stores result in cache (if truthy and not an error), and returns.

    Args:
        ttl: Cache time-to-live in seconds. Default 300 (5 min).
        prefix: Override for the cache key prefix. Defaults to function name.
        key_builder: Optional custom key builder function.
            Signature: (func, args, kwargs) -> str

    Usage:
        @cached(ttl=60)
        async def get_price(ticker: str):
            ...

        @cached(ttl=3600, prefix="history")
        async def get_history(ticker: str, period: str = "1mo"):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if key_builder:
                key = key_builder(func, args, kwargs)
            else:
                key = _make_cache_key(func, args, kwargs, prefix)

            cached_value = await _get_cache_safe(key)
            if cached_value is not None:
                logger.debug(f"Cache HIT: {key}")
                return cached_value

            logger.debug(f"Cache MISS: {key}")
            result = await func(*args, **kwargs)

            if result is not None:
                if isinstance(result, dict) and result.get("error"):
                    logger.debug(f"Not caching error response for {key}")
                else:
                    await _set_cache_safe(key, result, ttl)
                    logger.debug(f"Cached {key} for {ttl}s")

            return result

        return wrapper

    return decorator
