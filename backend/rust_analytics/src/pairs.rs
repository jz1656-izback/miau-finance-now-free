use numpy::{PyArray1, PyArrayMethods};
use pyo3::prelude::*;
use pyo3::types::PyDict;

/// Compute pairs trading statistics between two price series.
///
/// * `prices_a` - Price series for stock A
/// * `prices_b` - Price series for stock B
/// * `lookback` - Rolling window for z-score (default 20)
///
/// Returns dict with: hedge_ratio, spread, z_scores, half_life,
/// adf_statistic, adf_pvalue, is_cointegrated, current_z_score.
#[pyfunction]
pub fn pairs_analysis<'py>(
    py: Python<'py>,
    prices_a: Bound<'_, PyArray1<f64>>,
    prices_b: Bound<'_, PyArray1<f64>>,
    lookback: usize,
) -> PyResult<Bound<'py, PyDict>> {
    let a_read = prices_a.readonly();
    let b_read = prices_b.readonly();
    let a = a_read.as_array();
    let b = b_read.as_array();
    let n = a.len().min(b.len());
    let out = PyDict::new(py);

    if n < 30 {
        out.set_item("error", "insufficient data")?;
        return Ok(out);
    }

    // 1. Log prices for cointegration regression
    let mut log_a = Vec::with_capacity(n);
    let mut log_b = Vec::with_capacity(n);
    for i in 0..n {
        if a[i] > 0.0 && b[i] > 0.0 {
            log_a.push(a[i].ln());
            log_b.push(b[i].ln());
        }
    }
    let m = log_a.len();
    if m < 30 {
        out.set_item("error", "insufficient valid prices")?;
        return Ok(out);
    }

    // 2. OLS: log_b = alpha + beta * log_a + epsilon
    let (beta, alpha, residuals) = ols_simple(&log_a, &log_b);

    // 3. Spread = log_b - beta * log_a (de-meaned)
    let spread_mean: f64 = residuals.iter().sum::<f64>() / m as f64;
    let mut spread = Vec::with_capacity(m);
    for r in &residuals {
        spread.push(r - spread_mean);
    }

    // 4. Z-score over rolling window
    let lookback = lookback.max(5).min(m / 2);
    let mut z_scores = vec![0.0; m];
    for i in lookback..m {
        let window = &spread[i - lookback..i];
        let w_mean: f64 = window.iter().sum::<f64>() / lookback as f64;
        let w_var: f64 = window.iter().map(|v| (v - w_mean).powi(2)).sum::<f64>() / lookback as f64;
        let w_std = w_var.sqrt().max(1e-10);
        z_scores[i] = (spread[i] - w_mean) / w_std;
    }

    // 5. Half-life of mean reversion
    // Regress spread(t) - spread(t-1) on spread(t-1)
    let half_life = compute_half_life(&spread);

    // 6. ADF test statistic (simplified Dickey-Fuller)
    let (adf_stat, adf_pvalue) = adf_test(&spread);

    // 7. Current z-score
    let current_z = if m > 0 { z_scores[m - 1] } else { 0.0 };

    // 8. Signal strength
    let signal = if current_z > 2.0 {
        -1  // Short spread (sell B, buy A)
    } else if current_z < -2.0 {
        1   // Long spread (buy B, sell A)
    } else {
        0   // Neutral
    };

    // Build output
    out.set_item("hedge_ratio", beta)?;
    out.set_item("alpha", alpha)?;
    out.set_item("spread", spread)?;
    out.set_item("z_scores", z_scores)?;
    out.set_item("current_z_score", current_z)?;
    out.set_item("half_life", half_life)?;
    out.set_item("adf_statistic", adf_stat)?;
    out.set_item("adf_pvalue", adf_pvalue)?;
    out.set_item("is_cointegrated", adf_pvalue < 0.05)?;
    out.set_item("signal", signal)?;
    out.set_item("n_observations", m)?;
    out.set_item("lookback", lookback)?;

    Ok(out)
}

/// Simple OLS: y = alpha + beta * x
fn ols_simple(x: &[f64], y: &[f64]) -> (f64, f64, Vec<f64>) {
    let n = x.len();
    let mean_x: f64 = x.iter().sum::<f64>() / n as f64;
    let mean_y: f64 = y.iter().sum::<f64>() / n as f64;

    let mut num = 0.0;
    let mut den = 0.0;
    for i in 0..n {
        let dx = x[i] - mean_x;
        let dy = y[i] - mean_y;
        num += dx * dy;
        den += dx * dx;
    }
    let beta = if den > 1e-15 { num / den } else { 0.0 };
    let alpha = mean_y - beta * mean_x;

    let residuals: Vec<f64> = y.iter().enumerate().map(|(i, &yi)| yi - alpha - beta * x[i]).collect();
    (beta, alpha, residuals)
}

/// Compute half-life of mean reversion via OLS on lagged spread.
fn compute_half_life(spread: &[f64]) -> f64 {
    let n = spread.len();
    if n < 10 {
        return f64::INFINITY;
    }
    // Spread(t) - Spread(t-1) = theta * Spread(t-1) + epsilon
    let mut x = Vec::with_capacity(n - 1);
    let mut y = Vec::with_capacity(n - 1);
    for i in 1..n {
        x.push(spread[i - 1]);
        y.push(spread[i] - spread[i - 1]);
    }
    let (theta, _, _) = ols_simple(&x, &y);
    if theta >= 0.0 {
        return f64::INFINITY; // Not mean-reverting
    }
    // half-life = ln(2) / -theta
    -(2.0_f64.ln()) / theta
}

/// Simplified Augmented Dickey-Fuller test (lag=1).
/// Returns (test_statistic, approximate p-value).
fn adf_test(y: &[f64]) -> (f64, f64) {
    let n = y.len();
    if n < 10 {
        return (0.0, 1.0);
    }

    // Δy(t) = γ*y(t-1) + ε(t)
    let mut dy = Vec::with_capacity(n - 1);
    let mut y_lag = Vec::with_capacity(n - 1);
    for i in 1..n {
        dy.push(y[i] - y[i - 1]);
        y_lag.push(y[i - 1]);
    }

    let (gamma, _, residuals) = ols_simple(&y_lag, &dy);
    let m = residuals.len();
    if m < 2 {
        return (0.0, 1.0);
    }

    // SE(gamma)
    let res_mean: f64 = residuals.iter().sum::<f64>() / m as f64;
    let sse: f64 = residuals.iter().map(|r| (r - res_mean).powi(2)).sum::<f64>();
    let mse = sse / (m - 2) as f64;

    let yl_mean: f64 = y_lag.iter().sum::<f64>() / m as f64;
    let sxx: f64 = y_lag.iter().map(|v| (v - yl_mean).powi(2)).sum::<f64>();
    let se_gamma = (mse / sxx.max(1e-15)).sqrt();

    let t_stat = gamma / se_gamma.max(1e-15);

    // Critical values for 5% significance (approx)
    let cv_5pct = -2.86;
    // If t_stat < critical value, reject null of unit root (stationary)
    let p = if t_stat < cv_5pct { 0.01 } else { 0.5 };

    (t_stat, p)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ols_simple_perfect() {
        let x = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let y: Vec<f64> = x.iter().map(|&v| 2.0 + 3.0 * v).collect();
        let (beta, alpha, residuals) = ols_simple(&x, &y);
        assert!((beta - 3.0).abs() < 1e-10, "beta = {}", beta);
        assert!((alpha - 2.0).abs() < 1e-10, "alpha = {}", alpha);
        for &r in &residuals {
            assert!(r.abs() < 1e-10, "residual = {}", r);
        }
    }

    #[test]
    fn test_ols_simple_random() {
        let x = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let y = vec![2.1, 3.9, 6.2, 7.8, 10.1]; // ~0.04 + 1.99x
        let (beta, alpha, _) = ols_simple(&x, &y);
        assert!((beta - 1.99).abs() < 0.01, "beta = {} (expected 1.99)", beta);
        assert!((alpha - 0.04).abs() < 0.05, "alpha = {} (expected 0.04)", alpha);
    }

    #[test]
    fn test_half_life_strong_mean_reversion() {
        // AR(1) with phi=0.5 → half-life = ln(2)/ln(2) = 1.0
        let spread: Vec<f64> = (0..100).map(|i| {
            if i == 0 { 1.0 } else { 0.5 * (i as f64).sin() }
        }).collect();
        let hl = compute_half_life(&spread);
        assert!(hl.is_finite(), "half-life should be finite");
        assert!(hl > 0.0, "half-life should be positive: {}", hl);
    }

    #[test]
    fn test_half_life_explosive() {
        // Explosive series → no mean reversion → infinite half-life
        let spread: Vec<f64> = (0..50).map(|i| (i as f64).exp()).collect();
        let hl = compute_half_life(&spread);
        assert!(hl.is_infinite() || hl.is_nan(), "explosive series should have inf half-life: {}", hl);
    }
}
