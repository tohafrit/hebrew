"""add learning_paths table

Revision ID: 003
Revises: 002
Create Date: 2026-03-05 12:00:00.000000

"""
import os
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'learning_paths',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('level_id', sa.Integer(), sa.ForeignKey('levels.id'), nullable=False),
        sa.Column('unit', sa.Integer(), nullable=False),
        sa.Column('step', sa.Integer(), nullable=False),
        sa.Column('step_type', sa.String(30), nullable=False),  # vocabulary, grammar, exercise, reading, dialogue, srs_review
        sa.Column('content_id', sa.Integer(), nullable=True),  # FK to relevant table depending on step_type
        sa.Column('title_ru', sa.String(200), nullable=False),
        sa.Column('title_he', sa.String(200), nullable=True),
        sa.Column('description_ru', sa.String(500), nullable=True),
        sa.Column('icon', sa.String(10), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_learning_paths_level_unit', 'learning_paths', ['level_id', 'unit', 'step'])

    op.create_table(
        'user_path_progress',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('path_step_id', sa.Integer(), sa.ForeignKey('learning_paths.id', ondelete='CASCADE'), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'path_step_id', name='uq_user_path_step'),
    )
    op.create_index('ix_user_path_progress_user', 'user_path_progress', ['user_id'])

    # Seed the learning path data
    seed_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'seed')
    seed_dir = os.path.abspath(seed_dir)
    sql_file = os.path.join(seed_dir, 'learning_paths.sql')

    if os.path.exists(sql_file):
        conn = op.get_bind()
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql = f.read().strip()
        if sql:
            cursor = conn.connection.dbapi_connection.cursor()
            cursor.execute(sql)
            cursor.close()
            conn.execute(sa.text(
                "SELECT setval('learning_paths_id_seq', COALESCE((SELECT MAX(id) FROM learning_paths), 0) + 1, false)"
            ))


def downgrade() -> None:
    op.drop_table('user_path_progress')
    op.drop_table('learning_paths')
