"""Learning XP system — earn XP for completing lessons, quizzes, streaks."""

import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

XP_LESSON_COMPLETE = 50
XP_QUIZ_PASS = 100
XP_COURSE_COMPLETE = 500
XP_STREAK_BONUS = 25
XP_DAILY_CHALLENGE = 75


async def award_xp(db: AsyncSession, user_id: str, amount: int, reason: str) -> dict:
    await db.execute(
        text("""
            INSERT INTO education_xp (id, user_id, amount, reason)
            VALUES (gen_random_uuid(), :uid, :amt, :reason)
        """),
        {"uid": user_id, "amt": amount, "reason": reason},
    )
    total = await db.execute(
        text("SELECT COALESCE(SUM(amount), 0) FROM education_xp WHERE user_id = :uid"),
        {"uid": user_id},
    )
    await db.commit()
    total_xp = total.scalar() or 0
    return {"awarded": amount, "total_xp": total_xp, "reason": reason, "level": _calc_level(total_xp)}


async def get_xp(db: AsyncSession, user_id: str) -> dict:
    total = await db.execute(
        text("SELECT COALESCE(SUM(amount), 0) FROM education_xp WHERE user_id = :uid"),
        {"uid": user_id},
    )
    total_xp = total.scalar() or 0
    recent = await db.execute(
        text("SELECT amount, reason, created_at FROM education_xp WHERE user_id = :uid ORDER BY created_at DESC LIMIT 10"),
        {"uid": user_id},
    )
    return {
        "total_xp": total_xp,
        "level": _calc_level(total_xp),
        "xp_to_next_level": _xp_for_next(total_xp),
        "recent_activity": [dict(r) for r in recent.mappings().all()],
    }


async def get_leaderboard(db: AsyncSession, limit: int = 20) -> list[dict]:
    rows = await db.execute(
        text("""
            SELECT u.username, COALESCE(SUM(x.amount), 0) as total_xp
            FROM education_xp x
            JOIN users u ON u.id = x.user_id
            GROUP BY u.username
            ORDER BY total_xp DESC
            LIMIT :lim
        """),
        {"lim": limit},
    )
    return [{"rank": i + 1, **dict(r)} for i, r in enumerate(rows.mappings().all())]


def _calc_level(xp: int) -> int:
    return int(xp ** 0.5) + 1


def _xp_for_next(xp: int) -> int:
    current_level = _calc_level(xp)
    return (current_level ** 2) - xp
