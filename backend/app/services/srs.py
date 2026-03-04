"""SM-2 spaced repetition engine."""

import uuid
from datetime import datetime, timedelta

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.srs import SRSCard, SRSReview, SRSSchedule
from app.models.word import Word


def sm2_update(
    quality: int,
    repetitions: int,
    ease_factor: float,
    interval_days: float,
    lapses: int,
) -> tuple[float, float, int, int]:
    """Apply SM-2 algorithm.

    Returns (new_interval, new_ease, new_reps, new_lapses).
    """
    if quality >= 2:  # correct
        if repetitions == 0:
            new_interval = 1.0
        elif repetitions == 1:
            new_interval = 6.0
        else:
            new_interval = round(interval_days * ease_factor)
        new_reps = repetitions + 1
        new_lapses = lapses
        # Only update ease factor on correct answers (SM-2 spec)
        new_ease = max(
            1.3,
            ease_factor + 0.1 - (3 - quality) * (0.08 + (3 - quality) * 0.02),
        )
    else:  # incorrect
        new_interval = 1.0
        new_reps = 0
        new_lapses = lapses + 1
        # Preserve ease factor on incorrect answers to avoid death spiral
        new_ease = ease_factor

    return new_interval, new_ease, new_reps, new_lapses


async def create_cards_for_words(
    db: AsyncSession,
    user_id: uuid.UUID,
    word_ids: list[int],
    card_types: list[str],
) -> int:
    """Create SRS cards for given words. Skip duplicates."""
    created = 0
    now = datetime.utcnow()

    for word_id in word_ids:
        # Fetch word data for card content
        word = await db.get(Word, word_id)
        if not word:
            continue

        for card_type in card_types:
            # Check for existing card
            existing = await db.scalar(
                select(SRSCard.id).where(
                    SRSCard.user_id == user_id,
                    SRSCard.content_id == word_id,
                    SRSCard.card_type == card_type,
                )
            )
            if existing:
                continue

            if card_type == "word_he_ru":
                front = {"hebrew": word.hebrew, "transliteration": word.transliteration}
                back = {"translation": word.translation_ru, "pos": word.pos, "root": word.root}
            elif card_type == "word_ru_he":
                front = {"translation": word.translation_ru, "pos": word.pos}
                back = {"hebrew": word.hebrew, "transliteration": word.transliteration, "root": word.root}
            elif card_type == "cloze":
                front = {"hint": word.translation_ru, "pos": word.pos}
                back = {"hebrew": word.hebrew, "transliteration": word.transliteration}
            else:
                front = {"hebrew": word.hebrew}
                back = {"translation": word.translation_ru}

            card = SRSCard(
                user_id=user_id,
                card_type=card_type,
                content_id=word_id,
                front_json=front,
                back_json=back,
            )
            db.add(card)
            await db.flush()

            # Create initial schedule (due immediately)
            schedule = SRSSchedule(
                card_id=card.id,
                next_review=now,
                interval_days=1.0,
                ease_factor=2.5,
                repetitions=0,
                lapses=0,
            )
            db.add(schedule)
            created += 1

    await db.commit()
    return created


async def get_session_cards(
    db: AsyncSession,
    user_id: uuid.UUID,
    limit: int = 20,
) -> tuple[list[dict], int, int]:
    """Get cards due for review. Returns (cards, total_due, new_count)."""
    now = datetime.utcnow()

    # Count total due
    total_due = await db.scalar(
        select(func.count())
        .select_from(SRSCard)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(
            SRSCard.user_id == user_id,
            SRSSchedule.next_review <= now,
        )
    ) or 0

    # Count new (never reviewed)
    new_count = await db.scalar(
        select(func.count())
        .select_from(SRSCard)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(
            SRSCard.user_id == user_id,
            SRSSchedule.repetitions == 0,
            SRSSchedule.next_review <= now,
        )
    ) or 0

    # Fetch due cards: prioritize overdue, then new
    query = (
        select(SRSCard, SRSSchedule)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(
            SRSCard.user_id == user_id,
            SRSSchedule.next_review <= now,
        )
        .order_by(SRSSchedule.next_review)
        .limit(limit)
    )
    result = await db.execute(query)
    rows = result.all()

    cards = []
    for card, schedule in rows:
        cards.append({
            "id": card.id,
            "card_type": card.card_type,
            "content_id": card.content_id,
            "front_json": card.front_json,
            "back_json": card.back_json,
            "next_review": schedule.next_review,
            "interval_days": schedule.interval_days,
            "ease_factor": schedule.ease_factor,
            "repetitions": schedule.repetitions,
            "lapses": schedule.lapses,
        })

    return cards, total_due, new_count


async def review_card(
    db: AsyncSession,
    user_id: uuid.UUID,
    card_id: uuid.UUID,
    quality: int,
    response_time_ms: int | None = None,
) -> dict:
    """Submit a review for a card. Returns updated schedule."""
    # Verify card belongs to user
    card = await db.scalar(
        select(SRSCard).where(SRSCard.id == card_id, SRSCard.user_id == user_id)
    )
    if not card:
        raise ValueError("Card not found")

    schedule = await db.scalar(
        select(SRSSchedule).where(SRSSchedule.card_id == card_id)
    )
    if not schedule:
        raise ValueError("Schedule not found")

    # Record the review
    review = SRSReview(
        card_id=card_id,
        quality=quality,
        response_time_ms=response_time_ms,
    )
    db.add(review)

    # Apply SM-2
    new_interval, new_ease, new_reps, new_lapses = sm2_update(
        quality=quality,
        repetitions=schedule.repetitions,
        ease_factor=schedule.ease_factor,
        interval_days=schedule.interval_days,
        lapses=schedule.lapses,
    )

    schedule.interval_days = new_interval
    schedule.ease_factor = new_ease
    schedule.repetitions = new_reps
    schedule.lapses = new_lapses
    schedule.next_review = datetime.utcnow() + timedelta(days=new_interval)

    await db.commit()

    return {
        "card_id": card_id,
        "next_review": schedule.next_review,
        "interval_days": new_interval,
        "ease_factor": new_ease,
        "repetitions": new_reps,
    }


async def get_leech_cards(
    db: AsyncSession, user_id: uuid.UUID, threshold: int = 5
) -> list[dict]:
    """Get cards with lapses >= threshold (leech cards)."""
    query = (
        select(SRSCard, SRSSchedule)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(SRSCard.user_id == user_id, SRSSchedule.lapses >= threshold)
        .order_by(SRSSchedule.lapses.desc())
    )
    result = await db.execute(query)
    rows = result.all()

    cards = []
    for card, schedule in rows:
        cards.append({
            "id": card.id,
            "card_type": card.card_type,
            "content_id": card.content_id,
            "front_json": card.front_json,
            "back_json": card.back_json,
            "lapses": schedule.lapses,
            "ease_factor": schedule.ease_factor,
        })
    return cards


async def get_srs_stats(db: AsyncSession, user_id: uuid.UUID) -> dict:
    """Get SRS statistics for a user."""
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    total = await db.scalar(
        select(func.count()).select_from(SRSCard).where(SRSCard.user_id == user_id)
    ) or 0

    due = await db.scalar(
        select(func.count())
        .select_from(SRSCard)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(SRSCard.user_id == user_id, SRSSchedule.next_review <= now)
    ) or 0

    new_cards = await db.scalar(
        select(func.count())
        .select_from(SRSCard)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(SRSCard.user_id == user_id, SRSSchedule.repetitions == 0)
    ) or 0

    reviews_today = await db.scalar(
        select(func.count())
        .select_from(SRSReview)
        .join(SRSCard, SRSCard.id == SRSReview.card_id)
        .where(SRSCard.user_id == user_id, SRSReview.reviewed_at >= today_start)
    ) or 0

    avg_ease = await db.scalar(
        select(func.avg(SRSSchedule.ease_factor))
        .select_from(SRSSchedule)
        .join(SRSCard, SRSCard.id == SRSSchedule.card_id)
        .where(SRSCard.user_id == user_id)
    )

    return {
        "total_cards": total,
        "due_today": due,
        "new_cards": new_cards,
        "reviews_today": reviews_today,
        "streak_days": 0,  # TODO: compute from user model
        "average_ease": round(avg_ease, 2) if avg_ease else None,
    }
