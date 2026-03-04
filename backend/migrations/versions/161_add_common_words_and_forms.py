"""Add missing common words and word forms for better reader coverage.

Adds: של, יכול, לשקוע, לשרור + variant spelling word_forms.

Revision ID: 161
Revises: 160
"""
from alembic import op
import sqlalchemy as sa

revision = "161"
down_revision = "160"

words = sa.table(
    "words",
    sa.column("hebrew", sa.String),
    sa.column("translation_ru", sa.String),
    sa.column("transliteration", sa.String),
    sa.column("pos", sa.String),
    sa.column("root", sa.String),
    sa.column("level_id", sa.Integer),
    sa.column("frequency_rank", sa.Integer),
)

word_forms = sa.table(
    "word_forms",
    sa.column("word_id", sa.Integer),
    sa.column("hebrew", sa.String),
    sa.column("form_type", sa.String),
)

verb_conjugations = sa.table(
    "verb_conjugations",
    sa.column("word_id", sa.Integer),
    sa.column("binyan_id", sa.Integer),
    sa.column("tense", sa.String),
    sa.column("person", sa.String),
    sa.column("gender", sa.String),
    sa.column("number", sa.String),
    sa.column("form_he", sa.String),
)

# (hebrew, translation_ru, transliteration, pos, root, level_id, frequency_rank)
NEW_WORDS = [
    ("של", "принадлежащий; (предлог родительного падежа)", "shel", "prep", None, 1, 1),
    ("יכול", "может, способен", "yakhol", "adj", "י.כ.ל", 1, 1),
    ("לשקוע", "погружаться; заходить (о солнце)", "lishko'a", "verb", "ש.ק.ע", 3, 2),
    ("לשרור", "царить, господствовать", "lisror", "verb", "ש.ר.ר", 4, 3),
    ("אחד", "один", "ekhad", "num", None, 1, 1),
    ("שנים", "два (м.); годы", "shnaim", "num", None, 1, 1),
    ("מאוד", "очень", "me'od", "adv", None, 1, 1),
    ("עוד", "ещё", "od", "adv", None, 1, 1),
    ("כי", "потому что; что", "ki", "conj", None, 1, 1),
    ("אבל", "но, однако", "aval", "conj", None, 1, 1),
    ("אחרי", "после, за", "akharei", "prep", None, 1, 1),
    ("בין", "между", "bein", "prep", None, 1, 1),
    ("עד", "до", "ad", "prep", None, 1, 1),
    ("פה", "здесь; рот", "po", "adv", None, 1, 1),
    ("שם", "там; имя", "sham", "adv", None, 1, 1),
    ("כמה", "сколько; несколько", "kama", "adv", None, 1, 1),
    ("למה", "почему; зачем", "lama", "adv", None, 1, 1),
    ("איפה", "где", "eifo", "adv", None, 1, 1),
    ("מתי", "когда", "matai", "adv", None, 1, 1),
    ("איך", "как", "eikh", "adv", None, 1, 1),
    ("מי", "кто", "mi", "pron", None, 1, 1),
    ("מה", "что", "ma", "pron", None, 1, 1),
    ("בגלל", "из-за", "biglal", "prep", None, 1, 1),
    ("לפני", "перед, до", "lifnei", "prep", None, 1, 1),
    ("אצל", "у, возле (кого-л.)", "etsel", "prep", None, 2, 2),
    ("דרך", "путь, дорога; через", "derekh", "noun", "ד.ר.כ", 1, 1),
    ("חלק", "часть; гладкий", "khelek", "noun", "ח.ל.ק", 1, 1),
    ("מקום", "место", "makom", "noun", None, 1, 1),
    ("דבר", "вещь, предмет; слово", "davar", "noun", "ד.ב.ר", 1, 1),
    ("אדם", "человек", "adam", "noun", None, 1, 1),
    ("עולם", "мир, вселенная", "olam", "noun", None, 1, 1),
    ("ראש", "голова", "rosh", "noun", None, 1, 1),
    ("יד", "рука", "yad", "noun", None, 1, 1),
    ("עין", "глаз", "ayin", "noun", None, 1, 1),
    ("לב", "сердце", "lev", "noun", None, 1, 1),
    ("פנים", "лицо", "panim", "noun", None, 1, 1),
    ("בית", "дом", "bait", "noun", None, 1, 1),
    ("אחר", "другой, иной", "akher", "adj", "א.ח.ר", 1, 1),
    ("כך", "так, таким образом", "kakh", "adv", None, 1, 1),
    ("חיפה", "Хайфа", "kheifa", "propn", None, 1, 1),

    # === Prepositional pronoun forms (ב + pronoun) ===
    ("בו", "в нём", "bo", "pron", None, 1, 1),
    ("בה", "в ней", "ba", "pron", None, 1, 1),
    ("בי", "во мне", "bi", "pron", None, 1, 1),
    ("בנו", "в нас", "banu", "pron", None, 1, 1),
    ("בהם", "в них (м.)", "bahem", "pron", None, 1, 1),
    ("בהן", "в них (ж.)", "bahen", "pron", None, 2, 1),

    # === על + pronoun ===
    ("עליו", "на нём", "alav", "pron", None, 1, 1),
    ("עליה", "на ней", "aleha", "pron", None, 1, 1),
    ("עלינו", "на нас", "aleinu", "pron", None, 1, 1),
    ("עליהם", "на них (м.)", "aleihem", "pron", None, 1, 1),

    # === מן + pronoun ===
    ("ממנו", "от него; от нас", "mimenu", "pron", None, 1, 1),
    ("ממנה", "от неё", "mimena", "pron", None, 1, 1),

    # === אל + pronoun ===
    ("אליו", "к нему", "elav", "pron", None, 1, 1),
    ("אליה", "к ней", "eleha", "pron", None, 1, 1),
    ("אלינו", "к нам", "eleinu", "pron", None, 1, 1),
    ("אליהם", "к ним", "aleihem", "pron", None, 1, 1),

    # === של + pronoun (possessives) ===
    ("שלו", "его (принадлежность)", "shelo", "pron", None, 1, 1),
    ("שלה", "её (принадлежность)", "shela", "pron", None, 1, 1),
    ("שלי", "мой/моя", "sheli", "pron", None, 1, 1),
    ("שלנו", "наш/наша", "shelanu", "pron", None, 1, 1),
    ("שלהם", "их (м.)", "shelahem", "pron", None, 1, 1),
    ("שלכם", "ваш (м.)", "shelakhem", "pron", None, 1, 1),

    # === עם/את + pronoun ===
    ("איתו", "с ним", "ito", "pron", None, 1, 1),
    ("איתה", "с ней", "ita", "pron", None, 1, 1),
    ("איתי", "со мной", "iti", "pron", None, 1, 1),
    ("איתנו", "с нами", "itanu", "pron", None, 1, 1),

    # === Missing common adjectives ===
    ("טעים", "вкусный", "ta'im", "adj", "ט.ע.מ", 1, 1),
]

# Word forms for variant spellings and common inflections
# (form_hebrew, base_hebrew, form_type)
WORD_FORMS = [
    # Variant plene spellings
    ("שמיים", "שמים", "variant"),   # sky — double-yod variant
    # יכול inflections
    ("יכולה", "יכול", "fs"),
    ("יכולים", "יכול", "mp"),
    ("יכולות", "יכול", "fp"),
    # אחר inflections
    ("אחרת", "אחר", "fs"),
    ("אחרים", "אחר", "mp"),
    ("אחרות", "אחר", "fp"),
    # Irregular plurals
    ("חנויות", "חנות", "fp"),
    # טעים inflections
    ("טעימה", "טעים", "fs"),
    ("טעימים", "טעים", "mp"),
    ("טעימות", "טעים", "fp"),
]


def _row(word_id, binyan, tense, person, gender, number, form):
    return {
        "word_id": word_id, "binyan_id": binyan,
        "tense": tense, "person": person,
        "gender": gender, "number": number, "form_he": form,
    }


def upgrade() -> None:
    conn = op.get_bind()

    # --- Insert missing words (skip if already exists) ---
    for w in NEW_WORDS:
        exists = conn.execute(
            sa.text("SELECT id FROM words WHERE hebrew = :h LIMIT 1"),
            {"h": w[0]},
        ).fetchone()
        if not exists:
            conn.execute(
                words.insert().values(
                    hebrew=w[0], translation_ru=w[1], transliteration=w[2],
                    pos=w[3], root=w[4], level_id=w[5], frequency_rank=w[6],
                )
            )

    # --- Insert word forms ---
    for form_he, base_he, form_type in WORD_FORMS:
        row = conn.execute(
            sa.text("SELECT id FROM words WHERE hebrew = :h ORDER BY level_id ASC NULLS LAST LIMIT 1"),
            {"h": base_he},
        ).fetchone()
        if row:
            exists = conn.execute(
                sa.text("SELECT id FROM word_forms WHERE word_id = :wid AND hebrew = :h LIMIT 1"),
                {"wid": row[0], "h": form_he},
            ).fetchone()
            if not exists:
                conn.execute(
                    word_forms.insert().values(
                        word_id=row[0], hebrew=form_he, form_type=form_type,
                    )
                )

    # --- Generate conjugations for לשקוע (Pa'al, root ש.ק.ע) ---
    row = conn.execute(
        sa.text("SELECT id FROM words WHERE hebrew = 'לשקוע' LIMIT 1")
    ).fetchone()
    if row:
        wid = row[0]
        # Check if conjugations already exist
        cnt = conn.execute(
            sa.text("SELECT count(*) FROM verb_conjugations WHERE word_id = :wid"),
            {"wid": wid},
        ).scalar()
        if cnt == 0:
            R = lambda t, pe, g, n, f: _row(wid, 1, t, pe, g, n, f)
            conj = [
                # Past
                R("past", "1", "m", "s", "שקעתי"),
                R("past", "2", "m", "s", "שקעת"),
                R("past", "2", "f", "s", "שקעת"),
                R("past", "3", "m", "s", "שקע"),
                R("past", "3", "f", "s", "שקעה"),
                R("past", "1", "m", "p", "שקענו"),
                R("past", "2", "m", "p", "שקעתם"),
                R("past", "2", "f", "p", "שקעתן"),
                R("past", "3", "m", "p", "שקעו"),
                # Present
                R("present", "0", "m", "s", "שוקע"),
                R("present", "0", "f", "s", "שוקעת"),
                R("present", "0", "m", "p", "שוקעים"),
                R("present", "0", "f", "p", "שוקעות"),
                # Future
                R("future", "1", "m", "s", "אשקע"),
                R("future", "2", "m", "s", "תשקע"),
                R("future", "2", "f", "s", "תשקעי"),
                R("future", "3", "m", "s", "ישקע"),
                R("future", "3", "f", "s", "תשקע"),
                R("future", "1", "m", "p", "נשקע"),
                R("future", "2", "m", "p", "תשקעו"),
                R("future", "3", "m", "p", "ישקעו"),
            ]
            op.bulk_insert(verb_conjugations, conj)

    # --- Generate conjugations for לשרור (Pa'al, root ש.ר.ר) ---
    row = conn.execute(
        sa.text("SELECT id FROM words WHERE hebrew = 'לשרור' LIMIT 1")
    ).fetchone()
    if row:
        wid = row[0]
        cnt = conn.execute(
            sa.text("SELECT count(*) FROM verb_conjugations WHERE word_id = :wid"),
            {"wid": wid},
        ).scalar()
        if cnt == 0:
            R = lambda t, pe, g, n, f: _row(wid, 1, t, pe, g, n, f)
            conj = [
                # Past
                R("past", "3", "m", "s", "שרר"),
                R("past", "3", "f", "s", "שררה"),
                R("past", "3", "m", "p", "שררו"),
                # Present
                R("present", "0", "m", "s", "שורר"),
                R("present", "0", "f", "s", "שוררת"),
                R("present", "0", "m", "p", "שוררים"),
                R("present", "0", "f", "p", "שוררות"),
            ]
            op.bulk_insert(verb_conjugations, conj)

    # --- Fix lamed-he verb conjugations (e.g., לשחות — swim) ---
    row = conn.execute(
        sa.text("SELECT id FROM words WHERE hebrew = 'לשחות' AND pos = 'verb' LIMIT 1")
    ).fetchone()
    if row:
        wid = row[0]
        # Fix wrong present tense forms (שוחי→שוחה, שוחיים→שוחים, etc.)
        for old, new in [("שוחי", "שוחה"), ("שוחית", "שוחה"), ("שוחיים", "שוחים"), ("שוחיות", "שוחות")]:
            conn.execute(
                sa.text("UPDATE verb_conjugations SET form_he = :new WHERE word_id = :wid AND form_he = :old"),
                {"wid": wid, "new": new, "old": old},
            )

    # --- Add Huf'al passive forms as word_forms for common verbs ---
    # הוקמה (was established) → לקום
    row = conn.execute(
        sa.text("SELECT id FROM words WHERE hebrew = 'לקום' LIMIT 1")
    ).fetchone()
    if row:
        for form_he, ftype in [
            ("הוקם", "hufal_past_3ms"), ("הוקמה", "hufal_past_3fs"),
            ("הוקמו", "hufal_past_3p"), ("מוקם", "hufal_present_ms"),
        ]:
            exists = conn.execute(
                sa.text("SELECT id FROM word_forms WHERE word_id = :wid AND hebrew = :h LIMIT 1"),
                {"wid": row[0], "h": form_he},
            ).fetchone()
            if not exists:
                conn.execute(
                    word_forms.insert().values(word_id=row[0], hebrew=form_he, form_type=ftype)
                )

    # נצבעו (were painted) → לצבוע
    row = conn.execute(
        sa.text("SELECT id FROM words WHERE hebrew = 'לצבוע' LIMIT 1")
    ).fetchone()
    if row:
        for form_he, ftype in [
            ("נצבע", "nifal_past_3ms"), ("נצבעה", "nifal_past_3fs"),
            ("נצבעו", "nifal_past_3p"), ("נצבעים", "nifal_present_mp"),
        ]:
            exists = conn.execute(
                sa.text("SELECT id FROM word_forms WHERE word_id = :wid AND hebrew = :h LIMIT 1"),
                {"wid": row[0], "h": form_he},
            ).fetchone()
            if not exists:
                conn.execute(
                    word_forms.insert().values(word_id=row[0], hebrew=form_he, form_type=ftype)
                )

    # השתרר (Hitpa'el of שרר) → לשרור
    row = conn.execute(
        sa.text("SELECT id FROM words WHERE hebrew = 'לשרור' LIMIT 1")
    ).fetchone()
    if row:
        for form_he, ftype in [
            ("השתרר", "hitpael_past_3ms"), ("השתררה", "hitpael_past_3fs"),
            ("השתררו", "hitpael_past_3p"), ("משתרר", "hitpael_present_ms"),
        ]:
            exists = conn.execute(
                sa.text("SELECT id FROM word_forms WHERE word_id = :wid AND hebrew = :h LIMIT 1"),
                {"wid": row[0], "h": form_he},
            ).fetchone()
            if not exists:
                conn.execute(
                    word_forms.insert().values(word_id=row[0], hebrew=form_he, form_type=ftype)
                )


def downgrade() -> None:
    conn = op.get_bind()
    for w in NEW_WORDS:
        conn.execute(
            sa.text("DELETE FROM words WHERE hebrew = :h AND translation_ru = :t"),
            {"h": w[0], "t": w[1]},
        )
    for form_he, base_he, _ in WORD_FORMS:
        conn.execute(
            sa.text("""
                DELETE FROM word_forms WHERE hebrew = :fh
                AND word_id = (SELECT id FROM words WHERE hebrew = :bh LIMIT 1)
            """),
            {"fh": form_he, "bh": base_he},
        )
