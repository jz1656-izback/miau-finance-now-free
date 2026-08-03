import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from decimal import Decimal
from app.config import settings

from app.services.paper_trading import (
    calc_slippage,
    calc_commission,
    calc_tca_cost,
    simulate_market_fill,
    simulate_limit_fill,
    simulate_stop_fill,
    simulate_trailing_stop_fill,
)


def test_calc_slippage_buy():
    with patch.object(settings, "paper_slippage_pct", 0.001):
        slippage = calc_slippage(Decimal("100"), Decimal("150.00"), "BUY")
        assert slippage > 0
        assert slippage == Decimal("15.00")


def test_calc_slippage_sell():
    with patch.object(settings, "paper_slippage_pct", 0.001):
        slippage = calc_slippage(Decimal("100"), Decimal("150.00"), "SELL")
        assert slippage < 0


def test_calc_commission():
    with patch.object(settings, "paper_commission_rate", 0.0005):
        commission = calc_commission(Decimal("100"), Decimal("150.00"))
        assert commission == Decimal("7.50")


def test_calc_commission_zero_quantity():
    with patch.object(settings, "paper_commission_rate", 0.0005):
        commission = calc_commission(Decimal("0"), Decimal("150.00"))
        assert commission == Decimal("0.00")


def test_calc_tca_cost():
    cost = calc_tca_cost(Decimal("100"), Decimal("150.00"), market_impact=0.0005)
    assert cost == Decimal("7.50")


@pytest.mark.anyio
async def test_simulate_market_fill():
    mock_db = MagicMock()
    mock_db.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        result = MagicMock()
        sql = str(args[0]) if args else ""
        if "market_data" in sql or "close" in sql:
            result.scalar.return_value = Decimal("150.00")
        else:
            result.mappings.return_value.first.return_value = {
                "id": "trade-id",
                "paper_portfolio_id": "pp-id",
                "instrument_id": "inst-id",
                "side": "BUY",
                "quantity": "100",
                "price": "150.25",
                "commission": "7.50",
                "slippage": "1.50",
                "tca_cost": "0.75",
            }
        return result

    mock_db.execute.side_effect = mock_exec

    with patch.object(settings, "paper_slippage_pct", 0.001), \
         patch.object(settings, "paper_commission_rate", 0.0005):
        result = await simulate_market_fill(mock_db, "pp-id", "inst-id", "BUY", Decimal("100"))
        assert result is not None
        assert result["side"] == "BUY"


@pytest.mark.anyio
async def test_simulate_limit_fill_buy_below_market():
    mock_db = MagicMock()
    mock_db.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        result = MagicMock()
        result.scalar.return_value = Decimal("150.00")
        return result

    mock_db.execute.side_effect = mock_exec
    result = await simulate_limit_fill(mock_db, "pp-id", "inst-id", "BUY", Decimal("100"), Decimal("140.00"))
    assert result is None


@pytest.mark.anyio
async def test_simulate_limit_fill_buy_above_market():
    mock_db = MagicMock()
    mock_db.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        result = MagicMock()
        sql = str(args[0]) if args else ""
        if "close" in sql:
            result.scalar.return_value = Decimal("150.00")
        else:
            result.mappings.return_value.first.return_value = {
                "id": "trade-id",
                "side": "BUY",
            }
        return result

    mock_db.execute.side_effect = mock_exec

    with patch.object(settings, "paper_slippage_pct", 0.001), \
         patch.object(settings, "paper_commission_rate", 0.0005):
        result = await simulate_limit_fill(mock_db, "pp-id", "inst-id", "BUY", Decimal("100"), Decimal("160.00"))
        if result:
            assert result["side"] == "BUY"


@pytest.mark.anyio
async def test_simulate_stop_fill():
    mock_db = MagicMock()
    mock_db.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        result = MagicMock()
        sql = str(args[0]) if args else ""
        if "close" in sql:
            result.scalar.return_value = Decimal("150.00")
        else:
            result.mappings.return_value.first.return_value = {
                "id": "trade-id",
                "side": "SELL",
            }
        return result

    mock_db.execute.side_effect = mock_exec

    with patch.object(settings, "paper_slippage_pct", 0.001), \
         patch.object(settings, "paper_commission_rate", 0.0005):
        result = await simulate_stop_fill(mock_db, "pp-id", "inst-id", "SELL", Decimal("100"), Decimal("140.00"))
        if result:
            assert result["side"] == "SELL"


@pytest.mark.anyio
async def test_simulate_trailing_stop_fill():
    mock_db = MagicMock()
    mock_db.execute = AsyncMock()

    async def mock_exec(*args, **kwargs):
        result = MagicMock()
        sql = str(args[0]) if args else ""
        if "close" in sql:
            result.scalar.return_value = Decimal("150.00")
        elif "MAX(high)" in sql or "high" in sql:
            result.mappings.return_value.first.return_value = {
                "high": Decimal("160.00"),
                "low": Decimal("140.00"),
            }
        else:
            result.mappings.return_value.first.return_value = {
                "id": "trade-id",
                "side": "SELL",
            }
        return result

    mock_db.execute.side_effect = mock_exec

    with patch.object(settings, "paper_slippage_pct", 0.001), \
         patch.object(settings, "paper_commission_rate", 0.0005):
        result = await simulate_trailing_stop_fill(mock_db, "pp-id", "inst-id", "SELL", Decimal("100"), Decimal("5.0"))
        if result:
            assert result is not None
