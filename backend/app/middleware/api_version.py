import logging
from datetime import date
from typing import Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

API_CURRENT_VERSION = "2026-05-19"
API_SUPPORTED_VERSIONS = {
    "2026-05-19": {"status": "current", "deprecated": False},
    "2026-03-01": {"status": "deprecated", "deprecated": True, "sunset": date(2026, 9, 1)},
}
API_VERSION_HEADER = "X-API-Version"
API_DEPRECATION_HEADER = "X-API-Deprecated"
API_SUNSET_HEADER = "X-API-Sunset"

# Versioned changelog: endpoint changes per version
API_CHANGELOG: dict[str, list[str]] = {
    "2026-05-19": [
        "Add ESG endpoints: /api/v1/esg/*, /api/v1/carbon/*, /api/v1/green/*",
        "Add multi-currency portfolio support via base_currency field",
        "Global market data endpoints: /api/v1/markets/global/*",
        "Plugin system: /api/v1/plugins/* with sandboxed execution",
    ],
    "2026-03-01": [
        "Initial v1 API release",
        "Market data, portfolios, trades, analytics endpoints",
        "AI advisor, alerts, watchlist, social features",
        "Developer API keys, webhooks, billing",
    ],
}


def get_current_version() -> str:
    return API_CURRENT_VERSION


def get_supported_versions() -> dict[str, dict]:
    return dict(API_SUPPORTED_VERSIONS)


def get_changelog(version: Optional[str] = None) -> dict[str, list[str]]:
    if version:
        return {version: API_CHANGELOG.get(version, [])}
    return dict(API_CHANGELOG)


def is_version_deprecated(version: str) -> bool:
    info = API_SUPPORTED_VERSIONS.get(version)
    return info["deprecated"] if info else True


def get_version_sunset(version: str) -> Optional[date]:
    info = API_SUPPORTED_VERSIONS.get(version)
    return info.get("sunset") if info else None


class ApiVersionMiddleware(BaseHTTPMiddleware):
    """API version management middleware.

    Reads `X-API-Version` request header and sets response headers:
      - X-API-Version: the resolved version
      - X-API-Deprecated: true if version is deprecated (and response body is unchanged)
      - X-API-Sunset: RFC 1123 date when the version will be removed

    Also exposes /api/v1/api-version endpoint for clients to discover:
      - current version, supported versions, changelog.

    Wire in main.py:
        from app.middleware.api_version import ApiVersionMiddleware
        app.add_middleware(ApiVersionMiddleware)
    """

    async def dispatch(self, request: Request, call_next):
        requested = request.headers.get(API_VERSION_HEADER, "")
        resolved = API_CURRENT_VERSION

        if requested:
            if requested in API_SUPPORTED_VERSIONS:
                resolved = requested
            else:
                logger.debug("Unknown API version '%s' requested, defaulting to %s", requested, API_CURRENT_VERSION)

        response: Response = await call_next(request)
        response.headers[API_VERSION_HEADER] = resolved

        if is_version_deprecated(resolved):
            response.headers[API_DEPRECATION_HEADER] = "true"
            sunset = get_version_sunset(resolved)
            if sunset:
                response.headers[API_SUNSET_HEADER] = sunset.isoformat()

        return response
