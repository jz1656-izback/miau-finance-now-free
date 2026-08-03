import logging
import time
import asyncio
from collections import defaultdict
from typing import Optional
from fastapi import Depends, HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from app.config import settings
from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)

try:
    import redis.asyncio as aioredis

    _redis_available = True
except ImportError:
    _redis_available = False


# Share Redis connection pool from cache module
_shared_redis: Optional[aioredis.Redis] = None


async def _get_shared_redis() -> Optional[aioredis.Redis]:
    global _shared_redis
    if _shared_redis is None:
        try:
            _shared_redis = aioredis.from_url(
                settings.redis_url,
                socket_connect_timeout=2,
                socket_timeout=2,
                decode_responses=True,
                max_connections=10,
                socket_keepalive=True,
                retry_on_timeout=True,
                health_check_interval=30,
            )
            await _shared_redis.ping()
        except Exception as e:
            logger.warning("Shared Redis connection failed: %s", e)
            _shared_redis = None
    return _shared_redis


class _InMemoryRateLimiter:
    def __init__(self):
        self._minute_buckets: dict[str, list[float]] = defaultdict(list)
        self._hour_buckets: dict[str, list[float]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def is_allowed(self, key: str) -> tuple[bool, int, int]:
        now = time.time()
        minute_ago = now - 60
        hour_ago = now - 3600

        async with self._lock:
            minute_times = self._minute_buckets.get(key, [])
            hour_times = self._hour_buckets.get(key, [])

            minute_times = [t for t in minute_times if t > minute_ago]
            hour_times = [t for t in hour_times if t > hour_ago]

            minute_count = len(minute_times)
            hour_count = len(hour_times)

            allowed = (
                minute_count < settings.rate_limit_per_minute
                and hour_count < settings.rate_limit_per_hour
            )

            if allowed:
                minute_times.append(now)
                hour_times.append(now)
                self._minute_buckets[key] = minute_times
                self._hour_buckets[key] = hour_times

            reset_time = int(now) + 60

        return allowed, reset_time, max(0, settings.rate_limit_per_minute - minute_count - 1)


class RedisRateLimiter:
    def __init__(self):
        self._connected = False

    async def _ensure_connected(self):
        if not _redis_available:
            return
        if not self._connected:
            r = await _get_shared_redis()
            self._connected = r is not None

    async def is_allowed(self, key: str) -> tuple[bool, int, int]:
        await self._ensure_connected()
        if not self._connected:
            raise ConnectionError("Redis unavailable — rate limiter requires Redis")
        r = _shared_redis  # use the global shared connection

        now = int(time.time())
        minute_window = now // 60
        hour_window = now // 3600

        minute_key = f"rl:m:{minute_window}:{key}"
        hour_key = f"rl:h:{hour_window}:{key}"

        try:
            pipe = r.pipeline()
            pipe.incr(minute_key)
            pipe.expire(minute_key, 120)
            pipe.incr(hour_key)
            pipe.expire(hour_key, 3700)
            results = await pipe.execute()
            minute_count = results[0]
            hour_count = results[2]

            allowed = (
                minute_count <= settings.rate_limit_per_minute
                and hour_count <= settings.rate_limit_per_hour
            )

            reset_time = (minute_window + 1) * 60
            remaining = max(0, settings.rate_limit_per_minute - minute_count)

            return allowed, reset_time, remaining
        except Exception as e:
            logger.warning("Redis rate limit error, allowing request: %s", e)
            return True, 0, 0


class AIRateLimiter:
    def __init__(self):
        self._buckets: dict[str, list[float]] = defaultdict(list)
        self._lock = asyncio.Lock()
        self._ai_limit = 10

    async def is_allowed(self, key: str) -> tuple[bool, int]:
        now = time.time()
        window_ago = now - 60
        async with self._lock:
            times = [t for t in self._buckets.get(key, []) if t > window_ago]
            allowed = len(times) < self._ai_limit
            if allowed:
                times.append(now)
                self._buckets[key] = times
            reset_time = int(now) + 60
        return allowed, reset_time


class TierRateLimiter:
    def __init__(self):
        self._buckets: dict[str, list[float]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def is_allowed(self, key: str, limit_per_minute: int) -> tuple[bool, int]:
        now = time.time()
        window_ago = now - 60
        async with self._lock:
            times = [t for t in self._buckets.get(key, []) if t > window_ago]
            allowed = len(times) < limit_per_minute
            if allowed:
                times.append(now)
                self._buckets[key] = times
            reset_time = int(now) + 60
        return allowed, reset_time


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self._redis_limiter = RedisRateLimiter()
        self._memory_limiter = _InMemoryRateLimiter()
        self._ai_limiter = AIRateLimiter()
        self._tier_limiter = TierRateLimiter()

    async def _get_client_key(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        client_host = request.client.host if request.client else "unknown"
        return client_host

    async def _get_user_key(self, request: Request) -> str:
        uid = getattr(request.state, 'user_id', None)
        if uid:
            return f"user:{uid}"
        auth = request.headers.get("Authorization", "")
        if auth.startswith("Bearer "):
            try:
                from jose import jwt
                token = auth[7:]
                payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
                uid = payload.get("user_id") or payload.get("sub", "anonymous")
                return f"user:{uid}"
            except Exception:
                pass
        return await self._get_client_key(request)

    def _is_ai_endpoint(self, request: Request) -> bool:
        return request.url.path.startswith("/api/v1/ai/")

    def _should_skip(self, request: Request) -> bool:
        path = request.url.path
        return path == "/metrics"

    async def dispatch(self, request: Request, call_next):
        if self._should_skip(request):
            return await call_next(request)

        client_key = await self._get_client_key(request)

        if self._is_ai_endpoint(request):
            user_key = await self._get_user_key(request)
            ai_allowed, ai_reset = await self._ai_limiter.is_allowed(user_key)
            if not ai_allowed:
                retry_after = max(1, ai_reset - int(time.time()))
                return Response(
                    status_code=429,
                    content=f'{{"detail":"AI rate limit exceeded (10/min)","retry_after":{retry_after}}}',
                    media_type="application/json",
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(ai_reset),
                    },
                )

        tier = getattr(request.state, 'tier', 'free')
        from app.middleware.tier import get_tier_limits
        tier_cfg = get_tier_limits(tier)
        if tier_cfg.get("requests_per_minute", 0) < 10000:
            user_key = await self._get_user_key(request)
            tier_allowed, tier_reset = await self._tier_limiter.is_allowed(
                user_key, tier_cfg.get("requests_per_minute", settings.rate_limit_per_minute)
            )
            if not tier_allowed:
                retry_after = max(1, tier_reset - int(time.time()))
                return Response(
                    status_code=429,
                    content=f'{{"detail":"Tier rate limit exceeded ({tier}: {tier_cfg["requests_per_minute"]}/min). Upgrade for more."}}',
                    media_type="application/json",
                    headers={
                        "Retry-After": str(retry_after),
                        "X-RateLimit-Limit": str(tier_cfg["requests_per_minute"]),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(tier_reset),
                        "X-Tier": tier,
                    },
                )

        try:
            allowed, reset_time, remaining = await self._redis_limiter.is_allowed(client_key)
            if not self._redis_limiter._connected or _shared_redis is None:
                allowed, reset_time, remaining = await self._memory_limiter.is_allowed(client_key)
        except Exception as e:
            logger.warning("Rate limit check failed, allowing request from %s: %s", client_key, e)
            allowed, reset_time, remaining = await self._memory_limiter.is_allowed(client_key)

        if not allowed:
            retry_after = max(1, reset_time - int(time.time()))
            return Response(
                status_code=429,
                content='{"detail":"Too Many Requests","retry_after":' + str(retry_after) + '}',
                media_type="application/json",
                headers={
                    "Retry-After": str(retry_after),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_time),
                },
            )

        response: Response = await call_next(request)

        response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
        response.headers["X-RateLimit-Reset"] = str(reset_time)

        return response


_ai_buckets: dict[str, list[float]] = defaultdict(list)
_ai_lock = asyncio.Lock()
AI_RATE_LIMIT = 10  # requests per minute per user


async def ai_rate_limit(user: dict = Depends(get_current_user)) -> None:
    """AI-specific rate limiter: 10 requests/minute per user.

    Tracks requests by user ID (from JWT token). Returns 429 with
    Retry-After header if exceeded.

    Usage:
        @router.post("/advisor/portfolio")
        async def advisor_portfolio(
            req: PortfolioRequest,
            user=Depends(get_current_user),
            _=Depends(ai_rate_limit),
        ):
            ...
    """
    user_id = user.get("sub", "anonymous")
    now = time.time()
    window_ago = now - 60

    async with _ai_lock:
        timestamps = _ai_buckets.get(user_id, [])
        timestamps = [t for t in timestamps if t > window_ago]

        if len(timestamps) >= AI_RATE_LIMIT:
            retry_after = int(timestamps[0] + 60 - now) + 1
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "AI rate limit exceeded",
                    "retry_after": retry_after,
                    "limit": AI_RATE_LIMIT,
                    "window": "1m",
                },
                headers={"Retry-After": str(retry_after)},
            )

        timestamps.append(now)
        _ai_buckets[user_id] = timestamps
