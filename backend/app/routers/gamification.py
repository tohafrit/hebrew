from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.gamification import (
    AchievementDefOut, UserAchievementOut,
    StatsOverview, DailyActivityOut,
    CultureArticleBrief, CultureArticleDetail,
    RecommendationOut,
)
from app.schemas.mistakes import MistakesResponse, ExerciseMistakeOut, SRSFailureOut
from app.schemas.analytics import AnalyticsResponse
from app.services.gamification import (
    get_achievement_definitions, get_user_achievements,
    check_and_award_achievements, get_stats_overview,
    list_culture_articles, get_culture_article,
    LEVEL_THRESHOLDS,
)
from app.services.recommendations import get_recommendations
from app.services.mistakes import get_exercise_mistakes, get_srs_failures
from app.services.analytics import get_analytics

router = APIRouter(tags=["gamification"])


# ── Achievements ───────────────────────────────────────────────────────────

@router.get("/achievements/definitions", response_model=list[AchievementDefOut])
async def get_all_achievement_defs(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    defs = await get_achievement_definitions(db)
    return [AchievementDefOut.model_validate(d) for d in defs]


@router.get("/achievements/mine", response_model=list[UserAchievementOut])
async def get_my_achievements(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    achievements = await get_user_achievements(db, user.id)
    return [UserAchievementOut.model_validate(a) for a in achievements]


@router.post("/achievements/check", response_model=list[str])
async def check_achievements(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Check and award any new achievements. Returns list of newly unlocked codes."""
    newly_unlocked = await check_and_award_achievements(db, user)
    if newly_unlocked:
        await db.commit()
    return newly_unlocked


# ── Stats / Dashboard ─────────────────────────────────────────────────────

@router.get("/stats/overview", response_model=StatsOverview)
async def get_overview(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    data = await get_stats_overview(db, user)
    data["daily_activity"] = [
        DailyActivityOut.model_validate(a) for a in data["daily_activity"]
    ]
    return StatsOverview(**data)


@router.get("/stats/levels")
async def get_levels():
    """Return level thresholds."""
    return [
        {"level": lvl, "xp_required": xp, "name": name}
        for lvl, xp, name in LEVEL_THRESHOLDS
    ]


# ── Recommendations ───────────────────────────────────────────────────────

@router.get("/recommendations", response_model=list[RecommendationOut])
async def get_study_recommendations(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Get smart study recommendations for the user."""
    recs = await get_recommendations(db, user)
    return [RecommendationOut(**r) for r in recs]


# ── Mistakes ──────────────────────────────────────────────────────────────

@router.get("/stats/mistakes", response_model=MistakesResponse)
async def get_mistakes(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    exercise_mistakes = await get_exercise_mistakes(db, user.id, days=days, limit=limit)
    srs_failures = await get_srs_failures(db, user.id, days=days, limit=limit)
    return MistakesResponse(
        exercise_mistakes=[ExerciseMistakeOut(**m) for m in exercise_mistakes],
        srs_failures=[SRSFailureOut(**f) for f in srs_failures],
    )


# ── Analytics ─────────────────────────────────────────────────────────────

@router.get("/stats/analytics", response_model=AnalyticsResponse)
async def get_user_analytics(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    data = await get_analytics(db, user.id)
    return AnalyticsResponse(**data)


# ── Culture ────────────────────────────────────────────────────────────────

@router.get("/culture", response_model=list[CultureArticleBrief])
async def get_culture_articles(
    category: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    articles = await list_culture_articles(db, category=category)
    return [CultureArticleBrief.model_validate(a) for a in articles]


@router.get("/culture/{article_id}", response_model=CultureArticleDetail)
async def get_culture_article_detail(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    article = await get_culture_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return CultureArticleDetail.model_validate(article)
