use numpy::PyArrayMethods;
use numpy::PyArray1;
use pyo3::prelude::*;
use pyo3::Bound;
use rand::Rng;

pub fn z_score_anomaly(data: &[f64], threshold: f64) -> Vec<usize> {
    if data.len() < 2 {
        return Vec::new();
    }
    let n = data.len() as f64;
    let mean = data.iter().sum::<f64>() / n;
    let variance = data.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / (n - 1.0);
    let std = variance.sqrt();
    if std < 1e-12 {
        return Vec::new();
    }
    data.iter()
        .enumerate()
        .filter(|(_, &v)| (v - mean).abs() / std > threshold)
        .map(|(i, _)| i)
        .collect()
}

struct IsolationTree {
    split_value: f64,
    left: Option<Box<IsolationTree>>,
    right: Option<Box<IsolationTree>>,
    size: usize,
}

impl IsolationTree {
    fn new(data: &[Vec<f64>], depth: usize, max_depth: usize) -> Self {
        if depth >= max_depth || data.len() <= 1 {
            return IsolationTree {
                split_value: 0.0,
                left: None,
                right: None,
                size: data.len(),
            };
        }
        let n_features = data[0].len();
        let mut rng = rand::thread_rng();
        let feature_idx = rng.gen_range(0..n_features);
        let mut col: Vec<f64> = data.iter().map(|row| row[feature_idx]).collect();
        col.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());
        let min = col.first().copied().unwrap_or(0.0);
        let max = col.last().copied().unwrap_or(0.0);
        if (max - min).abs() < 1e-12 {
            return IsolationTree {
                split_value: 0.0,
                left: None,
                right: None,
                size: data.len(),
            };
        }
        let split_value = min + rng.gen::<f64>() * (max - min);
        let mut left_data = Vec::new();
        let mut right_data = Vec::new();
        for row in data {
            if row[feature_idx] < split_value {
                left_data.push(row.clone());
            } else {
                right_data.push(row.clone());
            }
        }
        if left_data.is_empty() || right_data.is_empty() {
            return IsolationTree {
                split_value: 0.0,
                left: None,
                right: None,
                size: data.len(),
            };
        }
        IsolationTree {
            split_value,
            left: Some(Box::new(IsolationTree::new(&left_data, depth + 1, max_depth))),
            right: Some(Box::new(IsolationTree::new(&right_data, depth + 1, max_depth))),
            size: data.len(),
        }
    }

    fn path_length(&self, point: &[f64], depth: usize, feature_idx: usize) -> usize {
        if self.left.is_none() && self.right.is_none() {
            return depth + c_factor(self.size);
        }
        if point[feature_idx] < self.split_value {
            if let Some(ref left) = self.left {
                return left.path_length(point, depth + 1, feature_idx);
            }
        } else if let Some(ref right) = self.right {
            return right.path_length(point, depth + 1, feature_idx);
        }
        depth + c_factor(self.size)
    }
}

fn c_factor(n: usize) -> usize {
    if n <= 1 {
        return 0;
    }
    let h = (n as f64).ln() + 0.5772156649;
    (2.0 * h - 2.0 * (n - 1) as f64 / n as f64).ceil() as usize
}

pub struct IsolationForest {
    trees: Vec<IsolationTree>,
    max_depth: usize,
    n_features: usize,
}

impl IsolationForest {
    pub fn new(n_estimators: usize, max_depth: Option<usize>) -> Self {
        IsolationForest {
            trees: Vec::with_capacity(n_estimators),
            max_depth: max_depth.unwrap_or(100),
            n_features: 0,
        }
    }

    pub fn fit(&mut self, data: &[Vec<f64>]) {
        if data.is_empty() || data[0].is_empty() {
            return;
        }
        self.n_features = data[0].len();
        let n_estimators = self.trees.capacity();
        for _ in 0..n_estimators {
            let tree = IsolationTree::new(data, 0, self.max_depth);
            self.trees.push(tree);
        }
    }

    pub fn predict(&self, point: &[f64]) -> f64 {
        if self.trees.is_empty() || self.n_features == 0 {
            return 0.5;
        }
        let avg_path: f64 = self
            .trees
            .iter()
            .map(|tree| tree.path_length(point, 0, 0) as f64)
            .sum::<f64>()
            / self.trees.len() as f64;
        let c = c_factor(self.trees[0].size) as f64;
        if c <= 0.0 {
            return 0.5;
        }
        let score = 2.0_f64.powf(-avg_path / c);
        score.clamp(0.0, 1.0)
    }
}

pub struct RollingStats {
    window: Vec<f64>,
    max_size: usize,
}

impl RollingStats {
    pub fn new(window_size: usize) -> Self {
        RollingStats {
            window: Vec::with_capacity(window_size),
            max_size: window_size,
        }
    }

    pub fn add(&mut self, value: f64) {
        if self.window.len() >= self.max_size {
            self.window.remove(0);
        }
        self.window.push(value);
    }

    pub fn mean(&self) -> f64 {
        if self.window.is_empty() {
            return 0.0;
        }
        self.window.iter().sum::<f64>() / self.window.len() as f64
    }

    pub fn std_dev(&self) -> f64 {
        let n = self.window.len();
        if n < 2 {
            return 0.0;
        }
        let m = self.mean();
        let variance = self.window.iter().map(|v| (v - m).powi(2)).sum::<f64>() / (n - 1) as f64;
        variance.sqrt()
    }

    pub fn is_anomaly(&self, value: f64, threshold: f64) -> bool {
        let n = self.window.len();
        if n < 2 {
            return false;
        }
        let m = self.mean();
        let s = self.std_dev();
        if s < 1e-12 {
            return false;
        }
        (value - m).abs() / s > threshold
    }
}

#[pyfunction]
pub fn z_score_anomaly_py(data: Bound<'_, PyArray1<f64>>, threshold: f64) -> Vec<usize> {
    let readonly = data.readonly();
    let arr = readonly.as_array();
    let v: Vec<f64> = arr.iter().copied().collect();
    z_score_anomaly(&v, threshold)
}

#[pyclass]
pub struct PyIsolationForest {
    inner: Option<IsolationForest>,
}

#[pymethods]
impl PyIsolationForest {
    #[new]
    #[pyo3(signature = (n_estimators, max_depth=None))]
    pub fn new(n_estimators: usize, max_depth: Option<usize>) -> Self {
        PyIsolationForest {
            inner: Some(IsolationForest::new(n_estimators, max_depth)),
        }
    }

    pub fn fit(&mut self, data: Vec<Vec<f64>>) {
        if let Some(ref mut forest) = self.inner {
            forest.fit(&data);
        }
    }

    pub fn predict(&self, point: Vec<f64>) -> f64 {
        match self.inner {
            Some(ref forest) => forest.predict(&point),
            None => 0.5,
        }
    }
}

#[pyclass]
pub struct PyRollingStats {
    inner: RollingStats,
}

#[pymethods]
impl PyRollingStats {
    #[new]
    pub fn new(window_size: usize) -> Self {
        PyRollingStats {
            inner: RollingStats::new(window_size),
        }
    }

    pub fn add(&mut self, value: f64) {
        self.inner.add(value);
    }

    pub fn mean(&self) -> f64 {
        self.inner.mean()
    }

    pub fn std_dev(&self) -> f64 {
        self.inner.std_dev()
    }

    pub fn is_anomaly(&self, value: f64, threshold: f64) -> bool {
        self.inner.is_anomaly(value, threshold)
    }
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(z_score_anomaly_py, m)?)?;
    m.add_class::<PyIsolationForest>()?;
    m.add_class::<PyRollingStats>()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_z_score_anomaly() {
        let data = vec![10.0, 12.0, 11.0, 13.0, 100.0, 9.0, 11.5, 10.5];
        let anomalies = z_score_anomaly(&data, 2.0);
        assert_eq!(anomalies, vec![4], "Should detect 100.0 as anomaly");
    }

    #[test]
    fn test_z_score_anomaly_none() {
        let data = vec![10.0, 11.0, 10.5, 11.5, 10.2];
        let anomalies = z_score_anomaly(&data, 3.0);
        assert!(anomalies.is_empty(), "No anomalies expected");
    }

    #[test]
    fn test_z_score_anomaly_short() {
        let anomalies = z_score_anomaly(&[1.0], 2.0);
        assert!(anomalies.is_empty());
    }

    #[test]
    fn test_z_score_multi_anomaly() {
        let data = vec![1.0, 1.0, 1.0, 100.0, 100.0, 1.0];
        let anomalies = z_score_anomaly(&data, 1.0);
        assert_eq!(anomalies, vec![3, 4]);
    }

    #[test]
    fn test_isolation_forest() {
        let mut forest = IsolationForest::new(50, Some(10));
        let data: Vec<Vec<f64>> = (0..100)
            .map(|_| vec![rand::thread_rng().gen_range(0.0..10.0)])
            .collect();
        forest.fit(&data);
        let normal_score = forest.predict(&[5.0]);
        let outlier_score = forest.predict(&[100.0]);
        assert!(
            outlier_score > normal_score,
            "Outlier should have higher anomaly score: outlier={}, normal={}",
            outlier_score,
            normal_score
        );
    }

    #[test]
    fn test_isolation_forest_empty() {
        let forest = IsolationForest::new(10, Some(5));
        assert!((forest.predict(&[1.0]) - 0.5).abs() < 0.01);
    }

    #[test]
    fn test_rolling_stats_add() {
        let mut rs = RollingStats::new(3);
        rs.add(10.0);
        rs.add(20.0);
        rs.add(30.0);
        assert!((rs.mean() - 20.0).abs() < 1e-10);
        rs.add(40.0);
        assert!((rs.mean() - 30.0).abs() < 1e-10);
    }

    #[test]
    fn test_rolling_stats_std_dev() {
        let mut rs = RollingStats::new(5);
        for v in &[10.0, 12.0, 11.0, 13.0, 11.5] {
            rs.add(*v);
        }
        assert!(rs.std_dev() > 0.0);
    }

    #[test]
    fn test_rolling_stats_is_anomaly() {
        let mut rs = RollingStats::new(5);
        for v in &[10.0, 10.5, 9.5, 10.2, 10.3] {
            rs.add(*v);
        }
        assert!(!rs.is_anomaly(10.5, 3.0));
        assert!(rs.is_anomaly(50.0, 3.0));
    }

    #[test]
    fn test_rolling_stats_is_anomaly_insufficient() {
        let mut rs = RollingStats::new(5);
        rs.add(10.0);
        assert!(!rs.is_anomaly(100.0, 3.0));
    }
}
