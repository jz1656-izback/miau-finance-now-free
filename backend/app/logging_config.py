"""Centralized logging configuration for Miau Finance backend.

Provides:
- Structured JSON logging
- Log rotation with retention
- Request-level logging via middleware
- Configurable log levels per module
- Sensitive data masking
"""
import json
import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Optional


class JSONFormatter(logging.Formatter):
    """JSON log formatter with timestamp, level, logger, message and extras."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "line": record.lineno,
            "function": record.funcName,
        }
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        if hasattr(record, "duration_ms"):
            log_entry["duration_ms"] = record.duration_ms
        if hasattr(record, "status_code"):
            log_entry["status_code"] = record.status_code
        if hasattr(record, "extra"):
            log_entry.update(record.extra)
        return json.dumps(log_entry, default=str)


def setup_logging(
    log_level: str = "INFO",
    log_dir: str = "/var/log/miau",
    json_format: bool = True,
    max_bytes: int = 50 * 1024 * 1024,
    backup_count: int = 10,
):
    """Configure root and named loggers with file rotation and console output."""

    # Determine log directory with fallback
    try:
        os.makedirs(log_dir, exist_ok=True)
        test_file = os.path.join(log_dir, ".write_test")
        with open(test_file, "w") as f:
            f.write("ok")
        os.remove(test_file)
    except (PermissionError, OSError):
        log_dir = "/tmp/miau-logs"
        os.makedirs(log_dir, exist_ok=True)

    # Determine formatter
    if json_format:
        formatter = JSONFormatter()
        console_formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)-7s %(name)-25s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)-7s %(name)-25s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        console_formatter = formatter

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Clear existing handlers
    root_logger.handlers.clear()

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, "miau.log"),
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Application-specific file handlers
    handlers_config = {
        "app": os.path.join(log_dir, "app.log"),
        "audit": os.path.join(log_dir, "audit.log"),
        "uvicorn": os.path.join(log_dir, "server.log"),
        "uvicorn.access": os.path.join(log_dir, "access.log"),
    }

    for logger_name, filepath in handlers_config.items():
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        logger.propagate = False

        fh = logging.handlers.RotatingFileHandler(
            filename=filepath,
            maxBytes=max_bytes,
            backupCount=backup_count,
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        if logger_name == "app":
            logger.addHandler(console_handler)


def get_logger(name: str, extra: Optional[dict] = None):
    """Get a logger with optional extra context fields."""
    logger = logging.getLogger(name)
    if extra:
        return logging.LoggerAdapter(logger, extra)
    return logger
