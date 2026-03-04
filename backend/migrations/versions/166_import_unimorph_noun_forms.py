"""Import ~2-3K noun/adjective inflected forms from UniMorph Hebrew dataset.

Downloads the `heb` file (unvocalized forms, ktiv male) from GitHub.
Matches lemmas against our words table and inserts inflected forms
(plurals, construct state, possessives) into word_forms.

Dataset: https://github.com/unimorph/heb
License: CC-BY-SA 3.0

Revision ID: 166
Revises: 165
"""
import os
import urllib.request

from alembic import op
import sqlalchemy as sa

revision = "166"
down_revision = "165"

HEB_URL = "https://raw.githubusercontent.com/unimorph/heb/master/heb"
HEB_PATH = "/tmp/unimorph_heb.tsv"


def _download_if_missing(url: str, path: str):
    if not os.path.exists(path):
        print(f"  Downloading {url}...")
        urllib.request.urlretrieve(url, path)
    else:
        print(f"  Using cached {path}")


def _tag_to_form_type(tag: str) -> str:
    """Map UniMorph tag string to a concise form_type label.

    Examples:
      N;PL;NDEF → plural
      N;SG;DEF → definite
      N;PL;DEF → plural_def
      N;SG;PSSD → construct
      N;PL;PSSD → construct_pl
      N;SG;PSSD;PSS1S → possessive
      N;PL;PSSD;PSS3S;MASC → possessive_pl
    """
    if 'PSS' in tag and 'PSSD' in tag:
        # Possessive forms (N;SG;PSSD;PSS1S or N;PL;PSSD;PSS3S;MASC)
        return 'possessive_pl' if 'PL' in tag else 'possessive'
    if 'PSSD' in tag:
        # Construct state (N;SG;PSSD or N;PL;PSSD)
        return 'construct_pl' if 'PL' in tag else 'construct'
    if 'DEF' in tag and 'NDEF' not in tag:
        return 'plural_def' if 'PL' in tag else 'definite'
    if 'PL' in tag:
        return 'plural'
    return 'singular'


def upgrade() -> None:
    _download_if_missing(HEB_URL, HEB_PATH)

    conn = op.get_bind()

    # Load all words: hebrew → word_id
    word_map = {}
    rows = conn.execute(sa.text("SELECT id, hebrew FROM words"))
    for row in rows:
        if row[1] not in word_map:
            word_map[row[1]] = row[0]
    print(f"  Words in DB: {len(word_map)}")

    # Load existing word_forms: (word_id, hebrew) pairs
    existing_forms = set()
    rows = conn.execute(sa.text("SELECT word_id, hebrew FROM word_forms"))
    for row in rows:
        existing_forms.add((row[0], row[1]))
    print(f"  Existing word_forms: {len(existing_forms)}")

    # Parse UniMorph file (TSV: lemma\tinflected\ttags)
    print("  Parsing UniMorph heb file...")
    to_insert = []
    seen = set()
    matched_lemmas = set()
    skipped_no_word = 0
    skipped_same = 0
    skipped_dup = 0
    skipped_non_noun = 0
    total_lines = 0

    with open(HEB_PATH, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total_lines += 1
            parts = line.split('\t')
            if len(parts) < 3:
                continue

            lemma, inflected, tags = parts[0], parts[1], parts[2]

            # Only import noun entries (N; prefix)
            if not tags.startswith('N;'):
                skipped_non_noun += 1
                continue

            # Match lemma against our words table
            word_id = word_map.get(lemma)
            if not word_id:
                skipped_no_word += 1
                continue

            matched_lemmas.add(lemma)

            # Skip if inflected form is same as lemma (base form already in words)
            if inflected == lemma:
                skipped_same += 1
                continue

            # Dedup
            key = (word_id, inflected)
            if key in existing_forms or key in seen:
                skipped_dup += 1
                continue
            seen.add(key)

            form_type = _tag_to_form_type(tags)
            to_insert.append({
                "word_id": word_id,
                "form_type": form_type,
                "hebrew": inflected,
                "nikkud": None,
                "transliteration": None,
                "description": tags,  # store full UniMorph tag as description
            })

    print(f"  Total lines: {total_lines}")
    print(f"  Matched lemmas: {len(matched_lemmas)}")
    print(f"  New forms to insert: {len(to_insert)}")
    print(f"  Skipped (non-noun):   {skipped_non_noun}")
    print(f"  Skipped (no word):    {skipped_no_word}")
    print(f"  Skipped (same form):  {skipped_same}")
    print(f"  Skipped (duplicate):  {skipped_dup}")

    # Bulk insert
    if to_insert:
        forms_table = sa.table(
            "word_forms",
            sa.column("word_id", sa.Integer),
            sa.column("form_type", sa.String),
            sa.column("hebrew", sa.String),
            sa.column("nikkud", sa.String),
            sa.column("transliteration", sa.String),
            sa.column("description", sa.String),
        )

        BATCH = 1000
        for i in range(0, len(to_insert), BATCH):
            batch = to_insert[i:i + BATCH]
            conn.execute(forms_table.insert(), batch)
            print(f"    Inserted {min(i + BATCH, len(to_insert))}/{len(to_insert)}")

    total = conn.execute(sa.text("SELECT count(*) FROM word_forms")).scalar()
    print(f"  Done! Total word_forms now: {total}")


def downgrade() -> None:
    print("  Note: downgrade does not remove imported word forms.")
    print("  To fully rollback, restore from a database backup.")
