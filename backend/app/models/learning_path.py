import uuid
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))
    unit: Mapped[int] = mapped_column()
    step: Mapped[int] = mapped_column()
    step_type: Mapped[str] = mapped_column(String(30))
    content_id: Mapped[int | None] = mapped_column(nullable=True)
    title_ru: Mapped[str] = mapped_column(String(200))
    title_he: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description_ru: Mapped[str | None] = mapped_column(String(500), nullable=True)
    icon: Mapped[str | None] = mapped_column(String(10), nullable=True)


class UserPathProgress(Base):
    __tablename__ = "user_path_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "path_step_id", name="uq_user_path_progress"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    path_step_id: Mapped[int] = mapped_column(ForeignKey("learning_paths.id", ondelete="CASCADE"))
    completed_at: Mapped[datetime] = mapped_column(DateTime)
