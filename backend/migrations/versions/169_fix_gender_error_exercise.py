"""Fix gender agreement error: remove 'זו ספר' from accepted answers.

ספר (book) is masculine, so only 'זה ספר' is correct.

Revision ID: 169
Revises: 168
"""
from alembic import op
import sqlalchemy as sa
import json

revision = "169"
down_revision = "168"


def upgrade():
    conn = op.get_bind()

    # Find exercises that accept "זו ספר" and fix them
    result = conn.execute(
        sa.text(
            "SELECT id, answer_json FROM exercises "
            "WHERE answer_json::text LIKE '%זו ספר%'"
        )
    )

    for row in result:
        answer = row.answer_json if isinstance(row.answer_json, dict) else json.loads(row.answer_json)
        accept = answer.get("accept", [])
        if "זו ספר" in accept:
            accept.remove("זו ספר")
            answer["accept"] = accept
            conn.execute(
                sa.text("UPDATE exercises SET answer_json = :aj WHERE id = :id"),
                {"aj": json.dumps(answer, ensure_ascii=False), "id": row.id},
            )


def downgrade():
    pass
