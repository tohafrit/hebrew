from pydantic import BaseModel


class AccuracyPoint(BaseModel):
    date: str
    accuracy: float
    total: int


class VocabGrowthPoint(BaseModel):
    date: str
    cumulative: int


class ExerciseBreakdown(BaseModel):
    type: str
    total: int
    correct: int
    accuracy: float


class WeakArea(BaseModel):
    type: str
    accuracy: float
    total: int


class AnalyticsResponse(BaseModel):
    accuracy_trend: list[AccuracyPoint]
    srs_retention_rate: float
    srs_total_reviews: int
    response_time_avg_ms: int | None
    vocab_growth: list[VocabGrowthPoint]
    exercise_breakdown: list[ExerciseBreakdown]
    weakest_areas: list[WeakArea]
