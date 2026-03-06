"""Add spaced_reading_schedules table and text_id FK to user_reading_sessions.

Revision ID: 010
Revises: 009
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision = "010"
down_revision = "009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "spaced_reading_schedules",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("text_id", sa.Integer(), sa.ForeignKey("reading_texts.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("next_review", sa.TIMESTAMP(), nullable=False),
        sa.Column("interval_days", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("review_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_known_pct", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.text("now()")),
    )

    # Add optional text_id to user_reading_sessions
    op.add_column(
        "user_reading_sessions",
        sa.Column("text_id", sa.Integer(), sa.ForeignKey("reading_texts.id", ondelete="SET NULL"), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("user_reading_sessions", "text_id")
    op.drop_table("spaced_reading_schedules")
