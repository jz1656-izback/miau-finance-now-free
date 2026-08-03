import re
import json
import logging
from typing import Optional
from urllib.parse import parse_qs
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

SUSPICIOUS_PATTERNS = re.compile(
    r"(<script|javascript:|onerror=|onload=|onclick=|alert\(|"
    r"prompt\(|confirm\(|SELECT\s.*FROM|DROP\sTABLE|DELETE\sFROM|"
    r"INSERT\sINTO|UPDATE\s.*SET|EXEC\s|xp_cmdshell|"
    r"UNION\s.*SELECT|--\s|/\*|\\\\\\)",
    re.IGNORECASE,
)

BLOCKED_IN_PATH = re.compile(r"[<>\"'\\{}]")

MAX_QUERY_STRING_LENGTH = 2048


def strip_html_tags(value: str) -> str:
    return re.sub(r"<[^>]*>", "", value)


def sanitize_string(value: str) -> str:
    value = value.replace("&", "&amp;")
    value = value.replace("<", "&lt;")
    value = value.replace(">", "&gt;")
    value = value.replace('"', "&quot;")
    value = value.replace("'", "&#x27;")
    value = strip_html_tags(value)
    return value


def validate_ticker(value: str) -> Optional[str]:
    cleaned = value.strip().upper()
    if not re.match(r"^[A-Z0-9]{1,10}$", cleaned):
        return None
    return cleaned


def validate_command(value: str) -> Optional[str]:
    cleaned = strip_html_tags(value.strip())
    dangerous = re.search(r"[;&|`$(){}!#~]", cleaned)
    if dangerous:
        return None
    if re.match(r"^[a-zA-Z0-9_\-\s\.\/:]+$", cleaned):
        return cleaned
    return None


class InputSanitizationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        query = request.url.query
        path = request.url.path

        if len(query) > MAX_QUERY_STRING_LENGTH:
            logger.warning("Query string too long: %d chars from %s", len(query), request.client.host if request.client else "unknown")
            return Response(
                status_code=414,
                content=json.dumps({"detail": "Query string too long"}),
                media_type="application/json",
            )

        if SUSPICIOUS_PATTERNS.search(query):
            logger.warning("Suspicious patterns in query from %s", request.client.host if request.client else "unknown")
            return Response(
                status_code=422,
                content=json.dumps({"detail": "Request blocked: suspicious characters in query"}),
                media_type="application/json",
            )

        if BLOCKED_IN_PATH.search(path):
            logger.warning("Blocked characters in path %s from %s", path, request.client.host if request.client else "unknown")
            return Response(
                status_code=422,
                content=json.dumps({"detail": "Request blocked: invalid characters in path"}),
                media_type="application/json",
            )

        if query:
            for values in parse_qs(query).values():
                for value in values:
                    if SUSPICIOUS_PATTERNS.search(value):
                        logger.warning("Suspicious content in query params from %s", request.client.host if request.client else "unknown")
                        return Response(
                            status_code=422,
                            content=json.dumps({"detail": "Request blocked: suspicious content in query parameters"}),
                            media_type="application/json",
                        )

        response: Response = await call_next(request)
        response.headers["X-Content-Sanitized"] = "true"
        return response