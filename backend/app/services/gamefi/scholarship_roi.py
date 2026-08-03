import logging
logger = logging.getLogger(__name__)

async def calculate(scholarship_cost_usd: float, expected_monthly_earnings_usd: float, guild_split_pct: float = 30) -> dict:
    scholar_share = expected_monthly_earnings_usd * (100 - guild_split_pct) / 100
    guild_share = expected_monthly_earnings_usd * guild_split_pct / 100
    months_to_breakeven = scholarship_cost_usd / scholar_share if scholar_share > 0 else 0
    annual_roi = (scholar_share * 12 / scholarship_cost_usd - 1) * 100 if scholarship_cost_usd > 0 else 0
    return {
        "scholarship_cost": scholarship_cost_usd,
        "gross_monthly": expected_monthly_earnings_usd,
        "guild_split_pct": guild_split_pct,
        "guild_share": round(guild_share, 2),
        "scholar_share": round(scholar_share, 2),
        "months_to_breakeven": round(months_to_breakeven, 1),
        "annual_roi_pct": round(annual_roi, 1),
        "5yr_profit": round(scholar_share * 60 - scholarship_cost_usd, 2),
        "verdict": "good" if annual_roi > 50 else ("ok" if annual_roi > 20 else "poor"),
    }

async def compare_scenarios(base_cost: float = 500) -> list[dict]:
    scenarios = [
        {"name": "Conservative", "monthly": 80, "split": 20},
        {"name": "Moderate", "monthly": 150, "split": 30},
        {"name": "Aggressive", "monthly": 250, "split": 40},
    ]
    results = []
    for s in scenarios:
        r = await calculate(base_cost, s["monthly"], s["split"])
        results.append({"scenario": s["name"], **r})
    return results
