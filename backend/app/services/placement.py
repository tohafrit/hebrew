"""Placement test: 28 questions (4 per level 1-7) to auto-assign starting level."""

import random
import re
import uuid
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.word import Word
from app.models.content import PlacementTestResult
from app.models.user import User


async def generate_placement_test(db: AsyncSession) -> list[dict]:
    """Generate 28 placement questions: 4 per level (1-7).

    Per level: 2x multiple_choice + 1x fill_blank + 1x translate_ru_he.
    """
    questions = []
    idx = 0

    for level in range(1, 8):
        # Get words for this level, prefer high-frequency
        result = await db.execute(
            select(Word)
            .where(Word.level_id == level)
            .order_by(Word.frequency_rank.asc().nulls_last())
            .limit(30)
        )
        level_words = list(result.scalars().all())

        if len(level_words) < 4:
            # Not enough words for this level, fill with what we have
            level_words = level_words * 4

        sampled = random.sample(level_words, min(4, len(level_words)))

        # Collect distractors from same level
        all_translations = [w.translation_ru for w in level_words]
        all_hebrew = [w.hebrew for w in level_words]

        for i, word in enumerate(sampled):
            if i < 2:
                # Multiple choice: show Hebrew, pick Russian translation
                distractors = [t for t in all_translations if t != word.translation_ru]
                distractor_sample = random.sample(distractors, min(3, len(distractors)))
                options = [word.translation_ru] + distractor_sample
                random.shuffle(options)

                questions.append({
                    "index": idx,
                    "level": level,
                    "type": "multiple_choice",
                    "prompt_he": word.nikkud or word.hebrew,
                    "prompt_ru": None,
                    "hint": word.transliteration,
                    "options": options,
                    "correct_answer": word.translation_ru,
                })
            elif i == 2:
                # Fill blank: show Russian, type Hebrew
                questions.append({
                    "index": idx,
                    "level": level,
                    "type": "fill_blank",
                    "prompt_he": None,
                    "prompt_ru": word.translation_ru,
                    "hint": word.transliteration,
                    "options": None,
                    "correct_answer": word.hebrew,
                })
            else:
                # Translate RU→HE: show Russian, pick Hebrew
                distractors = [h for h in all_hebrew if h != word.hebrew]
                distractor_sample = random.sample(distractors, min(3, len(distractors)))
                options = [word.hebrew] + distractor_sample
                random.shuffle(options)

                questions.append({
                    "index": idx,
                    "level": level,
                    "type": "translate_ru_he",
                    "prompt_he": None,
                    "prompt_ru": word.translation_ru,
                    "hint": None,
                    "options": options,
                    "correct_answer": word.hebrew,
                })
            idx += 1

    return questions


def _strip_nikkud(text: str) -> str:
    """Remove Hebrew vowel marks."""
    return re.sub(r"[\u0591-\u05C7]", "", text).replace("\u05BE", "-")


def score_placement_test(
    questions: list[dict],
    answers: list[dict],
) -> tuple[int, int, int, dict]:
    """Score placement test. Returns (assigned_level, total_correct, total_questions, per_level)."""
    answer_map = {a["index"]: a["answer"] for a in answers}

    per_level: dict[int, dict] = {}
    total_correct = 0

    for q in questions:
        level = q["level"]
        if level not in per_level:
            per_level[level] = {"correct": 0, "total": 0}
        per_level[level]["total"] += 1

        user_answer = answer_map.get(q["index"], "")
        correct = q["correct_answer"]

        # Compare stripping nikkud
        is_correct = (
            user_answer.strip() == correct.strip()
            or _strip_nikkud(user_answer.strip()) == _strip_nikkud(correct.strip())
        )

        if is_correct:
            per_level[level]["correct"] += 1
            total_correct += 1

    # Assign level: highest level with ≥70% accuracy
    assigned_level = 1
    for level in range(1, 8):
        stats = per_level.get(level, {"correct": 0, "total": 4})
        if stats["total"] > 0 and stats["correct"] / stats["total"] >= 0.7:
            assigned_level = level
        else:
            break

    per_level_str = {str(k): v for k, v in per_level.items()}
    return assigned_level, total_correct, len(questions), per_level_str


async def save_placement_result(
    db: AsyncSession,
    user: User,
    assigned_level: int,
    total_correct: int,
    total_questions: int,
    score_json: dict,
) -> None:
    """Save placement result and update user level."""
    result = PlacementTestResult(
        user_id=user.id,
        assigned_level=assigned_level,
        score_json=score_json,
        total_questions=total_questions,
        total_correct=total_correct,
    )
    db.add(result)
    user.current_level = assigned_level
    await db.commit()
