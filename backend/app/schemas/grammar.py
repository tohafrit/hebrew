from pydantic import BaseModel


class GrammarRuleOut(BaseModel):
    id: int
    rule_text_ru: str
    examples_json: dict | list | None = None
    exceptions_json: dict | list | None = None

    model_config = {"from_attributes": True}


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
