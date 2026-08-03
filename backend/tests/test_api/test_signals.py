import pytest
from httpx import AsyncClient
from unittest.mock import patch


@pytest.mark.anyio
async def test_generate_signals_happy_path(
    client: AsyncClient, mock_yf_history_many
):
    resp = await client.get(
        "/api/v1/signals/generate?ticker=AAPL&period=6mo", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert "trend" in data
    assert "signals" in data
    assert "indicators" in data


@pytest.mark.anyio
async def test_generate_signals_no_data(client: AsyncClient):
    with patch("app.services.analytics.signals.get_history", return_value=[]):
        resp = await client.get(
            "/api/v1/signals/generate?ticker=FAKE", 
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_generate_signals_default_ticker(
    client: AsyncClient, mock_yf_history_many
):
    resp = await client.get("/api/v1/signals/generate", )
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_multi_signal_happy_path(
    client: AsyncClient, mock_yf_history_many
):
    resp = await client.get(
        "/api/v1/signals/multi?tickers=AAPL,MSFT", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "signals" in data
    assert "AAPL" in data["signals"]
    assert "MSFT" in data["signals"]


@pytest.mark.anyio
async def test_multi_signal_default_tickers(
    client: AsyncClient, mock_yf_history_many
):
    resp = await client.get("/api/v1/signals/multi", )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["signals"]) >= 2


@pytest.mark.anyio
async def test_backtest_sma_cross_happy_path(
    client: AsyncClient, mock_yf_history_many
):
    resp = await client.get(
        "/api/v1/signals/backtest?ticker=AAPL&strategy=sma_cross&period=1y",
        
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["ticker"] == "AAPL"
    assert data["strategy"] == "sma_cross"
    assert "total_return_pct" in data
    assert "sharpe_ratio" in data
    assert "win_rate_pct" in data


@pytest.mark.anyio
async def test_backtest_unknown_strategy(
    client: AsyncClient, mock_yf_history_many
):
    resp = await client.get(
        "/api/v1/signals/backtest?ticker=AAPL&strategy=unknown", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_backtest_insufficient_data(client: AsyncClient):
    with patch("app.services.analytics.signals.get_history", return_value=[]):
        resp = await client.get(
            "/api/v1/signals/backtest?ticker=FAKE", 
        )
    assert resp.status_code == 200
    data = resp.json()
    assert "error" in data


@pytest.mark.anyio
async def test_backtest_custom_windows(
    client: AsyncClient, mock_yf_history_many
):
    resp = await client.get(
        "/api/v1/signals/backtest?ticker=AAPL&strategy=sma_cross&short_window=10&long_window=30&initial_capital=50000",
        
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["initial_capital"] == 50000


@pytest.mark.anyio
async def test_backtest_rsi_strategy(
    client: AsyncClient, mock_yf_history_many
):
    resp = await client.get(
        "/api/v1/signals/backtest?ticker=AAPL&strategy=rsi", 
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["strategy"] == "rsi"
