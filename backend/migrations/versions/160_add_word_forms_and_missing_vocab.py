"""Add word forms for adjectives, missing vocabulary words, and fix verb conjugations.

This migration:
1. Inserts 7 missing vocabulary words (לעשות, לשנות, חוץ, נוסף, עשוי, קול, רם)
2. Generates inflected adjective forms (fs/mp/fp) for all adjectives in the words table
3. Fixes wrong verb conjugation forms:
   a. Fixes hollow-verb sofit letters appearing before suffixes (regex replace)
   b. Replaces conjugations for לקום, לגלות, לפרסם, לחכות with correct forms
   c. Adds conjugations for the two new verbs לעשות and לשנות

Revision ID: 160
Revises: 159
"""
from alembic import op
import sqlalchemy as sa


revision = "160"
down_revision = "159"


# ─── Table references ─────────────────────────────────────────────────────────

words_table = sa.table(
    "words",
    sa.column("hebrew", sa.String),
    sa.column("translation_ru", sa.String),
    sa.column("transliteration", sa.String),
    sa.column("pos", sa.String),
    sa.column("root", sa.String),
    sa.column("level_id", sa.Integer),
    sa.column("frequency_rank", sa.Integer),
)

word_forms_table = sa.table(
    "word_forms",
    sa.column("word_id", sa.Integer),
    sa.column("form_type", sa.String),
    sa.column("hebrew", sa.String),
    sa.column("nikkud", sa.String),
    sa.column("transliteration", sa.String),
    sa.column("description", sa.String),
)

verb_conjugations_table = sa.table(
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


# ─── Part 1: Missing vocabulary words ─────────────────────────────────────────

# (hebrew, translation_ru, transliteration, pos, root, level_id, frequency_rank)
MISSING_WORDS = [
    ("לעשות", "делать", "la'asot", "verb", "ע.ש.ה", 1, 1),
    ("לשנות", "менять, изменять", "leshanot", "verb", "ש.נ.ה", 1, 1),
    ("חוץ", "снаружи; кроме", "khutz", "noun", None, 1, 1),
    ("נוסף", "дополнительный", "nosaf", "adj", "י.ס.פ", 2, 1),
    ("עשוי", "сделанный; может", "asuy", "adj", "ע.ש.ה", 2, 1),
    ("קול", "голос, звук", "kol", "noun", None, 1, 1),
    ("רם", "громкий, высокий", "ram", "adj", None, 1, 1),
]


# ─── Part 2: Adjective inflection helpers ─────────────────────────────────────

# Map sofit (final) letter → regular (medial) letter
SOFIT_TO_REGULAR = {
    'ך': 'כ',
    'ם': 'מ',
    'ן': 'נ',
    'ף': 'פ',
    'ץ': 'צ',
}


def generate_adjective_forms(word_id: int, base: str) -> list[dict]:
    """Return a list of word_forms rows for the given adjective base form."""
    forms = []

    if not base:
        return forms

    last = base[-1]

    if last == 'ה':
        # ה-ending adjectives: drop ה, add ים / ות
        stem = base[:-1]
        forms.append({
            "word_id": word_id,
            "form_type": "mp",
            "hebrew": stem + "ים",
            "nikkud": None,
            "transliteration": None,
            "description": None,
        })
        forms.append({
            "word_id": word_id,
            "form_type": "fp",
            "hebrew": stem + "ות",
            "nikkud": None,
            "transliteration": None,
            "description": None,
        })
        # fs == base for ה-ending adjectives; skip

    elif last == 'י':
        # י-ending adjectives (e.g. ישראלי): add ת / ים / ות
        forms.append({
            "word_id": word_id,
            "form_type": "fs",
            "hebrew": base + "ת",
            "nikkud": None,
            "transliteration": None,
            "description": None,
        })
        forms.append({
            "word_id": word_id,
            "form_type": "mp",
            "hebrew": base + "ים",
            "nikkud": None,
            "transliteration": None,
            "description": None,
        })
        forms.append({
            "word_id": word_id,
            "form_type": "fp",
            "hebrew": base + "ות",
            "nikkud": None,
            "transliteration": None,
            "description": None,
        })

    else:
        # Regular consonant ending (possibly sofit)
        # For suffixes, convert sofit to regular form first
        if last in SOFIT_TO_REGULAR:
            stem = base[:-1] + SOFIT_TO_REGULAR[last]
        else:
            stem = base

        forms.append({
            "word_id": word_id,
            "form_type": "fs",
            "hebrew": stem + "ה",
            "nikkud": None,
            "transliteration": None,
            "description": None,
        })
        forms.append({
            "word_id": word_id,
            "form_type": "mp",
            "hebrew": stem + "ים",
            "nikkud": None,
            "transliteration": None,
            "description": None,
        })
        forms.append({
            "word_id": word_id,
            "form_type": "fp",
            "hebrew": stem + "ות",
            "nikkud": None,
            "transliteration": None,
            "description": None,
        })

    return forms


# ─── Part 3: Correct conjugation data ─────────────────────────────────────────

def _conj(word_id, binyan_id, tense, person, gender, number, form_he):
    return {
        "word_id": word_id,
        "binyan_id": binyan_id,
        "tense": tense,
        "person": person,
        "gender": gender,
        "number": number,
        "form_he": form_he,
        "form_nikkud": None,
        "transliteration": None,
    }


def _build_verb_rows(word_id, binyan_id, past, present, future, imperative=None):
    """Build conjugation row dicts from compact lists.

    past: [1s, 2ms, 2fs, 3ms, 3fs, 1p, 2mp, 2fp, 3p]
    present: [ms, fs, mp, fp]
    future: [1s, 2ms, 2fs, 3ms, 3fs, 1p, 2mp, 3p]  (8 forms)
    imperative: [2ms, 2fs, 2mp]  (optional)
    """
    rows = []

    past_specs = [
        ('1s', 'mf', 's'), ('2ms', 'm', 's'), ('2fs', 'f', 's'),
        ('3ms', 'm', 's'), ('3fs', 'f', 's'),
        ('1p', 'mf', 'p'), ('2mp', 'm', 'p'), ('2fp', 'f', 'p'), ('3p', 'mf', 'p'),
    ]
    for (person, gender, number), form in zip(past_specs, past):
        rows.append(_conj(word_id, binyan_id, 'past', person, gender, number, form))

    present_specs = [
        ('ms', 'm', 's'), ('fs', 'f', 's'), ('mp', 'm', 'p'), ('fp', 'f', 'p'),
    ]
    for (person, gender, number), form in zip(present_specs, present):
        rows.append(_conj(word_id, binyan_id, 'present', person, gender, number, form))

    future_specs = [
        ('1s', 'mf', 's'), ('2ms', 'm', 's'), ('2fs', 'f', 's'),
        ('3ms', 'm', 's'), ('3fs', 'f', 's'),
        ('1p', 'mf', 'p'), ('2mp', 'm', 'p'), ('3p', 'mf', 'p'),
    ]
    for (person, gender, number), form in zip(future_specs, future):
        rows.append(_conj(word_id, binyan_id, 'future', person, gender, number, form))

    if imperative:
        imp_specs = [
            ('2ms', 'm', 's'), ('2fs', 'f', 's'), ('2mp', 'm', 'p'),
        ]
        for (person, gender, number), form in zip(imp_specs, imperative):
            rows.append(_conj(word_id, binyan_id, 'imperative', person, gender, number, form))

    return rows


# לקום — Pa'al hollow, root ק.ו.מ, word_id=377, binyan_id=1
LAQUM_ROWS = _build_verb_rows(
    word_id=377,
    binyan_id=1,
    past=['קמתי', 'קמת', 'קמת', 'קם', 'קמה', 'קמנו', 'קמתם', 'קמתן', 'קמו'],
    present=['קם', 'קמה', 'קמים', 'קמות'],
    future=['אקום', 'תקום', 'תקומי', 'יקום', 'תקום', 'נקום', 'תקומו', 'יקומו'],
    imperative=['קום', 'קומי', 'קומו'],
)

# לגלות — Pi'el lamed-he, root ג.ל.ה, word_id=727, binyan_id=3
LGALOT_ROWS = _build_verb_rows(
    word_id=727,
    binyan_id=3,
    past=['גיליתי', 'גילית', 'גילית', 'גילה', 'גילתה', 'גילינו', 'גיליתם', 'גיליתן', 'גילו'],
    present=['מגלה', 'מגלה', 'מגלים', 'מגלות'],
    future=['אגלה', 'תגלה', 'תגלי', 'יגלה', 'תגלה', 'נגלה', 'תגלו', 'יגלו'],
    imperative=['גלה', 'גלי', 'גלו'],
)

# לפרסם — Pi'el quadriliteral, root פ.ר.ס.מ, word_id=943, binyan_id=3
LPARSEM_ROWS = _build_verb_rows(
    word_id=943,
    binyan_id=3,
    past=['פירסמתי', 'פירסמת', 'פירסמת', 'פירסם', 'פירסמה', 'פירסמנו', 'פירסמתם', 'פירסמתן', 'פירסמו'],
    present=['מפרסם', 'מפרסמת', 'מפרסמים', 'מפרסמות'],
    future=['אפרסם', 'תפרסם', 'תפרסמי', 'יפרסם', 'תפרסם', 'נפרסם', 'תפרסמו', 'יפרסמו'],
    imperative=['פרסם', 'פרסמי', 'פרסמו'],
)

# לחכות — Pi'el lamed-he, root ח.כ.ה, word_id=1947, binyan_id=3
LKHAKOT_ROWS = _build_verb_rows(
    word_id=1947,
    binyan_id=3,
    past=['חיכיתי', 'חיכית', 'חיכית', 'חיכה', 'חיכתה', 'חיכינו', 'חיכיתם', 'חיכיתן', 'חיכו'],
    present=['מחכה', 'מחכה', 'מחכים', 'מחכות'],
    future=['אחכה', 'תחכה', 'תחכי', 'יחכה', 'תחכה', 'נחכה', 'תחכו', 'יחכו'],
)


def _lasot_rows(word_id):
    """לעשות — Pa'al lamed-he, root ע.ש.ה, binyan_id=1"""
    return _build_verb_rows(
        word_id=word_id,
        binyan_id=1,
        past=['עשיתי', 'עשית', 'עשית', 'עשה', 'עשתה', 'עשינו', 'עשיתם', 'עשיתן', 'עשו'],
        present=['עושה', 'עושה', 'עושים', 'עושות'],
        future=['אעשה', 'תעשה', 'תעשי', 'יעשה', 'תעשה', 'נעשה', 'תעשו', 'יעשו'],
        imperative=['עשה', 'עשי', 'עשו'],
    )


def _leshanot_rows(word_id):
    """לשנות — Pi'el lamed-he, root ש.נ.ה, binyan_id=3"""
    return _build_verb_rows(
        word_id=word_id,
        binyan_id=3,
        past=['שיניתי', 'שינית', 'שינית', 'שינה', 'שינתה', 'שינינו', 'שיניתם', 'שיניתן', 'שינו'],
        present=['משנה', 'משנה', 'משנים', 'משנות'],
        future=['אשנה', 'תשנה', 'תשני', 'ישנה', 'תשנה', 'נשנה', 'תשנו', 'ישנו'],
        imperative=['שנה', 'שני', 'שנו'],
    )


# ─── upgrade / downgrade ──────────────────────────────────────────────────────

def upgrade() -> None:
    conn = op.get_bind()

    # ── 1. Insert missing vocabulary words ────────────────────────────────────
    for hebrew, translation_ru, transliteration, pos, root, level_id, frequency_rank in MISSING_WORDS:
        existing = conn.execute(
            sa.text("SELECT id FROM words WHERE hebrew = :h AND pos = :p"),
            {"h": hebrew, "p": pos},
        ).fetchone()
        if existing is None:
            conn.execute(
                sa.text(
                    "INSERT INTO words "
                    "(hebrew, translation_ru, transliteration, pos, root, level_id, frequency_rank) "
                    "VALUES (:hebrew, :translation_ru, :transliteration, :pos, :root, :level_id, :frequency_rank)"
                ),
                {
                    "hebrew": hebrew,
                    "translation_ru": translation_ru,
                    "transliteration": transliteration,
                    "pos": pos,
                    "root": root,
                    "level_id": level_id,
                    "frequency_rank": frequency_rank,
                },
            )

    # ── 2. Generate adjective word forms ──────────────────────────────────────
    result = conn.execute(sa.text("SELECT id, hebrew FROM words WHERE pos = 'adj'"))
    adjectives = result.fetchall()

    all_adj_forms = []
    for row in adjectives:
        word_id, base = row[0], row[1]
        # Skip if forms already exist for this word
        existing_forms = conn.execute(
            sa.text("SELECT COUNT(*) FROM word_forms WHERE word_id = :wid"),
            {"wid": word_id},
        ).scalar()
        if existing_forms and existing_forms > 0:
            continue
        all_adj_forms.extend(generate_adjective_forms(word_id, base))

    if all_adj_forms:
        op.bulk_insert(word_forms_table, all_adj_forms)

    # ── 3a. Fix hollow-verb sofit letters appearing before suffixes ───────────
    # Sofit ם before past-tense suffixes
    conn.execute(sa.text(
        "UPDATE verb_conjugations "
        "SET form_he = regexp_replace(form_he, 'ם(תי|תם|תן|נו|ו|ה)$', 'מ\\1') "
        "WHERE form_he ~ 'ם(תי|תם|תן|נו|ו|ה)$'"
    ))
    # Sofit ן before past-tense suffixes
    conn.execute(sa.text(
        "UPDATE verb_conjugations "
        "SET form_he = regexp_replace(form_he, 'ן(תי|תם|תן|נו|ו|ה)$', 'נ\\1') "
        "WHERE form_he ~ 'ן(תי|תם|תן|נו|ו|ה)$'"
    ))
    # Sofit ם before ת (2fs past, fs present)
    conn.execute(sa.text(
        "UPDATE verb_conjugations "
        "SET form_he = REPLACE(form_he, 'םת', 'מת') "
        "WHERE form_he LIKE '%םת%'"
    ))
    # Sofit ן before ת
    conn.execute(sa.text(
        "UPDATE verb_conjugations "
        "SET form_he = REPLACE(form_he, 'ןת', 'נת') "
        "WHERE form_he LIKE '%ןת%'"
    ))
    # Sofit ן before נ
    conn.execute(sa.text(
        "UPDATE verb_conjugations "
        "SET form_he = REPLACE(form_he, 'ןנ', 'ננ') "
        "WHERE form_he LIKE '%ןנ%'"
    ))
    # Sofit ם before נ
    conn.execute(sa.text(
        "UPDATE verb_conjugations "
        "SET form_he = REPLACE(form_he, 'םנ', 'מנ') "
        "WHERE form_he LIKE '%םנ%'"
    ))

    # ── 3b. Replace conjugations for specific verbs with correct forms ─────────
    # Delete wrong conjugations for לקום, לגלות, לפרסם, לחכות
    conn.execute(sa.text(
        "DELETE FROM verb_conjugations WHERE word_id IN (377, 727, 943, 3023, 7620, 1947)"
    ))

    # Insert correct conjugations
    fixed_rows = LAQUM_ROWS + LGALOT_ROWS + LPARSEM_ROWS + LKHAKOT_ROWS
    if fixed_rows:
        op.bulk_insert(verb_conjugations_table, fixed_rows)

    # ── 3c. Add conjugations for the two new verbs ────────────────────────────
    # לעשות
    lasot_row = conn.execute(
        sa.text("SELECT id FROM words WHERE hebrew = 'לעשות' AND pos = 'verb'")
    ).fetchone()
    if lasot_row:
        lasot_id = lasot_row[0]
        existing = conn.execute(
            sa.text("SELECT COUNT(*) FROM verb_conjugations WHERE word_id = :wid"),
            {"wid": lasot_id},
        ).scalar()
        if not existing:
            op.bulk_insert(verb_conjugations_table, _lasot_rows(lasot_id))

    # לשנות
    leshanot_row = conn.execute(
        sa.text("SELECT id FROM words WHERE hebrew = 'לשנות' AND pos = 'verb'")
    ).fetchone()
    if leshanot_row:
        leshanot_id = leshanot_row[0]
        existing = conn.execute(
            sa.text("SELECT COUNT(*) FROM verb_conjugations WHERE word_id = :wid"),
            {"wid": leshanot_id},
        ).scalar()
        if not existing:
            op.bulk_insert(verb_conjugations_table, _leshanot_rows(leshanot_id))


def downgrade() -> None:
    conn = op.get_bind()

    # Remove conjugations added for the two new verbs
    for hebrew in ('לעשות', 'לשנות'):
        row = conn.execute(
            sa.text("SELECT id FROM words WHERE hebrew = :h AND pos = 'verb'"),
            {"h": hebrew},
        ).fetchone()
        if row:
            conn.execute(
                sa.text("DELETE FROM verb_conjugations WHERE word_id = :wid"),
                {"wid": row[0]},
            )

    # Remove word forms generated for adjectives (only the ones we inserted;
    # a safe approximation is to delete all word_forms for adjective word_ids)
    conn.execute(sa.text(
        "DELETE FROM word_forms "
        "WHERE word_id IN (SELECT id FROM words WHERE pos = 'adj')"
    ))

    # Remove inserted vocabulary words
    for hebrew, _translation_ru, _transliteration, pos, *_ in MISSING_WORDS:
        conn.execute(
            sa.text("DELETE FROM words WHERE hebrew = :h AND pos = :p"),
            {"h": hebrew, "p": pos},
        )

    # NOTE: The sofit-letter fixes (3a) and the conjugation replacements (3b)
    # are not reversed here because restoring the broken forms is not desirable.
    # If a full rollback is required, restore from a database backup.
