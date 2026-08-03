use ndarray::{Array1, Array2};
use numpy::{PyArray1, PyArray2, PyArrayMethods, ToPyArray};
use pyo3::prelude::*;

/// Compute implied equilibrium returns using Black-Litterman reverse optimization.
///
/// Under CAPM, the market portfolio is optimal. Reverse-engineer the expected
/// returns that would make the given market-cap weights optimal:
///
///     Π = δ * Σ * w_mkt
///
/// where δ is the risk aversion coefficient, Σ is the covariance matrix,
/// and w_mkt are the market-cap weights.
#[pyfunction]
pub fn black_litterman_implied_returns<'py>(
    py: Python<'py>,
    cov_matrix: Bound<'py, PyArray2<f64>>,
    market_weights: Bound<'py, PyArray1<f64>>,
    risk_aversion: f64,
) -> Bound<'py, PyArray1<f64>> {
    let cov = cov_matrix.readonly();
    let cov = cov.as_array();
    let w = market_weights.readonly();
    let w = w.as_array();
    let n = w.len();

    let mut implied = Array1::zeros(n);
    for i in 0..n {
        let mut s = 0.0;
        for j in 0..n {
            s += cov[[i, j]] * w[j];
        }
        implied[i] = risk_aversion * s;
    }
    implied.to_pyarray(py)
}

/// Compute the Black-Litterman posterior expected returns.
///
/// Combines the prior (implied equilibrium returns) with investor views:
///
///     E[R] = [(τΣ)⁻¹ + PᵀΩ⁻¹P]⁻¹ · [(τΣ)⁻¹Π + PᵀΩ⁻¹Q]
///
/// Parameters:
///   implied_returns — prior equilibrium returns (Π)
///   cov_matrix — asset return covariance matrix (Σ)
///   tau — uncertainty scalar (0.01–0.05)
///   pick_matrix — maps views to assets (k × n)
///   view_returns — expected return for each view (k)
///   view_uncertainties — uncertainty (variance) of each view (k)
#[pyfunction]
pub fn black_litterman_posterior<'py>(
    py: Python<'py>,
    implied_returns: Bound<'py, PyArray1<f64>>,
    cov_matrix: Bound<'py, PyArray2<f64>>,
    tau: f64,
    pick_matrix: Bound<'py, PyArray2<f64>>,
    view_returns: Bound<'py, PyArray1<f64>>,
    view_uncertainties: Bound<'py, PyArray1<f64>>,
) -> PyResult<Bound<'py, PyArray1<f64>>> {
    let pi = implied_returns.readonly();
    let pi = pi.as_array();
    let cov = cov_matrix.readonly();
    let cov = cov.as_array();
    let p = pick_matrix.readonly();
    let p = p.as_array();
    let q = view_returns.readonly();
    let q = q.as_array();
    let omega_diag = view_uncertainties.readonly();
    let omega_diag = omega_diag.as_array();

    let n = pi.len();
    let k = q.len();

    let tau = if tau <= 0.0 { 0.025 } else { tau };

    // Compute Ω⁻¹ (diagonal)
    let mut omega_inv = Array2::zeros((k, k));
    for i in 0..k {
        let v = omega_diag[i].max(1e-8);
        omega_inv[[i, i]] = 1.0 / v;
    }

    // Σ_τ = τ · Σ
    let mut sigma_tau = Array2::zeros((n, n));
    for i in 0..n {
        for j in 0..n {
            sigma_tau[[i, j]] = tau * cov[[i, j]];
        }
    }

    // (τΣ)⁻¹
    let sigma_tau_inv = invert_2d(&sigma_tau)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e))?;

    // Pᵀ · Ω⁻¹ (n × k)
    let mut pt_omega_inv = Array2::zeros((n, k));
    for i in 0..n {
        for j in 0..k {
            let mut s = 0.0;
            for m in 0..k {
                s += p[[m, i]] * omega_inv[[m, j]];
            }
            pt_omega_inv[[i, j]] = s;
        }
    }

    // A = (τΣ)⁻¹ + PᵀΩ⁻¹P  (n × n)
    let mut a = Array2::zeros((n, n));
    for i in 0..n {
        for j in 0..n {
            a[[i, j]] = sigma_tau_inv[[i, j]];
            let mut s = 0.0;
            for m in 0..k {
                s += pt_omega_inv[[i, m]] * p[[m, j]];
            }
            a[[i, j]] += s;
        }
    }

    // A⁻¹
    let a_inv = invert_2d(&a)
        .map_err(|e| pyo3::exceptions::PyValueError::new_err(e))?;

    // b = (τΣ)⁻¹ · Π  +  Pᵀ · Ω⁻¹ · Q
    // (τΣ)⁻¹ · Π
    let mut term1 = Array1::zeros(n);
    for i in 0..n {
        let mut s = 0.0;
        for j in 0..n {
            s += sigma_tau_inv[[i, j]] * pi[j];
        }
        term1[i] = s;
    }

    // Pᵀ · Ω⁻¹ · Q
    let mut term2 = Array1::zeros(n);
    for i in 0..n {
        let mut s = 0.0;
        for m in 0..k {
            s += pt_omega_inv[[i, m]] * q[m];
        }
        term2[i] = s;
    }

    // E[R] = A⁻¹ · (term1 + term2)
    let mut posterior = Array1::zeros(n);
    for i in 0..n {
        let mut s = 0.0;
        for j in 0..n {
            s += a_inv[[i, j]] * (term1[j] + term2[j]);
        }
        posterior[i] = s;
    }

    Ok(posterior.to_pyarray(py))
}

/// Invert a square matrix via Gauss-Jordan elimination with partial pivoting.
fn invert_2d(m: &Array2<f64>) -> Result<Array2<f64>, String> {
    let n = m.shape()[0];
    if m.shape()[1] != n {
        return Err("Matrix must be square".into());
    }

    let mut aug = Array2::zeros((n, 2 * n));
    for i in 0..n {
        for j in 0..n {
            aug[[i, j]] = m[[i, j]];
        }
        aug[[i, n + i]] = 1.0;
    }

    for col in 0..n {
        let mut max_val = aug[[col, col]].abs();
        let mut max_row = col;
        for row in (col + 1)..n {
            let val = aug[[row, col]].abs();
            if val > max_val {
                max_val = val;
                max_row = row;
            }
        }
        if max_val < 1e-15 {
            return Err(format!("Singular matrix at column {}", col));
        }
        if max_row != col {
            for j in col..(2 * n) {
                aug.swap([col, j], [max_row, j]);
            }
        }

        let pivot = aug[[col, col]];
        for j in col..(2 * n) {
            aug[[col, j]] /= pivot;
        }

        for row in 0..n {
            if row != col {
                let factor = aug[[row, col]];
                if factor.abs() > 1e-15 {
                    for j in col..(2 * n) {
                        aug[[row, j]] -= factor * aug[[col, j]];
                    }
                }
            }
        }
    }

    let mut inv = Array2::zeros((n, n));
    for i in 0..n {
        for j in 0..n {
            inv[[i, j]] = aug[[i, n + j]];
        }
    }
    Ok(inv)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_implied_returns() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let cov = Array2::from_shape_vec((3, 3), vec![
                0.04, 0.02, 0.01,
                0.02, 0.09, 0.03,
                0.01, 0.03, 0.06,
            ]).unwrap();
            let w = Array1::from_vec(vec![0.4, 0.4, 0.2]);
            let delta = 2.5;
            let pi = black_litterman_implied_returns(
                py, cov.to_pyarray(py), w.to_pyarray(py), delta,
            );
            let pi = pi.readonly();
            let pi = pi.as_array();
            assert!((pi[0] - 0.065).abs() < 1e-10, "pi[0]={}", pi[0]);
            assert!((pi[1] - 0.125).abs() < 1e-10, "pi[1]={}", pi[1]);
            assert!((pi[2] - 0.070).abs() < 1e-10, "pi[2]={}", pi[2]);
        });
    }

    #[test]
    fn test_posterior_basic() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let cov = Array2::from_shape_vec((2, 2), vec![
                0.04, 0.01,
                0.01, 0.06,
            ]).unwrap();
            let w = Array1::from_vec(vec![0.6, 0.4]);
            let pi = black_litterman_implied_returns(
                py, cov.to_pyarray(py), w.to_pyarray(py), 2.5,
            );

            let p = Array2::from_shape_vec((1, 2), vec![0.0, 1.0]).unwrap();
            let q = Array1::from_vec(vec![0.15]);
            let omega = Array1::from_vec(vec![0.001]);

            let post = black_litterman_posterior(
                py, pi, cov.to_pyarray(py), 0.05,
                p.to_pyarray(py), q.to_pyarray(py), omega.to_pyarray(py),
            ).unwrap();
            let post = post.readonly();
            let post = post.as_array();
            assert_eq!(post.len(), 2);
            assert!(post[1] > 0.10, "Asset 2 should be pulled toward view: {}", post[1]);
        });
    }

    #[test]
    fn test_invert_2d() {
        let m = Array2::from_shape_vec((2, 2), vec![
            4.0, 7.0,
            2.0, 6.0,
        ]).unwrap();
        let inv = invert_2d(&m).unwrap();
        let ident = m.dot(&inv);
        assert!((ident[[0, 0]] - 1.0).abs() < 1e-10);
        assert!((ident[[1, 1]] - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_invert_singular() {
        let m = Array2::from_shape_vec((2, 2), vec![
            1.0, 2.0,
            2.0, 4.0,
        ]).unwrap();
        assert!(invert_2d(&m).is_err());
    }
}
