import logging
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

MAX_CONTEXT_TOKENS = 4000


def _count_tokens(text: str) -> int:
    """Count approximate tokens by splitting on whitespace."""
    return len(text.split())


def truncate_context(context: str | dict[str, Any], max_tokens: int = MAX_CONTEXT_TOKENS) -> tuple[Any, int]:
    if isinstance(context, dict):
        text_repr = str(context)
    else:
        text_repr = context

    token_count = _count_tokens(text_repr)
    if token_count <= max_tokens:
        return context, token_count

    if isinstance(context, dict):
        context = _truncate_dict(context, max_tokens)
        return context, _count_tokens(str(context))

    truncated = " ".join(text_repr.split()[:max_tokens]) + "\n[Context truncated...]"
    return truncated, max_tokens


def _truncate_dict(d: dict[str, Any], max_tokens: int) -> dict[str, Any]:
    """Truncate dict values until total token count is within limit.

    Truncates largest string/list values first, halving them iteratively
    until the overall token count falls below max_tokens.
    """
    current = str(d)
    token_count = _count_tokens(current)

    if token_count <= max_tokens:
        return d

    result = {k: v for k, v in d.items()}

    while token_count > max_tokens:
        largest_key = None
        largest_size = 0

        for key, value in result.items():
            if isinstance(value, str):
                size = _count_tokens(value)
                if size > largest_size:
                    largest_size = size
                    largest_key = key
            elif isinstance(value, list):
                size = len(value)
                if size > largest_size:
                    largest_size = size
                    largest_key = key

        if largest_key is None or largest_size <= 1:
            break

        value = result[largest_key]
        if isinstance(value, str):
            words = value.split()
            result[largest_key] = " ".join(words[:len(words) // 2])
        elif isinstance(value, list):
            result[largest_key] = value[-(len(value) // 2):]

        current = str(result)
        token_count = _count_tokens(current)

    return result


async def build_portfolio_context(db: AsyncSession, portfolio_id: str) -> dict[str, Any]:
    holdings = await _get_holdings(db, portfolio_id)
    performance = await _get_performance(db, portfolio_id)
    risk_metrics = await _get_risk_metrics_text(db, portfolio_id)

    return {
        "holdings": holdings or "No holdings data available",
        "performance": performance or "No performance data available",
        "risk_metrics": risk_metrics or "No risk metrics available",
    }


async def build_market_context() -> dict[str, Any]:
    market_data = await _get_market_data()
    sectors = await _get_sectors()
    indicators = await _get_indicators()
    news = await _get_news()

    return {
        "market_data": _format_market_data(market_data),
        "sectors": _format_sectors(sectors),
        "indicators": _format_indicators(indicators),
        "news_summary": _format_news(news),
    }


async def build_risk_context(portfolio_id: str) -> dict[str, Any]:
    risk_data = await _get_risk_data(portfolio_id)
    return {
        "var": risk_data.get("var_95", {}).get("var", "N/A") if isinstance(risk_data.get("var_95"), dict) else "N/A",
        "cvar": risk_data.get("var_95", {}).get("cvar", "N/A") if isinstance(risk_data.get("var_95"), dict) else "N/A",
        "max_drawdown": risk_data.get("max_drawdown", "N/A"),
        "volatility": risk_data.get("volatility", "N/A"),
        "correlations": risk_data.get("correlations", {}),
    }


async def _get_holdings(db: AsyncSession, portfolio_id: str) -> str:
    result = await db.execute(
        text("""
            SELECT i.ticker, i.name, p.quantity, p.market_value,
                   p.unrealized_pnl, p.realized_pnl, p.cost_basis
            FROM positions p
            JOIN instruments i ON i.id = p.instrument_id
            WHERE p.portfolio_id = :pid
            ORDER BY p.market_value DESC
        """),
        {"pid": portfolio_id},
    )
    rows = result.mappings().all()
    if not rows:
        return ""

    lines = ["Ticker | Name | Qty | Market Value | Unrealized PnL | Realized PnL"]
    lines.append("-" * 80)
    for r in rows:
        lines.append(
            f"{r['ticker']:>6} | {r['name'][:30]:30} | {float(r['quantity']):>8.2f} | "
            f"${float(r['market_value'] or 0):>10.2f} | ${float(r['unrealized_pnl'] or 0):>10.2f} | "
            f"${float(r['realized_pnl'] or 0):>8.2f}"
        )
    return "\n".join(lines)


async def _get_performance(db: AsyncSession, portfolio_id: str) -> str:
    result = await db.execute(
        text("""
            SELECT COALESCE(SUM(unrealized_pnl), 0) as total_unrealized,
                   COALESCE(SUM(realized_pnl), 0) as total_realized,
                   COALESCE(SUM(market_value), 0) as total_market_value,
                   COALESCE(SUM(cost_basis), 0) as total_cost_basis,
                   COUNT(*) as num_positions
            FROM positions
            WHERE portfolio_id = :pid
        """),
        {"pid": portfolio_id},
    )
    row = dict(result.mappings().first())
    total_pnl = row["total_unrealized"] + row["total_realized"]
    return_pct = 0
    if row["total_cost_basis"]:
        return_pct = ((row["total_market_value"] - row["total_cost_basis"]) / abs(row["total_cost_basis"])) * 100

    return (
        f"Total Market Value: ${float(row['total_market_value']):,.2f}\n"
        f"Total Cost Basis: ${float(row['total_cost_basis']):,.2f}\n"
        f"Total Unrealized PnL: ${float(row['total_unrealized']):,.2f}\n"
        f"Total Realized PnL: ${float(row['total_realized']):,.2f}\n"
        f"Total PnL: ${float(total_pnl):,.2f}\n"
        f"Return: {float(return_pct):.2f}%\n"
        f"Number of Positions: {row['num_positions']}"
    )


async def _get_risk_metrics_text(db: AsyncSession, portfolio_id: str) -> str:
    result = await db.execute(
        text("""
            SELECT metric_name, metric_value, metric_type, as_of_date
            FROM risk_metrics
            WHERE portfolio_id = :pid
            ORDER BY as_of_date DESC
        """),
        {"pid": portfolio_id},
    )
    rows = result.mappings().all()
    if not rows:
        return ""

    lines = ["Metric | Value | Type | Date"]
    lines.append("-" * 60)
    for r in rows:
        lines.append(
            f"{r['metric_name']:25} | {float(r['metric_value'] or 0):>10.4f} | "
            f"{r['metric_type'] or '':15} | {r['as_of_date'] or ''}"
        )
    return "\n".join(lines)


async def _get_market_data() -> Any:
    try:
        from app.services.analytics.market_data import get_market_movers
        return await get_market_movers()
    except Exception as e:
        logger.warning("Failed to get market data: %s", e)
        return None


async def _get_sectors() -> Any:
    try:
        from app.services.analytics._yf import get_sector_etfs
        return await get_sector_etfs()
    except Exception as e:
        logger.warning("Failed to get sectors: %s", e)
        return None


async def _get_indicators() -> Any:
    try:
        from app.services.analytics.market_data import fetch_live_prices
        return await fetch_live_prices(["SPY", "QQQ", "IWM"])
    except Exception as e:
        logger.warning("Failed to get indicators: %s", e)
        return None


async def _get_news() -> Any:
    try:
        from app.services.analytics.news import yahoo_finance_news
        return await yahoo_finance_news(limit=10)
    except Exception as e:
        logger.warning("Failed to get news: %s", e)
        return None


async def _get_risk_data(portfolio_id: str) -> dict[str, Any]:
    try:
        from app.services.analytics import risk as risk_service
        tickers = await _get_portfolio_tickers(portfolio_id)
        ticker = tickers[0] if tickers else "SPY"
        return await risk_service.comprehensive_risk(ticker)
    except Exception as e:
        logger.warning("Failed to get risk data: %s", e)
        return {}


async def _get_portfolio_tickers(portfolio_id: str) -> list[str]:
    try:
        from app.database import get_db
        from sqlalchemy import text
        async for db in get_db():
            result = await db.execute(
                text("""
                    SELECT DISTINCT i.ticker FROM positions p
                    JOIN instruments i ON i.id = p.instrument_id
                    WHERE p.portfolio_id = :pid
                """),
                {"pid": portfolio_id},
            )
            return [row[0] for row in result.all()]
    except Exception as e:
        logger.warning("Failed to get portfolio tickers: %s", e)
        return []


def _format_market_data(data: Any) -> str:
    if not data:
        return "No market data available"
    return str(data)[:1000]


def _format_sectors(sectors: Any) -> str:
    if not sectors:
        return "No sector data available"
    return str(sectors)[:500]


def _format_indicators(indicators: Any) -> str:
    if not indicators:
        return "No indicator data available"
    return str(indicators)[:500]


def _format_news(news: Any) -> str:
    if not news:
        return "No news available"
    headlines = []
    for article in (news if isinstance(news, list) else []):
        if isinstance(article, dict):
            headlines.append(article.get("title", ""))
    return "\n".join(headlines[:10])
