use numpy::PyArrayMethods;
use numpy::PyArray1;
use pyo3::prelude::*;
use pyo3::Bound;

/// Compute percentiles from a 1-D array using linear interpolation.
pub fn percentile_linear(data: &[f64], p: f64) -> f64 {
    if data.is_empty() {
        return 0.0;
    }
    let mut sorted = data.to_vec();
    sorted.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());

    let n = sorted.len();
    let rank = (p / 100.0) * (n as f64 - 1.0);
    let lower = rank.floor() as usize;
    let upper = rank.ceil() as usize;

    if lower == upper || upper >= n {
        sorted[lower]
    } else {
        let frac = rank - lower as f64;
        sorted[lower] * (1.0 - frac) + sorted[upper] * frac
    }
}

/// Compute arithmetic mean.
pub fn mean(data: &[f64]) -> f64 {
    if data.is_empty() {
        return 0.0;
    }
    data.iter().sum::<f64>() / data.len() as f64
}

/// Compute sample standard deviation.
pub fn std_dev(data: &[f64], ddof: usize) -> f64 {
    let n = data.len();
    if n <= ddof {
        return 0.0;
    }
    let m = mean(data);
    let variance = data.iter().map(|v| (v - m).powi(2)).sum::<f64>() / (n - ddof) as f64;
    variance.sqrt()
}

/// Compute log returns: ln(x_i / x_{i-1}) for i = 1..n
pub fn log_returns(prices: &[f64]) -> Vec<f64> {
    prices
        .windows(2)
        .map(|w| (w[1] / w[0]).ln())
        .collect()
}

/// Compute the dot product of two vectors.
pub fn dot(a: &[f64], b: &[f64]) -> f64 {
    a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
}

/// Normalize a vector to sum to 1.0.
pub fn normalize(weights: &[f64]) -> Vec<f64> {
    let s: f64 = weights.iter().sum();
    if s.abs() < 1e-12 {
        let n = weights.len();
        vec![1.0 / n as f64; n]
    } else {
        weights.iter().map(|w| w / s).collect()
    }
}

/// Compute parametric VaR: VaR = -(mu * T + sigma * sqrt(T) * z)
pub fn parametric_var(mu: f64, sigma: f64, days: f64, confidence: f64) -> f64 {
    let z = match (confidence * 100.0).round() as i32 {
        99 => 2.326,
        97 => 1.881,
        95 => 1.645,
        90 => 1.282,
        _ => 1.645,
    };
    -(mu * days / 252.0 + sigma * (days / 252.0).sqrt() * z)
}

#[pyfunction]
pub fn compute_percentile(data: Bound<'_, PyArray1<f64>>, p: f64) -> f64 {
    let readonly = data.readonly();
    let arr = readonly.as_array();
    let v: Vec<f64> = arr.iter().copied().collect();
    percentile_linear(&v, p)
}

#[pyfunction]
pub fn compute_mean(data: Bound<'_, PyArray1<f64>>) -> f64 {
    let readonly = data.readonly();
    let arr = readonly.as_array();
    let v: Vec<f64> = arr.iter().copied().collect();
    mean(&v)
}

#[pyfunction]
pub fn compute_std(data: Bound<'_, PyArray1<f64>>, ddof: usize) -> f64 {
    let readonly = data.readonly();
    let arr = readonly.as_array();
    let v: Vec<f64> = arr.iter().copied().collect();
    std_dev(&v, ddof)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mean() {
        assert!((mean(&[1.0, 2.0, 3.0]) - 2.0).abs() < 1e-12);
        assert!((mean(&[5.0]) - 5.0).abs() < 1e-12);
        assert!((mean(&[]) - 0.0).abs() < 1e-12);
    }

    #[test]
    fn test_std_dev() {
        let data = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0];
        let s = std_dev(&data, 1);
        assert!((s - 2.138).abs() < 0.01, "std_dev={}", s);
    }

    #[test]
    fn test_log_returns() {
        let prices = [100.0, 105.0, 100.0];
        let rets = log_returns(&prices);
        assert_eq!(rets.len(), 2);
        assert!((rets[0] - 0.04879).abs() < 0.001);
        assert!((rets[1] - (-0.04879)).abs() < 0.001);
    }

    #[test]
    fn test_percentile_linear() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        assert!((percentile_linear(&data, 50.0) - 3.0).abs() < 1e-12);
        assert!((percentile_linear(&data, 0.0) - 1.0).abs() < 1e-12);
        assert!((percentile_linear(&data, 100.0) - 5.0).abs() < 1e-12);
    }

    #[test]
    fn test_dot() {
        assert!((dot(&[1.0, 2.0, 3.0], &[4.0, 5.0, 6.0]) - 32.0).abs() < 1e-12);
    }

    #[test]
    fn test_normalize() {
        let n = normalize(&[1.0, 2.0, 3.0]);
        assert!((n[0] - 1.0 / 6.0).abs() < 1e-12);
        assert!((n[1] - 2.0 / 6.0).abs() < 1e-12);
        assert!((n[2] - 3.0 / 6.0).abs() < 1e-12);
        assert!((n.iter().sum::<f64>() - 1.0).abs() < 1e-12);
    }

    #[test]
    fn test_normalize_zero() {
        let n = normalize(&[0.0, 0.0, 0.0]);
        assert_eq!(n.len(), 3);
        assert!((n[0] - 1.0 / 3.0).abs() < 1e-12);
    }

    #[test]
    fn test_parametric_var() {
        let var95 = parametric_var(0.08, 0.22, 21.0, 0.95);
        assert!(var95 < 0.0, "VaR should be negative for positive returns: {}", var95);
        let var99 = parametric_var(0.08, 0.22, 21.0, 0.99);
        assert!(var99 < var95, "VaR 99% should be more negative than VaR 95%: {} vs {}", var99, var95);
    }
}
