"""Import ~60-80K verb conjugation forms from Eran Tomer Hebrew NLP dataset.

Downloads InflectedVerbsExtended.csv (241K rows, 17MB) from GitHub.
Matches verbs against our words table via infinitive forms.
Only imports COMPLETE spelling (ktiv male — standard modern spelling).

Dataset: https://github.com/NNLP-IL/Resources/tree/master/linguistic_resources/word_lists/hebrew_verbs_eran_tomer
License: CC-BY 4.0

Revision ID: 165
Revises: 164
"""
import csv
import os
import re
import urllib.request

from alembic import op
import sqlalchemy as sa

revision = "165"
down_revision = "164"

CSV_URL = (
    "https://raw.githubusercontent.com/NNLP-IL/Resources/master/"
    "linguistic_resources/word_lists/hebrew_verbs_eran_tomer/InflectedVerbsExtended.csv"
)
CSV_PATH = "/tmp/InflectedVerbsExtended.csv"

# Nikkud (vowel marks) regex
NIKKUD_RE = re.compile(r'[\u0591-\u05C7]')

# Eran Tomer binyan letter → our binyanim.id
BINYAN_MAP = {
    'A': 1,  # Pa'al (פעל)
    'B': 2,  # Nif'al (נפעל)
    'C': 3,  # Pi'el (פיעל)
    'D': 4,  # Pu'al (פועל)
    'E': 7,  # Hitpa'el (התפעל)
    'F': 5,  # Hif'il (הפעיל)
    'G': 6,  # Huf'al (הופעל)
}

TENSE_MAP = {
    'PAST': 'past',
    'PRESENT': 'present',
    'FUTURE': 'future',
    'IMPERATIVE': 'imperative',
    'BEINONI': 'beinoni',
    'INFINITIVE': 'infinitive',
}


def _strip_nikkud(s: str) -> str:
    return NIKKUD_RE.sub('', s).strip()


def _download_if_missing(url: str, path: str):
    if not os.path.exists(path):
        print(f"  Downloading {url}...")
        urllib.request.urlretrieve(url, path)
    else:
        print(f"  Using cached {path}")


def _parse_morphology(morph: str):
    """Parse Eran Tomer morphology string → (tense, person, gender, number) or None.

    Format: TENSE+PERSON+GENDER+NUMBER+SPELLING
    Examples:
      PAST+FIRST+MF+SINGULAR+COMPLETE → ('past', '1s', 'mf', 's')
      PRESENT+THIRD+M+SINGULAR+COMPLETE → ('present', 'ms', 'm', 's')
      INFINITIVE+E+E+E+COMPLETE → ('infinitive', '-', None, 's')
    """
    parts = morph.split('+')
    if len(parts) < 5:
        return None

    tense_raw, person_raw, gender_raw, number_raw, spelling = parts[:5]

    if spelling != 'COMPLETE':
        return None

    tense = TENSE_MAP.get(tense_raw)
    if not tense:
        return None

    # Gender
    gender = {'M': 'm', 'F': 'f', 'MF': 'mf', 'E': None}.get(gender_raw)

    # Number
    number = 'p' if number_raw == 'PLURAL' else 's'

    # Person — depends on tense
    if tense == 'infinitive':
        return tense, '-', None, 's'

    if tense in ('present', 'beinoni'):
        # Present/beinoni: person number is irrelevant, only gender+number matter
        g = gender or 'm'
        return tense, f"{g}{number}", gender, number

    # Past, future, imperative: include person number
    pnum = {'FIRST': '1', 'SECOND': '2', 'THIRD': '3'}.get(person_raw, '-')
    if number == 's':
        person = f"{pnum}s" if gender == 'mf' else f"{pnum}{gender}s"
    else:
        person = f"{pnum}p" if gender == 'mf' else f"{pnum}{gender}p"

    return tense, person, gender, number


def upgrade() -> None:
    _download_if_missing(CSV_URL, CSV_PATH)

    conn = op.get_bind()

    # 1. Load all verb words from DB: hebrew → word_id
    verb_words = {}
    rows = conn.execute(sa.text("SELECT id, hebrew FROM words WHERE pos = 'verb'"))
    for row in rows:
        if row[1] not in verb_words:
            verb_words[row[1]] = row[0]
    print(f"  Verb words in DB: {len(verb_words)}")

    # 2. Load existing conjugation base forms: form_he (past 3ms) → word_id
    conj_base = {}
    rows = conn.execute(sa.text(
        "SELECT DISTINCT word_id, form_he FROM verb_conjugations "
        "WHERE tense = 'past' AND person = '3ms'"
    ))
    for row in rows:
        conj_base[row[1]] = row[0]
    print(f"  Existing past-3ms conjugations: {len(conj_base)}")

    # 3. Load existing (word_id, form_he) pairs to skip duplicates
    existing_pairs = set()
    rows = conn.execute(sa.text("SELECT word_id, form_he FROM verb_conjugations"))
    for row in rows:
        existing_pairs.add((row[0], row[1]))
    print(f"  Existing conjugation entries: {len(existing_pairs)}")

    # 4. Parse CSV
    print("  Parsing CSV...")
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)
    print(f"  Total CSV rows: {len(all_rows)}")

    # 5. Build base_form → infinitive mapping (from INFINITIVE+COMPLETE rows)
    base_to_inf = {}
    for row in all_rows:
        morph = row['morphology']
        if morph.startswith('INFINITIVE') and morph.endswith('COMPLETE'):
            base_plain = _strip_nikkud(row['base_form'])
            inf_plain = _strip_nikkud(row['vocalized_inflection'])
            if base_plain and inf_plain:
                base_to_inf[base_plain] = inf_plain
    print(f"  Base → infinitive mappings: {len(base_to_inf)}")

    # 6. Match base forms → word_ids
    unique_bases = set()
    for row in all_rows:
        bp = _strip_nikkud(row['base_form'])
        if bp:
            unique_bases.add(bp)

    base_to_word_id = {}
    matched_inf = matched_base = matched_conj = 0

    for base_plain in unique_bases:
        # Try 1: infinitive → verb words table
        inf = base_to_inf.get(base_plain)
        if inf and inf in verb_words:
            base_to_word_id[base_plain] = verb_words[inf]
            matched_inf += 1
            continue

        # Try 2: base form (past 3ms) → verb words table
        if base_plain in verb_words:
            base_to_word_id[base_plain] = verb_words[base_plain]
            matched_base += 1
            continue

        # Try 3: base form → existing conjugation base forms
        if base_plain in conj_base:
            base_to_word_id[base_plain] = conj_base[base_plain]
            matched_conj += 1
            continue

    print(f"  Matched verbs: {len(base_to_word_id)}/{len(unique_bases)}")
    print(f"    via infinitive: {matched_inf}")
    print(f"    via base form:  {matched_base}")
    print(f"    via existing conj: {matched_conj}")

    # 7. Build insert list with deduplication
    to_insert = []
    seen = set()  # (word_id, form_he) dedup
    skipped_no_word = 0
    skipped_morph = 0
    skipped_dup = 0

    for row in all_rows:
        base_plain = _strip_nikkud(row['base_form'])
        word_id = base_to_word_id.get(base_plain)
        if not word_id:
            skipped_no_word += 1
            continue

        parsed = _parse_morphology(row['morphology'])
        if not parsed:
            skipped_morph += 1
            continue

        tense, person, gender, number = parsed
        form_he = _strip_nikkud(row['vocalized_inflection'])
        if not form_he:
            continue

        key = (word_id, form_he)
        if key in existing_pairs or key in seen:
            skipped_dup += 1
            continue
        seen.add(key)

        binyan_id = BINYAN_MAP.get(row['pattern'])
        if not binyan_id:
            continue

        to_insert.append({
            "word_id": word_id,
            "binyan_id": binyan_id,
            "tense": tense,
            "person": person,
            "gender": gender,
            "number": number,
            "form_he": form_he,
            "form_nikkud": row['vocalized_inflection'],
            "transliteration": None,
        })

    print(f"  New forms to insert: {len(to_insert)}")
    print(f"  Skipped (no word match): {skipped_no_word}")
    print(f"  Skipped (non-COMPLETE): {skipped_morph}")
    print(f"  Skipped (duplicate):    {skipped_dup}")

    # 8. Bulk insert
    if to_insert:
        conj_table = sa.table(
            "verb_conjugations",
            sa.column("word_id", sa.Integer),
            sa.column("binyan_id", sa.Integer),
            sa.column("tense", sa.String),
            sa.column("person", sa.String),
            sa.column("gender", sa.String),
            sa.column("number", sa.String),
            sa.column("form_he", sa.String),
            sa.column("form_nikkud", sa.String),
            sa.column("transliteration", sa.String),
        )

        BATCH = 2000
        for i in range(0, len(to_insert), BATCH):
            batch = to_insert[i:i + BATCH]
            conn.execute(conj_table.insert(), batch)
            print(f"    Inserted {min(i + BATCH, len(to_insert))}/{len(to_insert)}")

    total = conn.execute(sa.text("SELECT count(*) FROM verb_conjugations")).scalar()
    print(f"  Done! Total verb conjugations now: {total}")


def downgrade() -> None:
    print("  Note: downgrade does not remove imported conjugations.")
    print("  To fully rollback, restore from a database backup.")
