import uuid
from datetime import datetime, date, timezone

from sqlalchemy import ForeignKey, String, Date, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(50))
    unlocked_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    metadata_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class WeeklyChallenge(Base):
    __tablename__ = "weekly_challenges"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    week_start: Mapped[date] = mapped_column(Date, index=True)
    title_ru: Mapped[str] = mapped_column(String(200))
    description_ru: Mapped[str] = mapped_column(Text)
    challenge_type: Mapped[str] = mapped_column(String(50))  # earn_xp, complete_exercises, review_cards, study_minutes, active_days
    target_count: Mapped[int] = mapped_column()
    xp_reward: Mapped[int] = mapped_column(default=50)
