"""Add 285 Level 2 (A2) words to the Hebrew dictionary

Adds practical everyday vocabulary across six topics:
  1. Work & Office (50)
  2. Health & Medicine (50)
  3. Travel & Leisure (50)
  4. Shopping & Money (45)
  5. Emotions & Character (45)
  6. Public Places & Services (45)

Revision ID: 045
Revises: 044
Create Date: 2026-03-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "045"
down_revision: Union[str, None] = "044"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ══════════════════════════════════════════════════════════════════════════════
# Table reference
# ══════════════════════════════════════════════════════════════════════════════

words_table = sa.table(
    "words",
    sa.column("hebrew", sa.String),
    sa.column("nikkud", sa.String),
    sa.column("transliteration", sa.String),
    sa.column("translation_ru", sa.String),
    sa.column("pos", sa.String),
    sa.column("gender", sa.String),
    sa.column("number", sa.String),
    sa.column("root", sa.String),
    sa.column("frequency_rank", sa.Integer),
    sa.column("level_id", sa.Integer),
    sa.column("audio_url", sa.String),
    sa.column("image_url", sa.String),
)

# ══════════════════════════════════════════════════════════════════════════════
# 1. Работа и офис — Work & Office (50 words)
# ══════════════════════════════════════════════════════════════════════════════

WORK_OFFICE = [
    {"hebrew": "משרד", "nikkud": None, "transliteration": "мисрАд", "translation_ru": "офис, контора", "pos": "noun", "gender": "m", "number": "singular", "root": "ש.ר.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "פגישה", "nikkud": None, "transliteration": "пгишА", "translation_ru": "встреча, совещание", "pos": "noun", "gender": "f", "number": "singular", "root": "פ.ג.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שכר", "nikkud": None, "transliteration": "сахАр", "translation_ru": "зарплата", "pos": "noun", "gender": "m", "number": "singular", "root": "ש.כ.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חופשה", "nikkud": None, "transliteration": "хуфшА", "translation_ru": "отпуск, каникулы", "pos": "noun", "gender": "f", "number": "singular", "root": "ח.פ.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "פיטורים", "nikkud": None, "transliteration": "питурИм", "translation_ru": "увольнение", "pos": "noun", "gender": "m", "number": "plural", "root": "פ.ט.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "קידום", "nikkud": None, "transliteration": "кидУм", "translation_ru": "продвижение (по службе)", "pos": "noun", "gender": "m", "number": "singular", "root": "ק.ד.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ראיון", "nikkud": None, "transliteration": "реайОн", "translation_ru": "собеседование, интервью", "pos": "noun", "gender": "m", "number": "singular", "root": "ר.א.י", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עמית", "nikkud": None, "transliteration": "амИт", "translation_ru": "коллега", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בוס", "nikkud": None, "transliteration": "бос", "translation_ru": "босс, начальник", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מנהל", "nikkud": None, "transliteration": "менаhЭль", "translation_ru": "директор, управляющий", "pos": "noun", "gender": "m", "number": "singular", "root": "נ.ה.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חשבון", "nikkud": None, "transliteration": "хешбОн", "translation_ru": "счёт", "pos": "noun", "gender": "m", "number": "singular", "root": "ח.ש.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חשבונית", "nikkud": None, "transliteration": "хешбонИт", "translation_ru": "счёт-фактура, квитанция", "pos": "noun", "gender": "f", "number": "singular", "root": "ח.ש.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "קבלה", "nikkud": None, "transliteration": "кабалА", "translation_ru": "квитанция, чек", "pos": "noun", "gender": "f", "number": "singular", "root": "ק.ב.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חתימה", "nikkud": None, "transliteration": "хатимА", "translation_ru": "подпись", "pos": "noun", "gender": "f", "number": "singular", "root": "ח.ת.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מכתב", "nikkud": None, "transliteration": "михтАв", "translation_ru": "письмо", "pos": "noun", "gender": "m", "number": "singular", "root": "כ.ת.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "דוא״ל", "nikkud": None, "transliteration": "дОэль", "translation_ru": "электронная почта", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "הודעה", "nikkud": None, "transliteration": "hодаА", "translation_ru": "сообщение, уведомление", "pos": "noun", "gender": "f", "number": "singular", "root": "י.ד.ע", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לוח שנה", "nikkud": None, "transliteration": "лУах шанА", "translation_ru": "календарь", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "יומן", "nikkud": None, "transliteration": "йомАн", "translation_ru": "ежедневник, дневник", "pos": "noun", "gender": "m", "number": "singular", "root": "י.ו.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "דד-ליין", "nikkud": None, "transliteration": "дэдлАйн", "translation_ru": "крайний срок", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מועד", "nikkud": None, "transliteration": "моЭд", "translation_ru": "срок, дата", "pos": "noun", "gender": "m", "number": "singular", "root": "י.ע.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תוכנית", "nikkud": None, "transliteration": "тохнИт", "translation_ru": "план, программа", "pos": "noun", "gender": "f", "number": "singular", "root": "ת.כ.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ישיבה", "nikkud": None, "transliteration": "йешивА", "translation_ru": "заседание", "pos": "noun", "gender": "f", "number": "singular", "root": "י.ש.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "פרוטוקול", "nikkud": None, "transliteration": "протокОль", "translation_ru": "протокол", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "דו״ח", "nikkud": None, "transliteration": "дОах", "translation_ru": "отчёт, доклад", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מסמך", "nikkud": None, "transliteration": "мисмАх", "translation_ru": "документ", "pos": "noun", "gender": "m", "number": "singular", "root": "ס.מ.כ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תיק", "nikkud": None, "transliteration": "тик", "translation_ru": "папка, портфель; дело", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "הדפסה", "nikkud": None, "transliteration": "hадпасА", "translation_ru": "печать, распечатка", "pos": "noun", "gender": "f", "number": "singular", "root": "ד.פ.ס", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מדפסת", "nikkud": None, "transliteration": "мадпЕсет", "translation_ru": "принтер", "pos": "noun", "gender": "f", "number": "singular", "root": "ד.פ.ס", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "סורק", "nikkud": None, "transliteration": "сорЭк", "translation_ru": "сканер", "pos": "noun", "gender": "m", "number": "singular", "root": "ס.ר.ק", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "פקס", "nikkud": None, "transliteration": "факс", "translation_ru": "факс", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "משימה", "nikkud": None, "transliteration": "мешимА", "translation_ru": "задание, задача", "pos": "noun", "gender": "f", "number": "singular", "root": "ש.י.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "פרויקט", "nikkud": None, "transliteration": "проЕкт", "translation_ru": "проект", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לקוח", "nikkud": None, "transliteration": "лакОах", "translation_ru": "клиент", "pos": "noun", "gender": "m", "number": "singular", "root": "ל.ק.ח", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ספק", "nikkud": None, "transliteration": "сапАк", "translation_ru": "поставщик", "pos": "noun", "gender": "m", "number": "singular", "root": "ס.פ.ק", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חוזה", "nikkud": None, "transliteration": "хозЭ", "translation_ru": "контракт, договор", "pos": "noun", "gender": "m", "number": "singular", "root": "ח.ז.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "הסכם", "nikkud": None, "transliteration": "hэскЭм", "translation_ru": "соглашение", "pos": "noun", "gender": "m", "number": "singular", "root": "ס.כ.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תקציב", "nikkud": None, "transliteration": "такцИв", "translation_ru": "бюджет", "pos": "noun", "gender": "m", "number": "singular", "root": "ק.צ.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "רווח", "nikkud": None, "transliteration": "рЕвах", "translation_ru": "прибыль", "pos": "noun", "gender": "m", "number": "singular", "root": "ר.ו.ח", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "הפסד", "nikkud": None, "transliteration": "hэфсЭд", "translation_ru": "убыток, потеря", "pos": "noun", "gender": "m", "number": "singular", "root": "פ.ס.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עובד", "nikkud": None, "transliteration": "овЭд", "translation_ru": "работник, сотрудник", "pos": "noun", "gender": "m", "number": "singular", "root": "ע.ב.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מעסיק", "nikkud": None, "transliteration": "маасИк", "translation_ru": "работодатель", "pos": "noun", "gender": "m", "number": "singular", "root": "ע.ס.ק", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "משרה", "nikkud": None, "transliteration": "масрА", "translation_ru": "должность, ставка", "pos": "noun", "gender": "f", "number": "singular", "root": "ש.ר.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "קורות חיים", "nikkud": None, "transliteration": "корОт хайИм", "translation_ru": "резюме (CV)", "pos": "noun", "gender": "m", "number": "plural", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שעות נוספות", "nikkud": None, "transliteration": "шаОт носафОт", "translation_ru": "сверхурочные", "pos": "noun", "gender": "f", "number": "plural", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "העלאה", "nikkud": None, "transliteration": "hаалаА", "translation_ru": "повышение (зарплаты)", "pos": "noun", "gender": "f", "number": "singular", "root": "ע.ל.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "התפטרות", "nikkud": None, "transliteration": "hитпатрУт", "translation_ru": "увольнение (по собственному)", "pos": "noun", "gender": "f", "number": "singular", "root": "פ.ט.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "גיוס", "nikkud": None, "transliteration": "гиЮс", "translation_ru": "набор (на работу); призыв", "pos": "noun", "gender": "m", "number": "singular", "root": "ג.י.ס", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "הכשרה", "nikkud": None, "transliteration": "hахшарА", "translation_ru": "обучение, подготовка", "pos": "noun", "gender": "f", "number": "singular", "root": "כ.ש.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מחלקה", "nikkud": None, "transliteration": "махлакА", "translation_ru": "отдел, подразделение", "pos": "noun", "gender": "f", "number": "singular", "root": "ח.ל.ק", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. Здоровье и медицина — Health & Medicine (50 words)
# ══════════════════════════════════════════════════════════════════════════════

HEALTH_MEDICINE = [
    {"hebrew": "רופא עיניים", "nikkud": None, "transliteration": "рофЭ эйнАйим", "translation_ru": "окулист, офтальмолог", "pos": "noun", "gender": "m", "number": "singular", "root": "ר.פ.א", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "רופא שיניים", "nikkud": None, "transliteration": "рофЭ шинАйим", "translation_ru": "стоматолог", "pos": "noun", "gender": "m", "number": "singular", "root": "ר.פ.א", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אלרגיה", "nikkud": None, "transliteration": "алЭргия", "translation_ru": "аллергия", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "דלקת", "nikkud": None, "transliteration": "далЕкет", "translation_ru": "воспаление", "pos": "noun", "gender": "f", "number": "singular", "root": "ד.ל.ק", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "זיהום", "nikkud": None, "transliteration": "зиhУм", "translation_ru": "инфекция, заражение", "pos": "noun", "gender": "m", "number": "singular", "root": "ז.ה.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ניתוח", "nikkud": None, "transliteration": "нитУах", "translation_ru": "операция (хирургическая)", "pos": "noun", "gender": "m", "number": "singular", "root": "נ.ת.ח", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בדיקה", "nikkud": None, "transliteration": "бдикА", "translation_ru": "анализ, проверка", "pos": "noun", "gender": "f", "number": "singular", "root": "ב.ד.ק", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "צילום", "nikkud": None, "transliteration": "цилУм", "translation_ru": "снимок, рентген", "pos": "noun", "gender": "m", "number": "singular", "root": "צ.ל.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "דם", "nikkud": None, "transliteration": "дам", "translation_ru": "кровь", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לחץ דם", "nikkud": None, "transliteration": "лАхац дам", "translation_ru": "давление (кровяное)", "pos": "noun", "gender": "m", "number": "singular", "root": "ל.ח.ץ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "סוכרת", "nikkud": None, "transliteration": "сукЕрет", "translation_ru": "сахарный диабет", "pos": "noun", "gender": "f", "number": "singular", "root": "ס.כ.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אנטיביוטיקה", "nikkud": None, "transliteration": "антибиОтика", "translation_ru": "антибиотик", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "זריקה", "nikkud": None, "transliteration": "зрикА", "translation_ru": "укол, инъекция", "pos": "noun", "gender": "f", "number": "singular", "root": "ז.ר.ק", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חיסון", "nikkud": None, "transliteration": "хисУн", "translation_ru": "прививка, вакцина", "pos": "noun", "gender": "m", "number": "singular", "root": "ח.ס.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תחבושת", "nikkud": None, "transliteration": "тахбОшет", "translation_ru": "повязка, бинт", "pos": "noun", "gender": "f", "number": "singular", "root": "ח.ב.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "גבס", "nikkud": None, "transliteration": "гЕвес", "translation_ru": "гипс", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אשפוז", "nikkud": None, "transliteration": "ишпУз", "translation_ru": "госпитализация", "pos": "noun", "gender": "m", "number": "singular", "root": "ש.פ.ז", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שחרור", "nikkud": None, "transliteration": "шихрУр", "translation_ru": "выписка (из больницы)", "pos": "noun", "gender": "m", "number": "singular", "root": "ש.ח.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מיון", "nikkud": None, "transliteration": "миЮн", "translation_ru": "сортировка; приёмный покой", "pos": "noun", "gender": "m", "number": "singular", "root": "מ.י.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חדר מיון", "nikkud": None, "transliteration": "хЕдер миЮн", "translation_ru": "приёмный покой", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מרשם", "nikkud": None, "transliteration": "миршАм", "translation_ru": "рецепт (врачебный)", "pos": "noun", "gender": "m", "number": "singular", "root": "ר.ש.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תרופה", "nikkud": None, "transliteration": "труфА", "translation_ru": "лекарство", "pos": "noun", "gender": "f", "number": "singular", "root": "ר.פ.א", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כדור", "nikkud": None, "transliteration": "кадУр", "translation_ru": "таблетка; мяч", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "משחה", "nikkud": None, "transliteration": "мишхА", "translation_ru": "мазь", "pos": "noun", "gender": "f", "number": "singular", "root": "מ.ש.ח", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "טיפות", "nikkud": None, "transliteration": "типОт", "translation_ru": "капли (лекарство)", "pos": "noun", "gender": "f", "number": "plural", "root": "ט.פ.ף", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תסמין", "nikkud": None, "transliteration": "тасмИн", "translation_ru": "симптом", "pos": "noun", "gender": "m", "number": "singular", "root": "ס.מ.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אבחנה", "nikkud": None, "transliteration": "авханА", "translation_ru": "диагноз", "pos": "noun", "gender": "f", "number": "singular", "root": "ב.ח.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "טיפול", "nikkud": None, "transliteration": "типУль", "translation_ru": "лечение, уход", "pos": "noun", "gender": "m", "number": "singular", "root": "ט.פ.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "החלמה", "nikkud": None, "transliteration": "hахламА", "translation_ru": "выздоровление", "pos": "noun", "gender": "f", "number": "singular", "root": "ח.ל.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חום", "nikkud": None, "transliteration": "хом", "translation_ru": "температура, жар", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שיעול", "nikkud": None, "transliteration": "шиУль", "translation_ru": "кашель", "pos": "noun", "gender": "m", "number": "singular", "root": "ש.ע.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "נזלת", "nikkud": None, "transliteration": "назЕлет", "translation_ru": "насморк", "pos": "noun", "gender": "f", "number": "singular", "root": "נ.ז.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כאב ראש", "nikkud": None, "transliteration": "кеЭв рош", "translation_ru": "головная боль", "pos": "noun", "gender": "m", "number": "singular", "root": "כ.א.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "סחרחורת", "nikkud": None, "transliteration": "схархОрет", "translation_ru": "головокружение", "pos": "noun", "gender": "f", "number": "singular", "root": "ס.ח.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בחילה", "nikkud": None, "transliteration": "бхилА", "translation_ru": "тошнота", "pos": "noun", "gender": "f", "number": "singular", "root": "ב.ח.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "פצע", "nikkud": None, "transliteration": "пЕца", "translation_ru": "рана", "pos": "noun", "gender": "m", "number": "singular", "root": "פ.צ.ע", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שבר", "nikkud": None, "transliteration": "шЕвер", "translation_ru": "перелом", "pos": "noun", "gender": "m", "number": "singular", "root": "ש.ב.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כוויה", "nikkud": None, "transliteration": "квиЯ", "translation_ru": "ожог", "pos": "noun", "gender": "f", "number": "singular", "root": "כ.ו.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עצם", "nikkud": None, "transliteration": "Эцем", "translation_ru": "кость", "pos": "noun", "gender": "f", "number": "singular", "root": "ע.צ.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שריר", "nikkud": None, "transliteration": "шрир", "translation_ru": "мышца", "pos": "noun", "gender": "m", "number": "singular", "root": "ש.ר.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מפרק", "nikkud": None, "transliteration": "мифрАк", "translation_ru": "сустав", "pos": "noun", "gender": "m", "number": "singular", "root": "פ.ר.ק", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ריאות", "nikkud": None, "transliteration": "реОт", "translation_ru": "лёгкие", "pos": "noun", "gender": "f", "number": "plural", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כליות", "nikkud": None, "transliteration": "клайОт", "translation_ru": "почки", "pos": "noun", "gender": "f", "number": "plural", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כבד", "nikkud": None, "transliteration": "кавЭд", "translation_ru": "печень", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "קיבה", "nikkud": None, "transliteration": "кейвА", "translation_ru": "желудок", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אחות", "nikkud": None, "transliteration": "ахОт", "translation_ru": "медсестра", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חולה", "nikkud": None, "transliteration": "холЭ", "translation_ru": "больной, пациент", "pos": "noun", "gender": "m", "number": "singular", "root": "ח.ל.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "קופת חולים", "nikkud": None, "transliteration": "купАт холИм", "translation_ru": "больничная касса", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מרפאה", "nikkud": None, "transliteration": "мирпаА", "translation_ru": "поликлиника, клиника", "pos": "noun", "gender": "f", "number": "singular", "root": "ר.פ.א", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בית חולים", "nikkud": None, "transliteration": "бейт холИм", "translation_ru": "больница", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. Путешествия и отдых — Travel & Leisure (50 words)
# ══════════════════════════════════════════════════════════════════════════════

TRAVEL_LEISURE = [
    {"hebrew": "טיסה", "nikkud": None, "transliteration": "тисА", "translation_ru": "перелёт, рейс", "pos": "noun", "gender": "f", "number": "singular", "root": "ט.י.ס", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כרטיס", "nikkud": None, "transliteration": "картИс", "translation_ru": "билет", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "דרכון", "nikkud": None, "transliteration": "даркОн", "translation_ru": "паспорт", "pos": "noun", "gender": "m", "number": "singular", "root": "ד.ר.כ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ויזה", "nikkud": None, "transliteration": "вИза", "translation_ru": "виза", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מזוודה", "nikkud": None, "transliteration": "мизвадА", "translation_ru": "чемодан", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מלון", "nikkud": None, "transliteration": "малОн", "translation_ru": "гостиница, отель", "pos": "noun", "gender": "m", "number": "singular", "root": "ל.ו.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "הזמנה", "nikkud": None, "transliteration": "hазманА", "translation_ru": "бронирование, заказ", "pos": "noun", "gender": "f", "number": "singular", "root": "ז.מ.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ביטוח", "nikkud": None, "transliteration": "битУах", "translation_ru": "страховка", "pos": "noun", "gender": "m", "number": "singular", "root": "ב.ט.ח", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מדריך", "nikkud": None, "transliteration": "мадрИх", "translation_ru": "гид, путеводитель", "pos": "noun", "gender": "m", "number": "singular", "root": "ד.ר.כ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "סיור", "nikkud": None, "transliteration": "сиЮр", "translation_ru": "экскурсия, тур", "pos": "noun", "gender": "m", "number": "singular", "root": "ס.י.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אטרקציה", "nikkud": None, "transliteration": "атракцИя", "translation_ru": "достопримечательность", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חוף", "nikkud": None, "transliteration": "хоф", "translation_ru": "пляж, берег", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בריכה", "nikkud": None, "transliteration": "брехА", "translation_ru": "бассейн", "pos": "noun", "gender": "f", "number": "singular", "root": "ב.ר.כ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מסלול", "nikkud": None, "transliteration": "маслУль", "translation_ru": "маршрут, трасса", "pos": "noun", "gender": "m", "number": "singular", "root": "ס.ל.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מפה", "nikkud": None, "transliteration": "мапА", "translation_ru": "карта (географическая)", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מזג אוויר", "nikkud": None, "transliteration": "мЕзег авИр", "translation_ru": "погода", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שער", "nikkud": None, "transliteration": "шАар", "translation_ru": "ворота; выход (на посадку)", "pos": "noun", "gender": "m", "number": "singular", "root": "ש.ע.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "נחיתה", "nikkud": None, "transliteration": "нехитА", "translation_ru": "посадка (самолёта)", "pos": "noun", "gender": "f", "number": "singular", "root": "נ.ח.ת", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "המראה", "nikkud": None, "transliteration": "hамраА", "translation_ru": "взлёт", "pos": "noun", "gender": "f", "number": "singular", "root": "מ.ר.א", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "טרמינל", "nikkud": None, "transliteration": "терминАль", "translation_ru": "терминал", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מכס", "nikkud": None, "transliteration": "мЕхес", "translation_ru": "таможня", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עיכוב", "nikkud": None, "transliteration": "икУв", "translation_ru": "задержка", "pos": "noun", "gender": "m", "number": "singular", "root": "ע.כ.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ביטול", "nikkud": None, "transliteration": "битУль", "translation_ru": "отмена", "pos": "noun", "gender": "m", "number": "singular", "root": "ב.ט.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חניה", "nikkud": None, "transliteration": "ханайА", "translation_ru": "парковка, стоянка", "pos": "noun", "gender": "f", "number": "singular", "root": "ח.נ.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "השכרה", "nikkud": None, "transliteration": "hаскарА", "translation_ru": "аренда, прокат", "pos": "noun", "gender": "f", "number": "singular", "root": "ש.כ.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מוזיאון", "nikkud": None, "transliteration": "музеОн", "translation_ru": "музей", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תערוכה", "nikkud": None, "transliteration": "таарухА", "translation_ru": "выставка", "pos": "noun", "gender": "f", "number": "singular", "root": "ע.ר.כ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "הופעה", "nikkud": None, "transliteration": "hофаА", "translation_ru": "представление, концерт", "pos": "noun", "gender": "f", "number": "singular", "root": "י.פ.ע", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כניסה", "nikkud": None, "transliteration": "книсА", "translation_ru": "вход", "pos": "noun", "gender": "f", "number": "singular", "root": "כ.נ.ס", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "יציאה", "nikkud": None, "transliteration": "йециА", "translation_ru": "выход", "pos": "noun", "gender": "f", "number": "singular", "root": "י.צ.א", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אוהל", "nikkud": None, "transliteration": "Оhель", "translation_ru": "палатка", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שביל", "nikkud": None, "transliteration": "швиль", "translation_ru": "тропа, тропинка", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "טיול", "nikkud": None, "transliteration": "тиЮль", "translation_ru": "поход, путешествие", "pos": "noun", "gender": "m", "number": "singular", "root": "ט.י.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "צימר", "nikkud": None, "transliteration": "цИмер", "translation_ru": "загородный домик (цимер)", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אכסניה", "nikkud": None, "transliteration": "ахсанИя", "translation_ru": "хостел, общежитие", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "נופש", "nikkud": None, "transliteration": "нОфеш", "translation_ru": "отдых, курорт", "pos": "noun", "gender": "m", "number": "singular", "root": "נ.פ.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תיירות", "nikkud": None, "transliteration": "таярУт", "translation_ru": "туризм", "pos": "noun", "gender": "f", "number": "singular", "root": "ת.י.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תייר", "nikkud": None, "transliteration": "таяР", "translation_ru": "турист", "pos": "noun", "gender": "m", "number": "singular", "root": "ת.י.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מזכרת", "nikkud": None, "transliteration": "мазкЕрет", "translation_ru": "сувенир", "pos": "noun", "gender": "f", "number": "singular", "root": "ז.כ.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "צלילה", "nikkud": None, "transliteration": "цлилА", "translation_ru": "дайвинг, погружение", "pos": "noun", "gender": "f", "number": "singular", "root": "צ.ל.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "גלישה", "nikkud": None, "transliteration": "глишА", "translation_ru": "серфинг", "pos": "noun", "gender": "f", "number": "singular", "root": "ג.ל.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שייט", "nikkud": None, "transliteration": "шАйит", "translation_ru": "круиз, плавание", "pos": "noun", "gender": "m", "number": "singular", "root": "ש.י.ט", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "קמפינג", "nikkud": None, "transliteration": "кЭмпинг", "translation_ru": "кемпинг", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לארוז", "nikkud": None, "transliteration": "лээрОз", "translation_ru": "паковать", "pos": "verb", "gender": None, "number": None, "root": "א.ר.ז", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "להזמין", "nikkud": None, "transliteration": "леhазмИн", "translation_ru": "заказывать, бронировать", "pos": "verb", "gender": None, "number": None, "root": "ז.מ.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לבטל", "nikkud": None, "transliteration": "леватЭль", "translation_ru": "отменять", "pos": "verb", "gender": None, "number": None, "root": "ב.ט.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לטייל", "nikkud": None, "transliteration": "летайЭль", "translation_ru": "путешествовать, гулять", "pos": "verb", "gender": None, "number": None, "root": "ט.י.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "להמריא", "nikkud": None, "transliteration": "леhамрИ", "translation_ru": "взлетать", "pos": "verb", "gender": None, "number": None, "root": "מ.ר.א", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לנחות", "nikkud": None, "transliteration": "линхОт", "translation_ru": "приземляться", "pos": "verb", "gender": None, "number": None, "root": "נ.ח.ת", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לצלם", "nikkud": None, "transliteration": "лецалЭм", "translation_ru": "фотографировать", "pos": "verb", "gender": None, "number": None, "root": "צ.ל.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. Покупки и деньги — Shopping & Money (45 words)
# ══════════════════════════════════════════════════════════════════════════════

SHOPPING_MONEY = [
    {"hebrew": "מחיר", "nikkud": None, "transliteration": "мехИр", "translation_ru": "цена", "pos": "noun", "gender": "m", "number": "singular", "root": "מ.ח.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "הנחה", "nikkud": None, "transliteration": "hанахА", "translation_ru": "скидка", "pos": "noun", "gender": "f", "number": "singular", "root": "נ.ח.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מבצע", "nikkud": None, "transliteration": "мивцА", "translation_ru": "акция, распродажа", "pos": "noun", "gender": "m", "number": "singular", "root": "ב.צ.ע", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "קנייה", "nikkud": None, "transliteration": "книйА", "translation_ru": "покупка", "pos": "noun", "gender": "f", "number": "singular", "root": "ק.נ.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "החזר", "nikkud": None, "transliteration": "hэхзЭр", "translation_ru": "возврат (денег)", "pos": "noun", "gender": "m", "number": "singular", "root": "ח.ז.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ערבות", "nikkud": None, "transliteration": "аравУт", "translation_ru": "гарантия, залог", "pos": "noun", "gender": "f", "number": "singular", "root": "ע.ר.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תשלום", "nikkud": None, "transliteration": "ташлУм", "translation_ru": "оплата, платёж", "pos": "noun", "gender": "m", "number": "singular", "root": "ש.ל.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מזומן", "nikkud": None, "transliteration": "мезумАн", "translation_ru": "наличные", "pos": "noun", "gender": "m", "number": "singular", "root": "ז.מ.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "העברה", "nikkud": None, "transliteration": "hааварА", "translation_ru": "перевод (денежный)", "pos": "noun", "gender": "f", "number": "singular", "root": "ע.ב.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חיסכון", "nikkud": None, "transliteration": "хисахОн", "translation_ru": "сбережения, накопления", "pos": "noun", "gender": "m", "number": "singular", "root": "ח.ס.כ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "הלוואה", "nikkud": None, "transliteration": "hалваА", "translation_ru": "кредит, ссуда", "pos": "noun", "gender": "f", "number": "singular", "root": "ל.ו.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ריבית", "nikkud": None, "transliteration": "рибИт", "translation_ru": "процент (банковский)", "pos": "noun", "gender": "f", "number": "singular", "root": "ר.ב.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חשבון בנק", "nikkud": None, "transliteration": "хешбОн банк", "translation_ru": "банковский счёт", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כרטיס אשראי", "nikkud": None, "transliteration": "картИс ашрАй", "translation_ru": "кредитная карта", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עודף", "nikkud": None, "transliteration": "одЭф", "translation_ru": "сдача (деньги)", "pos": "noun", "gender": "m", "number": "singular", "root": "ע.ד.ף", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מס", "nikkud": None, "transliteration": "мас", "translation_ru": "налог", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מע״מ", "nikkud": None, "transliteration": "маАм", "translation_ru": "НДС", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "קניון", "nikkud": None, "transliteration": "каньОн", "translation_ru": "торговый центр", "pos": "noun", "gender": "m", "number": "singular", "root": "ק.נ.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חנות", "nikkud": None, "transliteration": "ханУт", "translation_ru": "магазин", "pos": "noun", "gender": "f", "number": "singular", "root": "ח.נ.ת", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שוק", "nikkud": None, "transliteration": "шук", "translation_ru": "рынок", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "קופה", "nikkud": None, "transliteration": "купА", "translation_ru": "касса", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עגלה", "nikkud": None, "transliteration": "агалА", "translation_ru": "тележка (в магазине)", "pos": "noun", "gender": "f", "number": "singular", "root": "ע.ג.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שקית", "nikkud": None, "transliteration": "сакИт", "translation_ru": "пакет", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מידה", "nikkud": None, "transliteration": "мидА", "translation_ru": "размер", "pos": "noun", "gender": "f", "number": "singular", "root": "מ.ד.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תווית", "nikkud": None, "transliteration": "тавИт", "translation_ru": "этикетка, бирка", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אחריות", "nikkud": None, "transliteration": "ахраЮт", "translation_ru": "гарантия, ответственность", "pos": "noun", "gender": "f", "number": "singular", "root": "א.ח.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "משלוח", "nikkud": None, "transliteration": "мишлОах", "translation_ru": "доставка", "pos": "noun", "gender": "m", "number": "singular", "root": "ש.ל.ח", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חבילה", "nikkud": None, "transliteration": "хавилА", "translation_ru": "посылка, пакет", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כספומט", "nikkud": None, "transliteration": "каспомАт", "translation_ru": "банкомат", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שער חליפין", "nikkud": None, "transliteration": "шАар халифИн", "translation_ru": "обменный курс", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מטבע", "nikkud": None, "transliteration": "матбЭа", "translation_ru": "монета; валюта", "pos": "noun", "gender": "m", "number": "singular", "root": "ט.ב.ע", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שטר", "nikkud": None, "transliteration": "штар", "translation_ru": "купюра", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ארנק", "nikkud": None, "transliteration": "арнАк", "translation_ru": "кошелёк", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תקציר", "nikkud": None, "transliteration": "такцИр", "translation_ru": "выписка (банковская)", "pos": "noun", "gender": "m", "number": "singular", "root": "ק.צ.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לקנות", "nikkud": None, "transliteration": "ликнОт", "translation_ru": "покупать", "pos": "verb", "gender": None, "number": None, "root": "ק.נ.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "למכור", "nikkud": None, "transliteration": "лимкОр", "translation_ru": "продавать", "pos": "verb", "gender": None, "number": None, "root": "מ.כ.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לשלם", "nikkud": None, "transliteration": "лешалЭм", "translation_ru": "платить", "pos": "verb", "gender": None, "number": None, "root": "ש.ל.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לחסוך", "nikkud": None, "transliteration": "лахсОх", "translation_ru": "экономить, копить", "pos": "verb", "gender": None, "number": None, "root": "ח.ס.כ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "להלוות", "nikkud": None, "transliteration": "леhалвОт", "translation_ru": "одалживать", "pos": "verb", "gender": None, "number": None, "root": "ל.ו.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "להחזיר", "nikkud": None, "transliteration": "леhахзИр", "translation_ru": "возвращать", "pos": "verb", "gender": None, "number": None, "root": "ח.ז.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "להחליף", "nikkud": None, "transliteration": "леhахлИф", "translation_ru": "обменивать", "pos": "verb", "gender": None, "number": None, "root": "ח.ל.ף", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "למדוד", "nikkud": None, "transliteration": "лимдОд", "translation_ru": "мерить, измерять", "pos": "verb", "gender": None, "number": None, "root": "מ.ד.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "יקר", "nikkud": None, "transliteration": "якАр", "translation_ru": "дорогой", "pos": "adj", "gender": "m", "number": "singular", "root": "י.ק.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "זול", "nikkud": None, "transliteration": "золь", "translation_ru": "дешёвый", "pos": "adj", "gender": "m", "number": "singular", "root": "ז.ל.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חינם", "nikkud": None, "transliteration": "хинАм", "translation_ru": "бесплатно", "pos": "adv", "gender": None, "number": None, "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. Эмоции и характер — Emotions & Character (45 words)
# ══════════════════════════════════════════════════════════════════════════════

EMOTIONS_CHARACTER = [
    {"hebrew": "גאווה", "nikkud": None, "transliteration": "гаавА", "translation_ru": "гордость", "pos": "noun", "gender": "f", "number": "singular", "root": "ג.א.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "קנאה", "nikkud": None, "transliteration": "кинА", "translation_ru": "зависть, ревность", "pos": "noun", "gender": "f", "number": "singular", "root": "ק.נ.א", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בושה", "nikkud": None, "transliteration": "бушА", "translation_ru": "стыд", "pos": "noun", "gender": "f", "number": "singular", "root": "ב.ו.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אכזבה", "nikkud": None, "transliteration": "ахзавА", "translation_ru": "разочарование", "pos": "noun", "gender": "f", "number": "singular", "root": "כ.ז.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "הפתעה", "nikkud": None, "transliteration": "hафтаА", "translation_ru": "сюрприз, удивление", "pos": "noun", "gender": "f", "number": "singular", "root": "פ.ת.ע", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "דאגה", "nikkud": None, "transliteration": "деагА", "translation_ru": "беспокойство, забота", "pos": "noun", "gender": "f", "number": "singular", "root": "ד.א.ג", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "חרדה", "nikkud": None, "transliteration": "харадА", "translation_ru": "тревога", "pos": "noun", "gender": "f", "number": "singular", "root": "ח.ר.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ביטחון", "nikkud": None, "transliteration": "битахОн", "translation_ru": "уверенность; безопасность", "pos": "noun", "gender": "m", "number": "singular", "root": "ב.ט.ח", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אמונה", "nikkud": None, "transliteration": "эмунА", "translation_ru": "вера", "pos": "noun", "gender": "f", "number": "singular", "root": "א.מ.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "סבלנות", "nikkud": None, "transliteration": "савланУт", "translation_ru": "терпение", "pos": "noun", "gender": "f", "number": "singular", "root": "ס.ב.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "נדיבות", "nikkud": None, "transliteration": "недивУт", "translation_ru": "щедрость", "pos": "noun", "gender": "f", "number": "singular", "root": "נ.ד.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אמיץ", "nikkud": None, "transliteration": "амИц", "translation_ru": "смелый, храбрый", "pos": "adj", "gender": "m", "number": "singular", "root": "א.מ.ץ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ביישן", "nikkud": None, "transliteration": "байшАн", "translation_ru": "застенчивый", "pos": "adj", "gender": "m", "number": "singular", "root": "ב.י.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עיקש", "nikkud": None, "transliteration": "икЭш", "translation_ru": "упрямый", "pos": "adj", "gender": "m", "number": "singular", "root": "ע.ק.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "סקרן", "nikkud": None, "transliteration": "сакрАн", "translation_ru": "любопытный", "pos": "adj", "gender": "m", "number": "singular", "root": "ס.ק.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אופטימי", "nikkud": None, "transliteration": "оптИми", "translation_ru": "оптимистичный", "pos": "adj", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "פסימי", "nikkud": None, "transliteration": "песИми", "translation_ru": "пессимистичный", "pos": "adj", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "רגיש", "nikkud": None, "transliteration": "рагИш", "translation_ru": "чувствительный", "pos": "adj", "gender": "m", "number": "singular", "root": "ר.ג.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אדיש", "nikkud": None, "transliteration": "адИш", "translation_ru": "равнодушный", "pos": "adj", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עצבני", "nikkud": None, "transliteration": "ацбанИ", "translation_ru": "нервный, раздражительный", "pos": "adj", "gender": "m", "number": "singular", "root": "ע.צ.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "רגוע", "nikkud": None, "transliteration": "рагУа", "translation_ru": "спокойный", "pos": "adj", "gender": "m", "number": "singular", "root": "ר.ג.ע", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עליז", "nikkud": None, "transliteration": "алИз", "translation_ru": "весёлый, жизнерадостный", "pos": "adj", "gender": "m", "number": "singular", "root": "ע.ל.ז", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עצוב", "nikkud": None, "transliteration": "ацУв", "translation_ru": "грустный", "pos": "adj", "gender": "m", "number": "singular", "root": "ע.צ.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כועס", "nikkud": None, "transliteration": "коЭс", "translation_ru": "сердитый, злой", "pos": "adj", "gender": "m", "number": "singular", "root": "כ.ע.ס", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מאוכזב", "nikkud": None, "transliteration": "меухзАв", "translation_ru": "разочарованный", "pos": "adj", "gender": "m", "number": "singular", "root": "כ.ז.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מופתע", "nikkud": None, "transliteration": "муфтА", "translation_ru": "удивлённый", "pos": "adj", "gender": "m", "number": "singular", "root": "פ.ת.ע", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מודאג", "nikkud": None, "transliteration": "мудАг", "translation_ru": "обеспокоенный", "pos": "adj", "gender": "m", "number": "singular", "root": "ד.א.ג", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "נלהב", "nikkud": None, "transliteration": "нильhАв", "translation_ru": "восторженный, увлечённый", "pos": "adj", "gender": "m", "number": "singular", "root": "ל.ה.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "גמיש", "nikkud": None, "transliteration": "гамИш", "translation_ru": "гибкий", "pos": "adj", "gender": "m", "number": "singular", "root": "ג.מ.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אחראי", "nikkud": None, "transliteration": "ахраИ", "translation_ru": "ответственный", "pos": "adj", "gender": "m", "number": "singular", "root": "א.ח.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "יצירתי", "nikkud": None, "transliteration": "йециратИ", "translation_ru": "творческий", "pos": "adj", "gender": "m", "number": "singular", "root": "י.צ.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שמחה", "nikkud": None, "transliteration": "симхА", "translation_ru": "радость", "pos": "noun", "gender": "f", "number": "singular", "root": "ש.מ.ח", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עצב", "nikkud": None, "transliteration": "Эцев", "translation_ru": "грусть, печаль", "pos": "noun", "gender": "m", "number": "singular", "root": "ע.צ.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כעס", "nikkud": None, "transliteration": "кАас", "translation_ru": "гнев, злость", "pos": "noun", "gender": "m", "number": "singular", "root": "כ.ע.ס", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "פחד", "nikkud": None, "transliteration": "пАхад", "translation_ru": "страх", "pos": "noun", "gender": "m", "number": "singular", "root": "פ.ח.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תקווה", "nikkud": None, "transliteration": "тиквА", "translation_ru": "надежда", "pos": "noun", "gender": "f", "number": "singular", "root": "ק.ו.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אהבה", "nikkud": None, "transliteration": "аhавА", "translation_ru": "любовь", "pos": "noun", "gender": "f", "number": "singular", "root": "א.ה.ב", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שנאה", "nikkud": None, "transliteration": "синА", "translation_ru": "ненависть", "pos": "noun", "gender": "f", "number": "singular", "root": "ש.נ.א", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בדידות", "nikkud": None, "transliteration": "бдидУт", "translation_ru": "одиночество", "pos": "noun", "gender": "f", "number": "singular", "root": "ב.ד.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "התרגשות", "nikkud": None, "transliteration": "hитрагшУт", "translation_ru": "волнение, возбуждение", "pos": "noun", "gender": "f", "number": "singular", "root": "ר.ג.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לכעוס", "nikkud": None, "transliteration": "лихОс", "translation_ru": "злиться, сердиться", "pos": "verb", "gender": None, "number": None, "root": "כ.ע.ס", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לפחד", "nikkud": None, "transliteration": "лефахЭд", "translation_ru": "бояться", "pos": "verb", "gender": None, "number": None, "root": "פ.ח.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "להתרגש", "nikkud": None, "transliteration": "леhитрагЭш", "translation_ru": "волноваться", "pos": "verb", "gender": None, "number": None, "root": "ר.ג.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לדאוג", "nikkud": None, "transliteration": "лидОг", "translation_ru": "беспокоиться, заботиться", "pos": "verb", "gender": None, "number": None, "root": "ד.א.ג", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "להתבייש", "nikkud": None, "transliteration": "леhитбайЭш", "translation_ru": "стесняться, стыдиться", "pos": "verb", "gender": None, "number": None, "root": "ב.י.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. Общественные места и услуги — Public Places & Services (45 words)
# ══════════════════════════════════════════════════════════════════════════════

PUBLIC_SERVICES = [
    {"hebrew": "עירייה", "nikkud": None, "transliteration": "ирийА", "translation_ru": "муниципалитет, мэрия", "pos": "noun", "gender": "f", "number": "singular", "root": "ע.י.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "משטרה", "nikkud": None, "transliteration": "миштарА", "translation_ru": "полиция", "pos": "noun", "gender": "f", "number": "singular", "root": "ש.ט.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כבאים", "nikkud": None, "transliteration": "кабаИм", "translation_ru": "пожарные", "pos": "noun", "gender": "m", "number": "plural", "root": "כ.ב.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אמבולנס", "nikkud": None, "transliteration": "амбулАнс", "translation_ru": "скорая помощь", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ביטוח לאומי", "nikkud": None, "transliteration": "битУах леумИ", "translation_ru": "национальное страхование", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "משרד הפנים", "nikkud": None, "transliteration": "мисрАд hапнИм", "translation_ru": "МВД", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "רשות", "nikkud": None, "transliteration": "решУт", "translation_ru": "ведомство, управление", "pos": "noun", "gender": "f", "number": "singular", "root": "ר.ש.י", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "פקיד", "nikkud": None, "transliteration": "пакИд", "translation_ru": "чиновник, клерк", "pos": "noun", "gender": "m", "number": "singular", "root": "פ.ק.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "טופס", "nikkud": None, "transliteration": "тОфес", "translation_ru": "бланк, анкета", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תור", "nikkud": None, "transliteration": "тор", "translation_ru": "очередь", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תלונה", "nikkud": None, "transliteration": "тлунА", "translation_ru": "жалоба", "pos": "noun", "gender": "f", "number": "singular", "root": "ל.ו.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בקשה", "nikkud": None, "transliteration": "бакашА", "translation_ru": "просьба, заявление", "pos": "noun", "gender": "f", "number": "singular", "root": "ב.ק.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "אישור", "nikkud": None, "transliteration": "ишУр", "translation_ru": "разрешение, подтверждение", "pos": "noun", "gender": "m", "number": "singular", "root": "א.ש.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "רישיון", "nikkud": None, "transliteration": "ришайОн", "translation_ru": "лицензия, права (водительские)", "pos": "noun", "gender": "m", "number": "singular", "root": "ר.ש.י", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תעודה", "nikkud": None, "transliteration": "теудА", "translation_ru": "удостоверение, свидетельство", "pos": "noun", "gender": "f", "number": "singular", "root": "ע.ו.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "תעודת זהות", "nikkud": None, "transliteration": "теудАт зеhУт", "translation_ru": "удостоверение личности", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "דואר", "nikkud": None, "transliteration": "дОар", "translation_ru": "почта", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ספרייה", "nikkud": None, "transliteration": "сифриЯ", "translation_ru": "библиотека", "pos": "noun", "gender": "f", "number": "singular", "root": "ס.פ.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בית משפט", "nikkud": None, "transliteration": "бейт мишпАт", "translation_ru": "суд", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "שגרירות", "nikkud": None, "transliteration": "шагрирУт", "translation_ru": "посольство", "pos": "noun", "gender": "f", "number": "singular", "root": "ש.ג.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "קונסוליה", "nikkud": None, "transliteration": "консулИя", "translation_ru": "консульство", "pos": "noun", "gender": "f", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מכבי אש", "nikkud": None, "transliteration": "мехабЭй эш", "translation_ru": "пожарная служба", "pos": "noun", "gender": "m", "number": "plural", "root": "כ.ב.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "הצלה", "nikkud": None, "transliteration": "hацалА", "translation_ru": "спасение; служба спасения", "pos": "noun", "gender": "f", "number": "singular", "root": "נ.צ.ל", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בנק", "nikkud": None, "transliteration": "банк", "translation_ru": "банк", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "סניף", "nikkud": None, "transliteration": "снИф", "translation_ru": "филиал, отделение", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מתנ״ס", "nikkud": None, "transliteration": "матнАс", "translation_ru": "общинный центр", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "גן ציבורי", "nikkud": None, "transliteration": "ган цибурИ", "translation_ru": "общественный парк", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מגרש משחקים", "nikkud": None, "transliteration": "мигрАш мисхакИм", "translation_ru": "детская площадка", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בית כנסת", "nikkud": None, "transliteration": "бейт кнЕсет", "translation_ru": "синагога", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מסגד", "nikkud": None, "transliteration": "мисгАд", "translation_ru": "мечеть", "pos": "noun", "gender": "m", "number": "singular", "root": "ס.ג.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "כנסייה", "nikkud": None, "transliteration": "кнесиЯ", "translation_ru": "церковь", "pos": "noun", "gender": "f", "number": "singular", "root": "כ.נ.ס", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "בית עלמין", "nikkud": None, "transliteration": "бейт алмИн", "translation_ru": "кладбище", "pos": "noun", "gender": "m", "number": "singular", "root": None, "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "מוסד", "nikkud": None, "transliteration": "мосАд", "translation_ru": "учреждение, институт", "pos": "noun", "gender": "m", "number": "singular", "root": "י.ס.ד", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לפנות", "nikkud": None, "transliteration": "лифнОт", "translation_ru": "обращаться (в инстанцию)", "pos": "verb", "gender": None, "number": None, "root": "פ.נ.ה", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "להגיש", "nikkud": None, "transliteration": "леhагИш", "translation_ru": "подавать (заявление)", "pos": "verb", "gender": None, "number": None, "root": "נ.ג.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לחתום", "nikkud": None, "transliteration": "лахтОм", "translation_ru": "подписывать", "pos": "verb", "gender": None, "number": None, "root": "ח.ת.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "למלא", "nikkud": None, "transliteration": "лемалЭ", "translation_ru": "заполнять (бланк)", "pos": "verb", "gender": None, "number": None, "root": "מ.ל.א", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "להתלונן", "nikkud": None, "transliteration": "леhитлонЭн", "translation_ru": "жаловаться", "pos": "verb", "gender": None, "number": None, "root": "ל.ו.נ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לאשר", "nikkud": None, "transliteration": "леашЭр", "translation_ru": "утверждать, подтверждать", "pos": "verb", "gender": None, "number": None, "root": "א.ש.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לחדש", "nikkud": None, "transliteration": "лехадЭш", "translation_ru": "обновлять, продлевать", "pos": "verb", "gender": None, "number": None, "root": "ח.ד.ש", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לדווח", "nikkud": None, "transliteration": "ледавЭах", "translation_ru": "сообщать, докладывать", "pos": "verb", "gender": None, "number": None, "root": "ד.ו.ח", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "להירשם", "nikkud": None, "transliteration": "леhирашЭм", "translation_ru": "регистрироваться, записываться", "pos": "verb", "gender": None, "number": None, "root": "ר.ש.מ", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "לערער", "nikkud": None, "transliteration": "леарЭр", "translation_ru": "обжаловать, подавать апелляцию", "pos": "verb", "gender": None, "number": None, "root": "ע.ר.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "ציבורי", "nikkud": None, "transliteration": "цибурИ", "translation_ru": "общественный, публичный", "pos": "adj", "gender": "m", "number": "singular", "root": "צ.ב.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
    {"hebrew": "עירוני", "nikkud": None, "transliteration": "иронИ", "translation_ru": "городской, муниципальный", "pos": "adj", "gender": "m", "number": "singular", "root": "ע.י.ר", "frequency_rank": 2, "level_id": 2, "audio_url": None, "image_url": None},
]

# ══════════════════════════════════════════════════════════════════════════════
# Collect all Hebrew values for downgrade DELETE
# ══════════════════════════════════════════════════════════════════════════════

ALL_WORDS = WORK_OFFICE + HEALTH_MEDICINE + TRAVEL_LEISURE + SHOPPING_MONEY + EMOTIONS_CHARACTER + PUBLIC_SERVICES


def upgrade() -> None:
    # Reset sequence to avoid conflicts
    op.execute(
        "SELECT setval('words_id_seq', GREATEST((SELECT COALESCE(MAX(id), 0) FROM words), 1))"
    )

    op.bulk_insert(words_table, WORK_OFFICE)
    op.bulk_insert(words_table, HEALTH_MEDICINE)
    op.bulk_insert(words_table, TRAVEL_LEISURE)
    op.bulk_insert(words_table, SHOPPING_MONEY)
    op.bulk_insert(words_table, EMOTIONS_CHARACTER)
    op.bulk_insert(words_table, PUBLIC_SERVICES)

    # Fix sequence after bulk insert
    op.execute(
        "SELECT setval('words_id_seq', (SELECT COALESCE(MAX(id), 0) FROM words))"
    )


def downgrade() -> None:
    # Build a list of hebrew values to delete exactly the words added by this migration
    hebrew_values = [w["hebrew"] for w in ALL_WORDS]
    placeholders = ", ".join(f"'{v}'" for v in hebrew_values)
    op.execute(f"DELETE FROM words WHERE hebrew IN ({placeholders}) AND level_id = 2")

    # Fix sequence after deletion
    op.execute(
        "SELECT setval('words_id_seq', GREATEST((SELECT COALESCE(MAX(id), 0) FROM words), 1))"
    )
