pub mod anomaly;
pub mod black_litterman;
pub mod lib_math;
pub mod monte_carlo;
pub mod pairs;
pub mod portfolio;
pub mod regime;
pub mod regression;
pub mod risk;
pub mod strategy_robustness;
pub mod tokenizer;

use pyo3::prelude::*;

/// Miau Finance — Rust-accelerated analytics engine.
#[pymodule]
fn _core(_py: Python<'_>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(black_litterman::black_litterman_implied_returns, m)?)?;
    m.add_function(wrap_pyfunction!(black_litterman::black_litterman_posterior, m)?)?;
    m.add_function(wrap_pyfunction!(monte_carlo::monte_carlo_gbm, m)?)?;
    m.add_function(wrap_pyfunction!(monte_carlo::histogram_bins, m)?)?;
    m.add_function(wrap_pyfunction!(portfolio::portfolio_stats, m)?)?;
    m.add_function(wrap_pyfunction!(portfolio::portfolio_evaluate, m)?)?;
    m.add_function(wrap_pyfunction!(portfolio::efficient_frontier, m)?)?;
    m.add_function(wrap_pyfunction!(regression::ols_regression, m)?)?;
    m.add_function(wrap_pyfunction!(regime::hmm_regime_detection, m)?)?;
    m.add_function(wrap_pyfunction!(pairs::pairs_analysis, m)?)?;
    m.add_function(wrap_pyfunction!(risk::historical_var, m)?)?;
    m.add_function(wrap_pyfunction!(risk::compute_beta, m)?)?;
    m.add_function(wrap_pyfunction!(risk::stress_scenario, m)?)?;
    m.add_function(wrap_pyfunction!(lib_math::compute_percentile, m)?)?;
    m.add_function(wrap_pyfunction!(lib_math::compute_mean, m)?)?;
    m.add_function(wrap_pyfunction!(lib_math::compute_std, m)?)?;
    m.add_function(wrap_pyfunction!(strategy_robustness::mc_robustness_test, m)?)?;
    anomaly::register(m)?;
    tokenizer::register(m)?;
    Ok(())
}

/// Validate price array — rejects empty, NaN, or negative values.
pub fn validate_prices(prices: &[f64]) -> Result<(), String> {
    if prices.is_empty() {
        return Err("Empty price array".into());
    }
    for &p in prices {
        if !p.is_finite() || p <= 0.0 {
            return Err(format!("Invalid price value: {}", p));
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validate_prices_empty() {
        assert!(validate_prices(&[]).is_err());
    }

    #[test]
    fn test_validate_prices_negative() {
        assert!(validate_prices(&[-1.0, 2.0]).is_err());
    }

    #[test]
    fn test_validate_prices_nan() {
        assert!(validate_prices(&[f64::NAN, 2.0]).is_err());
    }

    #[test]
    fn test_validate_prices_ok() {
        assert!(validate_prices(&[100.0, 101.0, 102.0]).is_ok());
    }
}
