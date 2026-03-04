"""Fix verb conjugation word_id mappings from migration 037.

Migration 037 mapped conjugation forms to wrong word_ids (shifted by 1
starting at id 1283). The migration expected לרוץ at id=1283, but the
actual words table has לכתוב there (לרוץ is at id=1974).

This remaps all affected conjugation rows to the correct word_ids.

Revision ID: 155
Revises: 154
"""
from alembic import op

revision = "155"
down_revision = "154"


def upgrade() -> None:
    # Remap conjugation word_ids that were assigned to wrong verbs.
    #
    # Migration 037 mapping (wrong) → Correct mapping:
    # word_id 1283 has לרוץ forms    → should be word_id 1974 (actual לרוץ)
    # word_id 1284 has לכתוב forms   → should be word_id 1283 (actual לכתוב)
    # word_id 1285 has לקרוא forms   → should be word_id 1284 (actual לקרוא)
    # word_id 1286 has לדבר forms    → should be word_id 1285 (actual לדבר)
    # word_id 1287 has לשמוע forms   → should be word_id 1286 (actual לשמוע)
    # word_id 1288 has לראות forms   → should be word_id 1287 (actual לראות)
    # word_id 1289 has לתת forms     → should be word_id 1288 (actual לתת)
    # word_id 1290 has לקחת forms    → should be word_id 1289 (actual לקחת)
    # word_id 1291 has לשחק forms    → should be word_id 1290 (actual לשחק)
    # word_id 1292 has ללמוד forms   → should be word_id 1291 (actual ללמוד)
    # word_id 1293 has לעבוד forms   → should be word_id 1292 (actual לעבוד)
    op.execute("""
        UPDATE verb_conjugations
        SET word_id = CASE word_id
            WHEN 1283 THEN 1974
            WHEN 1284 THEN 1283
            WHEN 1285 THEN 1284
            WHEN 1286 THEN 1285
            WHEN 1287 THEN 1286
            WHEN 1288 THEN 1287
            WHEN 1289 THEN 1288
            WHEN 1290 THEN 1289
            WHEN 1291 THEN 1290
            WHEN 1292 THEN 1291
            WHEN 1293 THEN 1292
        END
        WHERE word_id IN (1283, 1284, 1285, 1286, 1287, 1288, 1289, 1290, 1291, 1292, 1293)
    """)

    # Also delete conjugations assigned to non-verb words.
    # Migration 037 may have created conjugations for nouns/adjectives.
    op.execute("""
        DELETE FROM verb_conjugations vc
        USING words w
        WHERE vc.word_id = w.id AND w.pos != 'verb'
    """)


def downgrade() -> None:
    pass
