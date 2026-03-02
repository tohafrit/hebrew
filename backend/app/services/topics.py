import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.topic import Topic, UserTopicProgress


async def list_topics(
    db: AsyncSession, level_id: int | None = None
) -> list[Topic]:
    q = select(Topic).order_by(Topic.level_id, Topic.order)
    if level_id is not None:
        q = q.where(Topic.level_id == level_id)
    result = await db.execute(q)
    return list(result.scalars().all())


async def list_topics_with_progress(
    db: AsyncSession, user_id: uuid.UUID, level_id: int | None = None
) -> list[dict]:
    q = (
        select(Topic, UserTopicProgress)
        .outerjoin(
            UserTopicProgress,
            (UserTopicProgress.topic_id == Topic.id)
            & (UserTopicProgress.user_id == user_id),
        )
        .order_by(Topic.level_id, Topic.order)
    )
    if level_id is not None:
        q = q.where(Topic.level_id == level_id)

    result = await db.execute(q)
    rows = result.all()

    topics = []
    for topic, progress in rows:
        d = {
            "id": topic.id,
            "name_ru": topic.name_ru,
            "name_he": topic.name_he,
            "icon": topic.icon,
            "level_id": topic.level_id,
            "order": topic.order,
            "words_learned": progress.words_learned if progress else 0,
            "exercises_done": progress.exercises_done if progress else 0,
            "mastery_pct": progress.mastery_pct if progress else 0.0,
        }
        topics.append(d)
    return topics
