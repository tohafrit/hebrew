import uuid
from datetime import datetime, timezone, timedelta

from sqlalchemy import select, func, cast, Date, and_, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import Exercise, ExerciseResult
from app.models.srs import SRSCard, SRSReview


async def get_analytics(db: AsyncSession, user_id: uuid.UUID) -> dict:
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)

    # 1. Daily accuracy trend (30 days)
    accuracy_q = (
        select(
            cast(ExerciseResult.created_at, Date).label("day"),
            func.count().label("total"),
            func.sum(case((ExerciseResult.is_correct == True, 1), else_=0)).label("correct"),  # noqa: E712
        )
        .where(
            and_(
                ExerciseResult.user_id == user_id,
                ExerciseResult.created_at >= thirty_days_ago,
            )
        )
        .group_by("day")
        .order_by("day")
    )
    accuracy_rows = (await db.execute(accuracy_q)).all()
    accuracy_trend = [
        {
            "date": str(row.day),
            "accuracy": round(row.correct / row.total * 100, 1) if row.total > 0 else 0,
            "total": row.total,
        }
        for row in accuracy_rows
    ]

    # 2. SRS retention rate
    srs_q = (
        select(
            func.count().label("total"),
            func.sum(case((SRSReview.quality >= 2, 1), else_=0)).label("retained"),
            func.avg(SRSReview.response_time_ms).label("avg_time"),
        )
        .join(SRSCard, SRSReview.card_id == SRSCard.id)
        .where(
            and_(
                SRSCard.user_id == user_id,
                SRSReview.reviewed_at >= thirty_days_ago,
            )
        )
    )
    srs_row = (await db.execute(srs_q)).one()
    srs_total = srs_row.total or 0
    srs_retained = srs_row.retained or 0
    retention_rate = round(srs_retained / srs_total * 100, 1) if srs_total > 0 else 0
    avg_time = int(srs_row.avg_time) if srs_row.avg_time else None

    # 3. Vocabulary growth (cumulative SRS cards by creation date)
    vocab_q = (
        select(
            cast(SRSCard.created_at, Date).label("day"),
            func.count().label("count"),
        )
        .where(SRSCard.user_id == user_id)
        .group_by("day")
        .order_by("day")
    )
    vocab_rows = (await db.execute(vocab_q)).all()
    cumulative = 0
    vocab_growth = []
    for row in vocab_rows:
        cumulative += row.count
        vocab_growth.append({"date": str(row.day), "cumulative": cumulative})

    # 4. Exercise type breakdown
    breakdown_q = (
        select(
            Exercise.type,
            func.count().label("total"),
            func.sum(case((ExerciseResult.is_correct == True, 1), else_=0)).label("correct"),  # noqa: E712
        )
        .join(Exercise, ExerciseResult.exercise_id == Exercise.id)
        .where(
            and_(
                ExerciseResult.user_id == user_id,
                ExerciseResult.created_at >= thirty_days_ago,
            )
        )
        .group_by(Exercise.type)
    )
    breakdown_rows = (await db.execute(breakdown_q)).all()
    exercise_breakdown = [
        {
            "type": row.type,
            "total": row.total,
            "correct": row.correct,
            "accuracy": round(row.correct / row.total * 100, 1) if row.total > 0 else 0,
        }
        for row in breakdown_rows
    ]

    # 5. Weakest areas (sorted by accuracy ascending, top 5)
    weakest_areas = sorted(exercise_breakdown, key=lambda x: x["accuracy"])[:5]

    return {
        "accuracy_trend": accuracy_trend,
        "srs_retention_rate": retention_rate,
        "srs_total_reviews": srs_total,
        "response_time_avg_ms": avg_time,
        "vocab_growth": vocab_growth,
        "exercise_breakdown": exercise_breakdown,
        "weakest_areas": [
            {"type": a["type"], "accuracy": a["accuracy"], "total": a["total"]}
            for a in weakest_areas
        ],
    }
