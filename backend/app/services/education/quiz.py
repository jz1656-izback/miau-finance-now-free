"""Quiz engine — multiple choice, true/false, and coding quizzes."""

import json
import logging
import random
from typing import Any, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


async def get_quiz(db: AsyncSession, lesson_id: str) -> list[dict]:
    rows = await db.execute(
        text("SELECT id, question, options, correct_index, explanation, order_index FROM education_quizzes WHERE lesson_id = :lid ORDER BY order_index"),
        {"lid": lesson_id},
    )
    return [dict(r) for r in rows.mappings().all()]


async def submit_answer(db: AsyncSession, user_id: str, lesson_id: str, answers: list[dict]) -> dict:
    rows = await db.execute(
        text("SELECT id, correct_index FROM education_quizzes WHERE lesson_id = :lid"),
        {"lid": lesson_id},
    )
    quiz_map = {str(r["id"]): r["correct_index"] for r in rows.mappings().all()}

    correct = 0
    total = len(quiz_map)
    for a in answers:
        qid = a.get("quiz_id", "")
        selected = a.get("selected_index", -1)
        if quiz_map.get(qid) == selected:
            correct += 1

    score = round((correct / total) * 100, 1) if total > 0 else 0

    await db.execute(
        text("UPDATE education_enrollments SET quiz_score = :score WHERE user_id = :uid AND course_id = (SELECT course_id FROM education_lessons WHERE id = :lid)"),
        {"score": score, "uid": user_id, "lid": lesson_id},
    )
    await db.commit()

    return {"correct": correct, "total": total, "score": score, "passed": score >= 70}


async def generate_practice_quiz(topic: str, count: int = 5) -> list[dict]:
    questions = _QUESTION_BANK.get(topic.lower(), _QUESTION_BANK["general"])
    selected = random.sample(questions, min(count, len(questions)))
    return [{"id": i, **q} for i, q in enumerate(selected)]


_QUESTION_BANK: dict[str, list[dict]] = {
    "terminal": [
        {"question": "What command shows live prices?", "options": ["price <ticker>", "show <ticker>", "live <ticker>", "quote <ticker>"], "correct": 0},
        {"question": "How do you toggle the 3D globe?", "options": ["globe", "world", "map", "3d"], "correct": 2},
        {"question": "Which command clears the screen?", "options": ["reset", "clear", "clean", "erase"], "correct": 1},
    ],
    "portfolio": [
        {"question": "What does 'optimize' do?", "options": ["Max Sharpe", "Min variance", "Equal weight", "All of the above"], "correct": 3},
        {"question": "Which command shows portfolio positions?", "options": ["positions <id>", "holdings <id>", "portfolio <id>", "stocks"], "correct": 2},
    ],
    "general": [
        {"question": "What type of platform is Miau Finance?", "options": ["Banking app", "Terminal-based financial analytics", "Mobile game", "Spreadsheet"], "correct": 1},
        {"question": "Which animal is the mascot?", "options": ["Dog", "Cat", "Fish", "Fox"], "correct": 1},
        {"question": "What format are API responses?", "options": ["XML", "JSON", "CSV", "YAML"], "correct": 1},
    ],
}
