"""Request/response logging middleware with timing, status, and sensitive data masking."""
import logging
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


logger = logging.getLogger("app")

EXCLUDED_PATHS = {"/metrics", "/health", "/openapi.json", "/docs", "/redoc"}


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every request with method, path, status, duration, and client IP."""

    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        start = time.time()
        client_ip = request.client.host if request.client else "unknown"
        request_id = getattr(request.state, "request_id", "")

        if request.method in ("POST", "PUT", "PATCH"):
            logger.info(
                "→ %s %s from %s", request.method, request.url.path, client_ip,
                extra={"request_id": request_id, "method": request.method, "path": request.url.path, "client_ip": client_ip},
            )

        try:
            response: Response = await call_next(request)
            duration_ms = round((time.time() - start) * 1000, 1)

            log_level = logging.WARNING if response.status_code >= 400 else logging.INFO
            logger.log(
                log_level,
                "← %s %s → %s (%sms)", request.method, request.url.path, response.status_code, duration_ms,
                extra={"request_id": request_id, "method": request.method, "path": request.url.path,
                       "status_code": response.status_code, "duration_ms": duration_ms, "client_ip": client_ip},
            )

            if duration_ms > 5000:
                logger.warning(
                    "SLOW: %s %s took %sms", request.method, request.url.path, duration_ms,
                    extra={"request_id": request_id, "method": request.method, "path": request.url.path,
                           "duration_ms": duration_ms, "client_ip": client_ip},
                )

            return response
        except Exception as e:
            duration_ms = round((time.time() - start) * 1000, 1)
            logger.error(
                "ERROR: %s %s failed after %sms: %s", request.method, request.url.path, duration_ms, str(e),
                extra={"request_id": request_id, "method": request.method, "path": request.url.path,
                       "duration_ms": duration_ms, "client_ip": client_ip},
            )
            raise
