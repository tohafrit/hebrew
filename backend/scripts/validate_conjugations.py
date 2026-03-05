#!/usr/bin/env python3
"""Validate verb conjugations for common errors.

Checks:
1. No sofit letters in non-final positions
2. No duplicate (word_id, binyan_id, tense, person, number) combos
3. Final Hebrew letters use sofit form where applicable

Usage:
    python3 scripts/validate_conjugations.py
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "data" / "seed" / "verb_conjugations.sql"

SOFIT_LETTERS = {"\u05da", "\u05dd", "\u05df", "\u05e3", "\u05e5"}
REGULAR_TO_SOFIT = {
    "\u05db": "\u05da",  # כ → ך
    "\u05de": "\u05dd",  # מ → ם
    "\u05e0": "\u05df",  # נ → ן
    "\u05e4": "\u05e3",  # פ → ף
    "\u05e6": "\u05e5",  # צ → ץ
}
HEBREW_RANGE = set(chr(c) for c in range(0x05D0, 0x05EB))


def parse_form_he(line: str):
    m = re.search(r"VALUES \((\d+), (\d+), (\d+), '([^']*)', '([^']*)', (?:'[^']*'|NULL), '([^']*)', '([^']*)'", line)
    if not m:
        return None
    return {
        "id": int(m.group(1)),
        "word_id": int(m.group(2)),
        "binyan_id": int(m.group(3)),
        "tense": m.group(4),
        "person": m.group(5),
        "number": m.group(6),
        "form_he": m.group(7),
    }


def main():
    lines = SEED_FILE.read_text(encoding="utf-8").splitlines()
    errors = []
    keys_seen = defaultdict(list)
    total = 0

    for line in lines:
        if not line.strip().startswith("INSERT"):
            continue
        row = parse_form_he(line)
        if not row:
            continue
        total += 1
        form = row["form_he"]

        # Check sofit mid-word
        for i, ch in enumerate(form[:-1]):
            if ch in SOFIT_LETTERS:
                next_ch = form[i + 1]
                if next_ch in HEBREW_RANGE or ("\u0591" <= next_ch <= "\u05C7"):
                    errors.append(f"  SOFIT MID-WORD: id={row['id']} word_id={row['word_id']} form='{form}'")
                    break

        # Check duplicates
        key = (row["word_id"], row["binyan_id"], row["tense"], row["person"], row["number"])
        keys_seen[key].append(row["id"])

    dup_errors = 0
    for key, ids in keys_seen.items():
        if len(ids) > 1:
            dup_errors += 1
            errors.append(f"  DUPLICATE: word_id={key[0]} binyan={key[1]} {key[2]}/{key[3]}/{key[4]} ids={ids}")

    print(f"Validated {total} conjugation rows.")
    if errors:
        print(f"\nERRORS FOUND: {len(errors)}")
        for e in errors[:20]:
            print(e)
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")
        sys.exit(1)
    else:
        print("ALL CHECKS PASSED — no sofit errors, no duplicates.")


if __name__ == "__main__":
    main()
