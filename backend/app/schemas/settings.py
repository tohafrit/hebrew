from pydantic import BaseModel, Field


class UserSettingsOut(BaseModel):
    daily_goal_minutes: int = 15
    daily_new_cards: int = 10
    srs_algorithm: str = "sm2"
    ui_theme: str = "light"
    notifications: bool = True

    model_config = {"from_attributes": True}


class UserSettingsUpdate(BaseModel):
    daily_goal_minutes: int | None = Field(None, ge=5, le=120)
    daily_new_cards: int | None = Field(None, ge=1, le=50)
    ui_theme: str | None = Field(None, pattern=r"^(light|dark|system)$")
    notifications: bool | None = None
