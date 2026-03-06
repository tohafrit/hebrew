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


class ErrorPatternExample(BaseModel):
    user_answer: str
    correct_answer: str
    exercise_type: str


class ErrorPattern(BaseModel):
    type: str
    name: str
    count: int
    pct: int
    examples: list[ErrorPatternExample]
    tip: str


class ErrorPatternsResponse(BaseModel):
    patterns: list[ErrorPattern]
    total_mistakes: int
    top_pattern: str | None = None
