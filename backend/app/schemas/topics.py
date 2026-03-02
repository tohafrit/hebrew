from pydantic import BaseModel


class TopicOut(BaseModel):
    id: int
    name_ru: str
    name_he: str | None = None
    icon: str | None = None
    level_id: int | None = None
    order: int = 0

    model_config = {"from_attributes": True}


class TopicWithProgress(TopicOut):
    words_learned: int = 0
    exercises_done: int = 0
    mastery_pct: float = 0.0
