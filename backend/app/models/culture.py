import uuid
from datetime import date

from sqlalchemy import ForeignKey, String, Text, Date, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AchievementDefinition(Base):
    __tablename__ = "achievement_definitions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), unique=True)
    title_ru: Mapped[str] = mapped_column(String(100))
    description_ru: Mapped[str] = mapped_column(String(300))
    icon: Mapped[str | None] = mapped_column(String(10), nullable=True)
    category: Mapped[str] = mapped_column(String(30))
    condition_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)


class CultureArticle(Base):
    __tablename__ = "culture_articles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(30))
    title_ru: Mapped[str] = mapped_column(String(200))
    title_he: Mapped[str | None] = mapped_column(String(200), nullable=True)
    content_md: Mapped[str] = mapped_column(Text)
    level_id: Mapped[int | None] = mapped_column(ForeignKey("levels.id"), nullable=True)


class UserDailyActivity(Base):
    __tablename__ = "user_daily_activity"
    __table_args__ = (UniqueConstraint("user_id", "date", name="uq_user_daily"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date)
    xp_earned: Mapped[int] = mapped_column(default=0)
    exercises_done: Mapped[int] = mapped_column(default=0)
    reviews_done: Mapped[int] = mapped_column(default=0)
    time_minutes: Mapped[int] = mapped_column(default=0)
