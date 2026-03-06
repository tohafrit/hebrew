from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.minimal_pairs import (
    MinimalPairQuestion,
    MinimalPairsDrillResponse,
    MinimalPairCheckRequest,
    MinimalPairCheckResponse,
)
from app.services.minimal_pairs import get_minimal_pairs_drill, check_minimal_pair
from app.services.gamification import award_xp

router = APIRouter(prefix="/minimal-pairs", tags=["minimal-pairs"])


@router.get("/drill", response_model=MinimalPairsDrillResponse)
async def get_drill(
    count: int = Query(10, ge=1, le=20),
    user: User = Depends(get_current_user),
):
    questions = get_minimal_pairs_drill(count)
    return MinimalPairsDrillResponse(
        questions=[MinimalPairQuestion(**q) for q in questions]
    )


@router.post("/check", response_model=MinimalPairCheckResponse)
async def check_answer(
    body: MinimalPairCheckRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    correct = check_minimal_pair(body.pair_id, body.answer_letter, body.correct_letter)
    xp = 0
    if correct:
        xp = 10
        await award_xp(db, user, xp, "minimal_pair_correct")
        await db.commit()
    return MinimalPairCheckResponse(correct=correct, xp_earned=xp)
