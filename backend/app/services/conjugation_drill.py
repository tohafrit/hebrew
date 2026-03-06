import random
import re

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.grammar import VerbConjugation, Binyan
from app.models.word import Word


async def generate_drill_questions(
    db: AsyncSession,
    *,
    level_id: int | None = None,
    binyan_id: int | None = None,
    tense: str | None = None,
    count: int = 10,
) -> list[dict]:
    """Generate conjugation drill questions from existing verb_conjugations data."""
    q = (
        select(VerbConjugation, Word.hebrew, Word.nikkud, Word.translation_ru, Binyan.name_ru)
        .join(Word, VerbConjugation.word_id == Word.id)
        .join(Binyan, VerbConjugation.binyan_id == Binyan.id)
    )
    if level_id is not None:
        q = q.where(Word.level_id == level_id)
    if binyan_id is not None:
        q = q.where(VerbConjugation.binyan_id == binyan_id)
    if tense is not None:
        q = q.where(VerbConjugation.tense == tense)

    result = await db.execute(q)
    rows = result.all()

    if not rows:
        return []

    # Shuffle and take up to count
    sampled = random.sample(rows, min(count, len(rows)))

    # Collect all form_he for distractors
    all_forms = list({r[0].form_he for r in rows})

    questions = []
    for conj, word_he, word_nikkud, translation_ru, binyan_name in sampled:
        # Generate 3 distractors from other forms
        distractors = [f for f in all_forms if f != conj.form_he]
        distractor_sample = random.sample(distractors, min(3, len(distractors)))
        options = [conj.form_he] + distractor_sample
        random.shuffle(options)

        questions.append({
            "word_id": conj.word_id,
            "word_hebrew": word_he,
            "word_nikkud": word_nikkud,
            "translation_ru": translation_ru,
            "binyan_id": conj.binyan_id,
            "binyan_name": binyan_name,
            "tense": conj.tense,
            "person": conj.person,
            "gender": conj.gender,
            "number": conj.number,
            "correct_answer": conj.form_he,
            "correct_nikkud": conj.form_nikkud,
            "transliteration": conj.transliteration,
            "options": options,
        })

    return questions


async def generate_table_drill(
    db: AsyncSession,
    *,
    word_id: int | None = None,
    binyan_id: int | None = None,
    tense: str | None = None,
    level_id: int | None = None,
    blank_count: int = 5,
) -> dict | None:
    """Generate a full conjugation table with some cells blanked."""
    q = (
        select(VerbConjugation, Word.hebrew, Word.nikkud, Word.translation_ru, Binyan.name_ru)
        .join(Word, VerbConjugation.word_id == Word.id)
        .join(Binyan, VerbConjugation.binyan_id == Binyan.id)
    )
    if word_id:
        q = q.where(VerbConjugation.word_id == word_id)
    if binyan_id:
        q = q.where(VerbConjugation.binyan_id == binyan_id)
    if tense:
        q = q.where(VerbConjugation.tense == tense)
    if level_id:
        q = q.where(Word.level_id == level_id)

    q = q.order_by(VerbConjugation.word_id, VerbConjugation.tense, VerbConjugation.id)
    result = await db.execute(q)
    rows = result.all()

    if not rows:
        return None

    # Pick a random verb+tense group
    groups: dict[tuple, list] = {}
    for conj, word_he, word_nikkud, translation_ru, binyan_name in rows:
        key = (conj.word_id, conj.binyan_id, conj.tense)
        if key not in groups:
            groups[key] = {
                "word_hebrew": word_he,
                "word_nikkud": word_nikkud,
                "translation_ru": translation_ru,
                "binyan_name": binyan_name,
                "tense": conj.tense,
                "word_id": conj.word_id,
                "binyan_id": conj.binyan_id,
                "cells": [],
            }
        groups[key]["cells"].append({
            "person": conj.person,
            "gender": conj.gender,
            "number": conj.number,
            "form_he": conj.form_he,
            "form_nikkud": conj.form_nikkud,
            "transliteration": conj.transliteration,
            "is_blank": False,
        })

    group = random.choice(list(groups.values()))
    cells = group["cells"]

    # Randomly blank cells, keep at least 2 visible
    n_blank = min(blank_count, max(0, len(cells) - 2))
    blank_indices = random.sample(range(len(cells)), n_blank)
    for idx in blank_indices:
        cells[idx]["is_blank"] = True

    return group


def _strip_nikkud(text: str) -> str:
    """Remove Hebrew vowel marks (nikkud) from text."""
    return re.sub(r"[\u0591-\u05C7]", "", text).replace("\u05BE", "-")


async def check_drill_answer(
    db: AsyncSession,
    *,
    word_id: int,
    binyan_id: int,
    tense: str,
    person: str,
    answer: str,
) -> dict:
    """Check if the user's answer matches the expected conjugation form."""
    result = await db.execute(
        select(VerbConjugation).where(
            VerbConjugation.word_id == word_id,
            VerbConjugation.binyan_id == binyan_id,
            VerbConjugation.tense == tense,
            VerbConjugation.person == person,
        )
    )
    conj = result.scalar_one_or_none()
    if not conj:
        return {"correct": False, "correct_answer": "", "correct_nikkud": None, "transliteration": None}

    # Compare stripping nikkud from both
    user_clean = _strip_nikkud(answer.strip())
    correct_clean = _strip_nikkud(conj.form_he)
    is_correct = user_clean == correct_clean

    # Also accept nikkud form match
    if not is_correct and conj.form_nikkud:
        is_correct = user_clean == _strip_nikkud(conj.form_nikkud)

    return {
        "correct": is_correct,
        "correct_answer": conj.form_he,
        "correct_nikkud": conj.form_nikkud,
        "transliteration": conj.transliteration,
    }
