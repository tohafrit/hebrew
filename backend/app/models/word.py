import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hebrew: Mapped[str] = mapped_column(String(100), index=True)
    nikkud: Mapped[str | None] = mapped_column(String(100), nullable=True)
    transliteration: Mapped[str | None] = mapped_column(String(200), nullable=True)
    translation_ru: Mapped[str] = mapped_column(String(500))
    pos: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gender: Mapped[str | None] = mapped_column(String(20), nullable=True)
    number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    root: Mapped[str | None] = mapped_column(String(20), nullable=True)
    frequency_rank: Mapped[int | None] = mapped_column(nullable=True)
    level_id: Mapped[int | None] = mapped_column(ForeignKey("levels.id"), nullable=True)
    audio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    forms: Mapped[list["WordForm"]] = relationship(back_populates="word")
    examples: Mapped[list["ExampleSentence"]] = relationship(back_populates="word")


class WordForm(Base):
    __tablename__ = "word_forms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"), index=True)
    form_type: Mapped[str] = mapped_column(String(50))
    hebrew: Mapped[str] = mapped_column(String(100))
    nikkud: Mapped[str | None] = mapped_column(String(100), nullable=True)
    transliteration: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)

    word: Mapped["Word"] = relationship(back_populates="forms")


class RootFamily(Base):
    __tablename__ = "root_families"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    root: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    meaning_ru: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    members: Mapped[list["RootFamilyMember"]] = relationship(back_populates="family")


class RootFamilyMember(Base):
    __tablename__ = "root_family_members"

    root_family_id: Mapped[int] = mapped_column(ForeignKey("root_families.id", ondelete="CASCADE"), primary_key=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"), primary_key=True)

    family: Mapped["RootFamily"] = relationship(back_populates="members")


class WordRelation(Base):
    __tablename__ = "word_relations"

    word_id_1: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"), primary_key=True)
    word_id_2: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"), primary_key=True)
    relation_type: Mapped[str] = mapped_column(String(30), primary_key=True)


class Collocation(Base):
    __tablename__ = "collocations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"), index=True)
    phrase_he: Mapped[str] = mapped_column(String(300))
    phrase_ru: Mapped[str] = mapped_column(String(300))
    frequency: Mapped[int | None] = mapped_column(nullable=True)


# Forward reference import
from app.models.sentence import ExampleSentence  # noqa: E402
