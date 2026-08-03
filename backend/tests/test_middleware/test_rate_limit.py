import pytest
import time
from unittest.mock import AsyncMock, MagicMock, patch

from app.config import settings


class TestInMemoryRateLimiter:
    @pytest.mark.anyio
    async def test_allows_request_within_limit(self):
        from app.middleware.rate_limit import _InMemoryRateLimiter

        limiter = _InMemoryRateLimiter()
        allowed, reset, remaining = await limiter.is_allowed("test_key")
        assert allowed is True
        assert reset > int(time.time())
        assert remaining >= 0

    @pytest.mark.anyio
    async def test_exhausts_minute_limit(self):
        from app.middleware.rate_limit import _InMemoryRateLimiter

        original = settings.rate_limit_per_minute
        settings.rate_limit_per_minute = 3
        try:
            limiter = _InMemoryRateLimiter()
            for _ in range(3):
                allowed, _, _ = await limiter.is_allowed("burst_key")
                assert allowed is True
            allowed, _, _ = await limiter.is_allowed("burst_key")
            assert allowed is False
        finally:
            settings.rate_limit_per_minute = original

    @pytest.mark.anyio
    async def test_exhausts_hour_limit(self):
        from app.middleware.rate_limit import _InMemoryRateLimiter

        original_hour = settings.rate_limit_per_hour
        original_minute = settings.rate_limit_per_minute
        settings.rate_limit_per_hour = 2
        settings.rate_limit_per_minute = 1000
        try:
            limiter = _InMemoryRateLimiter()
            for _ in range(2):
                allowed, _, _ = await limiter.is_allowed("hour_burst")
                assert allowed is True
            allowed, _, _ = await limiter.is_allowed("hour_burst")
            assert allowed is False
        finally:
            settings.rate_limit_per_hour = original_hour
            settings.rate_limit_per_minute = original_minute

    @pytest.mark.anyio
    async def test_resets_after_window(self):
        from app.middleware.rate_limit import _InMemoryRateLimiter

        original = settings.rate_limit_per_minute
        settings.rate_limit_per_minute = 1
        try:
            limiter = _InMemoryRateLimiter()
            allowed, _, _ = await limiter.is_allowed("reset_key")
            assert allowed is True
            allowed, _, _ = await limiter.is_allowed("reset_key")
            assert allowed is False

            old_times = limiter._minute_buckets["reset_key"]
            limiter._minute_buckets["reset_key"] = [t - 120 for t in old_times]
            allowed, _, _ = await limiter.is_allowed("reset_key")
            assert allowed is True
        finally:
            settings.rate_limit_per_minute = original

    @pytest.mark.anyio
    async def test_different_keys_independent(self):
        from app.middleware.rate_limit import _InMemoryRateLimiter

        original = settings.rate_limit_per_minute
        settings.rate_limit_per_minute = 2
        try:
            limiter = _InMemoryRateLimiter()
            assert (await limiter.is_allowed("key_a"))[0] is True
            assert (await limiter.is_allowed("key_a"))[0] is True
            assert (await limiter.is_allowed("key_a"))[0] is False
            assert (await limiter.is_allowed("key_b"))[0] is True
        finally:
            settings.rate_limit_per_minute = original


class TestAIRateLimiter:
    @pytest.mark.anyio
    async def test_allows_up_to_limit(self):
        from app.middleware.rate_limit import AIRateLimiter

        limiter = AIRateLimiter()
        for _ in range(10):
            allowed, _ = await limiter.is_allowed("ai_user")
            assert allowed is True
        allowed, _ = await limiter.is_allowed("ai_user")
        assert allowed is False

    @pytest.mark.anyio
    async def test_resets_after_minute(self):
        from app.middleware.rate_limit import AIRateLimiter

        limiter = AIRateLimiter()
        for _ in range(10):
            await limiter.is_allowed("ai_user2")
        old = limiter._buckets["ai_user2"]
        limiter._buckets["ai_user2"] = [t - 120 for t in old]
        allowed, _ = await limiter.is_allowed("ai_user2")
        assert allowed is True


class TestTierRateLimiter:
    @pytest.mark.anyio
    async def test_allows_up_to_custom_limit(self):
        from app.middleware.rate_limit import TierRateLimiter

        limiter = TierRateLimiter()
        for _ in range(5):
            allowed, _ = await limiter.is_allowed("tier_user", 5)
            assert allowed is True
        allowed, _ = await limiter.is_allowed("tier_user", 5)
        assert allowed is False

    @pytest.mark.anyio
    async def test_different_limits_per_key(self):
        from app.middleware.rate_limit import TierRateLimiter

        limiter = TierRateLimiter()
        for _ in range(3):
            await limiter.is_allowed("tier_low", 3)
        assert (await limiter.is_allowed("tier_low", 3))[0] is False
        assert (await limiter.is_allowed("tier_high", 10))[0] is True


class TestRedisRateLimiter:
    @pytest.mark.anyio
    async def test_raises_connection_error_when_not_connected(self):
        from app.middleware.rate_limit import RedisRateLimiter

        limiter = RedisRateLimiter()
        with pytest.raises(ConnectionError):
            await limiter.is_allowed("key")

    @pytest.mark.anyio
    async def test_fallback_to_in_memory_in_middleware(self):
        from app.middleware.rate_limit import RedisRateLimiter, RateLimitMiddleware

        limiter = RedisRateLimiter()
        assert limiter._connected is False
        assert limiter._redis is None


class TestAiRateLimitDependency:
    @pytest.mark.anyio
    async def test_allows_within_limit(self):
        from app.middleware.rate_limit import ai_rate_limit, _ai_buckets

        _ai_buckets.clear()
        user = {"sub": "test_user"}
        result = await ai_rate_limit(user=user)
        assert result is None

    @pytest.mark.anyio
    async def test_raises_429_when_exceeded(self):
        from app.middleware.rate_limit import ai_rate_limit, _ai_buckets, AI_RATE_LIMIT
        from fastapi import HTTPException

        _ai_buckets.clear()
        user = {"sub": "burst_user"}
        now = time.time()
        _ai_buckets["burst_user"] = [now] * AI_RATE_LIMIT

        with pytest.raises(HTTPException) as exc:
            await ai_rate_limit(user=user)
        assert exc.value.status_code == 429
        assert "AI rate limit exceeded" in str(exc.value.detail)


class TestRateLimitMiddleware:
    @pytest.mark.anyio
    async def test_skips_metrics_endpoint(self):
        from app.middleware.rate_limit import RateLimitMiddleware

        mock_request = MagicMock()
        mock_request.url.path = "/metrics"
        mock_call_next = AsyncMock()
        mock_call_next.return_value = MagicMock(headers={})

        middleware = RateLimitMiddleware.__new__(RateLimitMiddleware)
        middleware._redis_limiter = AsyncMock()
        middleware._redis_limiter.is_allowed.return_value = (True, 0)
        middleware._memory_limiter = AsyncMock()
        middleware._memory_limiter.is_allowed.return_value = (True, 0)
        middleware._ai_limiter = AsyncMock()
        middleware._ai_limiter.is_allowed.return_value = (True, 0)
        middleware._tier_limiter = AsyncMock()
        middleware._tier_limiter.is_allowed.return_value = (True, 0)

        await middleware.dispatch(mock_request, mock_call_next)
        mock_call_next.assert_awaited_once()

    @pytest.mark.anyio
    async def test_returns_429_when_rate_exceeded(self):
        from app.middleware.rate_limit import RateLimitMiddleware

        mock_request = MagicMock()
        mock_request.url.path = "/api/v1/test"
        mock_request.headers = {}
        mock_request.client.host = "1.2.3.4"

        mock_memory = AsyncMock()
        mock_memory.is_allowed.return_value = (False, int(time.time()) + 60, 0)

        middleware = RateLimitMiddleware.__new__(RateLimitMiddleware)
        middleware._redis_limiter = AsyncMock()
        middleware._redis_limiter.is_allowed.return_value = (False, int(time.time()) + 60, 0)
        middleware._redis_limiter._connected = True
        middleware._memory_limiter = mock_memory
        middleware._ai_limiter = MagicMock()
        middleware._tier_limiter = AsyncMock()
        middleware._tier_limiter.is_allowed.return_value = (True, 0)

        resp = await middleware.dispatch(mock_request, MagicMock())
        assert resp.status_code == 429

    @pytest.mark.anyio
    async def test_ai_endpoint_rate_limit(self):
        from app.middleware.rate_limit import RateLimitMiddleware

        mock_request = MagicMock()
        mock_request.url.path = "/api/v1/ai/advisor"
        mock_request.headers = {"Authorization": "Bearer valid.jwt.token"}

        middleware = RateLimitMiddleware.__new__(RateLimitMiddleware)
        mock_ai = AsyncMock()
        mock_ai.is_allowed.return_value = (False, int(time.time()) + 60)
        middleware._ai_limiter = mock_ai
        middleware._redis_limiter = AsyncMock()
        middleware._redis_limiter.is_allowed.return_value = (True, 0)
        middleware._memory_limiter = AsyncMock()
        middleware._memory_limiter.is_allowed.return_value = (True, 0)
        middleware._tier_limiter = AsyncMock()
        middleware._tier_limiter.is_allowed.return_value = (True, 0)

        resp = await middleware.dispatch(mock_request, MagicMock())
        assert resp.status_code == 429

    @pytest.mark.anyio
    async def test_adds_rate_limit_headers_on_success(self):
        from app.middleware.rate_limit import RateLimitMiddleware
        from starlette.responses import Response

        mock_request = MagicMock()
        mock_request.url.path = "/api/v1/test"
        mock_request.headers = {}
        mock_request.client.host = "1.2.3.4"

        inner_response = Response()
        mock_call_next = AsyncMock(return_value=inner_response)

        middleware = RateLimitMiddleware.__new__(RateLimitMiddleware)
        middleware._redis_limiter = AsyncMock()
        middleware._redis_limiter.is_allowed.return_value = (True, int(time.time()) + 60, 58)
        middleware._redis_limiter._connected = True
        middleware._memory_limiter = MagicMock()
        middleware._ai_limiter = MagicMock()
        middleware._tier_limiter = AsyncMock()
        middleware._tier_limiter.is_allowed.return_value = (True, 0)

        resp = await middleware.dispatch(mock_request, mock_call_next)
        assert "X-RateLimit-Remaining" in resp.headers
        assert "X-RateLimit-Reset" in resp.headers

    @pytest.mark.anyio
    async def test_falls_back_to_in_memory_on_redis_failure(self):
        from app.middleware.rate_limit import RateLimitMiddleware
        from starlette.responses import Response

        mock_request = MagicMock()
        mock_request.url.path = "/api/v1/test"
        mock_request.headers = {}
        mock_request.client.host = "1.2.3.4"

        inner_response = Response()
        mock_call_next = AsyncMock(return_value=inner_response)

        middleware = RateLimitMiddleware.__new__(RateLimitMiddleware)
        middleware._redis_limiter = AsyncMock()
        middleware._redis_limiter.is_allowed.side_effect = Exception("Redis down")
        middleware._memory_limiter = AsyncMock()
        middleware._memory_limiter.is_allowed.return_value = (True, int(time.time()) + 60, 59)
        middleware._ai_limiter = MagicMock()
        middleware._tier_limiter = AsyncMock()
        middleware._tier_limiter.is_allowed.return_value = (True, 0)

        resp = await middleware.dispatch(mock_request, mock_call_next)
        middleware._memory_limiter.is_allowed.assert_awaited_once()
        assert resp.status_code != 429
