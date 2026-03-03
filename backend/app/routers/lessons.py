from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.lesson import (
    LessonBrief, LessonDetail, ExerciseOut,
    ExerciseCheckRequest, ExerciseCheckResponse,
    ReadingTextBrief, ReadingTextDetail,
)
from app.services.lesson import (
    list_lessons, get_lesson_detail, get_lesson_exercises,
    get_exercise, check_answer, save_exercise_result,
    list_reading_texts, get_reading_text,
    get_lesson_completion,
)
from app.services.gamification import award_xp, check_and_award_achievements

router = APIRouter(tags=["lessons"])


# ── Lessons ────────────────────────────────────────────────────────────────

@router.get("/lessons", response_model=list[LessonBrief])
async def get_lessons(
    level_id: int | None = Query(None),
    type: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lessons = await list_lessons(db, level_id=level_id, lesson_type=type)
    lesson_ids = [l.id for l in lessons]
    completions = await get_lesson_completion(db, user.id, lesson_ids)
    result = []
    for l in lessons:
        brief = LessonBrief.model_validate(l)
        brief.completed = completions.get(l.id, False)
        result.append(brief)
    return result


@router.get("/lessons/{lesson_id}", response_model=LessonDetail)
async def get_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    lesson = await get_lesson_detail(db, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    exercises = await get_lesson_exercises(db, lesson_id)
    detail = LessonDetail.model_validate(lesson)
    detail.exercises = [ExerciseOut.model_validate(e) for e in exercises]
    return detail


@router.get("/lessons/{lesson_id}/exercises", response_model=list[ExerciseOut])
async def get_exercises(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    exercises = await get_lesson_exercises(db, lesson_id)
    return [ExerciseOut.model_validate(e) for e in exercises]


# ── Exercise checking ──────────────────────────────────────────────────────

@router.post("/exercises/check", response_model=ExerciseCheckResponse)
async def check_exercise(
    req: ExerciseCheckRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    exercise = await get_exercise(db, req.exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    is_correct, correct_answer, explanation = check_answer(exercise, req.answer)
    points = exercise.points if is_correct else 2

    await save_exercise_result(
        db, user_id=user.id, exercise_id=exercise.id,
        answer=req.answer, is_correct=is_correct,
    )

    xp_reason = "exercise_correct" if is_correct else "exercise_wrong"
    total_xp = await award_xp(db, user, points, xp_reason)
    new_achievements = await check_and_award_achievements(db, user)

    return ExerciseCheckResponse(
        correct=is_correct,
        correct_answer=correct_answer,
        explanation=explanation,
        points_earned=points,
        xp_earned=points,
        total_xp=total_xp,
        new_achievements=new_achievements,
    )


# ── Reading texts ──────────────────────────────────────────────────────────

@router.get("/reading", response_model=list[ReadingTextBrief])
async def get_reading_texts(
    level_id: int | None = Query(None),
    category: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    texts = await list_reading_texts(db, level_id=level_id, category=category)
    return [ReadingTextBrief.model_validate(t) for t in texts]


@router.get("/reading/{text_id}", response_model=ReadingTextDetail)
async def get_reading_text_detail(
    text_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    text = await get_reading_text(db, text_id)
    if not text:
        raise HTTPException(status_code=404, detail="Reading text not found")
    return ReadingTextDetail.model_validate(text)
