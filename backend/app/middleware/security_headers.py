import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        health_prefixes = ("/api/v1/health", "/metrics")
        if settings.environment == "production" and request.url.scheme == "http" and \
                not path.startswith(health_prefixes):
            return Response(
                status_code=301,
                headers={"Location": str(request.url).replace("http://", "https://", 1)},
            )

        response: Response = await call_next(request)

        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "worker-src 'self'; "
            "connect-src 'self' https://api.openai.com https://api.anthropic.com https://query1.finance.yahoo.com https://api.coingecko.com; "
            "frame-ancestors 'none'; "
            "form-action 'self'; "
            "base-uri 'self'; "
            "upgrade-insecure-requests"
        )
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-DNS-Prefetch-Control"] = "off"
        response.headers["Permissions-Policy"] = (
            "accelerometer=(), camera=(), geolocation=(), gyroscope=(), "
            "magnetometer=(), microphone=(), payment=(), usb=()"
        )
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"

        # Remove server header (don't leak FastAPI version)
        response.headers["server"] = "miau"

        # Set Cache-Control for sensitive (non-GET) responses
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            response.headers.setdefault("Cache-Control", "no-store, no-cache, must-revalidate")
            response.headers.setdefault("Pragma", "no-cache")

        return response
