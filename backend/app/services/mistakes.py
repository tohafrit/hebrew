import uuid
from datetime import datetime, timedelta

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import Exercise, ExerciseResult
from app.models.srs import SRSCard, SRSReview


async def get_exercise_mistakes(
    db: AsyncSession, user_id: uuid.UUID, *, days: int = 30, limit: int = 50
) -> list[dict]:
    """Get recent wrong exercise answers for a user."""
    cutoff = datetime.utcnow() - timedelta(days=days)

    q = (
        select(ExerciseResult, Exercise)
        .join(Exercise, ExerciseResult.exercise_id == Exercise.id)
        .where(
            and_(
                ExerciseResult.user_id == user_id,
                ExerciseResult.is_correct == False,  # noqa: E712
                ExerciseResult.created_at >= cutoff,
            )
        )
        .order_by(ExerciseResult.created_at.desc())
        .limit(limit)
    )
    result = await db.execute(q)
    rows = result.all()

    return [
        {
            "exercise_id": ex_result.exercise_id,
            "exercise_type": exercise.type,
            "prompt": exercise.prompt_json,
            "user_answer": ex_result.answer_json,
            "correct_answer": exercise.answer_json,
            "created_at": ex_result.created_at,
        }
        for ex_result, exercise in rows
    ]


async def get_srs_failures(
    db: AsyncSession, user_id: uuid.UUID, *, days: int = 30, limit: int = 50
) -> list[dict]:
    """Get recent failed SRS reviews (quality <= 1) for a user, deduped by card."""
    cutoff = datetime.utcnow() - timedelta(days=days)

    # Subquery to get the latest failed review per card
    q = (
        select(SRSReview, SRSCard)
        .join(SRSCard, SRSReview.card_id == SRSCard.id)
        .where(
            and_(
                SRSCard.user_id == user_id,
                SRSReview.quality <= 1,
                SRSReview.reviewed_at >= cutoff,
            )
        )
        .order_by(SRSReview.reviewed_at.desc())
        .limit(limit)
    )
    result = await db.execute(q)
    rows = result.all()

    # Dedupe by card_id, keeping most recent
    seen_cards: set[str] = set()
    deduped = []
    for review, card in rows:
        card_key = str(card.id)
        if card_key in seen_cards:
            continue
        seen_cards.add(card_key)
        deduped.append({
            "card_id": card_key,
            "card_type": card.card_type,
            "front": card.front_json,
            "back": card.back_json,
            "quality": review.quality,
            "reviewed_at": review.reviewed_at,
        })

    return deduped
