"""add nikkud to reading texts that lack vowel marks

Revision ID: 021
Revises: 020
Create Date: 2026-03-07

Uses the words table (which has nikkud for all entries) to add vowel marks
to reading texts. For each word in the text, looks up the nikkud form and
replaces the bare consonantal form.
"""
from typing import Sequence, Union
import re

from alembic import op
from sqlalchemy import text as sa_text

revision: str = '021'
down_revision: Union[str, None] = '020'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Nikkud unicode range
NIKKUD_RE = re.compile(r'[\u0591-\u05C7]')

# Hebrew letter range (for detecting Hebrew tokens)
HE_RE = re.compile(r'[\u05D0-\u05EA]+')


def _has_nikkud(text: str) -> bool:
    return bool(NIKKUD_RE.search(text))


def _build_nikkud_map(conn) -> dict[str, str]:
    """Build mapping from consonantal Hebrew to nikkud form.
    For duplicates, prefer: lower level_id, then noun/verb over other POS.
    """
    rows = conn.execute(sa_text("""
        SELECT hebrew, nikkud, pos, COALESCE(level_id, 99) as lvl
        FROM words
        WHERE nikkud IS NOT NULL AND nikkud != ''
        ORDER BY COALESCE(level_id, 99) ASC, id ASC
    """)).fetchall()

    nikkud_map: dict[str, str] = {}
    for hebrew, nikkud, pos, lvl in rows:
        clean = NIKKUD_RE.sub("", hebrew)
        if clean not in nikkud_map:
            nikkud_map[clean] = nikkud
    return nikkud_map


def _add_nikkud_to_text(text: str, nikkud_map: dict[str, str]) -> str:
    """Replace bare Hebrew words with their nikkud forms."""
    if _has_nikkud(text):
        return text

    def replace_word(match):
        word = match.group(0)
        return nikkud_map.get(word, word)

    return HE_RE.sub(replace_word, text)


def upgrade() -> None:
    conn = op.get_bind()

    # Build nikkud lookup from words table
    nikkud_map = _build_nikkud_map(conn)
    print(f"  [021] Nikkud map: {len(nikkud_map)} entries")

    # Find texts without nikkud
    rows = conn.execute(sa_text("""
        SELECT id, content_he FROM reading_texts
        WHERE content_he IS NOT NULL
          AND content_he !~ '[\u0591-\u05C7]'
    """)).fetchall()

    updated = 0
    for text_id, content_he in rows:
        new_content = _add_nikkud_to_text(content_he, nikkud_map)
        if new_content != content_he:
            conn.execute(sa_text(
                "UPDATE reading_texts SET content_he = :content WHERE id = :id"
            ), {"content": new_content, "id": text_id})
            updated += 1

    print(f"  [021] Updated {updated} of {len(rows)} texts without nikkud")


def downgrade() -> None:
    pass
