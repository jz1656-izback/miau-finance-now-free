import importlib
import json
import logging
import math
import resource
import signal
import sys
import textwrap
import time
from typing import Any, Optional

logger = logging.getLogger(__name__)

SANDBOX_TIMEOUT_SECONDS = 5
SANDBOX_MAX_MEMORY_MB = 64
SANDBOX_MAX_OUTPUT_SIZE = 1024 * 100  # 100KB max output

SAFE_BUILTINS: dict[str, Any] = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "format": format,
    "frozenset": frozenset,
    "int": int,
    "isinstance": isinstance,
    "issubclass": issubclass,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "range": range,
    "repr": repr,
    "reversed": reversed,
    "round": round,
    "set": set,
    "slice": slice,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "type": type,
    "zip": zip,
    "True": True,
    "False": False,
    "None": None,
    "json": json,
    "math": math,
}

BLOCKED_MODULES = {
    "os", "subprocess", "sys", "shutil", "socket", "ctypes",
    "importlib", "inspect", "atexit", "code", "codeop",
    "compile", "compileall", "dis", "distutils",
    "email", "ftplib", "http", "imaplib", "nntplib",
    "poplib", "smtplib", "telnetlib", "urllib",
    "webbrowser", "antigravity", "pickle", "cPickle",
    "marshal", "shelve", "dbm", "sqlite3", "turtle",
    "tkinter", "wave", "audioop", "crypt",
}


class SandboxError(Exception):
    pass


class TimeoutError(SandboxError):
    pass


class MemoryLimitError(SandboxError):
    pass


class BlockedModuleError(SandboxError):
    pass


class SandboxResult:
    def __init__(
        self,
        success: bool,
        result: Any = None,
        error: Optional[str] = None,
        execution_time_ms: float = 0.0,
        output: str = "",
    ):
        self.success = success
        self.result = result
        self.error = error
        self.execution_time_ms = execution_time_ms
        self.output = output


class _SandboxScope:
    def __init__(self, api_context: Optional[dict] = None):
        self._api_context = api_context or {}
        self._call_count = 0
        self._max_calls = 50

    def api_call(self, endpoint: str, params: Optional[dict] = None) -> Any:
        self._call_count += 1
        if self._call_count > self._max_calls:
            raise SandboxError(f"API call limit exceeded ({self._max_calls} max)")
        apis = self._api_context.get("apis", {})
        handler = apis.get(endpoint)
        if not handler:
            raise SandboxError(f"Unknown API endpoint: {endpoint}")
        return handler(**(params or {}))

    def log(self, message: str) -> None:
        self._api_context.setdefault("_logs", []).append(str(message))


def _check_module_import(name: str, *args: Any, **kwargs: Any) -> Any:
    base = name.split(".")[0]
    if base in BLOCKED_MODULES:
        raise BlockedModuleError(f"Module '{name}' is not allowed in sandbox")
    return importlib.import_module(name, *args, **kwargs)


def _timeout_handler(signum: int, frame: Any) -> None:
    raise TimeoutError(f"Sandbox execution timed out after {SANDBOX_TIMEOUT_SECONDS}s")


def run_sandboxed(
    code: str,
    api_context: Optional[dict] = None,
    timeout: int = SANDBOX_TIMEOUT_SECONDS,
    max_memory_mb: int = SANDBOX_MAX_MEMORY_MB,
) -> SandboxResult:
    safe_builtins = dict(SAFE_BUILTINS)
    safe_builtins["__import__"] = _check_module_import
    scope = _SandboxScope(api_context)

    local_ns: dict[str, Any] = {
        "api": scope,
        "miau": scope,
    }

    global_ns: dict[str, Any] = {
        "__builtins__": safe_builtins,
        "__name__": "__miau_sandbox__",
    }

    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout)

    try:
        soft, hard = resource.getrlimit(resource.RLIMIT_AS)
        memory_bytes = max_memory_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, hard))
    except Exception as e:
        logger.warning("Failed to set sandbox memory limit: %s", e)

    start = time.time()
    try:
        compiled = compile(textwrap.dedent(code), "<sandbox>", "exec")
        exec(compiled, global_ns, local_ns)
        execution_time = (time.time() - start) * 1000

        result_value = local_ns.get("result", None)
        output_logs = scope._api_context.get("_logs", [])

        output_text = "\n".join(str(l) for l in output_logs)
        if len(output_text) > SANDBOX_MAX_OUTPUT_SIZE:
            output_text = output_text[:SANDBOX_MAX_OUTPUT_SIZE] + "\n... (truncated)"

        signal.alarm(0)
        return SandboxResult(
            success=True,
            result=result_value,
            execution_time_ms=round(execution_time, 1),
            output=output_text,
        )
    except TimeoutError as e:
        signal.alarm(0)
        return SandboxResult(success=False, error=str(e), execution_time_ms=(time.time() - start) * 1000)
    except BlockedModuleError as e:
        return SandboxResult(success=False, error=str(e), execution_time_ms=(time.time() - start) * 1000)
    except MemoryError:
        return SandboxResult(
            success=False,
            error=f"Sandbox exceeded memory limit ({max_memory_mb}MB)",
            execution_time_ms=(time.time() - start) * 1000,
        )
    except SyntaxError as e:
        return SandboxResult(success=False, error=f"Syntax error: {e}", execution_time_ms=0)
    except Exception as e:
        return SandboxResult(
            success=False,
            error=f"Sandbox error: {type(e).__name__}: {e}",
            execution_time_ms=(time.time() - start) * 1000,
        )
