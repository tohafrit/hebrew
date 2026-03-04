"""Interactive reader — analyze Hebrew text and annotate words with dictionary data."""

import re

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.word import Word, WordForm
from app.models.grammar import VerbConjugation

router = APIRouter(tags=["reader"])

# Hebrew punctuation / connectors to strip when matching
_STRIP_RE = re.compile(r'[.,!?;:"\'"״""«»()\[\]{}\u05BE\u200F\u200E]')
# Common Hebrew prefixes (ב, כ, ל, מ, ה, ו, ש)
_PREFIXES = ["ו", "ה", "ב", "כ", "ל", "מ", "ש", "וה", "וב", "וכ", "ול", "ומ", "וש",
             "שה", "שב", "שכ", "של", "שמ", "מה", "בה", "כש", "לה"]

# Common Hebrew suffixes for noun/adjective inflection
# ים- (masculine plural), ות- (feminine plural), ת- (feminine singular),
# ה- (feminine/directional), י- (construct/possessive 1s), ן- (archaic feminine plural)
_SUFFIXES = ["ים", "ות", "ית", "ת", "ה", "י", "יים", "ן", "ם"]


class AnalyzeRequest(BaseModel):
    text: str


class TokenAnnotation(BaseModel):
    token: str  # original token as it appears in text
    clean: str  # cleaned form (no punctuation)
    word_id: int | None = None
    hebrew: str | None = None  # dictionary form
    translation_ru: str | None = None
    transliteration: str | None = None
    pos: str | None = None
    root: str | None = None
    level_id: int | None = None
    match_type: str | None = None  # "exact", "form", "conjugation", "prefix"
    is_space: bool = False


class AnalyzeResponse(BaseModel):
    tokens: list[TokenAnnotation]
    stats: dict  # known_count, unknown_count, total_words


@router.post("/reader/analyze", response_model=AnalyzeResponse)
async def analyze_text(
    req: AnalyzeRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    text = req.text.strip()
    if not text:
        return AnalyzeResponse(tokens=[], stats={"known_count": 0, "unknown_count": 0, "total_words": 0})

    # Build lookup caches from DB
    word_cache = await _build_word_cache(db)
    form_cache = await _build_form_cache(db)
    conj_cache = await _build_conjugation_cache(db)

    # Tokenize: split on whitespace, keeping newlines as separate tokens
    raw_tokens = re.split(r'(\s+)', text)

    tokens: list[TokenAnnotation] = []
    known_count = 0
    total_words = 0

    for raw in raw_tokens:
        if not raw:
            continue
        if raw.isspace():
            tokens.append(TokenAnnotation(token=raw, clean="", is_space=True))
            continue

        clean = _STRIP_RE.sub("", raw)
        if not clean:
            tokens.append(TokenAnnotation(token=raw, clean=""))
            continue

        total_words += 1
        annotation = _lookup_word(clean, word_cache, form_cache, conj_cache)

        if annotation:
            known_count += 1
            tokens.append(TokenAnnotation(
                token=raw,
                clean=clean,
                **annotation,
            ))
        else:
            tokens.append(TokenAnnotation(token=raw, clean=clean))

    return AnalyzeResponse(
        tokens=tokens,
        stats={
            "known_count": known_count,
            "unknown_count": total_words - known_count,
            "total_words": total_words,
        },
    )


def _lookup_word(
    clean: str,
    word_cache: dict,
    form_cache: dict,
    conj_cache: dict,
) -> dict | None:
    """Try to match a token against dictionary, forms, conjugations, with prefix/suffix stripping.

    Priority order reflects Hebrew morphology reliability:
    1. Exact matches (most reliable)
    2. Word forms from DB
    3. Single-letter prefix stripping (ה/ב/כ/ל/מ/ו/ש — very common, reliable)
    4. Suffix stripping (plural/feminine — less reliable, can produce false stems)
    5. Verb conjugations
    6. Multi-letter prefixes
    7. Combined prefix + suffix
    """

    # 1. Exact match in words table
    if clean in word_cache:
        w = word_cache[clean]
        return {**w, "match_type": "exact"}

    # 2. Match in word_forms
    if clean in form_cache:
        w = form_cache[clean]
        return {**w, "match_type": "form"}

    # 3. Single-letter prefix → word_cache (catches ל+בית, ה+ילדים, ב+ירושלים)
    for prefix in ["ה", "ו", "ב", "כ", "ל", "מ", "ש"]:
        if clean.startswith(prefix) and len(clean) > 2:
            stem = clean[len(prefix):]
            if stem in word_cache:
                w = word_cache[stem]
                return {**w, "match_type": "prefix"}

    # 4. Suffix stripping → word_cache (catches plural/feminine: ילדים→ילד)
    for suffix in _SUFFIXES:
        if clean.endswith(suffix) and len(clean) > len(suffix) + 1:
            stem = clean[:-len(suffix)]
            if stem in word_cache:
                w = word_cache[stem]
                return {**w, "match_type": "form"}

    # 5. Verb conjugations (only actual verbs, filtered at cache build time)
    if clean in conj_cache:
        w = conj_cache[clean]
        return {**w, "match_type": "conjugation"}

    # 6. Single-letter prefix → form_cache/conj_cache
    for prefix in ["ה", "ו", "ב", "כ", "ל", "מ", "ש"]:
        if clean.startswith(prefix) and len(clean) > 2:
            stem = clean[len(prefix):]
            if stem in form_cache:
                w = form_cache[stem]
                return {**w, "match_type": "prefix"}
            if stem in conj_cache:
                w = conj_cache[stem]
                return {**w, "match_type": "prefix"}

    # 7. Suffix stripping → form_cache
    for suffix in _SUFFIXES:
        if clean.endswith(suffix) and len(clean) > len(suffix) + 1:
            stem = clean[:-len(suffix)]
            if stem in form_cache:
                w = form_cache[stem]
                return {**w, "match_type": "form"}

    # 8. Multi-letter prefixes (וה, של, כש, etc.)
    for prefix in _PREFIXES:
        if len(prefix) > 1 and clean.startswith(prefix) and len(clean) > len(prefix) + 1:
            stem = clean[len(prefix):]
            if stem in word_cache:
                w = word_cache[stem]
                return {**w, "match_type": "prefix"}
            if stem in form_cache:
                w = form_cache[stem]
                return {**w, "match_type": "prefix"}
            if stem in conj_cache:
                w = conj_cache[stem]
                return {**w, "match_type": "prefix"}

    # 9. Combined prefix + suffix stripping
    for prefix in ["ה", "ו", "ב", "כ", "ל", "מ", "ש"]:
        if clean.startswith(prefix) and len(clean) > 3:
            after_prefix = clean[len(prefix):]
            for suffix in _SUFFIXES:
                if after_prefix.endswith(suffix) and len(after_prefix) > len(suffix) + 1:
                    inner = after_prefix[:-len(suffix)]
                    if inner in word_cache:
                        w = word_cache[inner]
                        return {**w, "match_type": "prefix"}
                    if inner in form_cache:
                        w = form_cache[inner]
                        return {**w, "match_type": "prefix"}

    return None


async def _build_word_cache(db: AsyncSession) -> dict[str, dict]:
    """Build hebrew -> word info dict for all words.
    Prioritize: low level (basic) > high frequency > low ID.
    """
    result = await db.execute(
        select(Word.id, Word.hebrew, Word.translation_ru, Word.transliteration,
               Word.pos, Word.root, Word.level_id, Word.frequency_rank)
        .order_by(
            # Prefer lower level (more basic words first)
            func.coalesce(Word.level_id, 99).asc(),
            # Then by frequency_rank (1=high, 4=rare, NULL last)
            func.coalesce(Word.frequency_rank, 99).asc(),
            Word.id.asc(),
        )
    )
    cache: dict[str, dict] = {}
    for row in result:
        if row.hebrew not in cache:  # first (highest priority) wins
            cache[row.hebrew] = {
                "word_id": row.id,
                "hebrew": row.hebrew,
                "translation_ru": row.translation_ru,
                "transliteration": row.transliteration,
                "pos": row.pos,
                "root": row.root,
                "level_id": row.level_id,
            }
    return cache


async def _build_form_cache(db: AsyncSession) -> dict[str, dict]:
    """Build form_hebrew -> parent word info dict."""
    result = await db.execute(
        select(
            WordForm.hebrew,
            WordForm.form_type,
            Word.id,
            Word.hebrew.label("word_hebrew"),
            Word.translation_ru,
            Word.transliteration,
            Word.pos,
            Word.root,
            Word.level_id,
        ).join(Word, WordForm.word_id == Word.id)
        .order_by(func.coalesce(Word.level_id, 99).asc(),
                  func.coalesce(Word.frequency_rank, 99).asc(),
                  Word.id.asc())
    )
    cache: dict[str, dict] = {}
    for row in result:
        if row.hebrew not in cache:  # first match wins
            cache[row.hebrew] = {
                "word_id": row.id,
                "hebrew": row.word_hebrew,
                "translation_ru": row.translation_ru,
                "transliteration": row.transliteration,
                "pos": row.pos,
                "root": row.root,
                "level_id": row.level_id,
            }
    return cache


async def _build_conjugation_cache(db: AsyncSession) -> dict[str, dict]:
    """Build conjugated_form -> parent word info dict. Prioritize high-frequency words."""
    result = await db.execute(
        select(
            VerbConjugation.form_he,
            Word.id,
            Word.hebrew.label("word_hebrew"),
            Word.translation_ru,
            Word.transliteration,
            Word.pos,
            Word.root,
            Word.level_id,
        ).join(Word, VerbConjugation.word_id == Word.id)
        .where(Word.pos == "verb")  # Only actual verbs, not nouns with erroneous conjugations
        .order_by(func.coalesce(Word.level_id, 99).asc(),
                  func.coalesce(Word.frequency_rank, 99).asc(),
                  Word.id.asc())
    )
    cache: dict[str, dict] = {}
    for row in result:
        if row.form_he not in cache:
            cache[row.form_he] = {
                "word_id": row.id,
                "hebrew": row.word_hebrew,
                "translation_ru": row.translation_ru,
                "transliteration": row.transliteration,
                "pos": row.pos,
                "root": row.root,
                "level_id": row.level_id,
            }
    return cache
