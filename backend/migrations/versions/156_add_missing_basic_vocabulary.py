"""Add missing basic vocabulary — function words, pronouns, common words.

These are essential words that appear in nearly every Hebrew text but
were missing from the dictionary, causing the reader to show gaps.

Revision ID: 156
Revises: 155
"""
from alembic import op
import sqlalchemy as sa

revision = "156"
down_revision = "155"

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


# (hebrew, translation_ru, transliteration, pos, root, level_id, frequency_rank)
BASIC_WORDS = [
    # === Preposition + pronoun suffix forms (ל + pronoun) ===
    ("לי", "мне", "li", "pron", None, 1, 1),
    ("לך", "тебе", "lekha", "pron", None, 1, 1),
    ("לו", "ему", "lo", "pron", None, 1, 1),
    ("לה", "ей", "la", "pron", None, 1, 1),
    ("לנו", "нам", "lanu", "pron", None, 1, 1),
    ("לכם", "вам (м.)", "lakhem", "pron", None, 1, 1),
    ("להם", "им (м.)", "lahem", "pron", None, 1, 1),
    ("להן", "им (ж.)", "lahen", "pron", None, 2, 1),

    # === Direct object pronoun forms (את + pronoun) ===
    ("אותי", "меня", "oti", "pron", None, 1, 1),
    ("אותך", "тебя", "otkha", "pron", None, 1, 1),
    ("אותנו", "нас", "otanu", "pron", None, 1, 1),
    ("אתכם", "вас", "etkhem", "pron", None, 2, 1),

    # === Demonstratives ===
    ("זו", "это; эта", "zo", "pron", None, 1, 1),
    ("אלו", "эти; те", "elu", "pron", None, 2, 1),

    # === Essential function words ===
    ("כל", "каждый; весь, всё", "kol", "det", None, 1, 1),
    ("גם", "тоже, также", "gam", "adv", None, 1, 1),
    ("אם", "если", "im", "conj", None, 1, 1),
    ("או", "или", "o", "conj", None, 1, 1),
    ("רק", "только", "rak", "adv", None, 1, 1),
    ("כבר", "уже", "kvar", "adv", None, 1, 1),
    ("ממש", "действительно; прямо", "mamash", "adv", None, 2, 1),
    ("כמו", "как, подобно", "kmo", "prep", None, 1, 1),
    ("יותר", "больше, более", "yoter", "adv", None, 1, 1),
    ("פחות", "меньше, менее", "pakhot", "adv", None, 1, 1),
    ("שוב", "снова, опять", "shuv", "adv", None, 1, 1),
    ("באמת", "действительно, правда", "be'emet", "adv", None, 1, 1),
    ("ביותר", "самый, наиболее", "beyoter", "adv", None, 2, 2),
    ("בזמן", "во время", "bizman", "prep", None, 2, 2),
    ("האם", "ли (вопросительная частица)", "ha'im", "part", None, 2, 1),

    # === Prepositions ===
    ("כנגד", "против, напротив", "kneged", "prep", None, 3, 2),
    ("תחת", "под", "takhat", "prep", None, 2, 2),

    # === Existential particles ===
    ("יש", "есть, имеется", "yesh", "part", None, 1, 1),
    ("אין", "нет, не имеется", "ein", "part", None, 1, 1),

    # === Time words ===
    ("אז", "тогда", "az", "adv", None, 1, 1),

    # === Common nouns ===
    ("חיים", "жизнь", "khaim", "noun", None, 1, 1),
    ("אוכל", "еда, пища", "okhel", "noun", "א.כ.ל", 1, 1),
    ("מוסיקה", "музыка", "musika", "noun", None, 1, 1),

    # === kol- forms ===
    ("כולם", "все (они)", "kulam", "pron", None, 1, 1),
    ("כולו", "весь (он)", "kulo", "pron", None, 2, 1),
    ("כולה", "вся (она)", "kula", "pron", None, 2, 1),

    # === Places ===
    ("ישראל", "Израиль", "yisrael", "propn", None, 1, 1),
    ("תל", "холм (в назв. «Тель-Авив»)", "tel", "propn", None, 2, 2),

    # === Adjectives ===
    ("צעיר", "молодой", "tsa'ir", "adj", None, 1, 1),
    ("נחמד", "приятный, милый", "nekhmad", "adj", "ח.מ.ד", 1, 1),
]


def upgrade() -> None:
    op.bulk_insert(
        words,
        [
            {
                "hebrew": w[0],
                "translation_ru": w[1],
                "transliteration": w[2],
                "pos": w[3],
                "root": w[4],
                "level_id": w[5],
                "frequency_rank": w[6],
            }
            for w in BASIC_WORDS
        ],
    )


def downgrade() -> None:
    for w in BASIC_WORDS:
        op.execute(
            sa.text("DELETE FROM words WHERE hebrew = :h AND translation_ru = :t"),
            {"h": w[0], "t": w[1]},
        )
