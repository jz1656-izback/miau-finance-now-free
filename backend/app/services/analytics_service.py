from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional


async def calculate_portfolio_pnl(db: AsyncSession, portfolio_id: UUID):
    result = await db.execute(
        text("""
            SELECT
                COALESCE(SUM(unrealized_pnl), 0) as total_unrealized_pnl,
                COALESCE(SUM(realized_pnl), 0) as total_realized_pnl,
                COALESCE(SUM(market_value), 0) as total_market_value,
                COALESCE(SUM(cost_basis), 0) as total_cost_basis
            FROM positions
            WHERE portfolio_id = :pid
        """),
        {"pid": portfolio_id},
    )
    return dict(result.mappings().first())


async def get_portfolio_summary(db: AsyncSession, portfolio_id: UUID):
    result = await db.execute(
        text("""
            SELECT
                p.id, p.name, p.portfolio_type, p.base_currency,
                p.management_style,
                COUNT(DISTINCT pos.instrument_id) as num_positions,
                COALESCE(SUM(pos.market_value), 0) as total_market_value,
                COALESCE(SUM(pos.unrealized_pnl), 0) as total_unrealized_pnl,
                COALESCE(SUM(pos.realized_pnl), 0) as total_realized_pnl,
                COUNT(DISTINCT t.id) as num_trades,
                COALESCE(SUM(pos.market_value) - SUM(pos.cost_basis), 0) as total_pnl
            FROM portfolios p
            LEFT JOIN positions pos ON pos.portfolio_id = p.id
            LEFT JOIN trades t ON t.portfolio_id = p.id
            WHERE p.id = :pid
            GROUP BY p.id, p.name, p.portfolio_type, p.base_currency, p.management_style
        """),
        {"pid": portfolio_id},
    )
    return dict(result.mappings().first()) if result else None


async def get_instrument_performance(db: AsyncSession, instrument_id: UUID):
    result = await db.execute(
        text("""
            SELECT
                i.id, i.ticker, i.name, i.instrument_type,
                pos.quantity, pos.average_price, pos.market_value,
                pos.unrealized_pnl, pos.realized_pnl,
                ROUND(
                    CASE WHEN pos.cost_basis != 0
                    THEN ((pos.market_value - pos.cost_basis) / ABS(pos.cost_basis)) * 100
                    ELSE 0 END, 2
                ) as return_pct
            FROM instruments i
            JOIN positions pos ON pos.instrument_id = i.id
            WHERE i.id = :iid
        """),
        {"iid": instrument_id},
    )
    return [dict(row) for row in result.mappings().all()]


async def get_pnl_timeseries(db: AsyncSession, portfolio_id: Optional[UUID] = None, days: int = 30):
    params = {"days": days}
    where = ""
    if portfolio_id:
        where = "AND portfolio_id = :pid"
        params["pid"] = portfolio_id

    result = await db.execute(
        text(f"""
            SELECT
                DATE(to_date) as date,
                portfolio_id,
                pnl_type,
                SUM(pnl_amount) as total_pnl
            FROM pnl
            WHERE to_date >= NOW() - INTERVAL ':days days'
            {where}
            GROUP BY DATE(to_date), portfolio_id, pnl_type
            ORDER BY date DESC
        """),
        params,
    )
    return [dict(row) for row in result.mappings().all()]


async def get_portfolio_risk_metrics(db: AsyncSession, portfolio_id: UUID):
    result = await db.execute(
        text("""
            SELECT metric_name, metric_value, metric_type, currency, as_of_date
            FROM risk_metrics
            WHERE portfolio_id = :pid
            ORDER BY as_of_date DESC
        """),
        {"pid": portfolio_id},
    )
    return [dict(row) for row in result.mappings().all()]


async def get_summary_dashboard(db: AsyncSession):
    result = await db.execute(text("""
        SELECT
            COUNT(DISTINCT p.id) as total_portfolios,
            COUNT(DISTINCT i.id) as total_instruments,
            COUNT(DISTINCT t.id) as total_trades,
            COALESCE(SUM(pos.market_value), 0) as total_aum,
            COALESCE(SUM(pos.unrealized_pnl), 0) as total_unrealized_pnl,
            COALESCE(SUM(pos.realized_pnl), 0) as total_realized_pnl
        FROM portfolios p
        LEFT JOIN positions pos ON pos.portfolio_id = p.id
        LEFT JOIN instruments i ON 1=1
        LEFT JOIN trades t ON 1=1
    """))
    return dict(result.mappings().first())
