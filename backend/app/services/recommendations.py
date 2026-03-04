"""Smart study recommendations engine."""

import uuid
from datetime import datetime, date, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.srs import SRSCard, SRSSchedule
from app.models.content import Lesson, ExerciseResult
from app.models.user import User, UserSettings
from app.models.culture import UserDailyActivity


async def get_recommendations(
    db: AsyncSession, user: User
) -> list[dict]:
    """Return top-5 study recommendations sorted by priority.

    Considers:
    1. Due SRS cards (highest priority if many are overdue)
    2. Streak maintenance (if user hasn't studied today)
    3. Daily goal progress
    4. Weakest skill / least practiced area
    5. Unseen lessons
    """
    user_id = user.id
    now = datetime.utcnow()
    today = date.today()
    recommendations: list[dict] = []

    # 1. Due SRS cards
    due_count = await db.scalar(
        select(func.count())
        .select_from(SRSCard)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(SRSCard.user_id == user_id, SRSSchedule.next_review <= now)
    ) or 0

    if due_count > 0:
        recommendations.append({
            "type": "srs_review",
            "priority": min(100, 50 + due_count),
            "title": "Повторить карточки",
            "description": f"{due_count} карточек ждут повторения",
            "link": "/srs",
            "icon": "🔄",
        })

    # 2. Today's activity check (streak maintenance)
    daily = await db.scalar(
        select(UserDailyActivity).where(
            UserDailyActivity.user_id == user_id,
            UserDailyActivity.date == today,
        )
    )
    today_xp = daily.xp_earned if daily else 0

    if today_xp == 0:
        recommendations.append({
            "type": "streak",
            "priority": 90,
            "title": "Сохранить серию",
            "description": f"Ваша серия: {user.streak_days} дней. Позанимайтесь сегодня!",
            "link": "/lessons",
            "icon": "🔥",
        })

    # 3. Daily goal progress
    settings = await db.scalar(
        select(UserSettings).where(UserSettings.user_id == user_id)
    )
    goal_minutes = settings.daily_goal_minutes if settings else 15
    today_minutes = daily.time_minutes if daily else 0

    if today_minutes < goal_minutes:
        remaining = goal_minutes - today_minutes
        pct = round(today_minutes / goal_minutes * 100) if goal_minutes > 0 else 0
        recommendations.append({
            "type": "daily_goal",
            "priority": 70,
            "title": "Дневная цель",
            "description": f"Прогресс: {pct}% — осталось {remaining} мин.",
            "link": "/lessons",
            "icon": "🎯",
        })

    # 4. Weakest area — exercises vs reviews balance
    total_exercises = await db.scalar(
        select(func.count())
        .select_from(ExerciseResult)
        .where(ExerciseResult.user_id == user_id)
    ) or 0

    total_cards = await db.scalar(
        select(func.count())
        .select_from(SRSCard)
        .where(SRSCard.user_id == user_id)
    ) or 0

    if total_cards < 10:
        recommendations.append({
            "type": "vocabulary",
            "priority": 60,
            "title": "Пополнить словарь",
            "description": "Добавьте слова из словаря в карточки",
            "link": "/dictionary",
            "icon": "📖",
        })
    elif total_exercises < total_cards:
        recommendations.append({
            "type": "practice",
            "priority": 55,
            "title": "Выполнить упражнения",
            "description": "Практика закрепляет знания",
            "link": "/lessons",
            "icon": "✏️",
        })

    # 5. Unseen lessons
    completed_lessons = await db.execute(
        select(ExerciseResult.exercise_id)
        .where(ExerciseResult.user_id == user_id)
        .distinct()
    )
    completed_ids = {r[0] for r in completed_lessons.all()}

    total_lessons = await db.scalar(
        select(func.count()).select_from(Lesson)
    ) or 0

    if total_lessons > 0 and len(completed_ids) < total_lessons * 3:
        recommendations.append({
            "type": "new_lesson",
            "priority": 45,
            "title": "Новый урок",
            "description": "Откройте новый урок для изучения",
            "link": "/lessons",
            "icon": "📚",
        })

    # Sort by priority descending, return top 5
    recommendations.sort(key=lambda r: r["priority"], reverse=True)
    return recommendations[:5]
