from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import Dialogue


async def list_dialogues(
    db: AsyncSession,
    level_id: int | None = None,
) -> list[Dialogue]:
    q = select(Dialogue).order_by(Dialogue.level_id, Dialogue.id)
    if level_id is not None:
        q = q.where(Dialogue.level_id == level_id)
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_dialogue(db: AsyncSession, dialogue_id: int) -> Dialogue | None:
    result = await db.execute(
        select(Dialogue).where(Dialogue.id == dialogue_id)
    )
    return result.scalar_one_or_none()


def check_dialogue_answer(
    dialogue: Dialogue, line_index: int, selected_option: int
) -> tuple[bool, int, str]:
    """Check if user selected the correct option for a dialogue line.
    Returns (is_correct, correct_option_index, correct_text_he).
    """
    lines = dialogue.lines_json or []
    if line_index < 0 or line_index >= len(lines):
        return False, 0, ""

    line = lines[line_index]
    correct_idx = line.get("correct_option", 0)
    options = line.get("options", [])
    correct_text = options[correct_idx] if correct_idx < len(options) else ""

    return selected_option == correct_idx, correct_idx, correct_text
