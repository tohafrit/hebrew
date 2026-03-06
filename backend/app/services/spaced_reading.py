"""Spaced reading: re-read texts at intervals, track comprehension improvement."""

import uuid
from datetime import datetime, timedelta

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import SpacedReadingSchedule, ReadingText, UserReadingSession

INTERVALS = [1, 3, 7, 14, 30, 60, 90]


async def get_due_readings(
    db: AsyncSession, user_id: uuid.UUID, limit: int = 5
) -> list[dict]:
    """Get texts due for spaced re-reading."""
    now = datetime.utcnow()
    result = await db.execute(
        select(SpacedReadingSchedule, ReadingText)
        .join(ReadingText, SpacedReadingSchedule.text_id == ReadingText.id)
        .where(
            SpacedReadingSchedule.user_id == user_id,
            SpacedReadingSchedule.next_review <= now,
        )
        .order_by(SpacedReadingSchedule.next_review)
        .limit(limit)
    )
    rows = result.all()
    return [
        {
            "schedule_id": str(s.id),
            "text_id": s.text_id,
            "title_he": t.title_he,
            "title_ru": t.title_ru,
            "level_id": t.level_id,
            "review_count": s.review_count,
            "last_known_pct": s.last_known_pct,
            "interval_days": s.interval_days,
            "next_review": s.next_review.isoformat(),
        }
        for s, t in rows
    ]


async def enroll_text(
    db: AsyncSession, user_id: uuid.UUID, text_id: int
) -> dict:
    """Enroll a text for spaced reading."""
    # Check if already enrolled
    existing = await db.scalar(
        select(SpacedReadingSchedule).where(
            SpacedReadingSchedule.user_id == user_id,
            SpacedReadingSchedule.text_id == text_id,
        )
    )
    if existing:
        return {"enrolled": False, "message": "Already enrolled"}

    schedule = SpacedReadingSchedule(
        user_id=user_id,
        text_id=text_id,
        next_review=datetime.utcnow() + timedelta(days=1),
        interval_days=1,
        review_count=0,
        last_known_pct=0,
    )
    db.add(schedule)
    await db.commit()
    return {"enrolled": True, "message": "Enrolled for spaced reading"}


async def record_reading_review(
    db: AsyncSession, user_id: uuid.UUID, text_id: int, known_pct: int
) -> dict:
    """Record a spaced reading review and advance/regress the interval."""
    schedule = await db.scalar(
        select(SpacedReadingSchedule).where(
            SpacedReadingSchedule.user_id == user_id,
            SpacedReadingSchedule.text_id == text_id,
        )
    )
    if not schedule:
        return {"error": "Not enrolled"}

    old_pct = schedule.last_known_pct
    schedule.last_known_pct = known_pct
    schedule.review_count += 1

    # Advance or regress interval
    current_idx = INTERVALS.index(schedule.interval_days) if schedule.interval_days in INTERVALS else 0

    if known_pct > old_pct or known_pct >= 80:
        # Improvement: advance interval
        new_idx = min(current_idx + 1, len(INTERVALS) - 1)
    elif known_pct < old_pct - 10:
        # Decline: regress interval
        new_idx = max(current_idx - 1, 0)
    else:
        # Stable: keep same interval
        new_idx = current_idx

    schedule.interval_days = INTERVALS[new_idx]
    schedule.next_review = datetime.utcnow() + timedelta(days=schedule.interval_days)

    await db.commit()
    return {
        "review_count": schedule.review_count,
        "interval_days": schedule.interval_days,
        "known_pct": known_pct,
        "improved": known_pct > old_pct,
    }


async def get_reading_improvement(
    db: AsyncSession, user_id: uuid.UUID, text_id: int | None = None
) -> list[dict]:
    """Get known_pct improvement over time for enrolled texts."""
    q = select(SpacedReadingSchedule).where(SpacedReadingSchedule.user_id == user_id)
    if text_id:
        q = q.where(SpacedReadingSchedule.text_id == text_id)

    result = await db.execute(q.order_by(SpacedReadingSchedule.created_at))
    schedules = result.scalars().all()

    return [
        {
            "text_id": s.text_id,
            "review_count": s.review_count,
            "last_known_pct": s.last_known_pct,
            "interval_days": s.interval_days,
            "created_at": s.created_at.isoformat(),
        }
        for s in schedules
    ]
