import uuid
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))
    unit: Mapped[int] = mapped_column(default=1)
    order: Mapped[int] = mapped_column(default=0)
    title_ru: Mapped[str] = mapped_column(String(200))
    title_he: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    content_md: Mapped[str | None] = mapped_column(Text, nullable=True)
    type: Mapped[str] = mapped_column(String(30))


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), index=True)
    type: Mapped[str] = mapped_column(String(30))
    difficulty: Mapped[int] = mapped_column(default=1)
    prompt_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    answer_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    explanation_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    points: Mapped[int] = mapped_column(default=10)


class ExerciseResult(Base):
    __tablename__ = "exercise_results"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id", ondelete="CASCADE"), index=True)
    answer_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    is_correct: Mapped[bool] = mapped_column()
    time_ms: Mapped[int | None] = mapped_column(nullable=True)
    attempt: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class ReadingText(Base):
    __tablename__ = "reading_texts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))
    title_he: Mapped[str] = mapped_column(String(200))
    title_ru: Mapped[str] = mapped_column(String(200))
    content_he: Mapped[str] = mapped_column(Text)
    content_ru: Mapped[str] = mapped_column(Text)
    vocabulary_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    audio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    category: Mapped[str] = mapped_column(String(30), default="story")


class Dialogue(Base):
    __tablename__ = "dialogues"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))
    title: Mapped[str] = mapped_column(String(200))
    situation_ru: Mapped[str | None] = mapped_column(Text, nullable=True)
    lines_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    vocabulary_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    audio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
