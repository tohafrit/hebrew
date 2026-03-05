"""Translate English translations to Russian using Google Translate.

Uses Google's free translate endpoint with batched texts via httpx.
Connects directly to PostgreSQL.

Usage:
    python scripts/translate_to_russian.py [--dry-run] [--limit N]
"""
import argparse
import json
import os
import sys
import time

import httpx
import psycopg2

DB_URL = os.environ.get(
    "SYNC_DATABASE_URL",
    "postgresql://ulpan:change_me@db:5432/ulpan",
)
MAX_BATCH_CHARS = 400  # Max combined text chars per batch

client = httpx.Client(timeout=15, headers={'User-Agent': 'Mozilla/5.0'})


def translate_batch(texts, src='en', tgt='ru'):
    """Translate texts using Google's free API with newline-separated text."""
    combined = '\n'.join(texts)
    resp = client.get(
        'https://translate.googleapis.com/translate_a/single',
        params={'client': 'gtx', 'sl': src, 'tl': tgt, 'dt': 't', 'q': combined},
    )
    resp.raise_for_status()
    data = resp.json()
    translated = ''.join(part[0] for part in data[0])
    return translated.split('\n')


def make_batches(rows, max_chars=MAX_BATCH_CHARS):
    """Split rows into batches that fit within char limits."""
    batches = []
    current_batch = []
    current_len = 0

    for row in rows:
        text_len = len(row[1]) + 1  # +1 for newline
        if current_len + text_len > max_chars and current_batch:
            batches.append(current_batch)
            current_batch = []
            current_len = 0
        current_batch.append(row)
        current_len += text_len

    if current_batch:
        batches.append(current_batch)
    return batches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True
    cur = conn.cursor()

    # Find words with English-only translations
    cur.execute("""
        SELECT id, translation_ru FROM words
        WHERE translation_ru ~ '[a-zA-Z]'
          AND NOT translation_ru ~ '[а-яА-ЯёЁ]'
        ORDER BY frequency_rank ASC NULLS LAST, id
    """)
    rows = cur.fetchall()

    total = len(rows)
    if args.limit > 0:
        rows = rows[:args.limit]
        total = len(rows)

    print(f"Words to translate: {total}", flush=True)

    if args.dry_run:
        for row in rows[:10]:
            print(f"  [{row[0]}] {row[1]}")
        return

    batches = make_batches(rows)
    print(f"Split into {len(batches)} batches", flush=True)

    updated = 0
    errors = 0
    mismatches = 0
    done = 0
    start_time = time.time()

    for batch_idx, batch in enumerate(batches):
        texts = [r[1] for r in batch]
        ids = [r[0] for r in batch]

        retries = 0
        while retries < 3:
            try:
                translated = translate_batch(texts)

                if len(translated) == len(ids):
                    for word_id, russian in zip(ids, translated):
                        if russian and russian.strip():
                            cur.execute(
                                "UPDATE words SET translation_ru = %s WHERE id = %s",
                                (russian.strip(), word_id),
                            )
                            updated += 1
                else:
                    mismatches += 1
                    # Mismatch — translate one by one
                    for word_id, text in zip(ids, texts):
                        try:
                            result = translate_batch([text])
                            if result and result[0].strip():
                                cur.execute(
                                    "UPDATE words SET translation_ru = %s WHERE id = %s",
                                    (result[0].strip(), word_id),
                                )
                                updated += 1
                        except Exception:
                            errors += 1
                break  # Success

            except Exception as e:
                retries += 1
                if retries >= 3:
                    print(f"  Batch {batch_idx} failed: {e}", flush=True)
                    errors += len(batch)
                else:
                    time.sleep(1 * retries)

        done += len(batch)
        if done % 1000 < len(batch) or done >= total:
            elapsed = time.time() - start_time
            rate = done / elapsed if elapsed > 0 else 0
            eta = (total - done) / rate if rate > 0 else 0
            print(f"  {done}/{total} ({rate:.0f} w/s, ETA {eta/60:.1f}m, "
                  f"ok: {updated}, err: {errors}, mismatch: {mismatches})", flush=True)

        time.sleep(0.2)

    elapsed = time.time() - start_time
    print(f"\nDone in {elapsed:.0f}s! Updated {updated}, errors: {errors}, "
          f"mismatches: {mismatches}", flush=True)
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
