from pydantic import BaseModel


class AlphabetLetterOut(BaseModel):
    id: int
    letter: str
    name_ru: str
    translit: str
    sound_description: str | None = None
    numeric_value: int | None = None
    is_sofit: bool = False
    sofit_of: str | None = None
    order: int

    model_config = {"from_attributes": True}


class NikkudOut(BaseModel):
    id: int
    symbol: str
    name_he: str
    name_ru: str
    sound: str
    example_word: str | None = None
    example_translit: str | None = None

    model_config = {"from_attributes": True}


class AlphabetResponse(BaseModel):
    letters: list[AlphabetLetterOut]
    nikkud: list[NikkudOut]
