from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.topics import TopicWithProgress
from app.services.topics import list_topics_with_progress

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=list[TopicWithProgress])
async def get_topics(
    level_id: int | None = Query(None),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    topics = await list_topics_with_progress(db, user.id, level_id)
    return [TopicWithProgress(**t) for t in topics]
