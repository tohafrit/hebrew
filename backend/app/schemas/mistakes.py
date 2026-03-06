from datetime import datetime

from pydantic import BaseModel


class ExerciseMistakeOut(BaseModel):
    exercise_id: int
    exercise_type: str
    prompt: dict | None = None
    user_answer: dict | None = None
    correct_answer: dict | None = None
    created_at: datetime


class SRSFailureOut(BaseModel):
    card_id: str
    card_type: str
    front: dict | None = None
    back: dict | None = None
    quality: int
    reviewed_at: datetime


class MistakesResponse(BaseModel):
    exercise_mistakes: list[ExerciseMistakeOut]
    srs_failures: list[SRSFailureOut]
