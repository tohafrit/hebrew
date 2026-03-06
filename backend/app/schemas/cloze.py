from pydantic import BaseModel


class ClozeExercise(BaseModel):
    sentence_he: str
    sentence_he_blanked: str
    sentence_ru: str
    hint: str
    answer: str
    transliteration: str | None = None


class ClozeExercisesResponse(BaseModel):
    exercises: list[ClozeExercise]
    text_id: int
