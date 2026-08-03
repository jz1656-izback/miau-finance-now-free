import csv
import io
import json
from datetime import timezone, datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.services.currency_service import convert_amount, update_portfolio_currency

from fastapi.responses import StreamingResponse

router = APIRouter()


async def get_current_user_db(
    db: AsyncSession = Depends(get_db),
    token_user: dict = Depends(get_current_user),
) -> dict:
    username = token_user.get("sub")
    result = await db.execute(
        text("SELECT id, username, email, role FROM users WHERE username = :username"),
        {"username": username},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(401, "User not found")
    return dict(row)


@router.get("")
async def list_portfolios(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("""
            SELECT p.*,
                   COUNT(DISTINCT pos.instrument_id) as num_positions,
                   COALESCE(SUM(pos.market_value), 0) as total_value
            FROM portfolios p
            LEFT JOIN positions pos ON pos.portfolio_id = p.id
            GROUP BY p.id
            ORDER BY p.name
        """)
    )
    return [dict(row) for row in result.mappings().all()]


@router.get("/{portfolio_id}")
async def get_portfolio(portfolio_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("SELECT * FROM portfolios WHERE id = :id"), {"id": portfolio_id}
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, "Portfolio not found")
    base = row["base_currency"] or "USD"

    positions = await db.execute(
        text("""
            SELECT pos.*, i.ticker, i.name as instrument_name, i.instrument_type
            FROM positions pos
            JOIN instruments i ON pos.instrument_id = i.id
            WHERE pos.portfolio_id = :pid
        """),
        {"pid": portfolio_id},
    )
    pos_list = []
    for r in positions.mappings().all():
        d = dict(r)
        pos_currency = d.get("currency", "USD")
        if pos_currency != base:
            for field in ("market_value", "cost_basis", "unrealized_pnl", "realized_pnl"):
                val = d.get(field)
                if val is not None:
                    converted = await convert_amount(db, Decimal(str(val)), pos_currency, base)
                    if converted is not None:
                        d[field] = float(converted)
        pos_list.append(d)

    return {
        **dict(row),
        "positions": pos_list,
    }


@router.get("/{portfolio_id}/positions")
async def get_positions(portfolio_id: UUID, db: AsyncSession = Depends(get_db)):
    pf = await db.execute(
        text("SELECT base_currency FROM portfolios WHERE id = :pid"),
        {"pid": portfolio_id},
    )
    pf_row = pf.mappings().first()
    base = pf_row["base_currency"] or "USD" if pf_row else "USD"

    result = await db.execute(
        text("""
            SELECT pos.*, i.ticker, i.name as instrument_name,
                   i.instrument_type, i.sector
            FROM positions pos
            JOIN instruments i ON pos.instrument_id = i.id
            WHERE pos.portfolio_id = :pid
            ORDER BY ABS(pos.market_value) DESC
        """),
        {"pid": portfolio_id},
    )
    pos_list = []
    for r in result.mappings().all():
        d = dict(r)
        pos_currency = d.get("currency", "USD")
        if pos_currency != base:
            for field in ("market_value", "cost_basis", "unrealized_pnl", "realized_pnl"):
                val = d.get(field)
                if val is not None:
                    converted = await convert_amount(db, Decimal(str(val)), pos_currency, base)
                    if converted is not None:
                        d[field] = float(converted)
        pos_list.append(d)
    return pos_list


@router.get("/{portfolio_id}/trades")
async def get_portfolio_trades(
    portfolio_id: UUID,
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        text("""
            SELECT t.*, i.ticker, i.name as instrument_name
            FROM trades t
            JOIN instruments i ON t.instrument_id = i.id
            WHERE t.portfolio_id = :pid
            ORDER BY t.trade_date DESC
            LIMIT :limit
        """),
        {"pid": portfolio_id, "limit": limit},
    )
    return [dict(row) for row in result.mappings().all()]


@router.post("/{portfolio_id}/share")
async def share_portfolio(
    portfolio_id: UUID,
    workspace_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    portfolio = await db.execute(
        text("SELECT id FROM portfolios WHERE id = :id"),
        {"id": portfolio_id},
    )
    if not portfolio.mappings().first():
        raise HTTPException(404, "Portfolio not found")

    workspace = await db.execute(
        text("SELECT id FROM workspaces WHERE id = :id"),
        {"id": workspace_id},
    )
    if not workspace.mappings().first():
        raise HTTPException(404, "Workspace not found")

    result = await db.execute(
        text("""
            INSERT INTO portfolio_shares (id, portfolio_id, workspace_id, shared_by)
            VALUES (gen_random_uuid(), :portfolio_id, :workspace_id, :shared_by)
            RETURNING id, portfolio_id, workspace_id, shared_by, created_at
        """),
        {"portfolio_id": portfolio_id, "workspace_id": workspace_id, "shared_by": current_user["id"]},
    )
    await db.commit()
    return dict(result.mappings().first())


@router.delete("/{portfolio_id}/share/{workspace_id}")
async def unshare_portfolio(
    portfolio_id: UUID,
    workspace_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            DELETE FROM portfolio_shares
            WHERE portfolio_id = :portfolio_id AND workspace_id = :workspace_id AND shared_by = :user_id
            RETURNING id
        """),
        {"portfolio_id": portfolio_id, "workspace_id": workspace_id, "user_id": current_user["id"]},
    )
    await db.commit()
    if not result.rowcount:
        raise HTTPException(404, "Share not found")
    return {"message": "Portfolio unshared"}


@router.get("/shared")
async def list_shared_portfolios(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            SELECT ps.id, ps.portfolio_id, ps.workspace_id, ps.shared_by, ps.created_at,
                   p.name as portfolio_name, w.name as workspace_name,
                   u.username as shared_by_username
            FROM portfolio_shares ps
            JOIN portfolios p ON p.id = ps.portfolio_id
            JOIN workspaces w ON w.id = ps.workspace_id
            JOIN users u ON u.id = ps.shared_by
            WHERE ps.workspace_id IN (
                SELECT wm.workspace_id FROM workspace_members wm WHERE wm.user_id = :user_id
                UNION
                SELECT t.id FROM teams t WHERE t.owner_id = :owner_id
            )
            ORDER BY ps.created_at DESC
        """),
        {"user_id": current_user["id"], "owner_id": current_user["id"]},
    )
    return [dict(row) for row in result.mappings().all()]


@router.put("/{portfolio_id}/currency")
async def set_portfolio_currency(
    portfolio_id: str,
    currency: str = Query(..., min_length=3, max_length=5),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    result = await update_portfolio_currency(db, portfolio_id, currency.upper(), current_user["id"])
    if result is None:
        raise HTTPException(404, "Portfolio not found")
    return result


@router.get("/{portfolio_id}/export")
async def export_portfolio(
    portfolio_id: str,
    format: str = Query("json", pattern="^(json|csv|pdf)$"),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_db),
):
    uid = current_user["id"]
    portfolio = await db.execute(
        text("SELECT id, name, base_currency FROM portfolios WHERE id = :pid AND id IN "
             "(SELECT portfolio_id FROM positions WHERE portfolio_id = :pid2)"),
        {"pid": portfolio_id, "uid": uid, "pid2": portfolio_id},
    )
    pf = portfolio.mappings().first()
    if not pf:
        raise HTTPException(404, "Portfolio not found")

    owner = await db.execute(
        text("SELECT 1 FROM portfolios WHERE id = :pid AND id IN "
             "(SELECT p.id FROM portfolios p JOIN positions pos ON pos.portfolio_id = p.id WHERE p.id = :pid2)"),
        {"pid": portfolio_id, "uid": uid, "pid2": portfolio_id},
    )
    if not owner.mappings().first():
        raise HTTPException(403, "Access denied")

    positions = await db.execute(
        text("""
            SELECT pos.ticker, pos.quantity, pos.average_price, pos.market_value,
                   pos.unrealized_pnl, pos.realized_pnl, pos.currency
            FROM positions pos
            WHERE pos.portfolio_id = :pid
            ORDER BY pos.ticker
        """),
        {"pid": portfolio_id},
    )
    rows = [dict(r) for r in positions.mappings().all()]
    now = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"portfolio_{pf['name']}_{now}"

    if format == "csv":
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=["ticker", "quantity", "average_price", "market_value", "unrealized_pnl", "realized_pnl", "currency"])
        writer.writeheader()
        for r in rows:
            r["average_price"] = float(r["average_price"]) if r["average_price"] else 0
            r["market_value"] = float(r["market_value"]) if r["market_value"] else 0
            r["unrealized_pnl"] = float(r["unrealized_pnl"]) if r["unrealized_pnl"] else 0
            r["realized_pnl"] = float(r["realized_pnl"]) if r["realized_pnl"] else 0
            writer.writerow(r)
        buf.seek(0)
        return StreamingResponse(
            iter([buf.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}.csv"'},
        )

    if format == "pdf":
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet
        except ImportError:
            raise HTTPException(501, "PDF generation requires reportlab")
        pdf_buf = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buf, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        elements = [
            Paragraph("Miau Finance — Portfolio Report", styles["Title"]),
            Spacer(1, 12),
            Paragraph(f"<b>Name:</b> {pf['name']}", styles["Normal"]),
            Paragraph(f"<b>Currency:</b> {pf['base_currency']}", styles["Normal"]),
            Paragraph(f"<b>Generated:</b> {datetime.now(timezone.utc).isoformat()}", styles["Normal"]),
            Spacer(1, 20),
        ]
        if rows:
            data = [["Ticker", "Qty", "Price", "Market Value", "P&L"]]
            for r in rows:
                mv = float(r.get("market_value", 0) or 0)
                upnl = float(r.get("unrealized_pnl", 0) or 0)
                data.append([r["ticker"], str(r["quantity"]), f"${float(r['average_price'] or 0):.2f}", f"${mv:,.2f}", f"${upnl:+,.2f}"])
            t = Table(data, colWidths=[60, 50, 70, 90, 80])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0, 0.78, 0.53)),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.Color(0.8, 0.8, 0.8)),
            ]))
            elements.append(t)
        else:
            elements.append(Paragraph("<i>No positions.</i>", styles["Normal"]))
        doc.build(elements)
        pdf_buf.seek(0)
        return StreamingResponse(
            iter([pdf_buf.getvalue()]),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{filename}.pdf"'},
        )

    return {
        "portfolio": {"id": str(pf["id"]), "name": pf["name"], "base_currency": pf["base_currency"]},
        "positions": [
            {
                "ticker": r["ticker"],
                "quantity": float(r["quantity"]),
                "average_price": float(r["average_price"]) if r["average_price"] else 0,
                "market_value": float(r["market_value"]) if r["market_value"] else 0,
                "unrealized_pnl": float(r["unrealized_pnl"]) if r["unrealized_pnl"] else 0,
                "realized_pnl": float(r["realized_pnl"]) if r["realized_pnl"] else 0,
                "currency": r["currency"],
            }
            for r in rows
        ],
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "total_positions": len(rows),
        "total_value": sum(float(r["market_value"] or 0) for r in rows),
    }
