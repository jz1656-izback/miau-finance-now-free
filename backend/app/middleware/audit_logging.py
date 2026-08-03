"""
🔒 AUDIT LOGGING MIDDLEWARE
Logs all API calls for compliance, security investigation, and anomaly detection
Required for: PCI-DSS, SOC 2, GDPR, HIPAA
"""

import os
import time
import json
import logging
from typing import Optional
from datetime import datetime, timezone
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class JSONFormatter(logging.Formatter):
    """Structured JSON log formatter"""
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


# Configure audit logger
audit_logger = logging.getLogger("audit")
if not audit_logger.handlers:
    log_dir = "/var/log/miau"
    os.makedirs(log_dir, exist_ok=True)
    try:
        handler = logging.FileHandler(os.path.join(log_dir, "audit.log"))
    except (PermissionError, OSError):
        handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    audit_logger.addHandler(handler)
    audit_logger.setLevel(logging.INFO)


class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """
    Log all API requests and responses for:
    - Compliance audit trails
    - Security incident investigation
    - Anomaly detection
    - User activity tracking
    """

    # Paths that don't need logging (reduce noise)
    SKIP_PATHS = {
        "/metrics",
        "/health",
        "/openapi.json",
        "/docs",
        "/redoc",
    }

    # Sensitive fields to mask in logs
    SENSITIVE_FIELDS = {
        "password", "secret", "token", "key", "credential",
        "api_key", "access_token", "refresh_token", "jwt"
    }

    async def dispatch(self, request: Request, call_next):
        # Skip non-essential paths
        if request.url.path in self.SKIP_PATHS:
            return await call_next(request)

        # Get request metadata
        start_time = time.time()
        client_ip = self._get_client_ip(request)
        request_id = request.headers.get("X-Request-ID", "unknown")

        # Extract user info if authenticated (prefer resolved TierMiddleware values)
        user_id = getattr(request.state, "user_id", None) or "anonymous"
        tier = getattr(request.state, "tier", None) or "unknown"
        auth_type = getattr(request.state, "auth_type", None) or "none"
        if not getattr(request.state, "user_id", None):
            try:
                auth_header = request.headers.get("Authorization", "")
                if auth_header.startswith("Bearer "):
                    user_id = f"token:{auth_header[7:20]}..."
            except Exception as e:
                audit_logger.debug(f"Could not extract user from auth header: {e}")

        # Process request first so body isn't consumed
        response: Response = await call_next(request)

        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000

        # Log the request
        self._log_request(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            query=request.url.query,
            client_ip=client_ip,
            user_id=user_id,
            tier=tier,
            auth_type=auth_type,
            status_code=response.status_code,
            duration_ms=duration_ms,
            request=request,
        )

        # Add audit headers to response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Audit-Logged"] = "true"

        return response

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP from request, checking for proxies"""
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        client = request.client
        return client.host if client else "unknown"

    def _mask_sensitive_data(self, data: dict) -> dict:
        """Mask sensitive fields in logs"""
        masked = {}
        for key, value in data.items():
            if any(sensitive in key.lower() for sensitive in self.SENSITIVE_FIELDS):
                masked[key] = "***REDACTED***"
            elif isinstance(value, dict):
                masked[key] = self._mask_sensitive_data(value)
            elif isinstance(value, list):
                masked[key] = [
                    self._mask_sensitive_data(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                masked[key] = value
        return masked

    def _log_request(
        self,
        request_id: str,
        method: str,
        path: str,
        query: str,
        client_ip: str,
        user_id: str,
        tier: str = "unknown",
        auth_type: str = "none",
        status_code: int = 200,
        duration_ms: float = 0.0,
        request: Optional[Request] = None,
    ):
        """Log request with structured JSON format"""

        log_level = "INFO"
        if status_code >= 500:
            log_level = "ERROR"
        elif status_code >= 400:
            log_level = "WARNING"

        fallback = (
            f"method={method} path={path} status={status_code} "
            f"duration={duration_ms:.0f}ms client={client_ip} user={user_id} "
            f"tier={tier} auth={auth_type}"
        )

        if request and hasattr(request.state, "request_id"):
            rid = getattr(request.state, "request_id", request_id)
            audit_logger.info(
                f"REQUEST | {rid} | {method} {path} -> {status_code} ({duration_ms:.0f}ms) | {tier} | {auth_type}",
                extra={"request_id": rid},
            )
        else:
            audit_logger.log(getattr(logging, log_level), fallback)

        if status_code == 401:
            audit_logger.warning(
                f"UNAUTHORIZED_ACCESS client={client_ip} user={user_id} path={path}"
            )
        elif status_code == 403:
            audit_logger.warning(
                f"FORBIDDEN_ACCESS client={client_ip} user={user_id} path={path}"
            )
        elif duration_ms > 5000:
            audit_logger.info(f"SLOW_REQUEST path={path} duration={duration_ms:.0f}ms")


# Configure audit logging for different environments
def setup_audit_logging(environment: str):
    """Setup audit logging based on environment"""
    if environment == "production":
        # Production: Log to file
        audit_logger.setLevel(logging.INFO)
    else:
        # Development: Also log to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )
        console_handler.setFormatter(formatter)
        audit_logger.addHandler(console_handler)
        audit_logger.setLevel(logging.DEBUG)
