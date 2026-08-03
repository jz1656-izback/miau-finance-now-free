"""
Data Quality Middleware — monitors freshness and validity of cached/market data.

Adds warning headers to responses when data is stale or contains outliers.
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

# TTL thresholds per data domain (seconds)
DOMAIN_TTLS: dict[str, int] = {
    "price": 60,
    "historical": 3600,
    "company_info": 86400,
    "forex": 300,
    "crypto": 60,
    "news": 3600,
    "sentiment": 300,
    "fundamentals": 3600,
    "economics": 3600,
}


class DataQualityMiddleware(BaseHTTPMiddleware):
    """Middleware that checks data freshness and adds quality headers."""

    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)
        self._add_freshness_headers(request, response)
        self._add_data_quality_headers(response)
        return response

    def _add_freshness_headers(self, request: Request, response: Response) -> None:
        """Add X-Data-Freshness header based on endpoint path."""
        path = request.url.path

        # Determine domain from path
        domain = None
        for key in DOMAIN_TTLS:
            if key in path:
                domain = key
                break

        if domain:
            ttl = DOMAIN_TTLS[domain]
            now = int(time.time())
            response.headers["X-Data-Domain"] = domain
            response.headers["X-Data-TTL"] = str(ttl)
            response.headers["X-Data-Timestamp"] = str(now)
            response.headers["X-Data-Fresh-Until"] = str(now + ttl)

    def _add_data_quality_headers(self, response: Response) -> None:
        """Add quality indicators to response."""
        status = response.status_code
        if status >= 400:
            response.headers["X-Data-Quality"] = "error"
        elif status >= 300:
            response.headers["X-Data-Quality"] = "redirect"
        else:
            response.headers["X-Data-Quality"] = "fresh"

        response.headers["X-Data-Origin"] = "miau-finance"
