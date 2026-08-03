"""Unified caching layer for data source responses with TTL tiers."""
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Optional

logger = logging.getLogger(__name__)

TTL_TIERS = {
    "realtime": 10,
    "fast": 60,
    "normal": 300,
    "slow": 3600,
    "daily": 86400,
}


class DataCache:
    """Unified cache for data source responses.

    Wraps Redis cache with in-memory fallback. Provides data-source-aware
    key namespacing and hit/miss tracking.
    """

    def __init__(self, redis_client: Any = None):
        self._redis = redis_client
        self._memory: dict[str, tuple[Any, float]] = {}
        self.hits = 0
        self.misses = 0

    def _key(self, provider: str, *parts: str) -> str:
        raw = f"ds:{provider}:" + ":".join(parts)
        if len(raw) > 200:
            raw = f"ds:{provider}:" + hashlib.md5(raw.encode()).hexdigest()[:16]
        return raw

    def get(self, provider: str, *parts: str) -> Optional[Any]:
        key = self._key(provider, *parts)
        if self._redis:
            try:
                data = self._redis.get(key)
                if data:
                    self.hits += 1
                    return json.loads(data)
            except Exception:
                logger.debug(f"Redis unavailable for GET {key}")
        entry = self._memory.get(key)
        if entry and entry[1] > datetime.now().timestamp():
            self.hits += 1
            return entry[0]
        self.misses += 1
        return None

    def set(self, provider: str, *parts: str, value: Any, ttl: int = 300) -> bool:
        key = self._key(provider, *parts)
        expiry = datetime.now().timestamp() + ttl
        if self._redis:
            try:
                self._redis.setex(key, ttl, json.dumps(value, default=str))
                return True
            except Exception:
                logger.debug(f"Redis unavailable for SET {key}")
        self._memory[key] = (value, expiry)
        return True

    def delete(self, provider: str, *parts: str) -> bool:
        key = self._key(provider, *parts)
        self._memory.pop(key, None)
        if self._redis:
            try:
                self._redis.delete(key)
            except Exception:
                pass
        return True

    def stats(self) -> dict:
        total = self.hits + self.misses
        hit_rate = round(self.hits / total * 100, 1) if total > 0 else 0
        return {
            "memory_entries": len(self._memory),
            "hit_rate_pct": hit_rate,
            "hits": self.hits,
            "misses": self.misses,
            "tiers": TTL_TIERS,
        }


# Module-level singleton
data_cache = DataCache()
