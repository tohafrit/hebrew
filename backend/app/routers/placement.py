from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.placement import (
    PlacementQuestion,
    PlacementTestResponse,
    PlacementSubmitRequest,
    PlacementResultOut,
)
from app.services.placement import generate_placement_test, score_placement_test, save_placement_result

router = APIRouter(prefix="/placement", tags=["placement"])

# Store generated tests in memory keyed by user_id (simple approach)
_test_cache: dict[str, list[dict]] = {}


@router.get("/test", response_model=PlacementTestResponse)
async def get_placement_test(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Generate a 28-question placement test."""
    questions = await generate_placement_test(db)
    _test_cache[str(user.id)] = questions

    # Return questions without correct_answer
    safe_questions = []
    for q in questions:
        safe_questions.append(PlacementQuestion(
            index=q["index"],
            level=q["level"],
            type=q["type"],
            prompt_he=q["prompt_he"],
            prompt_ru=q["prompt_ru"],
            hint=q["hint"],
            options=q["options"],
            correct_answer="",  # hidden from client
        ))
    return PlacementTestResponse(questions=safe_questions)


@router.post("/submit", response_model=PlacementResultOut)
async def submit_placement_test(
    body: PlacementSubmitRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Score placement test and assign user level."""
    user_key = str(user.id)
    questions = _test_cache.pop(user_key, None)

    if not questions:
        # Regenerate if cache miss
        questions = await generate_placement_test(db)

    answers = [{"index": a.index, "answer": a.answer} for a in body.answers]
    assigned_level, total_correct, total_questions, per_level = score_placement_test(questions, answers)

    await save_placement_result(
        db, user, assigned_level, total_correct, total_questions, per_level,
    )

    return PlacementResultOut(
        assigned_level=assigned_level,
        total_questions=total_questions,
        total_correct=total_correct,
        per_level=per_level,
    )
