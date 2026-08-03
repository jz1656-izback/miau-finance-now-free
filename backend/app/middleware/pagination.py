"""
🔒 PAGINATION ENFORCEMENT
Ensure all list endpoints have limits to prevent memory bomb attacks
"""

import logging
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
from typing import Optional, Generic, TypeVar, List

# 🔒 Pagination limits
DEFAULT_LIMIT = 20
MAX_LIMIT = 500
DEFAULT_OFFSET = 0
MAX_OFFSET = 1_000_000


class PaginationParams(BaseModel):
    """Standard pagination parameters for all list endpoints"""
    limit: int = Field(DEFAULT_LIMIT, ge=1, le=MAX_LIMIT, description="Max items per page")
    offset: int = Field(DEFAULT_OFFSET, ge=0, le=MAX_OFFSET, description="Pagination offset")
    
    class Config:
        schema_extra = {
            "example": {
                "limit": 20,
                "offset": 0
            }
        }


T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response format"""
    items: List[T]
    total: int = Field(..., description="Total number of items available")
    limit: int = Field(..., description="Items per page")
    offset: int = Field(..., description="Current offset")
    has_more: bool = Field(..., description="Whether more items are available")
    
    class Config:
        schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "limit": 20,
                "offset": 0,
                "has_more": True
            }
        }


def apply_pagination(
    items: List[T],
    total: int,
    limit: int = DEFAULT_LIMIT,
    offset: int = DEFAULT_OFFSET,
) -> dict:
    """
    Apply pagination to a list of items
    
    Usage in endpoints:
        @app.get("/items")
        async def get_items(limit: int = 20, offset: int = 0):
            all_items = await db.get_all_items()
            paginated = apply_pagination(
                items=all_items,
                total=len(all_items),
                limit=limit,
                offset=offset
            )
            return paginated
    """
    # 🔒 Enforce limits
    limit = min(limit, MAX_LIMIT)
    limit = max(limit, 1)
    offset = max(0, offset)
    logger.debug("Pagination: limit=%d offset=%d total=%d", limit, offset, total)
    
    # Apply pagination
    paginated_items = items[offset:offset + limit]
    
    return {
        "items": paginated_items,
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + limit < total
    }


import asyncio
import functools


def enforce_pagination(func):
    """
    Decorator to enforce pagination on async list endpoints.

    Works with both sync and async FastAPI endpoints.
    
    Usage:
        @router.get("/items")
        @enforce_pagination
        async def get_items(limit: int = 20, offset: int = 0):
            ...
    """
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            limit = kwargs.get('limit', DEFAULT_LIMIT)
            offset = kwargs.get('offset', DEFAULT_OFFSET)
            kwargs['limit'] = max(1, min(limit, MAX_LIMIT))
            kwargs['offset'] = max(0, offset)
            return await func(*args, **kwargs)
        return async_wrapper
    else:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            limit = kwargs.get('limit', DEFAULT_LIMIT)
            offset = kwargs.get('offset', DEFAULT_OFFSET)
            kwargs['limit'] = max(1, min(limit, MAX_LIMIT))
            kwargs['offset'] = max(0, offset)
            return func(*args, **kwargs)
        return sync_wrapper
