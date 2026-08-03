from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.strategies import BacktestRequest
from app.services.strategies.registry import discover_strategies, list_strategies, get_strategy
from app.services.strategies.backtest import BacktestEngine
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/strategies", tags=["strategies"])


@router.get("")
async def get_strategies(user=Depends(get_current_user)):
    discover_strategies()
    return {"strategies": list_strategies()}


@router.get("/{name}")
async def get_strategy_detail(name: str, user=Depends(get_current_user)):
    discover_strategies()
    try:
        cls = get_strategy(name)
        instance = cls()
        info = instance.get_info()
        return {
            "name": info.name,
            "description": info.description,
            "version": info.version,
            "params": info.params,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{name}/params")
async def get_strategy_params(name: str, user=Depends(get_current_user)):
    discover_strategies()
    try:
        cls = get_strategy(name)
        instance = cls()
        return {"strategy": name, "params": instance.get_params()}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/backtest")
async def run_backtest(req: BacktestRequest, user=Depends(get_current_user)):
    engine = BacktestEngine(initial_capital=float(req.initial_capital))
    try:
        result = await engine.run(
            strategy_name=req.strategy_name,
            ticker=req.ticker,
            period=req.period,
            params=req.params or None,
        )
        return {
            "strategy": result.strategy_name,
            "ticker": result.ticker,
            "initial_capital": result.initial_capital,
            "final_value": result.final_value,
            "total_return_pct": result.total_return,
            "sharpe_ratio": result.sharpe_ratio,
            "max_drawdown_pct": result.max_drawdown,
            "win_rate_pct": result.win_rate,
            "total_trades": result.total_trades,
            "trades": result.trades,
            "equity_curve": result.equity_curve,
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
