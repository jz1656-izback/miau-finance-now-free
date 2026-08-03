"""Log viewer API — serves log files to the log dashboard."""
import os
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException
from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/logs", tags=["Logs"])

LOG_DIRS = [
    os.getenv("LOG_DIR", "/var/log/miau"),
    "/tmp/miau-logs",
]

LOG_FILES = {
    "all": "miau.log",
    "app": "app.log",
    "audit": "audit.log",
    "server": "server.log",
    "access": "access.log",
}


@router.get("/files")
async def list_log_files(user: dict = Depends(get_current_user)):
    """List available log files with sizes and modification times."""
    files = []
    for log_dir in LOG_DIRS:
        if not os.path.isdir(log_dir):
            continue
        for key, filename in LOG_FILES.items():
            filepath = os.path.join(log_dir, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    "key": key,
                    "name": filename,
                    "path": filepath,
                    "size_bytes": stat.st_size,
                    "size_display": _fmt_size(stat.st_size),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "lines": _count_lines(filepath, 50000),
                })
    if not files:
        raise HTTPException(404, "No log files found. Is logging configured?")
    return {"files": files, "log_dir": next((d for d in LOG_DIRS if os.path.isdir(d)), None)}


@router.get("/tail/{log_key}")
async def tail_log(
    log_key: str,
    lines: int = Query(100, ge=10, le=5000, description="Number of lines to return"),
    level: str = Query("", description="Filter by level: ERROR, WARN, INFO, DEBUG"),
    search: str = Query("", description="Search string filter"),
    since: str = Query("", description="Only show entries after ISO timestamp"),
    user: dict = Depends(get_current_user),
):
    """Tail a log file with optional filtering."""
    if log_key not in LOG_FILES:
        raise HTTPException(400, f"Unknown log file: {log_key}. Options: {', '.join(LOG_FILES.keys())}")

    filepath = None
    for log_dir in LOG_DIRS:
        candidate = os.path.join(log_dir, LOG_FILES[log_key])
        if os.path.isfile(candidate):
            filepath = candidate
            break

    if not filepath:
        raise HTTPException(404, f"Log file '{LOG_FILES[log_key]}' not found")

    try:
        with open(filepath, "r") as f:
            all_lines = f.readlines()
    except Exception as e:
        raise HTTPException(500, f"Cannot read log file: {e}")

    # Parse and filter
    result = []
    level_upper = level.upper() if level else ""
    search_lower = search.lower() if search else ""
    since_dt = None
    if since:
        try:
            since_dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
        except ValueError:
            pass

    for line in reversed(all_lines):
        line = line.rstrip("\n")
        if not line:
            continue

        entry = _parse_log_line(line)

        # Filter by level
        if level_upper and entry.get("level", "").upper() != level_upper:
            continue

        # Filter by search
        if search_lower and search_lower not in line.lower():
            continue

        # Filter by timestamp
        if since_dt and entry.get("timestamp"):
            try:
                ts = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                if ts < since_dt:
                    continue
            except ValueError:
                pass

        result.append(entry)
        if len(result) >= lines:
            break

    return {
        "file": LOG_FILES[log_key],
        "total_lines": len(all_lines),
        "returned": len(result),
        "entries": result,
    }


@router.get("/stats")
async def log_stats(user: dict = Depends(get_current_user)):
    """Return log statistics: count by level for each log file."""
    stats = {}
    for log_key in LOG_FILES:
        filepath = None
        for log_dir in LOG_DIRS:
            candidate = os.path.join(log_dir, LOG_FILES[log_key])
            if os.path.isfile(candidate):
                filepath = candidate
                break
        if not filepath:
            continue

        counts = {"ERROR": 0, "WARNING": 0, "INFO": 0, "DEBUG": 0}
        try:
            with open(filepath, "r") as f:
                for line in f:
                    entry = _parse_log_line(line.rstrip())
                    lvl = entry.get("level", "").upper()
                    if lvl in counts:
                        counts[lvl] += 1
        except Exception:
            pass

        stats[log_key] = {
            "name": LOG_FILES[log_key],
            "counts": counts,
            "total": sum(counts.values()),
        }

    return {"stats": stats}


@router.get("/stream")
async def stream_logs(
    log_key: str = Query("app"),
    user: dict = Depends(get_current_user),
):
    """SSE endpoint for real-time log streaming (fallback: returns last 10 entries)."""
    filepath = None
    for log_dir in LOG_DIRS:
        candidate = os.path.join(log_dir, LOG_FILES.get(log_key, "app.log"))
        if os.path.isfile(candidate):
            filepath = candidate
            break

    if not filepath:
        raise HTTPException(404, "Log file not found")

    try:
        with open(filepath, "r") as f:
            all_lines = f.readlines()
    except Exception as e:
        raise HTTPException(500, str(e))

    entries = []
    for line in all_lines[-10:]:
        line = line.rstrip("\n")
        if line:
            entries.append(_parse_log_line(line))

    return {"entries": entries, "file": LOG_FILES.get(log_key, "app.log")}


def _parse_log_line(line: str) -> dict:
    """Parse a log line, trying JSON first, then plain text."""
    if line.startswith("{"):
        try:
            import json
            return json.loads(line)
        except json.JSONDecodeError:
            pass

    # Plain text log parsing
    entry = {"raw": line, "level": "INFO", "timestamp": "", "logger": "", "message": line}

    # Try to extract structured fields from common log formats
    # Format: [timestamp] LEVEL    logger    message
    import re
    m = re.match(r"\[(.*?)\]\s+(\w+)\s+(\S+)\s+(.*)", line)
    if m:
        entry["timestamp"] = m.group(1)
        entry["level"] = m.group(2)
        entry["logger"] = m.group(3)
        entry["message"] = m.group(4)
    else:
        # Try: LEVEL:message
        m2 = re.match(r"(\w+):\s*(.*)", line)
        if m2:
            entry["level"] = m2.group(1)
            entry["message"] = m2.group(2)

    return entry


def _fmt_size(bytes: int) -> str:
    if bytes >= 1024 * 1024:
        return f"{bytes / (1024 * 1024):.1f} MB"
    if bytes >= 1024:
        return f"{bytes / 1024:.1f} KB"
    return f"{bytes} B"


def _count_lines(filepath: str, max_lines: int = 50000) -> int:
    try:
        with open(filepath, "r") as f:
            for i, _ in enumerate(f):
                if i >= max_lines:
                    return max_lines + 1
            return i + 1
    except Exception:
        return 0
