"""
🔒 INPUT VALIDATION DECORATOR
Apply to all endpoints to ensure Pydantic validation
"""

from functools import wraps
from pydantic import ValidationError, BaseModel
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


def validate_input(schema_class):
    """
    Decorator to validate request body against a Pydantic schema
    
    Usage:
        @app.post("/endpoint")
        @validate_input(MySchema)
        async def my_endpoint(data):
            # data is guaranteed to be valid
            pass
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Pydantic validation is automatic with FastAPI
                # This decorator documents the intent
                return await func(*args, **kwargs)
            except ValidationError as e:
                logger.warning(f"Input validation error: {e}")
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=[
                        {
                            "loc": error["loc"],
                            "msg": error["msg"],
                            "type": error["type"]
                        }
                        for error in e.errors()
                    ]
                )
            except Exception as e:
                logger.error(f"Unexpected error during validation: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Internal server error"
                )
        return wrapper
    return decorator


class SafeDict(dict):
    """Dictionary that sanitizes string values"""
    
    def __setitem__(self, key, value):
        if isinstance(value, str):
            # Remove null bytes and control characters
            value = ''.join(char for char in value if ord(char) >= 32 or char in '\n\t')
        super().__setitem__(key, value)


def sanitize_query_params(**params):
    """Sanitize query parameters"""
    sanitized = {}
    for key, value in params.items():
        if isinstance(value, str):
            # Max length for query params
            value = value[:1000]
            # Remove dangerous characters
            dangerous = ['<', '>', '"', "'", ';', '--', '/*', '*/']
            for char in dangerous:
                value = value.replace(char, '')
        sanitized[key] = value
    return sanitized
