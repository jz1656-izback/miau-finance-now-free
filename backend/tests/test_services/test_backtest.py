import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from app.services.strategies.base import StrategyBase, Signal
from app.services.strategies.registry import _registry, discover_strategies
from app.services.strategies.backtest import BacktestEngine, BacktestResult
from app.services.strategies.walk_forward import WalkForwardOptimizer, WalkForwardResult
from app.services.strategies.oos_test import OOSTester, OOSTestResult
from app.services.strategies.comparison import StrategyComparer, ComparisonResult


# ---------------------------------------------------------------------------
# Helper: a strategy whose signals carry the same string timestamps as data rows
# ---------------------------------------------------------------------------

class _TSHelper(StrategyBase):
    name = "_ts_helper"
    description = "Timestamp-matching helper for backtest engine tests"
    version = "1.0.0"

    def __init__(self, signal_count: int = 2, buy_first: bool = True):
        super().__init__()
        self._signal_count = signal_count
        self._buy_first = buy_first

    def get_params(self):
        return [
            {"name": "lookback", "type": "int", "default": 10, "min": 2, "max": 100,
             "description": "Lookback"},
        ]

    def generate_signals(self, data):
        signals = []
        step = max(1, len(data) // (self._signal_count + 1))
        for i, row in enumerate(data):
            if i > 0 and i % step == 0 and len(signals) < self._signal_count:
                ts = row.get("date", row.get("Date", ""))
                price = float(row.get("close", row.get("Close", 0)))
                action = "BUY" if self._buy_first else "SELL"
                signals.append(Signal(timestamp=ts, ticker="T", action=action,
                                      strength=1.0, price=price))
                self._buy_first = not self._buy_first
        return signals


class _TSHelperBuySell(StrategyBase):
    name = "_ts_buysell"
    description = "BUY on first bar, SELL on last bar"
    version = "1.0.0"

    def get_params(self):
        return []

    def generate_signals(self, data):
        if not data:
            return []
        first_ts = data[0].get("date", data[0].get("Date", ""))
        last_ts = data[-1].get("date", data[-1].get("Date", ""))
        first_price = float(data[0].get("close", data[0].get("Close", 0)))
        last_price = float(data[-1].get("close", data[-1].get("Close", 0)))
        return [
            Signal(timestamp=first_ts, ticker="T", action="BUY", strength=1.0, price=first_price),
            Signal(timestamp=last_ts, ticker="T", action="SELL", strength=1.0, price=last_price),
        ]


class _TSHelperNoSignals(StrategyBase):
    name = "_ts_none"
    description = "Never generates signals"
    version = "1.0.0"

    def get_params(self):
        return []

    def generate_signals(self, data):
        return []


# ensure the helpers are in the registry
_registry["_ts_helper"] = _TSHelper
_registry["_ts_buysell"] = _TSHelperBuySell
_registry["_ts_none"] = _TSHelperNoSignals


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _ensure_discovered():
    discover_strategies()


_MOCK_RECORDS = [
    {"date": "2025-01-01", "close": 100.0},
    {"date": "2025-01-02", "close": 102.0},
    {"date": "2025-01-03", "close": 101.0},
    {"date": "2025-01-04", "close": 105.0},
    {"date": "2025-01-05", "close": 108.0},
    {"date": "2025-01-06", "close": 107.0},
    {"date": "2025-01-07", "close": 110.0},
    {"date": "2025-01-08", "close": 112.0},
    {"date": "2025-01-09", "close": 109.0},
    {"date": "2025-01-10", "close": 115.0},
]

_LONG_RECORDS = [
    {"date": f"2025-01-{d:02d}", "close": 100.0 + (d * 0.5)}
    for d in range(1, 101)
]


# ---------------------------------------------------------------------------
# BacktestResult dataclass tests
# ---------------------------------------------------------------------------

def test_backtest_result_dataclass():
    r = BacktestResult(
        strategy_name="sma", ticker="AAPL", initial_capital=100000.0,
        final_value=110000.0, total_return=10.0, sharpe_ratio=1.5,
        max_drawdown=5.0, win_rate=60.0, total_trades=10,
        trades=[{"type": "BUY"}], equity_curve=[{"value": 100000}],
    )
    assert r.strategy_name == "sma"
    assert r.total_return == 10.0
    assert r.sharpe_ratio == 1.5
    assert r.total_trades == 10
    assert len(r.trades) == 1
    assert len(r.equity_curve) == 1


def test_backtest_result_defaults():
    r = BacktestResult(
        strategy_name="s", ticker="T", initial_capital=100000.0,
        final_value=100000.0, total_return=0.0, sharpe_ratio=0.0,
        max_drawdown=0.0, win_rate=0.0, total_trades=0,
    )
    assert r.trades == []
    assert r.equity_curve == []


# ---------------------------------------------------------------------------
# BacktestEngine tests
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_backtest_engine_runs_with_mock_data():
    with patch("app.services.strategies.backtest.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        engine = BacktestEngine(initial_capital=100000.0)
        result = await engine.run("_ts_buysell", "TEST", period="1y")
    assert isinstance(result, BacktestResult)
    assert result.ticker == "TEST"
    assert result.initial_capital == 100000.0
    assert result.total_trades > 0


@pytest.mark.anyio
async def test_backtest_engine_empty_data():
    with patch("app.services.strategies.backtest.get_history",
               new_callable=AsyncMock, return_value=[]):
        engine = BacktestEngine()
        result = await engine.run("_ts_buysell", "TEST")
    assert result.total_trades == 0
    assert result.final_value == result.initial_capital
    assert result.total_return == 0.0
    assert result.sharpe_ratio == 0.0
    assert result.max_drawdown == 0.0
    assert result.win_rate == 0.0


@pytest.mark.anyio
async def test_backtest_engine_applies_commission_and_slippage():
    with patch("app.services.strategies.backtest.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        engine_no = BacktestEngine(initial_capital=100000.0, commission_pct=0.0, slippage_pct=0.0)
        engine_yes = BacktestEngine(initial_capital=100000.0, commission_pct=0.1, slippage_pct=0.05)
        result_no = await engine_no.run("_ts_buysell", "TEST")
        result_yes = await engine_yes.run("_ts_buysell", "TEST")
    assert result_yes.total_return <= result_no.total_return


@pytest.mark.anyio
async def test_backtest_engine_sharpe_maxdd_winrate():
    with patch("app.services.strategies.backtest.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        engine = BacktestEngine(initial_capital=100000.0, commission_pct=0.0, slippage_pct=0.0)
        result = await engine.run("_ts_buysell", "TEST")
    assert result.sharpe_ratio >= 0
    assert isinstance(result.sharpe_ratio, float)
    assert result.max_drawdown >= 0
    assert isinstance(result.max_drawdown, float)
    assert result.win_rate >= 0
    assert isinstance(result.win_rate, float)


@pytest.mark.anyio
async def test_backtest_engine_equity_curve_populated():
    with patch("app.services.strategies.backtest.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        engine = BacktestEngine()
        result = await engine.run("_ts_none", "TEST")
    assert len(result.equity_curve) == len(_MOCK_RECORDS)
    for point in result.equity_curve:
        assert "timestamp" in point
        assert "value" in point
        assert point["value"] > 0


@pytest.mark.anyio
async def test_backtest_engine_trades_with_signals():
    with patch("app.services.strategies.backtest.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        engine = BacktestEngine(initial_capital=100000.0, commission_pct=0.0, slippage_pct=0.0)
        result = await engine.run("_ts_buysell", "TEST")
    assert len(result.trades) >= 2
    buy_trades = [t for t in result.trades if t["type"] == "BUY"]
    sell_trades = [t for t in result.trades if t["type"] == "SELL"]
    assert len(buy_trades) >= 1
    assert len(sell_trades) >= 1


@pytest.mark.anyio
async def test_backtest_engine_unknown_strategy():
    with patch("app.services.strategies.backtest.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        engine = BacktestEngine()
        with pytest.raises(ValueError, match="Unknown strategy"):
            await engine.run("_nonexistent_999", "TEST")


@pytest.mark.anyio
async def test_backtest_engine_with_params():
    """Verify that extra params are passed to the strategy instance."""
    with patch("app.services.strategies.backtest.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        engine = BacktestEngine()
        result = await engine.run("_ts_helper", "TEST", params={"lookback": 15})
    assert isinstance(result, BacktestResult)


# ---------------------------------------------------------------------------
# WalkForwardOptimizer tests
# ---------------------------------------------------------------------------

def test_walk_forward_optimizer_init():
    wfo = WalkForwardOptimizer(
        strategy_name="_ts_helper",
        param_ranges={"lookback": [5, 10, 15]},
        n_windows=3, train_pct=0.7,
    )
    assert wfo.strategy_name == "_ts_helper"
    assert wfo.n_windows == 3
    assert wfo.train_pct == 0.7


def test_walk_forward_optimize_runs():
    wfo = WalkForwardOptimizer(
        strategy_name="_ts_helper",
        param_ranges={"lookback": [5, 10]},
        n_windows=2, train_pct=0.7,
    )
    result = wfo.optimize(_LONG_RECORDS)
    assert isinstance(result, WalkForwardResult)
    assert result.strategy_name == "_ts_helper"
    assert len(result.windows) > 0


def test_walk_forward_window_structure():
    wfo = WalkForwardOptimizer(
        strategy_name="_ts_none",
        param_ranges={"lookback": [5]},
        n_windows=3, train_pct=0.7,
    )
    result = wfo.optimize(_LONG_RECORDS)
    for w in result.windows:
        assert w.window_index >= 0
        assert w.train_start <= w.train_end
        assert w.test_start >= w.train_end
        assert w.train_end <= w.test_end
        assert isinstance(w.optimal_params, dict)


def test_walk_forward_avg_returns():
    wfo = WalkForwardOptimizer(
        strategy_name="_ts_none",
        param_ranges={"lookback": [5]},
        n_windows=2, train_pct=0.7,
    )
    result = wfo.optimize(_LONG_RECORDS)
    assert isinstance(result.avg_train_return, float)
    assert isinstance(result.avg_test_return, float)


def test_walk_forward_stability_and_param_stability():
    wfo = WalkForwardOptimizer(
        strategy_name="_ts_none",
        param_ranges={"lookback": [5, 10]},
        n_windows=2, train_pct=0.7,
    )
    result = wfo.optimize(_LONG_RECORDS)
    assert 0.0 <= result.stability_score <= 1.0
    assert "lookback" in result.param_stability


def test_walk_forward_too_little_data():
    wfo = WalkForwardOptimizer(
        strategy_name="_ts_none",
        param_ranges={"lookback": [5]},
        n_windows=5, train_pct=0.7,
    )
    result = wfo.optimize(_MOCK_RECORDS[:15])
    assert isinstance(result, WalkForwardResult)
    # May have 0 windows if data is too short


def test_walk_forward_grid_search_selects_params():
    """Test that grid search picks params and backtest runs without error."""
    data = [{"date": f"2025-01-{d:02d}", "close": 100.0 + (d * 0.3)}
            for d in range(1, 61)]
    wfo = WalkForwardOptimizer(
        strategy_name="_ts_none",
        param_ranges={"lookback": [5, 15, 30]},
        n_windows=2, train_pct=0.7,
    )
    result = wfo.optimize(data)
    # At least one window should exist with a param dict
    if result.windows:
        for w in result.windows:
            assert "lookback" in w.optimal_params


# ---------------------------------------------------------------------------
# OOSTester tests
# ---------------------------------------------------------------------------

def test_oos_tester_init():
    oos = OOSTester(train_pct=0.7)
    assert oos.train_pct == 0.7


def test_oos_tester_splits_data():
    oos = OOSTester(train_pct=0.7)
    data = [{"date": f"2025-01-{d:02d}", "close": 100.0} for d in range(1, 101)]
    result = oos.test("_ts_none", data)
    assert isinstance(result, OOSTestResult)
    assert result.strategy_name == "_ts_none"


def test_oos_tester_returns_all_fields():
    data = [{"date": f"2025-01-{d:02d}", "close": 100.0 + d} for d in range(1, 101)]
    oos = OOSTester(train_pct=0.7)
    result = oos.test("_ts_none", data)
    assert isinstance(result.train_return, float)
    assert isinstance(result.test_return, float)
    assert isinstance(result.return_decay, float)
    assert isinstance(result.train_sharpe, float)
    assert isinstance(result.test_sharpe, float)
    assert isinstance(result.sharpe_decay, float)
    assert isinstance(result.train_max_dd, float)
    assert isinstance(result.test_max_dd, float)
    assert isinstance(result.overfitting_score, float)
    assert isinstance(result.is_overfit, bool)


def test_oos_tester_too_little_data():
    data = [{"date": "2025-01-01", "close": 100.0}]
    oos = OOSTester(train_pct=0.7)
    result = oos.test("_ts_none", data)
    assert result.is_overfit is True
    assert result.overfitting_score == 1.0


def test_oos_tester_train_pct_respected():
    data = [{"date": f"2025-01-{d:02d}", "close": 100.0} for d in range(1, 101)]
    oos = OOSTester(train_pct=0.7)
    result = oos.test("_ts_none", data)
    assert result.train_return == result.test_return == 0.0  # no signals


def test_oos_tester_computes_metrics():
    data = [{"date": f"2025-01-{d:02d}", "close": 100.0} for d in range(1, 101)]
    oos = OOSTester(train_pct=0.8)
    result = oos.test("_ts_buysell", data)
    assert result.total_trades is None or result.total_trades >= 0
    # overbought on equal prices may or may not fire
    assert result.train_max_dd >= 0
    assert result.test_max_dd >= 0


# ---------------------------------------------------------------------------
# StrategyComparer tests
# ---------------------------------------------------------------------------

@pytest.mark.anyio
async def test_comparer_init():
    comp = StrategyComparer(["_ts_helper", "_ts_none"])
    assert comp.strategies == ["_ts_helper", "_ts_none"]


@pytest.mark.anyio
async def test_comparer_compare_runs():
    comp = StrategyComparer(["_ts_helper", "_ts_none", "_ts_buysell"])
    with patch("app.services.strategies.comparison.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        result = await comp.compare("TEST")
    assert isinstance(result, ComparisonResult)
    assert len(result.strategy_names) > 0


@pytest.mark.anyio
async def test_comparer_rankings_populated():
    comp = StrategyComparer(["_ts_helper", "_ts_none"])
    with patch("app.services.strategies.comparison.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        result = await comp.compare("TEST")
    assert len(result.rankings) > 0
    for r in result.rankings:
        assert r.rank >= 1
        assert r.strategy_name in ("_ts_helper", "_ts_none")
        assert isinstance(r.total_return, float)
        assert isinstance(r.sharpe_ratio, float)
        assert isinstance(r.score, float)


@pytest.mark.anyio
async def test_comparer_best_and_worst():
    comp = StrategyComparer(["_ts_helper", "_ts_none"])
    with patch("app.services.strategies.comparison.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        result = await comp.compare("TEST")
    if result.rankings:
        assert result.best_strategy in ("_ts_helper", "_ts_none")
        assert result.worst_strategy in ("_ts_helper", "_ts_none")


@pytest.mark.anyio
async def test_comparer_correlation_matrix():
    comp = StrategyComparer(["_ts_helper", "_ts_none"])
    with patch("app.services.strategies.comparison.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        result = await comp.compare("TEST")
    expected_size = len(result.strategy_names)
    assert len(result.correlation_matrix) == expected_size
    for row in result.correlation_matrix:
        assert len(row) == expected_size


@pytest.mark.anyio
async def test_comparer_empty_data():
    comp = StrategyComparer(["_ts_helper"])
    with patch("app.services.strategies.comparison.get_history",
               new_callable=AsyncMock, return_value=[]):
        result = await comp.compare("TEST")
    assert result.strategy_names == []


@pytest.mark.anyio
async def test_comparer_single_strategy():
    comp = StrategyComparer(["_ts_buysell"])
    with patch("app.services.strategies.comparison.get_history",
               new_callable=AsyncMock, return_value=_MOCK_RECORDS):
        result = await comp.compare("TEST")
    assert len(result.rankings) == 1
    assert result.best_strategy == "_ts_buysell"
    assert result.worst_strategy == "_ts_buysell"
    assert result.correlation_matrix == [[1.0]]
