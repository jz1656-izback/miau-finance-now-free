use pyo3::prelude::*;
use rand::rngs::StdRng;
use rand::seq::SliceRandom;
use rand::Rng;
use rand::SeedableRng;
use rayon::prelude::*;

fn percentile(sorted: &[f64], p: f64) -> f64 {
    if sorted.is_empty() {
        return 0.0;
    }
    let idx = ((sorted.len() - 1) as f64 * p / 100.0).round() as usize;
    sorted[idx.min(sorted.len() - 1)]
}

fn compute_metrics(equity: &[f64]) -> (f64, f64, f64) {
    let n = equity.len() as f64;
    if n < 2.0 {
        return (0.0, 0.0, 0.0);
    }
    let total_return = (equity[equity.len() - 1] / equity[0]) - 1.0;
    let mut daily_returns = Vec::with_capacity(equity.len() - 1);
    for i in 1..equity.len() {
        daily_returns.push((equity[i] / equity[i - 1]) - 1.0);
    }
    let mean_ret: f64 = daily_returns.iter().sum::<f64>() / daily_returns.len() as f64;
    let variance: f64 = daily_returns.iter().map(|r| (r - mean_ret).powi(2)).sum::<f64>()
        / (daily_returns.len() - 1) as f64;
    let std = variance.sqrt();
    let sharpe = if std > 0.0 {
        (mean_ret / std) * (252.0_f64).sqrt()
    } else {
        0.0
    };
    let mut max_dd = 0.0;
    let mut peak = equity[0];
    for &v in equity.iter() {
        if v > peak {
            peak = v;
        }
        let dd = (peak - v) / peak;
        if dd > max_dd {
            max_dd = dd;
        }
    }
    (total_return * 100.0, sharpe, max_dd * 100.0)
}

#[pyfunction]
pub fn mc_robustness_test(
    equity_curve: Vec<f64>,
    iterations: usize,
    seed: u64,
) -> PyResult<Vec<f64>> {
    if equity_curve.len() < 10 {
        return Ok(vec![0.0; 6]);
    }

    let results: Vec<(f64, f64, f64)> = (0..iterations)
        .into_par_iter()
        .map(|i| {
            let mut rng = StdRng::seed_from_u64(seed.wrapping_add((i as u64).wrapping_mul(6364136223846793005)));
            let mut shuffled = equity_curve.clone();

            shuffled.shuffle(&mut rng);
            let mut noise_added: Vec<f64> = shuffled
                .iter()
                .map(|&v| {
                    let noise = rng.gen_range(-1.0..1.0) * v * 0.01;
                    v * (1.0 + noise)
                })
                .collect();
            noise_added.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));

            let skip_count = (equity_curve.len() as f64 * 0.1).round() as usize;
            let sampled: Vec<f64> = if skip_count > 0 && skip_count < noise_added.len() {
                noise_added[skip_count..].to_vec()
            } else {
                noise_added
            };

            compute_metrics(&sampled)
        })
        .collect();

    let mut returns: Vec<f64> = results.iter().map(|r| r.0).collect();
    let mut sharpes: Vec<f64> = results.iter().map(|r| r.1).collect();
    let mut drawdowns: Vec<f64> = results.iter().map(|r| r.2).collect();

    returns.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());
    sharpes.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());
    drawdowns.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());

    Ok(vec![
        percentile(&returns, 5.0),
        percentile(&returns, 50.0),
        percentile(&returns, 95.0),
        percentile(&sharpes, 50.0),
        percentile(&drawdowns, 95.0),
        percentile(&drawdowns, 50.0),
    ])
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mc_robustness_basic() {
        let equity: Vec<f64> = (0..100).map(|i| 100.0 + (i as f64) * 0.5).collect();
        let result = mc_robustness_test(equity, 100, 42).unwrap();
        assert_eq!(result.len(), 6);
        assert!(result[1] > 0.0, "Median return should be positive");
    }

    #[test]
    fn test_mc_robustness_short() {
        let result = mc_robustness_test(vec![100.0, 101.0], 10, 42).unwrap();
        assert_eq!(result.len(), 6);
    }

    #[test]
    fn test_percentile() {
        let data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        assert!((percentile(&data, 50.0) - 3.0).abs() < 0.01);
    }
}
