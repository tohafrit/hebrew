"""fix verb conjugation data quality issues

Revision ID: 018
Revises: 017
Create Date: 2026-03-07

Fixes:
1. Sofit letters in non-final positions (ץ→צ, ם→מ, ן→נ, ף→פ, ך→כ mid-word)
2. Remove duplicate conjugation rows (keep highest ID = newest/corrected)
3. Remove beinoni entries that duplicate present tense
4. Fix invalid person codes (bare '0','1','2','3')
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text as sa_text

revision: str = '018'
down_revision: Union[str, None] = '017'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Sofit → regular letter mapping (for mid-word fix)
SOFIT_TO_REGULAR = {
    "\u05da": "\u05db",  # ך → כ
    "\u05dd": "\u05de",  # ם → מ
    "\u05df": "\u05e0",  # ן → נ
    "\u05e3": "\u05e4",  # ף → פ
    "\u05e5": "\u05e6",  # ץ → צ
}

HEBREW_RANGE = set(chr(c) for c in range(0x05D0, 0x05EB))


def fix_sofit_in_text(text: str) -> str:
    """Fix sofit letters that appear before another Hebrew letter or nikkud."""
    if not text:
        return text
    chars = list(text)
    changed = False
    for i in range(len(chars) - 1):
        if chars[i] in SOFIT_TO_REGULAR:
            next_ch = chars[i + 1]
            if next_ch in HEBREW_RANGE or ("\u0591" <= next_ch <= "\u05C7"):
                chars[i] = SOFIT_TO_REGULAR[chars[i]]
                changed = True
    return "".join(chars) if changed else text


def upgrade() -> None:
    conn = op.get_bind()

    # ── 1. Fix sofit letters in non-final positions ──────────────────────
    # Fetch all forms with potential sofit issues
    sofit_chars = "".join(SOFIT_TO_REGULAR.keys())
    # Use a broad query — any form containing a sofit letter (we'll check position in Python)
    rows = conn.execute(sa_text(
        "SELECT id, form_he, form_nikkud FROM verb_conjugations"
    )).fetchall()

    sofit_fixes = 0
    for row_id, form_he, form_nikkud in rows:
        new_he = fix_sofit_in_text(form_he)
        new_nk = fix_sofit_in_text(form_nikkud) if form_nikkud else form_nikkud
        if new_he != form_he or new_nk != form_nikkud:
            conn.execute(sa_text(
                "UPDATE verb_conjugations SET form_he = :he, form_nikkud = :nk WHERE id = :id"
            ), {"he": new_he, "nk": new_nk, "id": row_id})
            sofit_fixes += 1
    print(f"  [018] Sofit fixes: {sofit_fixes}")

    # ── 2. Remove duplicate conjugation rows ─────────────────────────────
    # For each (word_id, binyan_id, tense, person, gender, number), keep max(id)
    result = conn.execute(sa_text("""
        DELETE FROM verb_conjugations
        WHERE id NOT IN (
            SELECT MAX(id)
            FROM verb_conjugations
            GROUP BY word_id, binyan_id, tense, person, gender, number
        )
    """))
    print(f"  [018] Duplicate rows removed: {result.rowcount}")

    # ── 3. Remove beinoni rows where present exists for same word+binyan ─
    result = conn.execute(sa_text("""
        DELETE FROM verb_conjugations
        WHERE tense = 'beinoni'
          AND word_id IN (
              SELECT DISTINCT word_id FROM verb_conjugations WHERE tense = 'present'
          )
    """))
    print(f"  [018] Redundant beinoni rows removed: {result.rowcount}")

    # ── 4. Delete rows with bare numeric person codes ────────────────────
    result = conn.execute(sa_text("""
        DELETE FROM verb_conjugations
        WHERE person IN ('0', '1', '2', '3')
    """))
    print(f"  [018] Invalid person code rows removed: {result.rowcount}")


def downgrade() -> None:
    # Data fixes — not reversible without backup
    pass
