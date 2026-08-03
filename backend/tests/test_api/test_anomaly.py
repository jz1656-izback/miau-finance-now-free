import pytest
from httpx import AsyncClient

from app.services.analytics.data_sources import detect_outliers


def test_detect_outliers_zscore():
    data = [10.0, 12.0, 11.0, 13.0, 100.0, 9.0, 11.5, 10.5]
    result = detect_outliers(data, method="zscore", threshold=2.0)
    assert result["outlier_count"] >= 1
    assert 100.0 in result["outlier_values"]
    assert result["method"] == "zscore"


def test_detect_outliers_no_anomaly():
    data = [10.0, 10.5, 9.8, 10.2, 10.1]
    result = detect_outliers(data, method="zscore", threshold=3.0)
    assert result["outlier_count"] == 0


def test_detect_outliers_empty():
    result = detect_outliers([], method="zscore")
    assert result["outlier_count"] == 0
    assert result["total"] == 0


def test_detect_outliers_single():
    result = detect_outliers([42.0], method="zscore")
    assert result["outlier_count"] == 0
    assert result["total"] == 1


def test_detect_outliers_iqr():
    data = [1, 2, 3, 4, 5, 100]
    result = detect_outliers(data, method="iqr")
    assert result["outlier_count"] >= 1
    assert result["method"] == "iqr"


def test_detect_outliers_constant():
    data = [5.0, 5.0, 5.0, 5.0]
    result = detect_outliers(data, method="zscore")
    assert result["outlier_count"] == 0


def test_detect_outliers_invalid_method():
    with pytest.raises(ValueError, match="Unknown method"):
        detect_outliers([1, 2, 3], method="invalid")


@pytest.mark.anyio
async def test_anomaly_endpoint(client: AsyncClient):
    resp = await client.get("/api/v1/market/indicators")
    assert resp.status_code == 200


def test_detect_outliers_all_outliers():
    data = [1.0, 1.0, 1.0, 100.0, 100.0, 1.0]
    result = detect_outliers(data, method="zscore", threshold=1.0)
    assert result["outlier_count"] >= 2


def test_detect_outliers_negative_values():
    data = [-100, -1, 0, 1, 2, 3]
    result = detect_outliers(data, method="zscore", threshold=2.0)
    assert result["total"] == 6
