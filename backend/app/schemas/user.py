import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    display_name: str
    native_lang: str
    current_level: int
    xp: int
    streak_days: int
    created_at: datetime

    model_config = {"from_attributes": True}
