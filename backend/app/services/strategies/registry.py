from typing import Any
from app.services.strategies.base import StrategyBase


_registry: dict[str, type[StrategyBase]] = {}


def register(name: str = ""):
    def decorator(cls: type[StrategyBase]) -> type[StrategyBase]:
        key = name or cls.name or cls.__name__
        _registry[key] = cls
        return cls
    return decorator


def get_strategy(name: str) -> type[StrategyBase]:
    if name not in _registry:
        raise ValueError(f"Unknown strategy: {name}. Available: {list_strategies()}")
    return _registry[name]


def list_strategies() -> list[dict[str, Any]]:
    result = []
    for name, cls in _registry.items():
        try:
            instance = cls()
            params = instance.get_params()
        except Exception:
            params = []
        result.append({"name": name, "description": cls.description, "version": cls.version, "params": params})
    return result


def discover_strategies() -> None:
    import importlib
    import pkgutil
    import app.services.strategies

    for _, name, _ in pkgutil.iter_modules(app.services.strategies.__path__):
        if name not in ("__init__", "base", "registry", "backtest"):
            importlib.import_module(f"app.services.strategies.{name}")
