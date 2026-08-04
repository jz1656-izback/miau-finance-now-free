import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
import random
import math

from app.middleware.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/ai", tags=["AI Commands"])


def _cat_commentary() -> str:
    lines = [
        "😸 This analysis was purr-reviewed by the Miau AI committee.",
        "🐱 The cat sat on the keyboard while generating this report.",
        "😿 Warning: This AI may contain traces of catnip.",
        "🙀 Your cat has opinions about this stock. Strong opinions.",
        "😻 This stock passed the whisker test. Barely.",
        "🐈 The AI model was trained on a diet of tuna and market data.",
        "😼 This analysis is 100% organic, free-range, and cat-approved.",
        "😹 The cat responsible for this analysis is currently napping.",
    ]
    return random.choice(lines)


def _fake_ticker_name(ticker: str) -> str:
    names = {
        "AAPL": "Apple Inc.",
        "MSFT": "Microsoft Corporation",
        "GOOGL": "Alphabet Inc.",
        "AMZN": "Amazon.com Inc.",
        "TSLA": "Tesla Inc.",
        "META": "Meta Platforms Inc.",
        "NVDA": "NVIDIA Corporation",
        "SPY": "SPDR S&P 500 ETF Trust",
    }
    return names.get(ticker.upper(), f"{ticker.upper()} Corp.")


def _sparkline_data(n: int = 10) -> list[float]:
    v = 100.0
    out = []
    for _ in range(n):
        v += random.gauss(0, 2)
        out.append(round(v, 2))
    return out


def _score_to_label(s: float) -> str:
    if s >= 0.5:
        return "🟢 Bullish"
    if s >= 0.1:
        return "🟡 Slightly Bullish"
    if s >= -0.1:
        return "⚪ Neutral"
    if s >= -0.5:
        return "🟠 Slightly Bearish"
    return "🔴 Bearish"


def _risk_score_to_label(s: float) -> str:
    if s <= 2:
        return "🟢 Low Risk"
    if s <= 5:
        return "🟡 Moderate Risk"
    if s <= 7:
        return "🟠 Elevated Risk"
    return "🔴 High Risk"


@router.get("/summary/{ticker}")
async def ai_summary(
    ticker: str,
    user: dict = Depends(get_current_user),
    
):
    logger.debug("ai_summary: ticker=%s", ticker)
    ticker = ticker.upper()
    name = _fake_ticker_name(ticker)
    scores = {
        "business_overview": (
            f"{name} ({ticker}) operates in a highly competitive global market. "
            f"The company has established a strong brand presence and maintains a diversified revenue stream "
            f"across multiple segments. Recent strategic initiatives have focused on expanding into adjacent markets "
            f"while strengthening core operations through operational efficiency programs. "
            f"The management team has demonstrated consistent execution capability, though macroeconomic headwinds "
            f"remain a concern for near-term growth prospects."
        ),
        "financial_health": (
            f"The company maintains a {random.choice(['strong', 'moderate', 'healthy', 'stable'])} balance sheet "
            f"with a current ratio of {random.uniform(1.2, 3.5):.1f}x and debt-to-equity of {random.uniform(0.1, 1.5):.1f}x. "
            f"Revenue growth has been tracking at {random.uniform(5, 25):.1f}% YoY with operating margins "
            f"of {random.uniform(10, 40):.1f}%. Free cash flow generation remains "
            f"{random.choice(['robust', 'adequate', 'stable', 'improving'])}, "
            f"supporting both organic reinvestment and shareholder returns. "
            f"The company has {random.choice(['increased', 'maintained', 'initiated'])} its dividend "
            f"by {random.uniform(5, 20):.1f}% over the past year."
        ),
        "market_position": (
            f"{name} holds a {random.choice(['dominant', 'leading', 'strong', 'notable'])} position "
            f"within its industry, commanding approximately {random.uniform(10, 45):.1f}% market share. "
            f"Key competitive advantages include {random.choice(['brand loyalty', 'patent portfolio', 'scale economies', 'network effects', 'switching costs'])} "
            f"that create meaningful barriers to entry. "
            f"The company faces competition from both traditional peers and emerging disruptors, "
            f"but its {random.choice(['R&D pipeline', 'distribution network', 'customer relationships', 'technology stack'])} "
            f"provides a durable edge. Analyst sentiment is "
            f"{random.choice(['overwhelmingly positive', 'cautiously optimistic', 'mixed', 'constructive'])} "
            f"with a consensus price target implying {random.uniform(5, 30):.1f}% upside."
        ),
    }
    return {
        "ticker": ticker,
        "name": name,
        "summary": scores,
        "cat_commentary": _cat_commentary(),
        "generated_at": "2026-05-20T12:00:00Z",
    }


@router.get("/sentiment/{ticker}")
async def ai_sentiment(
    ticker: str,
    user: dict = Depends(get_current_user),
    
):
    logger.debug("ai_sentiment: ticker=%s", ticker)
    ticker = ticker.upper()
    overall = round(random.uniform(-0.8, 0.8), 3)
    trend_data = _sparkline_data(14)
    sources = {
        "news_sentiment": round(random.uniform(-1, 1), 3),
        "social_media_buzz": round(random.uniform(-1, 1), 3),
        "fundamental_signals": round(random.uniform(-1, 1), 3),
        "analyst_consensus": round(random.uniform(-1, 1), 3),
        "insider_sentiment": round(random.uniform(-1, 1), 3),
    }
    return {
        "ticker": ticker,
        "overall_score": overall,
        "overall_label": _score_to_label(overall),
        "source_breakdown": sources,
        "trend_sparkline": trend_data,
        "trend_direction": "improving" if trend_data[-1] > trend_data[0] else "declining" if trend_data[-1] < trend_data[0] else "stable",
        "momentum": random.choice(["strengthening", "weakening", "neutral"]),
        "cat_commentary": (
            f"{_cat_commentary()} "
            f"The sentiment whiskers are twitching {random.choice(['northward', 'southward', 'in circles'])} for {ticker}."
        ),
        "generated_at": "2026-05-20T12:00:00Z",
    }


@router.get("/insight/{ticker}")
async def ai_insight(
    ticker: str,
    user: dict = Depends(get_current_user),
    
):
    logger.debug("ai_insight: ticker=%s", ticker)
    ticker = ticker.upper()
    name = _fake_ticker_name(ticker)
    verdict = random.choice(["BUY", "HOLD", "SELL"])
    conviction = round(random.uniform(0.3, 0.95), 2)

    moats = [
        "Brand intangible asset — strong customer loyalty and premium pricing power.",
        "Cost advantage — economies of scale that competitors cannot replicate.",
        "Network effects — each new user increases the value of the platform.",
        "Switching costs — high barriers for customers to migrate to alternatives.",
        "Regulatory moat — patents and licenses that restrict competition.",
    ]
    risks = [
        "Macroeconomic slowdown reducing consumer spending power.",
        "Regulatory scrutiny increasing compliance costs and limiting operations.",
        "Technological disruption from agile startups and AI-native competitors.",
        "Supply chain concentration risk in key manufacturing regions.",
        "Valuation premium leaves limited margin of safety in bear scenarios.",
        "Key person dependency on founder-led management team.",
        "Currency headwinds from international revenue exposure.",
    ]
    catalysts = [
        "Upcoming product launch expected to drive revenue acceleration.",
        "Share buyback program returning capital and supporting EPS growth.",
        "Margin expansion from cost optimization and operational leverage.",
        "New market entry opening TAM by approximately 30%.",
        "Strategic partnership or M&A activity in adjacent verticals.",
        "Favorable regulatory developments reducing compliance overhead.",
        "Dividend increase signaling management confidence.",
    ]

    return {
        "ticker": ticker,
        "name": name,
        "verdict": verdict,
        "conviction": conviction,
        "conviction_label": "High" if conviction > 0.7 else "Medium" if conviction > 0.4 else "Low",
        "competitive_moat": random.choice(moats),
        "key_risks": random.sample(risks, 3),
        "catalysts": random.sample(catalysts, 3),
        "valuation_metrics": {
            "current_pe": round(random.uniform(10, 50), 1),
            "forward_pe": round(random.uniform(8, 40), 1),
            "ev_ebitda": round(random.uniform(8, 35), 1),
            "peg_ratio": round(random.uniform(0.5, 4.0), 2),
            "dcf_fair_value": round(random.uniform(50, 500), 2),
            "upside_to_dcf": f"{round(random.uniform(-20, 50), 1)}%",
        },
        "price_targets": {
            "high": round(random.uniform(150, 600), 2),
            "median": round(random.uniform(120, 500), 2),
            "low": round(random.uniform(80, 400), 2),
        },
        "cat_commentary": (
            f"🐱 After careful analysis (and three cat naps), Miau AI recommends: {verdict} on {ticker}. "
            f"Conviction: {conviction_label.lower()}. "
            f"{random.choice(['The cat has spoken.', 'Follow the whiskers.', 'Tuna for thought.', 'Paws before you buy.'])}"
        ),
        "generated_at": "2026-05-20T12:00:00Z",
    }


@router.get("/report")
async def ai_report(
    sector: Optional[str] = Query(None),
    period: str = Query("daily"),
    user: dict = Depends(get_current_user),
    
):
    logger.debug("ai_report: sector=%s period=%s", sector, period)
    sectors_data = [
        {"name": "Technology", "change_pct": round(random.uniform(-3, 5), 2), "volume": random.randint(50000, 200000)},
        {"name": "Healthcare", "change_pct": round(random.uniform(-2, 3), 2), "volume": random.randint(30000, 150000)},
        {"name": "Finance", "change_pct": round(random.uniform(-2.5, 3.5), 2), "volume": random.randint(40000, 180000)},
        {"name": "Energy", "change_pct": round(random.uniform(-4, 4), 2), "volume": random.randint(20000, 100000)},
        {"name": "Consumer Cyclical", "change_pct": round(random.uniform(-3, 4), 2), "volume": random.randint(25000, 120000)},
        {"name": "Consumer Defensive", "change_pct": round(random.uniform(-1.5, 2.5), 2), "volume": random.randint(15000, 80000)},
        {"name": "Industrials", "change_pct": round(random.uniform(-2, 3), 2), "volume": random.randint(20000, 110000)},
        {"name": "Utilities", "change_pct": round(random.uniform(-1, 2), 2), "volume": random.randint(10000, 50000)},
        {"name": "Real Estate", "change_pct": round(random.uniform(-2.5, 2.5), 2), "volume": random.randint(10000, 60000)},
        {"name": "Materials", "change_pct": round(random.uniform(-3, 3.5), 2), "volume": random.randint(12000, 70000)},
        {"name": "Communication", "change_pct": round(random.uniform(-2, 4), 2), "volume": random.randint(18000, 90000)},
    ]
    if sector:
        sectors_data = [s for s in sectors_data if s["name"].lower() == sector.lower()]

    top_movers = [
        {"ticker": "NVDA", "name": "NVIDIA Corp.", "change_pct": round(random.uniform(-8, 10), 2), "price": round(random.uniform(400, 1200), 2)},
        {"ticker": "AAPL", "name": "Apple Inc.", "change_pct": round(random.uniform(-5, 6), 2), "price": round(random.uniform(150, 250), 2)},
        {"ticker": "TSLA", "name": "Tesla Inc.", "change_pct": round(random.uniform(-10, 12), 2), "price": round(random.uniform(150, 400), 2)},
        {"ticker": "META", "name": "Meta Platforms", "change_pct": round(random.uniform(-6, 8), 2), "price": round(random.uniform(250, 550), 2)},
        {"ticker": "AMZN", "name": "Amazon.com Inc.", "change_pct": round(random.uniform(-4, 5), 2), "price": round(random.uniform(100, 200), 2)},
    ]

    market_condition = random.choice([
        "bullish", "cautiously bullish", "neutral", "cautiously bearish", "bearish"
    ])
    vix = round(random.uniform(12, 35), 1)

    return {
        "period": period,
        "sector_filter": sector or "all",
        "market_condition": market_condition,
        "vix": vix,
        "top_movers": sorted(top_movers, key=lambda x: abs(x["change_pct"]), reverse=True),
        "sectors": sorted(sectors_data, key=lambda x: abs(x["change_pct"]), reverse=True),
        "market_summary": (
            f"Markets are trading in a {market_condition} tone with VIX at {vix}. "
            f"{random.choice(['Breadth favors bulls', 'Breadth is mixed', 'Defensive sectors leading', 'Cyclicals outperforming'])}. "
            f"The {period} outlook suggests "
            f"{random.choice(['continued momentum', 'potential reversal', 'range-bound trading', 'volatility expansion'])} "
            f"ahead of key economic data releases."
        ),
        "cat_commentary": (
            f"🐱 Miau AI has scanned the markets (while chasing a laser pointer). "
            f"Overall vibe: {market_condition}. "
            f"{random.choice(['The cat thinks this is a buying opportunity.', 'The cat recommends waiting for a better entry.',
                           'The cat is indifferent. The cat is always indifferent.', 'The cat smells uncertainty.'])}"
        ),
        "generated_at": "2026-05-20T12:00:00Z",
    }


@router.get("/allocate")
async def ai_allocate(
    risk_profile: str = Query("moderate"),
    user: dict = Depends(get_current_user),
    
):
    logger.debug("ai_allocate: risk_profile=%s", risk_profile)
    profiles = {
        "conservative": {
            "label": "🛡️ Conservative — Capital Preservation",
            "allocation": {
                "US_Treasuries": 40,
                "Investment_Grade_Bonds": 20,
                "Large_Cap_Value": 15,
                "Cash": 10,
                "Gold": 8,
                "Dividend_Growth": 5,
                "TIPS": 2,
            },
            "expected_return": "4-6%",
            "expected_volatility": "6-9%",
            "max_drawdown": "~10%",
        },
        "moderate": {
            "label": "⚖️ Moderate — Balanced Growth",
            "allocation": {
                "US_Large_Cap": 25,
                "International_Equity": 15,
                "US_Treasuries": 15,
                "Corporate_Bonds": 10,
                "Small_Cap": 10,
                "REITs": 8,
                "Gold": 7,
                "Emerging_Markets": 5,
                "Cash": 5,
            },
            "expected_return": "7-9%",
            "expected_volatility": "10-14%",
            "max_drawdown": "~18%",
        },
        "aggressive": {
            "label": "🚀 Aggressive — Maximum Growth",
            "allocation": {
                "US_Large_Cap_Growth": 30,
                "International_Equity": 20,
                "Small_Cap_Growth": 15,
                "Emerging_Markets": 12,
                "Sector_ETFs": 10,
                "Crypto": 5,
                "Private_Equity": 5,
                "Cash": 3,
            },
            "expected_return": "10-15%",
            "expected_volatility": "18-25%",
            "max_drawdown": "~35%",
        },
    }

    profile = profiles.get(risk_profile.lower(), profiles["moderate"])
    total = sum(profile["allocation"].values())
    normalized = {k: round(v / total * 100, 1) for k, v in profile["allocation"].items()}

    return {
        "risk_profile": risk_profile.lower(),
        "profile_label": profile["label"],
        "allocation": normalized,
        "expected_return": profile["expected_return"],
        "expected_volatility": profile["expected_volatility"],
        "max_drawdown": profile["max_drawdown"],
        "rationale": (
            f"This allocation is optimized for a {risk_profile} risk profile. "
            f"{random.choice([
                'The portfolio emphasizes capital preservation with a bias toward fixed income and defensive equities.',
                'A balanced approach combining growth assets with income-generating securities for steady accumulation.',
                'Maximum growth orientation with higher allocation to equities, alternatives, and emerging markets.',
            ])} "
            f"Asset allocation is dynamically adjusted based on market conditions, valuation metrics, "
            f"and the cat's current mood. Rebalancing is recommended quarterly or when deviations exceed 5%."
        ),
        "cat_commentary": (
            f"{_cat_commentary()} "
            f"{random.choice([
                'This allocation has been taste-tested by our resident feline.',
                'The cat approves of this diversification. It reminds them of a mixed bag of treats.',
                'Even the cat knows not to put all their tuna in one basket.',
            ])}"
        ),
        "generated_at": "2026-05-20T12:00:00Z",
    }


@router.get("/risk/{ticker}")
async def ai_risk(
    ticker: str,
    user: dict = Depends(get_current_user),
    
):
    logger.debug("ai_risk: ticker=%s", ticker)
    ticker = ticker.upper()
    name = _fake_ticker_name(ticker)
    risk_score = round(random.uniform(1, 10), 1)

    risk_catalog = [
        {"name": "Market Risk", "severity": random.choice(["Low", "Medium", "High"]),
         "description": "Systematic market exposure through beta correlation with broad market indices.",
         "mitigation": "Hedging via put options or inverse ETFs; reducing position size."},
        {"name": "Concentration Risk", "severity": random.choice(["Low", "Medium", "High"]),
         "description": "Overweight exposure to a single sector, geography, or revenue stream.",
         "mitigation": "Diversification across uncorrelated assets and geographic regions."},
        {"name": "Valuation Risk", "severity": random.choice(["Low", "Medium", "High"]),
         "description": "Trading at elevated multiples relative to historical averages and peer group.",
         "mitigation": "Dollar-cost averaging; waiting for a pullback to accumulate."},
        {"name": "Liquidity Risk", "severity": random.choice(["Low", "Medium", "High"]),
         "description": "Thin trading volumes could impact execution quality in stressed conditions.",
         "mitigation": "Limit orders; avoiding illiquid securities in concentrated portfolios."},
        {"name": "Regulatory Risk", "severity": random.choice(["Low", "Medium", "High"]),
         "description": "Pending legislation or regulatory actions could impact business model.",
         "mitigation": "Monitoring regulatory developments; reducing exposure before catalysts."},
        {"name": "Technology Risk", "severity": random.choice(["Low", "Medium", "High"]),
         "description": "Disruption risk from emerging technologies or AI-native competitors.",
         "mitigation": "Investing in companies with strong innovation pipelines and R&D moats."},
        {"name": "Currency Risk", "severity": random.choice(["Low", "Medium", "High"]),
         "description": "International revenue exposure creates FX translation volatility.",
         "mitigation": "Currency hedging via forwards or ETFs; natural hedging through operations."},
        {"name": "Geopolitical Risk", "severity": random.choice(["Low", "Medium", "High"]),
         "description": "Operations in or exposure to geopolitically sensitive regions.",
         "mitigation": "Geographic diversification; political risk insurance."},
    ]

    selected_risks = random.sample(risk_catalog, min(5, len(risk_catalog)))

    return {
        "ticker": ticker,
        "name": name,
        "overall_risk_score": risk_score,
        "risk_label": _risk_score_to_label(risk_score),
        "top_risks": selected_risks,
        "risk_summary": (
            f"{name} carries a {_risk_score_to_label(risk_score).lower()} profile with a composite score "
            f"of {risk_score}/10. The primary concerns revolve around "
            f"{selected_risks[0]['name'].lower()} and {selected_risks[1]['name'].lower()}."
        ),
        "cat_commentary": (
            f"🐱 The cat has analyzed {ticker}'s risk profile. "
            f"{random.choice([
                'The tail is twitching — proceed with caution.',
                'The cat is purring. That means low risk. Probably.',
                'The cat knocked this stock off the table. Literally.',
                'Risk is like a cat: unpredictable, but manageable with proper handling.',
            ])}"
        ),
        "generated_at": "2026-05-20T12:00:00Z",
    }


@router.get("/trade/{ticker}")
async def ai_trade(
    ticker: str,
    user: dict = Depends(get_current_user),
    
):
    logger.debug("ai_summary: ticker=%s", ticker)
    ticker = ticker.upper()
    name = _fake_ticker_name(ticker)
    direction = random.choice(["BUY", "SELL", "HOLD"])
    confidence = round(random.uniform(0.3, 0.95), 2)
    current_price = round(random.uniform(50, 800), 2)
    entry_low = round(current_price * (1 - random.uniform(0.02, 0.15)), 2)
    entry_high = current_price
    target_price = round(current_price * (1 + random.uniform(0.05, 0.35)), 2)
    stop_loss = round(current_price * (1 - random.uniform(0.05, 0.25)), 2)

    theses = {
        "BUY": (
            f"{name} presents a compelling entry point at current levels. "
            f"Technical indicators show {random.choice(['a bullish flag pattern', 'oversold RSI conditions', 'a golden cross forming', 'support at key moving average'])} "
            f"while fundamentals support upside with {random.choice(['accelerating revenue growth', 'margin expansion potential', 'strong free cash flow generation', 'a catalyst-rich pipeline'])}. "
            f"Risk/reward favors the long side with asymmetric upside."
        ),
        "SELL": (
            f"{name} faces headwinds that suggest de-risking is warranted. "
            f"The stock has {random.choice(['broken below key support levels', 'formed a death cross', 'shown declining relative strength', 'experienced distribution days'])} "
            f"and valuation appears stretched at {random.choice(['30x+ forward earnings', 'elevated EV/EBITDA', 'peak-cycle margins'])}. "
            f"Locking in profits or cutting losses before further downside is prudent."
        ),
        "HOLD": (
            f"{name} remains a quality name but lacks a clear near-term catalyst. "
            f"Current positioning is appropriate and neither adding nor reducing is recommended. "
            f"Wait for {random.choice(['the next earnings report', 'a better risk/reward entry', 'technical confirmation', 'macro clarity'])} "
            f"before taking directional action."
        ),
    }

    return {
        "ticker": ticker,
        "name": name,
        "current_price": current_price,
        "direction": direction,
        "confidence": confidence,
        "confidence_label": "High" if confidence > 0.7 else "Medium" if confidence > 0.4 else "Low",
        "entry_range": {"low": entry_low, "high": entry_high},
        "target_price": target_price,
        "stop_loss": stop_loss,
        "risk_reward_ratio": round((target_price - entry_high) / (entry_high - stop_loss), 2) if entry_high != stop_loss else 0,
        "thesis": theses[direction],
        "time_horizon": random.choice(["short-term (1-4 weeks)", "medium-term (1-6 months)", "long-term (6-12 months)"]),
        "cat_commentary": (
            f"{_cat_commentary()} "
            f"{random.choice([
                f'The cat says {direction} on {ticker}. The cat is never wrong. Usually.',
                f'{direction.upper()} — the whiskers have spoken.',
                f'The cat stared at the chart for 3 hours. It says {direction}.',
            ])}"
        ),
        "generated_at": "2026-05-20T12:00:00Z",
    }


@router.get("/choose")
async def ai_choose(
    tickers: str = Query(..., description="Comma-separated tickers (at least 2)"),
    capital: float = Query(..., description="Capital amount to allocate"),
    user: dict = Depends(get_current_user),
    
):
    logger.debug("ai_choose: tickers=%s capital=%s", tickers, capital)
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    if len(ticker_list) < 2:
        raise HTTPException(status_code=400, detail="At least 2 tickers required")

    ticker_list = ticker_list[:5]
    analysis = []
    for t in ticker_list:
        score = round(random.uniform(1, 10), 1)
        analysis.append({
            "ticker": t,
            "name": _fake_ticker_name(t),
            "overall_score": score,
            "score_components": {
                "value": round(random.uniform(1, 10), 1),
                "growth": round(random.uniform(1, 10), 1),
                "momentum": round(random.uniform(1, 10), 1),
                "quality": round(random.uniform(1, 10), 1),
                "sentiment": round(random.uniform(1, 10), 1),
            },
            "current_price": round(random.uniform(20, 800), 2),
            "target_price": round(random.uniform(30, 1000), 2),
            "upside_pct": round(random.uniform(-15, 50), 1),
            "risk_level": random.choice(["Low", "Medium", "High"]),
        })

    analysis.sort(key=lambda x: x["overall_score"], reverse=True)
    best = analysis[0]

    allocations = {}
    remaining = capital
    for i, a in enumerate(analysis):
        if i == len(analysis) - 1:
            allocations[a["ticker"]] = round(remaining, 2)
        else:
            weight = a["overall_score"] / sum(a["overall_score"] for a in analysis)
            alloc = round(capital * weight, 2)
            allocations[a["ticker"]] = alloc
            remaining -= alloc

    return {
        "best_pick": best["ticker"],
        "best_name": best["name"],
        "best_score": best["overall_score"],
        "capital": capital,
        "analysis": analysis,
        "suggested_allocation": allocations,
        "reasoning": (
            f"After comprehensive multi-factor analysis, **{best['ticker']}** emerges as the top pick "
            f"with a composite score of {best['overall_score']}/10. "
            f"The stock offers compelling {random.choice(['value', 'growth', 'momentum'])} characteristics "
            f"with {best['upside_pct']}% upside potential to target price. "
            f"Risk is assessed as {best['risk_level'].lower()} within the current market environment."
        ),
        "cat_commentary": (
            f"🐱 After careful consideration (and chasing {len(ticker_list)} laser pointers), "
            f"Miau AI declares **{best['ticker']}** the winner. "
            f"{random.choice([
                'The cat has chosen wisely.',
                'This pick comes with a purr of approval.',
                'The cat is putting their tuna budget into this one.',
                'Winner winner chicken (tuna) dinner!',
            ])}"
        ),
        "generated_at": "2026-05-20T12:00:00Z",
    }
