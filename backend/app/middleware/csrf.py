import logging
import secrets
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

CSRF_TOKEN_HEADER = "X-CSRF-Token"
CSRF_COOKIE_NAME = "csrf_token"
SAFE_METHODS = {"GET", "HEAD", "OPTIONS", "TRACE"}
MAX_CSRF_TOKEN_AGE = 3600


class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method in SAFE_METHODS:
            response: Response = await call_next(request)
            if not request.cookies.get(CSRF_COOKIE_NAME):
                token = secrets.token_urlsafe(32)
                response.set_cookie(
                    key=CSRF_COOKIE_NAME,
                    value=token,
                    httponly=False,
                    secure=request.url.scheme == "https",
                    samesite="lax",
                    max_age=MAX_CSRF_TOKEN_AGE,
                    path="/",
                )
            return response

        if request.url.path in ("/api/v1/auth/token", "/api/v1/auth/register", "/api/v1/auth/education-student", "/api/v1/marketing/track", "/api/v1/pawdentity/login", "/api/v1/pawdentity/logout") or request.url.path.startswith("/api/v1/marketing/public/"):
            response: Response = await call_next(request)
            return response

        csrf_cookie = request.cookies.get(CSRF_COOKIE_NAME)
        csrf_header = request.headers.get(CSRF_TOKEN_HEADER)

        if not csrf_cookie or not csrf_header:
            logger.warning(f"CSRF validation failed: missing token from {request.client.host if request.client else 'unknown'} {request.method} {request.url.path}")
            return Response(
                content='{"detail":"CSRF token missing"}',
                status_code=403,
                media_type="application/json",
            )

        if not secrets.compare_digest(csrf_cookie, csrf_header):
            logger.warning(f"CSRF token mismatch from {request.client.host if request.client else 'unknown'} {request.method} {request.url.path}")
            return Response(
                content='{"detail":"CSRF token mismatch"}',
                status_code=403,
                media_type="application/json",
            )

        response: Response = await call_next(request)
        return response


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or secrets.token_urlsafe(16)
        request.state.request_id = request_id
        request.state.request_start_time = time.time()

        response: Response = await call_next(request)

        response.headers["X-Request-ID"] = request_id
        duration_ms = (time.time() - request.state.request_start_time) * 1000
        response.headers["X-Response-Time-Ms"] = f"{duration_ms:.1f}"

        return response