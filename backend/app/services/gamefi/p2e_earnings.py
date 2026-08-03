import logging
logger = logging.getLogger(__name__)

PLAYERS = {
    "axie_infinity": {"name": "Axie Infinity", "active_players": 280000, "avg_daily_earnings_usd": 5.80, "top_earners_usd": 850, "total_paid_usd": "$420M"},
    "splinterlands": {"name": "Splinterlands", "active_players": 420000, "avg_daily_earnings_usd": 2.10, "top_earners_usd": 120, "total_paid_usd": "$85M"},
    "alien_worlds": {"name": "Alien Worlds", "active_players": 180000, "avg_daily_earnings_usd": 1.50, "top_earners_usd": 65, "total_paid_usd": "$45M"},
    "sandbox": {"name": "The Sandbox", "active_players": 95000, "avg_daily_earnings_usd": 4.20, "top_earners_usd": 350, "total_paid_usd": "$180M"},
    "gods_unchained": {"name": "Gods Unchained", "active_players": 65000, "avg_daily_earnings_usd": 3.40, "top_earners_usd": 200, "total_paid_usd": "$62M"},
}

async def list_games() -> list[dict]:
    return [{"id": k, **v} for k, v in PLAYERS.items()]

async def get_game(game_id: str) -> dict:
    g = PLAYERS.get(game_id)
    if not g:
        return {"error": "Game not found"}
    return {"id": game_id, **g}

async def simulate_earnings(game_id: str, hours_per_day: float = 4) -> dict:
    g = PLAYERS.get(game_id)
    if not g:
        return {"error": "Game not found"}
    hourly = g["avg_daily_earnings_usd"] / 4
    return {
        "game": g["name"],
        "hours_per_day": hours_per_day,
        "daily": round(hourly * hours_per_day, 2),
        "weekly": round(hourly * hours_per_day * 7, 2),
        "monthly": round(hourly * hours_per_day * 30, 2),
        "yearly": round(hourly * hours_per_day * 365, 2),
        "roi_pct": round(hourly * hours_per_day * 365 / 1000 * 100, 1),
    }

async def leaderboard() -> list[dict]:
    sorted_games = sorted(PLAYERS.values(), key=lambda x: x["avg_daily_earnings_usd"], reverse=True)
    return [{"rank": i+1, **g} for i, g in enumerate(sorted_games)]
