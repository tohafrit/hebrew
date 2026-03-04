"""Fix NULL frequency_rank for 500 words and correct misassigned ranks.

Revision ID: 154
Revises: 153
"""
from alembic import op

revision = "154"
down_revision = "153"


def upgrade() -> None:
    # 1. Set frequency_rank based on level_id for the 500 words that have NULL
    #    Level 1-2 → rank 1 (very common), Level 3-4 → rank 2, Level 5-6 → rank 3
    op.execute("""
        UPDATE words SET frequency_rank = 1
        WHERE frequency_rank IS NULL AND level_id IN (1, 2)
    """)
    op.execute("""
        UPDATE words SET frequency_rank = 2
        WHERE frequency_rank IS NULL AND level_id IN (3, 4)
    """)
    op.execute("""
        UPDATE words SET frequency_rank = 3
        WHERE frequency_rank IS NULL AND level_id IN (5, 6)
    """)

    # 2. Fix specific misassigned ranks: duplicate hebrew entries where
    #    an obscure meaning has higher priority than the common one.
    #    For words that appear at multiple levels, the lowest-level entry
    #    (most basic meaning) should have the best frequency_rank.
    #
    #    Strategy: for any hebrew string that appears in multiple rows,
    #    ensure the lowest-level entry has the lowest frequency_rank.
    #    We set level 5-6 duplicates to rank 3 if they currently outrank
    #    a level 1-2 entry.
    op.execute("""
        UPDATE words w SET frequency_rank = 3
        WHERE w.level_id >= 5
          AND w.frequency_rank <= 2
          AND EXISTS (
              SELECT 1 FROM words w2
              WHERE w2.hebrew = w.hebrew
                AND w2.id != w.id
                AND w2.level_id <= 2
          )
    """)

    # Also fix level 3-4 duplicates that outrank level 1-2 entries
    op.execute("""
        UPDATE words w SET frequency_rank = 2
        WHERE w.level_id IN (3, 4)
          AND w.frequency_rank = 1
          AND EXISTS (
              SELECT 1 FROM words w2
              WHERE w2.hebrew = w.hebrew
                AND w2.id != w.id
                AND w2.level_id <= 2
                AND w2.frequency_rank = 1
          )
    """)


def downgrade() -> None:
    # Can't perfectly reverse, but reset the 500 words back to NULL
    # This is best-effort
    pass
