"""Per-API-key request/response debug log.

Stores the last N requests per API key with timing, status, and error messages.
Useful for developer debugging and API analytics.
"""

import logging
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional

logger = logging.getLogger(__name__)

MAX_REQUESTS_PER_KEY = 100
MAX_ENTRIES = 10000

_logs: dict[str, deque[dict]] = defaultdict(lambda: deque(maxlen=MAX_REQUESTS_PER_KEY))
_total_entries = 0


@dataclass
class LogEntry:
    api_key_id: str
    method: str
    path: str
    status_code: int
    duration_ms: float
    timestamp: str
    ip: str = ""
    user_agent: str = ""
    error: str = ""


def record_request(
    api_key_id: str,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    ip: str = "",
    user_agent: str = "",
    error: str = "",
) -> None:
    global _total_entries
    entry = {
        "api_key_id": api_key_id,
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": round(duration_ms, 1),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ip": ip,
        "user_agent": user_agent,
        "error": error,
    }
    _logs[api_key_id].append(entry)
    _total_entries += 1
    if _total_entries > MAX_ENTRIES:
        _trim()


def _trim() -> None:
    global _total_entries
    while _total_entries > MAX_ENTRIES * 0.8:
        oldest_key = min(_logs.keys(), key=lambda k: _logs[k][0]["timestamp"] if _logs[k] else "")
        if oldest_key:
            removed = _logs[oldest_key].popleft() if _logs[oldest_key] else None
            if removed:
                _total_entries -= 1
            if not _logs[oldest_key]:
                del _logs[oldest_key]


def get_logs(api_key_id: Optional[str] = None, limit: int = 50, offset: int = 0) -> list[dict]:
    if api_key_id:
        entries = list(_logs.get(api_key_id, []))
    else:
        entries = []
        for key_queue in _logs.values():
            entries.extend(key_queue)
        entries.sort(key=lambda e: e["timestamp"], reverse=True)

    entries.reverse()
    total = len(entries)
    return entries[offset:offset + limit], total


def get_logs_for_key(api_key_id: str) -> list[dict]:
    return list(_logs.get(api_key_id, []))


def clear_logs(api_key_id: Optional[str] = None) -> int:
    global _total_entries
    if api_key_id:
        removed = len(_logs.pop(api_key_id, []))
        _total_entries -= removed
        return removed
    else:
        count = sum(len(q) for q in _logs.values())
        _logs.clear()
        _total_entries = 0
        return count


def get_stats() -> dict:
    key_count = len(_logs)
    total = _total_entries
    status_counts: dict[int, int] = {}
    for queue in _logs.values():
        for entry in queue:
            status_counts[entry["status_code"]] = status_counts.get(entry["status_code"], 0) + 1
    avg_duration = 0.0
    if total > 0:
        all_durations = [e["duration_ms"] for q in _logs.values() for e in q]
        avg_duration = sum(all_durations) / len(all_durations)
    return {
        "total_requests": total,
        "api_keys_tracked": key_count,
        "status_code_distribution": dict(sorted(status_counts.items())),
        "avg_duration_ms": round(avg_duration, 1),
    }
