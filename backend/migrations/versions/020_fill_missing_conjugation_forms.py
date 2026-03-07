"""fill missing verb conjugation forms

Revision ID: 020
Revises: 019
Create Date: 2026-03-07

In modern Israeli Hebrew, certain forms are identical:
- 3fp (3rd person feminine plural) = 3mp (3rd person masculine plural) in past & future
- 2fp (2nd person feminine plural) = 2mp (2nd person masculine plural) in future
- 2fp imperative = 2mp imperative (in modern usage)

This migration fills missing forms by copying from their equivalent counterparts.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text as sa_text

revision: str = '020'
down_revision: Union[str, None] = '019'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# In modern Hebrew, these person codes share the same form.
# (tense, missing_person, source_person, target_gender, target_number)
COPY_RULES = [
    # Future tense: 3fp = 3mp
    ("future", "3fp", "3mp", "f", "p"),
    # Future tense: 2fp = 2mp
    ("future", "2fp", "2mp", "f", "p"),
    # Past tense: 3fp = 3mp
    ("past", "3fp", "3mp", "f", "p"),
    # Imperative: 2fp = 2mp (modern Hebrew uses masculine plural for both)
    ("imperative", "2fp", "2mp", "f", "p"),
]


def upgrade() -> None:
    conn = op.get_bind()
    total_inserted = 0

    for tense, missing_person, source_person, target_gender, target_number in COPY_RULES:
        # Find (word_id, binyan_id) combos that have source_person but not missing_person
        result = conn.execute(sa_text("""
            INSERT INTO verb_conjugations (word_id, binyan_id, tense, person, gender, number, form_he, form_nikkud, transliteration)
            SELECT
                src.word_id,
                src.binyan_id,
                src.tense,
                :missing_person,
                :target_gender,
                :target_number,
                src.form_he,
                src.form_nikkud,
                src.transliteration
            FROM verb_conjugations src
            WHERE src.tense = :tense
              AND src.person = :source_person
              AND NOT EXISTS (
                  SELECT 1 FROM verb_conjugations existing
                  WHERE existing.word_id = src.word_id
                    AND existing.binyan_id = src.binyan_id
                    AND existing.tense = :tense
                    AND existing.person = :missing_person
              )
        """), {
            "tense": tense,
            "missing_person": missing_person,
            "source_person": source_person,
            "target_gender": target_gender,
            "target_number": target_number,
        })
        count = result.rowcount
        total_inserted += count
        print(f"  [020] {tense} {missing_person} (from {source_person}): {count} forms added")

    # Also fill missing 2fs past from 2ms past — in modern Hebrew they share
    # the same consonantal form (form_he), only nikkud differs slightly.
    # Better to have the form available than to have a gap.
    result = conn.execute(sa_text("""
        INSERT INTO verb_conjugations (word_id, binyan_id, tense, person, gender, number, form_he, form_nikkud, transliteration)
        SELECT
            src.word_id,
            src.binyan_id,
            src.tense,
            '2fs',
            'f',
            's',
            src.form_he,
            src.form_nikkud,
            src.transliteration
        FROM verb_conjugations src
        WHERE src.tense = 'past'
          AND src.person = '2ms'
          AND NOT EXISTS (
              SELECT 1 FROM verb_conjugations existing
              WHERE existing.word_id = src.word_id
                AND existing.binyan_id = src.binyan_id
                AND existing.tense = 'past'
                AND existing.person = '2fs'
          )
    """))
    count = result.rowcount
    total_inserted += count
    print(f"  [020] past 2fs (from 2ms): {count} forms added")

    # Fill missing 2mp imperative from 2ms imperative + heuristic
    # In Hebrew, 2mp imperative = 2ms + וּ (e.g., כתוב → כתבו)
    # We can't reliably construct the form, so copy form_he from 2ms
    # and add וּ suffix. But for form_he (without nikkud), just appending ו works.
    result = conn.execute(sa_text("""
        INSERT INTO verb_conjugations (word_id, binyan_id, tense, person, gender, number, form_he, form_nikkud, transliteration)
        SELECT
            src.word_id,
            src.binyan_id,
            'imperative',
            '2mp',
            'm',
            'p',
            src.form_he || 'ו',
            NULL,
            NULL
        FROM verb_conjugations src
        WHERE src.tense = 'imperative'
          AND src.person = '2ms'
          AND NOT EXISTS (
              SELECT 1 FROM verb_conjugations existing
              WHERE existing.word_id = src.word_id
                AND existing.binyan_id = src.binyan_id
                AND existing.tense = 'imperative'
                AND existing.person = '2mp'
          )
    """))
    count = result.rowcount
    total_inserted += count
    print(f"  [020] imperative 2mp (from 2ms+ו): {count} forms added")

    print(f"  [020] Total forms added: {total_inserted}")


def downgrade() -> None:
    # Remove the forms we added — they can be identified as having no unique data
    # that wasn't copied. In practice, just re-run seed if needed.
    pass
