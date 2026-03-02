from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.settings import UserSettingsOut, UserSettingsUpdate
from app.services.settings import get_user_settings, update_user_settings

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=UserSettingsOut)
async def get_settings(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    settings = await get_user_settings(db, user.id)
    return UserSettingsOut.model_validate(settings)


@router.put("", response_model=UserSettingsOut)
async def put_settings(
    body: UserSettingsUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    updates = body.model_dump(exclude_unset=True)
    settings = await update_user_settings(db, user.id, updates)
    return UserSettingsOut.model_validate(settings)
