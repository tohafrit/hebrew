import uuid
from datetime import datetime

from pydantic import BaseModel


class PlacementQuestion(BaseModel):
    index: int
    level: int
    type: str  # multiple_choice, fill_blank, translate_ru_he
    prompt_he: str | None = None
    prompt_ru: str | None = None
    hint: str | None = None
    options: list[str] | None = None
    correct_answer: str


class PlacementTestResponse(BaseModel):
    questions: list[PlacementQuestion]


class PlacementAnswerIn(BaseModel):
    index: int
    answer: str


class PlacementSubmitRequest(BaseModel):
    answers: list[PlacementAnswerIn]


class PlacementResultOut(BaseModel):
    assigned_level: int
    total_questions: int
    total_correct: int
    per_level: dict[str, dict]  # {"1": {"correct": 3, "total": 4}, ...}
