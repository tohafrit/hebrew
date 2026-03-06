from pydantic import BaseModel


class WordBrief(BaseModel):
    id: int
    hebrew: str
    nikkud: str | None = None
    transliteration: str | None = None
    translation_ru: str
    pos: str | None = None
    root: str | None = None
    frequency_rank: int | None = None
    level_id: int | None = None

    model_config = {"from_attributes": True}


class WordDetail(WordBrief):
    gender: str | None = None
    number: str | None = None
    audio_url: str | None = None
    image_url: str | None = None
    forms: list["WordFormOut"] = []
    examples: list["ExampleSentenceOut"] = []
    root_family: list["RootFamilyWordOut"] | None = None


class WordFormOut(BaseModel):
    id: int
    form_type: str
    hebrew: str
    nikkud: str | None = None
    transliteration: str | None = None
    description: str | None = None

    model_config = {"from_attributes": True}


class ExampleSentenceOut(BaseModel):
    id: int
    hebrew: str
    translation_ru: str
    transliteration: str | None = None

    model_config = {"from_attributes": True}


class RootFamilyOut(BaseModel):
    id: int
    root: str
    meaning_ru: str | None = None
    words: list["RootFamilyWordOut"] = []

    model_config = {"from_attributes": True}


class RootFamilyWordOut(BaseModel):
    id: int
    hebrew: str
    transliteration: str | None = None
    translation_ru: str
    pos: str | None = None

    model_config = {"from_attributes": True}


class WordListResponse(BaseModel):
    items: list[WordBrief]
    total: int
    page: int
    per_page: int


class RootExplorerWord(BaseModel):
    id: int
    hebrew: str
    nikkud: str | None = None
    transliteration: str | None = None
    translation_ru: str
    pos: str | None = None
    level_id: int | None = None
    frequency_rank: int | None = None

    model_config = {"from_attributes": True}


class RootExplorerResponse(BaseModel):
    root: str
    meaning_ru: str | None = None
    words_by_pos: dict[str, list[RootExplorerWord]]
    total_words: int


class DictionaryStats(BaseModel):
    total_words: int
    by_pos: dict[str, int]
    by_frequency: dict[str, int]
    root_families: int
