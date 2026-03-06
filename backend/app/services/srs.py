"""SM-2 spaced repetition engine."""

import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.srs import SRSCard, SRSReview, SRSSchedule
from app.models.sentence import ExampleSentence
from app.models.grammar import VerbConjugation, Binyan
from app.models.user import User
from app.models.word import Word


def sm2_update(
    quality: int,
    repetitions: int,
    ease_factor: float,
    interval_days: float,
    lapses: int,
) -> tuple[float, float, int, int]:
    """Apply SM-2 algorithm.

    Returns (new_interval, new_ease, new_reps, new_lapses).
    """
    if quality >= 2:  # correct — 2 ("remember") and 3 ("easy") advance the card
        if repetitions == 0:
            new_interval = 1.0
        elif repetitions == 1:
            new_interval = 6.0
        else:
            new_interval = round(interval_days * ease_factor)
        new_reps = repetitions + 1
        new_lapses = lapses
        # Only update ease factor on correct answers (SM-2 spec)
        new_ease = max(
            1.3,
            ease_factor + 0.1 - (3 - quality) * (0.08 + (3 - quality) * 0.02),
        )
    else:  # incorrect
        new_interval = 1.0
        new_reps = 0
        new_lapses = lapses + 1
        # Preserve ease factor on incorrect answers to avoid death spiral
        new_ease = ease_factor

    return new_interval, new_ease, new_reps, new_lapses


async def create_cards_for_words(
    db: AsyncSession,
    user_id: uuid.UUID,
    word_ids: list[int],
    card_types: list[str],
) -> int:
    """Create SRS cards for given words. Skip duplicates."""
    now = datetime.now(timezone.utc)

    # Batch-fetch all words at once
    words_result = await db.execute(
        select(Word).where(Word.id.in_(word_ids))
    )
    words_map = {w.id: w for w in words_result.scalars().all()}

    # Batch-check existing cards
    existing_result = await db.execute(
        select(SRSCard.content_id, SRSCard.card_type, SRSCard.front_json).where(
            SRSCard.user_id == user_id,
            SRSCard.content_id.in_(word_ids),
            SRSCard.card_type.in_(card_types),
        )
    )
    # For word cards: (content_id, card_type) is unique
    # For sentence cards: include sentence text to allow multiple per word
    existing_set: set[tuple] = set()
    existing_sentence_set: set[tuple] = set()
    for row in existing_result:
        if row.card_type.startswith("sentence_"):
            # Key by (content_id, card_type, hebrew_text) for per-sentence dedup
            hebrew = (row.front_json or {}).get("hebrew") or (row.front_json or {}).get("translation") or ""
            existing_sentence_set.add((row.content_id, row.card_type, hebrew))
        else:
            existing_set.add((row.content_id, row.card_type))

    # Pre-fetch example sentences for sentence card types
    sentence_types = {"sentence_he_ru", "sentence_ru_he"}
    need_sentences = bool(sentence_types & set(card_types))
    sentences_by_word: dict[int, list[ExampleSentence]] = {}
    if need_sentences:
        sent_result = await db.execute(
            select(ExampleSentence).where(ExampleSentence.word_id.in_(word_ids))
        )
        for sent in sent_result.scalars().all():
            sentences_by_word.setdefault(sent.word_id, []).append(sent)

    created = 0
    for word_id in word_ids:
        word = words_map.get(word_id)
        if not word:
            continue

        for card_type in card_types:
            if card_type in sentence_types:
                # Create one card per example sentence
                examples = sentences_by_word.get(word_id, [])
                for ex in examples:
                    # Per-sentence dedup: key includes the sentence text
                    dedup_text = ex.hebrew if card_type == "sentence_he_ru" else ex.translation_ru
                    if (word_id, card_type, dedup_text) in existing_sentence_set:
                        continue
                    if card_type == "sentence_he_ru":
                        front = {"hebrew": ex.hebrew, "type": "sentence"}
                        back = {"translation": ex.translation_ru, "source_word": word.hebrew}
                    else:  # sentence_ru_he
                        front = {"translation": ex.translation_ru, "hint_word": word.hebrew, "type": "sentence"}
                        back = {"hebrew": ex.hebrew}

                    card = SRSCard(
                        user_id=user_id,
                        card_type=card_type,
                        content_id=word_id,
                        front_json=front,
                        back_json=back,
                    )
                    db.add(card)
                    await db.flush()

                    schedule = SRSSchedule(
                        card_id=card.id,
                        next_review=now,
                        interval_days=1.0,
                        ease_factor=2.5,
                        repetitions=0,
                        lapses=0,
                    )
                    db.add(schedule)
                    created += 1
                continue

            if (word_id, card_type) in existing_set:
                continue

            level_label = {1: "Алеф", 2: "Бет", 3: "Гимель", 4: "Далет", 5: "Хей", 6: "Вав"}.get(word.level_id)

            if card_type == "word_he_ru":
                front = {"hebrew": word.hebrew, "nikkud": word.nikkud, "transliteration": word.transliteration}
                back = {"translation": word.translation_ru, "pos": word.pos, "root": word.root, "level": level_label}
            elif card_type == "word_ru_he":
                front = {"translation": word.translation_ru, "pos": word.pos}
                back = {"hebrew": word.hebrew, "nikkud": word.nikkud, "transliteration": word.transliteration, "root": word.root, "level": level_label}
            elif card_type == "cloze":
                front = {"hint": word.translation_ru, "pos": word.pos}
                back = {"hebrew": word.hebrew, "nikkud": word.nikkud, "transliteration": word.transliteration, "level": level_label}
            else:
                front = {"hebrew": word.hebrew, "nikkud": word.nikkud}
                back = {"translation": word.translation_ru, "level": level_label}

            card = SRSCard(
                user_id=user_id,
                card_type=card_type,
                content_id=word_id,
                front_json=front,
                back_json=back,
            )
            db.add(card)
            await db.flush()

            schedule = SRSSchedule(
                card_id=card.id,
                next_review=now,
                interval_days=1.0,
                ease_factor=2.5,
                repetitions=0,
                lapses=0,
            )
            db.add(schedule)
            created += 1

    await db.commit()
    return created


async def create_grammar_cards_for_words(
    db: AsyncSession,
    user_id: uuid.UUID,
    word_ids: list[int],
    tenses: list[str] | None = None,
) -> int:
    """Create SRS cards for verb conjugations. One card per conjugation row.

    Card types:
    - 'conjugation': front={verb, tense, person_label}, back={form_he, form_nikkud, transliteration}
    - 'binyan_id': front={form_he, tense}, back={binyan_name, verb, translation}
    """
    if tenses is None:
        tenses = ["present", "past"]
    now = datetime.now(timezone.utc)

    # Fetch conjugations for the given words + tenses
    conj_result = await db.execute(
        select(VerbConjugation, Word, Binyan)
        .join(Word, VerbConjugation.word_id == Word.id)
        .join(Binyan, VerbConjugation.binyan_id == Binyan.id)
        .where(
            VerbConjugation.word_id.in_(word_ids),
            VerbConjugation.tense.in_(tenses),
        )
        .order_by(VerbConjugation.word_id, VerbConjugation.tense, VerbConjugation.id)
    )
    all_conjs = conj_result.all()

    if not all_conjs:
        return 0

    # Sample up to 12 conjugations per verb (2 tenses x 6 persons)
    by_word: dict[int, list] = {}
    for conj, word, binyan in all_conjs:
        by_word.setdefault(conj.word_id, []).append((conj, word, binyan))

    sampled = []
    for wid, items in by_word.items():
        sampled.extend(items[:12])

    # Check existing cards to avoid duplicates (content_id = conjugation.id for grammar cards)
    conj_ids = [conj.id for conj, _, _ in sampled]
    existing_result = await db.execute(
        select(SRSCard.content_id, SRSCard.card_type).where(
            SRSCard.user_id == user_id,
            SRSCard.content_id.in_(conj_ids),
            SRSCard.card_type.in_(["conjugation", "binyan_id"]),
        )
    )
    existing_set = {(row.content_id, row.card_type) for row in existing_result}

    person_labels = {
        "1s": "я", "2ms": "ты (м)", "2fs": "ты (ж)",
        "3ms": "он", "3fs": "она", "1p": "мы",
        "2mp": "вы (м)", "2fp": "вы (ж)", "3mp": "они (м)", "3fp": "они (ж)",
        "ms": "м.р.", "fs": "ж.р.", "mp": "м.р. мн.", "fp": "ж.р. мн.",
    }
    tense_labels = {"past": "прошедшее", "present": "настоящее", "future": "будущее", "imperative": "повелительное"}

    created = 0
    for conj, word, binyan in sampled:
        # Conjugation card
        if (conj.id, "conjugation") not in existing_set:
            card = SRSCard(
                user_id=user_id,
                card_type="conjugation",
                content_id=conj.id,
                front_json={
                    "verb": word.hebrew,
                    "translation": word.translation_ru,
                    "tense": tense_labels.get(conj.tense, conj.tense),
                    "person_label": person_labels.get(conj.person, conj.person),
                },
                back_json={
                    "form_he": conj.form_he,
                    "form_nikkud": conj.form_nikkud,
                    "transliteration": conj.transliteration,
                },
            )
            db.add(card)
            await db.flush()
            db.add(SRSSchedule(
                card_id=card.id, next_review=now,
                interval_days=1.0, ease_factor=2.5, repetitions=0, lapses=0,
            ))
            created += 1

        # Binyan identification card
        if (conj.id, "binyan_id") not in existing_set:
            card = SRSCard(
                user_id=user_id,
                card_type="binyan_id",
                content_id=conj.id,
                front_json={
                    "form_he": conj.form_he,
                    "tense": tense_labels.get(conj.tense, conj.tense),
                },
                back_json={
                    "binyan_name": binyan.name_ru,
                    "verb": word.hebrew,
                    "translation": word.translation_ru,
                },
            )
            db.add(card)
            await db.flush()
            db.add(SRSSchedule(
                card_id=card.id, next_review=now,
                interval_days=1.0, ease_factor=2.5, repetitions=0, lapses=0,
            ))
            created += 1

    await db.commit()
    return created


async def get_session_cards(
    db: AsyncSession,
    user_id: uuid.UUID,
    limit: int = 20,
) -> tuple[list[dict], int, int]:
    """Get cards due for review. Returns (cards, total_due, new_count)."""
    now = datetime.now(timezone.utc)

    # Count total due
    total_due = await db.scalar(
        select(func.count())
        .select_from(SRSCard)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(
            SRSCard.user_id == user_id,
            SRSSchedule.next_review <= now,
        )
    ) or 0

    # Count new (never reviewed)
    new_count = await db.scalar(
        select(func.count())
        .select_from(SRSCard)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(
            SRSCard.user_id == user_id,
            SRSSchedule.repetitions == 0,
            SRSSchedule.next_review <= now,
        )
    ) or 0

    # Fetch due cards: prioritize overdue, then new
    query = (
        select(SRSCard, SRSSchedule)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(
            SRSCard.user_id == user_id,
            SRSSchedule.next_review <= now,
        )
        .order_by(SRSSchedule.next_review)
        .limit(limit)
    )
    result = await db.execute(query)
    rows = result.all()

    cards = []
    for card, schedule in rows:
        cards.append({
            "id": card.id,
            "card_type": card.card_type,
            "content_id": card.content_id,
            "front_json": card.front_json,
            "back_json": card.back_json,
            "next_review": schedule.next_review,
            "interval_days": schedule.interval_days,
            "ease_factor": schedule.ease_factor,
            "repetitions": schedule.repetitions,
            "lapses": schedule.lapses,
        })

    # Order cards so word cards come before their sentence cards (same content_id).
    # This ensures the user sees the word first, then its sentence for reinforcement.
    _type_order = {"word_he_ru": 0, "word_ru_he": 1, "cloze": 2, "sentence_he_ru": 3, "sentence_ru_he": 4}
    cards.sort(key=lambda c: (c["content_id"], _type_order.get(c["card_type"], 5)))

    return cards, total_due, new_count


async def review_card(
    db: AsyncSession,
    user_id: uuid.UUID,
    card_id: uuid.UUID,
    quality: int,
    response_time_ms: int | None = None,
) -> dict:
    """Submit a review for a card. Returns updated schedule."""
    # Verify card belongs to user
    card = await db.scalar(
        select(SRSCard).where(SRSCard.id == card_id, SRSCard.user_id == user_id)
    )
    if not card:
        raise ValueError("Card not found")

    schedule = await db.scalar(
        select(SRSSchedule).where(SRSSchedule.card_id == card_id)
    )
    if not schedule:
        raise ValueError("Schedule not found")

    # Record the review
    review = SRSReview(
        card_id=card_id,
        quality=quality,
        response_time_ms=response_time_ms,
    )
    db.add(review)

    # Apply SM-2
    new_interval, new_ease, new_reps, new_lapses = sm2_update(
        quality=quality,
        repetitions=schedule.repetitions,
        ease_factor=schedule.ease_factor,
        interval_days=schedule.interval_days,
        lapses=schedule.lapses,
    )

    schedule.interval_days = new_interval
    schedule.ease_factor = new_ease
    schedule.repetitions = new_reps
    schedule.lapses = new_lapses
    schedule.next_review = datetime.now(timezone.utc) + timedelta(days=new_interval)

    await db.flush()

    return {
        "card_id": card_id,
        "next_review": schedule.next_review,
        "interval_days": new_interval,
        "ease_factor": new_ease,
        "repetitions": new_reps,
    }


async def get_leech_cards(
    db: AsyncSession, user_id: uuid.UUID, threshold: int = 5
) -> list[dict]:
    """Get cards with lapses >= threshold (leech cards)."""
    query = (
        select(SRSCard, SRSSchedule)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(SRSCard.user_id == user_id, SRSSchedule.lapses >= threshold)
        .order_by(SRSSchedule.lapses.desc())
    )
    result = await db.execute(query)
    rows = result.all()

    cards = []
    for card, schedule in rows:
        cards.append({
            "id": card.id,
            "card_type": card.card_type,
            "content_id": card.content_id,
            "front_json": card.front_json,
            "back_json": card.back_json,
            "lapses": schedule.lapses,
            "ease_factor": schedule.ease_factor,
        })
    return cards


async def get_srs_stats(db: AsyncSession, user: User) -> dict:
    """Get SRS statistics for a user."""
    user_id = user.id
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    total = await db.scalar(
        select(func.count()).select_from(SRSCard).where(SRSCard.user_id == user_id)
    ) or 0

    due = await db.scalar(
        select(func.count())
        .select_from(SRSCard)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(SRSCard.user_id == user_id, SRSSchedule.next_review <= now)
    ) or 0

    new_cards = await db.scalar(
        select(func.count())
        .select_from(SRSCard)
        .join(SRSSchedule, SRSSchedule.card_id == SRSCard.id)
        .where(SRSCard.user_id == user_id, SRSSchedule.repetitions == 0)
    ) or 0

    reviews_today = await db.scalar(
        select(func.count())
        .select_from(SRSReview)
        .join(SRSCard, SRSCard.id == SRSReview.card_id)
        .where(SRSCard.user_id == user_id, SRSReview.reviewed_at >= today_start)
    ) or 0

    avg_ease = await db.scalar(
        select(func.avg(SRSSchedule.ease_factor))
        .select_from(SRSSchedule)
        .join(SRSCard, SRSCard.id == SRSSchedule.card_id)
        .where(SRSCard.user_id == user_id)
    )

    return {
        "total_cards": total,
        "due_today": due,
        "new_cards": new_cards,
        "reviews_today": reviews_today,
        "streak_days": user.streak_days,
        "average_ease": round(avg_ease, 2) if avg_ease else None,
    }
