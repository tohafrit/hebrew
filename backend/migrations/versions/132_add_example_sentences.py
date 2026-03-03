"""Add example sentences for 6,117 words that have none.

Generates 1 sentence per word using POS-aware and level-aware templates.
- Nouns, verbs, adjectives get specialized templates
- Other POS types get generic templates
- Levels 1-2 use simple sentences, levels 4-6 use academic/complex sentences

Revision ID: 132
Revises: 131
"""

import json
import random
from alembic import op
import sqlalchemy as sa

revision = "132"
down_revision = "131"
branch_labels = None
depends_on = None

# ── Noun templates ────────────────────────────────────────────────────────

NOUN_TEMPLATES_SIMPLE = [
    # (hebrew_template, russian_template)
    ("ה{word} הוא דבר חשוב", "{tr} — это важная вещь"),
    ("ראיתי {word} יפה", "Я видел(а) красивый {tr}"),
    ("אנחנו צריכים {word}", "Нам нужен {tr}"),
    ("יש לי {word} חדש", "У меня есть новый {tr}"),
    ("ה{word} על השולחן", "{tr} на столе"),
    ("אני אוהב את ה{word}", "Я люблю {tr}"),
    ("זה {word} טוב מאוד", "Это очень хороший {tr}"),
    ("ה{word} שלי גדול", "Мой {tr} большой"),
    ("אין לי {word}", "У меня нет {tr}"),
    ("איפה ה{word}?", "Где {tr}?"),
    ("ה{word} הזה יפה", "Этот {tr} красивый"),
    ("קניתי {word} חדש", "Я купил(а) новый {tr}"),
    ("ה{word} נמצא כאן", "{tr} находится здесь"),
    ("תביא לי את ה{word}", "Принеси мне {tr}"),
    ("ה{word} שלך מעניין", "Твой {tr} интересный"),
]

NOUN_TEMPLATES_ADVANCED = [
    ("ה{word} הוא חלק חשוב מהחיים", "{tr} — важная часть жизни"),
    ("ה{word} משחק תפקיד מרכזי בחברה", "{tr} играет центральную роль в обществе"),
    ("מחקרים רבים עוסקים ב{word}", "Многие исследования посвящены {tr}"),
    ("ה{word} נחשב לנושא מורכב", "{tr} считается сложной темой"),
    ("הבנת ה{word} דורשת ידע מעמיק", "Понимание {tr} требует глубоких знаний"),
    ("ה{word} התפתח במהלך השנים", "{tr} развивался на протяжении лет"),
    ("לא ניתן להתעלם מחשיבות ה{word}", "Нельзя игнорировать важность {tr}"),
    ("ה{word} מהווה בסיס לדיון אקדמי", "{tr} составляет основу академической дискуссии"),
    ("ישנם היבטים שונים של ה{word}", "Существуют различные аспекты {tr}"),
    ("ה{word} קשור לתחומים רבים", "{tr} связан со многими областями"),
    ("ניתוח ה{word} חושף תובנות חדשות", "Анализ {tr} раскрывает новые идеи"),
    ("ה{word} מעורר עניין בקרב חוקרים", "{tr} вызывает интерес у исследователей"),
    ("ה{word} נידון בהרחבה בספרות המקצועית", "{tr} широко обсуждается в профессиональной литературе"),
    ("ההשפעה של ה{word} ניכרת בתרבות", "Влияние {tr} заметно в культуре"),
    ("חקירת ה{word} מובילה לתגליות חשובות", "Исследование {tr} приводит к важным открытиям"),
]

# ── Verb templates ────────────────────────────────────────────────────────

VERB_TEMPLATES_SIMPLE = [
    ("אני אוהב ל{word}", "Я люблю {tr}"),
    ("הם {word} כל יום", "Они {tr} каждый день"),
    ("אנחנו {word} ביחד", "Мы {tr} вместе"),
    ("היא {word} בבוקר", "Она {tr} утром"),
    ("אתה צריך ל{word}", "Тебе нужно {tr}"),
    ("אני רוצה ל{word}", "Я хочу {tr}"),
    ("הילדים {word} בחוץ", "Дети {tr} на улице"),
    ("מתי אתה {word}?", "Когда ты {tr}?"),
    ("אני לא יכול ל{word}", "Я не могу {tr}"),
    ("בוא נ{word} ביחד", "Давай {tr} вместе"),
    ("הוא {word} מהר", "Он {tr} быстро"),
    ("למה את לא {word}?", "Почему ты не {tr}?"),
    ("אני {word} כל בוקר", "Я {tr} каждое утро"),
    ("הם אוהבים ל{word}", "Они любят {tr}"),
    ("חשוב ל{word} נכון", "Важно {tr} правильно"),
]

VERB_TEMPLATES_ADVANCED = [
    ("חשוב ל{word} בצורה נכונה", "Важно {tr} правильным образом"),
    ("הסטודנטים למדו ל{word} באופן עצמאי", "Студенты научились {tr} самостоятельно"),
    ("היכולת ל{word} היא מיומנות חיונית", "Умение {tr} — важный навык"),
    ("אנחנו צריכים ל{word} לפני שנמשיך", "Нам нужно {tr}, прежде чем продолжить"),
    ("המומחים ממליצים ל{word} באופן קבוע", "Эксперты рекомендуют {tr} регулярно"),
    ("לא תמיד קל ל{word}", "Не всегда легко {tr}"),
    ("ניתן ל{word} בדרכים שונות", "Можно {tr} разными способами"),
    ("הם החליטו ל{word} ביחד", "Они решили {tr} вместе"),
    ("עלינו ל{word} בזהירות", "Нам следует {tr} осторожно"),
    ("חוקרים מנסים ל{word} את התופעה", "Исследователи пытаются {tr} это явление"),
    ("הכישרון ל{word} אינו מולד", "Талант {tr} не является врождённым"),
    ("אנשים רבים מעדיפים ל{word} בערב", "Многие люди предпочитают {tr} вечером"),
    ("המטרה היא ל{word} ביעילות", "Цель — {tr} эффективно"),
    ("לאורך ההיסטוריה, אנשים {word}", "На протяжении истории люди {tr}"),
    ("לפני ש{word}, כדאי לתכנן", "Прежде чем {tr}, стоит спланировать"),
]

# ── Adjective templates ───────────────────────────────────────────────────

ADJ_TEMPLATES_SIMPLE = [
    ("הספר הזה מאוד {word}", "Эта книга очень {tr}"),
    ("היא אדם {word}", "Она {tr} человек"),
    ("זה היה יום {word}", "Это был {tr} день"),
    ("הבית הזה {word}", "Этот дом {tr}"),
    ("אני מרגיש {word}", "Я чувствую себя {tr}"),
    ("המזג אוויר {word} היום", "Погода сегодня {tr}"),
    ("התשובה שלך {word}", "Твой ответ {tr}"),
    ("האוכל פה {word}", "Еда здесь {tr}"),
    ("הסרט היה {word}", "Фильм был {tr}"),
    ("הילד הזה {word}", "Этот ребёнок {tr}"),
    ("המוסיקה הזאת {word}", "Эта музыка {tr}"),
    ("הכלב שלי {word}", "Моя собака {tr}"),
    ("הדרך הזאת {word}", "Эта дорога {tr}"),
    ("החדר נראה {word}", "Комната выглядит {tr}"),
    ("זה רעיון {word}", "Это {tr} идея"),
]

ADJ_TEMPLATES_ADVANCED = [
    ("התגלית הזאת {word} במיוחד", "Это открытие особенно {tr}"),
    ("הנושא הזה {word} ומורכב", "Эта тема {tr} и сложная"),
    ("הגישה הזאת {word} לדעת רבים", "Этот подход {tr}, по мнению многих"),
    ("הפתרון שהוצע {word} ביותר", "Предложенное решение наиболее {tr}"),
    ("ההיבט ה{word} של הנושא ראוי לתשומת לב", "{tr} аспект темы заслуживает внимания"),
    ("ניתן לומר שהמצב {word}", "Можно сказать, что ситуация {tr}"),
    ("התוצאות היו {word} מהצפוי", "Результаты оказались {tr}, чем ожидалось"),
    ("הטקסט הזה {word} להבנה", "Этот текст {tr} для понимания"),
    ("המחקר הציג תמונה {word}", "Исследование представило {tr} картину"),
    ("ההשפעה הזאת {word} וארוכת טווח", "Это влияние {tr} и долгосрочное"),
    ("הדיון היה {word} ומעמיק", "Обсуждение было {tr} и глубоким"),
    ("הבעיה {word} ממה שחשבנו", "Проблема оказалась {tr}, чем мы думали"),
    ("הסגנון שלו {word} ומקורי", "Его стиль {tr} и оригинален"),
    ("התהליך {word} אך הכרחי", "Процесс {tr}, но необходимый"),
    ("הפרויקט {word} במיוחד", "Проект особенно {tr}"),
]

# ── Generic templates (for other POS: adverbs, prepositions, etc.) ────────

GENERIC_TEMPLATES_SIMPLE = [
    ("השתמשנו במילה {word} במשפט", "Мы использовали слово {tr} в предложении"),
    ("המילה {word} נפוצה בעברית", "Слово {tr} распространено в иврите"),
    ("למדנו את המילה {word}", "Мы выучили слово {tr}"),
    ("אפשר להשתמש ב{word} כך", "Можно использовать {tr} так"),
    ("{word} — מילה שימושית", "{tr} — полезное слово"),
    ("חשוב לדעת את המילה {word}", "Важно знать слово {tr}"),
    ("המילה {word} קלה לזכירה", "Слово {tr} легко запомнить"),
    ("שמעתי את המילה {word} בשיחה", "Я услышал(а) слово {tr} в разговоре"),
    ("אני משתמש ב{word} לעיתים קרובות", "Я часто использую {tr}"),
    ("המורה לימד אותנו את {word}", "Учитель научил нас слову {tr}"),
    ("ה{word} מופיע בטקסט", "{tr} появляется в тексте"),
    ("הביטוי עם {word} מעניין", "Выражение с {tr} интересное"),
    ("נתרגל את המילה {word}", "Потренируем слово {tr}"),
    ("ה{word} שימושי בחיי היומיום", "{tr} полезно в повседневной жизни"),
    ("כדאי לזכור את {word}", "Стоит запомнить {tr}"),
]

GENERIC_TEMPLATES_ADVANCED = [
    ("השימוש ב{word} נפוץ בשפה האקדמית", "Использование {tr} распространено в академическом языке"),
    ("הביטוי {word} מופיע בטקסטים רבים", "Выражение {tr} встречается во многих текстах"),
    ("הבנת {word} חיונית לקריאת טקסטים", "Понимание {tr} необходимо для чтения текстов"),
    ("המילה {word} בעלת משמעות עמוקה", "Слово {tr} имеет глубокий смысл"),
    ("{word} משמש בהקשרים שונים", "{tr} используется в различных контекстах"),
    ("ניתן למצוא את {word} בספרות", "Можно найти {tr} в литературе"),
    ("השימוש ב{word} משתנה בהתאם להקשר", "Использование {tr} зависит от контекста"),
    ("חוקרי לשון דנים ב{word}", "Лингвисты обсуждают {tr}"),
    ("{word} הוא חלק מאוצר המילים המתקדם", "{tr} — часть продвинутого словарного запаса"),
    ("בטקסט זה {word} מופיע מספר פעמים", "В этом тексте {tr} встречается несколько раз"),
    ("הכרת {word} מעשירה את השפה", "Знание {tr} обогащает язык"),
    ("{word} — ביטוי חשוב בעברית המודרנית", "{tr} — важное выражение в современном иврите"),
    ("שימוש נכון ב{word} מעיד על רמת שפה גבוהה", "Правильное использование {tr} свидетельствует о высоком уровне языка"),
    ("המושג {word} דורש הסבר נוסף", "Понятие {tr} требует дополнительного объяснения"),
    ("ב{word} טמון רעיון מעניין", "В {tr} заложена интересная идея"),
]


def _pick_template(pos, level_id, rng, word_idx):
    """Select appropriate templates based on POS and level."""
    is_advanced = level_id is not None and level_id >= 4

    if pos and pos.lower() in ("noun", "существительное", "n"):
        pool = NOUN_TEMPLATES_ADVANCED if is_advanced else NOUN_TEMPLATES_SIMPLE
    elif pos and pos.lower() in ("verb", "глагол", "v"):
        pool = VERB_TEMPLATES_ADVANCED if is_advanced else VERB_TEMPLATES_SIMPLE
    elif pos and pos.lower() in ("adjective", "adj", "прилагательное", "a"):
        pool = ADJ_TEMPLATES_ADVANCED if is_advanced else ADJ_TEMPLATES_SIMPLE
    else:
        pool = GENERIC_TEMPLATES_ADVANCED if is_advanced else GENERIC_TEMPLATES_SIMPLE

    idx = word_idx % len(pool)
    return pool[idx]


def upgrade() -> None:
    conn = op.get_bind()
    rng = random.Random(132)

    # Find all words without example sentences
    words = conn.execute(sa.text("""
        SELECT w.id, w.hebrew, w.translation_ru, w.pos, w.level_id
        FROM words w
        LEFT JOIN example_sentences es ON es.word_id = w.id
        WHERE es.id IS NULL
        ORDER BY w.id
    """)).fetchall()

    print(f"Found {len(words)} words without example sentences")

    if not words:
        return

    sentences_table = sa.table(
        "example_sentences",
        sa.column("word_id", sa.Integer),
        sa.column("hebrew", sa.Text),
        sa.column("translation_ru", sa.Text),
        sa.column("transliteration", sa.Text),
        sa.column("audio_url", sa.String),
        sa.column("level_id", sa.Integer),
    )

    # Process in batches for efficiency
    BATCH_SIZE = 500
    batch = []
    total = 0

    for i, word_row in enumerate(words):
        word_id = word_row[0]
        hebrew = word_row[1]
        translation_ru = word_row[2]
        pos = word_row[3]
        level_id = word_row[4]

        he_tmpl, ru_tmpl = _pick_template(pos, level_id, rng, i)

        he_sentence = he_tmpl.format(word=hebrew)
        ru_sentence = ru_tmpl.format(tr=translation_ru)

        batch.append({
            "word_id": word_id,
            "hebrew": he_sentence,
            "translation_ru": ru_sentence,
            "transliteration": None,
            "audio_url": None,
            "level_id": level_id,
        })

        if len(batch) >= BATCH_SIZE:
            op.bulk_insert(sentences_table, batch)
            total += len(batch)
            batch = []

    # Insert remaining
    if batch:
        op.bulk_insert(sentences_table, batch)
        total += len(batch)

    print(f"Inserted {total} example sentences for {len(words)} words")


def downgrade() -> None:
    conn = op.get_bind()
    # Delete all sentences that were generated by this migration.
    # These are identifiable as having transliteration = NULL and audio_url = NULL
    # and matching our template patterns. But for safety, we'll just delete
    # sentences for words that would match the original query.
    conn.execute(sa.text("""
        DELETE FROM example_sentences
        WHERE transliteration IS NULL
        AND audio_url IS NULL
        AND id IN (
            SELECT es.id FROM example_sentences es
            JOIN (
                SELECT w.id AS word_id FROM words w
                LEFT JOIN example_sentences es2 ON es2.word_id = w.id
                GROUP BY w.id
                HAVING COUNT(es2.id) = 1
            ) single ON single.word_id = es.word_id
        )
    """))
