"""seed_content_data

Revision ID: 002
Revises: 001
Create Date: 2026-03-05 07:45:00.000000

"""
import os
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Tables in FK-dependency order (parents before children)
SEED_TABLES = [
    'levels',
    'skills',
    'alphabet_letters',
    'nikkud',
    'prepositions',
    'root_families',
    'achievement_definitions',
    # tables that depend on levels
    'binyanim',
    'topics',
    'grammar_topics',
    'lessons',
    'reading_texts',
    'dialogues',
    'culture_articles',
    'words',
    # tables that depend on words/topics/lessons/etc
    'word_forms',
    'collocations',
    'example_sentences',
    'grammar_rules',
    'verb_conjugations',
    'root_family_members',
    'exercises',
]


def upgrade() -> None:
    seed_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'seed')
    seed_dir = os.path.abspath(seed_dir)

    conn = op.get_bind()

    for table in SEED_TABLES:
        sql_file = os.path.join(seed_dir, f'{table}.sql')
        if not os.path.exists(sql_file):
            raise FileNotFoundError(f'Seed file not found: {sql_file}')

        with open(sql_file, 'r', encoding='utf-8') as f:
            sql = f.read().strip()

        if not sql:
            continue

        # Execute entire file as a single batch via raw DBAPI cursor
        cursor = conn.connection.dbapi_connection.cursor()
        cursor.execute(sql)
        cursor.close()

    # Create default admin user
    conn.execute(sa.text("""
        INSERT INTO users (id, email, password_hash, display_name, native_lang, current_level, xp, streak_days, created_at)
        VALUES (
            'a0000000-0000-0000-0000-000000000001',
            'admin@ulpan.ai',
            '$2b$12$5gOdtGXwFiALNjLTU1Q5LeSFcrx2sPt1aqN526gLv1a4VdlolpOZm',
            'Admin',
            'ru',
            1,
            0,
            0,
            NOW()
        )
        ON CONFLICT (email) DO NOTHING
    """))

    # Reset all sequences to max(id) + 1
    for table in SEED_TABLES:
        seq_name = f'{table}_id_seq'
        result = conn.execute(sa.text(
            "SELECT EXISTS(SELECT 1 FROM pg_class WHERE relname = :seq)"
        ), {'seq': seq_name})
        if result.scalar():
            conn.execute(sa.text(
                f"SELECT setval('{seq_name}', COALESCE((SELECT MAX(id) FROM {table}), 0) + 1, false)"
            ))


def downgrade() -> None:
    conn = op.get_bind()
    for table in reversed(SEED_TABLES):
        conn.execute(sa.text(f'DELETE FROM {table}'))
