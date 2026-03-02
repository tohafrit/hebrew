from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.grammar import GrammarTopic, GrammarRule, Binyan, VerbConjugation, Preposition


async def list_topics(db: AsyncSession, level_id: int | None = None) -> list[GrammarTopic]:
    q = select(GrammarTopic).order_by(GrammarTopic.level_id, GrammarTopic.order)
    if level_id is not None:
        q = q.where(GrammarTopic.level_id == level_id)
    result = await db.execute(q)
    return list(result.scalars().all())


async def get_topic_detail(db: AsyncSession, topic_id: int) -> GrammarTopic | None:
    result = await db.execute(
        select(GrammarTopic)
        .options(selectinload(GrammarTopic.rules))
        .where(GrammarTopic.id == topic_id)
    )
    return result.scalar_one_or_none()


async def list_binyanim(db: AsyncSession) -> list[Binyan]:
    result = await db.execute(select(Binyan).order_by(Binyan.id))
    return list(result.scalars().all())


async def list_prepositions(db: AsyncSession) -> list[Preposition]:
    result = await db.execute(select(Preposition).order_by(Preposition.id))
    return list(result.scalars().all())


async def get_conjugations(
    db: AsyncSession, word_id: int, binyan_id: int | None = None, tense: str | None = None
) -> list[VerbConjugation]:
    q = select(VerbConjugation).where(VerbConjugation.word_id == word_id)
    if binyan_id is not None:
        q = q.where(VerbConjugation.binyan_id == binyan_id)
    if tense is not None:
        q = q.where(VerbConjugation.tense == tense)
    q = q.order_by(VerbConjugation.tense, VerbConjugation.person)
    result = await db.execute(q)
    return list(result.scalars().all())
