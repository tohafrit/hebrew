"""Add grammar_rule_tags table.

Revision ID: 011
Revises: 010
"""

from alembic import op
import sqlalchemy as sa

revision = "011"
down_revision = "010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "grammar_rule_tags",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("rule_id", sa.Integer(), sa.ForeignKey("grammar_topics.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("tag", sa.String(50), nullable=False, index=True),
    )

    # Seed tags based on typical grammar topic titles
    # This seeds tags for topics that likely exist based on common Hebrew grammar curriculum
    op.execute("""
        INSERT INTO grammar_rule_tags (rule_id, tag)
        SELECT id, 'conjugation_present'
        FROM grammar_topics
        WHERE lower(title_ru) LIKE '%настоящ%' OR lower(title_ru) LIKE '%present%'
    """)
    op.execute("""
        INSERT INTO grammar_rule_tags (rule_id, tag)
        SELECT id, 'conjugation_past'
        FROM grammar_topics
        WHERE lower(title_ru) LIKE '%прошедш%' OR lower(title_ru) LIKE '%past%'
    """)
    op.execute("""
        INSERT INTO grammar_rule_tags (rule_id, tag)
        SELECT id, 'conjugation_future'
        FROM grammar_topics
        WHERE lower(title_ru) LIKE '%будущ%' OR lower(title_ru) LIKE '%future%'
    """)
    op.execute("""
        INSERT INTO grammar_rule_tags (rule_id, tag)
        SELECT id, 'gender'
        FROM grammar_topics
        WHERE lower(title_ru) LIKE '%род%' OR lower(title_ru) LIKE '%gender%'
    """)
    op.execute("""
        INSERT INTO grammar_rule_tags (rule_id, tag)
        SELECT id, 'plural'
        FROM grammar_topics
        WHERE lower(title_ru) LIKE '%множественн%' OR lower(title_ru) LIKE '%plural%'
    """)
    op.execute("""
        INSERT INTO grammar_rule_tags (rule_id, tag)
        SELECT id, 'binyan_paal'
        FROM grammar_topics
        WHERE lower(title_ru) LIKE '%пааль%' OR lower(title_ru) LIKE '%pa''al%'
    """)


def downgrade() -> None:
    op.drop_table("grammar_rule_tags")
