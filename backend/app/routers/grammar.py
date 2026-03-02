from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.grammar import GrammarTopicBrief, GrammarTopicDetail, BinyanOut, ConjugationOut, PrepositionOut
from app.services.grammar import list_topics, get_topic_detail, list_binyanim, get_conjugations, list_prepositions

router = APIRouter(tags=["grammar"])


@router.get("/grammar/topics", response_model=list[GrammarTopicBrief])
async def get_topics(
    level_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    topics = await list_topics(db, level_id=level_id)
    return [GrammarTopicBrief.model_validate(t) for t in topics]


@router.get("/grammar/topics/{topic_id}", response_model=GrammarTopicDetail)
async def get_topic(
    topic_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    topic = await get_topic_detail(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return GrammarTopicDetail.model_validate(topic)


@router.get("/grammar/binyanim", response_model=list[BinyanOut])
async def get_binyanim(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    binyanim = await list_binyanim(db)
    return [BinyanOut.model_validate(b) for b in binyanim]


@router.get("/grammar/prepositions", response_model=list[PrepositionOut])
async def get_prepositions(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    preps = await list_prepositions(db)
    return [PrepositionOut.model_validate(p) for p in preps]


@router.get("/grammar/conjugations/{word_id}", response_model=list[ConjugationOut])
async def get_word_conjugations(
    word_id: int,
    binyan_id: int | None = Query(None),
    tense: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    conjugations = await get_conjugations(db, word_id, binyan_id=binyan_id, tense=tense)
    return [ConjugationOut.model_validate(c) for c in conjugations]
