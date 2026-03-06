"""Classify wrong answers into error pattern categories with personalized tips."""

import re
import uuid
from collections import Counter

from sqlalchemy.ext.asyncio import AsyncSession

from app.services.mistakes import get_exercise_mistakes

# Similar sound pairs in Hebrew
SIMILAR_SOUND_PAIRS = [
    ("כ", "ח"), ("ק", "כ"), ("ט", "ת"), ("ס", "שׂ"), ("א", "ע"),
    ("ד", "ר"), ("ב", "ו"), ("ח", "ה"), ("שׁ", "שׂ"), ("צ", "ס"),
]

# Gender suffixes
GENDER_SUFFIXES = ["ה", "ים", "ות", "ת"]

# Tips per pattern type (in Russian)
PATTERN_TIPS = {
    "gender_confusion": "Обратите внимание на окончания: -ים для мужского множественного, -ות для женского множественного, -ה/-ת для женского единственного.",
    "similar_sounds": "Путаница похожих звуков. Слушайте TTS внимательно и практикуйте минимальные пары (/minimal-pairs).",
    "vowel_errors": "Ошибки в огласовках (никуд). Включите показ никуда в настройках и обращайте внимание на точки.",
    "word_order": "Ошибки в порядке слов. В иврите порядок обычно: подлежащее-сказуемое-дополнение.",
    "spelling": "Орфографические ошибки. Практикуйте написание в разделе «Письмо» (/handwriting).",
    "other": "Разные ошибки. Повторите проблемные слова через SRS-карточки.",
}

PATTERN_NAMES = {
    "gender_confusion": "Путаница рода",
    "similar_sounds": "Похожие звуки",
    "vowel_errors": "Ошибки огласовок",
    "word_order": "Порядок слов",
    "spelling": "Орфография",
    "other": "Другие",
}


def _strip_nikkud(text: str) -> str:
    return re.sub(r"[\u0591-\u05C7]", "", text).replace("\u05BE", "-")


def _classify_error(user_answer: str, correct_answer: str, exercise_type: str) -> str:
    """Classify a single error into a category."""
    user_clean = _strip_nikkud(user_answer.strip())
    correct_clean = _strip_nikkud(correct_answer.strip())

    if not user_clean or not correct_clean:
        return "other"

    # Gender confusion: differs only in gender suffix
    for suffix in GENDER_SUFFIXES:
        if correct_clean.endswith(suffix) and not user_clean.endswith(suffix):
            # Check if base is similar
            base_correct = correct_clean[:-len(suffix)]
            if user_clean.startswith(base_correct[:max(2, len(base_correct) - 1)]):
                return "gender_confusion"
        if user_clean.endswith(suffix) and not correct_clean.endswith(suffix):
            base_user = user_clean[:-len(suffix)]
            if correct_clean.startswith(base_user[:max(2, len(base_user) - 1)]):
                return "gender_confusion"

    # Similar sounds: one consonant differs by a known pair
    if len(user_clean) == len(correct_clean):
        diffs = [(u, c) for u, c in zip(user_clean, correct_clean) if u != c]
        if len(diffs) == 1:
            u_char, c_char = diffs[0]
            for a, b in SIMILAR_SOUND_PAIRS:
                if (u_char == a and c_char == b) or (u_char == b and c_char == a):
                    return "similar_sounds"

    # Vowel errors: stripped nikkud matches
    if user_clean == correct_clean and user_answer.strip() != correct_answer.strip():
        return "vowel_errors"

    # Word order: same words different order
    if exercise_type == "word_order":
        return "word_order"

    # Spelling: close but not matching
    if abs(len(user_clean) - len(correct_clean)) <= 2:
        return "spelling"

    return "other"


async def analyze_error_patterns(
    db: AsyncSession, user_id: uuid.UUID, days: int = 30
) -> dict:
    """Analyze user's mistakes and classify into error patterns."""
    mistakes = await get_exercise_mistakes(db, user_id, days=days, limit=200)

    if not mistakes:
        return {
            "patterns": [],
            "total_mistakes": 0,
            "top_pattern": None,
        }

    pattern_counts: Counter = Counter()
    pattern_examples: dict[str, list] = {}

    for m in mistakes:
        user_answer_text = ""
        correct_answer_text = ""

        if m.get("user_answer"):
            user_answer_text = str(
                m["user_answer"].get("text", "")
                or m["user_answer"].get("answer", "")
                or m["user_answer"].get("selected", "")
            )
        if m.get("correct_answer"):
            correct_answer_text = str(
                m["correct_answer"].get("text", "")
                or m["correct_answer"].get("answer", "")
                or m["correct_answer"].get("correct", "")
            )

        if not user_answer_text and not correct_answer_text:
            pattern_type = "other"
        else:
            pattern_type = _classify_error(
                user_answer_text, correct_answer_text, m.get("exercise_type", "")
            )

        pattern_counts[pattern_type] += 1
        if pattern_type not in pattern_examples:
            pattern_examples[pattern_type] = []
        if len(pattern_examples[pattern_type]) < 3:
            pattern_examples[pattern_type].append({
                "user_answer": user_answer_text,
                "correct_answer": correct_answer_text,
                "exercise_type": m.get("exercise_type", ""),
            })

    total = sum(pattern_counts.values())
    patterns = []
    for pattern_type, count in pattern_counts.most_common():
        patterns.append({
            "type": pattern_type,
            "name": PATTERN_NAMES.get(pattern_type, pattern_type),
            "count": count,
            "pct": round(count / total * 100) if total > 0 else 0,
            "examples": pattern_examples.get(pattern_type, []),
            "tip": PATTERN_TIPS.get(pattern_type, ""),
        })

    return {
        "patterns": patterns,
        "total_mistakes": total,
        "top_pattern": patterns[0]["type"] if patterns else None,
    }
