from pydantic import BaseModel


class MinimalPairOption(BaseModel):
    letter: str
    word: str
    translation: str


class MinimalPairQuestion(BaseModel):
    pair_id: str
    target_word: str
    target_translation: str
    correct_letter: str
    option1: MinimalPairOption
    option2: MinimalPairOption


class MinimalPairsDrillResponse(BaseModel):
    questions: list[MinimalPairQuestion]


class MinimalPairCheckRequest(BaseModel):
    pair_id: str
    answer_letter: str
    correct_letter: str


class MinimalPairCheckResponse(BaseModel):
    correct: bool
    xp_earned: int
