from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class GrammarTopic(Base):
    __tablename__ = "grammar_topics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title_ru: Mapped[str] = mapped_column(String(200))
    title_he: Mapped[str | None] = mapped_column(String(200), nullable=True)
    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))
    order: Mapped[int] = mapped_column(default=0)
    content_md: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    rules: Mapped[list["GrammarRule"]] = relationship(back_populates="topic")


class GrammarRule(Base):
    __tablename__ = "grammar_rules"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("grammar_topics.id", ondelete="CASCADE"), index=True)
    rule_text_ru: Mapped[str] = mapped_column(Text)
    examples_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    exceptions_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    topic: Mapped["GrammarTopic"] = relationship(back_populates="rules")


class Binyan(Base):
    __tablename__ = "binyanim"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_he: Mapped[str] = mapped_column(String(50))
    name_ru: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    pattern: Mapped[str | None] = mapped_column(String(50), nullable=True)
    example_root: Mapped[str | None] = mapped_column(String(20), nullable=True)
    level_id: Mapped[int | None] = mapped_column(ForeignKey("levels.id"), nullable=True)


class VerbConjugation(Base):
    __tablename__ = "verb_conjugations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word_id: Mapped[int] = mapped_column(ForeignKey("words.id", ondelete="CASCADE"), index=True)
    binyan_id: Mapped[int] = mapped_column(ForeignKey("binyanim.id"), index=True)
    tense: Mapped[str] = mapped_column(String(20))
    person: Mapped[str] = mapped_column(String(5))
    gender: Mapped[str | None] = mapped_column(String(10), nullable=True)
    number: Mapped[str] = mapped_column(String(10))
    form_he: Mapped[str] = mapped_column(String(100))
    form_nikkud: Mapped[str | None] = mapped_column(String(100), nullable=True)
    transliteration: Mapped[str | None] = mapped_column(String(200), nullable=True)


class GrammarRuleTag(Base):
    __tablename__ = "grammar_rule_tags"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rule_id: Mapped[int] = mapped_column(ForeignKey("grammar_topics.id", ondelete="CASCADE"), index=True)
    tag: Mapped[str] = mapped_column(String(50), index=True)


class Preposition(Base):
    __tablename__ = "prepositions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    base_form: Mapped[str] = mapped_column(String(30))
    meaning_ru: Mapped[str] = mapped_column(String(100))
    declension_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
