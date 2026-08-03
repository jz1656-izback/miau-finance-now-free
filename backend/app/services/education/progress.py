"""Progress tracking — enrollment, lesson completion, percentage."""

import logging
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def enroll(db: AsyncSession, user_id: str, course_slug: str) -> dict:
    course = await db.execute(
        text("SELECT id, lesson_count FROM education_courses WHERE slug = :slug AND is_published = TRUE"),
        {"slug": course_slug},
    )
    c = course.mappings().first()
    if not c:
        return {"error": "Course not found"}

    existing = await db.execute(
        text("SELECT id FROM education_enrollments WHERE user_id = :uid AND course_id = :cid"),
        {"uid": user_id, "cid": c["id"]},
    )
    if existing.mappings().first():
        return {"status": "already_enrolled"}

    await db.execute(
        text("INSERT INTO education_enrollments (id, user_id, course_id) VALUES (gen_random_uuid(), :uid, :cid)"),
        {"uid": user_id, "cid": c["id"]},
    )
    await db.commit()
    return {"status": "enrolled", "course_id": str(c["id"]), "total_lessons": c["lesson_count"]}


async def complete_lesson(db: AsyncSession, user_id: str, lesson_id: str) -> dict:
    lesson = await db.execute(
        text("SELECT course_id FROM education_lessons WHERE id = :lid"),
        {"lid": lesson_id},
    )
    l = lesson.mappings().first()
    if not l:
        return {"error": "Lesson not found"}

    course = await db.execute(
        text("SELECT lesson_count FROM education_courses WHERE id = :cid"),
        {"cid": l["course_id"]},
    )
    total = course.mappings().first()["lesson_count"]

    enrollment = await db.execute(
        text("""
            UPDATE education_enrollments
            SET completed_lessons = completed_lessons + 1,
                progress_pct = LEAST(100, (completed_lessons + 1)::numeric / :total * 100),
                is_completed = (completed_lessons + 1 >= :total2)
            WHERE user_id = :uid AND course_id = :cid
            RETURNING progress_pct, completed_lessons, is_completed
        """),
        {"uid": user_id, "cid": l["course_id"], "total": total, "total2": total},
    )
    await db.commit()
    result = enrollment.mappings().first()
    return {
        "status": "completed",
        "progress_pct": float(result["progress_pct"]) if result else 0,
        "completed_lessons": result["completed_lessons"] if result else 0,
        "course_completed": result["is_completed"] if result else False,
    }


async def get_progress(db: AsyncSession, user_id: str) -> list[dict]:
    rows = await db.execute(
        text("""
            SELECT e.course_id, c.title, c.slug, c.lesson_count, e.progress_pct,
                   e.completed_lessons, e.quiz_score, e.is_completed, e.enrolled_at, e.completed_at
            FROM education_enrollments e
            JOIN education_courses c ON c.id = e.course_id
            WHERE e.user_id = :uid
            ORDER BY e.enrolled_at DESC
        """),
        {"uid": user_id},
    )
    return [dict(r) for r in rows.mappings().all()]
