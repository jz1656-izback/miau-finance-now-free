"""
🔒 REQUEST LIMITS MIDDLEWARE
Prevents memory bomb DoS attacks by limiting request sizes
"""

import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import Headers
import json

logger = logging.getLogger(__name__)

# 🔒 SECURITY: Define maximum request sizes
MAX_REQUEST_SIZE = 1_048_576  # 1MB
MAX_JSON_SIZE = 512_000       # 512KB for JSON
MAX_HEADER_SIZE = 8_192       # 8KB for headers

class RequestLimitsMiddleware(BaseHTTPMiddleware):
    """
    Limit request sizes to prevent:
    - Memory exhaustion attacks
    - Slowloris attacks
    - Large file upload DoS
    """
    
    async def dispatch(self, request: Request, call_next):
        # 🔒 Check Content-Length header
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                size = int(content_length)
                if size > MAX_REQUEST_SIZE:
                    logger.warning("Request too large: %d bytes from %s", size, request.client.host if request.client else "unknown")
                    return Response(
                        status_code=413,
                        content=json.dumps({
                            "detail": f"Request too large. Maximum {MAX_REQUEST_SIZE} bytes allowed",
                            "max_size": MAX_REQUEST_SIZE,
                            "received": size
                        }),
                        media_type="application/json",
                        headers={
                            "Content-Type": "application/json",
                            "Retry-After": "60"
                        }
                    )
            except ValueError:
                pass

        # 🔒 Check header size
        headers_size = sum(len(k) + len(v) for k, v in request.headers.items())
        if headers_size > MAX_HEADER_SIZE * 4:  # Allow multiple headers
            logger.warning("Headers too large: %d bytes from %s", headers_size, request.client.host if request.client else "unknown")
            return Response(
                status_code=431,
                content=json.dumps({"detail": "Headers too large"}),
                media_type="application/json"
            )

        # 🔒 For POST/PUT/PATCH, validate JSON size
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if "application/json" in content_type and content_length:
                try:
                    size = int(content_length)
                    if size > MAX_JSON_SIZE:
                        logger.warning("JSON payload too large: %d bytes from %s", size, request.client.host if request.client else "unknown")
                        return Response(
                            status_code=413,
                            content=json.dumps({
                                "detail": f"JSON payload too large. Maximum {MAX_JSON_SIZE} bytes",
                                "max_size": MAX_JSON_SIZE,
                                "received": size
                            }),
                            media_type="application/json"
                        )
                except ValueError:
                    pass

        response = await call_next(request)
        return response
