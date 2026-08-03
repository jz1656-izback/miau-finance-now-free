import ast
import logging
import types
from typing import Any, Optional

from app.config import settings
from app.services.ai.client import AIClient
from app.services.strategies.base import Signal, StrategyBase
from app.services.strategies.registry import register

logger = logging.getLogger(__name__)

STRATEGY_GENERATION_PROMPT = """
You are a quantitative trading strategy generator. Given a natural language description and sample market data, generate a Python class that implements the strategy.

The class must:
- Be named `GeneratedStrategy`
- Inherit from `StrategyBase` with methods: `generate_signals(self, data: list[dict]) -> list[Signal]` and `get_params(self) -> list[dict]`
- Import `from app.services.strategies.base import StrategyBase, Signal`
- Import `from datetime import datetime`
- Be safe to execute (no imports beyond pandas, numpy, datetime)
- Handle edge cases (empty data, NaN values)

Each `Signal` has fields: timestamp (datetime), ticker (str), action (str: 'BUY'/'SELL'/'HOLD'), strength (float 0-1), price (float).

Return ONLY the Python code, no explanation.
"""


def _validate_strategy_code(code: str) -> bool:
    """Validate that generated strategy code is safe to execute.

    🔒 SECURITY (V7-004/H3): blocks dangerous calls both as attribute calls
    (``obj.exec(...)``) AND bare name calls (``exec(...)``, ``open(...)``),
    plus introspection primitives used to escape the exec sandbox.
    """
    _BLOCKED_CALLS = {"open", "exec", "eval", "__import__", "compile", "getattr", "setattr", "globals", "locals", "vars", "input"}
    _BLOCKED_ATTRS = {
        "_", "mro", "__subclasses__", "__bases__", "__class__", "__globals__",
        "__code__", "__builtins__", "__import__", "__loader__", "__spec__",
    }
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    # For `from X import Y`, the module root comes from node.module
                    # (alias.name is the imported symbol, not the module path).
                    module = node.module if isinstance(node, ast.ImportFrom) else alias.name
                    root = module.split(".")[0] if module else ""
                    if root not in {"pandas", "numpy", "pd", "np", "datetime", "typing", "app"}:
                        return False
            if isinstance(node, ast.Call):
                func = node.func
                # Attribute call: obj.open(...) / obj.__class__ / obj.__subclasses__()
                if isinstance(func, ast.Attribute):
                    if func.attr in _BLOCKED_CALLS or func.attr in _BLOCKED_ATTRS or func.attr.startswith("__"):
                        return False
                # Bare name call: exec(...) / open(...) / eval(...) / getattr(...)
                elif isinstance(func, ast.Name):
                    if func.id in _BLOCKED_CALLS:
                        return False
                # Subscript call: builtins.__dict__["exec"](...), globals()[...]
                elif isinstance(func, (ast.Subscript, ast.Call)):
                    return False
            # Block attribute access to dunder names on any object
            if isinstance(node, ast.Attribute):
                if node.attr.startswith("__") and node.attr.endswith("__"):
                    return False
        return True
    except SyntaxError:
        return False


@register("ai_generated")
class AIGeneratedStrategy(StrategyBase):
    name = "ai_generated"
    description = "AI-generated custom strategy"
    version = "1.0.0"

    def __init__(self, ai_client: Optional[AIClient] = None):
        super().__init__()
        self.ai_client = ai_client or AIClient(
            provider=settings.ai_provider or "openai",
            api_key=settings.ai_api_key or "",
            model=settings.ai_model or "gpt-4o-mini",
        )
        self._strategy_code: Optional[str] = None
        self._compiled_class: Optional[type] = None

    def get_params(self) -> list[dict[str, Any]]:
        return [
            {"name": "description", "type": "string", "default": "", "description": "Natural language strategy description"},
        ]

    async def generate_strategy(self, description: str, data_summary: Optional[str] = None) -> str:
        prompt = STRATEGY_GENERATION_PROMPT
        if data_summary:
            prompt += f"\n\nSample data summary: {data_summary}"
        prompt += f"\n\nStrategy description: {description}"

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Generate a trading strategy for: {description}"},
        ]

        response = await self.ai_client.chat(messages)
        code = response.get("content", "")

        code = code.strip()
        if "```python" in code:
            code = code.split("```python")[1]
        if "```" in code:
            code = code.split("```")[0]
        code = code.strip()

        if not _validate_strategy_code(code):
            raise ValueError("Generated strategy code failed validation")

        self._strategy_code = code
        return code

    def _compile_strategy(self) -> type:
        if not self._strategy_code:
            raise ValueError("No strategy code generated yet")
        module = types.ModuleType("generated_strategy")
        module.__dict__.update({
            "StrategyBase": StrategyBase,
            "Signal": Signal,
            "datetime": __import__("datetime", fromlist=["datetime"]).datetime,
        })
        exec(self._strategy_code, module.__dict__)
        cls = getattr(module, "GeneratedStrategy", None)
        if cls is None or not issubclass(cls, StrategyBase):
            raise ValueError("Generated code must define a 'GeneratedStrategy' class inheriting from StrategyBase")
        self._compiled_class = cls
        return cls

    def generate_signals(self, data: list[dict[str, Any]]) -> list[Signal]:
        if not self._compiled_class:
            self._compile_strategy()
        instance = self._compiled_class()
        return instance.generate_signals(data)

    async def execute(self, description: str, data: Optional[list[dict[str, Any]]] = None) -> dict[str, Any]:
        data_summary = None
        if data:
            closes = [r.get("close", 0) for r in data if r.get("close")]
            data_summary = f"Period: {len(data)} bars, price range: {min(closes):.2f}-{max(closes):.2f}"

        code = await self.generate_strategy(description, data_summary)
        cls = self._compile_strategy()

        result = {"strategy_code": code, "description": description, "status": "generated"}

        if data:
            instance = cls()
            signals = instance.generate_signals(data)
            backtest = instance.backtest(data) if hasattr(instance, "backtest") else None
            result["signals"] = [str(s) for s in signals]
            result["signals_count"] = len(signals)
            if backtest:
                result["backtest"] = backtest

        return result
