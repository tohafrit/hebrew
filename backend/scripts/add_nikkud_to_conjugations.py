#!/usr/bin/env python3
"""Add nikkud to verb conjugation forms using Dicta Nakdan API (batch mode).

Sends unique forms in batches, then bulk-updates the DB.

Usage:
    docker compose exec -T backend python scripts/add_nikkud_to_conjugations.py
"""
import asyncio
import sys
import time

import requests
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

sys.path.insert(0, ".")
from app.database import async_session
from app.models.grammar import VerbConjugation

NAKDAN_URL = "https://nakdan-2-0.loadbalancer.dicta.org.il/api"
BATCH_SIZE = 80  # words per API call
DELAY = 0.3


def call_nakdan(words: list[str]) -> dict[str, str]:
    """Send space-separated words, parse per-token nikkud from response."""
    text = " ".join(words)
    payload = {"task": "nakdan", "data": text, "genre": "modern", "addmorph": False}
    try:
        resp = requests.post(NAKDAN_URL, json=payload, timeout=30)
        resp.raise_for_status()
        items = resp.json()
    except Exception as e:
        print(f"    API error: {e}")
        return {}

    if not isinstance(items, list):
        return {}

    mapping: dict[str, str] = {}
    for item in items:
        word = item.get("word", "").strip()
        options = item.get("options", [])
        if word and options:
            nikkud = options[0]
            if nikkud != word:
                mapping[word] = nikkud
    return mapping


async def main():
    async with async_session() as db:
        # Get all unique forms without nikkud
        rows = (await db.execute(
            select(VerbConjugation.form_he)
            .where(VerbConjugation.form_nikkud.is_(None))
            .distinct()
        )).all()
        unique_forms = [r[0] for r in rows]
        print(f"Unique forms without nikkud: {len(unique_forms)}")

        if not unique_forms:
            print("Nothing to do.")
            return

        # Call API in batches
        all_nikkud: dict[str, str] = {}
        total_batches = (len(unique_forms) + BATCH_SIZE - 1) // BATCH_SIZE

        for i in range(0, len(unique_forms), BATCH_SIZE):
            batch = unique_forms[i:i + BATCH_SIZE]
            batch_num = i // BATCH_SIZE + 1
            result = call_nakdan(batch)
            all_nikkud.update(result)
            print(f"  Batch {batch_num}/{total_batches}: got {len(result)} nikkud ({len(all_nikkud)} total)")
            time.sleep(DELAY)

        print(f"\nNikkud obtained for {len(all_nikkud)}/{len(unique_forms)} unique forms")

        # Bulk update DB
        updated = 0
        for form_he, nikkud in all_nikkud.items():
            result = await db.execute(
                update(VerbConjugation)
                .where(VerbConjugation.form_he == form_he, VerbConjugation.form_nikkud.is_(None))
                .values(form_nikkud=nikkud)
            )
            updated += result.rowcount

        await db.commit()
        print(f"Updated {updated} conjugation rows with nikkud.")

        # Final stats
        total = await db.scalar(select(func.count()).select_from(VerbConjugation))
        nk = await db.scalar(select(func.count()).where(VerbConjugation.form_nikkud.isnot(None)).select_from(VerbConjugation))
        print(f"Final: {nk}/{total} ({nk * 100 // total}%) have nikkud")


if __name__ == "__main__":
    asyncio.run(main())
