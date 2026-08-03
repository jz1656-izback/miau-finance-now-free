"""Strategy NFT minting — users mint trading strategies as NFTs with metadata."""

import logging
import uuid
from datetime import timezone, datetime
from typing import Optional

logger = logging.getLogger(__name__)

_strategies: dict[str, dict] = {}


async def mint_strategy(name: str, author: str, description: str, code_hash: str, backtest_stats: dict) -> dict:
    sid = str(uuid.uuid4())[:8]
    strategy = {
        "id": sid,
        "name": name,
        "author": author,
        "description": description,
        "code_hash": code_hash,
        "backtest_stats": {
            "total_return_pct": backtest_stats.get("total_return_pct", 0),
            "sharpe_ratio": backtest_stats.get("sharpe_ratio", 0),
            "max_drawdown_pct": backtest_stats.get("max_drawdown_pct", 0),
            "win_rate_pct": backtest_stats.get("win_rate_pct", 0),
            "num_trades": backtest_stats.get("num_trades", 0),
        },
        "license": "standard",
        "price_miau": 0,
        "is_listed": False,
        "rating": 0.0,
        "downloads": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _strategies[sid] = strategy
    logger.info("Strategy minted: %s (%s)", name, sid)
    return strategy


async def get_strategy(strategy_id: str) -> Optional[dict]:
    return _strategies.get(strategy_id)


async def list_strategies(limit: int = 20, offset: int = 0) -> tuple[list[dict], int]:
    all_strats = [s for s in _strategies.values() if s.get("is_listed")]
    return all_strats[offset:offset + limit], len(all_strats)


async def list_my_strategies(author: str) -> list[dict]:
    return [s for s in _strategies.values() if s.get("author") == author]
