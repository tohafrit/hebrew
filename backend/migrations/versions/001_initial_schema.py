"""Initial schema with seed data

Revision ID: 001
Revises:
Create Date: 2026-03-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Users ---
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("display_name", sa.String(100), nullable=False),
        sa.Column("native_lang", sa.String(10), server_default="ru", nullable=False),
        sa.Column("current_level", sa.Integer(), server_default="1", nullable=False),
        sa.Column("xp", sa.Integer(), server_default="0", nullable=False),
        sa.Column("streak_days", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "user_settings",
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("daily_goal_minutes", sa.Integer(), server_default="15", nullable=False),
        sa.Column("daily_new_cards", sa.Integer(), server_default="10", nullable=False),
        sa.Column("srs_algorithm", sa.String(20), server_default="sm2", nullable=False),
        sa.Column("ui_theme", sa.String(10), server_default="light", nullable=False),
        sa.Column("notifications", sa.Boolean(), server_default="true", nullable=False),
    )
    op.create_table(
        "user_sessions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("started_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("module", sa.String(50), nullable=True),
        sa.Column("xp_earned", sa.Integer(), server_default="0", nullable=False),
    )

    # --- Levels ---
    op.create_table(
        "levels",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("code", sa.String(10), unique=True, nullable=False),
        sa.Column("name_ru", sa.String(50), nullable=False),
        sa.Column("name_he", sa.String(50), nullable=False),
        sa.Column("description", sa.String(500), nullable=True),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("cefr_equivalent", sa.String(5), nullable=False),
    )

    # --- Words ---
    op.create_table(
        "words",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("hebrew", sa.String(100), index=True, nullable=False),
        sa.Column("nikkud", sa.String(100), nullable=True),
        sa.Column("transliteration", sa.String(200), nullable=True),
        sa.Column("translation_ru", sa.String(500), nullable=False),
        sa.Column("pos", sa.String(50), nullable=True),
        sa.Column("gender", sa.String(20), nullable=True),
        sa.Column("number", sa.String(20), nullable=True),
        sa.Column("root", sa.String(20), nullable=True),
        sa.Column("frequency_rank", sa.Integer(), nullable=True),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id"), nullable=True),
        sa.Column("audio_url", sa.String(500), nullable=True),
        sa.Column("image_url", sa.String(500), nullable=True),
    )
    op.create_table(
        "word_forms",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("word_id", sa.Integer(), sa.ForeignKey("words.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("form_type", sa.String(50), nullable=False),
        sa.Column("hebrew", sa.String(100), nullable=False),
        sa.Column("nikkud", sa.String(100), nullable=True),
        sa.Column("transliteration", sa.String(200), nullable=True),
        sa.Column("description", sa.String(200), nullable=True),
    )
    op.create_table(
        "root_families",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("root", sa.String(20), unique=True, index=True, nullable=False),
        sa.Column("meaning_ru", sa.String(200), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
    )
    op.create_table(
        "root_family_members",
        sa.Column("root_family_id", sa.Integer(), sa.ForeignKey("root_families.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("word_id", sa.Integer(), sa.ForeignKey("words.id", ondelete="CASCADE"), primary_key=True),
    )
    op.create_table(
        "word_relations",
        sa.Column("word_id_1", sa.Integer(), sa.ForeignKey("words.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("word_id_2", sa.Integer(), sa.ForeignKey("words.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("relation_type", sa.String(30), primary_key=True),
    )
    op.create_table(
        "collocations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("word_id", sa.Integer(), sa.ForeignKey("words.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("phrase_he", sa.String(300), nullable=False),
        sa.Column("phrase_ru", sa.String(300), nullable=False),
        sa.Column("frequency", sa.Integer(), nullable=True),
    )
    op.create_table(
        "example_sentences",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("word_id", sa.Integer(), sa.ForeignKey("words.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("hebrew", sa.Text(), nullable=False),
        sa.Column("translation_ru", sa.Text(), nullable=False),
        sa.Column("transliteration", sa.Text(), nullable=True),
        sa.Column("audio_url", sa.String(500), nullable=True),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id"), nullable=True),
    )

    # --- Grammar ---
    op.create_table(
        "grammar_topics",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title_ru", sa.String(200), nullable=False),
        sa.Column("title_he", sa.String(200), nullable=True),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id"), nullable=False),
        sa.Column("order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("content_md", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
    )
    op.create_table(
        "grammar_rules",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("topic_id", sa.Integer(), sa.ForeignKey("grammar_topics.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("rule_text_ru", sa.Text(), nullable=False),
        sa.Column("examples_json", postgresql.JSONB(), nullable=True),
        sa.Column("exceptions_json", postgresql.JSONB(), nullable=True),
    )
    op.create_table(
        "binyanim",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name_he", sa.String(50), nullable=False),
        sa.Column("name_ru", sa.String(50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("pattern", sa.String(50), nullable=True),
        sa.Column("example_root", sa.String(20), nullable=True),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id"), nullable=True),
    )
    op.create_table(
        "verb_conjugations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("word_id", sa.Integer(), sa.ForeignKey("words.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("binyan_id", sa.Integer(), sa.ForeignKey("binyanim.id"), index=True, nullable=False),
        sa.Column("tense", sa.String(20), nullable=False),
        sa.Column("person", sa.String(5), nullable=False),
        sa.Column("gender", sa.String(10), nullable=True),
        sa.Column("number", sa.String(10), nullable=False),
        sa.Column("form_he", sa.String(100), nullable=False),
        sa.Column("form_nikkud", sa.String(100), nullable=True),
        sa.Column("transliteration", sa.String(200), nullable=True),
    )
    op.create_table(
        "prepositions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("base_form", sa.String(30), nullable=False),
        sa.Column("meaning_ru", sa.String(100), nullable=False),
        sa.Column("declension_json", postgresql.JSONB(), nullable=True),
    )

    # --- SRS ---
    op.create_table(
        "srs_cards",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("card_type", sa.String(30), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column("front_json", postgresql.JSONB(), nullable=True),
        sa.Column("back_json", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "srs_reviews",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("card_id", sa.Uuid(), sa.ForeignKey("srs_cards.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("reviewed_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("quality", sa.Integer(), nullable=False),
        sa.Column("response_time_ms", sa.Integer(), nullable=True),
    )
    op.create_table(
        "srs_schedule",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("card_id", sa.Uuid(), sa.ForeignKey("srs_cards.id", ondelete="CASCADE"), unique=True, nullable=False),
        sa.Column("next_review", sa.DateTime(), nullable=False),
        sa.Column("interval_days", sa.Float(), server_default="1.0", nullable=False),
        sa.Column("ease_factor", sa.Float(), server_default="2.5", nullable=False),
        sa.Column("repetitions", sa.Integer(), server_default="0", nullable=False),
        sa.Column("lapses", sa.Integer(), server_default="0", nullable=False),
    )

    # --- Content ---
    op.create_table(
        "lessons",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id"), nullable=False),
        sa.Column("unit", sa.Integer(), server_default="1", nullable=False),
        sa.Column("order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("title_ru", sa.String(200), nullable=False),
        sa.Column("title_he", sa.String(200), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("type", sa.String(30), nullable=False),
    )
    op.create_table(
        "exercises",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("lesson_id", sa.Integer(), sa.ForeignKey("lessons.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("type", sa.String(30), nullable=False),
        sa.Column("difficulty", sa.Integer(), server_default="1", nullable=False),
        sa.Column("prompt_json", postgresql.JSONB(), nullable=True),
        sa.Column("answer_json", postgresql.JSONB(), nullable=True),
        sa.Column("explanation_json", postgresql.JSONB(), nullable=True),
        sa.Column("points", sa.Integer(), server_default="10", nullable=False),
    )
    op.create_table(
        "exercise_results",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("exercise_id", sa.Integer(), sa.ForeignKey("exercises.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("answer_json", postgresql.JSONB(), nullable=True),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("time_ms", sa.Integer(), nullable=True),
        sa.Column("attempt", sa.Integer(), server_default="1", nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )
    op.create_table(
        "reading_texts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id"), nullable=False),
        sa.Column("title_he", sa.String(200), nullable=False),
        sa.Column("title_ru", sa.String(200), nullable=False),
        sa.Column("content_he", sa.Text(), nullable=False),
        sa.Column("content_ru", sa.Text(), nullable=False),
        sa.Column("vocabulary_json", postgresql.JSONB(), nullable=True),
        sa.Column("audio_url", sa.String(500), nullable=True),
        sa.Column("category", sa.String(30), server_default="story", nullable=False),
    )
    op.create_table(
        "dialogues",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("situation_ru", sa.Text(), nullable=True),
        sa.Column("lines_json", postgresql.JSONB(), nullable=True),
        sa.Column("vocabulary_json", postgresql.JSONB(), nullable=True),
        sa.Column("audio_url", sa.String(500), nullable=True),
    )

    # --- Topics & Skills ---
    op.create_table(
        "topics",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name_ru", sa.String(100), nullable=False),
        sa.Column("name_he", sa.String(100), nullable=True),
        sa.Column("icon", sa.String(50), nullable=True),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id"), nullable=True),
        sa.Column("order", sa.Integer(), server_default="0", nullable=False),
    )
    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(50), unique=True, nullable=False),
        sa.Column("description", sa.String(200), nullable=True),
        sa.Column("max_level", sa.Integer(), server_default="10", nullable=False),
    )
    op.create_table(
        "user_skill_progress",
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("skill_id", sa.Integer(), sa.ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("level", sa.Integer(), server_default="0", nullable=False),
        sa.Column("xp", sa.Integer(), server_default="0", nullable=False),
        sa.Column("last_practice", sa.DateTime(), nullable=True),
    )
    op.create_table(
        "user_topic_progress",
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("topic_id", sa.Integer(), sa.ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("words_learned", sa.Integer(), server_default="0", nullable=False),
        sa.Column("exercises_done", sa.Integer(), server_default="0", nullable=False),
        sa.Column("mastery_pct", sa.Float(), server_default="0.0", nullable=False),
    )

    # --- Gamification ---
    op.create_table(
        "achievements",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("unlocked_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("metadata_json", postgresql.JSONB(), nullable=True),
    )

    # === SEED DATA ===

    # Levels (6 ulpan levels)
    levels_table = sa.table(
        "levels",
        sa.column("id", sa.Integer),
        sa.column("code", sa.String),
        sa.column("name_ru", sa.String),
        sa.column("name_he", sa.String),
        sa.column("description", sa.String),
        sa.column("order", sa.Integer),
        sa.column("cefr_equivalent", sa.String),
    )
    op.bulk_insert(levels_table, [
        {"id": 1, "code": "alef", "name_ru": "Алеф", "name_he": "אלף", "description": "Начальный уровень: алфавит, базовые слова, простые фразы", "order": 1, "cefr_equivalent": "A1"},
        {"id": 2, "code": "bet", "name_ru": "Бет", "name_he": "בית", "description": "Элементарный: повседневные темы, простые предложения, настоящее время", "order": 2, "cefr_equivalent": "A2"},
        {"id": 3, "code": "gimel", "name_ru": "Гимель", "name_he": "גימל", "description": "Средний: все времена, биньяны, чтение адаптированных текстов", "order": 3, "cefr_equivalent": "B1"},
        {"id": 4, "code": "dalet", "name_ru": "Далет", "name_he": "דלת", "description": "Выше среднего: сложные тексты, деловой иврит, СМИ", "order": 4, "cefr_equivalent": "B2"},
        {"id": 5, "code": "he", "name_ru": "Хей", "name_he": "הא", "description": "Продвинутый: литературный иврит, академические тексты, идиомы", "order": 5, "cefr_equivalent": "C1"},
        {"id": 6, "code": "vav", "name_ru": "Вав", "name_he": "ואו", "description": "Свободное владение: носительский уровень, все стили речи", "order": 6, "cefr_equivalent": "C2"},
    ])

    # Binyanim (7 verb patterns)
    binyanim_table = sa.table(
        "binyanim",
        sa.column("id", sa.Integer),
        sa.column("name_he", sa.String),
        sa.column("name_ru", sa.String),
        sa.column("description", sa.Text),
        sa.column("pattern", sa.String),
        sa.column("example_root", sa.String),
        sa.column("level_id", sa.Integer),
    )
    op.bulk_insert(binyanim_table, [
        {"id": 1, "name_he": "פָּעַל", "name_ru": "Пааль", "description": "Основной активный биньян, простое действие", "pattern": "קָטַל", "example_root": "כ.ת.ב", "level_id": 1},
        {"id": 2, "name_he": "נִפְעַל", "name_ru": "Нифъаль", "description": "Пассив от Пааль или возвратное действие", "pattern": "נִקְטַל", "example_root": "כ.ת.ב", "level_id": 2},
        {"id": 3, "name_he": "פִּיעֵל", "name_ru": "Пиэль", "description": "Интенсивное действие, каузатив", "pattern": "קִטֵּל", "example_root": "ד.ב.ר", "level_id": 2},
        {"id": 4, "name_he": "פּוּעַל", "name_ru": "Пуаль", "description": "Пассив от Пиэль", "pattern": "קֻטַּל", "example_root": "ד.ב.ר", "level_id": 2},
        {"id": 5, "name_he": "הִפְעִיל", "name_ru": "Хифъиль", "description": "Каузатив, побуждение к действию", "pattern": "הִקְטִיל", "example_root": "ז.כ.ר", "level_id": 2},
        {"id": 6, "name_he": "הוּפְעַל", "name_ru": "Хуфъаль", "description": "Пассив от Хифъиль", "pattern": "הוּקְטַל", "example_root": "ז.כ.ר", "level_id": 3},
        {"id": 7, "name_he": "הִתְפַּעֵל", "name_ru": "Хитпаэль", "description": "Возвратное действие, взаимное действие", "pattern": "הִתְקַטֵּל", "example_root": "ל.ב.ש", "level_id": 2},
    ])

    # Skills (6 language skills)
    skills_table = sa.table(
        "skills",
        sa.column("id", sa.Integer),
        sa.column("name", sa.String),
        sa.column("description", sa.String),
        sa.column("max_level", sa.Integer),
    )
    op.bulk_insert(skills_table, [
        {"id": 1, "name": "reading", "description": "Чтение и понимание текстов", "max_level": 10},
        {"id": 2, "name": "writing", "description": "Письмо и составление текстов", "max_level": 10},
        {"id": 3, "name": "listening", "description": "Аудирование и понимание речи", "max_level": 10},
        {"id": 4, "name": "speaking", "description": "Говорение и произношение", "max_level": 10},
        {"id": 5, "name": "grammar", "description": "Грамматика и языковые структуры", "max_level": 10},
        {"id": 6, "name": "vocabulary", "description": "Словарный запас", "max_level": 10},
    ])


def downgrade() -> None:
    op.drop_table("achievements")
    op.drop_table("user_topic_progress")
    op.drop_table("user_skill_progress")
    op.drop_table("skills")
    op.drop_table("topics")
    op.drop_table("dialogues")
    op.drop_table("reading_texts")
    op.drop_table("exercise_results")
    op.drop_table("exercises")
    op.drop_table("lessons")
    op.drop_table("srs_schedule")
    op.drop_table("srs_reviews")
    op.drop_table("srs_cards")
    op.drop_table("prepositions")
    op.drop_table("verb_conjugations")
    op.drop_table("binyanim")
    op.drop_table("grammar_rules")
    op.drop_table("grammar_topics")
    op.drop_table("example_sentences")
    op.drop_table("collocations")
    op.drop_table("word_relations")
    op.drop_table("root_family_members")
    op.drop_table("root_families")
    op.drop_table("word_forms")
    op.drop_table("words")
    op.drop_table("levels")
    op.drop_table("user_sessions")
    op.drop_table("user_settings")
    op.drop_table("users")
