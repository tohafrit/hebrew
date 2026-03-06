import uuid
from datetime import datetime

from pydantic import BaseModel


class CardOut(BaseModel):
    id: uuid.UUID
    card_type: str
    content_id: int
    front_json: dict | None = None
    back_json: dict | None = None

    model_config = {"from_attributes": True}


class CardWithSchedule(CardOut):
    next_review: datetime | None = None
    interval_days: float = 1.0
    ease_factor: float = 2.5
    repetitions: int = 0
    lapses: int = 0


class ReviewRequest(BaseModel):
    card_id: uuid.UUID
    quality: int  # 0-3
    response_time_ms: int | None = None


class ReviewResponse(BaseModel):
    card_id: uuid.UUID
    next_review: datetime
    interval_days: float
    ease_factor: float
    repetitions: int


class SessionResponse(BaseModel):
    cards: list[CardWithSchedule]
    total_due: int
    new_cards: int


class CreateCardsRequest(BaseModel):
    word_ids: list[int]
    card_types: list[str] = ["word_he_ru", "word_ru_he"]


class CreateCardsResponse(BaseModel):
    created: int


class SRSStats(BaseModel):
    total_cards: int
    due_today: int
    new_cards: int
    reviews_today: int
    streak_days: int
    average_ease: float | None = None


class GrammarCardsRequest(BaseModel):
    word_ids: list[int]
    tenses: list[str] = ["present", "past"]


class SentenceCardsRequest(BaseModel):
    text_id: int
    max_cards: int = 10


class LeechCard(BaseModel):
    id: uuid.UUID
    card_type: str
    content_id: int
    front_json: dict | None = None
    back_json: dict | None = None
    lapses: int
    ease_factor: float

    model_config = {"from_attributes": True}


class LeechResponse(BaseModel):
    cards: list[LeechCard]
    count: int
