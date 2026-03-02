import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserSettings


async def get_user_settings(db: AsyncSession, user_id: uuid.UUID) -> UserSettings:
    """Get user settings, auto-creating a row if missing."""
    result = await db.execute(
        select(UserSettings).where(UserSettings.user_id == user_id)
    )
    settings = result.scalar_one_or_none()
    if not settings:
        settings = UserSettings(user_id=user_id)
        db.add(settings)
        await db.commit()
        await db.refresh(settings)
    return settings


async def update_user_settings(
    db: AsyncSession, user_id: uuid.UUID, updates: dict
) -> UserSettings:
    """Update user settings with provided fields."""
    settings = await get_user_settings(db, user_id)
    for key, value in updates.items():
        if value is not None and hasattr(settings, key):
            setattr(settings, key, value)
    await db.commit()
    await db.refresh(settings)
    return settings
