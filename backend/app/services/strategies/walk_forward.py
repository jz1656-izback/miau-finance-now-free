from dataclasses import dataclass, field
from typing import Any
from app.services.strategies.registry import discover_strategies, get_strategy


@dataclass
class WindowResult:
    window_index: int
    train_start: int
    train_end: int
    test_start: int
    test_end: int
    train_return: float
    test_return: float
    optimal_params: dict[str, Any] = field(default_factory=dict)
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0


@dataclass
class WalkForwardResult:
    strategy_name: str
    windows: list[WindowResult] = field(default_factory=list)
    avg_train_return: float = 0.0
    avg_test_return: float = 0.0
    stability_score: float = 0.0
    param_stability: dict[str, float] = field(default_factory=dict)


class WalkForwardOptimizer:
    def __init__(self, strategy_name: str, param_ranges: dict[str, list[Any]], n_windows: int = 5, train_pct: float = 0.7):
        discover_strategies()
        strategy_cls = get_strategy(strategy_name)
        self._strategy_cls = strategy_cls
        self.strategy_name = strategy_name
        self.param_ranges = param_ranges
        self.n_windows = n_windows
        self.train_pct = train_pct

    def _compute_metrics(self, data: list[dict], params: dict) -> dict:
        strategy = self._strategy_cls()
        for k, v in params.items():
            if hasattr(strategy, k):
                setattr(strategy, k, v)
        result = strategy.backtest(data)
        return result

    def _grid_search_params(self, data: list[dict]) -> tuple[dict[str, Any], dict]:
        best_return = -float("inf")
        best_params = {}
        best_metrics = {}

        def _iter_params(ranges: dict, current: dict, keys: list[str], idx: int):
            nonlocal best_return, best_params, best_metrics
            if idx == len(keys):
                metrics = self._compute_metrics(data, current)
                ret = metrics.get("total_return", -float("inf"))
                if ret > best_return:
                    best_return = ret
                    best_params = dict(current)
                    best_metrics = metrics
                return
            key = keys[idx]
            for val in ranges[key]:
                current[key] = val
                _iter_params(ranges, current, keys, idx + 1)

        _iter_params(self.param_ranges, {}, list(self.param_ranges.keys()), 0)
        return best_params, best_metrics

    def optimize(self, data: list[dict]) -> WalkForwardResult:
        n = len(data)
        window_size = n // self.n_windows
        results = []

        for w in range(self.n_windows):
            train_end = int((w + 1) * window_size * self.train_pct)
            test_end = (w + 1) * window_size
            if w == self.n_windows - 1:
                test_end = n
            train_data = data[:train_end]
            test_data = data[train_end:test_end]

            if len(train_data) < 20 or len(test_data) < 5:
                continue

            optimal_params, train_metrics = self._grid_search_params(train_data)

            test_strategy = self._strategy_cls()
            for k, v in optimal_params.items():
                if hasattr(test_strategy, k):
                    setattr(test_strategy, k, v)
            test_metrics = test_strategy.backtest(test_data)

            results.append(WindowResult(
                window_index=w,
                train_start=0,
                train_end=train_end,
                test_start=train_end,
                test_end=test_end,
                train_return=train_metrics.get("total_return", 0),
                test_return=test_metrics.get("total_return", 0),
                optimal_params=optimal_params,
            ))

        if not results:
            return WalkForwardResult(strategy_name=self.strategy_name)

        avg_train = sum(r.train_return for r in results) / len(results)
        avg_test = sum(r.test_return for r in results) / len(results)
        returns = [r.test_return for r in results]
        mean_r = sum(returns) / len(returns) if returns else 0
        var_r = sum((r - mean_r) ** 2 for r in returns) / len(returns) if returns else 0
        stability = 1.0 - min(1.0, var_r / 1000.0) if var_r < 1000 else 0.0

        param_keys = list(self.param_ranges.keys())
        param_stability = {}
        for pk in param_keys:
            vals = [r.optimal_params.get(pk) for r in results if pk in r.optimal_params]
            if vals and all(v == vals[0] for v in vals):
                param_stability[pk] = 1.0
            elif vals:
                try:
                    fvals = [float(v) for v in vals]
                    rng = max(fvals) - min(fvals)
                    total_rng = max(float(v) for v in self.param_ranges[pk]) - min(float(v) for v in self.param_ranges[pk])
                    param_stability[pk] = 1.0 - (rng / total_rng) if total_rng > 0 else 1.0
                except (ValueError, TypeError):
                    unique = len(set(str(v) for v in vals))
                    param_stability[pk] = 1.0 / unique if unique > 0 else 0.0
            else:
                param_stability[pk] = 0.0

        return WalkForwardResult(
            strategy_name=self.strategy_name,
            windows=results,
            avg_train_return=round(avg_train, 2),
            avg_test_return=round(avg_test, 2),
            stability_score=round(stability, 4),
            param_stability=param_stability,
        )
