"""Add common vocabulary for news/journalism coverage.

Adds month names, common verbs, nouns, and other words frequently
found in Israeli news articles.

Revision ID: 162
Revises: 161
"""
from alembic import op
import sqlalchemy as sa

revision = "162"
down_revision = "161"

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

word_forms = sa.table(
    "word_forms",
    sa.column("word_id", sa.Integer),
    sa.column("hebrew", sa.String),
    sa.column("form_type", sa.String),
)

# (hebrew, translation_ru, transliteration, pos, root, level_id, frequency_rank)
NEW_WORDS = [
    # === Month names ===
    ("ינואר", "январь", "yanuar", "noun", None, 1, 2),
    ("פברואר", "февраль", "februar", "noun", None, 1, 2),
    ("מרץ", "март", "merts", "noun", None, 1, 2),
    ("אפריל", "апрель", "april", "noun", None, 1, 2),
    ("מאי", "май", "mai", "noun", None, 1, 2),
    ("יוני", "июнь", "yuni", "noun", None, 1, 2),
    ("יולי", "июль", "yuli", "noun", None, 1, 2),
    ("אוגוסט", "август", "ogust", "noun", None, 1, 2),
    ("ספטמבר", "сентябрь", "september", "noun", None, 1, 2),
    ("אוקטובר", "октябрь", "oktober", "noun", None, 1, 2),
    ("נובמבר", "ноябрь", "november", "noun", None, 1, 2),
    ("דצמבר", "декабрь", "detsember", "noun", None, 1, 2),

    # === Common verbs ===
    ("לעבור", "проходить, переходить", "la'avor", "verb", "ע.ב.ר", 1, 1),
    ("לאבד", "терять", "le'abed", "verb", "א.ב.ד", 2, 1),
    ("להציב", "ставить, размещать", "lehatsiv", "verb", "י.צ.ב", 3, 2),
    ("להתכוון", "иметь в виду, намереваться", "lehitkaven", "verb", "כ.ו.ן", 2, 1),
    ("להוביל", "вести, возглавлять", "lehovil", "verb", "י.ב.ל", 2, 1),
    ("להשיג", "достигать, получать", "lehasig", "verb", "נ.ש.ג", 3, 2),
    ("להפוך", "превращаться, переворачивать", "lehafokh", "verb", "ה.פ.כ", 2, 1),
    ("לנהל", "управлять, руководить", "lenahel", "verb", "נ.ה.ל", 2, 1),
    ("להחליט", "решать, принимать решение", "lehakhlit", "verb", "ח.ל.ט", 2, 1),
    ("לפתח", "развивать", "lefate'akh", "verb", "פ.ת.ח", 2, 1),
    ("להצליח", "преуспевать, удаваться", "lehatsli'akh", "verb", "צ.ל.ח", 2, 1),
    ("לנסות", "пытаться, пробовать", "lenasot", "verb", "נ.ס.ה", 2, 1),
    ("לחזור", "возвращаться", "lakhzor", "verb", "ח.ז.ר", 1, 1),
    ("לשמור", "хранить, беречь", "lishmor", "verb", "ש.מ.ר", 1, 1),
    ("להשתמש", "использовать", "lehishtamesh", "verb", "ש.מ.ש", 2, 1),
    ("לבחור", "выбирать", "livkhor", "verb", "ב.ח.ר", 2, 1),
    ("להרגיש", "чувствовать", "lehargish", "verb", "ר.ג.ש", 2, 1),
    ("לחשוב", "думать", "lakhshov", "verb", "ח.ש.ב", 1, 1),
    ("להסביר", "объяснять", "lehasbir", "verb", "ס.ב.ר", 2, 1),
    ("להצביע", "голосовать; указывать", "lehatsbi'a", "verb", "צ.ב.ע", 3, 2),
    ("להתחיל", "начинать", "lehatchil", "verb", "ח.ל.ל", 1, 1),
    ("לסיים", "заканчивать", "lesayem", "verb", "ס.י.מ", 2, 1),
    ("להכיר", "знать, узнавать", "lehakir", "verb", "נ.כ.ר", 2, 1),
    ("לקבל", "получать", "lekabel", "verb", "ק.ב.ל", 1, 1),
    ("לספר", "рассказывать", "lesaper", "verb", "ס.פ.ר", 1, 1),
    ("לעזור", "помогать", "la'azor", "verb", "ע.ז.ר", 1, 1),
    ("להגיע", "прибывать, достигать", "lehagi'a", "verb", "נ.ג.ע", 1, 1),
    ("לצאת", "выходить", "latset", "verb", "י.צ.א", 1, 1),
    ("למצוא", "находить", "limtso", "verb", "מ.צ.א", 1, 1),
    ("להביא", "приносить", "lehavi", "verb", "ב.ו.א", 1, 1),
    ("לשים", "ставить, класть", "lasim", "verb", "ש.י.מ", 1, 1),
    ("לפתוח", "открывать", "lifto'akh", "verb", "פ.ת.ח", 1, 1),
    ("לסגור", "закрывать", "lisgor", "verb", "ס.ג.ר", 1, 1),
    ("להישאר", "оставаться", "lehisha'er", "verb", "ש.א.ר", 2, 1),

    # === Common nouns ===
    ("מועמד", "кандидат", "mu'amad", "noun", "ע.מ.ד", 2, 1),
    ("ראשות", "руководство, главенство", "rashut", "noun", None, 3, 2),
    ("ריאליטי", "реалити (шоу)", "realiti", "noun", None, 3, 3),
    ("ממשלה", "правительство", "memshala", "noun", "מ.ש.ל", 2, 1),
    ("חברה", "общество; компания", "khevra", "noun", "ח.ב.ר", 1, 1),
    ("משפחה", "семья", "mishpakha", "noun", None, 1, 1),
    ("בעיה", "проблема", "be'aya", "noun", None, 1, 1),
    ("תוכנית", "программа, план", "tokhnit", "noun", None, 2, 1),
    ("הזדמנות", "возможность, шанс", "hizdamnut", "noun", None, 2, 1),
    ("השפעה", "влияние", "hashpa'a", "noun", None, 2, 1),
    ("תקופה", "период, эпоха", "tkufa", "noun", None, 2, 1),
    ("סיבה", "причина", "siba", "noun", None, 2, 1),
    ("תוצאה", "результат", "totsa'a", "noun", None, 2, 1),
    ("מצב", "ситуация, положение", "matsav", "noun", "י.צ.ב", 1, 1),
    ("שאלה", "вопрос", "she'ela", "noun", "ש.א.ל", 1, 1),
    ("תשובה", "ответ", "tshuva", "noun", "ש.ו.ב", 1, 1),
    ("רחוב", "улица", "rekhov", "noun", None, 1, 1),
    ("חדש", "новый", "khadash", "adj", "ח.ד.ש", 1, 1),
    ("ישן", "старый", "yashan", "adj", None, 1, 1),
    ("גדול", "большой", "gadol", "adj", None, 1, 1),
    ("קטן", "маленький", "katan", "adj", None, 1, 1),
    ("חזק", "сильный", "khazak", "adj", "ח.ז.ק", 1, 1),
    ("חשוב", "важный", "khashuv", "adj", "ח.ש.ב", 1, 1),
    ("שונה", "другой, различный", "shone", "adj", "ש.נ.ה", 1, 1),
    ("ראשון", "первый", "rishon", "adj", None, 1, 1),
    ("אחרון", "последний", "akharon", "adj", "א.ח.ר", 1, 1),
    ("רב", "многочисленный; раввин", "rav", "adj", None, 1, 1),
    ("ציבורי", "общественный, публичный", "tsiburi", "adj", None, 2, 1),
    ("פוליטי", "политический", "politi", "adj", None, 2, 2),
    ("כלכלי", "экономический", "kalkali", "adj", None, 2, 2),

    # === Adverbs / particles ===
    ("במפתיע", "неожиданно, врасплох", "bemafti'a", "adv", None, 3, 2),
    ("לפחות", "по крайней мере", "lefakhot", "adv", None, 2, 1),
    ("בערך", "приблизительно", "be'erekh", "adv", None, 2, 1),
    ("אולי", "может быть", "ulai", "adv", None, 1, 1),
    ("בכלל", "вообще", "bikhlal", "adv", None, 1, 1),
    ("לגמרי", "совершенно, полностью", "legamrei", "adv", None, 2, 1),
    ("כנראה", "по-видимому, вероятно", "kanir'e", "adv", None, 2, 1),
    ("דווקא", "именно, как раз", "davka", "adv", None, 2, 1),
    ("הנה", "вот", "hine", "part", None, 1, 1),
    ("לא", "нет, не", "lo", "part", None, 1, 1),
    ("כן", "да", "ken", "part", None, 1, 1),
    ("בסדר", "хорошо, в порядке", "beseder", "adv", None, 1, 1),
    ("ביחד", "вместе", "beyakhad", "adv", None, 1, 1),
    ("לבד", "один, в одиночку", "levad", "adv", None, 1, 1),
    ("הרבה", "много", "harbe", "adv", None, 1, 1),
    ("קצת", "немного", "ktsat", "adv", None, 1, 1),
    ("תמיד", "всегда", "tamid", "adv", None, 1, 1),
    ("אף פעם", "никогда", "af pa'am", "adv", None, 1, 1),
    ("לפעמים", "иногда", "lif'amim", "adv", None, 1, 1),
    ("היום", "сегодня", "hayom", "adv", None, 1, 1),
    ("אתמול", "вчера", "etmol", "adv", None, 1, 1),
    ("מחר", "завтра", "makhar", "adv", None, 1, 1),
    ("עכשיו", "сейчас", "akhshav", "adv", None, 1, 1),
    ("פתאום", "вдруг", "pit'om", "adv", None, 2, 1),
    ("בדיוק", "точно, именно", "bediyuk", "adv", None, 1, 1),
    ("בטח", "конечно, наверняка", "betakh", "adv", None, 1, 1),

    # === Prepositions / conjunctions ===
    ("בזמן", "во время", "bizman", "prep", None, 2, 2),
    ("לפי", "по, согласно", "lefi", "prep", None, 2, 1),
    ("בשביל", "для, ради", "bishvil", "prep", None, 1, 1),
    ("נגד", "против", "neged", "prep", None, 2, 1),
    ("דרך", "через, по", "derekh", "prep", None, 1, 1),
    ("בלי", "без", "bli", "prep", None, 1, 1),
    ("למרות", "несмотря на", "lamrot", "adv", None, 2, 1),
    ("אלא", "а, но (после отрицания)", "ela", "conj", None, 2, 1),
    ("כלומר", "то есть", "klomar", "conj", None, 3, 2),
    ("אילו", "если бы", "ilu", "conj", None, 3, 2),
    ("כאשר", "когда", "ka'asher", "conj", None, 2, 1),
    ("כדי", "чтобы", "kedei", "conj", None, 1, 1),
]


def upgrade() -> None:
    conn = op.get_bind()

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


def downgrade() -> None:
    conn = op.get_bind()
    for w in NEW_WORDS:
        conn.execute(
            sa.text("DELETE FROM words WHERE hebrew = :h AND translation_ru = :t"),
            {"h": w[0], "t": w[1]},
        )
