"""Auto-generate fill-in-the-blank exercises from ReadingText vocabulary."""

import random
import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import ReadingText


async def generate_cloze_from_text(
    db: AsyncSession, text_id: int, count: int = 10
) -> list[dict]:
    """Generate cloze exercises from a reading text's vocabulary and content."""
    result = await db.execute(
        select(ReadingText).where(ReadingText.id == text_id)
    )
    text = result.scalar_one_or_none()
    if not text:
        return []

    vocab = text.vocabulary_json or []
    if not vocab:
        return []

    # Split content into sentences
    he_sentences = re.split(r'[.!?]\s*', text.content_he.strip())
    ru_sentences = re.split(r'[.!?]\s*', text.content_ru.strip())
    he_sentences = [s.strip() for s in he_sentences if s.strip()]
    ru_sentences = [s.strip() for s in ru_sentences if s.strip()]

    exercises = []
    for word_entry in vocab:
        he_word = word_entry.get("he", "")
        ru_word = word_entry.get("ru", "")
        translit = word_entry.get("translit", "")

        if not he_word or not ru_word:
            continue

        # Find a sentence containing this word
        matching_he = None
        matching_ru = None
        for i, sent in enumerate(he_sentences):
            if he_word in sent:
                matching_he = sent
                if i < len(ru_sentences):
                    matching_ru = ru_sentences[i]
                break

        if not matching_he:
            # Use a simple prompt instead
            matching_he = he_word
            matching_ru = ru_word

        # Create blanked sentence
        blanked = matching_he.replace(he_word, "___", 1)

        exercises.append({
            "sentence_he": matching_he,
            "sentence_he_blanked": blanked,
            "sentence_ru": matching_ru or ru_word,
            "hint": ru_word,
            "answer": he_word,
            "transliteration": translit,
        })

    random.shuffle(exercises)
    return exercises[:count]
