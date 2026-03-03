"""Fix all broken match_pairs exercises across L1-L6.

Two different broken formats exist in the database:

FORMAT 1 (migrations 074-075, ~55 exercises, L1):
  prompt_json: {"pairs_left": [...], "pairs_right": [...]}   ← OK
  answer_json: {"correct_pairs": {...}}                       ← WRONG KEY
  Fix: rename "correct_pairs" → "matches"

FORMAT 2 (migrations 076-083, ~212 exercises, L2-L6):
  prompt_json: {"instruction": "...", "pairs": [{"left": "x", "right": "y"}, ...]}
  answer_json: {"pairs": [[0,0], [1,1], ...]}
  Fix: convert to {"pairs_left": [...], "pairs_right": [...]}
       and {"matches": {"x": "y", ...}}

Expected format (frontend + backend):
  prompt_json: {"pairs_left": string[], "pairs_right": string[]}
  answer_json: {"matches": {left: right, ...}}

Revision ID: 147
Revises: 146
"""

import json
from alembic import op
import sqlalchemy as sa

revision = "147"
down_revision = "146"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # ══════════════════════════════════════════════════════════════════════
    # FIX 1: answer_json has "correct_pairs" instead of "matches"
    # (migrations 074-075, L1 exercises)
    # ══════════════════════════════════════════════════════════════════════

    rows_f1 = conn.execute(sa.text(
        "SELECT id, answer_json FROM exercises "
        "WHERE type = 'match_pairs' "
        "AND answer_json::text LIKE '%correct_pairs%'"
    )).fetchall()

    fixed_f1 = 0
    for row in rows_f1:
        answer = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        if "correct_pairs" in answer:
            answer["matches"] = answer.pop("correct_pairs")
            conn.execute(
                sa.text("UPDATE exercises SET answer_json = :aj WHERE id = :id"),
                {"aj": json.dumps(answer, ensure_ascii=False), "id": row[0]},
            )
            fixed_f1 += 1

    print(f"  FIX 1: renamed correct_pairs → matches in {fixed_f1} exercises")

    # ══════════════════════════════════════════════════════════════════════
    # FIX 2: prompt_json has {instruction, pairs[{left,right}]} format
    #         answer_json has {pairs: [[i,i],...]} format
    # (migrations 076-083, L2-L6 exercises)
    # ══════════════════════════════════════════════════════════════════════

    rows_f2 = conn.execute(sa.text(
        "SELECT id, prompt_json, answer_json FROM exercises "
        "WHERE type = 'match_pairs' "
        "AND prompt_json::text LIKE '%\"pairs\"%' "
        "AND prompt_json::text NOT LIKE '%pairs_left%'"
    )).fetchall()

    fixed_f2 = 0
    for row in rows_f2:
        prompt = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        pairs = prompt.get("pairs", [])
        if not pairs or not isinstance(pairs[0], dict):
            continue

        pairs_left = [p["left"] for p in pairs]
        pairs_right = [p["right"] for p in pairs]
        matches = {p["left"]: p["right"] for p in pairs}

        new_prompt = {"pairs_left": pairs_left, "pairs_right": pairs_right}
        new_answer = {"matches": matches}

        conn.execute(
            sa.text(
                "UPDATE exercises SET prompt_json = :pj, answer_json = :aj WHERE id = :id"
            ),
            {
                "pj": json.dumps(new_prompt, ensure_ascii=False),
                "aj": json.dumps(new_answer, ensure_ascii=False),
                "id": row[0],
            },
        )
        fixed_f2 += 1

    print(f"  FIX 2: converted pairs[] format → pairs_left/pairs_right in {fixed_f2} exercises")
    print(f"  TOTAL: fixed {fixed_f1 + fixed_f2} match_pairs exercises")


def downgrade() -> None:
    # Data transformation — cannot cleanly reverse without storing originals.
    # The new format is the canonical one expected by frontend + backend,
    # so reverting would re-break the exercises.
    pass
