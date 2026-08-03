import logging
logger = logging.getLogger(__name__)

GUILDS = {
    "ygg": {"name": "Yield Guild Games", "members": 12500, "scholars": 4500, "total_earnings_usd": "$85M", "games": ["Axie", "Splinterlands", "Pegaxy"], "tvl_usd": "$180M"},
    "merit_circle": {"name": "Merit Circle", "members": 8500, "scholars": 3200, "total_earnings_usd": "$42M", "games": ["Axie", "Cyball", "Thetan Arena"], "tvl_usd": "$95M"},
    "guildfi": {"name": "GuildFi", "members": 6200, "scholars": 2800, "total_earnings_usd": "$28M", "games": ["Axie", "Pegaxy", "Genopets"], "tvl_usd": "$65M"},
    "avocado": {"name": "Avocado Guild", "members": 4800, "scholars": 1800, "total_earnings_usd": "$18M", "games": ["Axie", "Cyball"], "tvl_usd": "$42M"},
}

async def list_guilds() -> list[dict]:
    return [{"id": k, **v} for k, v in GUILDS.items()]

async def get_guild(guild_id: str) -> dict:
    g = GUILDS.get(guild_id)
    if not g:
        return {"error": "Guild not found"}
    return {"id": guild_id, **g}

async def scholarship_roi(scholarship_cost_usd: float, expected_monthly_earnings: float, guild_split_pct: float = 30) -> dict:
    scholar_share = expected_monthly_earnings * (100 - guild_split_pct) / 100
    months_to_break_even = scholarship_cost_usd / scholar_share if scholar_share > 0 else 0
    annual_roi = (scholar_share * 12 / scholarship_cost_usd - 1) * 100 if scholarship_cost_usd > 0 else 0
    return {
        "scholarship_cost": scholarship_cost_usd,
        "gross_monthly": expected_monthly_earnings,
        "guild_split_pct": guild_split_pct,
        "scholar_share": round(scholar_share, 2),
        "months_to_breakeven": round(months_to_break_even, 1),
        "annual_roi_pct": round(annual_roi, 1),
        "verdict": "good" if annual_roi > 50 else ("ok" if annual_roi > 20 else "poor"),
    }

async def guild_comparison() -> list[dict]:
    results = []
    for gid, g in GUILDS.items():
        earnings_per_member = 0
        if g["members"] > 0:
            earnings_str = g["total_earnings_usd"].replace("$", "").replace("M", "e6").replace("B", "e9")
            earnings_per_member = float(earnings_str) / g["members"]
        results.append({"id": gid, "name": g["name"], "members": g["members"], "scholars": g["scholars"], "earnings_per_member": round(earnings_per_member, 0)})
    return sorted(results, key=lambda x: x["earnings_per_member"], reverse=True)
