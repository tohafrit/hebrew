from pydantic import BaseModel


class LessonBrief(BaseModel):
    id: int
    level_id: int
    unit: int
    order: int
    title_ru: str
    title_he: str | None = None
    description: str | None = None
    content_md: str | None = None
    type: str
    completed: bool = False

    model_config = {"from_attributes": True}


class LessonDetail(LessonBrief):
    exercises: list["ExerciseOut"] = []


class ExerciseOut(BaseModel):
    id: int
    lesson_id: int
    type: str
    difficulty: int
    prompt_json: dict | None = None
    answer_json: dict | None = None
    explanation_json: dict | None = None
    points: int = 10

    model_config = {"from_attributes": True}


class ExerciseCheckRequest(BaseModel):
    exercise_id: int
    answer: str | dict | list


class ExerciseCheckResponse(BaseModel):
    correct: bool
    correct_answer: str | dict | list | None = None
    explanation: str | None = None
    points_earned: int = 0
    xp_earned: int = 0
    total_xp: int = 0
    new_achievements: list[str] = []


class LessonStatsOut(BaseModel):
    total: int
    correct: int
    accuracy_pct: int
    time_ms: int


class ReadingTextBrief(BaseModel):
    id: int
    level_id: int
    title_he: str
    title_ru: str
    category: str

    model_config = {"from_attributes": True}


class ReadingTextDetail(ReadingTextBrief):
    content_he: str
    content_ru: str
    vocabulary_json: dict | list | None = None
    audio_url: str | None = None
