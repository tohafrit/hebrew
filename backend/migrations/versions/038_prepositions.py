"""Populate prepositions table with Hebrew prepositions and pronominal suffix declensions.

Revision ID: 038
Revises: 037
"""

import json

from alembic import op
import sqlalchemy as sa

revision = "038"
down_revision = "037"
branch_labels = None
depends_on = None


prepositions_table = sa.table(
    "prepositions",
    sa.column("id", sa.Integer),
    sa.column("base_form", sa.String),
    sa.column("meaning_ru", sa.String),
    sa.column("declension_json", sa.Text),
)


DATA = [
    # 1. ב (бэ) — в, внутри
    {
        "base_form": "ב",
        "meaning_ru": "в, внутри",
        "declension_json": json.dumps(
            {
                "1s": {"form": "בי", "translit": "би"},
                "2ms": {"form": "בך", "translit": "бэха"},
                "2fs": {"form": "בך", "translit": "бах"},
                "3ms": {"form": "בו", "translit": "бо"},
                "3fs": {"form": "בה", "translit": "ба"},
                "1p": {"form": "בנו", "translit": "бану"},
                "2mp": {"form": "בכם", "translit": "бахэм"},
                "2fp": {"form": "בכן", "translit": "бахэн"},
                "3mp": {"form": "בהם", "translit": "баhэм"},
                "3fp": {"form": "בהן", "translit": "баhэн"},
            },
            ensure_ascii=False,
        ),
    },
    # 2. ל (лэ) — к, для
    {
        "base_form": "ל",
        "meaning_ru": "к, для",
        "declension_json": json.dumps(
            {
                "1s": {"form": "לי", "translit": "ли"},
                "2ms": {"form": "לך", "translit": "лэха"},
                "2fs": {"form": "לך", "translit": "лах"},
                "3ms": {"form": "לו", "translit": "ло"},
                "3fs": {"form": "לה", "translit": "ла"},
                "1p": {"form": "לנו", "translit": "лану"},
                "2mp": {"form": "לכם", "translit": "лахэм"},
                "2fp": {"form": "לכן", "translit": "лахэн"},
                "3mp": {"form": "להם", "translit": "лаhэм"},
                "3fp": {"form": "להן", "translit": "лаhэн"},
            },
            ensure_ascii=False,
        ),
    },
    # 3. מ / מן (ми/мин) — из, от
    {
        "base_form": "מ / מן",
        "meaning_ru": "из, от",
        "declension_json": json.dumps(
            {
                "1s": {"form": "ממני", "translit": "мимЭни"},
                "2ms": {"form": "ממך", "translit": "мимхА"},
                "2fs": {"form": "ממך", "translit": "мимЭх"},
                "3ms": {"form": "ממנו", "translit": "мимЭну"},
                "3fs": {"form": "ממנה", "translit": "мимЭна"},
                "1p": {"form": "מאיתנו", "translit": "мэитАну"},
                "2mp": {"form": "מכם", "translit": "микЭм"},
                "2fp": {"form": "מכן", "translit": "микЭн"},
                "3mp": {"form": "מהם", "translit": "мэhЭм"},
                "3fp": {"form": "מהן", "translit": "мэhЭн"},
            },
            ensure_ascii=False,
        ),
    },
    # 4. על (аль) — на, о
    {
        "base_form": "על",
        "meaning_ru": "на, о",
        "declension_json": json.dumps(
            {
                "1s": {"form": "עליי", "translit": "алАй"},
                "2ms": {"form": "עליך", "translit": "алЕйха"},
                "2fs": {"form": "עלייך", "translit": "алАйих"},
                "3ms": {"form": "עליו", "translit": "алАв"},
                "3fs": {"form": "עליה", "translit": "алЕйhа"},
                "1p": {"form": "עלינו", "translit": "алЕйну"},
                "2mp": {"form": "עליכם", "translit": "алейхЭм"},
                "2fp": {"form": "עליכן", "translit": "алейхЭн"},
                "3mp": {"form": "עליהם", "translit": "алейhЭм"},
                "3fp": {"form": "עליהן", "translit": "алейhЭн"},
            },
            ensure_ascii=False,
        ),
    },
    # 5. אל (эль) — к, в направлении
    {
        "base_form": "אל",
        "meaning_ru": "к, в направлении",
        "declension_json": json.dumps(
            {
                "1s": {"form": "אליי", "translit": "элАй"},
                "2ms": {"form": "אליך", "translit": "элЕйха"},
                "2fs": {"form": "אלייך", "translit": "элАйих"},
                "3ms": {"form": "אליו", "translit": "элАв"},
                "3fs": {"form": "אליה", "translit": "элЕйhа"},
                "1p": {"form": "אלינו", "translit": "элЕйну"},
                "2mp": {"form": "אליכם", "translit": "алейхЭм"},
                "2fp": {"form": "אליכן", "translit": "алейхЭн"},
                "3mp": {"form": "אליהם", "translit": "алейhЭм"},
                "3fp": {"form": "אליהן", "translit": "алейhЭн"},
            },
            ensure_ascii=False,
        ),
    },
    # 6. עם (им) — с (together)
    {
        "base_form": "עם",
        "meaning_ru": "с (вместе)",
        "declension_json": json.dumps(
            {
                "1s": {"form": "איתי", "translit": "итИ"},
                "2ms": {"form": "איתך", "translit": "итхА"},
                "2fs": {"form": "איתך", "translit": "итАх"},
                "3ms": {"form": "איתו", "translit": "итО"},
                "3fs": {"form": "איתה", "translit": "итА"},
                "1p": {"form": "איתנו", "translit": "итАну"},
                "2mp": {"form": "איתכם", "translit": "итхЭм"},
                "2fp": {"form": "איתכן", "translit": "итхЭн"},
                "3mp": {"form": "איתם", "translit": "итАм"},
                "3fp": {"form": "איתן", "translit": "итАн"},
            },
            ensure_ascii=False,
        ),
    },
    # 7. את (эт) — с (together, alternative), also accusative marker
    {
        "base_form": "את",
        "meaning_ru": "с (вместе); маркер прямого дополнения",
        "declension_json": json.dumps(
            {
                "1s": {"form": "אותי / איתי", "translit": "отИ / итИ"},
                "2ms": {"form": "אותך / איתך", "translit": "отхА / итхА"},
                "2fs": {"form": "אותך / איתך", "translit": "отАх / итАх"},
                "3ms": {"form": "אותו / איתו", "translit": "отО / итО"},
                "3fs": {"form": "אותה / איתה", "translit": "отА / итА"},
                "1p": {"form": "אותנו / איתנו", "translit": "отАну / итАну"},
                "2mp": {"form": "אתכם / איתכם", "translit": "этхЭм / итхЭм"},
                "2fp": {"form": "אתכן / איתכן", "translit": "этхЭн / итхЭн"},
                "3mp": {"form": "אותם / איתם", "translit": "отАм / итАм"},
                "3fp": {"form": "אותן / איתן", "translit": "отАн / итАн"},
            },
            ensure_ascii=False,
        ),
    },
    # 8. של (шель) — принадлежность (of)
    {
        "base_form": "של",
        "meaning_ru": "принадлежность (of)",
        "declension_json": json.dumps(
            {
                "1s": {"form": "שלי", "translit": "шелИ"},
                "2ms": {"form": "שלך", "translit": "шелхА"},
                "2fs": {"form": "שלך", "translit": "шелАх"},
                "3ms": {"form": "שלו", "translit": "шелО"},
                "3fs": {"form": "שלה", "translit": "шелА"},
                "1p": {"form": "שלנו", "translit": "шелАну"},
                "2mp": {"form": "שלכם", "translit": "шелахЭм"},
                "2fp": {"form": "שלכן", "translit": "шелахЭн"},
                "3mp": {"form": "שלהם", "translit": "шелаhЭм"},
                "3fp": {"form": "שלהן", "translit": "шелаhЭн"},
            },
            ensure_ascii=False,
        ),
    },
    # 9. בשביל (бишвиль) — для, ради
    {
        "base_form": "בשביל",
        "meaning_ru": "для, ради",
        "declension_json": json.dumps(
            {
                "1s": {"form": "בשבילי", "translit": "бишвилИ"},
                "2ms": {"form": "בשבילך", "translit": "бишвилхА"},
                "2fs": {"form": "בשבילך", "translit": "бишвилЭх"},
                "3ms": {"form": "בשבילו", "translit": "бишвилО"},
                "3fs": {"form": "בשבילה", "translit": "бишвилА"},
                "1p": {"form": "בשבילנו", "translit": "бишвилЭну"},
                "2mp": {"form": "בשבילכם", "translit": "бишвилхЭм"},
                "2fp": {"form": "בשבילכן", "translit": "бишвилхЭн"},
                "3mp": {"form": "בשבילם", "translit": "бишвилАм"},
                "3fp": {"form": "בשבילן", "translit": "бишвилАн"},
            },
            ensure_ascii=False,
        ),
    },
    # 10. בלי (бли) — без (no pronominal suffixes in standard usage)
    {
        "base_form": "בלי",
        "meaning_ru": "без",
        "declension_json": None,
    },
    # 11. לפני (лифнэй) — перед, до
    {
        "base_form": "לפני",
        "meaning_ru": "перед, до",
        "declension_json": json.dumps(
            {
                "1s": {"form": "לפניי", "translit": "лэфанАй"},
                "2ms": {"form": "לפניך", "translit": "лэфанЕйха"},
                "2fs": {"form": "לפנייך", "translit": "лэфанАйих"},
                "3ms": {"form": "לפניו", "translit": "лэфанАв"},
                "3fs": {"form": "לפניה", "translit": "лэфанЕйhа"},
                "1p": {"form": "לפנינו", "translit": "лэфанЕйну"},
                "2mp": {"form": "לפניכם", "translit": "лифнейхЭм"},
                "2fp": {"form": "לפניכן", "translit": "лифнейхЭн"},
                "3mp": {"form": "לפניהם", "translit": "лифнейhЭм"},
                "3fp": {"form": "לפניהן", "translit": "лифнейhЭн"},
            },
            ensure_ascii=False,
        ),
    },
    # 12. אחרי (ахарэй) — после, за
    {
        "base_form": "אחרי",
        "meaning_ru": "после, за",
        "declension_json": json.dumps(
            {
                "1s": {"form": "אחריי", "translit": "ахарАй"},
                "2ms": {"form": "אחריך", "translit": "ахарЕйха"},
                "2fs": {"form": "אחרייך", "translit": "ахарАйих"},
                "3ms": {"form": "אחריו", "translit": "ахарАв"},
                "3fs": {"form": "אחריה", "translit": "ахарЕйhа"},
                "1p": {"form": "אחרינו", "translit": "ахарЕйну"},
                "2mp": {"form": "אחריכם", "translit": "ахарейхЭм"},
                "2fp": {"form": "אחריכן", "translit": "ахарейхЭн"},
                "3mp": {"form": "אחריהם", "translit": "ахарейhЭм"},
                "3fp": {"form": "אחריהן", "translit": "ахарейhЭн"},
            },
            ensure_ascii=False,
        ),
    },
    # 13. ליד (лэяд) — рядом с
    {
        "base_form": "ליד",
        "meaning_ru": "рядом с",
        "declension_json": json.dumps(
            {
                "1s": {"form": "לידי", "translit": "лэядИ"},
                "2ms": {"form": "לידך", "translit": "лэядхА"},
                "2fs": {"form": "לידך", "translit": "лэядЭх"},
                "3ms": {"form": "לידו", "translit": "лэядО"},
                "3fs": {"form": "לידה", "translit": "лэядА"},
                "1p": {"form": "לידנו", "translit": "лэядЭну"},
                "2mp": {"form": "לידכם", "translit": "лэядхЭм"},
                "2fp": {"form": "לידכן", "translit": "лэядхЭн"},
                "3mp": {"form": "לידם", "translit": "лэядАм"},
                "3fp": {"form": "לידן", "translit": "лэядАн"},
            },
            ensure_ascii=False,
        ),
    },
    # 14. בין (бэйн) — между
    {
        "base_form": "בין",
        "meaning_ru": "между",
        "declension_json": json.dumps(
            {
                "1s": {"form": "ביני", "translit": "бейнИ"},
                "2ms": {"form": "בינך", "translit": "бейнхА"},
                "2fs": {"form": "בינך", "translit": "бейнЭх"},
                "3ms": {"form": "בינו", "translit": "бейнО"},
                "3fs": {"form": "בינה", "translit": "бейнА"},
                "1p": {"form": "בינינו", "translit": "бейнЕйну"},
                "2mp": {"form": "ביניכם", "translit": "бейнейхЭм"},
                "2fp": {"form": "ביניכן", "translit": "бейнейхЭн"},
                "3mp": {"form": "ביניהם", "translit": "бейнейhЭм"},
                "3fp": {"form": "ביניהן", "translit": "бейнейhЭн"},
            },
            ensure_ascii=False,
        ),
    },
    # 15. מול (муль) — напротив
    {
        "base_form": "מול",
        "meaning_ru": "напротив",
        "declension_json": json.dumps(
            {
                "1s": {"form": "מולי", "translit": "мулИ"},
                "2ms": {"form": "מולך", "translit": "мулхА"},
                "2fs": {"form": "מולך", "translit": "мулЭх"},
                "3ms": {"form": "מולו", "translit": "мулО"},
                "3fs": {"form": "מולה", "translit": "мулА"},
                "1p": {"form": "מולנו", "translit": "мулЭну"},
                "2mp": {"form": "מולכם", "translit": "мулхЭм"},
                "2fp": {"form": "מולכן", "translit": "мулхЭн"},
                "3mp": {"form": "מולם", "translit": "мулАм"},
                "3fp": {"form": "מולן", "translit": "мулАн"},
            },
            ensure_ascii=False,
        ),
    },
    # 16. תחת (тахат) — под
    {
        "base_form": "תחת",
        "meaning_ru": "под",
        "declension_json": json.dumps(
            {
                "1s": {"form": "תחתיי", "translit": "тахтАй"},
                "2ms": {"form": "תחתיך", "translit": "тахтЕйха"},
                "2fs": {"form": "תחתייך", "translit": "тахтАйих"},
                "3ms": {"form": "תחתיו", "translit": "тахтАв"},
                "3fs": {"form": "תחתיה", "translit": "тахтЕйhа"},
                "1p": {"form": "תחתינו", "translit": "тахтЕйну"},
                "2mp": {"form": "תחתיכם", "translit": "тахтейхЭм"},
                "2fp": {"form": "תחתיכן", "translit": "тахтейхЭн"},
                "3mp": {"form": "תחתיהם", "translit": "тахтейhЭм"},
                "3fp": {"form": "תחתיהן", "translit": "тахтейhЭн"},
            },
            ensure_ascii=False,
        ),
    },
    # 17. מעל (мэаль) — над
    {
        "base_form": "מעל",
        "meaning_ru": "над",
        "declension_json": json.dumps(
            {
                "1s": {"form": "מעליי", "translit": "мэалАй"},
                "2ms": {"form": "מעליך", "translit": "мэалЕйха"},
                "2fs": {"form": "מעלייך", "translit": "мэалАйих"},
                "3ms": {"form": "מעליו", "translit": "мэалАв"},
                "3fs": {"form": "מעליה", "translit": "мэалЕйhа"},
                "1p": {"form": "מעלינו", "translit": "мэалЕйну"},
                "2mp": {"form": "מעליכם", "translit": "мэалейхЭм"},
                "2fp": {"form": "מעליכן", "translit": "мэалейхЭн"},
                "3mp": {"form": "מעליהם", "translit": "мэалейhЭм"},
                "3fp": {"form": "מעליהן", "translit": "мэалейhЭн"},
            },
            ensure_ascii=False,
        ),
    },
    # 18. סביב (савив) — вокруг
    {
        "base_form": "סביב",
        "meaning_ru": "вокруг",
        "declension_json": json.dumps(
            {
                "1s": {"form": "סביבי", "translit": "свивИ"},
                "2ms": {"form": "סביבך", "translit": "свивхА"},
                "2fs": {"form": "סביבך", "translit": "свивЭх"},
                "3ms": {"form": "סביבו", "translit": "свивО"},
                "3fs": {"form": "סביבה", "translit": "свивА"},
                "1p": {"form": "סביבנו", "translit": "свивЭну"},
                "2mp": {"form": "סביבכם", "translit": "свивхЭм"},
                "2fp": {"form": "סביבכן", "translit": "свивхЭн"},
                "3mp": {"form": "סביבם", "translit": "свивАм"},
                "3fp": {"form": "סביבן", "translit": "свивАн"},
            },
            ensure_ascii=False,
        ),
    },
    # 19. כמו (кмо) — как (no pronominal suffixes in standard modern Hebrew)
    {
        "base_form": "כמו",
        "meaning_ru": "как",
        "declension_json": json.dumps(
            {
                "1s": {"form": "כמוני", "translit": "камОни"},
                "2ms": {"form": "כמוך", "translit": "камОха"},
                "2fs": {"form": "כמוך", "translit": "камОх"},
                "3ms": {"form": "כמוהו", "translit": "камОhу"},
                "3fs": {"form": "כמוה", "translit": "камОhа"},
                "1p": {"form": "כמונו", "translit": "камОну"},
                "2mp": {"form": "כמוכם", "translit": "камохЭм"},
                "2fp": {"form": "כמוכן", "translit": "камохЭн"},
                "3mp": {"form": "כמוהם", "translit": "камоhЭм"},
                "3fp": {"form": "כמוהן", "translit": "камоhЭн"},
            },
            ensure_ascii=False,
        ),
    },
    # 20. בגלל (бигляль) — из-за
    {
        "base_form": "בגלל",
        "meaning_ru": "из-за",
        "declension_json": json.dumps(
            {
                "1s": {"form": "בגללי", "translit": "биглалИ"},
                "2ms": {"form": "בגללך", "translit": "биглалхА"},
                "2fs": {"form": "בגללך", "translit": "биглалЭх"},
                "3ms": {"form": "בגללו", "translit": "биглалО"},
                "3fs": {"form": "בגללה", "translit": "биглалА"},
                "1p": {"form": "בגללנו", "translit": "биглалЭну"},
                "2mp": {"form": "בגללכם", "translit": "биглалхЭм"},
                "2fp": {"form": "בגללכן", "translit": "биглалхЭн"},
                "3mp": {"form": "בגללם", "translit": "биглалАм"},
                "3fp": {"form": "בגללן", "translit": "биглалАн"},
            },
            ensure_ascii=False,
        ),
    },
    # 21. למרות (ламрот) — несмотря на (no pronominal suffixes)
    {
        "base_form": "למרות",
        "meaning_ru": "несмотря на",
        "declension_json": None,
    },
    # 22. כלפי (клапэй) — по отношению к
    {
        "base_form": "כלפי",
        "meaning_ru": "по отношению к",
        "declension_json": json.dumps(
            {
                "1s": {"form": "כלפיי", "translit": "клапАй"},
                "2ms": {"form": "כלפיך", "translit": "клапЕйха"},
                "2fs": {"form": "כלפייך", "translit": "клапАйих"},
                "3ms": {"form": "כלפיו", "translit": "клапАв"},
                "3fs": {"form": "כלפיה", "translit": "клапЕйhа"},
                "1p": {"form": "כלפינו", "translit": "клапЕйну"},
                "2mp": {"form": "כלפיכם", "translit": "клапейхЭм"},
                "2fp": {"form": "כלפיכן", "translit": "клапейхЭн"},
                "3mp": {"form": "כלפיהם", "translit": "клапейhЭм"},
                "3fp": {"form": "כלפיהן", "translit": "клапейhЭн"},
            },
            ensure_ascii=False,
        ),
    },
    # 23. אצל (эцель) — у (чьего-то дома), возле
    {
        "base_form": "אצל",
        "meaning_ru": "у (чьего-то дома), возле",
        "declension_json": json.dumps(
            {
                "1s": {"form": "אצלי", "translit": "эцлИ"},
                "2ms": {"form": "אצלך", "translit": "эцлхА"},
                "2fs": {"form": "אצלך", "translit": "эцлЭх"},
                "3ms": {"form": "אצלו", "translit": "эцлО"},
                "3fs": {"form": "אצלה", "translit": "эцлА"},
                "1p": {"form": "אצלנו", "translit": "эцлЭну"},
                "2mp": {"form": "אצלכם", "translit": "эцлхЭм"},
                "2fp": {"form": "אצלכן", "translit": "эцлхЭн"},
                "3mp": {"form": "אצלם", "translit": "эцлАм"},
                "3fp": {"form": "אצלן", "translit": "эцлАн"},
            },
            ensure_ascii=False,
        ),
    },
    # 24. נגד (нэгед) — против
    {
        "base_form": "נגד",
        "meaning_ru": "против",
        "declension_json": json.dumps(
            {
                "1s": {"form": "נגדי", "translit": "нэгдИ"},
                "2ms": {"form": "נגדך", "translit": "нэгдхА"},
                "2fs": {"form": "נגדך", "translit": "нэгдЭх"},
                "3ms": {"form": "נגדו", "translit": "нэгдО"},
                "3fs": {"form": "נגדה", "translit": "нэгдА"},
                "1p": {"form": "נגדנו", "translit": "нэгдЭну"},
                "2mp": {"form": "נגדכם", "translit": "нэгдхЭм"},
                "2fp": {"form": "נגדכן", "translit": "нэгдхЭн"},
                "3mp": {"form": "נגדם", "translit": "нэгдАм"},
                "3fp": {"form": "נגדן", "translit": "нэгдАн"},
            },
            ensure_ascii=False,
        ),
    },
]


def upgrade():
    # Reset the sequence to avoid conflicts
    op.execute(
        "SELECT setval('prepositions_id_seq', GREATEST((SELECT COALESCE(MAX(id), 0) FROM prepositions), 1))"
    )

    op.bulk_insert(prepositions_table, DATA)


def downgrade():
    op.execute("DELETE FROM prepositions")
