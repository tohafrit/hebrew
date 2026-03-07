import uuid
from datetime import datetime, timezone

import sqlalchemy as sa
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import Lesson, Exercise, ExerciseResult, ReadingText
from app.services.hebrew_utils import strip_nikkud as _strip_nikkud, normalize_answer as _normalize_answer, answers_match as _answers_match


async def list_lessons(
    db: AsyncSession,
    level_id: int | None = None,
    lesson_type: str | None = None,
) -> list[Lesson]:
    q = select(Lesson).order_by(Lesson.level_id, Lesson.unit, Lesson.order)
    if level_id is not None:
        q = q.where(Lesson.level_id == level_id)
    if lesson_type is not None:
        q = q.where(Lesson.type == lesson_type)
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_lesson_detail(db: AsyncSession, lesson_id: int) -> Lesson | None:
    result = await db.execute(
        select(Lesson).where(Lesson.id == lesson_id)
    )
    return result.scalar_one_or_none()


async def get_lesson_exercises(db: AsyncSession, lesson_id: int) -> list[Exercise]:
    result = await db.execute(
        select(Exercise)
        .where(Exercise.lesson_id == lesson_id)
        .order_by(Exercise.id)
    )
    return list(result.scalars().all())


async def get_exercise(db: AsyncSession, exercise_id: int) -> Exercise | None:
    result = await db.execute(
        select(Exercise).where(Exercise.id == exercise_id)
    )
    return result.scalar_one_or_none()


def _build_accept_list(answer_data: dict) -> list:
    """Build the full list of accepted answers from answer_json.
    Merges 'correct', 'accept', and 'alternatives' fields.
    """
    correct = answer_data.get("correct", "")
    accept = list(answer_data.get("accept", [correct]))
    alternatives = answer_data.get("alternatives", [])
    if correct and correct not in accept:
        accept.append(correct)
    for alt in alternatives:
        if alt and alt not in accept:
            accept.append(alt)
    return accept


def check_answer(exercise: Exercise, user_answer) -> tuple[bool, str | dict | list | None, str | None]:
    """Check user's answer against the exercise answer_json.
    Returns (is_correct, correct_answer, explanation_text).
    """
    answer_data = exercise.answer_json or {}
    explanation_data = exercise.explanation_json or {}
    explanation_text = explanation_data.get("text") if isinstance(explanation_data, dict) else None

    if exercise.type == "multiple_choice":
        correct = answer_data.get("correct")
        correct_idx = answer_data.get("correct_index")
        # Accept either the answer text or the index
        if isinstance(user_answer, int):
            is_correct = user_answer == correct_idx
        else:
            is_correct = _normalize_answer(str(user_answer)) == _normalize_answer(str(correct))
        return is_correct, correct, explanation_text

    elif exercise.type == "fill_blank":
        correct = answer_data.get("correct", "")
        accept = _build_accept_list(answer_data)
        is_correct = _answers_match(str(user_answer), accept)
        return is_correct, correct, explanation_text

    elif exercise.type == "match_pairs":
        matches = answer_data.get("matches", {})
        if isinstance(user_answer, dict):
            is_correct = user_answer == matches
        else:
            is_correct = False
        return is_correct, matches, explanation_text

    elif exercise.type == "word_order":
        correct_order = answer_data.get("correct_order", [])
        if isinstance(user_answer, list):
            # Normalize each word for comparison
            is_correct = [_normalize_answer(w) for w in user_answer] == \
                         [_normalize_answer(w) for w in correct_order]
        elif isinstance(user_answer, str):
            is_correct = _normalize_answer(user_answer) == _normalize_answer(" ".join(correct_order))
        else:
            is_correct = False
        return is_correct, correct_order, explanation_text

    elif exercise.type in ("dictation", "hebrew_typing", "translate_ru_he"):
        correct = answer_data.get("correct", "")
        accept = _build_accept_list(answer_data)
        is_correct = _answers_match(str(user_answer), accept)
        return is_correct, correct, explanation_text

    elif exercise.type == "minimal_pairs":
        correct = answer_data.get("correct", "")
        is_correct = _normalize_answer(str(user_answer)) == _normalize_answer(str(correct))
        return is_correct, correct, explanation_text

    elif exercise.type == "listening_comprehension":
        correct_answers = answer_data.get("correct_answers", [])
        if isinstance(user_answer, list):
            is_correct = (
                len(user_answer) == len(correct_answers)
                and all(
                    _normalize_answer(str(u)) == _normalize_answer(str(c))
                    for u, c in zip(user_answer, correct_answers)
                )
            )
        else:
            is_correct = False
        return is_correct, correct_answers, explanation_text

    return False, None, explanation_text


async def save_exercise_result(
    db: AsyncSession,
    user_id: uuid.UUID,
    exercise_id: int,
    answer: dict | str | list,
    is_correct: bool,
    time_ms: int | None = None,
) -> ExerciseResult:
    answer_json = answer if isinstance(answer, dict) else {"value": answer}
    result = ExerciseResult(
        user_id=user_id,
        exercise_id=exercise_id,
        answer_json=answer_json,
        is_correct=is_correct,
        time_ms=time_ms,
        created_at=datetime.utcnow(),
    )
    db.add(result)
    await db.flush()
    await db.refresh(result)
    return result


async def get_lesson_completion(
    db: AsyncSession, user_id: uuid.UUID, lesson_ids: list[int]
) -> dict[int, bool]:
    """Check which lessons are completed (all exercises have at least one correct answer)."""
    if not lesson_ids:
        return {}

    # For each lesson, count total exercises and exercises with a correct result
    total_q = (
        select(Exercise.lesson_id, func.count(Exercise.id).label("total"))
        .where(Exercise.lesson_id.in_(lesson_ids))
        .group_by(Exercise.lesson_id)
    )
    total_result = await db.execute(total_q)
    totals = {row.lesson_id: row.total for row in total_result}

    # Exercises with at least one correct answer from this user
    correct_q = (
        select(
            Exercise.lesson_id,
            func.count(func.distinct(Exercise.id)).label("correct_count"),
        )
        .join(ExerciseResult, ExerciseResult.exercise_id == Exercise.id)
        .where(
            Exercise.lesson_id.in_(lesson_ids),
            ExerciseResult.user_id == user_id,
            ExerciseResult.is_correct == True,
        )
        .group_by(Exercise.lesson_id)
    )
    correct_result = await db.execute(correct_q)
    corrects = {row.lesson_id: row.correct_count for row in correct_result}

    return {
        lid: corrects.get(lid, 0) >= totals.get(lid, 1)
        for lid in lesson_ids
        if totals.get(lid, 0) > 0
    }


async def get_lesson_stats(
    db: AsyncSession, user_id: uuid.UUID, lesson_id: int
) -> dict:
    """Compute accuracy stats for a completed lesson."""
    # Get exercise IDs for this lesson
    exercises = await get_lesson_exercises(db, lesson_id)
    if not exercises:
        return {"total": 0, "correct": 0, "accuracy_pct": 0, "time_ms": 0}

    exercise_ids = [e.id for e in exercises]

    # Query results for these exercises by this user
    result = await db.execute(
        select(
            func.count().label("total"),
            func.sum(
                func.cast(ExerciseResult.is_correct, sa.Integer)
            ).label("correct"),
            func.sum(ExerciseResult.time_ms).label("time_ms"),
        )
        .where(
            ExerciseResult.user_id == user_id,
            ExerciseResult.exercise_id.in_(exercise_ids),
        )
    )
    row = result.one()
    total = row.total or 0
    correct = row.correct or 0
    time_ms = row.time_ms or 0
    accuracy_pct = round(correct * 100 / total) if total > 0 else 0

    return {
        "total": total,
        "correct": correct,
        "accuracy_pct": accuracy_pct,
        "time_ms": time_ms,
    }


async def list_reading_texts(
    db: AsyncSession,
    level_id: int | None = None,
    category: str | None = None,
) -> list[ReadingText]:
    q = select(ReadingText).order_by(ReadingText.level_id, ReadingText.id)
    if level_id is not None:
        q = q.where(ReadingText.level_id == level_id)
    if category is not None:
        q = q.where(ReadingText.category == category)
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_reading_text(db: AsyncSession, text_id: int) -> ReadingText | None:
    result = await db.execute(
        select(ReadingText).where(ReadingText.id == text_id)
    )
    return result.scalar_one_or_none()
