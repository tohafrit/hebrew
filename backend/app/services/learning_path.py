import uuid
from datetime import datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.learning_path import LearningPath, UserPathProgress


async def get_path_for_level(db: AsyncSession, level_id: int) -> list[LearningPath]:
    result = await db.execute(
        select(LearningPath)
        .where(LearningPath.level_id == level_id)
        .order_by(LearningPath.unit, LearningPath.step)
    )
    return list(result.scalars().all())


async def get_all_paths(db: AsyncSession) -> list[LearningPath]:
    result = await db.execute(
        select(LearningPath).order_by(LearningPath.level_id, LearningPath.unit, LearningPath.step)
    )
    return list(result.scalars().all())


async def get_user_progress(db: AsyncSession, user_id: uuid.UUID) -> set[int]:
    """Return set of completed path_step_ids for a user."""
    result = await db.execute(
        select(UserPathProgress.path_step_id)
        .where(UserPathProgress.user_id == user_id)
    )
    return set(result.scalars().all())


async def complete_step(
    db: AsyncSession, user_id: uuid.UUID, path_step_id: int
) -> bool:
    """Mark a path step as completed. Returns True if newly completed."""
    # Check if already completed
    existing = await db.execute(
        select(UserPathProgress)
        .where(
            UserPathProgress.user_id == user_id,
            UserPathProgress.path_step_id == path_step_id,
        )
    )
    if existing.scalar_one_or_none():
        return False

    # Verify step exists
    step = await db.execute(
        select(LearningPath).where(LearningPath.id == path_step_id)
    )
    if not step.scalar_one_or_none():
        return False

    progress = UserPathProgress(
        user_id=user_id,
        path_step_id=path_step_id,
        completed_at=datetime.utcnow(),
    )
    db.add(progress)
    await db.flush()
    return True


async def get_next_step(
    db: AsyncSession, user_id: uuid.UUID, level_id: int
) -> LearningPath | None:
    """Get the next uncompleted step for a user at a given level."""
    completed = await get_user_progress(db, user_id)
    steps = await get_path_for_level(db, level_id)

    for step in steps:
        if step.id not in completed:
            return step
    return None
