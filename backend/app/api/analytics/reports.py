import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from app.database import get_db
from app.services.analytics import reporting as reporting_service
from app.services.analytics.valuation import build_dcf, calculate_wacc, comparable_analysis, lbo_model

router = APIRouter()


@router.get("/portfolio/{portfolio_id}")
async def portfolio_report(portfolio_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("SELECT * FROM portfolios WHERE id = :id"), {"id": portfolio_id}
    )
    pf = result.mappings().first()
    if not pf:
        raise HTTPException(404, "Portfolio not found")

    positions = await db.execute(
        text("""
            SELECT pos.*, i.ticker, i.name as instrument_name, i.instrument_type
            FROM positions pos JOIN instruments i ON pos.instrument_id = i.id
            WHERE pos.portfolio_id = :pid
        """),
        {"pid": portfolio_id},
    )
    pos_list = [dict(r) for r in positions.mappings().all()]

    pnl = await db.execute(
        text("""
            SELECT DATE(to_date) as date, portfolio_id, pnl_type, SUM(pnl_amount) as total_pnl
            FROM pnl WHERE portfolio_id = :pid
            GROUP BY DATE(to_date), portfolio_id, pnl_type
            ORDER BY date DESC LIMIT 60
        """),
        {"pid": portfolio_id},
    )
    pnl_list = [dict(r) for r in pnl.mappings().all()]

    risk = await db.execute(
        text("""
            SELECT * FROM risk_metrics WHERE portfolio_id = :pid ORDER BY as_of_date DESC
        """),
        {"pid": portfolio_id},
    )
    risk_list = [dict(r) for r in risk.mappings().all()]

    summary = {
        "name": pf.name,
        "portfolio_type": pf.portfolio_type,
        "total_market_value": sum(p.get("market_value", 0) or 0 for p in pos_list),
        "total_unrealized_pnl": sum(p.get("unrealized_pnl", 0) or 0 for p in pos_list),
        "num_positions": len(pos_list),
        "num_trades": 0,
    }
    total = (summary["total_market_value"] - summary["total_unrealized_pnl"])
    summary["return_pct"] = round((summary["total_unrealized_pnl"] / total * 100), 2) if total != 0 else 0

    pdf_buf = reporting_service.generate_portfolio_report(
        pf.name, summary, pos_list, pnl_list, risk_list,
    )
    return Response(
        content=pdf_buf.read(),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={pf.name}_report.pdf",
        },
    )


@router.get("/portfolio/{portfolio_id}/excel")
async def portfolio_excel(portfolio_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT pos.*, i.ticker, i.name as instrument_name, i.instrument_type,
                   p.name as portfolio_name
            FROM positions pos
            JOIN instruments i ON pos.instrument_id = i.id
            JOIN portfolios p ON pos.portfolio_id = p.id
            WHERE pos.portfolio_id = :pid
        """),
        {"pid": portfolio_id},
    )
    positions = [dict(r) for r in result.mappings().all()]
    if not positions:
        raise HTTPException(404, "No positions found")

    buf = await reporting_service.export_positions_to_excel(positions)
    return Response(
        content=buf.read(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=positions.xlsx"},
    )


@router.get("/portfolio/{portfolio_id}/json")
async def portfolio_json(portfolio_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("SELECT * FROM portfolios WHERE id = :id"), {"id": portfolio_id}
    )
    pf = result.mappings().first()
    if not pf:
        raise HTTPException(404, "Portfolio not found")

    positions = await db.execute(
        text("""
            SELECT pos.*, i.ticker, i.name as instrument_name, i.instrument_type
            FROM positions pos JOIN instruments i ON pos.instrument_id = i.id
            WHERE pos.portfolio_id = :pid
        """),
        {"pid": portfolio_id},
    )
    pos_list = [dict(r) for r in positions.mappings().all()]

    for p in pos_list:
        for k, v in p.items():
            if hasattr(v, "isoformat"):
                p[k] = v.isoformat()

    import json as json_lib
    return Response(
        content=json_lib.dumps({
            "portfolio": {
                "id": str(pf.id),
                "name": pf.name,
                "type": pf.portfolio_type,
                "currency": pf.base_currency,
            },
            "summary": {
                "total_market_value": sum(p.get("market_value", 0) or 0 for p in pos_list),
                "total_unrealized_pnl": sum(p.get("unrealized_pnl", 0) or 0 for p in pos_list),
                "num_positions": len(pos_list),
            },
            "positions": [{
                "ticker": p["ticker"],
                "name": p.get("instrument_name"),
                "quantity": float(p.get("quantity", 0)),
                "average_price": float(p.get("average_price", 0)) if p.get("average_price") else None,
                "market_value": float(p.get("market_value", 0)) if p.get("market_value") else 0,
                "unrealized_pnl": float(p.get("unrealized_pnl", 0)) if p.get("unrealized_pnl") else 0,
            } for p in pos_list],
        }, indent=2, default=str),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={pf.name}_export.json"},
    )


@router.get("/portfolio/{portfolio_id}/csv")
async def portfolio_csv(portfolio_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT pos.*, i.ticker, i.name as instrument_name, i.instrument_type,
                   p.name as portfolio_name
            FROM positions pos
            JOIN instruments i ON pos.instrument_id = i.id
            JOIN portfolios p ON pos.portfolio_id = p.id
            WHERE pos.portfolio_id = :pid
        """),
        {"pid": portfolio_id},
    )
    positions = [dict(r) for r in result.mappings().all()]
    if not positions:
        raise HTTPException(404, "No positions found")

    csv = await reporting_service.export_trades_to_csv(positions)
    pf_name = positions[0].get("portfolio_name", "portfolio")
    return Response(
        content=csv,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={pf_name}_positions.csv"},
    )


@router.get("/trades/csv")
async def trades_csv(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT t.*, i.ticker, p.name as portfolio_name
            FROM trades t
            JOIN instruments i ON t.instrument_id = i.id
            LEFT JOIN portfolios p ON t.portfolio_id = p.id
            ORDER BY t.trade_date DESC LIMIT 1000
        """)
    )
    trades = [dict(r) for r in result.mappings().all()]
    csv = await reporting_service.export_trades_to_csv(trades)
    return Response(
        content=csv,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=trades.csv"},
    )


@router.get("/valuation/{ticker}")
async def valuation_export(
    ticker: str,
    models: str = Query("dcf,wacc,comps,lbo", description="Comma-separated list of models"),
):
    """Export valuation models as CSV."""
    import httpx
    model_list = [m.strip() for m in models.split(",")]
    rows = []

    async def fetch_json(url: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                resp = await client.get(url)
                if resp.status_code == 200:
                    return resp.json()
        except Exception:
            pass
        return {}

    base = f"http://localhost:8000/api/v1/analytics/valuation"

    if "dcf" in model_list:
        dcf = await build_dcf(ticker)
        if dcf:
            row = {"model": "DCF", "ticker": ticker}
            row.update({k: dcf.get(k, "") for k in ["dcf_value", "current_price", "upside_pct", "recommendation", "wacc", "growth_rate", "terminal_growth"]})
            rows.append(row)

    if "wacc" in model_list:
        wacc = await calculate_wacc(ticker)
        if wacc:
            row = {"model": "WACC", "ticker": ticker}
            row.update({k: wacc.get(k, "") for k in ["wacc", "cost_of_equity", "cost_of_debt", "tax_rate", "market_cap", "total_debt", "beta"]})
            rows.append(row)

    if "comps" in model_list:
        comps = await comparable_analysis(ticker)
        if comps:
            row = {"model": "Comps", "ticker": ticker}
            row.update({k: comps.get(k, "") for k in ["pe_ratio", "ev_ebitda", "price_to_book", "price_to_sales", "eps", "sector", "industry"]})
            rows.append(row)

    if "lbo" in model_list:
        lbo = await lbo_model(ticker)
        if lbo:
            row = {"model": "LBO", "ticker": ticker}
            row.update({k: lbo.get(k, "") for k in ["entry_ev", "exit_ev", "moic", "irr_pct", "entry_debt", "entry_equity", "debt_pct", "exit_multiple", "verdict"]})
            rows.append(row)

    buf = io.StringIO()
    if rows:
        writer = csv.DictWriter(buf, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    csv_content = buf.getvalue()
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={ticker}_valuation.csv"},
    )
