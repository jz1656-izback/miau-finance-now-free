use miau_analytics::anomaly::{z_score_anomaly, IsolationForest, RollingStats};

#[test]
fn test_z_score_anomaly_integration() {
    let data = vec![10.0, 12.0, 11.0, 13.0, 100.0, 9.0, 11.5, 10.5];
    let anomalies = z_score_anomaly(&data, 2.0);
    assert_eq!(anomalies, vec![4], "Should detect 100.0 as anomaly");
}

#[test]
fn test_z_score_anomaly_no_outliers() {
    let data = vec![100.0, 101.0, 99.0, 100.5, 101.5, 99.5];
    let anomalies = z_score_anomaly(&data, 3.0);
    assert!(anomalies.is_empty(), "No outliers expected in tight data");
}

#[test]
fn test_z_score_anomaly_empty() {
    let anomalies = z_score_anomaly(&[], 2.0);
    assert!(anomalies.is_empty());
}

#[test]
fn test_z_score_anomaly_single() {
    let anomalies = z_score_anomaly(&[42.0], 2.0);
    assert!(anomalies.is_empty());
}

#[test]
fn test_z_score_anomaly_identical() {
    let data = vec![5.0, 5.0, 5.0, 5.0];
    let anomalies = z_score_anomaly(&data, 3.0);
    assert!(anomalies.is_empty());
}

#[test]
fn test_z_score_anomaly_multiple() {
    let data = vec![1.0, 1.0, 1.0, 100.0, 100.0, 1.0];
    let anomalies = z_score_anomaly(&data, 1.0);
    assert_eq!(anomalies, vec![3, 4]);
}

#[test]
fn test_isolation_forest_integration() {
    let mut forest = IsolationForest::new(50, Some(10));
    let mut data = Vec::new();
    for _ in 0..100 {
        data.push(vec![rand::random::<f64>() * 10.0]);
    }
    forest.fit(&data);
    let normal_score = forest.predict(&[5.0]);
    let outlier_score = forest.predict(&[100.0]);
    assert!(
        outlier_score > normal_score,
        "Outlier should score higher: outlier={}, normal={}",
        outlier_score,
        normal_score
    );
}

#[test]
fn test_isolation_forest_empty() {
    let forest = IsolationForest::new(10, Some(5));
    let score = forest.predict(&[1.0]);
    assert!((score - 0.5).abs() < 0.01);
}

#[test]
fn test_isolation_forest_not_fitted() {
    let forest = IsolationForest::new(0, None);
    let score = forest.predict(&[1.0]);
    assert!((score - 0.5).abs() < 0.01);
}

#[test]
fn test_rolling_stats_integration() {
    let mut rs = RollingStats::new(3);
    rs.add(10.0);
    rs.add(20.0);
    rs.add(30.0);
    assert!((rs.mean() - 20.0).abs() < 1e-10);
    rs.add(40.0);
    assert!((rs.mean() - 30.0).abs() < 1e-10);
}

#[test]
fn test_rolling_stats_empty() {
    let rs = RollingStats::new(3);
    assert!((rs.mean() - 0.0).abs() < 1e-10);
    assert!((rs.std_dev() - 0.0).abs() < 1e-10);
}

#[test]
fn test_rolling_stats_anomaly_detection() {
    let mut rs = RollingStats::new(5);
    for &v in &[10.0, 10.5, 9.5, 10.2, 10.3] {
        rs.add(v);
    }
    assert!(!rs.is_anomaly(10.5, 3.0));
    assert!(rs.is_anomaly(50.0, 3.0));
}

#[test]
fn test_rolling_stats_anomaly_insufficient_data() {
    let mut rs = RollingStats::new(5);
    rs.add(10.0);
    assert!(!rs.is_anomaly(100.0, 3.0));
}

#[test]
fn test_rolling_stats_window_size() {
    let mut rs = RollingStats::new(2);
    rs.add(1.0);
    rs.add(2.0);
    rs.add(3.0);
    assert!((rs.mean() - 2.5).abs() < 1e-10);
}
