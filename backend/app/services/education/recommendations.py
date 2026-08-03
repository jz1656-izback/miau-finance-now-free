"""Course recommendations — suggest courses based on user activity."""

import logging
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def recommend_courses(db: AsyncSession, user_id: str, limit: int = 5) -> list[dict]:
    enrolled = await db.execute(
        text("SELECT course_id FROM education_enrollments WHERE user_id = :uid"),
        {"uid": user_id},
    )
    enrolled_ids = [str(r["course_id"]) for r in enrolled.mappings().all()]

    if enrolled_ids:
        rows = await db.execute(
            text("""
                SELECT c.slug, c.title, c.description, c.difficulty, c.icon, c.estimated_minutes, c.lesson_count
                FROM education_courses c
                WHERE c.is_published = TRUE AND c.id NOT IN :exclude
                ORDER BY c.order_index
                LIMIT :lim
            """),
            {"exclude": tuple(enrolled_ids), "lim": limit},
        )
    else:
        rows = await db.execute(
            text("""
                SELECT slug, title, description, difficulty, icon, estimated_minutes, lesson_count
                FROM education_courses WHERE is_published = TRUE ORDER BY order_index LIMIT :lim
            """),
            {"lim": limit},
        )

    return [dict(r) for r in rows.mappings().all()]
