import uuid
from datetime import datetime, timezone


from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SRSCard(Base):
    __tablename__ = "srs_cards"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    card_type: Mapped[str] = mapped_column(String(30))
    content_id: Mapped[int] = mapped_column()
    front_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    back_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    reviews: Mapped[list["SRSReview"]] = relationship(back_populates="card")
    schedule: Mapped["SRSSchedule | None"] = relationship(back_populates="card", uselist=False)


class SRSReview(Base):
    __tablename__ = "srs_reviews"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    card_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("srs_cards.id", ondelete="CASCADE"), index=True)
    reviewed_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    quality: Mapped[int] = mapped_column()
    response_time_ms: Mapped[int | None] = mapped_column(nullable=True)

    card: Mapped["SRSCard"] = relationship(back_populates="reviews")


class SRSSchedule(Base):
    __tablename__ = "srs_schedule"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    card_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("srs_cards.id", ondelete="CASCADE"), unique=True)
    next_review: Mapped[datetime] = mapped_column(index=True)
    interval_days: Mapped[float] = mapped_column(default=1.0)
    ease_factor: Mapped[float] = mapped_column(default=2.5)
    repetitions: Mapped[int] = mapped_column(default=0)
    lapses: Mapped[int] = mapped_column(default=0)

    card: Mapped["SRSCard"] = relationship(back_populates="schedule")
