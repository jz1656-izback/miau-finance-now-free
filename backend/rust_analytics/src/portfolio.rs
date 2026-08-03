use numpy::ToPyArray;
use numpy::PyArrayMethods;
use numpy::{PyArray1, PyArray2};
use pyo3::prelude::*;
use pyo3::Bound;
use rayon::prelude::*;

/// Compute annualized mean returns and covariance matrix from a price history matrix.
#[pyfunction]
pub fn portfolio_stats<'py>(
    py: Python<'py>,
    prices: Bound<'_, PyArray2<f64>>,
) -> PyResult<(Bound<'py, PyArray1<f64>>, Bound<'py, PyArray2<f64>>)> {
    let readonly = prices.readonly();
    let prices = readonly.as_array();
    let shape = prices.shape();
    let n_days = shape[0];
    let n_tickers = shape[1];

    if n_days < 2 {
        let mu = ndarray::Array1::zeros(n_tickers);
        let cov = ndarray::Array2::eye(n_tickers);
        return Ok((mu.to_pyarray(py), cov.to_pyarray(py)));
    }

    let n_ret = n_days - 1;
    let mut returns = Vec::with_capacity(n_ret * n_tickers);
    for i in 1..n_days {
        for j in 0..n_tickers {
            let prev = prices[[i - 1, j]];
            let curr = prices[[i, j]];
            returns.push(if prev > 0.0 { (curr / prev).ln() } else { 0.0 });
        }
    }

    let mut mean_returns = Vec::with_capacity(n_tickers);
    for j in 0..n_tickers {
        let mut s = 0.0;
        for i in 0..n_ret {
            s += returns[i * n_tickers + j];
        }
        mean_returns.push(s / n_ret as f64 * 252.0);
    }

    let mut cov_data = vec![0.0; n_tickers * n_tickers];
    for j1 in 0..n_tickers {
        for j2 in 0..n_tickers {
            let mut s = 0.0;
            let m1 = mean_returns[j1] / 252.0;
            let m2 = mean_returns[j2] / 252.0;
            for i in 0..n_ret {
                s += (returns[i * n_tickers + j1] - m1) * (returns[i * n_tickers + j2] - m2);
            }
            cov_data[j1 * n_tickers + j2] = s / (n_ret - 1) as f64 * 252.0;
        }
    }

    let mu_arr = ndarray::Array1::from_vec(mean_returns);
    let cov_arr = ndarray::Array2::from_shape_vec((n_tickers, n_tickers), cov_data).unwrap();
    Ok((mu_arr.to_pyarray(py), cov_arr.to_pyarray(py)))
}

/// Evaluate portfolio return, volatility, and Sharpe ratio.
#[pyfunction]
pub fn portfolio_evaluate(
    weights: Bound<'_, PyArray1<f64>>,
    mean_returns: Bound<'_, PyArray1<f64>>,
    cov_matrix: Bound<'_, PyArray2<f64>>,
    risk_free_rate: f64,
) -> (f64, f64, f64) {
    let w = weights.readonly();
    let w = w.as_array();
    let mu = mean_returns.readonly();
    let mu = mu.as_array();
    let cov = cov_matrix.readonly();
    let cov = cov.as_array();

    let n = w.len();
    let mut port_ret = 0.0;
    for i in 0..n {
        port_ret += w[i] * mu[i];
    }

    let mut port_var = 0.0_f64;
    for i in 0..n {
        for j in 0..n {
            port_var += w[i] * w[j] * cov[[i, j]];
        }
    }
    let port_vol = port_var.sqrt();
    let sharpe = if port_vol > 1e-12 {
        (port_ret - risk_free_rate) / port_vol
    } else {
        0.0
    };
    (port_ret, port_vol, sharpe)
}

/// Compute the efficient frontier by generating random portfolios.
#[pyfunction]
pub fn efficient_frontier(
    mean_returns: Bound<'_, PyArray1<f64>>,
    cov_matrix: Bound<'_, PyArray2<f64>>,
    risk_free_rate: f64,
    num_points: usize,
) -> Vec<(f64, f64, f64)> {
    let mu = mean_returns.readonly();
    let mu = mu.as_array();
    let cov = cov_matrix.readonly();
    let cov = cov.as_array();
    let n = mu.len();

    let num_random = num_points * 5;
    let points: Vec<(f64, f64, f64)> = (0..num_random)
        .into_par_iter()
        .map(|_| {
            let mut raw: Vec<f64> = (0..n).map(|_| rand::random::<f64>().abs()).collect();
            let s: f64 = raw.iter().sum();
            for w in raw.iter_mut() {
                *w /= s;
            }
            let mut port_ret = 0.0;
            let mut port_var = 0.0_f64;
            for i in 0..n {
                port_ret += raw[i] * mu[i];
                for j in 0..n {
                    port_var += raw[i] * raw[j] * cov[[i, j]];
                }
            }
            let port_vol = port_var.sqrt();
            let sharpe = if port_vol > 1e-12 {
                (port_ret - risk_free_rate) / port_vol
            } else {
                0.0
            };
            (port_vol, port_ret, sharpe)
        })
        .collect();

    let mut sorted = points;
    sorted.sort_unstable_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

    let bucket_size = sorted.len() / num_points;
    let mut frontier = Vec::with_capacity(num_points);
    for i in 0..num_points {
        let start = i * bucket_size;
        let end = ((i + 1) * bucket_size).min(sorted.len());
        if start >= sorted.len() {
            break;
        }
        if let Some(best) = sorted[start..end]
            .iter()
            .max_by(|a, b| a.2.partial_cmp(&b.2).unwrap())
        {
            frontier.push(*best);
        }
    }

    for i in 0..n {
        let mut s = 0.0_f64;
        for k in 0..n {
            s += cov[[i, k]];
        }
        let vol = s.sqrt();
        let ret = mu[i];
        let sharpe = if vol > 1e-12 { (ret - risk_free_rate) / vol } else { 0.0 };
        frontier.push((vol, ret, sharpe));
    }

    frontier.sort_unstable_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
    frontier.truncate(num_points + n);
    frontier
}

#[cfg(test)]
mod tests {
    use super::*;
    use numpy::ToPyArray;

    #[test]
    fn test_portfolio_evaluate() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let w = ndarray::Array1::from_vec(vec![0.5, 0.3, 0.2]);
            let mu = ndarray::Array1::from_vec(vec![0.10, 0.12, 0.08]);
            let cov = ndarray::Array2::from_shape_vec((3, 3), vec![
                0.04, 0.02, 0.01,
                0.02, 0.09, 0.03,
                0.01, 0.03, 0.06,
            ]).unwrap();

            let w_py = w.to_pyarray(py);
            let mu_py = mu.to_pyarray(py);
            let cov_py = cov.to_pyarray(py);

            let (ret, vol, sharpe) = portfolio_evaluate(w_py, mu_py, cov_py, 0.05);
            assert!(ret > 0.0, "return={}", ret);
            assert!(vol > 0.0, "vol={}", vol);
            let expected = (ret - 0.05) / vol;
            assert!((sharpe - expected).abs() < 0.01, "sharpe={} expected={}", sharpe, expected);
        });
    }

    #[test]
    fn test_portfolio_stats() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let prices = ndarray::Array2::from_shape_vec((5, 2), vec![
                100.0, 50.0,
                102.0, 51.0,
                101.0, 52.0,
                103.0, 50.5,
                104.0, 51.5,
            ]).unwrap();
            let p = prices.to_pyarray(py);
            let (mu, cov) = portfolio_stats(py, p).unwrap();
            assert_eq!(mu.readonly().as_array().len(), 2);
            assert_eq!(cov.readonly().as_array().shape(), &[2, 2]);
        });
    }

    #[test]
    fn test_efficient_frontier() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let mu = ndarray::Array1::from_vec(vec![0.12, 0.08, 0.10]);
            let cov = ndarray::Array2::from_shape_vec((3, 3), vec![
                0.04, 0.01, 0.02,
                0.01, 0.06, 0.01,
                0.02, 0.01, 0.05,
            ]).unwrap();
            let mu_py = mu.to_pyarray(py);
            let cov_py = cov.to_pyarray(py);
            let frontier = efficient_frontier(mu_py, cov_py, 0.05, 20);
            assert!(!frontier.is_empty());
            // Frontier should be sorted by volatility
            for i in 1..frontier.len() {
                assert!(frontier[i].0 >= frontier[i - 1].0 - 1e-10);
            }
        });
    }
}
