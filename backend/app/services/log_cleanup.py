"""Log retention: clean up old log files based on age and size."""
import os
import logging
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Default: keep logs for 30 days, max 500MB total
DEFAULT_MAX_AGE_DAYS = 30
DEFAULT_MAX_SIZE_MB = 500


def cleanup_logs(
    log_dir: str = None,
    max_age_days: int = DEFAULT_MAX_AGE_DAYS,
    max_size_mb: int = DEFAULT_MAX_SIZE_MB,
):
    """Remove rotated log files older than max_age_days.
    
    Rotated files follow the pattern: app.log.1, app.log.2.gz, etc.
    """
    if log_dir is None:
        log_dir = os.getenv("LOG_DIR", "/var/log/miau")
    
    if not os.path.isdir(log_dir):
        logger.warning("Log directory %s does not exist", log_dir)
        return 0
    
    cutoff = datetime.now() - timedelta(days=max_age_days)
    removed = 0
    
    for fname in os.listdir(log_dir):
        fpath = os.path.join(log_dir, fname)
        if not os.path.isfile(fpath):
            continue
        
        # Skip current log files (no numeric suffix)
        base, ext = os.path.splitext(fname)
        if ext in (".log",) and not any(c.isdigit() for c in base):
            continue
        
        try:
            mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
            if mtime < cutoff:
                os.remove(fpath)
                removed += 1
                logger.info("Removed old log: %s (last modified: %s)", fname, mtime.date())
        except Exception as e:
            logger.warning("Failed to remove %s: %s", fname, e)
    
    # Check total size
    total_size = sum(os.path.getsize(os.path.join(log_dir, f))
                     for f in os.listdir(log_dir)
                     if os.path.isfile(os.path.join(log_dir, f)))
    total_mb = total_size / (1024 * 1024)
    if total_mb > max_size_mb:
        logger.info("Total log size %.1f MB exceeds limit %d MB", total_mb, max_size_mb)
    
    return removed
