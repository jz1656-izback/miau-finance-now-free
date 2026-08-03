import json
import logging
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.middleware.rbac import get_current_user_db
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/education", tags=["Education"])


# --- Courses ---

@router.get("/courses")
async def list_courses(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    conditions = []
    params: dict = {}
    if category:
        conditions.append("category = :cat")
        params["cat"] = category
    if difficulty:
        conditions.append("difficulty = :diff")
        params["diff"] = difficulty
    where = "WHERE " + " AND ".join(conditions) if conditions else ""
    result = await db.execute(
        text(f"SELECT * FROM education_courses {where} ORDER BY order_index"),
        params,
    )
    return [dict(r) for r in result.mappings().all()]


@router.get("/courses/{course_id}")
async def get_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    result = await db.execute(
        text("SELECT * FROM education_courses WHERE id = :id"),
        {"id": course_id},
    )
    course = result.mappings().first()
    if not course:
        raise HTTPException(404, "Course not found")
    return dict(course)


# --- Lessons ---

@router.get("/courses/{course_id}/lessons")
async def list_lessons(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    result = await db.execute(
        text("SELECT * FROM education_lessons WHERE course_id = :cid ORDER BY order_index"),
        {"cid": course_id},
    )
    return [dict(r) for r in result.mappings().all()]


@router.get("/lessons/{lesson_id}")
async def get_lesson(
    lesson_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    result = await db.execute(
        text("SELECT * FROM education_lessons WHERE id = :id"),
        {"id": lesson_id},
    )
    lesson = result.mappings().first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    return dict(lesson)


# --- Quizzes ---

@router.get("/lessons/{lesson_id}/quiz")
async def get_quiz(
    lesson_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    result = await db.execute(
        text("SELECT * FROM education_quizzes WHERE lesson_id = :lid ORDER BY order_index"),
        {"lid": lesson_id},
    )
    questions = []
    for r in result.mappings().all():
        d = dict(r)
        d["id"] = str(d["id"])
        d["lesson_id"] = str(d["lesson_id"])
        try:
            d["options"] = json.loads(d["options"]) if isinstance(d["options"], str) else d["options"]
        except (json.JSONDecodeError, TypeError):
            d["options"] = []
        questions.append(d)
    return {"lesson_id": str(lesson_id), "questions": questions}


@router.post("/quizzes/{quiz_id}/answer")
async def submit_answer(
    quiz_id: UUID,
    selected_index: int = Query(..., ge=0),
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("SELECT * FROM education_quizzes WHERE id = :id"),
        {"id": quiz_id},
    )
    quiz = result.mappings().first()
    if not quiz:
        raise HTTPException(404, "Quiz question not found")
    correct = selected_index == quiz["correct_index"]
    return {
        "quiz_id": str(quiz_id),
        "correct": correct,
        "correct_index": quiz["correct_index"],
        "explanation": quiz["explanation"] or "",
    }


# --- Enrollment ---

@router.post("/courses/{course_id}/enroll")
async def enroll_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("SELECT id FROM education_courses WHERE id = :id"),
        {"id": course_id},
    )
    if not result.mappings().first():
        raise HTTPException(404, "Course not found")
    await db.execute(
        text("""
            INSERT INTO education_enrollments (id, user_id, course_id)
            VALUES (gen_random_uuid(), :uid, :cid)
            ON CONFLICT DO NOTHING
        """),
        {"uid": user["id"], "cid": course_id},
    )
    await db.commit()
    return {"status": "enrolled", "course_id": str(course_id)}


@router.get("/enrollments")
async def list_enrollments(
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("""
            SELECT e.*, c.title, c.slug, c.icon, c.difficulty
            FROM education_enrollments e
            JOIN education_courses c ON c.id = e.course_id
            WHERE e.user_id = :uid
            ORDER BY e.enrolled_at DESC
        """),
        {"uid": user["id"]},
    )
    return [dict(r) for r in result.mappings().all()]


# --- Progress ---

@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    lesson = await db.execute(
        text("SELECT course_id FROM education_lessons WHERE id = :id"),
        {"id": lesson_id},
    )
    lesson_row = lesson.mappings().first()
    if not lesson_row:
        raise HTTPException(404, "Lesson not found")

    await db.execute(
        text("""
            INSERT INTO education_lesson_completions (id, user_id, lesson_id)
            VALUES (gen_random_uuid(), :uid, :lid)
            ON CONFLICT DO NOTHING
        """),
        {"uid": user["id"], "lid": lesson_id},
    )

    total = await db.execute(
        text("SELECT COUNT(*) FROM education_lessons WHERE course_id = :cid"),
        {"cid": lesson_row["course_id"]},
    )
    total_count = total.scalar() or 1

    completed = await db.execute(
        text("""
            SELECT COUNT(*) FROM education_lesson_completions lc
            JOIN education_lessons l ON l.id = lc.lesson_id
            WHERE l.course_id = :cid AND lc.user_id = :uid
        """),
        {"cid": lesson_row["course_id"], "uid": user["id"]},
    )
    completed_count = completed.scalar() or 0

    pct = round(completed_count / total_count * 100, 2)
    await db.execute(
        text("""
            UPDATE education_enrollments
            SET completed_lessons = :cl, progress_pct = :pct
            WHERE user_id = :uid AND course_id = :cid
        """),
        {"cl": completed_count, "pct": pct, "uid": user["id"], "cid": lesson_row["course_id"]},
    )
    await db.commit()
    return {"lesson_id": str(lesson_id), "progress_pct": pct, "completed": completed_count, "total": total_count}


class TerminalCommand(BaseModel):
    command: str
    args: str = ""
    token: str = ""


@router.post("/terminal/execute")
async def execute_terminal_command(body: TerminalCommand = Body(...)):
    cmd = body.command.strip().lower()
    args = body.args.strip()
    token = body.token.strip()

    # Real API proxy — forward to actual Miau Finance API endpoints
    real_data = None
    if token:
        real_data = await _call_real_api(cmd, args, token)

    # Build responses — use real data if available, fall back to mock
    if cmd == "help":
        return {"output": _help_text(), "status": "ok"}

    if cmd == "clear":
        return {"output": "Screen cleared, ready for input.", "status": "ok"}

    if cmd in ("miau", "cat"):
        return {"output": "   ╱|、\n  (˚ˎ 。7\n   |、˜〵\n   じしˍ,)ノ\n  \"Miau!\"", "status": "ok"}

    if cmd == "theme":
        return {"output": f"Theme set to '{args or 'miau'}'. Terminal updated.", "status": "ok"}

    if cmd == "whoami":
        if real_data:
            return {"output": f"Logged in as: {real_data}", "status": "ok"}
        return {"output": "You are a Miau Finance student. Keep learning!", "status": "ok"}

    if cmd == "joke":
        jokes = [
            "Why did the cat become a CFA? Because tuna futures were looking bullish.",
            "What's a cat's favorite trading strategy? Buy the dip, nap through the rip.",
            "Why don't cats use stop-losses? They always land on their feet.",
            "A cat walked across a keyboard and bought 1000 shares of AAPL. Best trade of the day.",
        ]
        return {"output": jokes[len(args) % len(jokes) if args else 0], "status": "ok"}

    if cmd == "price":
        if real_data:
            lines = []
            for t in real_data:
                p = t.get("price", 0)
                c = t.get("change_pct", 0)
                sign = "+" if c >= 0 else ""
                lines.append(f"  {t.get('ticker','?'):6s} ${p:,.2f} ({sign}{c:.2f}%)")
            return {"output": "Live Market Data (REAL)\n" + "\n".join(lines), "status": "ok"}
        return {"output": _mock_price(args), "status": "ok"}

    if cmd == "risk":
        if real_data:
            d = real_data
            return {"output": f"Risk Report (LIVE)\n  VaR (95%):  {d.get('var_95','-'):.2f}%\n  CVaR:       {d.get('cvar_95','-'):.2f}%\n  Beta:       {d.get('beta','-'):.3f}\n  Sharpe:     {d.get('sharpe','-'):.3f}", "status": "ok"}
        return {"output": _mock_risk(), "status": "ok"}

    if cmd == "portfolio":
        if real_data:
            lines = []
            for pos in real_data:
                lines.append(f"  {pos.get('ticker','?'):5s} {pos.get('shares',0):5d} shares @ ${pos.get('price',0):,.2f}")
            return {"output": "Your Portfolio (LIVE)\n" + "\n".join(lines) if lines else "Portfolio empty — start trading!", "status": "ok"}
        return {"output": _mock_portfolio(), "status": "ok"}

    if cmd == "esg":
        if real_data:
            d = real_data
            return {"output": f"ESG Score (LIVE)\n  Environmental: {d.get('e',0)}\n  Social:        {d.get('s',0)}\n  Governance:    {d.get('g',0)}\n  Total:         {d.get('total',0)}", "status": "ok"}
        return {"output": _mock_esg(), "status": "ok"}

    if cmd == "forex":
        if real_data:
            lines = []
            for pair, rate in list(real_data.items())[:8]:
                lines.append(f"  USD/{pair}: {rate:.4f}")
            return {"output": "Forex Rates (LIVE)\n" + "\n".join(lines), "status": "ok"}
        return {"output": "Forex Rates (mock)\n  USD/EUR: 0.9250\n  USD/GBP: 0.7900\n  USD/JPY: 150.50\n  USD/CHF: 0.8850", "status": "ok"}

    if cmd in ("login", "logout"):
        return {"output": f"{cmd.capitalize()} successful.", "status": "ok"}

    if cmd == "exit" or cmd == "back":
        return {"output": "Returning to lesson view.", "status": "ok", "action": "back"}

    # Course commands — mock responses for education platform
    course_commands = {
        "chart": "AAPL Chart (1Y)\n    200 ┤        ╭─╮\n    190 ┤  ╭─╮╭──╯ ╰──╮\n    180 ┤──╯ ╰╯         ╰──\n    170 ┤",
        "signals": "Trading Signals (AAPL)\n  RSI(14): 52 NEUTRAL · MACD: BULLISH · SMA50: $185 · SMA200: $172\n  Overall: MODERATELY BULLISH (65/100)",
        "beta": "Beta: AAPL vs SPY = 1.17 (17% more volatile than market)",
        "var": "VaR (95%, 1-day): -2.34% · CVaR: -3.12% (AAPL)",
        "correlation": "Correlation Matrix\n         AAPL  MSFT  GOOGL\n  AAPL   1.00  0.72  0.65\n  MSFT   0.72  1.00  0.58\n  GOOGL  0.65  0.58  1.00",
        "fundamentals": "AAPL Fundamentals\n  Mkt Cap: $3.02T · P/E: 28.5 · EPS: $6.97 · Rev: $383B · Net Income: $97B · Div Yield: 0.48%",
        "earnings": "Earnings Calendar\n  AAPL Q2 2026: EPS $1.53 (beat by $0.08), Rev $94.8B\n  Next: Jul 25, 2026 (est)",
        "crypto": "BTC: $67,892 (+2.15%) · ETH: $3,456 (-1.23%) · SOL: $142.50 (+5.67%)",
        "news": "AAPL News: 🟢 M5 chip +2.3% 🟢 iPhone 17 pre-orders +15% 🟡 EU App Store review 🔴 Supplier cuts -0.8%",
        "sentiment": "AAPL Sentiment: News 72% positive · Social 68% positive · Consensus: BUY (32 analysts, target $215)",
        "options": "AAPL Options Jul26\n  $185C: $8.50 · $190C: $5.10 · $195C: $2.80 · $200C: $1.40 · IV: 22%",
        "sectors": "Sectors: Tech +2.3% · Health +1.1% · Fin +0.8% · Energy -0.5% · RE -1.2% · Utils -1.8%",
        "indicators": "VIX: 15.2 · P/C Ratio: 0.72 · Adv/Dec: 1850/1200 · New Hi/Lo: 245/38",
        "movers": "▲ NVDA +8.2% ▲ AMD +5.1% ▲ META +3.4%  ▼ INTC -4.2% ▼ PFE -2.8%",
        "commodities": "Gold $2,345 · Silver $28.90 · Oil $78.50 · Copper $4.52 · NatGas $2.85",
        "treasury": "UST Yields: 2Y 4.85% · 5Y 4.45% · 10Y 4.28% · 30Y 4.55% · Yield curve inverted (57bp)",
        "cryptomkt": "Crypto Market: Total Cap $2.45T · BTC Dom 52% · 24h Vol $85B",
        "fear": "Fear & Greed: 68 — GREED (last week 55, last month 42)",
        "watch": "Watchlist: AAPL $198.52 +1.2% · MSFT $425.67 -0.1% · TSLA $245.80 -0.9% · NVDA $892.35 +3.4%",
        "positions": "Positions: AAPL 100 @ $198.52 = $19,852 | MSFT 50 @ $425.67 = $21,284 | Cash $58,864 = $100K",
        "pnl": "P&L: Unrealized +$3,128 (+3.2%) · Realized MTD +$1,845 · NVDA best +8.2% · INTC worst -4.2%",
        "all": "NYSE $18,512 · NASDAQ $16,743 · S&P $5,342 · BTC $67,892 · VIX 15.2 · Gold $2,345",
        "sheetz": "Valuation: DCF $198 BUY · WACC 10% · Comps $185-210 · LBO IRR 18.5% · Use: sheetz miau -all <t>",
        "journal": "Journal: BUY 10 AAPL $180 😸 · SELL 5 TSLA $250 😿 · 60% win rate, +$3,128 P&L",
        "leaderboard": "#1 cat_trader +12.3% · #2 miau_master +9.8% · #3 tuna_whisperer +7.2% · You #42 +3.2%",
        "orders": "Orders: BUY LIMIT 10 NVDA @ $850 PENDING · SELL STOP 5 INTC @ $38 ACTIVE",
        "backtest": "Backtest SMA Cross AAPL 1Y: +24.3% return · Sharpe 1.42 · MaxDD -8.7% · 14 trades",
        "broker": "Brokers: Alpaca ✅ Paper · IBKR ⬜ Off · DEGIRO ⬜ Off",
        "apikey": "API Keys: 2 active · apikey create <name> to add",
        "subscription": "Subscription: Free tier · API Keys 0/2 · Requests 45/300 today",
        "pricing": "Free $0 · Pro $116/mo · Enterprise $396/mo",
        "devconsole": "Dev Console: 2 API keys · 1 webhook · 45/300 req today · 1,250/mo",
        "currency": "FX: USD→EUR 0.925 · USD→GBP 0.790 · USD→JPY 150.5 · USD→CHF 0.885",
        "map": "World Map: 21 exchanges, 5 continents. Type 'map' in full terminal.",
        "global": "Global: US +0.3% · UK +0.5% · DE +0.4% · JP +0.6% · CN +0.3% · BR +0.1%",
        "scenario": "Scenario AAPL: Bear $165 (-16.8%) · Base $195 (-1.9%) · Bull $225 (+13%) · Black Swan $120 (-40%)",
        "dividends": "Dividends: AAPL $0.24/q (0.48%) · MSFT $0.75/q (0.70%) · Ex: Aug 5, Aug 14",
        "rolling": "Rolling 12mo AAPL: Sharpe 1.42→1.31 · Beta 1.17→1.16 · Vol 14.2%→14.5%",
        "benchmark": "AAPL vs SPY: Alpha +3.2% · Beta 1.17 · Tracking Err 8.5% · Info Ratio 0.38",
        "defi": "DeFi: Uni TVL $5.2B · Aave TVL $12B · Curve $3.5B · Lido $20B · stETH APR 3.8%",
        "nft": "NFT: BAYC 25 ETH floor · Punks 35 ETH · Art Blocks 2 ETH · No NFTs owned",
        "dao": "DAO: 12 proposals active · 0 MIAU voting power",
        "dcf": "DCF AAPL: FCF $105B · 8% growth 5yr · WACC 10% · Intrinsic $198 · BUY (+13% upside)",
        "wacc": "WACC: CoE 11.2% · CoD 3.5% · Equity 85% · Debt 15% → WACC 10.0%",
        "lbo": "LBO AAPL: EBITDA $130B · 5x debt $650B · Exit 5yr $180B · IRR 18.5% → FEASIBLE",
        "accounting": "AAPL: Rev $383B · COGS $214B · GP $169B (44%) · OpInc $113B · NetInc $97B",
        "stress": "Stress Test AAPL: Under -30% SPY shock → AAPL -18% to -22% ($3,674 impact)",
        "sql": "SQL > SELECT * FROM market_data LIMIT 5;\n  AAPL|198.52  MSFT|425.67  TSLA|245.80",
        "gas": "Gas (gwei): ETH 12/18/25 · ARB 0.1 · OP 0.05 · MATIC 35",
        "bridge": "Bridges: LayerZero ETH→ARB $0.50/5min · Wormhole ETH→SOL $1.20/8min",
        "mev": "MEV: Sandwich risk LOW · Flashbots ✅ · Rec'd slippage 0.5%",
        "tokenomics": "MIAU Token: 1B total · 250M circ · Staking APR 8.5% · Buyback 2% of fees",
        "interview": "Q: Walk me through a DCF.\nA: Project FCF 5 years, terminal value, discount at WACC to PV. Compare to market cap for buy/hold/sell.",
        "summary": "Miau Finance v2.1.0 · 200+ endpoints · 10 Docker · 260+ tests · 1 well-fed cat",
    }

    if cmd in course_commands:
        return {"output": course_commands[cmd], "status": "ok"}

    return {"output": f"Unknown command: '{cmd}'. Try 'help' for available commands.", "status": "error"}


async def _call_real_api(cmd: str, args: str, token: str) -> Optional[dict]:
    """Proxy real Miau Finance API calls using the user's JWT token."""
    import httpx
    headers = {"Authorization": f"Bearer {token}"}
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            if cmd == "price":
                tickers = args or "AAPL,MSFT"
                r = await client.get(f"http://localhost:8000/api/v1/market/live?tickers={tickers}", headers=headers)
                if r.status_code == 200:
                    data = r.json()
                    return list(data.get("data", {}).values()) if data.get("data") else None
            elif cmd == "risk":
                ticker = args or "AAPL"
                r = await client.get(f"http://localhost:8000/api/v1/risk/comprehensive?ticker={ticker}", headers=headers)
                if r.status_code == 200:
                    return r.json()
            elif cmd == "portfolio":
                r = await client.get("http://localhost:8000/api/v1/portfolios", headers=headers)
                if r.status_code == 200 and isinstance(r.json(), list) and len(r.json()) > 0:
                    pid = r.json()[0].get("id")
                    p = await client.get(f"http://localhost:8000/api/v1/portfolios/{pid}/positions", headers=headers)
                    if p.status_code == 200:
                        return p.json() if isinstance(p.json(), list) else None
            elif cmd == "esg":
                ticker = args or "AAPL"
                r = await client.get(f"http://localhost:8000/api/v1/esg/{ticker}", headers=headers)
                if r.status_code == 200:
                    return r.json()
            elif cmd == "forex":
                r = await client.get("http://localhost:8000/api/v1/market/forex?base=USD", headers=headers)
                if r.status_code == 200:
                    data = r.json()
                    return data.get("rates", {})
            elif cmd == "whoami":
                r = await client.get("http://localhost:8000/api/v1/users/me", headers=headers)
                if r.status_code == 200:
                    d = r.json()
                    return d.get("username", "user")
    except Exception as e:
        logger.warning("Real API proxy failed for %s: %s", cmd, e)
    return None


def _help_text() -> str:
    sep = "─" * 50
    return "\n".join([
        "MIAU FINANCE — Available Commands (v2.1.0)",
        sep,
        "  help           Show this help",
        "  clear          Clear the terminal",
        "  price <t>      Live stock price (REAL data!)",
        "  risk <t>       Risk analytics — VaR, Beta, Sharpe",
        "  portfolio      Your portfolio positions",
        "  esg <t>        ESG scores for any ticker",
        "  forex          Live forex rates",
        "  sheetz         Valuation models (DCF, WACC, Comps, LBO)",
        "  theme <name>   Change terminal theme",
        "  whoami         Show who you are logged in as",
        "  cat            Print a cat",
        "  joke           Random cat/finance joke",
        "  login / logout Auth commands",
        sep,
        "💡 Type 'hint' for help with the current step.",
    ])


def _mock_price(args: str) -> str:
    return "Live Market Data (MOCK — log in for real!)\n  AAPL   $198.52 (+1.24%)\n  MSFT   $425.67 (-0.12%)\n  TSLA   $245.80 (-0.87%)"

def _mock_risk() -> str:
    return "Risk Report (MOCK — log in for real!)\n  VaR (95%):  -2.34%\n  Sharpe:      1.42\n  Beta:        0.87\n  Volatility: 14.2%"

def _mock_portfolio() -> str:
    return "Your Portfolio (MOCK — log in for real!)\n  AAPL  100 shares @ $198.52  = $19,852\n  MSFT   50 shares @ $425.67  = $21,284\n  Cash: $58,864  Total: $100,000"

def _mock_esg() -> str:
    return "ESG Scores (MOCK — log in for real!)\n  AAPL: E=72 S=68 G=85  Total=75  B\n  MSFT: E=88 S=82 G=90  Total=87  A"


@router.get("/progress/{course_id}")
async def get_progress(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user_db),
):
    result = await db.execute(
        text("SELECT * FROM education_enrollments WHERE user_id = :uid AND course_id = :cid"),
        {"uid": user["id"], "cid": course_id},
    )
    row = result.mappings().first()
    if not row:
        raise HTTPException(404, "Not enrolled in this course")
    return dict(row)
