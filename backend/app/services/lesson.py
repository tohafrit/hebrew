import uuid
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import Lesson, Exercise, ExerciseResult, ReadingText


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
            is_correct = str(user_answer).strip() == str(correct).strip()
        return is_correct, correct, explanation_text

    elif exercise.type == "fill_blank":
        correct = answer_data.get("correct", "")
        accept = answer_data.get("accept", [correct])
        user_str = str(user_answer).strip()
        stripped = _strip_nikkud(user_str)
        is_correct = user_str in [str(a).strip() for a in accept] or \
                     stripped in [_strip_nikkud(str(a).strip()) for a in accept]
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
            is_correct = user_answer == correct_order
        elif isinstance(user_answer, str):
            is_correct = user_answer.strip() == " ".join(correct_order)
        else:
            is_correct = False
        return is_correct, correct_order, explanation_text

    elif exercise.type in ("dictation", "hebrew_typing", "translate_ru_he"):
        correct = answer_data.get("correct", "")
        accept = answer_data.get("accept", [correct])
        user_str = str(user_answer).strip()
        # Strip nikkud for comparison
        stripped = _strip_nikkud(user_str)
        is_correct = user_str in [str(a).strip() for a in accept] or \
                     stripped in [_strip_nikkud(str(a).strip()) for a in accept]
        return is_correct, correct, explanation_text

    elif exercise.type == "minimal_pairs":
        correct = answer_data.get("correct", "")
        is_correct = str(user_answer).strip().lower() == str(correct).strip().lower()
        return is_correct, correct, explanation_text

    elif exercise.type == "listening_comprehension":
        correct_answers = answer_data.get("correct_answers", [])
        if isinstance(user_answer, list):
            is_correct = user_answer == correct_answers
        else:
            is_correct = False
        return is_correct, correct_answers, explanation_text

    return False, None, explanation_text


def _strip_nikkud(text: str) -> str:
    """Remove Hebrew nikkud (vowel marks) and cantillation marks from text for fuzzy comparison.
    Preserves maqaf (U+05BE, Hebrew hyphen) to keep compound words intact.
    """
    return "".join(
        c for c in text
        if not ('\u0591' <= c <= '\u05BD' or '\u05BF' <= c <= '\u05C7')
    )


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
        created_at=datetime.now(timezone.utc),
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
