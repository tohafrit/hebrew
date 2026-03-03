"""Fix broken multiple-choice exercises.

151a: Fix 44 MC with broken correct_index (integer instead of text)
151b: Fix 17 MC still containing "человек" in options
151c: Fix 1 MC with only 2 options (pad to 4)

Revision ID: 151
Revises: 150
"""

import json
import random
from alembic import op
import sqlalchemy as sa

revision = "151"
down_revision = "150"
branch_labels = None
depends_on = None

_j = lambda d: json.dumps(d, ensure_ascii=False)

# Pool of Russian academic/topic distractors to replace "человек"
RU_DISTRACTORS = [
    "процесс", "структура", "анализ", "явление", "метод",
    "система", "теория", "принцип", "результат", "подход",
    "функция", "элемент", "свойство", "категория", "объект",
    "модель", "критерий", "фактор", "аспект", "компонент",
]


def upgrade() -> None:
    conn = op.get_bind()
    rng = random.Random(151)

    # ── 151a: Fix 44 MC with broken correct_index ────────────────────────
    # These have answer_json = {"correct": <integer>} instead of
    # {"correct": "<text>", "correct_index": <int>}

    broken_rows = conn.execute(sa.text("""
        SELECT id, prompt_json, answer_json FROM exercises
        WHERE type = 'multiple_choice'
          AND answer_json::text ~ '"correct"\\s*:\\s*[0-9]'
          AND answer_json::text NOT LIKE '%correct_index%'
    """)).fetchall()

    fixed_a = 0
    for row in broken_rows:
        eid = row[0]
        prompt = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        answer = json.loads(row[2]) if isinstance(row[2], str) else row[2]

        correct_int = answer.get("correct")
        if not isinstance(correct_int, int):
            continue

        options = prompt.get("options", [])
        if correct_int < 0 or correct_int >= len(options):
            correct_int = 0  # safety fallback

        correct_text = options[correct_int]
        new_answer = {"correct": correct_text, "correct_index": correct_int}

        conn.execute(sa.text("""
            UPDATE exercises SET answer_json = :answer WHERE id = :eid
        """), {"answer": _j(new_answer), "eid": eid})
        fixed_a += 1

    print(f"151a: Fixed {fixed_a} MC exercises with broken correct_index")

    # ── 151b: Fix MC with "человек" in options ─────────────────────────
    # Only fix exercises where "человек" appears as a DISTRACTOR (not as
    # the correct answer). If "человек" IS the correct answer, the exercise
    # topic is about "person/man" and needs full reconstruction, not just
    # a distractor swap — skip those here.
    chelovek_rows = conn.execute(sa.text("""
        SELECT id, prompt_json, answer_json FROM exercises
        WHERE type = 'multiple_choice'
          AND prompt_json::text LIKE '%человек%'
    """)).fetchall()

    fixed_b = 0
    for row in chelovek_rows:
        eid = row[0]
        prompt = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        answer = json.loads(row[2]) if isinstance(row[2], str) else row[2]

        options = prompt.get("options", [])
        correct_text = answer.get("correct", "")

        # Skip if "человек" is the correct answer — distractor swap would break it
        if correct_text == "человек":
            continue
        # Skip if "человек" only appears in question text, not in options
        if "человек" not in options:
            continue

        changed = False
        new_options = []
        used_distractors = set()
        for opt in options:
            if opt == "человек":
                replacement = None
                for d in RU_DISTRACTORS:
                    if d not in used_distractors and d != correct_text and d not in options:
                        replacement = d
                        used_distractors.add(d)
                        break
                if replacement is None:
                    replacement = rng.choice(RU_DISTRACTORS)
                new_options.append(replacement)
                changed = True
            else:
                new_options.append(opt)

        if changed:
            prompt["options"] = new_options
            if correct_text in new_options:
                answer["correct_index"] = new_options.index(correct_text)
            conn.execute(sa.text("""
                UPDATE exercises
                SET prompt_json = :prompt, answer_json = :answer
                WHERE id = :eid
            """), {"prompt": _j(prompt), "answer": _j(answer), "eid": eid})
            fixed_b += 1

    print(f"151b: Fixed {fixed_b} MC exercises with 'человек' in options")

    # ── 151c: Fix MC with only 2 options (pad to 4) ──────────────────────
    short_rows = conn.execute(sa.text("""
        SELECT id, prompt_json, answer_json FROM exercises
        WHERE type = 'multiple_choice'
          AND jsonb_array_length(prompt_json->'options') < 4
    """)).fetchall()

    fixed_c = 0
    for row in short_rows:
        eid = row[0]
        prompt = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        answer = json.loads(row[2]) if isinstance(row[2], str) else row[2]

        options = prompt.get("options", [])
        correct_text = answer.get("correct", "")

        while len(options) < 4:
            for d in RU_DISTRACTORS:
                if d not in options and d != correct_text:
                    options.append(d)
                    break
            else:
                break

        prompt["options"] = options
        if correct_text in options:
            answer["correct_index"] = options.index(correct_text)

        conn.execute(sa.text("""
            UPDATE exercises
            SET prompt_json = :prompt, answer_json = :answer
            WHERE id = :eid
        """), {"prompt": _j(prompt), "answer": _j(answer), "eid": eid})
        fixed_c += 1

    print(f"151c: Fixed {fixed_c} MC exercises with < 4 options")


def downgrade() -> None:
    # These fixes are corrections — downgrade is a no-op.
    # The original broken data cannot be meaningfully restored.
    pass
