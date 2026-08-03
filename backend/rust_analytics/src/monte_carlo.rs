use ndarray::Array2;
use numpy::ToPyArray;
use numpy::PyArrayMethods;
use numpy::{PyArray1, PyArray2};
use pyo3::prelude::*;
use pyo3::Bound;
use rand::rngs::StdRng;
use rand::SeedableRng;
use rand_distr::{Distribution, StandardNormal};
use rayon::prelude::*;

/// Run Geometric Brownian Motion Monte Carlo simulation.
#[pyfunction]
pub fn monte_carlo_gbm(
    py: Python<'_>,
    last_price: f64,
    mu: f64,
    sigma: f64,
    num_simulations: usize,
    days: usize,
    seed: u64,
) -> PyResult<(Bound<'_, PyArray2<f64>>, Bound<'_, PyArray1<f64>>)> {
    let dt = 1.0 / 252.0;
    let drift = (mu - 0.5 * sigma * sigma) * dt;
    let vol = sigma * dt.sqrt();

    let sim_seeds: Vec<u64> = (0..num_simulations)
        .map(|i| seed.wrapping_add((i as u64).wrapping_mul(6364136223846793005)))
        .collect();

    let sims: Vec<(Vec<f64>, f64)> = sim_seeds
        .par_iter()
        .map(|&sim_seed| {
            let mut rng = StdRng::seed_from_u64(sim_seed);
            let mut path = Vec::with_capacity(days + 1);
            path.push(last_price);
            let mut price = last_price;
            for _ in 0..days {
                let z: f64 = StandardNormal.sample(&mut rng);
                price *= (drift + vol * z).exp();
                path.push(price);
            }
            (path, price)
        })
        .collect();

    let final_prices: Vec<f64> = sims.iter().map(|(_, f)| *f).collect();

    let mut flat = Vec::with_capacity((days + 1) * num_simulations);
    flat.resize((days + 1) * num_simulations, 0.0);
    for (sim_idx, (path, _)) in sims.iter().enumerate() {
        for (day, &val) in path.iter().enumerate() {
            flat[day * num_simulations + sim_idx] = val;
        }
    }

    let shape = [days + 1, num_simulations];
    let array = Array2::from_shape_vec(shape, flat).unwrap();
    let final_array = ndarray::Array1::from_vec(final_prices);

    Ok((
        array.to_pyarray(py),
        final_array.to_pyarray(py),
    ))
}

/// Compute histogram bins from final prices.
#[pyfunction]
pub fn histogram_bins(
    data: Bound<'_, PyArray1<f64>>,
    num_bins: usize,
) -> Vec<(f64, f64, usize)> {
    let readonly = data.readonly();
    let data = readonly.as_array();
    if data.is_empty() {
        return Vec::new();
    }
    let min_val = data.iter().cloned().fold(f64::INFINITY, f64::min);
    let max_val = data.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    if (max_val - min_val).abs() < 1e-12 {
        return vec![(min_val, max_val, data.len())];
    }
    let bin_width = (max_val - min_val) / num_bins as f64;
    let mut counts = vec![0usize; num_bins];
    for &val in data.iter() {
        let idx = ((val - min_val) / bin_width) as usize;
        let idx = idx.min(num_bins - 1);
        counts[idx] += 1;
    }
    counts
        .into_iter()
        .enumerate()
        .map(|(i, count)| {
            (
                min_val + i as f64 * bin_width,
                min_val + (i + 1) as f64 * bin_width,
                count,
            )
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gbm_basic() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let (paths, final_prices) = monte_carlo_gbm(py, 100.0, 0.08, 0.22, 100, 10, 42).unwrap();
            let paths = unsafe { paths.as_array() };
            let final_prices = unsafe { final_prices.as_array() };
            assert_eq!(paths.shape(), &[11, 100]);
            assert_eq!(final_prices.len(), 100);
            // All prices should be positive
            for &p in final_prices.iter() {
                assert!(p > 0.0, "Price should be positive: {}", p);
            }
            // Starting price should be last_price
            for j in 0..100 {
                assert!((paths[[0, j]] - 100.0).abs() < 1e-6);
            }
        });
    }

    #[test]
    fn test_gbm_deterministic() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let (_, f1) = monte_carlo_gbm(py, 150.0, 0.05, 0.30, 50, 21, 99).unwrap();
            let (_, f2) = monte_carlo_gbm(py, 150.0, 0.05, 0.30, 50, 21, 99).unwrap();
            let f1 = unsafe { f1.as_array() };
            let f2 = unsafe { f2.as_array() };
            for i in 0..50 {
                assert!((f1[i] - f2[i]).abs() < 1e-6, "Seed mismatch at {}", i);
            }
        });
    }

    #[test]
    fn test_histogram_bins() {
        pyo3::prepare_freethreaded_python();
        Python::with_gil(|py| {
            let data = ndarray::Array1::from_vec(vec![1.0, 2.0, 2.0, 3.0, 3.0, 3.0, 4.0, 5.0]);
            use numpy::ToPyArray;
            let pyarray = data.to_pyarray(py);
            let bins = histogram_bins(pyarray, 4);
            assert_eq!(bins.len(), 4);
            let total: usize = bins.iter().map(|(_, _, c)| c).sum();
            assert_eq!(total, 8);
        });
    }
}
