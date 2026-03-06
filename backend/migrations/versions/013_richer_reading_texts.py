"""Point early learning path reading steps to richer texts.

The original reading texts (IDs 1-5) are too short (190-317 chars).
Update learning path to use expanded texts (IDs 201+, 400-530 chars).

Revision ID: 013
Revises: 012
"""

from alembic import op

revision = "013"
down_revision = "012"
branch_labels = None
depends_on = None

# (learning_path_id, old_content_id, new_content_id, description)
FIXES = [
    (4, 1, 203, "В ульпане (250ch) -> Доброе утро (478ch)"),
    (14, 2, 201, "Семья (238ch) -> Моя семья (470ch)"),
    (20, 4, 222, "В магазине (290ch) -> На рынке Махане Иехуда (803ch)"),
    (30, 5, 223, "Тель-Авив (317ch) -> Поездка в Эйлат (826ch)"),
]


def upgrade() -> None:
    for path_id, old_cid, new_cid, desc in FIXES:
        op.execute(
            f"UPDATE learning_paths SET content_id = {new_cid} "
            f"WHERE id = {path_id} AND content_id = {old_cid}"
        )


def downgrade() -> None:
    for path_id, old_cid, new_cid, desc in FIXES:
        op.execute(
            f"UPDATE learning_paths SET content_id = {old_cid} "
            f"WHERE id = {path_id} AND content_id = {new_cid}"
        )
