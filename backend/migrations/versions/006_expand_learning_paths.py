"""Expand learning paths — add missing lessons, readings, dialogues.

Revision ID: 006
Revises: 005
"""

from alembic import op
import sqlalchemy as sa

revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None

# Step cycle pattern per unit
STEP_CYCLE = ["vocabulary", "grammar", "exercise", "reading", "dialogue", "srs_review"]

STEP_ICONS = {
    "vocabulary": "A",
    "grammar": "G",
    "exercise": "E",
    "reading": "R",
    "dialogue": "D",
    "srs_review": "S",
}

STEP_LABELS = {
    "vocabulary": "Словарь",
    "grammar": "Грамматика",
    "exercise": "Упражнения",
    "reading": "Чтение",
    "dialogue": "Диалог",
    "srs_review": "Повторение SRS",
}


def upgrade() -> None:
    conn = op.get_bind()

    # 1. Find lessons NOT yet in learning_paths
    missing_lessons = conn.execute(sa.text("""
        SELECT l.id, l.level_id, l.title_ru, l.title_he, l.type
        FROM lessons l
        WHERE NOT EXISTS (
            SELECT 1 FROM learning_paths lp
            WHERE lp.content_id = l.id AND lp.step_type IN ('vocabulary', 'exercise', 'grammar')
        )
        ORDER BY l.level_id, l.unit, l."order"
    """)).fetchall()

    # 2. Find reading texts NOT yet in learning_paths
    missing_readings = conn.execute(sa.text("""
        SELECT r.id, r.level_id, r.title_ru, r.title_he
        FROM reading_texts r
        WHERE NOT EXISTS (
            SELECT 1 FROM learning_paths lp
            WHERE lp.content_id = r.id AND lp.step_type = 'reading'
        )
        ORDER BY r.level_id, r.id
    """)).fetchall()

    # 3. Find dialogues NOT yet in learning_paths
    missing_dialogues = conn.execute(sa.text("""
        SELECT d.id, d.level_id, d.title, NULL as title_he
        FROM dialogues d
        WHERE NOT EXISTS (
            SELECT 1 FROM learning_paths lp
            WHERE lp.content_id = d.id AND lp.step_type = 'dialogue'
        )
        ORDER BY d.level_id, d.id
    """)).fetchall()

    if not missing_lessons and not missing_readings and not missing_dialogues:
        return

    # 4. Get current max (unit, step) per level
    max_positions = {}
    rows = conn.execute(sa.text("""
        SELECT level_id, MAX(unit) as max_unit, MAX(step) as max_step
        FROM learning_paths
        GROUP BY level_id
    """)).fetchall()
    for row in rows:
        max_positions[row.level_id] = {"unit": row.max_unit, "step": row.max_step}

    # 5. Group new items by level
    by_level = {}
    for lesson in missing_lessons:
        by_level.setdefault(lesson.level_id, []).append({
            "content_id": lesson.id,
            "step_type": "exercise" if lesson.type == "grammar" else "vocabulary",
            "title_ru": lesson.title_ru,
            "title_he": lesson.title_he,
        })

    for reading in missing_readings:
        by_level.setdefault(reading.level_id, []).append({
            "content_id": reading.id,
            "step_type": "reading",
            "title_ru": reading.title_ru,
            "title_he": reading.title_he,
        })

    for dialogue in missing_dialogues:
        by_level.setdefault(dialogue.level_id, []).append({
            "content_id": dialogue.id,
            "step_type": "dialogue",
            "title_ru": dialogue.title,
            "title_he": dialogue.title_he,
        })

    # 6. Insert grouped into units of ~10 steps with cycle pattern
    UNIT_SIZE = 10
    for level_id, items in sorted(by_level.items()):
        pos = max_positions.get(level_id, {"unit": 0, "step": 0})
        current_unit = pos["unit"]
        current_step = pos["step"]

        # Sort items by step_type to follow the cycle pattern
        type_order = {t: i for i, t in enumerate(STEP_CYCLE)}
        items.sort(key=lambda x: type_order.get(x["step_type"], 99))

        for i, item in enumerate(items):
            if i % UNIT_SIZE == 0:
                current_unit += 1
                current_step = 0

            current_step += 1
            label = STEP_LABELS.get(item["step_type"], item["step_type"])
            icon = STEP_ICONS.get(item["step_type"], "?")

            conn.execute(sa.text("""
                INSERT INTO learning_paths (level_id, unit, step, step_type, content_id, title_ru, title_he, description_ru, icon)
                VALUES (:level_id, :unit, :step, :step_type, :content_id, :title_ru, :title_he, :description_ru, :icon)
            """), {
                "level_id": level_id,
                "unit": current_unit,
                "step": current_step,
                "step_type": item["step_type"],
                "content_id": item["content_id"],
                "title_ru": item["title_ru"] or label,
                "title_he": item.get("title_he"),
                "description_ru": label,
                "icon": icon,
            })

        # Add srs_review step at end of each level's new units
        current_step += 1
        conn.execute(sa.text("""
            INSERT INTO learning_paths (level_id, unit, step, step_type, content_id, title_ru, title_he, description_ru, icon)
            VALUES (:level_id, :unit, :step, 'srs_review', NULL, 'Повторение SRS', NULL, 'Повторите карточки', 'S')
        """), {
            "level_id": level_id,
            "unit": current_unit,
            "step": current_step,
        })


def downgrade() -> None:
    # Remove only the steps added by this migration (those with unit > original max)
    # For safety, we just leave them — removing specific rows is fragile
    pass
