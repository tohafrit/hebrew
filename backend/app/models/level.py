from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Level(Base):
    __tablename__ = "levels"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True)
    name_ru: Mapped[str] = mapped_column(String(50))
    name_he: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    order: Mapped[int] = mapped_column()
    cefr_equivalent: Mapped[str] = mapped_column(String(5))
