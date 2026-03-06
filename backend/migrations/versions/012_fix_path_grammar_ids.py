"""Fix learning_paths grammar content_ids to match grammar_topics.

Revision ID: 012
Revises: 011
"""

from alembic import op

revision = "012"
down_revision = "011"
branch_labels = None
depends_on = None


# Mapping: learning_path id -> (old content_id, new content_id, description)
FIXES = [
    # Level 1
    (2, 1, 3, "Местоимения и глагол быть -> Личные местоимения (id=3)"),
    (12, 3, 91, "Принадлежность (של) -> Притяжательные суффиксы (id=91)"),
    # Level 2
    (18, 7, 94, "Настоящее время (Пааль) -> Глаголы группы Пааль настоящее (id=94)"),
    (23, 10, 95, "Прошедшее время (Пааль) -> Прошедшее время Пааль (id=95)"),
    (28, 12, 4, "Предлоги места -> Предлоги и их склонение (id=4)"),
    # Level 3
    (34, 13, 96, "Будущее время -> Будущее время Пааль (id=96)"),
    (40, 15, 109, "Биньян Пиэль -> Все 7 биньянов: сравнение (id=109)"),
    # Level 4
    (45, 20, 7, "Биньян Хифъиль -> Все 7 биньянов — обзор (id=7)"),
    (50, 21, 50, "Пассивный залог -> Пассивные биньяны: Нифъаль (id=50)"),
    # Level 5
    (55, 25, 105, "Сложные предложения -> Сложноподчинённые предложения (id=105)"),
    # Level 6
    (60, 35, 112, "Стилистика и регистры -> Стилистика: формальный vs разговорный (id=112)"),
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
