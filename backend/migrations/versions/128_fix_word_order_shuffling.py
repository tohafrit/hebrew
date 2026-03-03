"""Fix word_order exercises where words are in sequential order.

Shuffles the displayed words so students must actually reorder them.
Sets answer_json.correct_order to the list of words in correct order
(matching the check_answer() string comparison logic).

Revision ID: 128
Revises: 127
"""

import json
import random
from alembic import op
import sqlalchemy as sa

revision = "128"
down_revision = "127"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # Find all word_order exercises
    rows = conn.execute(sa.text(
        "SELECT id, prompt_json, answer_json FROM exercises WHERE type = 'word_order'"
    )).fetchall()

    rng = random.Random(42)  # seeded for reproducibility

    updated = 0
    for row in rows:
        ex_id = row[0]
        prompt = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        answer = json.loads(row[2]) if isinstance(row[2], str) else row[2]

        words = prompt.get("words", [])
        correct_order = answer.get("correct_order", [])

        if not words or len(words) < 2:
            continue

        # Check if correct_order is sequential indices [0, 1, 2, ...]
        is_sequential = (
            isinstance(correct_order, list)
            and len(correct_order) == len(words)
            and all(isinstance(x, int) for x in correct_order)
            and correct_order == list(range(len(words)))
        )

        if not is_sequential:
            continue

        # The words list IS the correct order
        correct_words = list(words)

        # Shuffle until different from original
        shuffled = list(words)
        attempts = 0
        while shuffled == correct_words and attempts < 20:
            rng.shuffle(shuffled)
            attempts += 1

        if shuffled == correct_words:
            # Last resort: swap first two
            shuffled[0], shuffled[1] = shuffled[1], shuffled[0]

        # Update prompt with shuffled words, answer with correct word list
        prompt["words"] = shuffled
        answer["correct_order"] = correct_words

        conn.execute(
            sa.text("UPDATE exercises SET prompt_json = :pj, answer_json = :aj WHERE id = :id"),
            {"pj": json.dumps(prompt, ensure_ascii=False),
             "aj": json.dumps(answer, ensure_ascii=False),
             "id": ex_id}
        )
        updated += 1

    print(f"Fixed {updated} word_order exercises")


def downgrade() -> None:
    # Cannot reliably reverse shuffling
    pass
