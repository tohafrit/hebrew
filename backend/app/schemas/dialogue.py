from pydantic import BaseModel


class DialogueLine(BaseModel):
    speaker: str
    speaker_name: str
    text_he: str
    text_ru: str
    is_user: bool = False
    options: list[str] | None = None
    correct_option: int | None = None


class DialogueBrief(BaseModel):
    id: int
    level_id: int
    title: str
    situation_ru: str | None = None

    model_config = {"from_attributes": True}


class DialogueDetail(DialogueBrief):
    lines_json: list[dict] | None = None
    vocabulary_json: list[dict] | None = None
    audio_url: str | None = None


class DialogueCheckRequest(BaseModel):
    dialogue_id: int
    line_index: int
    selected_option: int


class DialogueCheckResponse(BaseModel):
    correct: bool
    correct_option: int
    correct_text_he: str
