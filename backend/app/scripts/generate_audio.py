"""Pre-generate TTS audio for all Hebrew content.

Warms the edge-tts cache so users never experience first-time latency.
Uses the same cache mechanism as the /api/tts/speak endpoint.

Generates audio for:
  1. Words — hebrew field (~6,700 words)
  2. Example sentences — hebrew field (~8,000 sentences)
  3. Reading texts — content_he field (~250 texts, chunked if long)
  4. Dialogue lines — each speaker line from lines_json (~240 dialogues)

Usage:
  docker compose exec backend python -m app.scripts.generate_audio
  docker compose exec backend python -m app.scripts.generate_audio --only words
  docker compose exec backend python -m app.scripts.generate_audio --only sentences
  docker compose exec backend python -m app.scripts.generate_audio --only texts
  docker compose exec backend python -m app.scripts.generate_audio --only dialogues
  docker compose exec backend python -m app.scripts.generate_audio --dry-run
"""

import argparse
import asyncio
import hashlib
import sys
import time
from pathlib import Path

import edge_tts
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings

# ── Config ──────────────────────────────────────────────────────────────────

AUDIO_DIR = Path("/app/audio")
VOICE = "he-IL-AvriNeural"
RATE = "+0%"
MAX_CHUNK = 500  # edge-tts max comfortable length
BATCH_SIZE = 20  # concurrent TTS requests per batch
RETRY_LIMIT = 3
RETRY_DELAY = 2.0  # seconds


# ── Cache helpers (same logic as services/tts.py) ──────────────────────────

def _cache_key(txt: str) -> str:
    raw = f"{VOICE}:{RATE}:{txt}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _is_cached(txt: str) -> bool:
    return (AUDIO_DIR / f"{_cache_key(txt)}.mp3").exists()


async def _generate(txt: str) -> bool:
    """Generate TTS for a single text. Returns True if generated, False if cached."""
    txt = txt.strip()
    if not txt:
        return False

    key = _cache_key(txt)
    filepath = AUDIO_DIR / f"{key}.mp3"

    if filepath.exists():
        return False  # already cached

    for attempt in range(RETRY_LIMIT):
        try:
            comm = edge_tts.Communicate(txt, VOICE, rate=RATE)
            await comm.save(str(filepath))
            return True
        except Exception as e:
            if attempt < RETRY_LIMIT - 1:
                await asyncio.sleep(RETRY_DELAY * (attempt + 1))
            else:
                print(f"    FAIL after {RETRY_LIMIT} attempts: {txt[:60]}... — {e}")
                return False


def _chunk_text(text_content: str, max_len: int = MAX_CHUNK) -> list[str]:
    """Split long text into chunks at sentence boundaries."""
    if len(text_content) <= max_len:
        return [text_content]

    chunks = []
    current = ""
    # Split by sentences (period, question mark, exclamation)
    sentences = []
    buf = ""
    for ch in text_content:
        buf += ch
        if ch in ".?!。":
            sentences.append(buf.strip())
            buf = ""
    if buf.strip():
        sentences.append(buf.strip())

    for sent in sentences:
        if len(current) + len(sent) + 1 <= max_len:
            current = f"{current} {sent}".strip() if current else sent
        else:
            if current:
                chunks.append(current)
            # If a single sentence > max_len, split by words
            if len(sent) > max_len:
                words = sent.split()
                part = ""
                for w in words:
                    if len(part) + len(w) + 1 <= max_len:
                        part = f"{part} {w}".strip() if part else w
                    else:
                        if part:
                            chunks.append(part)
                        part = w
                if part:
                    chunks.append(part)
                current = ""
            else:
                current = sent
    if current:
        chunks.append(current)
    return chunks


# ── Batch processor ─────────────────────────────────────────────────────────

async def _process_batch(texts: list[str], label: str, dry_run: bool = False) -> tuple[int, int, int]:
    """Process a list of texts. Returns (total, generated, cached)."""
    total = len(texts)
    cached = sum(1 for t in texts if _is_cached(t.strip()))
    to_generate = [t for t in texts if not _is_cached(t.strip())]
    generated = 0

    if dry_run:
        print(f"  {label}: {total} total, {cached} cached, {len(to_generate)} to generate")
        return total, 0, cached

    print(f"  {label}: {total} total, {cached} cached, {len(to_generate)} to generate")

    for i in range(0, len(to_generate), BATCH_SIZE):
        batch = to_generate[i:i + BATCH_SIZE]
        results = await asyncio.gather(*[_generate(t) for t in batch])
        generated += sum(1 for r in results if r)

        done = cached + generated + (len(to_generate) - i - len(batch))
        pct = int((i + len(batch)) / len(to_generate) * 100) if to_generate else 100
        print(f"    [{pct:3d}%] generated {generated}/{len(to_generate)}", end="\r")

        # Small delay between batches to avoid throttling
        if i + BATCH_SIZE < len(to_generate):
            await asyncio.sleep(0.5)

    print(f"    Done: {generated} new + {cached} cached = {generated + cached}/{total}")
    return total, generated, cached


# ── Main generators ─────────────────────────────────────────────────────────

async def generate_words(session: AsyncSession, dry_run: bool) -> tuple[int, int, int]:
    """Generate TTS for all words."""
    print("\n═══ WORDS ═══")
    rows = (await session.execute(text(
        "SELECT hebrew FROM words WHERE hebrew IS NOT NULL AND hebrew != '' ORDER BY id"
    ))).fetchall()
    texts = [r[0] for r in rows]
    return await _process_batch(texts, "Words", dry_run)


async def generate_sentences(session: AsyncSession, dry_run: bool) -> tuple[int, int, int]:
    """Generate TTS for all example sentences."""
    print("\n═══ EXAMPLE SENTENCES ═══")
    rows = (await session.execute(text(
        "SELECT hebrew FROM example_sentences WHERE hebrew IS NOT NULL AND hebrew != '' ORDER BY id"
    ))).fetchall()
    texts = [r[0] for r in rows]
    return await _process_batch(texts, "Sentences", dry_run)


async def generate_texts(session: AsyncSession, dry_run: bool) -> tuple[int, int, int]:
    """Generate TTS for all reading texts (chunked)."""
    print("\n═══ READING TEXTS ═══")
    rows = (await session.execute(text(
        "SELECT id, content_he FROM reading_texts WHERE content_he IS NOT NULL AND content_he != '' ORDER BY id"
    ))).fetchall()

    all_chunks = []
    for row in rows:
        chunks = _chunk_text(row[1])
        all_chunks.extend(chunks)

    print(f"  {len(rows)} texts → {len(all_chunks)} chunks (avg {len(all_chunks) / max(len(rows), 1):.1f} per text)")
    return await _process_batch(all_chunks, "Text chunks", dry_run)


async def generate_dialogues(session: AsyncSession, dry_run: bool) -> tuple[int, int, int]:
    """Generate TTS for all dialogue lines."""
    print("\n═══ DIALOGUE LINES ═══")
    rows = (await session.execute(text(
        "SELECT id, lines_json FROM dialogues WHERE lines_json IS NOT NULL ORDER BY id"
    ))).fetchall()

    import json
    all_lines = []
    for row in rows:
        lines = row[1] if isinstance(row[1], list) else json.loads(row[1])
        for line in lines:
            he_text = line.get("text_he", "").strip()
            if he_text:
                all_lines.append(he_text)

    print(f"  {len(rows)} dialogues → {len(all_lines)} Hebrew lines")
    return await _process_batch(all_lines, "Dialogue lines", dry_run)


# ── Entry point ─────────────────────────────────────────────────────────────

async def main():
    parser = argparse.ArgumentParser(description="Pre-generate TTS audio for all Hebrew content")
    parser.add_argument("--only", choices=["words", "sentences", "texts", "dialogues"],
                        help="Generate only for a specific content type")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show counts without generating audio")
    args = parser.parse_args()

    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    print(f"TTS Audio Generator")
    print(f"  Voice:     {VOICE}")
    print(f"  Audio dir: {AUDIO_DIR}")
    print(f"  Batch:     {BATCH_SIZE} concurrent")
    if args.dry_run:
        print(f"  Mode:      DRY RUN (no generation)")

    start = time.time()
    totals = {"total": 0, "generated": 0, "cached": 0}

    async with async_session_factory() as session:
        generators = {
            "words": generate_words,
            "sentences": generate_sentences,
            "texts": generate_texts,
            "dialogues": generate_dialogues,
        }

        if args.only:
            tasks = {args.only: generators[args.only]}
        else:
            tasks = generators

        for name, gen_func in tasks.items():
            t, g, c = await gen_func(session, args.dry_run)
            totals["total"] += t
            totals["generated"] += g
            totals["cached"] += c

    elapsed = time.time() - start

    print(f"\n{'=' * 50}")
    print(f"SUMMARY")
    print(f"  Total items:  {totals['total']}")
    print(f"  Generated:    {totals['generated']}")
    print(f"  Already cached: {totals['cached']}")
    print(f"  Time:         {elapsed:.1f}s")
    if totals["generated"] > 0:
        print(f"  Avg speed:    {totals['generated'] / elapsed:.1f} items/sec")
    print(f"{'=' * 50}")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
