import json as _json

from pydantic import BaseModel, field_validator


class GrammarRuleOut(BaseModel):
    id: int
    rule_text_ru: str
    examples_json: dict | list | None = None
    exceptions_json: dict | list | None = None

    model_config = {"from_attributes": True}

    @field_validator("examples_json", "exceptions_json", mode="before")
    @classmethod
    def parse_json_string(cls, v):
        if isinstance(v, str):
            try:
                return _json.loads(v)
            except (ValueError, TypeError):
                return None
        return v


class GrammarTopicBrief(BaseModel):
    id: int
    title_ru: str
    title_he: str | None = None
    level_id: int
    order: int
    summary: str | None = None

    model_config = {"from_attributes": True}


class GrammarTopicDetail(GrammarTopicBrief):
    content_md: str | None = None
    rules: list[GrammarRuleOut] = []


class BinyanOut(BaseModel):
    id: int
    name_he: str
    name_ru: str
    description: str | None = None
    pattern: str | None = None
    example_root: str | None = None
    level_id: int | None = None

    model_config = {"from_attributes": True}


class PrepositionOut(BaseModel):
    id: int
    base_form: str
    meaning_ru: str
    declension_json: dict | None = None

    model_config = {"from_attributes": True}


class ConjugationOut(BaseModel):
    id: int
    word_id: int
    binyan_id: int
    tense: str
    person: str
    gender: str | None = None
    number: str
    form_he: str
    form_nikkud: str | None = None
    transliteration: str | None = None

    model_config = {"from_attributes": True}


# ── Conjugation Drill ────────────────────────────────────────────────────

class DrillQuestion(BaseModel):
    word_id: int
    word_hebrew: str
    word_nikkud: str | None = None
    translation_ru: str
    binyan_id: int
    binyan_name: str
    tense: str
    person: str
    gender: str | None = None
    number: str
    correct_answer: str
    correct_nikkud: str | None = None
    transliteration: str | None = None
    options: list[str] | None = None


class DrillCheckRequest(BaseModel):
    word_id: int
    binyan_id: int
    tense: str
    person: str
    answer: str


class DrillCheckResponse(BaseModel):
    correct: bool
    correct_answer: str
    correct_nikkud: str | None = None
    transliteration: str | None = None
