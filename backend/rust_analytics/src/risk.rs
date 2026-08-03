use numpy::PyArrayMethods;
use numpy::PyArray1;
use pyo3::prelude::*;
use pyo3::Bound;
use rayon::prelude::*;

use crate::lib_math;

/// Compute historical VaR and CVaR from a price series.
#[pyfunction]
pub fn historical_var(
    prices: Bound<'_, PyArray1<f64>>,
    confidence: f64,
) -> (f64, f64) {
    let readonly = prices.readonly();
    let data = readonly.as_array();
    let v: Vec<f64> = data.iter().copied().collect();

    let returns = lib_math::log_returns(&v);
    if returns.is_empty() {
        return (0.0, 0.0);
    }

    let var = lib_math::percentile_linear(&returns, (1.0 - confidence) * 100.0);
    let cvar = {
        let tail: Vec<f64> = returns.iter().filter(|&&r| r <= var).copied().collect();
        if tail.is_empty() {
            var
        } else {
            lib_math::mean(&tail)
        }
    };
    (var, cvar)
}

/// Compute Beta of a stock vs a benchmark.
#[pyfunction]
pub fn compute_beta(
    stock_prices: Bound<'_, PyArray1<f64>>,
    benchmark_prices: Bound<'_, PyArray1<f64>>,
) -> (f64, f64, f64) {
    let s = stock_prices.readonly();
    let s = s.as_array();
    let b = benchmark_prices.readonly();
    let b = b.as_array();

    let s_vals: Vec<f64> = s.iter().copied().collect();
    let b_vals: Vec<f64> = b.iter().copied().collect();

    let s_ret = lib_math::log_returns(&s_vals);
    let b_ret = lib_math::log_returns(&b_vals);

    let min_len = s_ret.len().min(b_ret.len());
    if min_len < 2 {
        return (1.0, 0.0, 0.0);
    }

    let s_ret = &s_ret[..min_len];
    let b_ret = &b_ret[..min_len];

    let mean_s = lib_math::mean(s_ret);
    let mean_b = lib_math::mean(b_ret);

    let mut cov = 0.0;
    let mut var_b = 0.0;
    for i in 0..min_len {
        cov += (s_ret[i] - mean_s) * (b_ret[i] - mean_b);
        var_b += (b_ret[i] - mean_b).powi(2);
    }
    cov /= (min_len - 1) as f64;
    var_b /= (min_len - 1) as f64;

    let beta = if var_b > 1e-12 { cov / var_b } else { 1.0 };
    let alpha = mean_s - beta * mean_b;
    let correlation = if var_b > 1e-12 {
        let std_s = lib_math::std_dev(s_ret, 1);
        let std_b = lib_math::std_dev(b_ret, 1);
        if std_s > 1e-12 && std_b > 1e-12 {
            cov / (std_s * std_b)
        } else {
            0.0
        }
    } else {
        0.0
    };
    (beta, alpha, correlation)
}

/// Compute historical stress scenario impact.
#[pyfunction]
pub fn stress_scenario(
    current_price: f64,
    shocks: Vec<f64>,
    scenario_names: Vec<String>,
) -> Vec<(String, f64, f64, String)> {
    shocks
        .into_par_iter()
        .zip(scenario_names.into_par_iter())
        .map(|(shock, name)| {
            let shocked_price = current_price * (1.0 + shock);
            let change_pct = shock * 100.0;
            let label = if shock >= 0.0 {
                format!("+{:.1}% (${:.2})", change_pct, shocked_price)
            } else {
                format!("{:.1}% (${:.2})", change_pct, shocked_price)
            };
            (name, shocked_price, change_pct, label)
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::lib_math;
    use numpy::ToPyArray;

    #[test]
    fn test_historical_var() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let prices = ndarray::Array1::from_vec(vec![
                100.0, 101.0, 99.0, 102.0, 98.0, 103.0, 97.0, 104.0,
            ]);
            let p = prices.to_pyarray(py);
            let (var, cvar) = historical_var(p, 0.95);
            assert!(var < 0.0, "VaR should be negative: {}", var);
            assert!(cvar <= var, "CVaR should be <= VaR: {} vs {}", cvar, var);
        });
    }

    #[test]
    fn test_compute_beta() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let stock = ndarray::Array1::from_vec(vec![
                100.0, 110.0, 120.0, 130.0, 140.0,
            ]);
            let bench = ndarray::Array1::from_vec(vec![
                100.0, 105.0, 110.0, 115.0, 120.0,
            ]);
            let s = stock.to_pyarray(py);
            let b = bench.to_pyarray(py);
            let (beta, _alpha, corr) = compute_beta(s, b);
            assert!(beta > 0.0, "beta should be positive: {}", beta);
            assert!(corr > 0.9, "corr={}", corr);
        });
    }

    #[test]
    fn test_stress_scenario() {
        let current = 100.0;
        let shocks = vec![-0.20, -0.10, 0.05, 0.10];
        let names = vec!["Crash".into(), "Dip".into(), "Rally".into(), "Boom".into()];
        let results = stress_scenario(current, shocks, names);
        assert_eq!(results.len(), 4);
        assert!((results[0].1 - 80.0).abs() < 1e-10, "Crash price: {}", results[0].1);
        assert!((results[3].1 - 110.0).abs() < 1e-10, "Boom price: {}", results[3].1);
    }

    #[test]
    fn test_log_returns_math() {
        let prices = vec![100.0, 110.0, 100.0];
        let rets = lib_math::log_returns(&prices);
        assert!((rets[0] - 0.09531).abs() < 0.001);
        assert!((rets[1] - (-0.09531)).abs() < 0.001);
    }
}
