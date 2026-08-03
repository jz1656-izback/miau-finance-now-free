from typing import Optional

BADGES = {
    "first_trade": {"name": "First Trade", "description": "Execute your first trade", "icon": "🎯", "requirement": "1 trade"},
    "profitable_week": {"name": "Profitable Week", "description": "Positive P&L for a week", "icon": "📈", "requirement": "positive weekly P&L"},
    "top_10_weekly": {"name": "Weekly Top 10", "description": "Top 10 on weekly leaderboard", "icon": "🏆", "requirement": "top 10 weekly"},
    "top_10_monthly": {"name": "Monthly Top 10", "description": "Top 10 on monthly leaderboard", "icon": "🥇", "requirement": "top 10 monthly"},
    "portfolio_shared": {"name": "Portfolio Sharer", "description": "Share a portfolio publicly", "icon": "📤", "requirement": "1 share"},
    "ai_master": {"name": "AI Master", "description": "Run 10 AI queries", "icon": "🤖", "requirement": "10 AI queries"},
}

POINTS = {
    "trade": 1,
    "profitable_trade": 5,
    "weekly_top10": 20,
    "portfolio_shared": 10,
}

LEVELS = [(0, "Bronze"), (50, "Silver"), (200, "Gold"), (500, "Platinum"), (1000, "Diamond")]


def calculate_reputation(total_points: int) -> dict:
    level = "Bronze"
    for threshold, name in reversed(LEVELS):
        if total_points >= threshold:
            level = name
            break
    next_level = None
    for threshold, name in LEVELS:
        if total_points < threshold:
            next_level = {"name": name, "points_needed": threshold - total_points}
            break
    return {
        "total_points": total_points,
        "level": level,
        "next_level": next_level,
    }


def check_badges(completed: list[str]) -> list[dict]:
    return [BADGES[b] for b in BADGES if b in completed]
