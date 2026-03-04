"""Add common Hebrew words missing from dictionary.

Adds: מייל (email)

Revision ID: 168
Revises: 167
"""
from alembic import op
import sqlalchemy as sa

revision = "168"
down_revision = "167"

WORDS = [
    {
        "hebrew": "מייל",
        "translation_ru": "электронная почта, имейл",
        "transliteration": "meyl",
        "pos": "noun",
        "frequency_rank": 2,
    },
]


def upgrade() -> None:
    conn = op.get_bind()
    words_table = sa.table(
        "words",
        sa.column("hebrew", sa.String),
        sa.column("translation_ru", sa.String),
        sa.column("transliteration", sa.String),
        sa.column("pos", sa.String),
        sa.column("frequency_rank", sa.Integer),
    )
    for w in WORDS:
        # Skip if already exists
        exists = conn.execute(
            sa.text("SELECT 1 FROM words WHERE hebrew = :h"),
            {"h": w["hebrew"]},
        ).first()
        if not exists:
            conn.execute(words_table.insert().values(**w))
            print(f"  Added: {w['hebrew']}")
        else:
            print(f"  Already exists: {w['hebrew']}")


def downgrade() -> None:
    conn = op.get_bind()
    for w in WORDS:
        conn.execute(
            sa.text("DELETE FROM words WHERE hebrew = :h AND transliteration = :t"),
            {"h": w["hebrew"], "t": w["transliteration"]},
        )
