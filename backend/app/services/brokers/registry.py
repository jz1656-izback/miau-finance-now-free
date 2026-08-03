import logging
from typing import Optional

from app.services.brokers.base import BrokerBase

logger = logging.getLogger(__name__)

_registry: dict[str, type[BrokerBase]] = {}


def register(name: str):
    def decorator(cls: type[BrokerBase]):
        _registry[name] = cls
        cls.name = name
        logger.info(f"Registered broker: {name}")
        return cls
    return decorator


def get_broker(name: str) -> Optional[type[BrokerBase]]:
    return _registry.get(name)


def list_brokers() -> list[dict[str, str]]:
    return [
        {"name": name, "display_name": cls.display_name or name}
        for name, cls in _registry.items()
    ]


def discover_brokers():
    _registry.clear()
    for module_name in ("alpaca", "ib", "saxo", "degiro", "rakuten", "zerodha"):
        try:
            __import__(f"app.services.brokers.{module_name}")
        except ImportError as e:
            logger.warning(f"Failed to load broker module {module_name}: {e}")
