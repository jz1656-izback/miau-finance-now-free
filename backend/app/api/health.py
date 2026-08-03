"""Enhanced health check with service status, webhook alerts, and Prometheus metrics."""
import os, logging, asyncio, json
from datetime import timezone, datetime, timedelta
from fastapi import APIRouter
from fastapi.responses import PlainTextResponse
from app.services.data.registry import registry
from app.config import settings
from app.async_utils import safe_task

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Health"])
START_TIME = datetime.now(timezone.utc)

LAST_ALERT_KEY = "health:last_alert"
HEALTH_HISTORY_TTL = 604800  # 7 days in seconds

# Stored for Prometheus metrics
_last_health_result: dict | None = None


async def get_redis():
    try:
        from app.cache import get_redis as _get_redis
        return await _get_redis()
    except Exception:
        return None


async def store_health_history(result: dict):
    try:
        r = await asyncio.wait_for(get_redis(), timeout=1)
        if r is None:
            return
        try:
            now = datetime.now(timezone.utc)
            hour_key = f"health:history:{now.strftime('%Y-%m-%d:%H')}"
            entry = {
                "timestamp": result["timestamp"],
                "providers_healthy": result["services"]["providers_healthy"],
                "providers_unhealthy": result["services"]["providers_unhealthy"],
                "total_providers": result["services"]["data_providers"],
            }
            await r.rpush(hour_key, json.dumps(entry))
            await r.expire(hour_key, HEALTH_HISTORY_TTL)
            await r.ltrim(hour_key, -60, -1)
        except Exception as e:
            logger.debug(f"Failed to store health history: {e}")
    except Exception:
        pass


async def send_webhook_alert(unhealthy: list[str]):
    webhook_url = settings.slack_webhook_url or os.getenv("SLACK_WEBHOOK_URL") or settings.webhook_notification_url or os.getenv("WEBHOOK_NOTIFICATION_URL")
    if not webhook_url:
        return
    try:
        r = await asyncio.wait_for(get_redis(), timeout=1)
        if r is not None:
            try:
                last = await r.get(LAST_ALERT_KEY)
                if last:
                    last_time = datetime.fromisoformat(last)
                    if datetime.now(timezone.utc) - last_time < timedelta(minutes=5):
                        return
                await r.setex(LAST_ALERT_KEY, 300, datetime.now(timezone.utc).isoformat())
            except Exception:
                pass
    except Exception:
        pass
    payload = {
        "text": f"🐱 *Miau Finance Alert*\nUnhealthy providers: {', '.join(unhealthy)}\n"
                f"Time: {datetime.now(timezone.utc).isoformat()}Z\n"
                f"Service: {os.getenv('APP_VERSION', 'v2.3.0')}",
    }
    try:
        import httpx
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.post(webhook_url, json=payload)
            logger.info(f"Webhook alert sent: {resp.status_code}")
    except Exception as e:
        logger.warning(f"Failed to send webhook alert: {e}")


SERVICE_CHECKS = [
    {"name": "Frontend", "url": "http://frontend:5173", "port": 5173},
    {"name": "Backend", "url": "http://backend:8000/api/v1/health", "port": 8000},
    {"name": "Education", "url": "http://education-platform:5174", "port": 5174},
    {"name": "Grafana", "url": "http://grafana:3000", "port": 3000},
    {"name": "Prometheus", "url": "http://prometheus:9090", "port": 9090},
]

HOST_SERVICES = [
    {"name": "Homepage", "port": 3001},
    {"name": "Marketing", "port": 5176},
    {"name": "Cat Galaxy", "port": 5181},
    {"name": "Admin", "port": 5179},
    {"name": "Miau Corp", "port": 5175},
]


@router.get("/api/v1/health")
async def health_check():
    try:
        return await asyncio.wait_for(_health_check(), timeout=2)
    except asyncio.TimeoutError:
        return {
            "status": "healthy",
            "version": os.getenv("APP_VERSION", "v2.5.0"),
            "uptime_seconds": int((datetime.now(timezone.utc) - START_TIME).total_seconds()),
            "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
            "services": {"api": True, "data_providers": registry.count(), "providers_healthy": 0, "providers_unhealthy": 0},
            "provider_health": {},
            "note": "provider health timed out — check individual endpoints",
        }


async def _health_check():
    provider_count = registry.count()
    provider_health = {}
    try:
        async def _check(p):
            try:
                h = await asyncio.wait_for(p.health(), timeout=2)
                return p.name, h.healthy if hasattr(h, 'healthy') else True
            except Exception:
                return p.name, False
        results = await asyncio.gather(*[_check(p) for p in registry.list()], return_exceptions=True)
        for r in results:
            if isinstance(r, tuple):
                provider_health[r[0]] = r[1]
    except Exception as e:
        provider_health = {"error": str(e)}

    log_status = {}
    for log_dir in [os.getenv("LOG_DIR", "/var/log/miau"), "/tmp/miau-logs"]:
        if os.path.isdir(log_dir):
            for f in ["miau.log", "app.log", "audit.log"]:
                fp = os.path.join(log_dir, f)
                if os.path.isfile(fp):
                    log_status[f] = {
                        "size_bytes": os.path.getsize(fp),
                        "modified": datetime.fromtimestamp(os.path.getmtime(fp)).isoformat(),
                    }

    unhealthy = [name for name, ok in provider_health.items() if not ok]
    if unhealthy:
        safe_task(send_webhook_alert(unhealthy), name="health-webhook-alert")

    result = {
        "status": "healthy",
        "version": os.getenv("APP_VERSION", "v2.5.0"),
        "uptime_seconds": int((datetime.now(timezone.utc) - START_TIME).total_seconds()),
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
        "services": {
            "api": True,
            "data_providers": registry.count(),
            "providers_healthy": sum(1 for h in provider_health.values() if h),
            "providers_unhealthy": sum(1 for h in provider_health.values() if not h),
        },
        "provider_health": provider_health,
        "log_files": log_status,
    }

    global _last_health_result
    _last_health_result = result
    safe_task(store_health_history(result), name="health-store-history")
    return result


@router.get("/api/v1/health/services")
async def services_health():
    results = {}
    async def _check_service(svc: dict):
        try:
            import httpx
            async with httpx.AsyncClient(timeout=3, follow_redirects=True) as client:
                resp = await client.head(svc["url"])
                results[svc["name"]] = {"up": True, "code": resp.status_code, "port": svc["port"]}
                return
        except Exception:
            pass
        results[svc["name"]] = {"up": False, "code": None, "port": svc["port"]}
    await asyncio.gather(*[_check_service(s) for s in SERVICE_CHECKS])
    for svc in HOST_SERVICES:
        if svc["name"] not in results:
            results[svc["name"]] = {"up": None, "code": None, "port": svc["port"], "note": "host-only (check from browser)"}
    total = len(SERVICE_CHECKS) + len(HOST_SERVICES)
    up = sum(1 for v in results.values() if v.get("up") is True)
    down = sum(1 for v in results.values() if v.get("up") is False)
    unknown = sum(1 for v in results.values() if v.get("up") is None)
    return {
        "status": "healthy" if up == total else "degraded",
        "total": total,
        "up": up,
        "down": down,
        "unknown": unknown,
        "services": results,
        "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
    }


@router.get("/api/v1/health/history")
async def health_history(hours: int = 24):
    r = await get_redis()
    if r is None:
        return {"history": [], "note": "Redis not available"}
    history = []
    now = datetime.now(timezone.utc)
    for i in range(hours):
        key = f"health:history:{(now - timedelta(hours=i)).strftime('%Y-%m-%d:%H')}"
        try:
            entries = await r.lrange(key, 0, -1)
            for e in entries:
                history.append(json.loads(e))
        except Exception:
            pass
    history.sort(key=lambda x: x["timestamp"])
    return {"history": history[-500:]}  # cap at 500 entries


@router.get("/metrics")
async def prometheus_metrics():
    try:
        from app.middleware.metrics import PrometheusMiddleware
        from app.main import app
        for m in app.user_middleware:
            if m.cls == PrometheusMiddleware:
                return PlainTextResponse(content=m.kwargs.get('app', app).get_metrics(), media_type="text/plain")
    except Exception as e:
        pass
    return PlainTextResponse(content="# metrics not available\n", media_type="text/plain")
