"""Replace ~391 remaining template exercises with diverse content.

152a: Replace 78 fill_blank "הם למדו על ה_____" templates
152b: Replace 78 match_pairs with generic לימוד/ידע fillers
152c: Replace ~157 translate_ru_he templates (очень важна / весь семестр)
152d: Replace 78 dictation "נלמד באוניברסיטאות רבות" templates
152e: Remove 3 duplicate match_pairs exercises

Revision ID: 152
Revises: 151
"""

import json
import random
from alembic import op
import sqlalchemy as sa

revision = "152"
down_revision = "151"
branch_labels = None
depends_on = None

_j = lambda d: json.dumps(d, ensure_ascii=False)

# ── Template pools ───────────────────────────────────────────────────────

# 152a: Fill-blank sentence templates (Hebrew, slot = _____)
FB_TEMPLATES = [
    "ה_____ הוא מושג מרכזי בתחום",
    "הסטודנטים חקרו את ה_____ בעבודה",
    "המרצה הסביר את ה_____ בשיעור",
    "ל_____ יש חשיבות רבה בתחום הזה",
    "ה_____ מופיע בטקסטים אקדמיים רבים",
    "חשוב להבין את ה_____ כדי להתקדם",
    "בספר הזה מוסבר ה_____ בצורה ברורה",
    "ה_____ משמש כבסיס להבנת הנושא",
    "הניסוי הדגים את ה_____ בצורה מעשית",
    "ה_____ קשור למושגים נוספים בתחום",
    "לימוד ה_____ דורש תשומת לב מיוחדת",
    "ה_____ התפתח עם השנים והשתנה מאוד",
    "הבנת ה_____ חיונית למחקר מודרני",
    "מומחים דנים ב_____ בכנסים אקדמיים",
    "ה_____ משפיע על תחומים רבים בחיים",
]

FB_HINTS = [
    "ключевое понятие темы",
    "центральный термин",
    "основное слово урока",
    "тематический термин",
    "главное понятие",
]

# 152b: Match-pairs — Hebrew↔Russian topic word pairs (per-topic)
MATCH_PAIR_SETS = [
    # Set 0: General academic
    {"pairs_left": ["מחקר", "ניסוי", "תוצאה", "מסקנה"],
     "pairs_right": ["исследование", "эксперимент", "результат", "вывод"],
     "matches": {"מחקר": "исследование", "ניסוי": "эксперимент", "תוצאה": "результат", "מסקנה": "вывод"}},
    # Set 1: Education
    {"pairs_left": ["שיעור", "מבחן", "ציון", "תעודה"],
     "pairs_right": ["урок", "экзамен", "оценка", "аттестат"],
     "matches": {"שיעור": "урок", "מבחן": "экзамен", "ציון": "оценка", "תעודה": "аттестат"}},
    # Set 2: Science
    {"pairs_left": ["תהליך", "מערכת", "חומר", "אנרגיה"],
     "pairs_right": ["процесс", "система", "вещество", "энергия"],
     "matches": {"תהליך": "процесс", "מערכת": "система", "חומר": "вещество", "אנרגיה": "энергия"}},
    # Set 3: History
    {"pairs_left": ["תקופה", "אירוע", "מנהיג", "מלחמה"],
     "pairs_right": ["эпоха", "событие", "лидер", "война"],
     "matches": {"תקופה": "эпоха", "אירוע": "событие", "מנהיג": "лидер", "מלחמה": "война"}},
    # Set 4: Literature
    {"pairs_left": ["סופר", "שיר", "סיפור", "דמות"],
     "pairs_right": ["писатель", "стихотворение", "рассказ", "персонаж"],
     "matches": {"סופר": "писатель", "שיר": "стихотворение", "סיפור": "рассказ", "דמות": "персонаж"}},
    # Set 5: Technology
    {"pairs_left": ["תוכנה", "מסך", "רשת", "נתונים"],
     "pairs_right": ["программа", "экран", "сеть", "данные"],
     "matches": {"תוכנה": "программа", "מסך": "экран", "רשת": "сеть", "נתונים": "данные"}},
    # Set 6: Nature
    {"pairs_left": ["צמח", "בעל חיים", "סביבה", "אקלים"],
     "pairs_right": ["растение", "животное", "среда", "климат"],
     "matches": {"צמח": "растение", "בעל חיים": "животное", "סביבה": "среда", "אקלים": "климат"}},
    # Set 7: Economy
    {"pairs_left": ["שוק", "מחיר", "ייצור", "סחר"],
     "pairs_right": ["рынок", "цена", "производство", "торговля"],
     "matches": {"שוק": "рынок", "מחיר": "цена", "ייצור": "производство", "סחר": "торговля"}},
    # Set 8: Society
    {"pairs_left": ["חברה", "תרבות", "חוק", "זכות"],
     "pairs_right": ["общество", "культура", "закон", "право"],
     "matches": {"חברה": "общество", "תרבות": "культура", "חוק": "закон", "זכות": "право"}},
    # Set 9: Health
    {"pairs_left": ["בריאות", "תרופה", "רופא", "טיפול"],
     "pairs_right": ["здоровье", "лекарство", "врач", "лечение"],
     "matches": {"בריאות": "здоровье", "תרופה": "лекарство", "רופא": "врач", "טיפול": "лечение"}},
    # Set 10: Geography
    {"pairs_left": ["עיר", "מדינה", "הר", "נהר"],
     "pairs_right": ["город", "государство", "гора", "река"],
     "matches": {"עיר": "город", "מדינה": "государство", "הר": "гора", "נהר": "река"}},
    # Set 11: Art
    {"pairs_left": ["ציור", "פסל", "תערוכה", "אמן"],
     "pairs_right": ["картина", "скульптура", "выставка", "художник"],
     "matches": {"ציור": "картина", "פסל": "скульптура", "תערוכה": "выставка", "אמן": "художник"}},
    # Set 12: Philosophy
    {"pairs_left": ["מחשבה", "רעיון", "ערך", "מוסר"],
     "pairs_right": ["мысль", "идея", "ценность", "нравственность"],
     "matches": {"מחשבה": "мысль", "רעיון": "идея", "ערך": "ценность", "מוסר": "нравственность"}},
    # Set 13: Media
    {"pairs_left": ["חדשות", "כתבה", "עיתון", "תקשורת"],
     "pairs_right": ["новости", "статья", "газета", "СМИ"],
     "matches": {"חדשות": "новости", "כתבה": "статья", "עיתון": "газета", "תקשורת": "СМИ"}},
    # Set 14: Law
    {"pairs_left": ["משפט", "שופט", "עדות", "פסק דין"],
     "pairs_right": ["суд", "судья", "показание", "приговор"],
     "matches": {"משפט": "суд", "שופט": "судья", "עדות": "показание", "פסק דין": "приговор"}},
    # Set 15: Psychology
    {"pairs_left": ["התנהגות", "רגש", "זיכרון", "תודעה"],
     "pairs_right": ["поведение", "эмоция", "память", "сознание"],
     "matches": {"התנהגות": "поведение", "רגש": "эмоция", "זיכרון": "память", "תודעה": "сознание"}},
]

# 152c: Translation (Russian→Hebrew) sentence templates
TRANSLATE_TEMPLATES_A = [
    "Эта тема имеет большое значение для студентов",
    "Мы изучали этот вопрос на прошлой неделе",
    "Результаты исследования были очень интересными",
    "Профессор объяснил основные принципы",
    "Студенты написали работу по этой теме",
    "В этой области произошли значительные изменения",
    "Данный подход широко используется в науке",
    "Этот метод был разработан в прошлом веке",
    "Учёные провели серию важных экспериментов",
    "Книга рассказывает об истории этого понятия",
    "Мы обсуждали этот вопрос на семинаре",
    "Преподаватель рекомендовал прочитать эту статью",
    "Этот термин часто встречается в научных текстах",
    "В последние годы интерес к этой теме вырос",
    "Работа была выполнена на высоком уровне",
]

TRANSLATE_ANSWERS_A = [
    "הנושא הזה חשוב מאוד לסטודנטים",
    "למדנו את השאלה הזו בשבוע שעבר",
    "תוצאות המחקר היו מעניינות מאוד",
    "הפרופסור הסביר את העקרונות הבסיסיים",
    "הסטודנטים כתבו עבודה בנושא הזה",
    "בתחום הזה חלו שינויים משמעותיים",
    "הגישה הזו נמצאת בשימוש נרחב במדע",
    "השיטה הזו פותחה במאה הקודמת",
    "המדענים ערכו סדרה של ניסויים חשובים",
    "הספר מספר על ההיסטוריה של המושג הזה",
    "דנו בשאלה הזו בסמינר",
    "המרצה המליץ לקרוא את המאמר הזה",
    "המונח הזה מופיע לעיתים קרובות בטקסטים מדעיים",
    "בשנים האחרונות העניין בנושא הזה גדל",
    "העבודה בוצעה ברמה גבוהה",
]

TRANSLATE_TEMPLATES_B = [
    "Студенты готовились к экзамену по этому предмету",
    "Исследователи опубликовали новые результаты",
    "В библиотеке есть много книг на эту тему",
    "Лекция была очень содержательной и полезной",
    "Учебный план включает несколько важных тем",
    "Каждый студент должен сдать итоговый экзамен",
    "Эта теория помогает объяснить сложные явления",
    "Научная статья была опубликована в журнале",
    "Практическое занятие прошло в лаборатории",
    "Домашнее задание нужно сдать до конца недели",
    "Этот курс рассчитан на два семестра",
    "Группа студентов представила свой проект",
    "На конференции обсуждали новые открытия",
    "Экзаменационная работа состоит из трёх частей",
    "Преподаватель дал полезные советы для подготовки",
]

TRANSLATE_ANSWERS_B = [
    "הסטודנטים התכוננו למבחן במקצוע הזה",
    "החוקרים פרסמו תוצאות חדשות",
    "בספרייה יש ספרים רבים על הנושא הזה",
    "ההרצאה הייתה מלאת תוכן ומועילה",
    "תוכנית הלימודים כוללת כמה נושאים חשובים",
    "כל סטודנט חייב לעבור מבחן סופי",
    "התיאוריה הזו עוזרת להסביר תופעות מורכבות",
    "המאמר המדעי פורסם בכתב עת",
    "השיעור המעשי התקיים במעבדה",
    "את שיעורי הבית צריך להגיש עד סוף השבוע",
    "הקורס הזה מתוכנן לשני סמסטרים",
    "קבוצת סטודנטים הציגה את הפרויקט שלה",
    "בכנס דנו בגילויים חדשים",
    "עבודת הבחינה מורכבת משלושה חלקים",
    "המרצה נתן עצות מועילות להכנה",
]

# 152d: Dictation sentence templates
DICTATION_TEMPLATES = [
    "הסטודנטים למדו נושאים חדשים בקורס",
    "המרצה הציג את החומר בצורה מעניינת",
    "הספרייה פתוחה כל יום מהבוקר עד הערב",
    "המחקר הראה תוצאות מפתיעות ומעניינות",
    "כדי להצליח צריך ללמוד ולתרגל הרבה",
    "הפרויקט הזה דרש עבודה קשה וארוכה",
    "המבחן יכלול שאלות מכל החומר הנלמד",
    "חשוב לקרוא את כל הטקסטים לפני השיעור",
    "הכיתה התמלאה בסטודנטים מתחילת הסמסטר",
    "העבודה האקדמית דורשת דיוק ותשומת לב",
    "המעבדה מצוידת בכלים מודרניים ומתקדמים",
    "הציון הסופי מורכב ממבחן ועבודות בית",
    "הספר הזה נכתב על ידי מומחה מוכר בתחום",
    "הסמינר עסק בנושאים אקטואליים וחשובים",
    "כל סטודנט קיבל משוב אישי על העבודה",
]

DICTATION_HINTS = [
    "Прослушайте и запишите предложение",
    "Запишите услышанное",
    "Диктант: запишите на иврите",
    "Внимательно прослушайте и запишите",
    "Запишите предложение целиком",
]


def _extract_keyword(conn, lesson_id):
    """Extract topic keyword from a lesson's existing exercises."""
    row = conn.execute(sa.text("""
        SELECT prompt_json FROM exercises
        WHERE lesson_id = :lid AND type = 'multiple_choice'
        ORDER BY id LIMIT 1
    """), {"lid": lesson_id}).fetchone()
    if row:
        prompt = json.loads(row[0]) if isinstance(row[0], str) else row[0]
        options = prompt.get("options", [])
        if options:
            return options[0]
    return "הנושא"


def upgrade() -> None:
    conn = op.get_bind()
    rng = random.Random(152)

    exercises_table = sa.table(
        "exercises",
        sa.column("lesson_id", sa.Integer),
        sa.column("type", sa.String),
        sa.column("difficulty", sa.Integer),
        sa.column("prompt_json", sa.Text),
        sa.column("answer_json", sa.Text),
        sa.column("explanation_json", sa.Text),
        sa.column("points", sa.Integer),
    )

    # ── 152a: Replace fill_blank "הם למדו על ה_____" templates ───────────

    fb_rows = conn.execute(sa.text("""
        SELECT DISTINCT lesson_id FROM exercises
        WHERE type = 'fill_blank'
        AND prompt_json::text LIKE '%הם למדו על ה_____%'
    """)).fetchall()
    fb_lesson_ids = [r[0] for r in fb_rows]

    # Get keywords before deleting
    fb_keywords = {}
    for lid in fb_lesson_ids:
        fb_keywords[lid] = _extract_keyword(conn, lid)

    d1 = conn.execute(sa.text("""
        DELETE FROM exercises
        WHERE type = 'fill_blank'
        AND prompt_json::text LIKE '%הם למדו על ה_____%'
    """))
    print(f"152a: Deleted {d1.rowcount} template fill_blank exercises")

    fb_inserted = 0
    for i, lid in enumerate(sorted(fb_lesson_ids)):
        keyword = fb_keywords.get(lid, "הנושא")
        template = FB_TEMPLATES[i % len(FB_TEMPLATES)]
        hint = FB_HINTS[i % len(FB_HINTS)]

        op.bulk_insert(exercises_table, [{
            "lesson_id": lid, "type": "fill_blank", "difficulty": 2, "points": 10,
            "prompt_json": _j({"sentence": template, "hint": hint}),
            "answer_json": _j({"correct": keyword, "alternatives": []}),
            "explanation_json": _j({"text": f"{keyword} — {hint}."}),
        }])
        fb_inserted += 1
    print(f"152a: Inserted {fb_inserted} diverse fill_blank replacements")

    # ── 152b: Replace match_pairs with generic לימוד/ידע fillers ─────────

    mp_rows = conn.execute(sa.text("""
        SELECT DISTINCT lesson_id FROM exercises
        WHERE type = 'match_pairs'
        AND (prompt_json::text LIKE '%לימוד%' OR prompt_json::text LIKE '%ידע%')
        AND prompt_json::text LIKE '%pairs_left%'
    """)).fetchall()
    mp_lesson_ids = [r[0] for r in mp_rows]

    d2 = conn.execute(sa.text("""
        DELETE FROM exercises
        WHERE type = 'match_pairs'
        AND (prompt_json::text LIKE '%לימוד%' OR prompt_json::text LIKE '%ידע%')
        AND prompt_json::text LIKE '%pairs_left%'
    """))
    print(f"152b: Deleted {d2.rowcount} template match_pairs exercises")

    mp_inserted = 0
    for i, lid in enumerate(sorted(mp_lesson_ids)):
        pair_set = MATCH_PAIR_SETS[i % len(MATCH_PAIR_SETS)]

        op.bulk_insert(exercises_table, [{
            "lesson_id": lid, "type": "match_pairs", "difficulty": 2, "points": 10,
            "prompt_json": _j({"pairs_left": pair_set["pairs_left"], "pairs_right": pair_set["pairs_right"]}),
            "answer_json": _j({"matches": pair_set["matches"]}),
            "explanation_json": _j({"text": "Соедините слова с их переводами."}),
        }])
        mp_inserted += 1
    print(f"152b: Inserted {mp_inserted} diverse match_pairs replacements")

    # ── 152c: Replace translate_ru_he templates ──────────────────────────

    # Pattern A: "очень важна в данной области"
    tr_a_rows = conn.execute(sa.text("""
        SELECT DISTINCT lesson_id FROM exercises
        WHERE type = 'translate_ru_he'
        AND prompt_json::text LIKE '%очень важна в данной области%'
    """)).fetchall()
    tr_a_ids = [r[0] for r in tr_a_rows]

    d3a = conn.execute(sa.text("""
        DELETE FROM exercises
        WHERE type = 'translate_ru_he'
        AND prompt_json::text LIKE '%очень важна в данной области%'
    """))
    print(f"152c: Deleted {d3a.rowcount} 'очень важна' translate templates")

    tr_a_inserted = 0
    for i, lid in enumerate(sorted(tr_a_ids)):
        idx = i % len(TRANSLATE_TEMPLATES_A)
        ru_text = TRANSLATE_TEMPLATES_A[idx]
        he_text = TRANSLATE_ANSWERS_A[idx]

        op.bulk_insert(exercises_table, [{
            "lesson_id": lid, "type": "translate_ru_he", "difficulty": 2, "points": 10,
            "prompt_json": _j({"text": ru_text}),
            "answer_json": _j({"correct": he_text, "accept": [he_text]}),
            "explanation_json": _j({"text": f"{ru_text} → {he_text}"}),
        }])
        tr_a_inserted += 1

    # Pattern B: "весь семестр"
    tr_b_rows = conn.execute(sa.text("""
        SELECT DISTINCT lesson_id FROM exercises
        WHERE type = 'translate_ru_he'
        AND prompt_json::text LIKE '%весь семестр%'
    """)).fetchall()
    tr_b_ids = [r[0] for r in tr_b_rows]

    d3b = conn.execute(sa.text("""
        DELETE FROM exercises
        WHERE type = 'translate_ru_he'
        AND prompt_json::text LIKE '%весь семестр%'
    """))
    print(f"152c: Deleted {d3b.rowcount} 'весь семестр' translate templates")

    tr_b_inserted = 0
    for i, lid in enumerate(sorted(tr_b_ids)):
        idx = i % len(TRANSLATE_TEMPLATES_B)
        ru_text = TRANSLATE_TEMPLATES_B[idx]
        he_text = TRANSLATE_ANSWERS_B[idx]

        op.bulk_insert(exercises_table, [{
            "lesson_id": lid, "type": "translate_ru_he", "difficulty": 2, "points": 10,
            "prompt_json": _j({"text": ru_text}),
            "answer_json": _j({"correct": he_text, "accept": [he_text]}),
            "explanation_json": _j({"text": f"{ru_text} → {he_text}"}),
        }])
        tr_b_inserted += 1

    print(f"152c: Inserted {tr_a_inserted + tr_b_inserted} diverse translate replacements")

    # ── 152d: Replace dictation "נלמד באוניברסיטאות רבות" templates ───────

    dc_rows = conn.execute(sa.text("""
        SELECT DISTINCT lesson_id FROM exercises
        WHERE type = 'dictation'
        AND prompt_json::text LIKE '%נלמד באוניברסיטאות רבות%'
    """)).fetchall()
    dc_lesson_ids = [r[0] for r in dc_rows]

    d4 = conn.execute(sa.text("""
        DELETE FROM exercises
        WHERE type = 'dictation'
        AND prompt_json::text LIKE '%נלמד באוניברסיטאות רבות%'
    """))
    print(f"152d: Deleted {d4.rowcount} template dictation exercises")

    dc_inserted = 0
    for i, lid in enumerate(sorted(dc_lesson_ids)):
        idx = i % len(DICTATION_TEMPLATES)
        sentence = DICTATION_TEMPLATES[idx]
        hint = DICTATION_HINTS[i % len(DICTATION_HINTS)]

        op.bulk_insert(exercises_table, [{
            "lesson_id": lid, "type": "dictation", "difficulty": 2, "points": 10,
            "prompt_json": _j({"audio_text": sentence, "hint": hint}),
            "answer_json": _j({"correct": sentence}),
            "explanation_json": _j({"text": f"Правильный ответ: {sentence}"}),
        }])
        dc_inserted += 1
    print(f"152d: Inserted {dc_inserted} diverse dictation replacements")

    # ── 152e: Remove duplicate match_pairs ────────────────────────────────

    dup_rows = conn.execute(sa.text("""
        SELECT e1.id
        FROM exercises e1
        JOIN exercises e2 ON e1.lesson_id = e2.lesson_id
            AND e1.type = e2.type
            AND e1.prompt_json::text = e2.prompt_json::text
            AND e1.id > e2.id
        WHERE e1.type = 'match_pairs'
    """)).fetchall()
    dup_ids = [r[0] for r in dup_rows]

    if dup_ids:
        conn.execute(sa.text(
            "DELETE FROM exercises WHERE id = ANY(:ids)"
        ), {"ids": dup_ids})
    print(f"152e: Removed {len(dup_ids)} duplicate match_pairs exercises")


def downgrade() -> None:
    conn = op.get_bind()

    # Delete replacements by their unique patterns
    for template in FB_TEMPLATES:
        pattern = template.split("_____")[0] if "_____" in template else template[:20]
        if pattern:
            conn.execute(sa.text(
                "DELETE FROM exercises WHERE type = 'fill_blank' AND prompt_json::text LIKE :pat"
            ), {"pat": f"%{pattern}%"})

    for template in DICTATION_TEMPLATES:
        pattern = template[:25]
        conn.execute(sa.text(
            "DELETE FROM exercises WHERE type = 'dictation' AND prompt_json::text LIKE :pat"
        ), {"pat": f"%{pattern}%"})

    # Note: cannot restore original template exercises or deleted duplicates.
