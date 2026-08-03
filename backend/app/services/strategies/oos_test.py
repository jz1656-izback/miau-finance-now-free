from typing import Any
from dataclasses import dataclass
from app.services.strategies.registry import discover_strategies, get_strategy


@dataclass
class OOSTestResult:
    strategy_name: str
    train_return: float
    test_return: float
    return_decay: float
    train_sharpe: float
    test_sharpe: float
    sharpe_decay: float
    train_max_dd: float
    test_max_dd: float
    overfitting_score: float
    is_overfit: bool


class OOSTester:
    def __init__(self, train_pct: float = 0.7):
        self.train_pct = train_pct

    def _compute_stats(self, data: list[dict], strategy) -> dict:
        result = strategy.backtest(data)
        trades = result.get("trades", [])
        equity_curve = result.get("equity_curve", [])
        total_return = result.get("total_return", 0)
        total_trades = result.get("total_trades", 0)

        daily_returns = []
        peak = 100000.0
        max_dd = 0.0
        for i, point in enumerate(equity_curve):
            val = point.get("value", 100000.0)
            if val > peak:
                peak = val
            dd = (peak - val) / peak * 100 if peak > 0 else 0
            if dd > max_dd:
                max_dd = dd
            if i > 0:
                prev = equity_curve[i - 1].get("value", 100000.0)
                daily_returns.append((val - prev) / prev if prev > 0 else 0)

        n = len(daily_returns)
        avg_ret = sum(daily_returns) / n if n > 0 else 0
        std_ret = (sum((r - avg_ret) ** 2 for r in daily_returns) / n) ** 0.5 if n > 0 else 0
        sharpe = (avg_ret / std_ret * (252 ** 0.5)) if std_ret > 0 else 0

        return {
            "total_return": total_return,
            "sharpe_ratio": round(sharpe, 4),
            "max_drawdown": round(max_dd, 2),
            "total_trades": total_trades,
        }

    def test(self, strategy_name: str, data: list[dict]) -> OOSTestResult:
        discover_strategies()
        strategy_cls = get_strategy(strategy_name)

        split = int(len(data) * self.train_pct)
        train_data = data[:split]
        test_data = data[split:]

        if len(train_data) < 20 or len(test_data) < 5:
            return OOSTestResult(
                strategy_name=strategy_name,
                train_return=0, test_return=0, return_decay=0,
                train_sharpe=0, test_sharpe=0, sharpe_decay=0,
                train_max_dd=0, test_max_dd=0,
                overfitting_score=1.0, is_overfit=True,
            )

        train_strategy = strategy_cls()
        train_stats = self._compute_stats(train_data, train_strategy)

        test_strategy = strategy_cls()
        test_stats = self._compute_stats(test_data, test_strategy)

        return_decay = train_stats["total_return"] - test_stats["total_return"]
        sharpe_decay = train_stats["sharpe_ratio"] - test_stats["sharpe_ratio"]

        norm_return = abs(train_stats["total_return"]) + abs(test_stats["total_return"])
        overfit_score = 0.0
        if norm_return > 0:
            gap = abs(train_stats["total_return"] - test_stats["total_return"])
            overfit_score = min(1.0, gap / max(norm_return, 0.01))

        is_overfit = (
            overfit_score > 0.5
            or (train_stats["total_return"] > 5 and test_stats["total_return"] < -5)
            or (train_stats["sharpe_ratio"] > 1.5 and test_stats["sharpe_ratio"] < 0)
        )

        return OOSTestResult(
            strategy_name=strategy_name,
            train_return=round(train_stats["total_return"], 2),
            test_return=round(test_stats["total_return"], 2),
            return_decay=round(return_decay, 2),
            train_sharpe=train_stats["sharpe_ratio"],
            test_sharpe=test_stats["sharpe_ratio"],
            sharpe_decay=round(sharpe_decay, 4),
            train_max_dd=train_stats["max_drawdown"],
            test_max_dd=test_stats["max_drawdown"],
            overfitting_score=round(overfit_score, 4),
            is_overfit=is_overfit,
        )
