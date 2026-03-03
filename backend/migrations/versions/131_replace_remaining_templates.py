"""Replace ~391 remaining template exercises with diverse content.

131a: Replace 78 fill_blank "הם למדו על ה_____" templates
131b: Replace 78 match_pairs with generic לימוד/ידע fillers
131c: Replace 157 translate_ru_he templates ("очень важна в данной области" + "весь семестр")
131d: Replace 78 dictation "נלמד באוניברסיטאות רבות" templates
131e: Remove 3 duplicate match_pairs exercises

Revision ID: 131
Revises: 130
"""

import json
import random
from alembic import op
import sqlalchemy as sa

revision = "131"
down_revision = "130"
branch_labels = None
depends_on = None

_j = lambda d: json.dumps(d, ensure_ascii=False)

# ── Fill-blank sentence templates (15+) ───────────────────────────────────
FB_TEMPLATES = [
    "ה_____ הוא מושג מרכזי בתחום",
    "הסטודנטים חקרו את ה_____ בעבודה",
    "ה_____ מתואר בפרק הראשון של הספר",
    "אנחנו לומדים על _____ בכיתה",
    "ה_____ משחק תפקיד חשוב בהבנת הנושא",
    "המרצה הרחיב על ה_____ בהרצאה",
    "יש קשר בין ה_____ לבין נושאים אחרים",
    "ה_____ נחקר רבות בשנים האחרונות",
    "הבנת ה_____ דורשת ידע בסיסי בתחום",
    "ה_____ מוזכר בטקסטים אקדמיים רבים",
    "חקירת ה_____ חשפה תובנות חדשות",
    "ה_____ מהווה בסיס לדיון מעמיק",
    "בעזרת ה_____ אפשר להבין את התמונה הרחבה",
    "הספר מציג את ה_____ בצורה ברורה",
    "ה_____ קשור לתחומים רבים בחיים",
    "הכרת ה_____ חיונית להצלחה בקורס",
]

FB_HINTS = [
    "מילת מפתח בנושא השיעור",
    "מושג מרכזי שלמדנו",
    "ключевое слово урока",
    "основной термин темы",
    "центральное понятие",
]

# ── Match pairs: general Hebrew↔Russian academic vocabulary ───────────────
# These are used as fallback when lesson vocabulary is insufficient
MATCH_PAIRS_POOL = [
    ("מחקר", "исследование"),
    ("ניתוח", "анализ"),
    ("תיאוריה", "теория"),
    ("שיטה", "метод"),
    ("מסקנה", "вывод"),
    ("דוגמה", "пример"),
    ("הסבר", "объяснение"),
    ("שאלה", "вопрос"),
    ("תשובה", "ответ"),
    ("בעיה", "проблема"),
    ("פתרון", "решение"),
    ("תוצאה", "результат"),
    ("מטרה", "цель"),
    ("תכנית", "план"),
    ("הגדרה", "определение"),
    ("נושא", "тема"),
    ("רעיון", "идея"),
    ("ערך", "ценность"),
    ("מבנה", "структура"),
    ("תהליך", "процесс"),
    ("השפעה", "влияние"),
    ("גישה", "подход"),
    ("עיקרון", "принцип"),
    ("היבט", "аспект"),
    ("תופעה", "явление"),
    ("מגמה", "тенденция"),
    ("כלי", "инструмент"),
    ("סגנון", "стиль"),
    ("מסורת", "традиция"),
    ("חידוש", "новшество"),
]

# ── Translate RU→HE sentence templates (15+) ─────────────────────────────
TRANSLATE_TEMPLATES = [
    "Напишите на иврите: {meaning} — это важный термин в данной теме",
    "Переведите: Мы изучали {meaning} на занятии",
    "Переведите на иврит: {meaning} играет важную роль в этой области",
    "Напишите на иврите: Студенты обсуждали {meaning} на семинаре",
    "Переведите: Понимание слова {meaning} помогает в учёбе",
    "Напишите на иврите: {meaning} встречается в академических текстах",
    "Переведите на иврит: Преподаватель объяснил значение {meaning}",
    "Напишите на иврите: {meaning} — ключевое понятие в этом уроке",
    "Переведите: Исследователи изучают {meaning} уже много лет",
    "Напишите на иврите: {meaning} связано с другими понятиями темы",
    "Переведите: В этом тексте подробно описано {meaning}",
    "Напишите на иврите: {meaning} имеет несколько значений",
    "Переведите на иврит: Знание {meaning} необходимо для экзамена",
    "Напишите на иврите: {meaning} часто используется в современном иврите",
    "Переведите: Мы начали урок с обсуждения {meaning}",
    "Напишите на иврите: {meaning} можно найти в словаре",
]

# Corresponding Hebrew answer templates (same index as TRANSLATE_TEMPLATES)
TRANSLATE_ANSWERS = [
    "{word} הוא מונח חשוב בנושא הזה",
    "למדנו על {word} בשיעור",
    "{word} ממלא תפקיד חשוב בתחום הזה",
    "הסטודנטים דנו ב{word} בסמינר",
    "הבנת המילה {word} עוזרת בלימודים",
    "{word} מופיע בטקסטים אקדמיים",
    "המרצה הסביר את המשמעות של {word}",
    "{word} הוא מושג מרכזי בשיעור הזה",
    "חוקרים חוקרים את ה{word} כבר שנים רבות",
    "{word} קשור למושגים אחרים בנושא",
    "בטקסט הזה מתואר {word} בפירוט",
    "ל{word} יש כמה משמעויות",
    "ידיעת {word} נחוצה למבחן",
    "{word} משמש לעיתים קרובות בעברית מודרנית",
    "התחלנו את השיעור בדיון על {word}",
    "אפשר למצוא את {word} במילון",
]

# ── Dictation sentence templates (15+, different from migration 127) ──────
DC_TEMPLATES = [
    "ה{word} נלמד בקורסים שונים באוניברסיטה",
    "חשוב להבין את ה{word} לפני המבחן",
    "הנושא של ה{word} מעניין סטודנטים רבים",
    "המרצה הציג את ה{word} בצורה מרתקת",
    "ניתן ללמוד על ה{word} גם באופן עצמאי",
    "ה{word} הוא נושא מרכזי בתוכנית הלימודים",
    "הסטודנטים כתבו עבודה על ה{word}",
    "ה{word} קשור לנושאים שלמדנו בשבוע שעבר",
    "הספרייה מכילה ספרים רבים על ה{word}",
    "לימוד ה{word} דורש סבלנות והתמדה",
    "ה{word} הוא חלק בלתי נפרד מהלימודים",
    "אנחנו נמשיך ללמוד על ה{word} בשבוע הבא",
    "ה{word} מופיע בכל ספרי הלימוד בתחום",
    "הכרת ה{word} מרחיבה את אופקי הידע שלנו",
    "הדיון על ה{word} היה מעניין ומאתגר",
    "ה{word} תורם להבנה מעמיקה של הנושא",
]

DC_HINTS = [
    "Прослушайте и запишите предложение",
    "Запишите услышанное на иврите",
    "Диктант: внимательно запишите",
    "Прослушайте и запишите точно",
    "Запишите предложение на иврите",
]

DC_EXPLANATIONS = [
    "Обратите внимание на определённый артикль ה перед словом {word}.",
    "Предлог ב означает «в», предлог ל означает «к/для».",
    "{word} — ключевое слово. Запомните его написание.",
    "Обратите внимание на порядок слов в предложении.",
    "Проверьте правильность написания слова {word}.",
]


def _get_lesson_context(conn, lesson_id):
    """Extract keyword and vocabulary from a lesson's non-template exercises."""
    # Try to get keyword from existing MC exercises
    mc_row = conn.execute(sa.text("""
        SELECT prompt_json, answer_json FROM exercises
        WHERE lesson_id = :lid AND type = 'multiple_choice'
        AND prompt_json::text NOT LIKE '%человек%'
        ORDER BY id LIMIT 1
    """), {"lid": lesson_id}).fetchone()

    keyword_he = "הנושא"
    keyword_ru = "тема"

    if mc_row:
        prompt = json.loads(mc_row[0]) if isinstance(mc_row[0], str) else mc_row[0]
        answer = json.loads(mc_row[1]) if isinstance(mc_row[1], str) else mc_row[1]
        question = prompt.get("question", "")

        # Extract Hebrew word from question like "Что означает X?"
        if "означает " in question:
            keyword_he = question.split("означает ")[1].rstrip("?").strip()
        elif "слово " in question:
            parts = question.split("слово ")
            if len(parts) > 1:
                keyword_he = parts[1].split(" ")[0].rstrip("?").strip()

        correct = answer.get("correct", "")
        if correct:
            keyword_ru = correct

    # Also try to get vocab words from the lesson for match_pairs
    vocab_rows = conn.execute(sa.text("""
        SELECT prompt_json, answer_json FROM exercises
        WHERE lesson_id = :lid
        AND type IN ('multiple_choice', 'fill_blank')
        AND prompt_json IS NOT NULL
        ORDER BY id
    """), {"lid": lesson_id}).fetchall()

    vocab_pairs = []
    seen_he = set()
    for vrow in vocab_rows:
        vp = json.loads(vrow[0]) if isinstance(vrow[0], str) else vrow[0]
        va = json.loads(vrow[1]) if isinstance(vrow[1], str) else vrow[1]

        # From MC: extract word and meaning
        q = vp.get("question", "")
        correct = va.get("correct", "")
        if "означает " in q and correct:
            he_word = q.split("означает ")[1].rstrip("?").strip()
            if he_word not in seen_he:
                vocab_pairs.append((he_word, correct))
                seen_he.add(he_word)

        # From fill_blank: keyword and its meaning
        fb_answer = va.get("correct", "")
        if fb_answer and fb_answer not in seen_he:
            # We don't have the Russian translation here, skip
            pass

    return {
        "keyword_he": keyword_he,
        "keyword_ru": keyword_ru,
        "vocab_pairs": vocab_pairs,
    }


def upgrade() -> None:
    conn = op.get_bind()
    rng = random.Random(131)

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

    # ── 131a: Replace fill_blank "הם למדו על ה_____" templates ────────────
    fb_rows = conn.execute(sa.text("""
        SELECT id, lesson_id FROM exercises
        WHERE type = 'fill_blank'
        AND prompt_json::text LIKE '%הם למדו על ה_____%'
    """)).fetchall()

    fb_lesson_ids = {}
    for row in fb_rows:
        fb_lesson_ids.setdefault(row[1], []).append(row[0])

    # Delete templates
    if fb_rows:
        conn.execute(sa.text("""
            DELETE FROM exercises
            WHERE type = 'fill_blank'
            AND prompt_json::text LIKE '%הם למדו על ה_____%'
        """))

    fb_inserted = 0
    for i, (lid, ex_ids) in enumerate(sorted(fb_lesson_ids.items())):
        ctx = _get_lesson_context(conn, lid)
        keyword = ctx["keyword_he"]
        topic = ctx["keyword_ru"]

        for j, _ex_id in enumerate(ex_ids):
            tmpl_idx = (i * 3 + j) % len(FB_TEMPLATES)
            hint_idx = (i + j) % len(FB_HINTS)
            sentence = FB_TEMPLATES[tmpl_idx]

            op.bulk_insert(exercises_table, [{
                "lesson_id": lid,
                "type": "fill_blank",
                "difficulty": 2,
                "points": 10,
                "prompt_json": _j({"sentence": sentence, "hint": FB_HINTS[hint_idx]}),
                "answer_json": _j({"correct": keyword, "alternatives": []}),
                "explanation_json": _j({"text": f"{keyword} ({topic}) — ключевое слово урока."}),
            }])
            fb_inserted += 1

    print(f"131a: Replaced {len(fb_rows)} fill_blank templates → {fb_inserted} new exercises")

    # ── 131b: Replace match_pairs with generic לימוד/ידע fillers ──────────
    mp_rows = conn.execute(sa.text("""
        SELECT id, lesson_id FROM exercises
        WHERE type = 'match_pairs'
        AND prompt_json::text LIKE '%לימוד%'
        AND prompt_json::text LIKE '%ידע%'
    """)).fetchall()

    mp_lesson_ids = {}
    for row in mp_rows:
        mp_lesson_ids.setdefault(row[1], []).append(row[0])

    if mp_rows:
        conn.execute(sa.text("""
            DELETE FROM exercises
            WHERE type = 'match_pairs'
            AND prompt_json::text LIKE '%לימוד%'
            AND prompt_json::text LIKE '%ידע%'
        """))

    mp_inserted = 0
    for i, (lid, ex_ids) in enumerate(sorted(mp_lesson_ids.items())):
        ctx = _get_lesson_context(conn, lid)
        vocab = ctx["vocab_pairs"]

        for j, _ex_id in enumerate(ex_ids):
            # Build 4-5 pairs from lesson vocab + pool
            pairs = []
            used = set()

            # First add lesson vocabulary pairs
            for he, ru in vocab:
                if len(pairs) >= 5:
                    break
                if he not in used:
                    pairs.append((he, ru))
                    used.add(he)

            # Fill remainder from pool (offset by lesson to get variety)
            pool_offset = (i * 5 + j * 3) % len(MATCH_PAIRS_POOL)
            for k in range(len(MATCH_PAIRS_POOL)):
                if len(pairs) >= 4:
                    break
                pair = MATCH_PAIRS_POOL[(pool_offset + k) % len(MATCH_PAIRS_POOL)]
                if pair[0] not in used:
                    pairs.append(pair)
                    used.add(pair[0])

            # Ensure at least 4 pairs
            if len(pairs) < 4:
                for pair in MATCH_PAIRS_POOL:
                    if pair[0] not in used:
                        pairs.append(pair)
                        used.add(pair[0])
                    if len(pairs) >= 4:
                        break

            pairs_left = [p[0] for p in pairs]
            pairs_right = [p[1] for p in pairs]
            matches = {p[0]: p[1] for p in pairs}

            # Shuffle right side so it's not trivially aligned
            shuffled_right = list(pairs_right)
            rng.shuffle(shuffled_right)

            op.bulk_insert(exercises_table, [{
                "lesson_id": lid,
                "type": "match_pairs",
                "difficulty": 2,
                "points": 15,
                "prompt_json": _j({"pairs_left": pairs_left, "pairs_right": shuffled_right}),
                "answer_json": _j({"matches": matches}),
                "explanation_json": _j({"text": "Соедините каждое слово на иврите с его переводом на русский."}),
            }])
            mp_inserted += 1

    print(f"131b: Replaced {len(mp_rows)} match_pairs templates → {mp_inserted} new exercises")

    # ── 131c: Replace translate_ru_he templates ───────────────────────────
    # Pattern 1: "очень важна в данной области"
    tr1_rows = conn.execute(sa.text("""
        SELECT id, lesson_id FROM exercises
        WHERE type = 'translate_ru_he'
        AND prompt_json::text LIKE '%очень важна в данной области%'
    """)).fetchall()

    # Pattern 2: "весь семестр"
    tr2_rows = conn.execute(sa.text("""
        SELECT id, lesson_id FROM exercises
        WHERE type = 'translate_ru_he'
        AND prompt_json::text LIKE '%весь семестр%'
    """)).fetchall()

    tr_lesson_ids = {}
    for row in tr1_rows + tr2_rows:
        tr_lesson_ids.setdefault(row[1], []).append(row[0])

    if tr1_rows:
        conn.execute(sa.text("""
            DELETE FROM exercises
            WHERE type = 'translate_ru_he'
            AND prompt_json::text LIKE '%очень важна в данной области%'
        """))
    if tr2_rows:
        conn.execute(sa.text("""
            DELETE FROM exercises
            WHERE type = 'translate_ru_he'
            AND prompt_json::text LIKE '%весь семестр%'
        """))

    tr_inserted = 0
    for i, (lid, ex_ids) in enumerate(sorted(tr_lesson_ids.items())):
        ctx = _get_lesson_context(conn, lid)
        word = ctx["keyword_he"]
        meaning = ctx["keyword_ru"]

        for j, _ex_id in enumerate(ex_ids):
            tmpl_idx = (i * 3 + j) % len(TRANSLATE_TEMPLATES)
            ru_sentence = TRANSLATE_TEMPLATES[tmpl_idx].format(meaning=meaning, word=word)
            he_answer = TRANSLATE_ANSWERS[tmpl_idx].format(word=word, meaning=meaning)

            op.bulk_insert(exercises_table, [{
                "lesson_id": lid,
                "type": "translate_ru_he",
                "difficulty": 3,
                "points": 15,
                "prompt_json": _j({"sentence": ru_sentence}),
                "answer_json": _j({"correct": he_answer, "accept": [he_answer]}),
                "explanation_json": _j({"text": f"{word} = {meaning}"}),
            }])
            tr_inserted += 1

    print(f"131c: Replaced {len(tr1_rows) + len(tr2_rows)} translate_ru_he templates → {tr_inserted} new exercises")

    # ── 131d: Replace dictation "נלמד באוניברסיטאות רבות" templates ────────
    dc_rows = conn.execute(sa.text("""
        SELECT id, lesson_id FROM exercises
        WHERE type = 'dictation'
        AND prompt_json::text LIKE '%נלמד באוניברסיטאות רבות%'
    """)).fetchall()

    dc_lesson_ids = {}
    for row in dc_rows:
        dc_lesson_ids.setdefault(row[1], []).append(row[0])

    if dc_rows:
        conn.execute(sa.text("""
            DELETE FROM exercises
            WHERE type = 'dictation'
            AND prompt_json::text LIKE '%נלמד באוניברסיטאות רבות%'
        """))

    dc_inserted = 0
    for i, (lid, ex_ids) in enumerate(sorted(dc_lesson_ids.items())):
        ctx = _get_lesson_context(conn, lid)
        keyword = ctx["keyword_he"]

        for j, _ex_id in enumerate(ex_ids):
            tmpl_idx = (i * 2 + j) % len(DC_TEMPLATES)
            hint_idx = (i + j) % len(DC_HINTS)
            expl_idx = (i + j) % len(DC_EXPLANATIONS)

            sentence = DC_TEMPLATES[tmpl_idx].format(word=keyword)
            explanation = DC_EXPLANATIONS[expl_idx].format(word=keyword)

            op.bulk_insert(exercises_table, [{
                "lesson_id": lid,
                "type": "dictation",
                "difficulty": 3,
                "points": 15,
                "prompt_json": _j({"audio_text": sentence, "hint": DC_HINTS[hint_idx]}),
                "answer_json": _j({"correct": sentence}),
                "explanation_json": _j({"text": explanation}),
            }])
            dc_inserted += 1

    print(f"131d: Replaced {len(dc_rows)} dictation templates → {dc_inserted} new exercises")

    # ── 131e: Remove duplicate match_pairs ────────────────────────────────
    dup_rows = conn.execute(sa.text("""
        SELECT e1.id
        FROM exercises e1
        JOIN exercises e2
          ON e1.lesson_id = e2.lesson_id
          AND e1.type = e2.type
          AND e1.prompt_json::text = e2.prompt_json::text
          AND e1.id > e2.id
        WHERE e1.type = 'match_pairs'
    """)).fetchall()

    if dup_rows:
        dup_ids = [r[0] for r in dup_rows]
        conn.execute(sa.text(
            "DELETE FROM exercises WHERE id = ANY(:ids)"
        ), {"ids": dup_ids})

    print(f"131e: Removed {len(dup_rows)} duplicate match_pairs exercises")


def downgrade() -> None:
    # Cannot restore original template exercises — they were broken content.
    # Re-run seed migrations (082, 083) if needed.
    pass
