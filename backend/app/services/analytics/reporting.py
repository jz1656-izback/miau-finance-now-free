import io
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable,
)
from reportlab.lib import colors
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from io import BytesIO


def _build_portfolio_table(data: dict) -> list:
    rows = [["Metric", "Value"]]
    metrics = [
        ("Total Value", f"${data.get('total_market_value', 0):,.2f}"),
        ("Unrealized P&L", f"${data.get('total_unrealized_pnl', 0):,.2f}"),
        ("Realized P&L", f"${data.get('total_realized_pnl', 0):,.2f}"),
        ("Number of Positions", str(data.get("num_positions", 0))),
        ("Number of Trades", str(data.get("num_trades", 0))),
        ("P&L", f"${data.get('total_pnl', 0):,.2f}"),
        ("Return", f"{data.get('return_pct', 0):.2f}%"),
    ]
    rows.extend(metrics)
    return rows


def generate_portfolio_report(portfolio_name: str, summary: dict, positions: list,
                                pnl_data: list, risk_data: list) -> BytesIO:
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=0.5 * inch)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle("Title2", parent=styles["Title"], fontSize=22, textColor=HexColor("#1a1a2e"))
    story.append(Paragraph(f"Miau Finance — Portfolio Report", title_style))
    story.append(Paragraph(f"Portfolio: {portfolio_name}", styles["Heading2"]))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    story.append(Spacer(1, 0.2 * inch))

    # Summary
    story.append(Paragraph("Summary", styles["Heading2"]))
    tbl = Table(_build_portfolio_table(summary), colWidths=[2.5 * inch, 3 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f8f9fa"), colors.white]),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.3 * inch))

    # Positions chart
    if positions:
        story.append(Paragraph("Position Allocation", styles["Heading2"]))
        fig, ax = plt.subplots(figsize=(6, 3.5))
        pos_df = pd.DataFrame(positions)
        if "market_value" in pos_df.columns and "ticker" in pos_df.columns:
            pos_df = pos_df.sort_values("market_value", ascending=True)
            colors_list = plt.cm.viridis(np.linspace(0.2, 0.8, len(pos_df)))
            ax.barh(pos_df["ticker"].values, pos_df["market_value"].values / 1e6, color=colors_list)
            ax.set_xlabel("Market Value ($M)")
            ax.set_title(f"Position Allocation — {portfolio_name}")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            plt.tight_layout()
            img_buf = BytesIO()
            fig.savefig(img_buf, format="png", dpi=150, bbox_inches="tight")
            plt.close(fig)
            story.append(Image(img_buf, width=5 * inch, height=3 * inch))
            story.append(Spacer(1, 0.2 * inch))
        else:
            plt.close(fig)

    # P&L Chart
    if pnl_data:
        story.append(Paragraph("P&L Trend", styles["Heading2"]))
        fig, ax = plt.subplots(figsize=(6, 2.5))
        pnl_df = pd.DataFrame(pnl_data)
        if "date" in pnl_df.columns and "total_pnl" in pnl_df.columns:
            pnl_df["date"] = pd.to_datetime(pnl_df["date"])
            pnl_df = pnl_df.sort_values("date")
            ax.plot(pnl_df["date"], pnl_df["total_pnl"], color="#5c7cfa", linewidth=2)
            ax.fill_between(pnl_df["date"], 0, pnl_df["total_pnl"], alpha=0.1, color="#5c7cfa")
            ax.axhline(y=0, color="gray", linestyle="--", linewidth=0.5)
            ax.set_ylabel("P&L ($)")
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            plt.xticks(rotation=45)
            plt.tight_layout()
            img_buf = BytesIO()
            fig.savefig(img_buf, format="png", dpi=150, bbox_inches="tight")
            plt.close(fig)
            story.append(Image(img_buf, width=5.5 * inch, height=2.2 * inch))
            story.append(Spacer(1, 0.2 * inch))
        else:
            plt.close(fig)

    # Positions table
    if positions:
        story.append(Paragraph("Position Details", styles["Heading2"]))
        pos_rows = [["Ticker", "Qty", "Avg Price", "Market Value", "Unrealized P&L"]]
        for p in positions[:20]:
            pos_rows.append([
                p.get("ticker", "N/A"),
                str(p.get("quantity", 0)),
                f"${p.get('average_price', 0):.2f}" if p.get("average_price") else "-",
                f"${p.get('market_value', 0):,.2f}" if p.get("market_value") else "-",
                f"${p.get('unrealized_pnl', 0):,.2f}" if p.get("unrealized_pnl") else "-",
            ])
        tbl = Table(pos_rows, colWidths=[0.8 * inch, 0.6 * inch, 0.9 * inch, 1.2 * inch, 1.2 * inch])
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f8f9fa"), colors.white]),
        ]))
        story.append(tbl)

    # Risk metrics
    if risk_data:
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("Risk Metrics", styles["Heading2"]))
        risk_rows = [["Metric", "Value", "Type", "Date"]]
        for r in risk_data[:15]:
            risk_rows.append([
                r.get("metric_name", ""),
                f"{r.get('metric_value', 0):.4f}",
                r.get("metric_type", ""),
                str(r.get("as_of_date", ""))[:10],
            ])
        if len(risk_rows) > 1:
            tbl = Table(risk_rows, colWidths=[1.5 * inch, 1 * inch, 1 * inch, 1.5 * inch])
            tbl.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1a1a2e")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.5, HexColor("#cccccc")),
            ]))
            story.append(tbl)

    # Footer
    story.append(Spacer(1, 0.5 * inch))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#cccccc")))
    story.append(Paragraph(
        f"Miau Finance — Confidential. Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        ParagraphStyle("Footer", parent=styles["Normal"], fontSize=7, textColor=HexColor("#999999")),
    ))

    doc.build(story)
    buf.seek(0)
    return buf


async def export_positions_to_excel(positions: list[dict]) -> BytesIO:
    import asyncio
    return await asyncio.to_thread(_build_excel, positions)


def _build_excel(positions: list[dict]) -> BytesIO:
    df = pd.DataFrame(positions)
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Positions", index=False)
        sheet = writer.sheets["Positions"]
        max_lens: list[int] = []
        for col in range(len(df.columns)):
            col_name = str(df.columns[col])
            max_len = max(df.iloc[:, col].astype(str).map(len).max(), len(col_name)) + 2
            max_lens.append(min(max_len, 30))
        for col, w in enumerate(max_lens):
            letter = chr(65 + col) if col < 26 else ""
            if letter:
                sheet.column_dimensions[letter].width = w
    buf.seek(0)
    return buf


async def export_trades_to_csv(trades: list[dict]) -> str:
    import asyncio
    return await asyncio.to_thread(_build_csv, trades)


def _build_csv(trades: list[dict]) -> str:
    df = pd.DataFrame(trades)
    return df.to_csv(index=False)
