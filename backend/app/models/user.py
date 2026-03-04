import uuid
from datetime import datetime, date, timezone

from sqlalchemy import ForeignKey, String, Text, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    display_name: Mapped[str] = mapped_column(String(100))
    native_lang: Mapped[str] = mapped_column(String(10), default="ru")
    current_level: Mapped[int] = mapped_column(default=1)
    xp: Mapped[int] = mapped_column(default=0)
    streak_days: Mapped[int] = mapped_column(default=0)
    last_activity_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    settings: Mapped["UserSettings | None"] = relationship(back_populates="user", uselist=False)
    sessions: Mapped[list["UserSession"]] = relationship(back_populates="user")


class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    daily_goal_minutes: Mapped[int] = mapped_column(default=15)
    daily_new_cards: Mapped[int] = mapped_column(default=10)
    srs_algorithm: Mapped[str] = mapped_column(String(20), default="sm2")
    ui_theme: Mapped[str] = mapped_column(String(10), default="light")
    notifications: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship(back_populates="settings")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    started_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(nullable=True)
    module: Mapped[str | None] = mapped_column(String(50), nullable=True)
    xp_earned: Mapped[int] = mapped_column(default=0)

    user: Mapped["User"] = relationship(back_populates="sessions")
