"""Singleton registry for all data source providers."""
from __future__ import annotations
from typing import Optional
from app.services.data.base import DataSource


registry: "DataSourceRegistry" = None  # will be set below


class DataSourceRegistry:
    """Thread-safe singleton registry for DataSource providers.

    Providers register themselves by name. The registry provides
    lookup by name, capability, health status, etc.
    """

    _instance: Optional["DataSourceRegistry"] = None

    def __new__(cls) -> "DataSourceRegistry":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._providers: dict[str, DataSource] = {}
        return cls._instance

    def register(self, provider: DataSource) -> None:
        """Register a provider by its name. Overwrites existing."""
        self._providers[provider.name] = provider

    def get(self, name: str) -> Optional[DataSource]:
        """Get a provider by its unique name/slug."""
        return self._providers.get(name)

    def list(self) -> list[DataSource]:
        """List all registered providers."""
        return list(self._providers.values())

    def get_by_capability(self, capability: str) -> list[DataSource]:
        """Return all providers that support a given capability tag."""
        return [p for p in self._providers.values() if capability in p.capabilities]

    def health_all(self) -> dict[str, dict]:
        """Check health of all registered providers in parallel.

        Returns a dict mapping provider name to its health status dict.
        """
        import asyncio

        async def _check_all():
            results = {}
            for name, provider in self._providers.items():
                try:
                    status = await provider.health()
                    results[name] = status.model_dump()
                except Exception as e:
                    results[name] = {"provider": name, "healthy": False, "error": str(e)}
            return results

        return asyncio.run(_check_all())

    def count(self) -> int:
        return len(self._providers)


# Module-level singleton
registry = DataSourceRegistry()
