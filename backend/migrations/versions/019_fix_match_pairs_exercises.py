"""fix exercise data: match_pairs and word_order

Revision ID: 019
Revises: 018
Create Date: 2026-03-07

Fixes:
1. 50 match_pairs stored answers as index-pair lists → convert to dicts
2. 275 word_order use prompt.words instead of prompt.words_shuffled → copy
3. 130 word_order have index-based correct_order → convert to word strings
4. 38 word_order have extra distractor words in shuffled → trim to match
"""
from typing import Sequence, Union
import random

from alembic import op
from sqlalchemy import text as sa_text
import json

revision: str = '019'
down_revision: Union[str, None] = '018'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # ── 1. Fix match_pairs: list → dict ──────────────────────────────────
    rows = conn.execute(sa_text(
        "SELECT id, prompt_json, answer_json FROM exercises WHERE type = 'match_pairs'"
    )).fetchall()

    fixed_mp = 0
    for row_id, prompt, answer in rows:
        matches = answer.get("matches", {})
        if not isinstance(matches, list):
            continue

        pairs_left = prompt.get("pairs_left", [])
        pairs_right = prompt.get("pairs_right", [])

        converted = {}
        for pair in matches:
            if isinstance(pair, list) and len(pair) == 2:
                li, ri = pair
                if li < len(pairs_left) and ri < len(pairs_right):
                    converted[pairs_left[li]] = pairs_right[ri]

        if converted:
            new_answer = {**answer, "matches": converted}
            conn.execute(sa_text(
                "UPDATE exercises SET answer_json = :ans WHERE id = :id"
            ), {"ans": json.dumps(new_answer, ensure_ascii=False), "id": row_id})
            fixed_mp += 1

    print(f"  [019] Fixed {fixed_mp} match_pairs exercises (list→dict)")

    # ── 2. Fix word_order exercises ──────────────────────────────────────
    rows = conn.execute(sa_text(
        "SELECT id, prompt_json, answer_json FROM exercises WHERE type = 'word_order'"
    )).fetchall()

    fixed_wo = 0
    for row_id, prompt, answer in rows:
        words_shuffled = prompt.get("words_shuffled", [])
        words = prompt.get("words", [])
        correct_order = answer.get("correct_order", [])
        changed = False
        new_prompt = dict(prompt)
        new_answer = dict(answer)

        # If words_shuffled is empty but words exists, use words
        source_words = words_shuffled or words
        if not source_words and not correct_order:
            continue

        # Convert index-based correct_order to word strings
        if correct_order and isinstance(correct_order[0], int):
            if source_words:
                try:
                    new_correct = [source_words[i] for i in correct_order]
                    new_answer["correct_order"] = new_correct
                    correct_order = new_correct
                    changed = True
                except IndexError:
                    continue

        # If words_shuffled is empty, fill from correct_order (shuffled)
        if not words_shuffled and correct_order:
            shuffled = list(correct_order)
            random.shuffle(shuffled)
            new_prompt["words_shuffled"] = shuffled
            source_words = shuffled
            changed = True

        # Fix extra words: if shuffled has words not in correct_order
        if source_words and correct_order:
            correct_set = set(correct_order)
            shuffled_set = set(source_words)
            if shuffled_set != correct_set:
                # Only keep words that are in correct_order
                trimmed = [w for w in source_words if w in correct_set]
                # Add any missing from correct_order
                for w in correct_order:
                    if w not in trimmed:
                        trimmed.append(w)
                new_prompt["words_shuffled"] = trimmed
                changed = True

        if changed:
            conn.execute(sa_text(
                "UPDATE exercises SET prompt_json = :p, answer_json = :a WHERE id = :id"
            ), {
                "p": json.dumps(new_prompt, ensure_ascii=False),
                "a": json.dumps(new_answer, ensure_ascii=False),
                "id": row_id,
            })
            fixed_wo += 1

    print(f"  [019] Fixed {fixed_wo} word_order exercises")


def downgrade() -> None:
    pass
