from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

_leaderboard_cache: dict[str, tuple[list[dict], str]] = {}


async def calculate_leaderboard(
    db: AsyncSession,
    metric: str = "total_return",
    period: str = "all_time",
    limit: int = 20,
) -> list[dict]:
    cache_key = f"{metric}:{period}:{limit}"
    cached = _leaderboard_cache.get(cache_key)
    if cached:
        return cached[0]

    if period == "weekly":
        date_filter = "AND p.as_of_date >= NOW() - INTERVAL '7 days'"
    elif period == "monthly":
        date_filter = "AND p.as_of_date >= NOW() - INTERVAL '30 days'"
    else:
        date_filter = ""

    col_map = {
        "total_return": "COALESCE(SUM(p.unrealized_pnl + p.realized_pnl), 0) / NULLIF(ABS(COALESCE(SUM(p.cost_basis), 1)), 0) * 100",
        "sharpe_ratio": "COALESCE(AVG(r.metric_value), 0)",
        "gain_amount": "COALESCE(SUM(p.unrealized_pnl + p.realized_pnl), 0)",
    }
    order_col = col_map.get(metric, col_map["total_return"])

    query = text(f"""
        SELECT u.id, u.username,
               {order_col} as metric_value,
               COUNT(DISTINCT p.id) as position_count
        FROM users u
        JOIN portfolios po ON po.ontology_object_id IS NOT NULL
        LEFT JOIN positions p ON p.portfolio_id = po.id {date_filter}
        LEFT JOIN risk_metrics r ON r.portfolio_id = po.id AND r.metric_name = 'sharpe_ratio'
        GROUP BY u.id, u.username
        ORDER BY metric_value DESC
        LIMIT :limit
    """)
    result = await db.execute(query, {"limit": limit})
    rows = [dict(r) for r in result.mappings().all()]
    ranked = [
        {"rank": i + 1, "user_id": str(r["id"]), "username": r["username"], "value": round(float(r["metric_value"]), 4), "positions": r["position_count"]}
        for i, r in enumerate(rows)
    ]
    _leaderboard_cache[cache_key] = (ranked, "cached")
    return ranked
