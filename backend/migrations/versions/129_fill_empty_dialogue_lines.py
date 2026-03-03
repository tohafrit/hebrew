"""Fill 129 empty dialogue lines where text_he is missing.

Each empty line is a user response with options[] where
options[correct_option] (default 0) contains the correct Hebrew text.
This migration copies the correct option into text_he.

Revision ID: 129
Revises: 128
"""

import json
from alembic import op
import sqlalchemy as sa

revision = "129"
down_revision = "128"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    rows = conn.execute(sa.text(
        "SELECT id, lines_json FROM dialogues WHERE lines_json IS NOT NULL"
    )).fetchall()

    filled = 0
    for row in rows:
        dialogue_id = row[0]
        lines = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        if not isinstance(lines, list):
            continue

        modified = False
        for line in lines:
            text_he = line.get("text_he", "")
            if text_he == "" and "options" in line:
                options = line["options"]
                correct_idx = line.get("correct_option", 0)
                if options and 0 <= correct_idx < len(options):
                    line["text_he"] = options[correct_idx]
                    modified = True
                    filled += 1

        if modified:
            conn.execute(
                sa.text("UPDATE dialogues SET lines_json = :lj WHERE id = :id"),
                {"lj": json.dumps(lines, ensure_ascii=False), "id": dialogue_id}
            )

    print(f"Filled {filled} empty dialogue lines")


def downgrade() -> None:
    conn = op.get_bind()

    rows = conn.execute(sa.text(
        "SELECT id, lines_json FROM dialogues WHERE lines_json IS NOT NULL"
    )).fetchall()

    for row in rows:
        dialogue_id = row[0]
        lines = json.loads(row[1]) if isinstance(row[1], str) else row[1]
        if not isinstance(lines, list):
            continue

        modified = False
        for line in lines:
            if line.get("is_user") and "options" in line:
                correct_idx = line.get("correct_option", 0)
                options = line.get("options", [])
                if options and line.get("text_he") == options[correct_idx]:
                    line["text_he"] = ""
                    modified = True

        if modified:
            conn.execute(
                sa.text("UPDATE dialogues SET lines_json = :lj WHERE id = :id"),
                {"lj": json.dumps(lines, ensure_ascii=False), "id": dialogue_id}
            )
