import io
import logging
import os
from datetime import date, timedelta
from decimal import Decimal
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")

FREE_REQUESTS = 0        # Tamagotchi: no data
TRIAL_REQUESTS = 1500    # ~50/day for 30 days
STARTER_REQUESTS = 15000 # ~500/day
PRO_REQUESTS = 90000     # ~3000/day
FUND_REQUESTS = 300000   # ~10000/day
OVERRAGE_RATE_PER_1000 = Decimal("0.20")

def calculate_usage_fee(request_count: int, tier: str) -> Decimal:
    tier_limits = {
        "tamagotchi": FREE_REQUESTS,
        "trial": TRIAL_REQUESTS,
        "starter": STARTER_REQUESTS,
        "pro": PRO_REQUESTS,
        "fund": FUND_REQUESTS,
        "enterprise": 100000000,
    }

    limit = tier_limits.get(tier, FREE_REQUESTS)
    overage = max(0, request_count - limit)
    return Decimal(overage) / 1000 * OVERAGE_RATE_PER_1000


async def generate_daily_usage_record(
    db: AsyncSession,
    user_id: str,
    request_count: int,
    api_key_id: Optional[str] = None,
    data_transfer_bytes: int = 0,
) -> dict:
    today = date.today()
    result = await db.execute(
        text("""
            INSERT INTO usage_records (id, user_id, api_key_id, date, request_count, data_transfer_bytes)
            VALUES (gen_random_uuid(), :uid, :kid, :date, :count, :bytes)
            ON CONFLICT (user_id, date) DO UPDATE SET
                request_count = usage_records.request_count + :count2,
                data_transfer_bytes = usage_records.data_transfer_bytes + :bytes2
            RETURNING *
        """),
        {"uid": user_id, "kid": api_key_id, "date": today,
         "count": request_count, "bytes": data_transfer_bytes,
         "count2": request_count, "bytes2": data_transfer_bytes},
    )
    await db.commit()
    return dict(result.mappings().first())


async def generate_monthly_invoice(
    db: AsyncSession,
    user_id: str,
    tier: str,
    period_start: date,
    period_end: date,
) -> Optional[dict]:
    usage = await db.execute(
        text("""
            SELECT COALESCE(SUM(request_count), 0) as total_requests,
                   COALESCE(SUM(data_transfer_bytes), 0) as total_bytes
            FROM usage_records
            WHERE user_id = :uid AND date >= :start AND date < :end
        """),
        {"uid": user_id, "start": period_start, "end": period_end},
    )
    row = usage.mappings().first()
    total_requests = int(row["total_requests"]) if row else 0

    usage_fee = calculate_usage_fee(total_requests, tier)
    if usage_fee <= 0 and tier == "free":
        return None

    result = await db.execute(
        text("""
            INSERT INTO invoices (id, user_id, amount, currency, status, period_start, period_end)
            VALUES (gen_random_uuid(), :uid, :amount, 'usd', 'draft', :start, :end)
            RETURNING *
        """),
        {"uid": user_id, "amount": usage_fee, "start": period_start, "end": period_end},
    )
    await db.commit()
    return dict(result.mappings().first())


async def get_usage_summary(db: AsyncSession, user_id: str) -> dict:
    today = date.today()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    today_usage = await db.execute(
        text("SELECT COALESCE(request_count, 0) FROM usage_records WHERE user_id = :uid AND date = :today"),
        {"uid": user_id, "today": today},
    )
    week_usage = await db.execute(
        text("SELECT COALESCE(SUM(request_count), 0) FROM usage_records WHERE user_id = :uid AND date >= :start"),
        {"uid": user_id, "start": week_ago},
    )
    month_usage = await db.execute(
        text("SELECT COALESCE(SUM(request_count), 0) FROM usage_records WHERE user_id = :uid AND date >= :start"),
        {"uid": user_id, "start": month_ago},
    )

    sub = await db.execute(
        text("SELECT tier, status FROM subscriptions WHERE user_id = :uid"),
        {"uid": user_id},
    )
    sub_row = sub.mappings().first()
    tier = sub_row["tier"] if sub_row else "free"
    tier_limits = {"tamagotchi": FREE_REQUESTS, "trial": TRIAL_REQUESTS, "starter": STARTER_REQUESTS, "pro": PRO_REQUESTS, "fund": FUND_REQUESTS, "enterprise": 100000000}
    limit = tier_limits.get(tier, FREE_REQUESTS)

    monthly = int(month_usage.scalar() or 0)
    return {
        "tier": tier,
        "limit": limit,
        "today": int(today_usage.scalar() or 0),
        "week": int(week_usage.scalar() or 0),
        "month": monthly,
        "usage_pct": round(monthly / limit * 100, 1) if limit > 0 else 0,
    }


def generate_invoice_pdf(invoice: dict) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='MiauTitle', parent=styles['Title'], fontSize=22, textColor=colors.HexColor('#6366f1'), spaceAfter=4*mm))
    styles.add(ParagraphStyle(name='MiauH2', parent=styles['Heading2'], fontSize=13, textColor=colors.HexColor('#374151')))
    styles.add(ParagraphStyle(name='RightAlign', parent=styles['Normal'], alignment=2))
    styles.add(ParagraphStyle(name='Bold', parent=styles['Normal'], fontName='Helvetica-Bold'))
    story = []

    story.append(Paragraph("MIAU FINANCE", styles['MiauTitle']))
    story.append(Paragraph("Invoice", styles['MiauH2']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#6366f1'), spaceAfter=6*mm))
    inv_id = str(invoice.get("id", ""))[:8]
    story.append(Paragraph(f"Invoice #MIU-{inv_id}", styles['Bold']))
    story.append(Paragraph(f"Date: {invoice.get('created_at', '').strftime('%B %d, %Y') if invoice.get('created_at') else 'N/A'}", styles['Normal']))
    story.append(Spacer(1, 4*mm))

    data = [
        ["Billing Period", f"{invoice.get('period_start', '').strftime('%b %d, %Y') if invoice.get('period_start') else 'N/A'} — {invoice.get('period_end', '').strftime('%b %d, %Y') if invoice.get('period_end') else 'N/A'}"],
        ["Status", invoice.get("status", "draft").upper()],
    ]
    t = Table(data, colWidths=[100, 320])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F3F4F6')),
    ]))
    story.append(t)
    story.append(Spacer(1, 6*mm))

    amount = float(invoice.get("amount", 0))
    line_data = [
        ["Description", "Amount"],
        [f"API Usage ({invoice.get('period_start', '').strftime('%b %Y') if invoice.get('period_start') else 'N/A'})", f"${amount:.2f}"],
    ]
    lt = Table(line_data, colWidths=[320, 100])
    lt.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTNAME', (1,1), (1,1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('LINEABOVE', (0,1), (-1,1), 1, colors.HexColor('#6366f1')),
    ]))
    story.append(lt)
    story.append(Spacer(1, 4*mm))

    status_color = colors.HexColor('#059669') if invoice.get("status") == "paid" else colors.HexColor('#D97706')
    story.append(Paragraph(f"<b>Total Due:</b> ${amount:.2f}", styles['RightAlign']))
    story.append(Paragraph(f"<b>Status:</b> <font color='{status_color.hexval()}'>{invoice.get('status', 'draft').upper()}</font>", styles['RightAlign']))
    story.append(Spacer(1, 10*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#D1D5DB')))
    story.append(Paragraph("Miau Finance — miau.finance", ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=1)))

    doc.build(story)
    return buf.getvalue()
