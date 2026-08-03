"""
Risk analytics — accelerated by Rust when available.
"""

from __future__ import annotations

import numpy as np

try:
    from miau_analytics._core import historical_var as _rust_hist_var
    from miau_analytics._core import compute_beta as _rust_beta
    from miau_analytics._core import stress_scenario as _rust_stress

    _HAS_RUST = True
except ImportError:
    _HAS_RUST = False


def compute_historical_var(prices: np.ndarray, confidence: float = 0.95) -> dict:
    """Compute historical VaR and CVaR from a price series.

    Parameters
    ----------
    prices : ndarray
        1-D array of closing prices.
    confidence : float
        Confidence level (default 0.95).

    Returns
    -------
    dict with var, cvar, confidence.
    """
    if _HAS_RUST:
        import miau_analytics._core as _rust

        var, cvar = _rust.historical_var(prices, confidence)
        return {
            "var": round(float(var), 4),
            "cvar": round(float(cvar), 4),
            "confidence": confidence,
        }

    returns = np.diff(np.log(prices))
    if len(returns) == 0:
        return {"var": 0.0, "cvar": 0.0, "confidence": confidence}

    var = float(np.percentile(returns, (1 - confidence) * 100))
    tail = returns[returns <= var]
    cvar = float(np.mean(tail)) if len(tail) > 0 else var
    return {
        "var": round(var, 4),
        "cvar": round(cvar, 4),
        "confidence": confidence,
    }


def compute_beta(
    stock_prices: np.ndarray,
    benchmark_prices: np.ndarray,
) -> dict:
    """Compute Beta, Alpha, and Correlation vs a benchmark.

    Parameters
    ----------
    stock_prices : ndarray
    benchmark_prices : ndarray

    Returns
    -------
    dict with beta, alpha, correlation.
    """
    if _HAS_RUST:
        import miau_analytics._core as _rust

        beta, alpha, corr = _rust.compute_beta(stock_prices, benchmark_prices)
        return {
            "beta": round(float(beta), 4),
            "alpha": round(float(alpha), 6),
            "correlation": round(float(corr), 4),
        }

    s_ret = np.diff(np.log(stock_prices))
    b_ret = np.diff(np.log(benchmark_prices))
    min_len = min(len(s_ret), len(b_ret))
    if min_len < 2:
        return {"beta": 1.0, "alpha": 0.0, "correlation": 0.0}

    s_ret = s_ret[:min_len]
    b_ret = b_ret[:min_len]

    cov = np.cov(s_ret, b_ret)[0, 1]
    var_b = np.var(b_ret, ddof=1)
    beta = cov / var_b if var_b > 1e-12 else 1.0
    alpha = np.mean(s_ret) - beta * np.mean(b_ret)
    corr = np.corrcoef(s_ret, b_ret)[0, 1] if len(s_ret) > 1 else 0.0

    return {
        "beta": round(float(beta), 4),
        "alpha": round(float(alpha), 6),
        "correlation": round(float(corr), 4),
    }


def run_stress_scenario(
    current_price: float,
    shocks: list[float] | None = None,
    scenario_names: list[str] | None = None,
) -> list[dict]:
    """Apply stress scenario shocks to a price.

    Parameters
    ----------
    current_price : float
    shocks : list of float, optional
        Percentage shocks (e.g. -0.20 for -20%). Defaults to 7 standard scenarios.
    scenario_names : list of str, optional

    Returns
    -------
    list of dict with name, shocked_price, change_pct, label.
    """
    if shocks is None:
        shocks = [-0.45, -0.30, -0.20, -0.10, -0.05, 0.05, 0.10]

    if scenario_names is None:
        scenario_names = [
            "2008 Financial Crisis",
            "COVID-19 Crash",
            "2022 Rate Hike",
            "Flash Crash",
            "Moderate Correction",
            "Bull Rally",
            "Mild Uptrend",
        ]

    if len(shocks) != len(scenario_names):
        scenario_names = [f"Scenario {i+1}" for i in range(len(shocks))]

    if _HAS_RUST:
        import miau_analytics._core as _rust

        results = _rust.stress_scenario(current_price, shocks, scenario_names)
        return [
            {"name": name, "shocked_price": round(price, 2), "change_pct": round(chg, 2), "label": label}
            for name, price, chg, label in results
        ]

    results = []
    for shock, name in zip(shocks, scenario_names):
        shocked_price = current_price * (1.0 + shock)
        change_pct = shock * 100.0
        label = f"{change_pct:+.1f}% (${shocked_price:.2f})"
        results.append({
            "name": name,
            "shocked_price": round(float(shocked_price), 2),
            "change_pct": round(float(change_pct), 2),
            "label": label,
        })
    return results
