from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AlphabetLetter(Base):
    __tablename__ = "alphabet_letters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    letter: Mapped[str] = mapped_column(String(5))
    name_ru: Mapped[str] = mapped_column(String(50))
    translit: Mapped[str] = mapped_column(String(20))
    sound_description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    numeric_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_sofit: Mapped[bool] = mapped_column(Boolean, server_default="false")
    sofit_of: Mapped[str | None] = mapped_column(String(5), nullable=True)
    order: Mapped[int] = mapped_column(Integer)


class Nikkud(Base):
    __tablename__ = "nikkud"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(5))
    name_he: Mapped[str] = mapped_column(String(50))
    name_ru: Mapped[str] = mapped_column(String(50))
    sound: Mapped[str] = mapped_column(String(50))
    example_word: Mapped[str | None] = mapped_column(String(50), nullable=True)
    example_translit: Mapped[str | None] = mapped_column(String(50), nullable=True)
