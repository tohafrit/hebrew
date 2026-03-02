"""Randomize correct_index in MC exercises and correct_option in dialogues.

73% of multiple_choice exercises had correct_index=0.
100% of dialogue user lines had correct_option=0.
This migration shuffles options so the correct answer is at a random position.

Revision ID: 109
Revises: 108
"""

from alembic import op
import sqlalchemy as sa
import json
import random

revision = "109"
down_revision = "108"
branch_labels = None
depends_on = None

random.seed(42)  # reproducible


def upgrade():
    conn = op.get_bind()

    # --- 1. Randomize MC exercises ---
    rows = conn.execute(sa.text(
        "SELECT id, prompt_json, answer_json FROM exercises WHERE type = 'multiple_choice'"
    )).fetchall()

    for row in rows:
        eid = row[0]
        prompt = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        answer = json.loads(row[2]) if isinstance(row[2], str) else row[2]

        options = prompt.get("options", [])
        correct_idx = answer.get("correct_index", 0)
        if not options or correct_idx is None:
            continue

        correct_val = answer.get("correct", options[correct_idx] if correct_idx < len(options) else None)
        if correct_val is None:
            continue

        # Shuffle options
        random.shuffle(options)
        new_idx = None
        for i, opt in enumerate(options):
            if opt == correct_val:
                new_idx = i
                break

        if new_idx is None:
            # correct value not found in options — try to match by index
            continue

        prompt["options"] = options
        answer["correct_index"] = new_idx

        conn.execute(sa.text(
            "UPDATE exercises SET prompt_json = CAST(:pj AS jsonb), answer_json = CAST(:aj AS jsonb) WHERE id = :eid"
        ), {"pj": json.dumps(prompt, ensure_ascii=False), "aj": json.dumps(answer, ensure_ascii=False), "eid": eid})

    # --- 2. Randomize dialogue correct_option ---
    rows = conn.execute(sa.text(
        "SELECT id, lines_json FROM dialogues"
    )).fetchall()

    for row in rows:
        did = row[0]
        lines = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        changed = False

        for line in lines:
            if not line.get("is_user"):
                continue
            options = line.get("options", [])
            correct_opt = line.get("correct_option", 0)
            if not options or len(options) < 2:
                continue

            correct_val = options[correct_opt] if correct_opt < len(options) else options[0]

            random.shuffle(options)
            new_idx = options.index(correct_val)

            line["options"] = options
            line["correct_option"] = new_idx
            changed = True

        if changed:
            conn.execute(sa.text(
                "UPDATE dialogues SET lines_json = CAST(:lj AS jsonb) WHERE id = :did"
            ), {"lj": json.dumps(lines, ensure_ascii=False), "did": did})


def downgrade():
    # Not reversible in a meaningful way — data is still valid, just differently ordered
    pass
