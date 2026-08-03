"""Plugin loader — discover, validate, sandbox, and lifecycle management."""

import importlib
import importlib.util
import inspect
import logging
import os
import sys
from typing import Any, Optional

from app.services.plugin.spec import HookPoint, PluginBase, PluginMeta

logger = logging.getLogger(__name__)

PLUGIN_DIRS = [
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "plugins"),
    os.environ.get("MIAU_PLUGIN_DIR", ""),
]


class PluginValidationError(Exception):
    """Raised when a plugin fails validation."""


class PluginLoadError(Exception):
    """Raised when a plugin cannot be loaded."""


def _find_plugin_dirs() -> list[str]:
    dirs = [d for d in PLUGIN_DIRS if d and os.path.isdir(d)]
    if not dirs:
        default = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "plugins"))
        if os.path.isdir(default):
            dirs = [default]
    return dirs


def discover_plugins() -> list[dict[str, str]]:
    """Scan plugin directories and return metadata for each discovered plugin."""
    found: list[dict[str, str]] = []
    for plugin_dir in _find_plugin_dirs():
        for entry in sorted(os.listdir(plugin_dir)):
            plugin_path = os.path.join(plugin_dir, entry)
            if not os.path.isdir(plugin_path) or entry.startswith("_"):
                continue
            main_file = os.path.join(plugin_path, "main.py")
            if not os.path.isfile(main_file):
                continue
            meta = _peek_meta(plugin_path, entry)
            if meta:
                found.append(meta)
    return found


def _peek_meta(plugin_path: str, name: str) -> Optional[dict[str, str]]:
    """Try to extract plugin metadata without fully loading it."""
    try:
        spec = importlib.util.spec_from_file_location(
            f"_plugin_peek_{name}",
            os.path.join(plugin_path, "main.py"),
        )
        if not spec or not spec.loader:
            return None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for _, cls in inspect.getmembers(mod, inspect.isclass):
            if issubclass(cls, PluginBase) and cls is not PluginBase:
                meta = getattr(cls, "meta", None)
                if meta and isinstance(meta, PluginMeta):
                    return {
                        "name": meta.name or name,
                        "version": meta.version,
                        "description": meta.description,
                        "author": meta.author,
                        "hooks": [h.value for h in (meta.hooks or [])],
                        "path": plugin_path,
                    }
    except Exception as e:
        logger.debug("Failed to peek plugin %s: %s", name, e)
    return None


async def load_plugin(name: str) -> PluginBase:
    """Fully load a plugin by name, validate it, and return an instance."""
    for plugin_dir in _find_plugin_dirs():
        plugin_path = os.path.join(plugin_dir, name)
        main_file = os.path.join(plugin_path, "main.py")
        if not os.path.isfile(main_file):
            continue

        spec = importlib.util.spec_from_file_location(f"_plugin_{name}", main_file)
        if not spec or not spec.loader:
            raise PluginLoadError(f"Cannot load spec for plugin: {name}")

        mod = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = mod
        spec.loader.exec_module(mod)

        plugin_cls = None
        for _, cls in inspect.getmembers(mod, inspect.isclass):
            if issubclass(cls, PluginBase) and cls is not PluginBase:
                plugin_cls = cls
                break

        if not plugin_cls:
            raise PluginValidationError(f"No PluginBase subclass found in plugin: {name}")

        instance: PluginBase = plugin_cls()
        if not hasattr(instance, "meta") or not isinstance(instance.meta, PluginMeta):
            raise PluginValidationError(f"Plugin {name} must define a `meta` attribute of type PluginMeta")

        logger.info("Loaded plugin: %s v%s", instance.meta.name, instance.meta.version)
        return instance

    raise PluginLoadError(f"Plugin not found: {name}")


class PluginManager:
    """Manages the lifecycle of all loaded plugins."""

    def __init__(self):
        self._plugins: dict[str, PluginBase] = {}
        self._hook_registry: dict[HookPoint, list[PluginBase]] = {
            hook: [] for hook in HookPoint
        }

    @property
    def loaded_plugins(self) -> list[dict[str, str]]:
        return [
            {
                "name": p.meta.name,
                "version": p.meta.version,
                "description": p.meta.description,
                "author": p.meta.author,
            }
            for p in self._plugins.values()
        ]

    async def load(self, name: str) -> dict[str, str]:
        if name in self._plugins:
            return {"name": name, "status": "already_loaded"}
        plugin = await load_plugin(name)
        await plugin.initialize()
        self._plugins[name] = plugin
        for hook in plugin.meta.hooks or []:
            if hook in self._hook_registry:
                self._hook_registry[hook].append(plugin)
        logger.info("Plugin initialized: %s", plugin.meta.name)
        return {"name": plugin.meta.name, "version": plugin.meta.version, "status": "loaded"}

    async def unload(self, name: str) -> dict[str, str]:
        plugin = self._plugins.pop(name, None)
        if not plugin:
            return {"name": name, "status": "not_found"}
        await plugin.shutdown()
        for hook_list in self._hook_registry.values():
            hook_list[:] = [p for p in hook_list if p.meta.name != name]
        logger.info("Plugin unloaded: %s", name)
        return {"name": name, "status": "unloaded"}

    async def unload_all(self) -> None:
        for name in list(self._plugins.keys()):
            await self.unload(name)

    async def run_hook(self, hook: HookPoint, **kwargs: Any) -> list[Any]:
        results = []
        for plugin in self._hook_registry.get(hook, []):
            handler = getattr(plugin, hook.value, None)
            if handler:
                try:
                    result = await handler(**kwargs)
                    results.append(result)
                except Exception as e:
                    logger.error("Plugin hook error [%s/%s]: %s", plugin.meta.name, hook.value, e)
        return results

    async def shutdown(self) -> None:
        await self.unload_all()


_manager: Optional[PluginManager] = None


def get_manager() -> PluginManager:
    global _manager
    if _manager is None:
        _manager = PluginManager()
    return _manager
