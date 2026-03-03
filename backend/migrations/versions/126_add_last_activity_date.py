"""Add last_activity_date column to users table.

Tracks the last date a user was active for streak calculation.

Revision ID: 126
Revises: 125
"""

from alembic import op
import sqlalchemy as sa

revision = "126"
down_revision = "125"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("last_activity_date", sa.Date(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "last_activity_date")
