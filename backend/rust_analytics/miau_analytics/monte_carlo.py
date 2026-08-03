"""
Monte Carlo simulation — accelerated by Rust when available.
"""

from __future__ import annotations

import numpy as np

try:
    from miau_analytics._core import monte_carlo_gbm as _rust_gbm
    from miau_analytics._core import histogram_bins as _rust_hist

    _HAS_RUST = True
except ImportError:
    _HAS_RUST = False


def run_monte_carlo_gbm(
    last_price: float,
    mu: float,
    sigma: float,
    num_simulations: int = 1000,
    days: int = 252,
    seed: int = 42,
) -> dict:
    """Run Geometric Brownian Motion Monte Carlo simulation.

    Parameters
    ----------
    last_price : float
        Most recent closing price (S₀).
    mu : float
        Annualized drift (mean log-return × 252).
    sigma : float
        Annualized volatility.
    num_simulations : int
        Number of independent paths.
    days : int
        Number of trading days to simulate.
    seed : int
        PRNG seed.

    Returns
    -------
    dict with keys:
        paths : ndarray, shape (days+1, num_simulations)
        final_prices : ndarray, shape (num_simulations,)
        mean_final_price : float
        median_final_price : float
        std_final_price : float
        min_final_price : float
        max_final_price : float
        prob_profit : float
        prob_loss : float
        var_95 : float
        var_99 : float
        cvar_95 : float
        histogram : list of (bin_start, bin_end, count)
        path_sample : list[list[float]]  (first 10 paths)
    """
    if _HAS_RUST:
        import miau_analytics._core as _rust

        paths, final_prices = _rust.monte_carlo_gbm(
            last_price, mu, sigma, num_simulations, days, seed,
        )
        paths = np.asarray(paths)
        final_prices = np.asarray(final_prices)
    else:
        paths, final_prices = _py_gbm(last_price, mu, sigma, num_simulations, days, seed)

    mean_final = float(np.mean(final_prices))
    std_final = float(np.std(final_prices))
    median_final = float(np.median(final_prices))
    prob_profit = float(np.mean(final_prices > last_price))
    prob_loss = float(np.mean(final_prices < last_price))

    var_95 = float(np.percentile(final_prices, 5))
    var_99 = float(np.percentile(final_prices, 1))
    cvar_95 = float(np.mean(final_prices[final_prices <= var_95])) if np.any(final_prices <= var_95) else var_95

    if _HAS_RUST:
        import miau_analytics._core as _rust

        hist_bins = list(_rust.histogram_bins(final_prices, 30))
    else:
        hist, bin_edges = np.histogram(final_prices, bins=30)
        hist_bins = [
            (round(float(bin_edges[i]), 2), round(float(bin_edges[i + 1]), 2), int(hist[i]))
            for i in range(len(hist))
        ]

    path_sample = paths[:10, :].T.tolist() if paths.ndim == 2 else [paths[:10].tolist()]
    sampled_days = [
        round(float(np.mean(paths[d, :])), 2)
        for d in range(0, days + 1, max(1, days // 20))
    ]

    return {
        "paths": paths,
        "final_prices": final_prices,
        "summary": {
            "mean_final_price": round(mean_final, 2),
            "median_final_price": round(median_final, 2),
            "std_final_price": round(std_final, 2),
            "min_final_price": round(float(np.min(final_prices)), 2),
            "max_final_price": round(float(np.max(final_prices)), 2),
        },
        "probability": {
            "profit": round(prob_profit, 4),
            "loss": round(prob_loss, 4),
        },
        "value_at_risk": {
            "var_95": round(var_95, 2),
            "var_99": round(var_99, 2),
            "cvar_95": round(cvar_95, 2),
        },
        "histogram": [
            {"bin_start": b[0], "bin_end": b[1], "count": b[2]}
            for b in hist_bins
        ],
        "path_sample": path_sample,
        "sampled_days": sampled_days,
    }


def _py_gbm(
    last_price: float,
    mu: float,
    sigma: float,
    num_simulations: int,
    days: int,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Pure-Python GBM fallback (mirrors the Rust implementation)."""
    dt = 1.0 / 252.0
    drift = (mu - 0.5 * sigma * sigma) * dt
    vol = sigma * np.sqrt(dt)

    rng = np.random.default_rng(seed)
    rand = rng.standard_normal((num_simulations, days))

    paths = np.zeros((days + 1, num_simulations))
    paths[0, :] = last_price
    for i in range(1, days + 1):
        paths[i, :] = paths[i - 1, :] * np.exp(drift + vol * rand[:, i - 1])

    final_prices = paths[-1, :].copy()
    return paths, final_prices
