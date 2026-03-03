"""Fix broken multiple_choice exercises.

130a: Fix 44 MC with integer correct_index (missing text in "correct" field).
      Reads options[correct_int] and sets proper {"correct": text, "correct_index": int}.

130b: Fix 17 MC still containing "человек" in options.
      Replace with a semantically appropriate Russian distractor.

130c: Fix 1 MC with only 2 options — pad to 4 options.

Revision ID: 130
Revises: 129
"""

import json
import random
from alembic import op
import sqlalchemy as sa

revision = "130"
down_revision = "129"
branch_labels = None
depends_on = None

_j = lambda d: json.dumps(d, ensure_ascii=False)

# Pool of Russian academic distractors to replace "человек"
RUSSIAN_DISTRACTORS = [
    "процесс", "результат", "система", "метод", "принцип",
    "теория", "структура", "подход", "анализ", "фактор",
    "элемент", "аспект", "функция", "модель", "контекст",
    "проблема", "решение", "концепция", "стратегия", "тенденция",
]

# Hebrew distractors for padding short MC exercises
HEBREW_PAD_DISTRACTORS = [
    "תהליך", "מבנה", "שיטה", "גישה", "ניתוח",
    "מחקר", "עיון", "רעיון", "ערך", "תופעה",
    "דיון", "סיכום", "השפעה", "פרשנות", "תיאור",
]


def upgrade() -> None:
    conn = op.get_bind()
    rng = random.Random(130)

    # ── 130a: Fix 44 MC with broken correct_index ─────────────────────────
    # These have answer_json = {"correct": <integer>} without text
    broken_rows = conn.execute(sa.text("""
        SELECT id, prompt_json, answer_json FROM exercises
        WHERE type = 'multiple_choice'
        AND answer_json::text ~ '"correct"\\s*:\\s*[0-9]'
        AND answer_json::text NOT LIKE '%correct_index%'
    """)).fetchall()

    fixed_a = 0
    for row in broken_rows:
        ex_id = row[0]
        prompt = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        answer = json.loads(row[2]) if isinstance(row[2], str) else row[2]

        correct_int = answer.get("correct")
        if not isinstance(correct_int, int):
            continue

        options = prompt.get("options", [])
        if correct_int < 0 or correct_int >= len(options):
            continue

        correct_text = options[correct_int]
        new_answer = {"correct": correct_text, "correct_index": correct_int}

        conn.execute(sa.text(
            "UPDATE exercises SET answer_json = :aj WHERE id = :id"
        ), {"aj": _j(new_answer), "id": ex_id})
        fixed_a += 1

    print(f"130a: Fixed {fixed_a} MC exercises with broken correct_index")

    # ── 130b: Fix 17 MC with "человек" in options ─────────────────────────
    chelovek_rows = conn.execute(sa.text("""
        SELECT id, prompt_json, answer_json FROM exercises
        WHERE type = 'multiple_choice'
        AND prompt_json::text LIKE '%человек%'
    """)).fetchall()

    fixed_b = 0
    used_distractors = set()
    for row in chelovek_rows:
        ex_id = row[0]
        prompt = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        answer = json.loads(row[2]) if isinstance(row[2], str) else row[2]

        options = prompt.get("options", [])
        correct_text = answer.get("correct", "")

        new_options = []
        changed = False
        for opt in options:
            if opt == "человек":
                # Pick a distractor not already in this exercise's options
                replacement = None
                for d in RUSSIAN_DISTRACTORS:
                    if d not in options and d not in new_options and d != correct_text and d not in used_distractors:
                        replacement = d
                        used_distractors.add(d)
                        break
                if replacement is None:
                    # Fallback: use any distractor not in current options
                    for d in RUSSIAN_DISTRACTORS:
                        if d not in options and d not in new_options and d != correct_text:
                            replacement = d
                            break
                if replacement is None:
                    replacement = "явление"  # last resort
                new_options.append(replacement)
                changed = True
            else:
                new_options.append(opt)

        if changed:
            # Update correct_index since options may have changed position
            correct_idx = None
            for i, opt in enumerate(new_options):
                if opt == correct_text:
                    correct_idx = i
                    break

            if correct_idx is None:
                # correct answer was "человек" itself — skip, it's a data issue
                continue

            prompt["options"] = new_options
            new_answer = {"correct": correct_text, "correct_index": correct_idx}

            conn.execute(sa.text(
                "UPDATE exercises SET prompt_json = :pj, answer_json = :aj WHERE id = :id"
            ), {"pj": _j(prompt), "aj": _j(new_answer), "id": ex_id})
            fixed_b += 1

    print(f"130b: Fixed {fixed_b} MC exercises with 'человек' in options")

    # ── 130c: Fix MC with fewer than 4 options ────────────────────────────
    short_rows = conn.execute(sa.text("""
        SELECT id, prompt_json, answer_json FROM exercises
        WHERE type = 'multiple_choice'
        AND jsonb_array_length(prompt_json::jsonb -> 'options') < 4
    """)).fetchall()

    fixed_c = 0
    for row in short_rows:
        ex_id = row[0]
        prompt = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        answer = json.loads(row[2]) if isinstance(row[2], str) else row[2]

        options = prompt.get("options", [])
        correct_text = answer.get("correct", "")

        # Pad to 4 options with distractors not already present
        while len(options) < 4:
            for d in HEBREW_PAD_DISTRACTORS:
                if d not in options and d != correct_text:
                    options.append(d)
                    break
            else:
                break  # exhausted distractors

        # Re-shuffle and update correct_index
        correct_idx_old = options.index(correct_text) if correct_text in options else 0
        correct_val = options[correct_idx_old]
        rng.shuffle(options)
        new_correct_idx = options.index(correct_val)

        prompt["options"] = options
        new_answer = {"correct": correct_val, "correct_index": new_correct_idx}

        conn.execute(sa.text(
            "UPDATE exercises SET prompt_json = :pj, answer_json = :aj WHERE id = :id"
        ), {"pj": _j(prompt), "aj": _j(new_answer), "id": ex_id})
        fixed_c += 1

    print(f"130c: Fixed {fixed_c} MC exercises with fewer than 4 options")


def downgrade() -> None:
    # Cannot reliably restore original broken data — these were bugs, not content.
    pass
