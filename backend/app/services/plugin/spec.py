"""Plugin API specification — hook points, lifecycle, and base class."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional


class HookPoint(str, Enum):
    """All extension points in the Miau Finance lifecycle."""
    ON_STARTUP = "on_startup"
    ON_SHUTDOWN = "on_shutdown"
    BEFORE_MARKET_DATA = "before_market_data"
    AFTER_MARKET_DATA = "after_market_data"
    BEFORE_ORDER = "before_order"
    AFTER_ORDER = "after_order"
    BEFORE_PORTFOLIO = "before_portfolio"
    AFTER_PORTFOLIO = "after_portfolio"
    ON_ANALYTICS = "on_analytics"
    ON_AI_ADVISOR = "on_ai_advisor"
    ON_ERROR = "on_error"
    CUSTOM = "custom"


@dataclass
class PluginMeta:
    """Metadata a plugin exposes via its `meta` attribute."""
    name: str
    version: str
    description: str = ""
    author: str = ""
    homepage: str = ""
    license: str = "Proprietary"
    hooks: list[HookPoint] = field(default_factory=list)
    permissions: list[str] = field(default_factory=lambda: ["market:read"])
    min_api_version: str = "0.12.0"


class PluginBase(ABC):
    """Base class all plugins must subclass."""

    meta: PluginMeta

    @abstractmethod
    async def initialize(self) -> None:
        """Called once when the plugin is loaded."""

    @abstractmethod
    async def shutdown(self) -> None:
        """Called when the plugin is unloaded or on app shutdown."""

    async def on_startup(self) -> None:
        """Hook: app startup."""

    async def on_shutdown(self) -> None:
        """Hook: app shutdown."""

    async def before_market_data(self, tickers: list[str], **kw: Any) -> list[str]:
        """Hook: transform/modify tickers before market data fetch."""
        return tickers

    async def after_market_data(self, data: dict[str, Any], **kw: Any) -> dict[str, Any]:
        """Hook: transform/enrich market data response."""
        return data

    async def before_order(self, order: dict[str, Any], **kw: Any) -> dict[str, Any]:
        """Hook: validate/modify order before submission."""
        return order

    async def after_order(self, result: dict[str, Any], **kw: Any) -> dict[str, Any]:
        """Hook: process order result after submission."""
        return result

    async def before_portfolio(self, portfolio_id: str, **kw: Any) -> str:
        return portfolio_id

    async def on_analytics(self, ticker: str, analytics: dict[str, Any], **kw: Any) -> dict[str, Any]:
        """Hook: enrich analytics results."""
        return analytics

    async def on_ai_advisor(self, query: str, context: dict[str, Any], **kw: Any) -> dict[str, Any]:
        """Hook: inject context into AI advisor prompts."""
        return context

    async def on_error(self, error: Exception, context: dict[str, Any], **kw: Any) -> Optional[dict[str, Any]]:
        """Hook: handle/log errors. Return a fallback response or None."""
        return None
