"""Certification system — auto-generate certificates on course completion."""

import hashlib
import logging
from datetime import timezone, datetime
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def issue_certificate(db: AsyncSession, user_id: str, enrollment_id: str) -> dict:
    enrollment = await db.execute(
        text("""
            SELECT e.user_id, e.course_id, e.quiz_score, c.title, c.slug, u.username
            FROM education_enrollments e
            JOIN education_courses c ON c.id = e.course_id
            JOIN users u ON u.id = e.user_id
            WHERE e.id = :eid AND e.user_id = :uid AND e.is_completed = TRUE
        """),
        {"eid": enrollment_id, "uid": user_id},
    )
    row = enrollment.mappings().first()
    if not row:
        return {"error": "Enrollment not found or course not completed"}

    raw = f"{user_id}-{row['course_id']}-{datetime.now(timezone.utc).isoformat()}"
    cert_id = hashlib.sha256(raw.encode()).hexdigest()[:16].upper()

    await db.execute(
        text("UPDATE education_enrollments SET certificate_id = :cid, completed_at = NOW() WHERE id = :eid"),
        {"cid": cert_id, "eid": enrollment_id},
    )
    await db.commit()

    return {
        "certificate_id": cert_id,
        "user": row["username"],
        "course": row["title"],
        "course_slug": row["slug"],
        "quiz_score": float(row["quiz_score"]),
        "issued_at": datetime.now(timezone.utc).isoformat(),
        "verify_url": f"/api/v1/education/certificates/{cert_id}",
    }


async def verify_certificate(db: AsyncSession, cert_id: str) -> Optional[dict]:
    row = await db.execute(
        text("""
            SELECT e.certificate_id, u.username, c.title, c.slug, e.quiz_score, e.completed_at
            FROM education_enrollments e
            JOIN users u ON u.id = e.user_id
            JOIN education_courses c ON c.id = e.course_id
            WHERE e.certificate_id = :cid
        """),
        {"cid": cert_id},
    )
    r = row.mappings().first()
    if not r:
        return None
    return dict(r)
