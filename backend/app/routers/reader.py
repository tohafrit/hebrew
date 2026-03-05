"""Interactive reader — analyze Hebrew text and annotate words with dictionary data."""

import asyncio
import re
import time
from urllib.parse import quote

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.models.word import Word, WordForm
from app.models.grammar import VerbConjugation

router = APIRouter(tags=["reader"])

# Application-level cache with TTL
_cache_word: dict[str, dict] | None = None
_cache_form: dict[str, dict] | None = None
_cache_conj: dict[str, dict] | None = None
_cache_time: float = 0
_cache_lock = asyncio.Lock()
_CACHE_TTL = 300  # 5 minutes

# Hebrew punctuation / connectors to strip when matching
_STRIP_RE = re.compile(r'[.,!?;:"\'"״""«»()\[\]{}/\\\u200F\u200E]')
# Number patterns (plain digits, or digits with Hebrew prefix like ב-2, ו-50)
_NUMBER_RE = re.compile(r'^[בכלמוה]?-?[\d]+[,.]?[\d]*$')
# Common Hebrew prefixes (ב, כ, ל, מ, ה, ו, ש)
_PREFIXES = ["ו", "ה", "ב", "כ", "ל", "מ", "ש", "וה", "וב", "וכ", "ול", "ומ", "וש",
             "שה", "שב", "שכ", "של", "שמ", "מה", "בה", "כש", "לה"]

# Override translations for common function words where the dictionary
# entry is misleading (e.g. את as "you(f)" vs accusative marker)
_WORD_OVERRIDES: dict[str, dict] = {
    "את": {
        "translation_ru": "(предлог прямого дополнения); ты (ж.)",
        "pos": "particle",
    },
}

# Common Hebrew suffixes for noun/adjective inflection
# ים- (masculine plural), ות- (feminine plural), ת- (feminine singular),
# ה- (feminine/directional), י- (construct/possessive 1s), ן- (archaic feminine plural)
# ך- (possessive 2ms), כם- (possessive 2mp)
_SUFFIXES = ["ים", "ויות", "ות", "ית", "ת", "ה", "י", "יים", "יהם", "יהן", "נו", "הם", "הן", "ן", "ם", "ך", "כם", "כן", "ו"]

# Reverse sofit map — to convert final forms back to medial when stripping suffixes
_SOFIT_TO_REGULAR = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}
# Forward sofit map — to apply final letter form after stripping suffix
# e.g., ארצות → strip ות → ארצ → apply sofit → ארץ
_REGULAR_TO_SOFIT = {'כ': 'ך', 'מ': 'ם', 'נ': 'ן', 'פ': 'ף', 'צ': 'ץ'}


class CheckWritingRequest(BaseModel):
    text: str = Field(..., max_length=5000)


class UnknownWord(BaseModel):
    token: str
    suggestion: str | None = None
    dictionary_url: str | None = None


class CheckWritingResponse(BaseModel):
    word_count: int
    sentence_count: int
    known_count: int
    unknown_count: int
    known_pct: int
    level_breakdown: dict[str, int]
    unknown_words: list[UnknownWord]
    feedback: list[str]


class AnalyzeRequest(BaseModel):
    text: str = Field(..., max_length=10000)


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
    match_type: str | None = None  # "exact", "form", "conjugation", "prefix", "number", "proper_noun"
    is_space: bool = False
    dictionary_url: str | None = None  # link to external dictionary


class AnalyzeResponse(BaseModel):
    tokens: list[TokenAnnotation]
    stats: dict  # known_count, unknown_count, total_words


def _levenshtein(s: str, t: str) -> int:
    """Compute Levenshtein edit distance between two strings."""
    if len(s) < len(t):
        return _levenshtein(t, s)
    if not t:
        return len(s)
    prev = list(range(len(t) + 1))
    for i, sc in enumerate(s):
        curr = [i + 1]
        for j, tc in enumerate(t):
            cost = 0 if sc == tc else 1
            curr.append(min(curr[j] + 1, prev[j + 1] + 1, prev[j] + cost))
        prev = curr
    return prev[-1]


def _find_spelling_suggestion(token: str, word_cache: dict, max_dist: int = 2) -> str | None:
    """Find the closest word in the cache by Levenshtein distance."""
    best = None
    best_dist = max_dist + 1
    for hebrew in word_cache:
        if abs(len(hebrew) - len(token)) > max_dist:
            continue
        d = _levenshtein(token, hebrew)
        if d < best_dist:
            best_dist = d
            best = hebrew
            if d == 1:
                break  # good enough
    return best if best_dist <= max_dist else None


@router.post("/reader/check-writing", response_model=CheckWritingResponse)
async def check_writing(
    req: CheckWritingRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Rule-based writing feedback: word analysis, spelling suggestions, level breakdown."""
    text = req.text.strip()
    if not text:
        return CheckWritingResponse(
            word_count=0, sentence_count=0, known_count=0, unknown_count=0,
            known_pct=0, level_breakdown={}, unknown_words=[], feedback=[],
        )

    # Build caches
    global _cache_word, _cache_form, _cache_conj, _cache_time
    now = time.time()
    if _cache_word is None or (now - _cache_time) > _CACHE_TTL:
        async with _cache_lock:
            if _cache_word is None or (time.time() - _cache_time) > _CACHE_TTL:
                _cache_word = await _build_word_cache(db)
                _cache_form = await _build_form_cache(db)
                _cache_conj = await _build_conjugation_cache(db)
                _cache_time = time.time()
    word_cache = _cache_word
    form_cache = _cache_form
    conj_cache = _cache_conj

    # Count sentences (split by period, exclamation, question mark, or newline)
    sentence_count = max(1, len(re.split(r'[.!?\n]+', text.strip())))

    # Tokenize
    raw_tokens = re.split(r'(\s+)', text)
    known_count = 0
    total_words = 0
    level_counts: dict[str, int] = {}
    unknown_words: list[UnknownWord] = []

    for raw in raw_tokens:
        if not raw or raw.isspace():
            continue
        clean = _STRIP_RE.sub("", raw)
        if not clean:
            continue
        total_words += 1

        if _NUMBER_RE.match(clean):
            known_count += 1
            continue

        annotation = _lookup_word(clean, word_cache, form_cache, conj_cache)

        if annotation:
            known_count += 1
            level = str(annotation.get("level_id") or "?")
            level_counts[level] = level_counts.get(level, 0) + 1
        else:
            # Try to find a spelling suggestion
            suggestion = _find_spelling_suggestion(clean, word_cache)
            dict_url = _dictionary_url(clean)
            unknown_words.append(UnknownWord(
                token=clean,
                suggestion=suggestion,
                dictionary_url=dict_url,
            ))

    known_pct = round(known_count * 100 / total_words) if total_words > 0 else 0

    # Generate feedback
    feedback: list[str] = []
    if unknown_words:
        has_suggestions = sum(1 for w in unknown_words if w.suggestion)
        if has_suggestions:
            feedback.append(
                f"{len(unknown_words)} слов не найдены в словаре — возможно, ошибки в написании"
            )
        else:
            feedback.append(
                f"{len(unknown_words)} слов не найдены в словаре"
            )

    if known_pct >= 80:
        feedback.append("Отличный уровень: большинство слов вам знакомы")
    elif known_pct >= 60:
        feedback.append("Хороший уровень: больше половины слов знакомы")
    elif total_words > 0:
        feedback.append("Много незнакомых слов — попробуйте использовать более простую лексику")

    if total_words < 5:
        feedback.append("Попробуйте написать больше — хотя бы несколько предложений")
    elif total_words >= 20:
        feedback.append("Хороший объём текста!")

    # Encourage variety
    if level_counts:
        max_level = max(level_counts, key=lambda k: level_counts[k])
        if max_level in ("1", "2") and len(level_counts) < 3:
            feedback.append("Попробуйте использовать более разнообразную лексику")

    return CheckWritingResponse(
        word_count=total_words,
        sentence_count=sentence_count,
        known_count=known_count,
        unknown_count=len(unknown_words),
        known_pct=known_pct,
        level_breakdown=level_counts,
        unknown_words=unknown_words,
        feedback=feedback,
    )


@router.post("/reader/analyze", response_model=AnalyzeResponse)
async def analyze_text(
    req: AnalyzeRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    text = req.text.strip()
    if not text:
        return AnalyzeResponse(tokens=[], stats={"known_count": 0, "unknown_count": 0, "total_words": 0})

    # Build lookup caches from DB (cached at app level with TTL)
    global _cache_word, _cache_form, _cache_conj, _cache_time
    now = time.time()
    if _cache_word is None or (now - _cache_time) > _CACHE_TTL:
        async with _cache_lock:
            # Double-check after acquiring lock
            if _cache_word is None or (time.time() - _cache_time) > _CACHE_TTL:
                _cache_word = await _build_word_cache(db)
                _cache_form = await _build_form_cache(db)
                _cache_conj = await _build_conjugation_cache(db)
                _cache_time = time.time()
    word_cache = _cache_word
    form_cache = _cache_form
    conj_cache = _cache_conj

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

        # Number detection — before dictionary lookup
        if _NUMBER_RE.match(clean):
            tokens.append(TokenAnnotation(token=raw, clean=clean, match_type="number"))
            known_count += 1
            continue

        annotation = _lookup_word(clean, word_cache, form_cache, conj_cache)

        # Try hyphenated word parts if main lookup failed
        if not annotation and '-' in clean:
            parts = clean.split('-')
            # Try each part as a separate lookup, use the first that matches
            for part in parts:
                if part:
                    annotation = _lookup_word(part, word_cache, form_cache, conj_cache)
                    if annotation:
                        break

        if annotation:
            known_count += 1
            dict_word = annotation.get("hebrew", clean)
            annotation["dictionary_url"] = _dictionary_url(dict_word, annotation.get("pos"))
            tokens.append(TokenAnnotation(
                token=raw,
                clean=clean,
                **annotation,
            ))
        else:
            # Proper noun heuristic — after all lookups fail
            if _is_likely_proper_noun(raw):
                tokens.append(TokenAnnotation(token=raw, clean=clean, match_type="proper_noun"))
                known_count += 1
            else:
                tokens.append(TokenAnnotation(token=raw, clean=clean))

    # Second pass: aggressive proper noun detection for remaining unknowns
    # Check if text has any confirmed proper nouns (context clue)
    has_names = any(t.match_type == "proper_noun" for t in tokens)
    for i, t in enumerate(tokens):
        if t.is_space or not t.clean or t.word_id is not None or t.match_type:
            continue
        if _is_likely_proper_noun_aggressive(t.clean, has_names):
            tokens[i] = t.model_copy(update={"match_type": "proper_noun"})
            known_count += 1

    return AnalyzeResponse(
        tokens=tokens,
        stats={
            "known_count": known_count,
            "unknown_count": total_words - known_count,
            "total_words": total_words,
        },
    )


def _dictionary_url(hebrew: str, pos: str | None = None) -> str:
    """Build a link to an external Hebrew dictionary for this word.
    Verbs → Pealim (conjugation tables), other words → Milog (definitions).
    """
    encoded = quote(hebrew)
    if pos == "verb":
        return f"https://www.pealim.com/search/?q={encoded}"
    return f"https://milog.co.il/{encoded}"


def _is_likely_proper_noun(raw: str) -> bool:
    """Detect transliterated foreign names.

    Checks for:
    1. Embedded geresh (׳) or apostrophe — אנג׳לס, ג׳ון
    2. Double-vav (וו) or double-yod (יי) — common in transliterations
    3. Rare letter combinations that don't occur in native Hebrew words
    """
    inner = raw.strip("'׳\"״.,!?;:()")
    if '׳' in inner or "'" in inner:
        return True
    # Double letters common in transliteration: וו (W), יי (double-Y)
    if 'וו' in inner or 'יי' in inner:
        return True
    # Sequences rare/impossible in native Hebrew
    if any(combo in inner for combo in ['אא', 'ייד', 'יידס', 'אלל']):
        return True
    return False


# Common short Hebrew words to exclude from proper noun guessing
_COMMON_SHORT = {
    "גם", "רק", "כל", "עם", "אם", "אז", "פה", "שם", "מי", "מה", "זה", "זו", "זאת",
    "לא", "כן", "עד", "יש", "אל", "אף", "אך", "או", "כי", "בו", "לו", "בה", "לה",
    "לך", "בי", "לי", "די", "דם", "גב", "חג", "גן", "עז", "רב", "רע", "טל", "נא",
}


def _is_likely_proper_noun_aggressive(clean: str, context_has_names: bool) -> bool:
    """More aggressive proper noun detection for unmatched words.

    Called only after ALL dictionary lookups fail. Considers:
    - Short words (2-3 letters) that aren't common Hebrew words
    - Words near other detected proper nouns (context_has_names)
    - Transliteration patterns
    """
    if len(clean) <= 1:
        return False
    # Short unknown words adjacent to proper nouns are likely names too
    # (e.g. "לוס אנג׳לס" — לוס is unknown, אנג׳לס is proper noun)
    if context_has_names and len(clean) <= 4 and clean not in _COMMON_SHORT:
        return True
    # Words ending in unusual-for-Hebrew patterns
    if clean.endswith('רס') or clean.endswith('נס') or clean.endswith('לס'):
        return True
    return False


def _match_stem(stem: str, cache: dict) -> dict | None:
    """Try stem with sofit letter adjustments against a cache."""
    if not stem:
        return None
    if stem in cache:
        return cache[stem]
    if stem[-1] in _REGULAR_TO_SOFIT:
        v = stem[:-1] + _REGULAR_TO_SOFIT[stem[-1]]
        if v in cache:
            return cache[v]
    if stem[-1] in _SOFIT_TO_REGULAR:
        v = stem[:-1] + _SOFIT_TO_REGULAR[stem[-1]]
        if v in cache:
            return cache[v]
    return None


def _find_suffix_match(clean: str, cache: dict) -> dict | None:
    """Try suffix stripping to find a match. Returns the best (lowest level) match or None."""
    for suffix in _SUFFIXES:
        if clean.endswith(suffix) and len(clean) > len(suffix) + 1:
            stem = clean[:-len(suffix)]
            if suffix == "ויות" and stem:
                stem_ut = stem + 'ות'
                if stem_ut in cache:
                    return cache[stem_ut]
            # Direct match first
            if stem in cache:
                return cache[stem]
            # ות→ה (prefer מדינה over מדין via sofit)
            if suffix == "ות" and stem:
                stem_h = stem + 'ה'
                if stem_h in cache:
                    return cache[stem_h]
            # Sofit adjustments
            w = _match_stem(stem, cache)
            if w:
                return w
    return None


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
    4. Suffix stripping (plural/feminine — with sofit + ות→ה restoration)
    5. Verb conjugations
    6. Single-letter prefix → form_cache/conj_cache (+ construct state)
    7. Suffix stripping → form_cache (with sofit + ות→ה)
    8. Multi-letter prefixes
    9. Combined prefix + suffix (with sofit + ות→ה)
    10. Multi-letter prefix + suffix
    """

    # 1. Exact match in words table
    exact = word_cache.get(clean)
    if exact:
        # Apply overrides for common function words
        if clean in _WORD_OVERRIDES:
            exact = {**exact, **_WORD_OVERRIDES[clean]}
        exact_level = exact.get("level_id") or 99
        # If exact match is a common word (level 1-3), return immediately
        if exact_level <= 3:
            return {**exact, "match_type": "exact"}
        # High-level exact: check forms, conjugations, AND suffix stripping for lower-level alternatives
        # (e.g. ערבים lv5 "twilight" vs plural of ערב lv1 "evening",
        #        רחובות lv4 "Rehovot" vs plural of רחוב lv1 "street",
        #        ישנות lv4 "old age" vs form of ישן lv1 "old")
        best_alt = None
        best_alt_level = exact_level
        if clean in form_cache:
            fl = form_cache[clean].get("level_id") or 99
            if fl < best_alt_level:
                best_alt = {**form_cache[clean], "match_type": "form"}
                best_alt_level = fl
        if clean in conj_cache:
            cl = conj_cache[clean].get("level_id") or 99
            if cl < best_alt_level:
                best_alt = {**conj_cache[clean], "match_type": "conjugation"}
                best_alt_level = cl
        # Try suffix stripping — plural of a common word beats obscure exact match
        # Only for words long enough that suffix stripping is reliable (4+ chars)
        # Avoids false positives like לחן (melody lv4) → לח (moist lv1)
        if len(clean) >= 4:
            suffix_match = _find_suffix_match(clean, word_cache)
            if suffix_match:
                sl = suffix_match.get("level_id") or 99
                if sl < best_alt_level:
                    best_alt = {**suffix_match, "match_type": "form"}
                    best_alt_level = sl
        if best_alt and best_alt_level < exact_level:
            return best_alt
        return {**exact, "match_type": "exact"}

    # 2. Match in word_forms
    if clean in form_cache:
        return {**form_cache[clean], "match_type": "form"}

    # 2b. Check if the whole word is a verb conjugation before prefix stripping
    # (ביקש is past tense of לבקש, not ב+יקש)
    if clean in conj_cache:
        return {**conj_cache[clean], "match_type": "conjugation"}

    # 3. Single-letter prefix → word_cache (catches ל+בית, ה+ילדים, ב+ירושלים)
    #    Also checks conjugations and suffix stripping for better matches.
    for prefix in ["ה", "ו", "ב", "כ", "ל", "מ", "ש"]:
        if clean.startswith(prefix) and len(clean) > 2:
            stem = clean[len(prefix):]
            # Find the best prefix-stripped match (word, form, or conjugation)
            prefix_match = None
            prefix_level = 99
            # Check all three caches and pick the lowest level
            candidates = []
            if stem in word_cache:
                candidates.append((word_cache[stem].get("level_id") or 99, word_cache[stem], "prefix"))
            if stem in form_cache:
                candidates.append((form_cache[stem].get("level_id") or 99, form_cache[stem], "prefix"))
            if stem in conj_cache:
                candidates.append((conj_cache[stem].get("level_id") or 99, conj_cache[stem], "prefix"))
            if candidates:
                candidates.sort(key=lambda x: x[0])
                prefix_level, best, match_type = candidates[0]
                prefix_match = {**best, "match_type": match_type}
            if prefix_match:
                # Before accepting, check if suffix stripping gives a match at same or better level
                # Suffix stripping is more reliable than prefix stripping
                # (בנם: ב+נם lv4 vs בנ-ם→בן lv1; מדינות: מ+דינות lv4 vs מדינ+ות→מדינה lv4)
                better_suffix = _find_suffix_match(clean, word_cache)
                if better_suffix:
                    suffix_level = better_suffix.get("level_id") or 99
                    if suffix_level <= prefix_level:
                        return {**better_suffix, "match_type": "form"}
                return prefix_match

    # 4. Suffix stripping → word_cache (catches plural/feminine: ילדים→ילד)
    for suffix in _SUFFIXES:
        if clean.endswith(suffix) and len(clean) > len(suffix) + 1:
            stem = clean[:-len(suffix)]
            # Plural of -ות nouns: סוכנויות→סוכנ+ויות→סוכנות
            if suffix == "ויות" and stem:
                stem_ut = stem + 'ות'
                if stem_ut in word_cache:
                    return {**word_cache[stem_ut], "match_type": "form"}
            # For ות suffix: collect candidates from both direct stem and stem+ה,
            # pick the lowest level (ארוחות: ארוח lv4 vs ארוחה lv1 → pick ארוחה)
            if suffix == "ות" and stem:
                candidates_4 = []
                if stem in word_cache:
                    candidates_4.append(word_cache[stem])
                stem_h = stem + 'ה'
                if stem_h in word_cache:
                    candidates_4.append(word_cache[stem_h])
                s = _match_stem(stem, word_cache)
                if s:
                    candidates_4.append(s)
                if candidates_4:
                    candidates_4.sort(key=lambda x: x.get("level_id") or 99)
                    return {**candidates_4[0], "match_type": "form"}
            else:
                # Non-ות suffixes: direct stem match
                if stem in word_cache:
                    return {**word_cache[stem], "match_type": "form"}
                # Sofit letter adjustments (ארצים→ארצ→ארץ)
                w = _match_stem(stem, word_cache)
                if w:
                    return {**w, "match_type": "form"}
            # Suffix + construct state: הולדתו→הולדת+ו→הולדה
            if stem and stem.endswith('ת') and len(stem) > 2:
                construct = stem[:-1] + 'ה'
                if construct in word_cache:
                    return {**word_cache[construct], "match_type": "form"}

    # 4b. Construct state: ת at end of word → try replacing with ה
    # (ארוחת→ארוחה, משפחת→משפחה, תוכנת→תוכנה)
    # Skip words ending in ות (plural) — handled by suffix stripping above
    if clean.endswith('ת') and not clean.endswith('ות') and len(clean) > 2:
        construct_stem = clean[:-1] + 'ה'
        if construct_stem in word_cache:
            return {**word_cache[construct_stem], "match_type": "form"}

    # 4c. Single-letter prefix + construct state: בשנת = ב + שנת → שנה
    # Skip words ending in ות (plural) — those are handled by suffix stripping
    for prefix in ["ה", "ו", "ב", "כ", "ל", "מ", "ש"]:
        if clean.startswith(prefix) and len(clean) > 3:
            stem = clean[len(prefix):]
            if stem.endswith('ת') and not stem.endswith('ות') and len(stem) > 2:
                construct = stem[:-1] + 'ה'
                if construct in word_cache:
                    return {**word_cache[construct], "match_type": "prefix"}

    # 5. Verb conjugations — already checked in step 2b above, but kept as fallback
    #    in case earlier steps didn't cover all paths
    if clean in conj_cache:
        return {**conj_cache[clean], "match_type": "conjugation"}

    # 6. Single-letter prefix → form_cache/conj_cache (+ construct state)
    for prefix in ["ה", "ו", "ב", "כ", "ל", "מ", "ש"]:
        if clean.startswith(prefix) and len(clean) > 2:
            stem = clean[len(prefix):]
            if stem in form_cache:
                return {**form_cache[stem], "match_type": "prefix"}
            if stem in conj_cache:
                return {**conj_cache[stem], "match_type": "prefix"}
            # Construct state after prefix → form_cache
            if stem.endswith('ת') and len(stem) > 2:
                construct = stem[:-1] + 'ה'
                if construct in form_cache:
                    return {**form_cache[construct], "match_type": "prefix"}

    # 7. Suffix stripping → form_cache (with sofit + ות→ה restoration)
    for suffix in _SUFFIXES:
        if clean.endswith(suffix) and len(clean) > len(suffix) + 1:
            stem = clean[:-len(suffix)]
            # ות→ה before sofit
            if suffix == "ות" and stem:
                stem_h = stem + 'ה'
                if stem_h in form_cache:
                    return {**form_cache[stem_h], "match_type": "form"}
            w = _match_stem(stem, form_cache)
            if w:
                return {**w, "match_type": "form"}

    # 8. Combined single prefix + suffix stripping (with sofit + ות→ה)
    #    (Before multi-letter prefixes so ו+מדינ+ות→מדינה wins over ומ+דינות)
    for prefix in ["ה", "ו", "ב", "כ", "ל", "מ", "ש"]:
        if clean.startswith(prefix) and len(clean) > 3:
            after_prefix = clean[len(prefix):]
            for suffix in _SUFFIXES:
                if after_prefix.endswith(suffix) and len(after_prefix) > len(suffix) + 1:
                    inner = after_prefix[:-len(suffix)]
                    # ויות→stem+ות (הרשויות = ה + רש + ויות → רשות)
                    if suffix == "ויות" and inner:
                        inner_ut = inner + 'ות'
                        if inner_ut in word_cache:
                            return {**word_cache[inner_ut], "match_type": "prefix"}
                    # Direct stem match first (מקצועות → מקצוע)
                    if inner in word_cache:
                        return {**word_cache[inner], "match_type": "prefix"}
                    if inner in form_cache:
                        return {**form_cache[inner], "match_type": "prefix"}
                    # ות→stem+ה (מדינות → מדינ → מדינה)
                    if suffix == "ות" and inner:
                        inner_h = inner + 'ה'
                        if inner_h in word_cache:
                            return {**word_cache[inner_h], "match_type": "prefix"}
                        if inner_h in form_cache:
                            return {**form_cache[inner_h], "match_type": "prefix"}
                    # Sofit letter adjustments
                    w = _match_stem(inner, word_cache)
                    if w:
                        return {**w, "match_type": "prefix"}
                    w = _match_stem(inner, form_cache)
                    if w:
                        return {**w, "match_type": "prefix"}

    # 9. Multi-letter prefixes (וה, של, כש, etc.)
    for prefix in _PREFIXES:
        if len(prefix) > 1 and clean.startswith(prefix) and len(clean) > len(prefix) + 1:
            stem = clean[len(prefix):]
            if stem in word_cache:
                return {**word_cache[stem], "match_type": "prefix"}
            if stem in form_cache:
                return {**form_cache[stem], "match_type": "prefix"}
            if stem in conj_cache:
                return {**conj_cache[stem], "match_type": "prefix"}
            # Construct state after multi-letter prefix
            if stem.endswith('ת') and len(stem) > 2:
                construct = stem[:-1] + 'ה'
                if construct in word_cache:
                    return {**word_cache[construct], "match_type": "prefix"}

    # 10. Multi-letter prefix + suffix stripping (with sofit + ות→ה)
    for prefix in _PREFIXES:
        if len(prefix) > 1 and clean.startswith(prefix) and len(clean) > len(prefix) + 2:
            after_prefix = clean[len(prefix):]
            for suffix in _SUFFIXES:
                if after_prefix.endswith(suffix) and len(after_prefix) > len(suffix) + 1:
                    inner = after_prefix[:-len(suffix)]
                    # ות→stem+ה before sofit
                    if suffix == "ות" and inner:
                        inner_h = inner + 'ה'
                        if inner_h in word_cache:
                            return {**word_cache[inner_h], "match_type": "prefix"}
                    w = _match_stem(inner, word_cache)
                    if w:
                        return {**w, "match_type": "prefix"}
                    w = _match_stem(inner, form_cache)
                    if w:
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
