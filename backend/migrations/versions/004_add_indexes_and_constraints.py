"""Add missing indexes and constraints.

Revision ID: 004
Revises: 003
"""

from alembic import op
import sqlalchemy as sa

revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Index on srs_schedule.next_review for fast due-card queries
    op.create_index("ix_srs_schedule_next_review", "srs_schedule", ["next_review"])

    # Index on word_forms.hebrew for reader lookups
    op.create_index("ix_word_forms_hebrew", "word_forms", ["hebrew"])

    # Index on verb_conjugations.form_he for reader lookups
    op.create_index("ix_verb_conjugations_form_he", "verb_conjugations", ["form_he"])

    # Unique constraint on achievements(user_id, type) to prevent duplicates
    op.create_unique_constraint("uq_achievements_user_type", "achievements", ["user_id", "type"])

    # Unique constraint on user_path_progress(user_id, path_step_id)
    op.create_unique_constraint("uq_user_path_progress", "user_path_progress", ["user_id", "path_step_id"])


def downgrade() -> None:
    op.drop_constraint("uq_user_path_progress", "user_path_progress", type_="unique")
    op.drop_constraint("uq_achievements_user_type", "achievements", type_="unique")
    op.drop_index("ix_verb_conjugations_form_he", "verb_conjugations")
    op.drop_index("ix_word_forms_hebrew", "word_forms")
    op.drop_index("ix_srs_schedule_next_review", "srs_schedule")
