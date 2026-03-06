from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.grammar import (
    GrammarTopicBrief, GrammarTopicDetail, BinyanOut, ConjugationOut, PrepositionOut,
    DrillQuestion, DrillCheckRequest, DrillCheckResponse,
)
from app.services.grammar import list_topics, get_topic_detail, list_binyanim, get_conjugations, list_prepositions
from app.services.conjugation_drill import generate_drill_questions, check_drill_answer

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


# ── Conjugation Drill ────────────────────────────────────────────────────

@router.get("/grammar/conjugation-drill", response_model=list[DrillQuestion])
async def get_drill_questions(
    level_id: int | None = Query(None),
    binyan_id: int | None = Query(None),
    tense: str | None = Query(None),
    count: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    questions = await generate_drill_questions(
        db, level_id=level_id, binyan_id=binyan_id, tense=tense, count=count,
    )
    return [DrillQuestion(**q) for q in questions]


@router.post("/grammar/conjugation-drill/check", response_model=DrillCheckResponse)
async def check_drill(
    body: DrillCheckRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await check_drill_answer(
        db,
        word_id=body.word_id,
        binyan_id=body.binyan_id,
        tense=body.tense,
        person=body.person,
        answer=body.answer,
    )
    return DrillCheckResponse(**result)
