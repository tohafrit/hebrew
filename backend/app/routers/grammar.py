from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.grammar import (
    GrammarTopicBrief, GrammarTopicDetail, BinyanOut, ConjugationOut, PrepositionOut,
    DrillQuestion, DrillCheckRequest, DrillCheckResponse,
    TableDrillCell, TableDrillResponse, TableDrillCheckRequest, TableDrillCheckResponse, TableDrillCheckResult,
    GrammarCardBrief, GrammarCardDetail, RelatedGrammarResponse,
)
from app.services.grammar import (
    list_topics, get_topic_detail, list_binyanim, get_conjugations, list_prepositions,
    get_grammar_cards, get_related_grammar_for_error, get_grammar_tags,
)
from app.services.conjugation_drill import generate_drill_questions, check_drill_answer, generate_table_drill, _strip_nikkud

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


# ── Conjugation Table Drill ──────────────────────────────────────────────

@router.get("/grammar/conjugation-table-drill")
async def get_table_drill(
    word_id: int | None = Query(None),
    binyan_id: int | None = Query(None),
    tense: str | None = Query(None),
    level_id: int | None = Query(None),
    blank_count: int = Query(5, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await generate_table_drill(
        db, word_id=word_id, binyan_id=binyan_id, tense=tense,
        level_id=level_id, blank_count=blank_count,
    )
    if not result:
        raise HTTPException(status_code=404, detail="No conjugation data found")
    return TableDrillResponse(
        word_id=result["word_id"],
        word_hebrew=result["word_hebrew"],
        word_nikkud=result["word_nikkud"],
        translation_ru=result["translation_ru"],
        binyan_id=result["binyan_id"],
        binyan_name=result["binyan_name"],
        tense=result["tense"],
        cells=[TableDrillCell(**c) for c in result["cells"]],
    )


@router.post("/grammar/conjugation-table-drill/check", response_model=TableDrillCheckResponse)
async def check_table_drill(
    body: TableDrillCheckRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    results = []
    for ans in body.answers:
        check = await check_drill_answer(
            db, word_id=body.word_id, binyan_id=body.binyan_id,
            tense=body.tense, person=ans.person, answer=ans.answer,
        )
        results.append(TableDrillCheckResult(
            person=ans.person,
            correct=check["correct"],
            correct_answer=check["correct_answer"],
            correct_nikkud=check.get("correct_nikkud"),
        ))
    total_correct = sum(1 for r in results if r.correct)
    return TableDrillCheckResponse(
        results=results,
        total_correct=total_correct,
        total_answers=len(results),
    )


# ── Grammar Cards ────────────────────────────────────────────────────────

@router.get("/grammar/cards", response_model=list[GrammarCardBrief])
async def get_cards(
    level_id: int | None = Query(None),
    tag: str | None = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return await get_grammar_cards(db, level_id=level_id, tag=tag, page=page, per_page=per_page)


@router.get("/grammar/cards/{topic_id}", response_model=GrammarCardDetail)
async def get_card_detail(
    topic_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    topic = await get_topic_detail(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    tags = await get_grammar_tags(db, topic_id)
    return GrammarCardDetail(
        id=topic.id,
        title_ru=topic.title_ru,
        title_he=topic.title_he,
        level_id=topic.level_id,
        summary=topic.summary,
        content_md=topic.content_md,
        rules=[],  # filled via model_validate if needed
        tags=tags,
    )


@router.get("/grammar/related", response_model=RelatedGrammarResponse)
async def get_related(
    error_type: str | None = Query(None),
    binyan: str | None = Query(None),
    tense: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    topics = await get_related_grammar_for_error(
        db, error_type=error_type, binyan=binyan, tense=tense,
    )
    return RelatedGrammarResponse(topics=topics)


@router.get("/grammar/tags")
async def list_all_tags(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from app.models.grammar import GrammarRuleTag
    from sqlalchemy import select, func
    result = await db.execute(
        select(GrammarRuleTag.tag, func.count())
        .group_by(GrammarRuleTag.tag)
        .order_by(GrammarRuleTag.tag)
    )
    return [{"tag": row[0], "count": row[1]} for row in result.all()]
