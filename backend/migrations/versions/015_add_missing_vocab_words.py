"""Add missing common vocabulary words used in reading texts.

Words like אולפן, תלמידים, מילים, חברים, שיעורים are referenced
in reading text vocabulary but were missing from the dictionary.

Revision ID: 015
Revises: 014
"""

from alembic import op
from sqlalchemy import text

revision = "015"
down_revision = "014"
branch_labels = None
depends_on = None


WORDS = [
    # (hebrew, nikkud, transliteration, translation_ru, pos, level_id, frequency_rank)
    ("אולפן", "אוּלְפָּן", "ulpan", "ульпан (школа иврита)", "noun", 1, 2),
    ("תלמידים", "תַּלְמִידִים", "talmidim", "ученики", "noun", 1, 2),
    ("מילים", "מִלִּים", "milim", "слова", "noun", 1, 1),
    ("חברים", "חֲבֵרִים", "xaverim", "друзья", "noun", 1, 1),
    ("שיעורים", "שִׁיעוּרִים", "shiurim", "уроки, занятия", "noun", 1, 2),
    ("ירקות", "יְרָקוֹת", "yerakot", "овощи", "noun", 1, 2),
    ("פירות", "פֵּרוֹת", "perot", "фрукты", "noun", 1, 2),
    ("תבלינים", "תְּבָלִינִים", "tavlinim", "специи", "noun", 2, 3),
    ("גבינה", "גְּבִינָה", "gvina", "сыр", "noun", 1, 2),
    ("דירה", "דִּירָה", "dira", "квартира", "noun", 1, 1),
    ("חתול", "חָתוּל", "xatul", "кот", "noun", 1, 2),
    ("כדורגל", "כַּדּוּרֶגֶל", "kaduregel", "футбол", "noun", 1, 2),
    ("נכדים", "נְכָדִים", "nexadim", "внуки", "noun", 2, 3),
    ("רשימה", "רְשִׁימָה", "reshima", "список", "noun", 2, 2),
    ("קניות", "קְנִיּוֹת", "kniyot", "покупки", "noun", 2, 2),
    ("מחלקה", "מַחְלָקָה", "maxlaka", "отдел", "noun", 2, 2),
    ("תור", "תּוֹר", "tor", "очередь", "noun", 2, 2),
    ("שקית", "שְׁקִית", "skit", "пакет, сумка", "noun", 2, 3),
]


def upgrade() -> None:
    conn = op.get_bind()
    # Fix sequence counter first
    conn.execute(text("SELECT setval('words_id_seq', (SELECT COALESCE(MAX(id), 0) + 1 FROM words), false)"))

    for hebrew, nikkud, translit, translation_ru, pos, level_id, freq in WORDS:
        conn.execute(
            text("""
                INSERT INTO words (hebrew, nikkud, transliteration, translation_ru, pos, level_id, frequency_rank)
                SELECT :hebrew, :nikkud, :translit, :translation_ru, :pos, :level_id, :freq
                WHERE NOT EXISTS (
                    SELECT 1 FROM words WHERE hebrew = :hebrew AND pos = :pos
                )
            """),
            {"hebrew": hebrew, "nikkud": nikkud, "translit": translit,
             "translation_ru": translation_ru, "pos": pos,
             "level_id": level_id, "freq": freq},
        )


def downgrade() -> None:
    conn = op.get_bind()
    for hebrew, nikkud, translit, translation_ru, pos, level_id, freq in WORDS:
        conn.execute(
            text("DELETE FROM words WHERE hebrew = :hebrew AND translation_ru = :tr AND pos = :pos AND id > 31688"),
            {"hebrew": hebrew, "tr": translation_ru, "pos": pos},
        )
