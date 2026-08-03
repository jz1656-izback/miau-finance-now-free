"""Prometheus metrics middleware and endpoint for FastAPI."""
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Track request count, duration, and status codes for Prometheus scraping."""

    def __init__(self, app):
        super().__init__(app)
        self._request_count = 0
        self._error_count = 0
        self._total_duration = 0.0
        self._requests_by_path: dict[str, int] = {}
        self._errors_by_path: dict[str, int] = {}
        self._duration_by_path: dict[str, float] = {}

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        try:
            response: Response = await call_next(request)
            status = response.status_code
        except Exception:
            status = 500
            raise
        finally:
            duration = time.time() - start
            path = request.url.path
            self._request_count += 1
            self._total_duration += duration
            self._requests_by_path[path] = self._requests_by_path.get(path, 0) + 1
            self._duration_by_path[path] = self._duration_by_path.get(path, 0) + duration
            if status >= 400:
                self._error_count += 1
                self._errors_by_path[path] = self._errors_by_path.get(path, 0) + 1
        return response

    def get_metrics(self) -> str:
        import re
        lines = [
            "# HELP miau_requests_total Total HTTP requests",
            "# TYPE miau_requests_total counter",
            f'miau_requests_total {self._request_count}',
            "# HELP miau_errors_total Total HTTP errors (4xx/5xx)",
            "# TYPE miau_errors_total counter",
            f'miau_errors_total {self._error_count}',
            "# HELP miau_request_duration_seconds_total Total request duration",
            "# TYPE miau_request_duration_seconds_total counter",
            f'miau_request_duration_seconds_total {self._total_duration:.3f}',
            "# HELP miau_requests_by_path Requests per path",
            "# TYPE miau_requests_by_path gauge",
        ]
        for path, count in sorted(self._requests_by_path.items()):
            safe_path = re.sub(r'[^a-zA-Z0-9_/]', '_', path)
            lines.append(f'miau_requests_by_path{{path="{safe_path}"}} {count}')
        lines.extend([
            "# HELP miau_errors_by_path Errors per path",
            "# TYPE miau_errors_by_path gauge",
        ])
        for path, count in sorted(self._errors_by_path.items()):
            safe_path = re.sub(r'[^a-zA-Z0-9_/]', '_', path)
            lines.append(f'miau_errors_by_path{{path="{safe_path}"}} {count}')
        # Provider health — pulled from health endpoint singleton
        try:
            from app.api.health import _last_health_result
            if _last_health_result:
                lines.extend([
                    "# HELP miau_providers_healthy Number of healthy providers",
                    "# TYPE miau_providers_healthy gauge",
                    f'miau_providers_healthy {_last_health_result["services"]["providers_healthy"]}',
                    "# HELP miau_providers_unhealthy Number of unhealthy providers",
                    "# TYPE miau_providers_unhealthy gauge",
                    f'miau_providers_unhealthy {_last_health_result["services"]["providers_unhealthy"]}',
                ])
        except Exception:
            pass
        return '\n'.join(lines) + '\n'


# Singleton
_metrics_middleware: PrometheusMiddleware = None


def get_metrics_middleware():
    global _metrics_middleware
    return _metrics_middleware


def set_metrics_middleware(mw: PrometheusMiddleware):
    global _metrics_middleware
    _metrics_middleware = mw
