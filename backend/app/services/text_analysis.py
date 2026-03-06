"""Shared text analysis utilities — extracted from routers/reader.py."""

import asyncio
import re
import time

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.word import Word, WordForm
from app.models.grammar import VerbConjugation


# Application-level cache with TTL
_cache_word: dict[str, dict] | None = None
_cache_form: dict[str, dict] | None = None
_cache_conj: dict[str, dict] | None = None
_cache_time: float = 0
_cache_lock = asyncio.Lock()
_CACHE_TTL = 300  # 5 minutes

# Hebrew punctuation / connectors to strip when matching
_STRIP_RE = re.compile(r'[.,!?;:"\'"״""«»()\[\]{}/\\\u200F\u200E]')


async def ensure_caches(db: AsyncSession):
    """Build or refresh the word/form/conjugation caches."""
    global _cache_word, _cache_form, _cache_conj, _cache_time
    now = time.time()
    if _cache_word is None or (now - _cache_time) > _CACHE_TTL:
        async with _cache_lock:
            if _cache_word is None or (time.time() - _cache_time) > _CACHE_TTL:
                _cache_word = await _build_word_cache(db)
                _cache_form = await _build_form_cache(db)
                _cache_conj = await _build_conjugation_cache(db)
                _cache_time = time.time()
    return _cache_word, _cache_form, _cache_conj


def get_caches():
    """Return current caches (must call ensure_caches first)."""
    return _cache_word, _cache_form, _cache_conj


def extract_hebrew_tokens(text: str) -> list[str]:
    """Extract cleaned Hebrew tokens from text."""
    raw_tokens = re.split(r'\s+', text)
    tokens = []
    for raw in raw_tokens:
        if not raw or raw.isspace():
            continue
        clean = _STRIP_RE.sub("", raw)
        if clean:
            tokens.append(clean)
    return tokens


async def _build_word_cache(db: AsyncSession) -> dict[str, dict]:
    result = await db.execute(
        select(Word.id, Word.hebrew, Word.translation_ru, Word.transliteration,
               Word.pos, Word.root, Word.level_id, Word.frequency_rank)
        .order_by(
            func.coalesce(Word.level_id, 99).asc(),
            func.coalesce(Word.frequency_rank, 99).asc(),
            Word.id.asc(),
        )
    )
    cache: dict[str, dict] = {}
    for row in result:
        if row.hebrew not in cache:
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
        if row.hebrew not in cache:
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
        .where(Word.pos == "verb")
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
