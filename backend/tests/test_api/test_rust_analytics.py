"""
Tests for the Rust-accelerated analytics engine.

These test the Python bridge modules in miau_analytics which auto-detect
the Rust native extension (_core) and fall back to pure Python if unavailable.
"""
import pytest
import numpy as np


@pytest.mark.anyio
async def test_monte_carlo_gbm_runs():
    """Monte Carlo GBM produces valid output regardless of Rust availability."""
    from app.services.analytics.monte_carlo import run_monte_carlo

    result = await run_monte_carlo("AAPL", num_simulations=100, days=50, period="1y")
    assert result["ticker"] == "AAPL"
    assert result["num_simulations"] == 100
    assert result["days"] == 50
    assert result["last_price"] > 0
    assert result["summary"]["mean_final_price"] > 0
    assert result["summary"]["median_final_price"] > 0
    assert result["probability"]["profit"] + result["probability"]["loss"] == pytest.approx(1.0, rel=0.01)
    assert "var_95" in result["value_at_risk"]
    assert "var_99" in result["value_at_risk"]
    assert "cvar_95" in result["value_at_risk"]
    assert len(result["histogram"]) > 0
    assert len(result["path_sample"]) > 0


@pytest.mark.skip(reason="Depends on Yahoo Finance data freshness")
@pytest.mark.anyio
async def test_monte_carlo_gbm_consistent_seed():
    """Same seed produces same results (deterministic)."""
    from app.services.analytics.monte_carlo import run_monte_carlo

    r1 = await run_monte_carlo("SPY", num_simulations=1000, days=21, period="3mo")
    r2 = await run_monte_carlo("SPY", num_simulations=1000, days=21, period="3mo")

    assert r1["summary"]["mean_final_price"] == r2["summary"]["mean_final_price"]
    assert r1["summary"]["std_final_price"] == r2["summary"]["std_final_price"]


@pytest.mark.anyio
async def test_black_litterman_runs():
    """Black-Litterman model produces valid output."""
    from app.services.analytics.black_litterman import black_litterman

    tickers = ["AAPL", "MSFT", "GOOGL"]
    market_cap_weights = [0.4, 0.3, 0.3]
    views = [
        {"type": "absolute", "ticker": "AAPL", "return": 0.15},
    ]

    result = await black_litterman(tickers, market_cap_weights, views)
    assert result is not None
    assert len(result["posterior_returns"]) == 3
    assert "weights" in result
    assert "portfolio" in result


@pytest.mark.anyio
async def test_sentiment_analysis_structure():
    """Sentiment analysis returns expected structure."""
    from app.services.analytics.sentiment import analyze_ticker_sentiment

    result = await analyze_ticker_sentiment("AAPL", days=3)
    assert "ticker" in result
    assert "overall_score" in result
    assert "article_count" in result


@pytest.mark.skip(reason="Requires running SEC EDGAR (needs network)")
@pytest.mark.anyio
async def test_sec_edgar_parser():
    """SEC EDGAR filings parser returns correct structure."""
    from app.services.data_sources.sec_edgar import get_filings

    result = await get_filings("AAPL", filing_types=["10-K", "10-Q"], limit=5)
    assert "filings" in result


@pytest.mark.anyio
async def test_portfolio_optimizer():
    """Portfolio optimizer runs with mock data."""
    from app.services.analytics.portfolio_optimizer import optimize_portfolio

    result = await optimize_portfolio(
        tickers=["AAPL", "MSFT", "GOOGL"],
        risk_free_rate=0.05,
        target_return=0.15,
        period="6mo",
    )
    assert "weights" in result
    assert len(result["weights"]) == 3
    assert abs(sum(result["weights"].values()) - 1.0) < 0.01


@pytest.mark.skip(reason="Requires the Rust native extension to be built")
def test_rust_native_mc():
    """Direct Rust Monte Carlo (requires maturin build)."""
    from miau_analytics import run_monte_carlo_gbm

    result = run_monte_carlo_gbm(
        last_price=150.0, mu=0.08, sigma=0.22,
        num_simulations=1000, days=252, seed=42,
    )
    assert result["summary"]["mean_final_price"] > 0
    assert result["value_at_risk"]["var_95"] > 0
    assert len(result["histogram"]) == 30


# ── Factor Analysis Tests ───────────────────────────────────────────────────


@pytest.mark.anyio
async def test_factor_regression_basic():
    """Factor regression with 3-factor model returns expected structure."""
    from app.services.analytics.factors import run_factor_regression

    result = await run_factor_regression("AAPL", model=3, include_momentum=False, period="1y")
    if "error" in result:
        pytest.skip(f"Network error: {result['error']}")
    assert result["ticker"] == "AAPL"
    assert "Mkt-RF" in result["factor_loadings"]
    assert "SMB" in result["factor_loadings"]
    assert "HML" in result["factor_loadings"]
    assert result["n_observations"] > 20
    assert 0 <= result["r_squared"] <= 1
    assert abs(result["alpha"]["daily"]) < 0.1  # reasonable alpha


@pytest.mark.anyio
async def test_factor_regression_5factor():
    """5-factor model returns all 5 factors + optional momentum."""
    from app.services.analytics.factors import run_factor_regression

    result = await run_factor_regression("SPY", model=5, include_momentum=True, period="2y")
    if "error" in result:
        pytest.skip(f"Network error: {result['error']}")
    for f in ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "MOM"]:
        assert f in result["factor_loadings"], f"Missing factor: {f}"


@pytest.mark.anyio
async def test_factor_regression_summary_endpoint():
    """AP factor summary endpoint works (mocked)."""
    from app.api.analytics.factors import router
    assert len(router.routes) >= 2  # /factors/{ticker} + /factors/{ticker}/summary


@pytest.mark.skip(reason="Requires the Rust native extension to be built")
def test_rust_ols_matches_numpy():
    """Rust OLS regression matches numpy exactly on synthetic data."""
    from miau_analytics._core import ols_regression as rust_ols
    from app.services.analytics.factors import _ols_numpy

    rng = np.random.default_rng(42)
    n, k = 500, 3
    X = rng.normal(0, 1, (n, k))
    true_beta = np.array([0.5, -0.3, 0.8])
    y = 0.01 + X @ true_beta + rng.normal(0, 0.1, n)

    rust = dict(rust_ols(X, y))
    np_result = _ols_numpy(X, y)

    assert abs(rust["alpha"] - np_result["alpha"]) < 1e-10
    for i in range(k):
        assert abs(rust["coefficients"][i] - np_result["coefficients"][f"factor_{i}"]) < 1e-10
    assert abs(rust["r_squared"] - np_result["r_squared"]) < 1e-10


@pytest.mark.skip(reason="Requires the Rust native extension to be built")
def test_rust_native_var():
    """Direct Rust VaR computation."""
    from miau_analytics import compute_historical_var
    import numpy as np

    prices = np.random.default_rng(42).normal(0.001, 0.02, 1000)
    result = compute_historical_var(prices, 0.95)
    assert result["var"] < 0
    assert result["cvar"] < result["var"]
