"""
Data Quality Health Endpoint — reports freshness metrics for all data domains.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone

from fastapi import APIRouter

from app.middleware.data_quality import DOMAIN_TTLS

router = APIRouter(tags=["Data Quality"])


@router.get("/api/v1/data-quality/health")
async def data_quality_health():
    """Report data quality status for all monitored domains."""
    now = int(time.time())
    domains = []
    for domain, ttl in DOMAIN_TTLS.items():
        domains.append({
            "domain": domain,
            "ttl_seconds": ttl,
            "ttl_label": _format_ttl(ttl),
            "status": "configured",
            "checked_at": now,
        })
    return {
        "status": "ok",
        "domains_monitored": len(domains),
        "domains": domains,
        "as_of": datetime.now(timezone.utc).isoformat(),
    }


@router.get("/api/v1/data-quality/domains")
async def data_quality_domains():
    """List all monitored data domains with their TTLs."""
    return {
        "domains": {k: {"ttl_seconds": v, "ttl_label": _format_ttl(v)} for k, v in DOMAIN_TTLS.items()},
        "total": len(DOMAIN_TTLS),
    }


def _format_ttl(seconds: int) -> str:
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m"
    return f"{seconds // 3600}h"
