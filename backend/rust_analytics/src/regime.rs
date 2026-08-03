use numpy::{PyArray1, PyArrayMethods};
use pyo3::prelude::*;
use pyo3::types::PyDict;

/// Hidden Markov Model for market regime detection.
///
/// Uses log-domain forward-backward algorithm for numerical stability.
///
/// * `returns` - 1D array of daily log returns
/// * `n_states` - Number of hidden regimes (default 3: Bull, Bear, Sideways)
/// * `n_iter` - EM iterations (default 50)
#[pyfunction]
pub fn hmm_regime_detection<'py>(
    py: Python<'py>,
    returns: Bound<'_, PyArray1<f64>>,
    n_states: usize,
    n_iter: usize,
) -> PyResult<Bound<'py, PyDict>> {
    let r_read = returns.readonly();
    let r_arr = r_read.as_array();
    let n = r_arr.len();
    let out = PyDict::new(py);

    if n < 10 || n_states < 2 {
        out.set_item("error", "insufficient data")?;
        return Ok(out);
    }

    let k = n_states;

    // Compute data stats for scaling
    let data_mean: f64 = r_arr.iter().sum::<f64>() / n as f64;
    let data_var: f64 = r_arr.iter().map(|v| (v - data_mean).powi(2)).sum::<f64>() / n as f64;
    let data_std = data_var.sqrt().max(1e-6);

    // Scale to N(0,1)
    let y: Vec<f64> = r_arr.iter().map(|v| (v - data_mean) / data_std).collect();

    // Initialize: k-means++ style spread
    let mut means = vec![0.0; k];
    let mut stds = vec![1.0; k];
    let min_y = y.iter().cloned().fold(f64::INFINITY, f64::min);
    let max_y = y.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    for i in 0..k {
        means[i] = min_y + (max_y - min_y) * (i as f64 + 0.5) / k as f64;
        stds[i] = (max_y - min_y) / k as f64 * 0.5 + 0.1;
    }

    // Uniform init and transition
    let mut trans = vec![0.0; k * k];
    let mut init = vec![0.0; k];
    for i in 0..k {
        init[i] = (1.0 / k as f64).ln();
        for j in 0..k {
            trans[i * k + j] = (1.0 / k as f64).ln();
        }
    }

    // Precompute log emissions
    let mut log_emit = vec![0.0; n * k];
    for t in 0..n {
        for s in 0..k {
            log_emit[t * k + s] = log_gaussian(y[t], means[s], stds[s]);
        }
    }

    let mut log_likelihood = f64::NEG_INFINITY;
    let mut final_log_alpha = vec![0.0; n * k];
    let mut final_log_beta = vec![0.0; n * k];

    for _iter in 0..n_iter {
        // ── Forward pass (log-alpha) ──
        let mut log_alpha = vec![f64::NEG_INFINITY; n * k];
        for s in 0..k {
            log_alpha[s] = init[s] + log_emit[s];
        }

        for t in 1..n {
            for s in 0..k {
                let mut max_val = f64::NEG_INFINITY;
                for sp in 0..k {
                    let v = log_alpha[(t - 1) * k + sp] + trans[sp * k + s];
                    if v > max_val {
                        max_val = v;
                    }
                }
                // log-sum-exp for numerical stability
                let mut sum_exp = 0.0;
                for sp in 0..k {
                    let v = log_alpha[(t - 1) * k + sp] + trans[sp * k + s];
                    if v > max_val - 700.0 {
                        sum_exp += (v - max_val).exp();
                    }
                }
                log_alpha[t * k + s] = max_val + sum_exp.ln() + log_emit[t * k + s];
            }
        }

        // Log-likelihood: log P(Y|θ)
        let mut ll = f64::NEG_INFINITY;
        for s in 0..k {
            let v = log_alpha[(n - 1) * k + s];
            if v > ll {
                if ll > f64::NEG_INFINITY {
                    ll = ll + (1.0 + (v - ll).exp()).ln(); // log(exp(ll) + exp(v))
                } else {
                    ll = v;
                }
            }
        }

        // ── Backward pass (log-beta) ──
        let mut log_beta = vec![f64::NEG_INFINITY; n * k];
        for s in 0..k {
            log_beta[(n - 1) * k + s] = 0.0;
        }
        for t in (0..n - 1).rev() {
            for s in 0..k {
                let mut max_val = f64::NEG_INFINITY;
                for sp in 0..k {
                    let v = trans[s * k + sp] + log_emit[(t + 1) * k + sp] + log_beta[(t + 1) * k + sp];
                    if v > max_val { max_val = v; }
                }
                let mut sum_exp = 0.0;
                for sp in 0..k {
                    let v = trans[s * k + sp] + log_emit[(t + 1) * k + sp] + log_beta[(t + 1) * k + sp];
                    if v > max_val - 700.0 { sum_exp += (v - max_val).exp(); }
                }
                log_beta[t * k + s] = max_val + sum_exp.ln();
            }
        }

        // Save for final probs
        final_log_alpha.copy_from_slice(&log_alpha);
        final_log_beta.copy_from_slice(&log_beta);

        // Convergence
        if (ll - log_likelihood).abs() < 1e-4 {
            break;
        }
        log_likelihood = ll;

        // ── Gamma (posterior state probs) ──
        let mut gamma = vec![0.0; n * k];
        let mut gamma_sum = vec![0.0; k];
        for t in 0..n {
            let mut max_val = f64::NEG_INFINITY;
            for s in 0..k {
                gamma[t * k + s] = log_alpha[t * k + s] + log_beta[t * k + s];
                if gamma[t * k + s] > max_val { max_val = gamma[t * k + s]; }
            }
            let mut norm = 0.0;
            for s in 0..k {
                gamma[t * k + s] = (gamma[t * k + s] - max_val).exp();
                norm += gamma[t * k + s];
            }
            if norm > 1e-300 {
                for s in 0..k {
                    gamma[t * k + s] /= norm;
                    gamma_sum[s] += gamma[t * k + s];
                }
            }
        }

        // ── Xi (transition posterior) ──
        let mut xi_sum = vec![0.0; k * k];
        for t in 0..n - 1 {
            let mut max_val = f64::NEG_INFINITY;
            let mut xi = vec![0.0; k * k];
            for i in 0..k {
                for j in 0..k {
                    let v = log_alpha[t * k + i] + trans[i * k + j]
                        + log_emit[(t + 1) * k + j] + log_beta[(t + 1) * k + j];
                    xi[i * k + j] = v;
                    if v > max_val { max_val = v; }
                }
            }
            if max_val > f64::NEG_INFINITY {
                let mut norm = 0.0;
                for i in 0..k {
                    for j in 0..k {
                        xi[i * k + j] = (xi[i * k + j] - max_val).exp();
                        norm += xi[i * k + j];
                    }
                }
                if norm > 1e-300 {
                    for i in 0..k {
                        for j in 0..k {
                            xi_sum[i * k + j] += xi[i * k + j] / norm;
                        }
                    }
                }
            }
        }

        // ── M-step ──
        for s in 0..k {
            let gs = gamma_sum[s].max(1e-300);
            let mut new_mean = 0.0;
            let mut new_var = 0.0;
            for t in 0..n {
                new_mean += gamma[t * k + s] * y[t];
            }
            new_mean /= gs;
            for t in 0..n {
                let d = y[t] - new_mean;
                new_var += gamma[t * k + s] * d * d;
            }
            means[s] = new_mean;
            stds[s] = (new_var / gs).sqrt().max(0.01);
        }

        for i in 0..k {
            let gs = gamma_sum[i].max(1e-300);
            for j in 0..k {
                trans[i * k + j] = (xi_sum[i * k + j] / gs).max(1e-10);
            }
            let row_sum: f64 = trans[i * k..(i + 1) * k].iter().sum();
            for j in 0..k {
                trans[i * k + j] = (trans[i * k + j] / row_sum).ln();
            }
        }

        // Update log emissions
        for t in 0..n {
            for s in 0..k {
                log_emit[t * k + s] = log_gaussian(y[t], means[s], stds[s]);
            }
        }
    }

    // ── Viterbi (most likely state sequence) ──
    let mut viterbi = vec![0usize; n];
    let mut delta = vec![f64::NEG_INFINITY; n * k];
    let mut psi = vec![0usize; n * k];

    for s in 0..k {
        delta[s] = init[s] + log_emit[s];
    }
    for t in 1..n {
        for s in 0..k {
            let mut max_val = f64::NEG_INFINITY;
            let mut max_idx = 0;
            for sp in 0..k {
                let v = delta[(t - 1) * k + sp] + trans[sp * k + s];
                if v > max_val { max_val = v; max_idx = sp; }
            }
            delta[t * k + s] = max_val + log_emit[t * k + s];
            psi[t * k + s] = max_idx;
        }
    }

    let mut max_val = f64::NEG_INFINITY;
    for s in 0..k {
        if delta[(n - 1) * k + s] > max_val {
            max_val = delta[(n - 1) * k + s];
            viterbi[n - 1] = s;
        }
    }
    for t in (0..n - 1).rev() {
        viterbi[t] = psi[(t + 1) * k + viterbi[t + 1]];
    }

    // ── State probabilities (from log-alpha + log-beta) ──
    let mut state_probs = vec![0.0; n * k];
    for t in 0..n {
        let mut max_val = f64::NEG_INFINITY;
        for s in 0..k {
            state_probs[t * k + s] = final_log_alpha[t * k + s] + final_log_beta[t * k + s];
            if state_probs[t * k + s] > max_val { max_val = state_probs[t * k + s]; }
        }
        if max_val > f64::NEG_INFINITY {
            let mut norm = 0.0;
            for s in 0..k {
                state_probs[t * k + s] = (state_probs[t * k + s] - max_val).exp();
                norm += state_probs[t * k + s];
            }
            if norm > 1e-300 {
                for s in 0..k { state_probs[t * k + s] /= norm; }
            }
        }
    }

    // De-scale means/stds
    for s in 0..k {
        means[s] = means[s] * data_std + data_mean;
        stds[s] *= data_std;
    }

    // Convert transition back from log
    let mut trans_linear = vec![0.0; k * k];
    for i in 0..k {
        let mut row_sum = 0.0;
        for j in 0..k {
            trans_linear[i * k + j] = trans[i * k + j].exp();
            row_sum += trans_linear[i * k + j];
        }
        for j in 0..k { trans_linear[i * k + j] /= row_sum; }
    }

    out.set_item("states", viterbi)?;
    out.set_item("state_probs", state_probs)?;
    out.set_item("transition", trans_linear)?;
    out.set_item("means", means)?;
    out.set_item("stds", stds)?;
    out.set_item("n_states", k)?;
    out.set_item("n_observations", n)?;
    out.set_item("log_likelihood", log_likelihood)?;

    Ok(out)
}

/// Log of Gaussian PDF
fn log_gaussian(x: f64, mu: f64, sigma: f64) -> f64 {
    let s = sigma.max(0.001);
    let z = (x - mu) / s;
    -0.5 * z * z - s.ln() - 0.5 * (2.0 * std::f64::consts::PI).ln()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_log_gaussian_peak_at_mean() {
        let l1 = log_gaussian(0.0, 0.0, 1.0);
        let l2 = log_gaussian(0.5, 0.0, 1.0);
        assert!(l1 > l2, "Log likelihood should be highest at mean");
    }

    #[test]
    fn test_log_gaussian_wide_sigma() {
        let l1 = log_gaussian(0.0, 0.0, 1.0);
        let l2 = log_gaussian(0.0, 0.0, 10.0);
        assert!(l1 > l2, "Narrower sigma should give higher peak");
    }

    #[test]
    fn test_log_gaussian_sigma_floor() {
        let l = log_gaussian(0.0, 0.0, 0.0);
        assert!(l.is_finite(), "Zero sigma should be floored, not crash");
    }

    #[test]
    fn test_log_gaussian_symmetry() {
        let l1 = log_gaussian(-1.0, 0.0, 1.0);
        let l2 = log_gaussian(1.0, 0.0, 1.0);
        assert!((l1 - l2).abs() < 1e-10, "Should be symmetric around mean");
    }
}
