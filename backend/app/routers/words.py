from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.word import (
    DictionaryStats,
    RootFamilyOut,
    RootFamilyWordOut,
    RootExplorerWord,
    RootExplorerResponse,
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
    get_root_family_detail,
    get_word_detail,
    list_words,
    search_root_families,
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


@router.get("/lookup")
async def lookup_word(
    q: str = Query(..., min_length=1, max_length=100),
    db: AsyncSession = Depends(get_db),
):
    """Look up a single Hebrew word across words, forms, and conjugations.

    Returns the dictionary entry for the word, including conjugated verb forms.
    If the query contains nikkud, tries nikkud-aware matching first to
    disambiguate homographs (e.g. שְׁמוֹ 'his name' vs שָׂמוּ 'they put').
    """
    from app.services.text_analysis import ensure_caches
    from app.routers.reader import _lookup_word, _NIKKUD_RE

    word_cache, form_cache, conj_cache = await ensure_caches(db)
    raw = q.strip()
    clean = _NIKKUD_RE.sub("", raw)

    # If query has nikkud, try to find an exact nikkud match in the DB first
    has_nikkud = raw != clean
    if has_nikkud:
        nikkud_result = await _lookup_by_nikkud(db, raw, clean)
        if nikkud_result:
            return nikkud_result

    result = _lookup_word(clean, word_cache, form_cache, conj_cache)
    if not result:
        return None
    return result


async def _lookup_by_nikkud(db: AsyncSession, raw: str, clean: str) -> dict | None:
    """Try to find a word matching by nikkud to disambiguate homographs."""
    from app.models.word import Word

    # Check words table for nikkud match
    result = await db.execute(
        select(Word).where(Word.hebrew == clean, Word.nikkud == raw).limit(1)
    )
    word = result.scalar_one_or_none()
    if word:
        return {
            "word_id": word.id,
            "hebrew": word.hebrew,
            "translation_ru": word.translation_ru,
            "transliteration": word.transliteration,
            "pos": word.pos,
            "match_type": "nikkud_exact",
        }
    return None


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


@router.get("/roots/explore/{root_str}", response_model=RootExplorerResponse)
async def explore_root(root_str: str, db: AsyncSession = Depends(get_db)):
    data = await get_root_family_detail(db, root_str)
    if not data:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Root not found")
    words_by_pos = {
        pos: [RootExplorerWord.model_validate(w) for w in words]
        for pos, words in data["words_by_pos"].items()
    }
    return RootExplorerResponse(
        root=data["root"],
        meaning_ru=data["meaning_ru"],
        words_by_pos=words_by_pos,
        total_words=data["total_words"],
    )


@router.get("/roots/search")
async def search_roots(
    q: str = Query("", min_length=1),
    db: AsyncSession = Depends(get_db),
):
    results = await search_root_families(db, q)
    return results


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
