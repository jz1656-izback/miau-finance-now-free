"""
miau_analytics — Rust-accelerated analytics engine for Miau Finance.

Provides fast implementations of computationally heavy analytics using
native Rust extensions (via PyO3), with automatic fallback to pure-Python
+numpy when the Rust module is not available.
"""

from __future__ import annotations

from .monte_carlo import run_monte_carlo_gbm
from .portfolio import portfolio_stats as run_portfolio_stats
from .portfolio import portfolio_evaluate
from .portfolio import efficient_frontier as compute_efficient_frontier
from .risk import compute_historical_var, compute_beta, run_stress_scenario

try:
    from miau_analytics._core import z_score_anomaly_py as z_score_anomaly
    from miau_analytics._core import black_litterman_implied_returns
    from miau_analytics._core import black_litterman_posterior
    from miau_analytics._core import PyIsolationForest as IsolationForest
    from miau_analytics._core import PyRollingStats as RollingStats

    _HAS_RUST_ANOMALY = True
except ImportError:
    _HAS_RUST_ANOMALY = False

try:
    from miau_analytics._core import tokenize, count_tokens

    _HAS_RUST_TOKENIZER = True
except ImportError:
    _HAS_RUST_TOKENIZER = False

try:
    from miau_analytics._core import black_litterman_implied_returns, black_litterman_posterior
    _HAS_RUST_BL = True
except ImportError:
    _HAS_RUST_BL = False

__all__ = [
    "run_monte_carlo_gbm",
    "run_portfolio_stats",
    "portfolio_evaluate",
    "compute_efficient_frontier",
    "compute_historical_var",
    "compute_beta",
    "run_stress_scenario",
    "z_score_anomaly",
    "IsolationForest",
    "RollingStats",
    "tokenize",
    "count_tokens",
    "black_litterman_implied_returns",
    "black_litterman_posterior",
]
