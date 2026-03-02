from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.word import (
    DictionaryStats,
    RootFamilyOut,
    RootFamilyWordOut,
    WordBrief,
    WordDetail,
    WordFormOut,
    ExampleSentenceOut,
    WordListResponse,
)
from app.services.word import (
    get_dictionary_stats,
    get_root_families,
    get_root_family,
    get_word_detail,
    list_words,
)

router = APIRouter(prefix="/words", tags=["words"])


@router.get("", response_model=WordListResponse)
async def get_words(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    search: str | None = None,
    pos: str | None = None,
    level_id: int | None = None,
    frequency: int | None = None,
    root: str | None = None,
    sort_by: str = "hebrew",
    db: AsyncSession = Depends(get_db),
):
    words, total = await list_words(
        db, page=page, per_page=per_page, search=search,
        pos=pos, level_id=level_id, frequency=frequency,
        root=root, sort_by=sort_by,
    )
    return WordListResponse(
        items=[WordBrief.model_validate(w) for w in words],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/stats", response_model=DictionaryStats)
async def get_stats(db: AsyncSession = Depends(get_db)):
    return await get_dictionary_stats(db)


@router.get("/roots")
async def get_roots(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    families, total = await get_root_families(db, page=page, per_page=per_page)
    items = []
    for fam in families:
        # Fetch actual words for each member
        member_word_ids = [m.word_id for m in fam.members]
        words = []
        if member_word_ids:
            from sqlalchemy import select
            from app.models.word import Word
            result = await db.execute(
                select(Word).where(Word.id.in_(member_word_ids))
            )
            words = [
                RootFamilyWordOut(
                    id=w.id, hebrew=w.hebrew,
                    transliteration=w.transliteration,
                    translation_ru=w.translation_ru, pos=w.pos,
                )
                for w in result.scalars().all()
            ]
        items.append(RootFamilyOut(
            id=fam.id, root=fam.root, meaning_ru=fam.meaning_ru, words=words,
        ))
    return {"items": items, "total": total, "page": page, "per_page": per_page}


@router.get("/root/{root_str}")
async def get_root_family_words(root_str: str, db: AsyncSession = Depends(get_db)):
    words = await get_root_family(db, root_str)
    return [RootFamilyWordOut.model_validate(w) for w in words]


@router.get("/{word_id}", response_model=WordDetail)
async def get_word(word_id: int, db: AsyncSession = Depends(get_db)):
    word = await get_word_detail(db, word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    # Build root family
    root_family = None
    if word.root:
        family_words = await get_root_family(db, word.root)
        root_family = [
            RootFamilyWordOut(
                id=w.id, hebrew=w.hebrew,
                transliteration=w.transliteration,
                translation_ru=w.translation_ru, pos=w.pos,
            )
            for w in family_words
            if w.id != word.id
        ]

    return WordDetail(
        id=word.id,
        hebrew=word.hebrew,
        nikkud=word.nikkud,
        transliteration=word.transliteration,
        translation_ru=word.translation_ru,
        pos=word.pos,
        gender=word.gender,
        number=word.number,
        root=word.root,
        frequency_rank=word.frequency_rank,
        level_id=word.level_id,
        audio_url=word.audio_url,
        image_url=word.image_url,
        forms=[WordFormOut.model_validate(f) for f in word.forms],
        examples=[ExampleSentenceOut.model_validate(e) for e in word.examples],
        root_family=root_family,
    )
