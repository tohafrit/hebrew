from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.gamification import (
    AchievementDefOut, UserAchievementOut,
    StatsOverview, DailyActivityOut,
    CultureArticleBrief, CultureArticleDetail,
    CultureWordOut,
    RecommendationOut,
    LeaderboardEntry, LeaderboardResponse,
    ChallengeOut, ChallengeProgressOut,
)
from app.schemas.mistakes import MistakesResponse, ExerciseMistakeOut, SRSFailureOut, ErrorPatternsResponse, ErrorPattern, ErrorPatternExample
from app.schemas.analytics import AnalyticsResponse
from app.services.gamification import (
    get_achievement_definitions, get_user_achievements,
    check_and_award_achievements, get_stats_overview,
    list_culture_articles, get_culture_article,
    LEVEL_THRESHOLDS,
)
from app.services.recommendations import get_recommendations
from app.services.text_analysis import ensure_caches, extract_hebrew_tokens
from app.services.gamification import award_xp as do_award_xp
from app.services.mistakes import get_exercise_mistakes, get_srs_failures
from app.services.analytics import get_analytics
from app.services.error_patterns import analyze_error_patterns
from app.services.leaderboard import get_leaderboard, get_user_rank, get_active_challenges, get_challenge_progress

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


# ── Error Patterns ────────────────────────────────────────────────────

@router.get("/stats/error-patterns", response_model=ErrorPatternsResponse)
async def get_error_patterns(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    data = await analyze_error_patterns(db, user.id, days=days)
    return ErrorPatternsResponse(
        patterns=[ErrorPattern(
            type=p["type"],
            name=p["name"],
            count=p["count"],
            pct=p["pct"],
            examples=[ErrorPatternExample(**e) for e in p["examples"]],
            tip=p["tip"],
        ) for p in data["patterns"]],
        total_mistakes=data["total_mistakes"],
        top_pattern=data["top_pattern"],
    )


# ── Analytics ─────────────────────────────────────────────────────────────

@router.get("/stats/analytics", response_model=AnalyticsResponse)
async def get_user_analytics(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    data = await get_analytics(db, user.id)
    return AnalyticsResponse(**data)


# ── Leaderboard ───────────────────────────────────────────────────────

@router.get("/leaderboard", response_model=LeaderboardResponse)
async def get_leaderboard_endpoint(
    period: str = Query("all_time"),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    entries = await get_leaderboard(db, period=period, limit=limit)
    return LeaderboardResponse(
        entries=[LeaderboardEntry(**e) for e in entries],
        period=period,
    )


@router.get("/leaderboard/rank", response_model=LeaderboardEntry)
async def get_my_rank(
    period: str = Query("all_time"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rank = await get_user_rank(db, user.id, period=period)
    return LeaderboardEntry(**rank)


# ── Challenges ────────────────────────────────────────────────────────

@router.get("/challenges", response_model=list[ChallengeOut])
async def get_challenges(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    challenges = await get_active_challenges(db)
    return [ChallengeOut(**c) for c in challenges]


@router.get("/challenges/progress", response_model=list[ChallengeProgressOut])
async def get_challenges_progress(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    progress = await get_challenge_progress(db, user.id)
    return [ChallengeProgressOut(**p) for p in progress]


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


@router.get("/culture/{article_id}/words", response_model=list[CultureWordOut])
async def get_culture_article_words(
    article_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Extract Hebrew words from a culture article and return dictionary matches."""
    article = await get_culture_article(db, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    word_cache, form_cache, conj_cache = await ensure_caches(db)

    # Extract Hebrew tokens from markdown content
    tokens = extract_hebrew_tokens(article.content_md)

    # Look up each token in caches, dedupe by word_id
    seen_ids: set[int] = set()
    words: list[CultureWordOut] = []

    for token in tokens:
        # Try exact match first
        entry = word_cache.get(token) or form_cache.get(token) or conj_cache.get(token)
        if entry and entry["word_id"] not in seen_ids:
            seen_ids.add(entry["word_id"])
            words.append(CultureWordOut(
                word_id=entry["word_id"],
                hebrew=entry["hebrew"],
                translation_ru=entry.get("translation_ru"),
                transliteration=entry.get("transliteration"),
                pos=entry.get("pos"),
                level_id=entry.get("level_id"),
            ))

    # Award 15 XP on first view (simple: always award, gamification handles streak)
    await do_award_xp(db, user, 15, "text_read")
    await db.commit()

    return words
