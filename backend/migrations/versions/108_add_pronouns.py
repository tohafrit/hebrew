"""Add comprehensive Hebrew pronouns to dictionary.

Only 2 pronouns existed (מי, מה). This adds personal pronouns,
demonstratives, possessives, reflexives, interrogatives, and indefinites.

Revision ID: 108
Revises: 107
"""

from alembic import op
import sqlalchemy as sa

revision = "108"
down_revision = "107"
branch_labels = None
depends_on = None


def upgrade():
    words_table = sa.table(
        "words",
        sa.column("hebrew", sa.String),
        sa.column("nikkud", sa.String),
        sa.column("transliteration", sa.String),
        sa.column("translation_ru", sa.String),
        sa.column("pos", sa.String),
        sa.column("gender", sa.String),
        sa.column("number", sa.String),
        sa.column("frequency_rank", sa.Integer),
        sa.column("level_id", sa.Integer),
    )

    pronouns = [
        # === Personal pronouns (L1, freq 1) ===
        ("אני", "אֲנִי", "ани", "я", "pron", None, "sg", 1, 1),
        ("אתה", "אַתָּה", "ата", "ты (м.)", "pron", "m", "sg", 1, 1),
        ("את", "אַתְּ", "ат", "ты (ж.)", "pron", "f", "sg", 1, 1),
        ("הוא", "הוּא", "ху", "он", "pron", "m", "sg", 1, 1),
        ("היא", "הִיא", "хи", "она", "pron", "f", "sg", 1, 1),
        ("אנחנו", "אֲנַחְנוּ", "анахну", "мы", "pron", None, "pl", 1, 1),
        ("אתם", "אַתֶּם", "атем", "вы (м.)", "pron", "m", "pl", 1, 1),
        ("אתן", "אַתֶּן", "атен", "вы (ж.)", "pron", "f", "pl", 1, 1),
        ("הם", "הֵם", "хем", "они (м.)", "pron", "m", "pl", 1, 1),
        ("הן", "הֵן", "хен", "они (ж.)", "pron", "f", "pl", 1, 1),

        # === Demonstrative pronouns (L1, freq 1) ===
        ("זה", "זֶה", "зэ", "это; этот", "pron", "m", "sg", 1, 1),
        ("זאת", "זֹאת", "зот", "это; эта", "pron", "f", "sg", 1, 1),
        ("אלה", "אֵלֶּה", "элэ", "эти", "pron", None, "pl", 1, 1),

        # === Interrogative pronouns (already have מי, מה) ===
        ("איזה", "אֵיזֶה", "эйзэ", "какой; который", "pron", "m", "sg", 1, 1),
        ("איזו", "אֵיזוֹ", "эйзо", "какая; которая", "pron", "f", "sg", 1, 1),
        ("אילו", "אֵילוּ", "эйлу", "какие; которые", "pron", None, "pl", 2, 2),

        # === Indefinite pronouns (L1-L2, freq 1-2) ===
        ("משהו", "מַשֶּׁהוּ", "машэху", "что-то", "pron", None, "sg", 1, 1),
        ("מישהו", "מִישֶׁהוּ", "мишэху", "кто-то", "pron", None, "sg", 1, 1),
        ("כלום", "כְּלוּם", "клум", "ничего", "pron", None, "sg", 1, 1),
        ("אף אחד", "אַף אֶחָד", "аф эхад", "никто", "pron", None, "sg", 1, 2),
        ("כל אחד", "כׇּל אֶחָד", "коль эхад", "каждый; любой", "pron", None, "sg", 1, 2),
        ("כולם", "כֻּלָּם", "кулам", "все (м.)", "pron", "m", "pl", 1, 1),
        ("כולן", "כֻּלָּן", "кулан", "все (ж.)", "pron", "f", "pl", 2, 2),
        ("כולנו", "כֻּלָּנוּ", "кулану", "мы все", "pron", None, "pl", 1, 2),

        # === Possessive pronouns (L1-L2) ===
        ("שלי", "שֶׁלִּי", "шели", "мой/моя/моё", "pron", None, None, 1, 1),
        ("שלך", "שֶׁלְּךָ", "шелха", "твой (м.)", "pron", "m", None, 1, 1),
        ("שלך", "שֶׁלָּךְ", "шелах", "твой (ж.)", "pron", "f", None, 1, 1),
        ("שלו", "שֶׁלּוֹ", "шело", "его", "pron", "m", None, 1, 1),
        ("שלה", "שֶׁלָּהּ", "шела", "её", "pron", "f", None, 1, 1),
        ("שלנו", "שֶׁלָּנוּ", "шелану", "наш", "pron", None, None, 1, 1),
        ("שלכם", "שֶׁלָּכֶם", "шелахем", "ваш (м.)", "pron", "m", None, 1, 2),
        ("שלכן", "שֶׁלָּכֶן", "шелахен", "ваш (ж.)", "pron", "f", None, 2, 2),
        ("שלהם", "שֶׁלָּהֶם", "шелахем", "их (м.)", "pron", "m", None, 1, 2),
        ("שלהן", "שֶׁלָּהֶן", "шелахен", "их (ж.)", "pron", "f", None, 2, 2),

        # === Reflexive/emphatic (L2-L3) ===
        ("עצמי", "עַצְמִי", "ацми", "сам (я сам)", "pron", None, "sg", 2, 2),
        ("עצמך", "עַצְמְךָ", "ацмеха", "сам (ты сам, м.)", "pron", "m", "sg", 2, 2),
        ("עצמך", "עַצְמֵךְ", "ацмех", "сама (ты сама)", "pron", "f", "sg", 2, 2),
        ("עצמו", "עַצְמוֹ", "ацмо", "сам (он сам)", "pron", "m", "sg", 1, 2),
        ("עצמה", "עַצְמָהּ", "ацма", "сама (она сама)", "pron", "f", "sg", 1, 2),
        ("עצמנו", "עַצְמֵנוּ", "ацмену", "сами (мы сами)", "pron", None, "pl", 2, 2),
        ("עצמם", "עַצְמָם", "ацмам", "сами (они сами, м.)", "pron", "m", "pl", 2, 3),
        ("עצמן", "עַצְמָן", "ацман", "сами (они сами, ж.)", "pron", "f", "pl", 3, 3),

        # === Other common pronouns (L2-L3) ===
        ("כזה", "כָּזֶה", "казэ", "такой", "pron", "m", "sg", 1, 2),
        ("כזאת", "כָּזֹאת", "казот", "такая", "pron", "f", "sg", 1, 2),
        ("אותו", "אוֹתוֹ", "ото", "его; тот самый", "pron", "m", "sg", 1, 2),
        ("אותה", "אוֹתָהּ", "ота", "её; ту самую", "pron", "f", "sg", 1, 2),
        ("אותם", "אוֹתָם", "отам", "их (м.); тех самых", "pron", "m", "pl", 1, 2),
        ("אותן", "אוֹתָן", "отан", "их (ж.); тех самых", "pron", "f", "pl", 2, 3),
        ("שם", "שָׁם", "шам", "там", "pron", None, None, 1, 1),
        ("פה", "פֹּה", "по", "здесь, тут", "pron", None, None, 1, 1),
        ("כאן", "כָּאן", "кан", "здесь", "pron", None, None, 1, 1),
    ]

    op.bulk_insert(
        words_table,
        [
            {
                "hebrew": p[0],
                "nikkud": p[1],
                "transliteration": p[2],
                "translation_ru": p[3],
                "pos": p[4],
                "gender": p[5],
                "number": p[6],
                "frequency_rank": p[7],
                "level_id": p[8],
            }
            for p in pronouns
        ],
    )


def downgrade():
    op.execute(
        "DELETE FROM words WHERE pos = 'pron' AND id > 8066"
    )
