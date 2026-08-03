import time

from fastapi import Request, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

active_connections = Gauge(
    "active_connections",
    "Number of active connections",
)

api_errors_total = Counter(
    "api_errors_total",
    "Total API errors",
    ["method", "endpoint", "error_type"],
)

redis_hits_total = Counter(
    "redis_hits_total",
    "Total Redis cache hits",
    ["key_prefix"],
)

redis_misses_total = Counter(
    "redis_misses_total",
    "Total Redis cache misses",
    ["key_prefix"],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        active_connections.inc()
        start_time = time.time()
        status = 500
        try:
            response: Response = await call_next(request)
            status = response.status_code
            return response
        finally:
            duration = time.time() - start_time
            endpoint = request.url.path
            method = request.method
            http_requests_total.labels(method=method, endpoint=endpoint, status=status).inc()
            http_request_duration_seconds.labels(method=method, endpoint=endpoint).observe(duration)
            if status >= 400:
                error_type = "client_error" if status < 500 else "server_error"
                api_errors_total.labels(method=method, endpoint=endpoint, error_type=error_type).inc()
            active_connections.dec()


async def metrics_endpoint():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
