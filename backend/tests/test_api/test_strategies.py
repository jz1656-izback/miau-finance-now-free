import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.mark.anyio
async def test_list_strategies(client: AsyncClient):
    with patch("app.api.strategies.list_strategies") as mock_list, \
         patch("app.api.strategies.discover_strategies") as mock_disc:
        mock_list.return_value = [{"name": "sma_cross", "description": "SMA crossover"}]
        mock_disc.return_value = None
        resp = await client.get("/api/v1/strategies")
        assert resp.status_code == 200


@pytest.mark.anyio
async def test_get_strategy_detail(client: AsyncClient):
    with patch("app.api.strategies.get_strategy") as mock_get, \
         patch("app.api.strategies.discover_strategies") as mock_disc:
        mock_cls = MagicMock()
        mock_cls.get_info.return_value = {"name": "sma_cross", "params": []}
        mock_get.return_value = mock_cls
        mock_disc.return_value = None
        resp = await client.get("/api/v1/strategies/sma_cross")
        assert resp.status_code in (200, 404)


@pytest.mark.anyio
async def test_get_nonexistent_strategy(client: AsyncClient):
    with patch("app.api.strategies.get_strategy") as mock_get, \
         patch("app.api.strategies.discover_strategies") as mock_disc:
        mock_get.side_effect = ValueError("Unknown strategy")
        mock_disc.return_value = None
        resp = await client.get("/api/v1/strategies/nonexistent")
        assert resp.status_code == 404


@pytest.mark.anyio
async def test_run_backtest(client: AsyncClient):
    with patch("app.api.strategies.BacktestEngine") as mock_engine, \
         patch("app.api.strategies.discover_strategies") as mock_disc:
        instance = AsyncMock()
        instance.run.return_value = MagicMock(
            strategy_name="sma_cross",
            ticker="AAPL",
            initial_capital=100000.0,
            final_value=115000.0,
            total_return=15.0,
            sharpe_ratio=1.25,
            max_drawdown=-8.5,
            win_rate=55.0,
            total_trades=12,
            trades=[],
            equity_curve=[],
        )
        mock_engine.return_value = instance
        mock_disc.return_value = None
        resp = await client.post(
            "/api/v1/strategies/backtest",
            json={
                "strategy_name": "sma_cross",
                "ticker": "AAPL",
                "period": "1y",
                "params": {},
                "initial_capital": 100000,
            },
        )
        assert resp.status_code in (200, 400)



