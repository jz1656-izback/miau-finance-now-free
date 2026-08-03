"""v3.0 Datavore Edition — consolidated API endpoints for all new data sources."""
import logging
import httpx
from fastapi import APIRouter, Depends, Query, HTTPException
from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)

from app.services.data.registry import registry
from app.services.data.companies import get_companies_by_continent, get_company_count, get_continent_centroid, CONTINENT_CENTROIDS

# router created in __init__.py


def _get_provider(name: str):
    p = registry.get(name)
    if not p:
        from fastapi import HTTPException
        raise HTTPException(404, f"Data source '{name}' not available")
    return p

