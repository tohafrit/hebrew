"""Add weekly_challenges table.

Revision ID: 009
Revises: 008
"""

from alembic import op
import sqlalchemy as sa

revision = "009"
down_revision = "008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "weekly_challenges",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("week_start", sa.Date(), nullable=False, index=True),
        sa.Column("title_ru", sa.String(200), nullable=False),
        sa.Column("description_ru", sa.Text(), nullable=False),
        sa.Column("challenge_type", sa.String(50), nullable=False),
        sa.Column("target_count", sa.Integer(), nullable=False),
        sa.Column("xp_reward", sa.Integer(), nullable=False, server_default="50"),
    )

    # Seed initial challenge templates for current week
    op.execute("""
        INSERT INTO weekly_challenges (week_start, title_ru, description_ru, challenge_type, target_count, xp_reward)
        VALUES
            (date_trunc('week', CURRENT_DATE)::date, 'Марафон XP', 'Заработайте 500 XP за неделю', 'earn_xp', 500, 100),
            (date_trunc('week', CURRENT_DATE)::date, 'Мастер упражнений', 'Выполните 50 упражнений', 'complete_exercises', 50, 75),
            (date_trunc('week', CURRENT_DATE)::date, 'Карточки каждый день', 'Повторите 100 карточек', 'review_cards', 100, 75),
            (date_trunc('week', CURRENT_DATE)::date, 'Регулярность', 'Занимайтесь 5 дней из 7', 'active_days', 5, 100),
            (date_trunc('week', CURRENT_DATE)::date, 'Время учиться', 'Проведите 60 минут в обучении', 'study_minutes', 60, 50)
    """)


def downgrade() -> None:
    op.drop_table("weekly_challenges")
