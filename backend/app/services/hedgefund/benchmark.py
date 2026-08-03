"""Benchmark comparison — SPY, QQQ, and hedge fund indices."""

import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

BENCHMARKS = {
    "SPY": {"name": "S&P 500 ETF", "category": "equity"},
    "QQQ": {"name": "Nasdaq-100 ETF", "category": "equity"},
    "IWM": {"name": "Russell 2000 ETF", "category": "equity"},
    "AGG": {"name": "US Aggregate Bond ETF", "category": "fixed_income"},
    "GLD": {"name": "Gold ETF", "category": "commodity"},
    "HFRXGL": {"name": "HFRX Global Hedge Fund Index", "category": "hedge_fund"},
    "HFRXEH": {"name": "HFRX Equity Hedge Index", "category": "hedge_fund"},
    "HFRXMA": {"name": "HFRX Macro Index", "category": "hedge_fund"},
}


async def get_benchmarks(category: Optional[str] = None) -> list[dict]:
    result = []
    for ticker, info in BENCHMARKS.items():
        if category and info["category"] != category:
            continue
        result.append({"ticker": ticker, **info})
    return result


async def compare_to_benchmark(
    fund_returns: list[float],
    benchmark_ticker: str = "SPY",
) -> dict:
    import numpy as np
    fund_arr = np.array(fund_returns) if hasattr(np, 'array') else fund_returns
    benchmark_returns = await _fetch_benchmark_returns(benchmark_ticker)
    n = min(len(fund_returns), len(benchmark_returns))
    if n < 2:
        return {"error": "Insufficient data for comparison"}

    f = fund_returns[:n]
    b = benchmark_returns[:n]

    import numpy as _np
    f_arr = _np.array(f)
    b_arr = _np.array(b)
    excess = f_arr - b_arr
    tracking_error = float(_np.std(excess)) * _np.sqrt(252) if len(excess) > 1 else 0
    correlation = float(_np.corrcoef(f_arr, b_arr)[0, 1]) if len(f_arr) > 1 else 0
    alpha = float(_np.mean(excess)) * 252
    beta = float(_np.cov(f_arr, b_arr)[0, 1] / _np.var(b_arr)) if _np.var(b_arr) > 0 else 0

    return {
        "benchmark": benchmark_ticker,
        "periods": n,
        "fund_return_pct": round(float(_np.sum(f_arr)) * 100, 2),
        "benchmark_return_pct": round(float(_np.sum(b_arr)) * 100, 2),
        "excess_return_pct": round(float(_np.sum(excess)) * 100, 2),
        "alpha": round(alpha * 100, 2),
        "beta": round(beta, 3),
        "tracking_error": round(tracking_error * 100, 2),
        "correlation": round(correlation, 3),
        "information_ratio": round(alpha / tracking_error, 2) if tracking_error > 0 else 0,
    }


async def _fetch_benchmark_returns(ticker: str) -> list[float]:
    """Fetch historical returns for a benchmark ticker."""
    from app.services.analytics._yf import get_history
    records = await get_history(ticker, "1y")
    prices = [r["close"] for r in (records or []) if r.get("close")]
    return [(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))] if len(prices) > 1 else []
