import uuid
from datetime import datetime, date

from pydantic import BaseModel


class AchievementDefOut(BaseModel):
    id: int
    code: str
    title_ru: str
    description_ru: str
    icon: str | None = None
    category: str
    condition_json: dict | None = None

    model_config = {"from_attributes": True}


class UserAchievementOut(BaseModel):
    id: uuid.UUID
    type: str  # = code
    unlocked_at: datetime
    definition: AchievementDefOut | None = None

    model_config = {"from_attributes": True}


class XPEvent(BaseModel):
    xp: int
    reason: str
    new_total: int


class DailyActivityOut(BaseModel):
    date: date
    xp_earned: int
    exercises_done: int
    reviews_done: int
    time_minutes: int

    model_config = {"from_attributes": True}


class StatsOverview(BaseModel):
    total_xp: int
    current_level: int
    level_name: str
    xp_to_next_level: int
    streak_days: int
    total_words: int
    total_cards: int
    total_reviews: int
    total_exercises: int
    total_texts_read: int
    total_dialogues: int
    daily_activity: list[DailyActivityOut]
    achievements_unlocked: int
    achievements_total: int
    skills: dict[str, float]  # skill_name -> 0..100


class CultureArticleBrief(BaseModel):
    id: int
    category: str
    title_ru: str
    title_he: str | None = None
    level_id: int | None = None

    model_config = {"from_attributes": True}


class CultureArticleDetail(CultureArticleBrief):
    content_md: str


class CultureWordOut(BaseModel):
    word_id: int
    hebrew: str
    translation_ru: str | None = None
    transliteration: str | None = None
    pos: str | None = None
    level_id: int | None = None


class RecommendationOut(BaseModel):
    type: str
    priority: int
    title: str
    description: str
    link: str
    icon: str


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: str
    display_name: str
    level: int
    xp: int


class LeaderboardResponse(BaseModel):
    entries: list[LeaderboardEntry]
    period: str


class ChallengeOut(BaseModel):
    id: int
    title_ru: str
    description_ru: str
    challenge_type: str
    target_count: int
    xp_reward: int


class ChallengeProgressOut(ChallengeOut):
    current: int
    completed: bool
