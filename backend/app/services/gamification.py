import uuid
from datetime import datetime, date, timedelta

from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.gamification import Achievement
from app.models.culture import AchievementDefinition, CultureArticle, UserDailyActivity
from app.models.srs import SRSCard, SRSReview
from app.models.content import ExerciseResult


# ── XP awards ──────────────────────────────────────────────────────────────

XP_AMOUNTS = {
    "exercise_correct": 10,
    "exercise_wrong": 2,
    "review_card": 5,
    "text_read": 15,
    "dialogue_done": 20,
    "daily_login": 5,
}

# Level thresholds (cumulative XP needed)
LEVEL_THRESHOLDS = [
    (1, 0, "Олэ Хадаш"),
    (2, 100, "Алеф"),
    (3, 300, "Бет"),
    (4, 600, "Гимель"),
    (5, 1000, "Далет"),
    (6, 1500, "Хей"),
    (7, 2200, "Вав"),
    (8, 3000, "Заин"),
    (9, 4000, "Хет"),
    (10, 5500, "Тет"),
    (11, 7500, "Йуд"),
    (12, 10000, "Сабра"),
]


def get_level_for_xp(xp: int) -> tuple[int, str, int]:
    """Returns (level, name, xp_to_next_level)."""
    current = LEVEL_THRESHOLDS[0]
    for threshold in LEVEL_THRESHOLDS:
        if xp >= threshold[1]:
            current = threshold
        else:
            return current[0], current[2], threshold[1] - xp
    return current[0], current[2], 0


async def award_xp(db: AsyncSession, user: User, amount: int, reason: str) -> int:
    """Award XP to user. Returns new total."""
    user.xp += amount
    new_level, _, _ = get_level_for_xp(user.xp)
    if new_level > user.current_level:
        user.current_level = new_level

    # Update daily activity
    today = date.today()
    result = await db.execute(
        select(UserDailyActivity).where(
            UserDailyActivity.user_id == user.id,
            UserDailyActivity.date == today,
        )
    )
    daily = result.scalar_one_or_none()
    if daily:
        daily.xp_earned += amount
        if "exercise" in reason:
            daily.exercises_done += 1
        if "review" in reason:
            daily.reviews_done += 1
    else:
        daily = UserDailyActivity(
            user_id=user.id,
            date=today,
            xp_earned=amount,
            exercises_done=1 if "exercise" in reason else 0,
            reviews_done=1 if "review" in reason else 0,
        )
        db.add(daily)

    await db.commit()
    return user.xp


# ── Achievements ───────────────────────────────────────────────────────────

async def get_achievement_definitions(db: AsyncSession) -> list[AchievementDefinition]:
    result = await db.execute(
        select(AchievementDefinition).order_by(AchievementDefinition.id)
    )
    return list(result.scalars().all())


async def get_user_achievements(db: AsyncSession, user_id: uuid.UUID) -> list[Achievement]:
    result = await db.execute(
        select(Achievement).where(Achievement.user_id == user_id).order_by(Achievement.unlocked_at.desc())
    )
    return list(result.scalars().all())


async def check_and_award_achievements(db: AsyncSession, user: User) -> list[str]:
    """Check all achievement conditions and award any new ones. Returns list of newly unlocked codes."""
    # Get all definitions and existing achievements
    defs = await get_achievement_definitions(db)
    existing = await get_user_achievements(db, user.id)
    existing_codes = {a.type for a in existing}

    # Gather stats
    stats = await _gather_user_stats(db, user.id, user)

    newly_unlocked = []
    for defn in defs:
        if defn.code in existing_codes:
            continue
        condition = defn.condition_json or {}
        ctype = condition.get("type", "")
        count = condition.get("count", 0)

        unlocked = False
        if ctype == "xp" and stats["xp"] >= count:
            unlocked = True
        elif ctype == "level" and stats["level"] >= count:
            unlocked = True
        elif ctype == "streak" and stats["streak"] >= count:
            unlocked = True
        elif ctype == "words_learned" and stats["words_learned"] >= count:
            unlocked = True
        elif ctype == "cards_created" and stats["cards_created"] >= count:
            unlocked = True
        elif ctype == "reviews" and stats["reviews"] >= count:
            unlocked = True
        elif ctype == "exercises_done" and stats["exercises_done"] >= count:
            unlocked = True
        elif ctype == "texts_read" and stats.get("texts_read", 0) >= count:
            unlocked = True
        elif ctype == "dialogues_done" and stats.get("dialogues_done", 0) >= count:
            unlocked = True
        elif ctype == "login" and count <= 1:
            unlocked = True

        if unlocked:
            achievement = Achievement(
                user_id=user.id,
                type=defn.code,
                unlocked_at=datetime.utcnow(),
            )
            db.add(achievement)
            newly_unlocked.append(defn.code)

    if newly_unlocked:
        await db.commit()

    return newly_unlocked


async def _gather_user_stats(db: AsyncSession, user_id: uuid.UUID, user: User) -> dict:
    """Gather user statistics for achievement checking."""
    # Cards created
    cards_result = await db.execute(
        select(func.count()).select_from(SRSCard).where(SRSCard.user_id == user_id)
    )
    cards_count = cards_result.scalar() or 0

    # Total reviews (SRSReview links through SRSCard)
    reviews_result = await db.execute(
        select(func.count()).select_from(SRSReview)
        .join(SRSCard, SRSReview.card_id == SRSCard.id)
        .where(SRSCard.user_id == user_id)
    )
    reviews_count = reviews_result.scalar() or 0

    # Exercises done
    exercises_result = await db.execute(
        select(func.count()).select_from(ExerciseResult).where(ExerciseResult.user_id == user_id)
    )
    exercises_count = exercises_result.scalar() or 0

    return {
        "xp": user.xp,
        "level": user.current_level,
        "streak": user.streak_days,
        "words_learned": cards_count,  # approximation
        "cards_created": cards_count,
        "reviews": reviews_count,
        "exercises_done": exercises_count,
        "texts_read": 0,  # would need tracking table
        "dialogues_done": 0,  # would need tracking table
    }


# ── Stats / Analytics ──────────────────────────────────────────────────────

async def get_stats_overview(db: AsyncSession, user: User) -> dict:
    """Get comprehensive stats for dashboard."""
    user_id = user.id

    # Cards
    cards_result = await db.execute(
        select(func.count()).select_from(SRSCard).where(SRSCard.user_id == user_id)
    )
    total_cards = cards_result.scalar() or 0

    # Reviews (SRSReview links through SRSCard)
    reviews_result = await db.execute(
        select(func.count()).select_from(SRSReview)
        .join(SRSCard, SRSReview.card_id == SRSCard.id)
        .where(SRSCard.user_id == user_id)
    )
    total_reviews = reviews_result.scalar() or 0

    # Exercises
    exercises_result = await db.execute(
        select(func.count()).select_from(ExerciseResult).where(ExerciseResult.user_id == user_id)
    )
    total_exercises = exercises_result.scalar() or 0

    # Correct exercises
    correct_result = await db.execute(
        select(func.count()).select_from(ExerciseResult).where(
            ExerciseResult.user_id == user_id,
            ExerciseResult.is_correct == True,
        )
    )
    correct_exercises = correct_result.scalar() or 0

    # Daily activity (last 90 days)
    ninety_ago = date.today() - timedelta(days=90)
    activity_result = await db.execute(
        select(UserDailyActivity)
        .where(
            UserDailyActivity.user_id == user_id,
            UserDailyActivity.date >= ninety_ago,
        )
        .order_by(UserDailyActivity.date)
    )
    daily_activity = list(activity_result.scalars().all())

    # Achievements
    achievements = await get_user_achievements(db, user_id)
    defs = await get_achievement_definitions(db)

    # Level info
    level, level_name, xp_to_next = get_level_for_xp(user.xp)

    # Skills radar (approximate)
    reading_score = min(100, total_cards * 2)
    writing_score = min(100, total_exercises * 3)
    listening_score = min(100, total_exercises * 2)
    grammar_score = min(100, correct_exercises * 4)
    vocabulary_score = min(100, total_cards * 1.5)
    speaking_score = min(100, total_reviews)

    return {
        "total_xp": user.xp,
        "current_level": level,
        "level_name": level_name,
        "xp_to_next_level": xp_to_next,
        "streak_days": user.streak_days,
        "total_words": total_cards,
        "total_cards": total_cards,
        "total_reviews": total_reviews,
        "total_exercises": total_exercises,
        "total_texts_read": 0,
        "total_dialogues": 0,
        "daily_activity": daily_activity,
        "achievements_unlocked": len(achievements),
        "achievements_total": len(defs),
        "skills": {
            "reading": reading_score,
            "writing": writing_score,
            "listening": listening_score,
            "grammar": grammar_score,
            "vocabulary": vocabulary_score,
            "speaking": speaking_score,
        },
    }


# ── Culture ────────────────────────────────────────────────────────────────

async def list_culture_articles(
    db: AsyncSession, category: str | None = None
) -> list[CultureArticle]:
    q = select(CultureArticle).order_by(CultureArticle.category, CultureArticle.id)
    if category:
        q = q.where(CultureArticle.category == category)
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_culture_article(db: AsyncSession, article_id: int) -> CultureArticle | None:
    result = await db.execute(
        select(CultureArticle).where(CultureArticle.id == article_id)
    )
    return result.scalar_one_or_none()
