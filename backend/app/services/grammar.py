from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.grammar import GrammarTopic, GrammarRule, Binyan, VerbConjugation, Preposition, GrammarRuleTag


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


async def get_grammar_cards(
    db: AsyncSession,
    *,
    level_id: int | None = None,
    tag: str | None = None,
    page: int = 1,
    per_page: int = 20,
) -> list[dict]:
    """Get grammar topics as browsable cards, optionally filtered by level/tag."""
    from sqlalchemy import func

    q = select(GrammarTopic)

    if level_id is not None:
        q = q.where(GrammarTopic.level_id == level_id)

    if tag:
        # Filter by tag via join
        topic_ids_q = select(GrammarRuleTag.rule_id).where(GrammarRuleTag.tag == tag)
        # rule_id actually refers to topic_id in our seeding
        q = q.where(GrammarTopic.id.in_(topic_ids_q))

    q = q.order_by(GrammarTopic.level_id, GrammarTopic.order)
    q = q.offset((page - 1) * per_page).limit(per_page)

    result = await db.execute(q)
    topics = result.scalars().all()

    cards = []
    for t in topics:
        # Get tags for this topic
        tag_result = await db.execute(
            select(GrammarRuleTag.tag).where(GrammarRuleTag.rule_id == t.id)
        )
        tags = [row[0] for row in tag_result.all()]
        cards.append({
            "id": t.id,
            "title_ru": t.title_ru,
            "title_he": t.title_he,
            "level_id": t.level_id,
            "summary": t.summary,
            "tags": tags,
        })

    return cards


async def get_grammar_tags(db: AsyncSession, topic_id: int) -> list[str]:
    """Get tags for a specific topic."""
    result = await db.execute(
        select(GrammarRuleTag.tag).where(GrammarRuleTag.rule_id == topic_id)
    )
    return [row[0] for row in result.all()]


async def get_related_grammar_for_error(
    db: AsyncSession,
    *,
    error_type: str | None = None,
    binyan: str | None = None,
    tense: str | None = None,
) -> list[dict]:
    """Find grammar topics related to an error context via tags."""
    # Build potential tags from error context
    search_tags = []
    if error_type:
        tag_map = {
            "gender_confusion": "gender",
            "similar_sounds": "pronunciation",
            "vowel_errors": "nikkud",
            "word_order": "syntax",
        }
        if error_type in tag_map:
            search_tags.append(tag_map[error_type])
    if binyan:
        search_tags.append(f"binyan_{binyan.lower()}")
    if tense:
        search_tags.append(f"conjugation_{tense}")

    if not search_tags:
        return []

    from sqlalchemy import or_
    q = (
        select(GrammarTopic)
        .join(GrammarRuleTag, GrammarRuleTag.rule_id == GrammarTopic.id)
        .where(GrammarRuleTag.tag.in_(search_tags))
        .distinct()
        .limit(5)
    )
    result = await db.execute(q)
    topics = result.scalars().all()

    return [
        {
            "id": t.id,
            "title_ru": t.title_ru,
            "title_he": t.title_he,
            "level_id": t.level_id,
            "summary": t.summary,
            "tags": [],
        }
        for t in topics
    ]
