import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.srs import (
    CardWithSchedule,
    CreateCardsRequest,
    CreateCardsResponse,
    LeechCard,
    LeechResponse,
    ReviewRequest,
    ReviewResponse,
    SessionResponse,
    SRSStats,
)
from app.services.srs import (
    create_cards_for_words,
    get_leech_cards,
    get_session_cards,
    get_srs_stats,
    review_card,
)
from app.services.gamification import award_xp, check_and_award_achievements

router = APIRouter(prefix="/srs", tags=["srs"])


@router.post("/cards", response_model=CreateCardsResponse)
async def create_cards(
    body: CreateCardsRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    created = await create_cards_for_words(
        db, user.id, body.word_ids, body.card_types,
    )
    return CreateCardsResponse(created=created)


@router.get("/session", response_model=SessionResponse)
async def get_session(
    limit: int = Query(20, ge=1, le=50),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cards, total_due, new_count = await get_session_cards(db, user.id, limit)
    return SessionResponse(
        cards=[CardWithSchedule(**c) for c in cards],
        total_due=total_due,
        new_cards=new_count,
    )


@router.post("/review", response_model=ReviewResponse)
async def submit_review(
    body: ReviewRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if body.quality < 0 or body.quality > 3:
        raise HTTPException(status_code=400, detail="Quality must be 0-3")
    try:
        result = await review_card(
            db, user.id, body.card_id, body.quality, body.response_time_ms,
        )
        await award_xp(db, user, 5, "review_card")
        await check_and_award_achievements(db, user)
        await db.commit()  # Single commit for review + XP + achievements
        return ReviewResponse(**result)
    except ValueError as e:
        await db.rollback()
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/stats", response_model=SRSStats)
async def stats(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await get_srs_stats(db, user)


@router.get("/leeches", response_model=LeechResponse)
async def leeches(
    threshold: int = Query(5, ge=1, le=20),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    cards = await get_leech_cards(db, user.id, threshold)
    return LeechResponse(
        cards=[LeechCard(**c) for c in cards],
        count=len(cards),
    )
