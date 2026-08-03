"""Tests for plugin system."""
import pytest
from app.services.plugin.spec import HookPoint, PluginBase, PluginMeta


class _TestPlugin(PluginBase):
    meta = PluginMeta(name="test_plugin", version="1.0.0")
    async def initialize(self): pass
    async def shutdown(self): pass


def test_plugin_base():
    p = _TestPlugin()
    assert p.meta.name == "test_plugin"
    assert p.meta.version == "1.0.0"


def test_hook_points():
    assert HookPoint.ON_STARTUP.value == "on_startup"
    assert HookPoint.BEFORE_ORDER.value == "before_order"
    assert HookPoint.AFTER_MARKET_DATA.value == "after_market_data"
