"""Leaderboard and weekly challenges."""

import uuid
from datetime import date, datetime, timedelta

from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.gamification import WeeklyChallenge


def _current_monday() -> date:
    """Get the Monday of the current week."""
    today = date.today()
    return today - timedelta(days=today.weekday())


async def get_leaderboard(
    db: AsyncSession, period: str = "all_time", limit: int = 50
) -> list[dict]:
    """Get XP leaderboard. Period: 'all_time' or 'weekly'."""
    if period == "weekly":
        monday = _current_monday()
        # Import here to avoid circular
        from app.models.culture import UserDailyActivity
        q = (
            select(
                User.id,
                User.display_name,
                User.current_level,
                func.coalesce(func.sum(UserDailyActivity.xp_earned), 0).label("xp"),
            )
            .outerjoin(
                UserDailyActivity,
                (UserDailyActivity.user_id == User.id) & (UserDailyActivity.date >= monday),
            )
            .group_by(User.id, User.display_name, User.current_level)
            .order_by(func.coalesce(func.sum(UserDailyActivity.xp_earned), 0).desc())
            .limit(limit)
        )
    else:
        q = (
            select(User.id, User.display_name, User.current_level, User.xp)
            .order_by(User.xp.desc())
            .limit(limit)
        )

    result = await db.execute(q)
    rows = result.all()

    return [
        {
            "rank": i + 1,
            "user_id": str(row[0]),
            "display_name": row[1],
            "level": row[2],
            "xp": row[3],
        }
        for i, row in enumerate(rows)
    ]


async def get_user_rank(
    db: AsyncSession, user_id: uuid.UUID, period: str = "all_time"
) -> dict:
    """Get a specific user's rank."""
    board = await get_leaderboard(db, period=period, limit=1000)
    user_str = str(user_id)
    for entry in board:
        if entry["user_id"] == user_str:
            return entry
    return {"rank": 0, "user_id": user_str, "display_name": "", "level": 1, "xp": 0}


async def get_active_challenges(db: AsyncSession) -> list[dict]:
    """Get challenges for the current week."""
    monday = _current_monday()
    result = await db.execute(
        select(WeeklyChallenge).where(WeeklyChallenge.week_start == monday)
    )
    challenges = result.scalars().all()

    return [
        {
            "id": c.id,
            "title_ru": c.title_ru,
            "description_ru": c.description_ru,
            "challenge_type": c.challenge_type,
            "target_count": c.target_count,
            "xp_reward": c.xp_reward,
        }
        for c in challenges
    ]


async def get_challenge_progress(
    db: AsyncSession, user_id: uuid.UUID
) -> list[dict]:
    """Compute progress for each active challenge from user activity data."""
    challenges = await get_active_challenges(db)
    if not challenges:
        return []

    monday = _current_monday()

    # Get weekly activity counts
    from app.models.culture import UserDailyActivity
    from app.models.srs import SRSReview, SRSCard
    from app.models.content import ExerciseResult

    # Sum daily activity for the week
    activity_result = await db.execute(
        select(
            func.coalesce(func.sum(UserDailyActivity.xp_earned), 0),
            func.coalesce(func.sum(UserDailyActivity.exercises_done), 0),
            func.coalesce(func.sum(UserDailyActivity.reviews_done), 0),
            func.coalesce(func.sum(UserDailyActivity.time_minutes), 0),
        )
        .where(UserDailyActivity.user_id == user_id, UserDailyActivity.date >= monday)
    )
    row = activity_result.one()
    weekly_xp = row[0]
    weekly_exercises = row[1]
    weekly_reviews = row[2]
    weekly_minutes = row[3]

    # Count distinct days active this week
    active_days = await db.scalar(
        select(func.count(func.distinct(UserDailyActivity.date)))
        .where(UserDailyActivity.user_id == user_id, UserDailyActivity.date >= monday)
    ) or 0

    progress_map = {
        "earn_xp": weekly_xp,
        "complete_exercises": weekly_exercises,
        "review_cards": weekly_reviews,
        "study_minutes": weekly_minutes,
        "active_days": active_days,
    }

    result = []
    for c in challenges:
        current = progress_map.get(c["challenge_type"], 0)
        result.append({
            **c,
            "current": current,
            "completed": current >= c["target_count"],
        })

    return result
