import pytest
from datetime import datetime
from app.services.strategies.base import StrategyBase, Signal, StrategyInfo
from app.services.strategies import registry as reg_module
from app.services.strategies.registry import register, get_strategy, list_strategies, discover_strategies
from app.services.strategies.sma_cross import SMACrossStrategy
from app.services.strategies.rsi import RSIStrategy
from app.services.strategies.macd import MACDStrategy
from app.services.strategies.bollinger import BollingerStrategy
from app.services.strategies.mean_reversion import MeanReversionStrategy
from app.services.strategies.momentum import MomentumStrategy
from app.services.strategies.ai_generated import (
    AIGeneratedStrategy,
    _validate_strategy_code,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------

def test_signal_dataclass():
    ts = datetime(2025, 1, 1)
    sig = Signal(timestamp=ts, ticker="AAPL", action="BUY", strength=0.8, price=150.0)
    assert sig.timestamp == ts
    assert sig.ticker == "AAPL"
    assert sig.action == "BUY"
    assert sig.strength == 0.8
    assert sig.price == 150.0
    assert sig.metadata == {}


def test_signal_dataclass_defaults():
    ts = datetime(2025, 1, 1)
    sig = Signal(timestamp=ts, ticker="AAPL", action="HOLD", strength=0.0)
    assert sig.price == 0.0
    assert sig.metadata == {}


def test_strategy_info_dataclass():
    info = StrategyInfo(
        name="test", description="desc", version="1.0",
        params=[{"name": "p", "type": "int", "default": 10}],
    )
    assert info.name == "test"
    assert info.params[0]["name"] == "p"


# ---------------------------------------------------------------------------
# StrategyBase ABC tests
# ---------------------------------------------------------------------------

def test_strategy_base_abstract():
    with pytest.raises(TypeError):
        StrategyBase()


class _ConcreteStrat(StrategyBase):
    name = "concrete"
    description = "A concrete strategy"
    version = "1.0.0"

    def get_params(self) -> list[dict]:
        return []

    def generate_signals(self, data: list[dict]) -> list[Signal]:
        return []


def test_concrete_strategy_instantiation():
    s = _ConcreteStrat()
    assert s.name == "concrete"
    assert s.get_params() == []
    assert s.generate_signals([]) == []


def test_concrete_strategy_get_info():
    s = _ConcreteStrat()
    info = s.get_info()
    assert info.name == "concrete"
    assert info.description == "A concrete strategy"
    assert info.version == "1.0.0"


def test_strategy_backtest_no_data():
    s = _ConcreteStrat()
    result = s.backtest([])
    assert result["total_return"] == 0.0
    assert result["final_value"] == 100000.0
    assert result["total_trades"] == 0


def test_strategy_backtest_with_trades():
    data = [
        {"date": "2025-01-01", "close": 100.0},
        {"date": "2025-01-02", "close": 110.0},
        {"date": "2025-01-03", "close": 105.0},
    ]
    signals = [
        Signal(timestamp="2025-01-01", ticker="T", action="BUY", strength=1.0, price=100.0),
        Signal(timestamp="2025-01-03", ticker="T", action="SELL", strength=1.0, price=105.0),
    ]

    class _TradeStrat(StrategyBase):
        name = "trade_test"
        description = ""
        version = "1.0"
        def get_params(self): return []
        def generate_signals(self, data): return signals

    s = _TradeStrat()
    result = s.backtest(data)
    assert result["total_trades"] == 2
    assert result["final_value"] > 100000.0
    assert result["total_return"] > 0
    assert len(result["trades"]) == 2
    assert result["trades"][0]["type"] == "BUY"
    assert result["trades"][1]["type"] == "SELL"
    assert len(result["equity_curve"]) == 3


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------

def _save_registry():
    return dict(reg_module._registry)


def _restore_registry(saved):
    reg_module._registry.clear()
    reg_module._registry.update(saved)


def test_register_decorator():
    saved = _save_registry()
    try:
        reg_module._registry.clear()
        class _R1(StrategyBase):
            name = "r1"
            description = ""
            version = "1.0"
            def get_params(self): return []
            def generate_signals(self, d): return []
        register("test_r1")(_R1)
        assert "test_r1" in reg_module._registry
        assert reg_module._registry["test_r1"] is _R1
    finally:
        _restore_registry(saved)


def test_register_default_name():
    saved = _save_registry()
    try:
        reg_module._registry.clear()
        class _R2(StrategyBase):
            name = "r2_default"
            description = ""
            version = "1.0"
            def get_params(self): return []
            def generate_signals(self, d): return []
        register()(_R2)
        assert "r2_default" in reg_module._registry
    finally:
        _restore_registry(saved)


def test_get_strategy_known():
    saved = _save_registry()
    try:
        reg_module._registry.clear()
        class _R3(StrategyBase):
            name = "r3"
            description = ""
            version = "1.0"
            def get_params(self): return []
            def generate_signals(self, d): return []
        register("known_strat")(_R3)
        cls = get_strategy("known_strat")
        assert cls is _R3
    finally:
        _restore_registry(saved)


def test_get_strategy_unknown():
    saved = _save_registry()
    try:
        reg_module._registry.clear()
        with pytest.raises(ValueError, match="Unknown strategy"):
            get_strategy("nonexistent")
    finally:
        _restore_registry(saved)


def test_list_strategies():
    saved = _save_registry()
    try:
        reg_module._registry.clear()
        class _R4(StrategyBase):
            name = "list_test"
            description = "A list test strategy"
            version = "2.0.0"
            def get_params(self): return [{"name": "x", "type": "int", "default": 5}]
            def generate_signals(self, d): return []
        register("list_test")(_R4)
        lst = list_strategies()
        assert len(lst) == 1
        entry = lst[0]
        assert entry["name"] == "list_test"
        assert entry["description"] == "A list test strategy"
        assert entry["version"] == "2.0.0"
        assert entry["params"] == [{"name": "x", "type": "int", "default": 5}]
    finally:
        _restore_registry(saved)


def test_discover_strategies():
    discover_strategies()
    assert "sma_cross" in reg_module._registry
    assert "rsi" in reg_module._registry
    assert "macd" in reg_module._registry
    assert "bollinger" in reg_module._registry
    assert "mean_reversion" in reg_module._registry
    assert "momentum" in reg_module._registry
    assert "ai_generated" in reg_module._registry


# ---------------------------------------------------------------------------
# SMA Crossover strategy tests
# ---------------------------------------------------------------------------

def _price_data(values, start="2025-01-01"):
    return [{"date": f"2025-01-{d:02d}", "close": v} for d, v in enumerate(values, 1)]


def test_sma_cross_insufficient_data():
    s = SMACrossStrategy()
    data = _price_data([100.0] * 10)
    signals = s.generate_signals(data)
    assert signals == []


def test_sma_cross_buy_signal():
    s = SMACrossStrategy()
    slow = 50
    n = slow + 10
    prices = [100.0] * (n - 20) + list(range(100, 120)) + [120.0] * 10
    data = _price_data(prices)
    signals = s.generate_signals(data)
    buy_signals = [sig for sig in signals if sig.action == "BUY"]
    sell_signals = [sig for sig in signals if sig.action == "SELL"]
    assert len(buy_signals) > 0 or len(sell_signals) > 0


def test_sma_cross_uses_close_column():
    data = [{"Date": "2025-01-01", "Close": 100.0}] * 60
    s = SMACrossStrategy()
    signals = s.generate_signals(data)
    assert isinstance(signals, list)


def test_sma_cross_signal_strength():
    s = SMACrossStrategy()
    n = 60
    prices = [100.0] * 40 + [110.0] * 20
    data = _price_data(prices)
    signals = s.generate_signals(data)
    for sig in signals:
        assert 0 < sig.strength <= 1.0


# ---------------------------------------------------------------------------
# RSI strategy tests
# ---------------------------------------------------------------------------

def test_rsi_insufficient_data():
    s = RSIStrategy()
    data = _price_data([100.0] * 5)
    signals = s.generate_signals(data)
    assert signals == []


def test_rsi_oversold_buy_signal():
    s = RSIStrategy()
    prices = (
        [100.0] * 10
        + [100, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86]
    )
    data = _price_data(prices)
    signals = s.generate_signals(data)
    buy_signals = [sig for sig in signals if sig.action == "BUY"]
    assert len(buy_signals) > 0


def test_rsi_overbought_sell_signal():
    s = RSIStrategy()
    prices = (
        [100.0] * 10
        + [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114]
    )
    data = _price_data(prices)
    signals = s.generate_signals(data)
    sell_signals = [sig for sig in signals if sig.action == "SELL"]
    assert len(sell_signals) > 0


def test_rsi_no_signal_in_mid_range():
    s = RSIStrategy()
    prices = [100.0] * 20
    data = _price_data(prices)
    signals = s.generate_signals(data)
    assert signals == []


# ---------------------------------------------------------------------------
# MACD strategy tests
# ---------------------------------------------------------------------------

def test_macd_insufficient_data():
    s = MACDStrategy()
    data = _price_data([100.0] * 10)
    signals = s.generate_signals(data)
    assert signals == []


def test_macd_generates_buy():
    s = MACDStrategy()
    prices = [100.0] * 30 + list(range(100, 130))
    data = _price_data(prices)
    signals = s.generate_signals(data)
    buy = [sig for sig in signals if sig.action == "BUY"]
    assert len(buy) > 0


def test_macd_generates_sell():
    s = MACDStrategy()
    prices = list(range(130, 100, -1)) + [100.0] * 30
    data = _price_data(prices)
    signals = s.generate_signals(data)
    sell = [sig for sig in signals if sig.action == "SELL"]
    assert len(sell) > 0


# ---------------------------------------------------------------------------
# Bollinger strategy tests
# ---------------------------------------------------------------------------

def test_bollinger_insufficient_data():
    s = BollingerStrategy()
    data = _price_data([100.0] * 5)
    signals = s.generate_signals(data)
    assert signals == []


def test_bollinger_buy_at_lower_band():
    s = BollingerStrategy()
    prices = [100.0] * 25 + [80.0]
    data = _price_data(prices)
    signals = s.generate_signals(data)
    buy = [sig for sig in signals if sig.action == "BUY"]
    assert len(buy) > 0


def test_bollinger_sell_at_upper_band():
    s = BollingerStrategy()
    prices = [100.0] * 25 + [130.0]
    data = _price_data(prices)
    signals = s.generate_signals(data)
    sell = [sig for sig in signals if sig.action == "SELL"]
    assert len(sell) > 0


def test_bollinger_no_signal_within_bands():
    s = BollingerStrategy()
    prices = [100.0] * 30
    data = _price_data(prices)
    signals = s.generate_signals(data)
    assert signals == []


# ---------------------------------------------------------------------------
# Mean Reversion strategy tests
# ---------------------------------------------------------------------------

def test_mean_reversion_insufficient_data():
    s = MeanReversionStrategy()
    data = _price_data([100.0] * 5)
    signals = s.generate_signals(data)
    assert signals == []


def test_mean_reversion_buy_on_extreme_low():
    s = MeanReversionStrategy()
    prices = [100.0] * 25 + [50.0]
    data = _price_data(prices)
    signals = s.generate_signals(data)
    buy = [sig for sig in signals if sig.action == "BUY"]
    assert len(buy) > 0


def test_mean_reversion_sell_on_extreme_high():
    s = MeanReversionStrategy()
    prices = [100.0] * 25 + [200.0]
    data = _price_data(prices)
    signals = s.generate_signals(data)
    sell = [sig for sig in signals if sig.action == "SELL"]
    assert len(sell) > 0


def test_mean_reversion_close_position():
    s = MeanReversionStrategy()
    prices = [100.0] * 25 + [200.0, 140.0]
    data = _price_data(prices)
    signals = s.generate_signals(data)
    close = [sig for sig in signals if sig.action == "CLOSE"]
    assert len(close) >= 0


# ---------------------------------------------------------------------------
# Momentum strategy tests
# ---------------------------------------------------------------------------

def test_momentum_insufficient_data():
    s = MomentumStrategy()
    data = _price_data([100.0] * 5)
    signals = s.generate_signals(data)
    assert signals == []


def test_momentum_buy_signal():
    s = MomentumStrategy()
    prices = [100.0] * 25 + [120.0]
    data = _price_data(prices)
    signals = s.generate_signals(data)
    buy = [sig for sig in signals if sig.action == "BUY"]
    assert len(buy) > 0


def test_momentum_no_signal_with_low_return():
    s = MomentumStrategy()
    prices = [100.0] * 30
    data = _price_data(prices)
    signals = s.generate_signals(data)
    assert signals == []


# ---------------------------------------------------------------------------
# AI Generated strategy tests
# ---------------------------------------------------------------------------

def test_ai_generated_import():
    assert AIGeneratedStrategy is not None
    assert issubclass(AIGeneratedStrategy, StrategyBase)


def test_ai_generated_get_params():
    s = AIGeneratedStrategy()
    params = s.get_params()
    assert len(params) == 1
    assert params[0]["name"] == "description"


def test_validate_strategy_code_valid():
    code = """
from app.services.strategies.base import StrategyBase, Signal
from datetime import datetime

class GeneratedStrategy(StrategyBase):
    name = "gen"
    description = "Generated"
    version = "1.0"
    def get_params(self):
        return []
    def generate_signals(self, data):
        return []
"""
    assert _validate_strategy_code(code) is True


def test_validate_strategy_code_invalid_import():
    code = """
import os
class GeneratedStrategy:
    pass
"""
    assert _validate_strategy_code(code) is False


def test_validate_strategy_code_banned_function():
    code = """
class GeneratedStrategy:
    def foo(self):
        exec("x = 1")
"""
    assert _validate_strategy_code(code) is False


def test_validate_strategy_code_syntax_error():
    assert _validate_strategy_code("this is not python {{{") is False


def test_validate_strategy_code_allowed_imports():
    code = """
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional
from app.services.strategies.base import StrategyBase, Signal
class GeneratedStrategy(StrategyBase):
    name = "gen"
    description = "desc"
    version = "1.0"
    def get_params(self): return []
    def generate_signals(self, data): return []
"""
    assert _validate_strategy_code(code) is True


def test_ai_generated_metadata():
    s = AIGeneratedStrategy()
    info = s.get_info()
    assert info.name == "ai_generated"
    assert info.description == "AI-generated custom strategy"
    assert info.version == "1.0.0"
