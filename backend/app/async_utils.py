"""Async utilities — safe fire-and-forget tasks that never leak exceptions."""

import asyncio
import logging

logger = logging.getLogger(__name__)


def safe_task(coro, name: str = "unnamed") -> asyncio.Task:
    """Create a fire-and-forget task that logs exceptions instead of crashing.

    Without this, unhandled exceptions in asyncio.create_task() produce:
        "Future exception was never retrieved"

    Usage:
        safe_task(some_coro(), name="my task")
    """
    task = asyncio.create_task(coro, name=name)
    task.add_done_callback(_log_exception)
    return task


def _log_exception(task: asyncio.Task) -> None:
    if task.cancelled():
        return
    exc = task.exception()
    if exc:
        logger.error(
            "Unhandled exception in async task '%s': %s: %s",
            task.get_name(),
            type(exc).__name__,
            exc,
        )
