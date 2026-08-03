use numpy::{PyArray1, PyArray2, PyArrayMethods};
use pyo3::prelude::*;
use pyo3::types::PyDict;

/// Run OLS regression: y = X * beta + epsilon
///
/// * `X` - Design matrix (n_obs × n_factors). NO constant column.
/// * `y` - Target vector (n_obs,)
///
/// Returns Python dict with alpha, coefficients, r_squared, adjusted_r_squared,
/// std_errors, t_statistics, residual_std.
#[pyfunction]
pub fn ols_regression<'py>(
    py: Python<'py>,
    x: Bound<'_, PyArray2<f64>>,
    y: Bound<'_, PyArray1<f64>>,
) -> PyResult<Bound<'py, PyDict>> {
    let x_read = x.readonly();
    let y_read = y.readonly();
    let x_arr = x_read.as_array();
    let y_arr = y_read.as_array();
    let n = y_arr.len();
    if n == 0 {
        let out = PyDict::new(py);
        out.set_item("error", "empty input")?;
        return Ok(out);
    }
    let k = x_arr.shape()[1];
    let out = PyDict::new(py);

    if n < 2 || k == 0 {
        out.set_item("error", true)?;
        return Ok(out);
    }

    // Build X'X and X'y
    let nc = k + 1;
    let mut xtx = vec![0.0; nc * nc];
    let mut xty = vec![0.0; nc];

    for i in 0..n {
        let yi = y_arr[i];
        xtx[0] += 1.0;
        xty[0] += yi;
        for j in 0..k {
            let xij = x_arr[(i, j)];
            let rj = j + 1;
            xtx[rj * nc] += xij;
            xtx[rj] += xij;
            xty[rj] += xij * yi;
            for l in 0..k {
                xtx[rj * nc + (l + 1)] += xij * x_arr[(i, l)];
            }
        }
    }

    let coefs = match solve_linear(&xtx, &xty, nc) {
        Some(c) => c,
        None => { out.set_item("error", "singular matrix")?; return Ok(out); }
    };

    let alpha = coefs[0];

    let y_mean: f64 = y_arr.iter().sum::<f64>() / n as f64;
    let mut ss_res = 0.0;
    let mut ss_tot = 0.0;

    for i in 0..n {
        let mut pred = alpha;
        for j in 0..k {
            pred += coefs[j + 1] * x_arr[(i, j)];
        }
        let res: f64 = y_arr[i] - pred;
        ss_res += res * res;
        ss_tot += (y_arr[i] - y_mean) * (y_arr[i] - y_mean);
    }

    let r_squared = if ss_tot > 1e-12 { 1.0 - ss_res / ss_tot } else { 0.0 };
    let dof = (n as f64 - k as f64 - 1.0).max(1.0);
    let dof_f64: f64 = dof;
    let adjusted = 1.0 - (1.0 - r_squared) * (n as f64 - 1.0) / dof_f64;
    let mse_f64: f64 = ss_res / dof_f64;
    let residual_std = mse_f64.sqrt();

    let xtx_inv = match invert_matrix(&xtx, nc) {
        Some(inv) => inv,
        None => { out.set_item("error", "singular cov")?; return Ok(out); }
    };

    let mut std_errors: Vec<f64> = Vec::with_capacity(nc);
    let mut t_stats: Vec<f64> = Vec::with_capacity(nc);
    for i in 0..nc {
        let se = (mse_f64 * xtx_inv[i * nc + i]).sqrt();
        std_errors.push(se);
        t_stats.push(coefs[i] / se.max(1e-15));
    }

    out.set_item("alpha", alpha)?;
    out.set_item("coefficients", coefs[1..].to_vec())?;
    out.set_item("r_squared", r_squared)?;
    out.set_item("adjusted_r_squared", adjusted)?;
    out.set_item("n_observations", n as i64)?;
    out.set_item("std_errors", std_errors)?;
    out.set_item("t_statistics", t_stats)?;
    out.set_item("residual_std", residual_std)?;

    Ok(out)
}

fn solve_linear(a: &[f64], b: &[f64], n: usize) -> Option<Vec<f64>> {
    let mut m = vec![0.0; n * (n + 1)];
    for i in 0..n {
        for j in 0..n {
            m[i * (n + 1) + j] = a[i * n + j];
        }
        m[i * (n + 1) + n] = b[i];
    }
    for col in 0..n {
        let mut max_row = col;
        let mut max_val = m[col * (n + 1) + col].abs();
        for row in (col + 1)..n {
            let v = m[row * (n + 1) + col].abs();
            if v > max_val { max_val = v; max_row = row; }
        }
        if max_val < 1e-15 { return None; }
        if max_row != col {
            for j in col..=n { m.swap(col * (n + 1) + j, max_row * (n + 1) + j); }
        }
        for row in (col + 1)..n {
            let factor = m[row * (n + 1) + col] / m[col * (n + 1) + col];
            for j in col..=n { m[row * (n + 1) + j] -= factor * m[col * (n + 1) + j]; }
        }
    }
    let mut x = vec![0.0; n];
    for i in (0..n).rev() {
        let mut sum = m[i * (n + 1) + n];
        for j in (i + 1)..n { sum -= m[i * (n + 1) + j] * x[j]; }
        x[i] = sum / m[i * (n + 1) + i];
    }
    Some(x)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solve_linear_2x2() {
        let a = vec![2.0, 1.0, 1.0, 3.0]; // 2x2 matrix
        let b = vec![5.0, 6.0];
        let x = solve_linear(&a, &b, 2).unwrap();
        assert!((x[0] - 1.8).abs() < 1e-10, "x[0] = {}", x[0]);
        assert!((x[1] - 1.4).abs() < 1e-10, "x[1] = {}", x[1]);
    }

    #[test]
    fn test_solve_linear_singular() {
        let a = vec![0.0, 0.0, 0.0, 0.0];
        let b = vec![1.0, 2.0];
        assert!(solve_linear(&a, &b, 2).is_none());
    }

    #[test]
    fn test_invert_2x2() {
        let a = vec![4.0, 7.0, 2.0, 6.0];
        let inv = invert_matrix(&a, 2).unwrap();
        // A * A^{-1} = I
        let p00 = a[0] * inv[0] + a[1] * inv[2];
        let p01 = a[0] * inv[1] + a[1] * inv[3];
        let p10 = a[2] * inv[0] + a[3] * inv[2];
        let p11 = a[2] * inv[1] + a[3] * inv[3];
        assert!((p00 - 1.0).abs() < 1e-10);
        assert!((p01 - 0.0).abs() < 1e-10);
        assert!((p10 - 0.0).abs() < 1e-10);
        assert!((p11 - 1.0).abs() < 1e-10);
    }

    #[test]
    fn test_invert_singular() {
        let a = vec![1.0, 2.0, 2.0, 4.0]; // singular: det = 0
        assert!(invert_matrix(&a, 2).is_none());
    }
}

fn invert_matrix(a: &[f64], n: usize) -> Option<Vec<f64>> {
    let mut aug = vec![0.0; n * (2 * n)];
    for i in 0..n {
        for j in 0..n { aug[i * (2 * n) + j] = a[i * n + j]; }
        aug[i * (2 * n) + n + i] = 1.0;
    }
    for col in 0..n {
        let mut max_row = col;
        let mut max_val = aug[col * (2 * n) + col].abs();
        for row in (col + 1)..n {
            let v = aug[row * (2 * n) + col].abs();
            if v > max_val { max_val = v; max_row = row; }
        }
        if max_val < 1e-15 { return None; }
        if max_row != col {
            for j in 0..(2 * n) { aug.swap(col * (2 * n) + j, max_row * (2 * n) + j); }
        }
        let piv = aug[col * (2 * n) + col];
        for j in 0..(2 * n) { aug[col * (2 * n) + j] /= piv; }
        for row in 0..n {
            if row != col {
                let factor = aug[row * (2 * n) + col];
                for j in 0..(2 * n) { aug[row * (2 * n) + j] -= factor * aug[col * (2 * n) + j]; }
            }
        }
    }
    let mut inv = vec![0.0; n * n];
    for i in 0..n {
        for j in 0..n { inv[i * n + j] = aug[i * (2 * n) + n + j]; }
    }
    Some(inv)
}
