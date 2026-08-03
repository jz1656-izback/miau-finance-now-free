"""Plugin hooks dispatcher — routes lifecycle events to loaded plugins."""

import logging
import traceback
from typing import Any, Optional

from app.services.plugin.loader import load_plugin, get_manager
from app.services.plugin.spec import HookPoint, PluginBase

logger = logging.getLogger(__name__)


_hook_registry: dict[HookPoint, list[PluginBase]] = {}


def register_plugin(plugin: PluginBase) -> None:
    """Register a plugin's hook methods into the dispatch registry."""
    for hook in plugin.meta.hooks:
        if hook not in _hook_registry:
            _hook_registry[hook] = []
        _hook_registry[hook].append(plugin)
    logger.info("Registered plugin %s for %d hooks", plugin.meta.name, len(plugin.meta.hooks))


def unregister_plugin(plugin: PluginBase) -> None:
    """Remove a plugin from the hook registry."""
    for hook, plugins in list(_hook_registry.items()):
        _hook_registry[hook] = [p for p in plugins if p is not plugin]
        if not _hook_registry[hook]:
            del _hook_registry[hook]
    logger.info("Unregistered plugin %s", plugin.meta.name)


def clear_registry() -> None:
    _hook_registry.clear()


async def dispatch(
    hook: HookPoint,
    **kwargs: Any,
) -> list[dict[str, Any]]:
    """Dispatch a hook event to all registered plugins.

    Each plugin's corresponding hook method is called in registration order.
    If a plugin raises, the error is logged and the next plugin runs.
    Returns a list of result dicts, one per plugin that responded.
    """
    results: list[dict[str, Any]] = []
    plugins = _hook_registry.get(hook, [])
    if not plugins:
        return results

    method_name = hook.value

    for plugin in plugins:
        method = getattr(plugin, method_name, None)
        if method is None:
            continue
        try:
            result = await method(**kwargs)
            results.append({"plugin": plugin.meta.name, "hook": hook.value, "result": result})
        except Exception as e:
            logger.error(
                "Plugin %s hook %s failed: %s\n%s",
                plugin.meta.name, hook.value, e, traceback.format_exc(),
            )
            results.append({"plugin": plugin.meta.name, "hook": hook.value, "error": str(e)})

    return results


async def dispatch_chain(
    hook: HookPoint,
    initial_value: Any,
    **kwargs: Any,
) -> Any:
    """Dispatch a transforming hook where each plugin can modify a value.

    Each plugin receives the output of the previous plugin.
    Useful for hooks like ``before_market_data``, ``after_market_data``,
    ``before_order``, ``after_order``, etc.
    """
    value = initial_value
    plugins = _hook_registry.get(hook, [])

    for plugin in plugins:
        method = getattr(plugin, hook.value, None)
        if method is None:
            continue
        try:
            value = await method(value, **kwargs)
        except Exception as e:
            logger.error(
                "Plugin %s chain hook %s failed: %s\n%s",
                plugin.meta.name, hook.value, e, traceback.format_exc(),
            )
            # Continue chain with current value on error

    return value


async def reload_all_plugins() -> int:
    """Reload all plugins from disk and rebuild the hook registry."""
    clear_registry()
    count = 0
    for meta in get_manager().loaded_plugins():
        plugin = load_plugin(meta["name"])
        if plugin:
            register_plugin(plugin)
            count += 1
    logger.info("Reloaded %d plugins into hook registry", count)
    return count


def get_registered_hooks() -> dict[str, list[str]]:
    """Return a map of hook point → plugin names for introspection."""
    return {
        h.value: [p.meta.name for p in plugins]
        for h, plugins in _hook_registry.items()
    }
