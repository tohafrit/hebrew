"""Replace 234 template exercises with diverse content.

Deletes exercises matching these template patterns:
- fill_blank with "חשוב מאוד בתחום הזה"
- multiple_choice with "время"/"место"/"человек" as distractors
- dictation with "המומחים דנו ב...מסקנותיהם"

Inserts 234 replacement exercises (3 per affected lesson) with:
- Diverse MC distractors (semantically close, not generic)
- Varied fill_blank sentence structures
- Unique dictation sentences
- Randomized correct_index for MC

Revision ID: 127
Revises: 126
"""

import json
import random
from alembic import op
import sqlalchemy as sa

revision = "127"
down_revision = "126"
branch_labels = None
depends_on = None

_j = lambda d: json.dumps(d, ensure_ascii=False)

# ── Pools of diverse replacement templates ────────────────────────────────

# MC: Hebrew distractor sets (semantically related academic/topic words)
MC_DISTRACTOR_SETS = [
    ["תהליך", "מבנה", "תוכנית"],       # process, structure, plan
    ["פרשנות", "השפעה", "גישה"],        # interpretation, influence, approach
    ["ניתוח", "השוואה", "סיכום"],        # analysis, comparison, summary
    ["תופעה", "מגמה", "שיטה"],          # phenomenon, trend, method
    ["יצירה", "ביטוי", "תפיסה"],        # creation, expression, perception
    ["מחקר", "עיון", "דיון"],            # research, study, discussion
    ["הגדרה", "סיווג", "תיאור"],        # definition, classification, description
    ["רעיון", "עיקרון", "ערך"],          # idea, principle, value
    ["טקסט", "שיח", "סגנון"],           # text, discourse, style
    ["מסורת", "חידוש", "מורשת"],        # tradition, innovation, heritage
    ["היבט", "זווית", "נקודת מבט"],     # aspect, angle, point of view
    ["כלי", "אמצעי", "דרך"],            # tool, means, way
    ["תכונה", "מאפיין", "סימן"],        # quality, characteristic, sign
]

# MC: Russian question templates (varied phrasing)
MC_QUESTION_TEMPLATES = [
    "Какое значение имеет слово {word} в данном контексте?",
    "Как переводится слово {word}?",
    "Выберите правильный перевод слова {word}:",
    "Что означает {word} в современном иврите?",
    "Какое слово соответствует переводу «{meaning}»?",
]

# FB: Hebrew sentence templates (slot = _____  for the keyword)
FB_SENTENCE_TEMPLATES = [
    "ה_____ הוא תחום מרכזי בלימודים ({topic})",
    "ב_____ יש היבטים רבים ומגוונים ({topic})",
    "השימוש ב_____ חשוב בכתיבה אקדמית ({topic})",
    "ל_____ יש תפקיד חשוב בתרבות ({topic})",
    "הבנת ה_____ עוזרת לנו להבין את הנושא ({topic})",
    "לומדים על _____ בקורסים מתקדמים ({topic})",
    "ה_____ משפיע על הבנת הטקסט ({topic})",
    "הכרת ה_____ מאפשרת הבנה עמוקה ({topic})",
    "_____ הוא מושג בסיסי בתחום הזה ({topic})",
    "ה_____ מופיע בטקסטים רבים ({topic})",
    "חשוב להבין את ה_____ לפני שממשיכים ({topic})",
    "ה_____ קשור לנושאים נוספים בתחום ({topic})",
    "כדי להבין את הנושא, צריך להכיר את ה_____ ({topic})",
]

# FB: Russian hint templates
FB_HINT_TEMPLATES = [
    "ключевое слово темы",
    "основной термин",
    "центральное понятие",
    "главное слово в теме",
    "тематический термин",
]

# DC: Hebrew dictation sentence templates
DC_SENTENCE_TEMPLATES = [
    "ה{word} הוא חלק חשוב מהלימודים שלנו השנה",
    "הסטודנטים הציגו עבודה מצוינת בנושא ה{word}",
    "ב{word} יש צדדים רבים שחשוב להכיר",
    "המרצה הסביר את ה{word} בצורה ברורה ומעניינת",
    "הספר הזה עוסק ב{word} מנקודת מבט חדשה",
    "לאחר שלמדנו על ה{word}, הבנו את הנושא טוב יותר",
    "ה{word} מעניין במיוחד כשלומדים אותו לעומק",
    "ישנם מחקרים רבים בתחום ה{word} בשנים האחרונות",
    "השיעור על ה{word} היה מרתק והעשיר את הידע שלנו",
    "חשוב לדעת על ה{word} כדי להבין נושאים מתקדמים",
    "ה{word} נחשב לאחד הנושאים המרכזיים בתחום",
    "אנחנו לומדים על ה{word} כי הוא רלוונטי בחיי היומיום",
    "ה{word} התפתח מאוד בעשורים האחרונים",
]

# DC: Russian hint templates
DC_HINT_TEMPLATES = [
    "Прослушайте и запишите предложение",
    "Запишите услышанное",
    "Диктант: запишите на иврите",
    "Внимательно прослушайте и запишите",
    "Прослушайте предложение и запишите его",
]

# DC: Explanation templates
DC_EXPLANATION_TEMPLATES = [
    "{word} — ключевое слово. Обратите внимание на структуру предложения.",
    "Предложение содержит тематическую лексику. {word} — центральный термин.",
    "Внимание на предлоги: ב — в, ל — к/для, על — о/на.",
    "Запомните: ה — определённый артикль перед {word}.",
    "Обратите внимание на порядок слов в иврите.",
]


def upgrade() -> None:
    conn = op.get_bind()
    rng = random.Random(127)  # seeded for reproducibility

    # ── Step 1: Find affected lesson_ids BEFORE deleting ──────────────────
    # Get lesson_ids that have template fill_blank exercises
    fb_rows = conn.execute(sa.text("""
        SELECT DISTINCT lesson_id FROM exercises
        WHERE type = 'fill_blank'
        AND prompt_json::text LIKE '%חשוב מאוד בתחום הזה%'
    """)).fetchall()
    affected_lesson_ids = [r[0] for r in fb_rows]

    # For each affected lesson, find the topic keyword from the first MC
    # (the non-template MC that has the topic word as first option)
    lesson_keywords = {}
    for lid in affected_lesson_ids:
        # Get the first MC exercise for this lesson (the one with topic context)
        mc_row = conn.execute(sa.text("""
            SELECT prompt_json FROM exercises
            WHERE lesson_id = :lid AND type = 'multiple_choice'
            AND prompt_json::text LIKE '%контексте%'
            ORDER BY id LIMIT 1
        """), {"lid": lid}).fetchone()

        if mc_row:
            prompt = json.loads(mc_row[0]) if isinstance(mc_row[0], str) else mc_row[0]
            options = prompt.get("options", [])
            question = prompt.get("question", "")
            if options:
                keyword = options[0]  # first option is the topic keyword
            else:
                keyword = "הנושא"
            # Extract topic from question (text between «» )
            topic = ""
            if "«" in question and "»" in question:
                topic = question.split("«")[1].split("»")[0]
        else:
            keyword = "הנושא"
            topic = ""

        # Also get the vocab word from the template MC (the "Что означает X?" one)
        vocab_row = conn.execute(sa.text("""
            SELECT prompt_json FROM exercises
            WHERE lesson_id = :lid AND type = 'multiple_choice'
            AND prompt_json::text LIKE '%время%'
            AND prompt_json::text LIKE '%место%'
            ORDER BY id LIMIT 1
        """), {"lid": lid}).fetchone()

        vocab_word = keyword  # fallback
        vocab_meaning = topic
        if vocab_row:
            vprompt = json.loads(vocab_row[0]) if isinstance(vocab_row[0], str) else vocab_row[0]
            vq = vprompt.get("question", "")
            # Extract Hebrew word from "Что означает X?"
            if "означает " in vq:
                vocab_word = vq.split("означает ")[1].rstrip("?").strip()
            vopts = vprompt.get("options", [])
            if vopts:
                vocab_meaning = vopts[0]  # correct translation

        lesson_keywords[lid] = {
            "keyword": keyword,
            "vocab_word": vocab_word,
            "vocab_meaning": vocab_meaning,
            "topic": topic,
        }

    # ── Step 2: Delete template exercises ──────────────────────────────────

    d1 = conn.execute(sa.text("""
        DELETE FROM exercises
        WHERE type = 'fill_blank'
        AND prompt_json::text LIKE '%חשוב מאוד בתחום הזה%'
    """))

    d2 = conn.execute(sa.text("""
        DELETE FROM exercises
        WHERE type = 'multiple_choice'
        AND prompt_json::text LIKE '%"время"%'
        AND prompt_json::text LIKE '%"место"%'
        AND prompt_json::text LIKE '%"человек"%'
    """))

    d3 = conn.execute(sa.text("""
        DELETE FROM exercises
        WHERE type = 'dictation'
        AND prompt_json::text LIKE '%המומחים דנו ב%'
        AND prompt_json::text LIKE '%מסקנותיהם%'
    """))

    total_deleted = d1.rowcount + d2.rowcount + d3.rowcount
    print(f"Deleted {total_deleted} template exercises ({d1.rowcount} FB + {d2.rowcount} MC + {d3.rowcount} DC)")

    # ── Step 3: Insert diverse replacement exercises ──────────────────────

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

    inserted = 0
    for i, lid in enumerate(sorted(affected_lesson_ids)):
        info = lesson_keywords.get(lid, {"keyword": "הנושא", "vocab_word": "מושג", "vocab_meaning": "понятие", "topic": "тема"})
        keyword = info["keyword"]
        vocab_word = info["vocab_word"]
        vocab_meaning = info["vocab_meaning"]
        topic = info["topic"] or "тема"

        # ── MC: Diverse question with semantically close distractors ──
        distractors = list(MC_DISTRACTOR_SETS[i % len(MC_DISTRACTOR_SETS)])
        # Remove keyword if it happens to be in distractors
        distractors = [d for d in distractors if d != vocab_word][:3]
        while len(distractors) < 3:
            extra = MC_DISTRACTOR_SETS[(i + 1) % len(MC_DISTRACTOR_SETS)]
            for e in extra:
                if e not in distractors and e != vocab_word:
                    distractors.append(e)
                if len(distractors) >= 3:
                    break

        correct_idx = rng.randint(0, 3)
        options_ru = list(distractors[:3])
        options_ru.insert(correct_idx, vocab_meaning)
        q_template = MC_QUESTION_TEMPLATES[i % len(MC_QUESTION_TEMPLATES)]
        question = q_template.format(word=vocab_word, meaning=vocab_meaning)

        mc_ex = {
            "lesson_id": lid, "type": "multiple_choice", "difficulty": 2, "points": 10,
            "prompt_json": _j({"question": question, "options": options_ru}),
            "answer_json": _j({"correct": vocab_meaning, "correct_index": correct_idx}),
            "explanation_json": _j({"text": f"{vocab_word} — {vocab_meaning}. Лексика темы «{topic}»."}),
        }

        # ── FB: Varied Hebrew sentence ──
        fb_template = FB_SENTENCE_TEMPLATES[i % len(FB_SENTENCE_TEMPLATES)]
        fb_hint = FB_HINT_TEMPLATES[i % len(FB_HINT_TEMPLATES)]
        fb_sentence = fb_template.format(topic=topic)

        fb_ex = {
            "lesson_id": lid, "type": "fill_blank", "difficulty": 2, "points": 10,
            "prompt_json": _j({"sentence": fb_sentence, "hint": fb_hint}),
            "answer_json": _j({"correct": keyword, "alternatives": []}),
            "explanation_json": _j({"text": f"{keyword} — ключевое слово в теме «{topic}»."}),
        }

        # ── DC: Unique dictation sentence ──
        dc_template = DC_SENTENCE_TEMPLATES[i % len(DC_SENTENCE_TEMPLATES)]
        dc_sentence = dc_template.format(word=keyword)
        dc_hint = DC_HINT_TEMPLATES[i % len(DC_HINT_TEMPLATES)]
        dc_explanation = DC_EXPLANATION_TEMPLATES[i % len(DC_EXPLANATION_TEMPLATES)].format(word=keyword)

        dc_ex = {
            "lesson_id": lid, "type": "dictation", "difficulty": 2, "points": 10,
            "prompt_json": _j({"audio_text": dc_sentence, "hint": dc_hint}),
            "answer_json": _j({"correct": dc_sentence}),
            "explanation_json": _j({"text": dc_explanation}),
        }

        op.bulk_insert(exercises_table, [mc_ex, fb_ex, dc_ex])
        inserted += 3

    print(f"Inserted {inserted} diverse replacement exercises across {len(affected_lesson_ids)} lessons")


def downgrade() -> None:
    conn = op.get_bind()

    # Delete the replacement exercises by their unique patterns
    for template in FB_SENTENCE_TEMPLATES:
        pattern = template.split("_____")[0] if "_____" in template else template[:20]
        if pattern:
            conn.execute(sa.text(
                "DELETE FROM exercises WHERE type = 'fill_blank' AND prompt_json::text LIKE :pattern"
            ), {"pattern": f"%{pattern}%"})

    for template in DC_SENTENCE_TEMPLATES:
        pattern = template.split("{word}")[0] if "{word}" in template else template[:20]
        if pattern:
            conn.execute(sa.text(
                "DELETE FROM exercises WHERE type = 'dictation' AND prompt_json::text LIKE :pattern"
            ), {"pattern": f"%{pattern}%"})

    # Note: downgrade cannot restore the original template exercises.
    # Run migrations 082 and 083 to re-seed if needed.
