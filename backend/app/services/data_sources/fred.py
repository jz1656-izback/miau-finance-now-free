import asyncio
import hashlib
import httpx
from datetime import datetime, timedelta
from typing import Optional

from app.cache_utils import cached

FRED_BASE = "https://api.stlouisfed.org/fred"

SERIES_MAP = {
    "GDP": {"id": "GDP", "name": "Gross Domestic Product"},
    "CPIAUCSL": {"id": "CPIAUCSL", "name": "Consumer Price Index (CPI)"},
    "UNRATE": {"id": "UNRATE", "name": "Unemployment Rate"},
    "FEDFUNDS": {"id": "FEDFUNDS", "name": "Federal Funds Effective Rate"},
    "DGS10": {"id": "DGS10", "name": "10-Year Treasury Constant Maturity Rate"},
    "DGS2": {"id": "DGS2", "name": "2-Year Treasury Constant Maturity Rate"},
}

SUPPORTED_SERIES = list(SERIES_MAP.keys())

_last_request_time = 0.0


async def _rate_limit():
    global _last_request_time
    now = asyncio.get_event_loop().time()
    elapsed = now - _last_request_time
    if elapsed < 0.1:
        await asyncio.sleep(0.1 - elapsed)
    _last_request_time = asyncio.get_event_loop().time()


async def _fetch_with_retry(
    client: httpx.AsyncClient, url: str, params: dict, max_retries: int = 3
) -> Optional[dict]:
    for attempt in range(max_retries):
        try:
            await _rate_limit()
            r = await client.get(url, params=params, timeout=15)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 429:
                wait = 2 ** attempt
                await asyncio.sleep(wait)
                continue
            return None
        except (httpx.TimeoutException, httpx.RequestError):
            if attempt == max_retries - 1:
                return None
            await asyncio.sleep(2 ** attempt)
    return None


def _generate_mock_observations(series_id: str, limit: int) -> list[dict]:
    """Generate mock FRED observations when the API is unavailable."""
    base_values = {
        "GDP": 28000.0,
        "CPIAUCSL": 300.0,
        "UNRATE": 4.0,
        "FEDFUNDS": 5.25,
        "DGS10": 4.5,
        "DGS2": 4.8,
    }
    base = base_values.get(series_id, 100.0)
    observations = []
    today = datetime.now()
    for i in range(min(limit, 12)):
        date = today - timedelta(days=30 * i)
        val = base + (i * 0.1) - (i % 3) * 0.2
        observations.append({
            "date": date.strftime("%Y-%m-%d"),
            "value": round(val, 2),
        })
    return observations


def _fred_key_builder(func, args, kwargs):
    """Cache key for FRED - excludes api_key to avoid secret in key."""
    series_ids = kwargs.get("series_ids", args[0] if args else [])
    limit = kwargs.get("limit", args[2] if len(args) > 2 else 100)
    ids = ":".join(sorted(series_ids)) if isinstance(series_ids, list) else str(series_ids)
    return f"fred:{ids}:{limit}"


@cached(ttl=3600, key_builder=_fred_key_builder)
async def get_observations(series_ids: list[str], api_key: str, limit: int = 100) -> dict:
    if not api_key:
        return {
            "error": "FRED API key not configured. Set FRED_API_KEY in environment or use 'demo'.",
            "series": [],
        }

    results = []
    for sid in series_ids:
        sid = sid.upper().strip()
        if sid not in SERIES_MAP:
            results.append({
                "series_id": sid,
                "series_name": sid,
                "error": f"Unsupported series. Supported: {', '.join(SUPPORTED_SERIES)}",
                "observations": [],
            })
            continue

        series_info = SERIES_MAP[sid]
        url = f"{FRED_BASE}/series/observations"
        params = {
            "series_id": sid,
            "api_key": api_key,
            "file_type": "json",
            "sort_order": "desc",
            "limit": limit,
        }

        try:
            async with httpx.AsyncClient(timeout=15) as client:
                data = await _fetch_with_retry(client, url, params)
                if data is None:
                    results.append({
                        "series_id": sid,
                        "series_name": series_info["name"],
                        "observations": _generate_mock_observations(sid, limit),
                        "last_updated": datetime.now().isoformat(),
                        "source": "FRED (mock data)",
                        "note": "FRED API unavailable. Returning mock observations.",
                    })
                    continue

                obs = data.get("observations", [])
                observations = []
                for o in obs:
                    val = o.get("value", "")
                    if val and val != ".":
                        observations.append({
                            "date": o.get("date", ""),
                            "value": float(val),
                        })

                results.append({
                    "series_id": sid,
                    "series_name": series_info["name"],
                    "observations": observations,
                    "last_updated": datetime.now().isoformat(),
                    "source": "FRED",
                })

        except Exception as e:
            results.append({
                "series_id": sid,
                "series_name": series_info["name"],
                "observations": _generate_mock_observations(sid, limit),
                "last_updated": datetime.now().isoformat(),
                "source": "FRED (mock data)",
                "note": f"Error: {str(e)}. Returning mock observations.",
            })

    return {"series": results}
