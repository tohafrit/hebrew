#!/usr/bin/env python3
"""Curate vocabulary for levels 4-6 by assigning frequency_rank.

Levels 1-3 typically have curated words with frequency_rank set.
Levels 4-6 have bulk-imported words, many with NULL frequency_rank.

This script assigns frequency_rank based on heuristics:
- Words that appear in example sentences → more frequent (rank 1-2)
- Words with root families (related to common roots) → medium (rank 2-3)
- Words with conjugation entries → used enough to conjugate (rank 2)
- Remaining words → rank 3-4

Operates directly on the SQL seed files.

Usage:
    python3 scripts/curate_vocabulary.py
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

SEED_DIR = Path(__file__).parent.parent / "data" / "seed"
WORDS_FILE = SEED_DIR / "words.sql"


def parse_words_sql(filepath: Path) -> list[dict]:
    """Parse words SQL file into dicts."""
    rows = []
    for line in filepath.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("INSERT INTO public.words"):
            continue
        # Extract id, level_id, frequency_rank from the INSERT
        # Format: INSERT INTO public.words (id, hebrew, nikkud, transliteration, translation_ru, pos, gender, number, root, frequency_rank, level_id, audio_url, image_url) VALUES (...)
        m = re.search(r"VALUES \((\d+), '([^']*)', (?:'[^']*'|NULL), (?:'[^']*'|NULL), (?:'[^']*'|NULL), (?:'([^']*)'|NULL), (?:'[^']*'|NULL), (?:'[^']*'|NULL), (?:'([^']*)'|NULL), (?:(\d+)|NULL), (?:(\d+)|NULL)", line)
        if m:
            rows.append({
                "id": int(m.group(1)),
                "hebrew": m.group(2),
                "pos": m.group(3),
                "root": m.group(4),
                "frequency_rank": int(m.group(5)) if m.group(5) else None,
                "level_id": int(m.group(6)) if m.group(6) else None,
                "raw_line": line,
            })
    return rows


def get_words_with_examples(seed_dir: Path) -> set[int]:
    """Get word IDs that have example sentences."""
    filepath = seed_dir / "example_sentences.sql"
    if not filepath.exists():
        return set()
    word_ids = set()
    for line in filepath.read_text(encoding="utf-8").splitlines():
        m = re.search(r"VALUES \(\d+, (\d+),", line)
        if m:
            word_ids.add(int(m.group(1)))
    return word_ids


def get_words_with_conjugations(seed_dir: Path) -> set[int]:
    """Get word IDs that have conjugation entries."""
    filepath = seed_dir / "verb_conjugations.sql"
    if not filepath.exists():
        return set()
    word_ids = set()
    for line in filepath.read_text(encoding="utf-8").splitlines():
        m = re.search(r"VALUES \(\d+, (\d+),", line)
        if m:
            word_ids.add(int(m.group(1)))
    return word_ids


def get_roots_with_families(seed_dir: Path) -> set[str]:
    """Get roots that have root families."""
    filepath = seed_dir / "root_families.sql"
    if not filepath.exists():
        return set()
    roots = set()
    for line in filepath.read_text(encoding="utf-8").splitlines():
        m = re.search(r"VALUES \(\d+, '([^']*)'", line)
        if m:
            roots.add(m.group(1))
    return roots


def main():
    if not WORDS_FILE.exists():
        print(f"ERROR: {WORDS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    print("Loading data...")
    words = parse_words_sql(WORDS_FILE)
    print(f"  Total words: {len(words)}")

    words_with_examples = get_words_with_examples(SEED_DIR)
    words_with_conjugations = get_words_with_conjugations(SEED_DIR)
    roots_with_families = get_roots_with_families(SEED_DIR)

    print(f"  Words with examples: {len(words_with_examples)}")
    print(f"  Words with conjugations: {len(words_with_conjugations)}")
    print(f"  Roots in families: {len(roots_with_families)}")

    # Count words by level that need frequency assignment
    needs_freq = [w for w in words if w["level_id"] and w["level_id"] >= 4 and w["frequency_rank"] is None]
    print(f"\n  Words in levels 4-6 without frequency_rank: {len(needs_freq)}")

    if not needs_freq:
        print("  Nothing to curate!")
        return

    # Assign frequency_rank
    assignments = {1: 0, 2: 0, 3: 0, 4: 0}
    for w in needs_freq:
        has_example = w["id"] in words_with_examples
        has_conj = w["id"] in words_with_conjugations
        has_root_family = w["root"] and w["root"] in roots_with_families

        if has_example and (has_conj or has_root_family):
            rank = 1  # High frequency indicator
        elif has_example or has_conj:
            rank = 2  # Medium-high
        elif has_root_family:
            rank = 3  # Medium — related to common roots
        else:
            rank = 4  # Rare — no contextual indicators

        w["new_rank"] = rank
        assignments[rank] += 1

    print(f"\n  Frequency assignments:")
    print(f"    Rank 1 (high):   {assignments[1]}")
    print(f"    Rank 2 (medium): {assignments[2]}")
    print(f"    Rank 3 (low):    {assignments[3]}")
    print(f"    Rank 4 (rare):   {assignments[4]}")

    # Build map of word_id → new_rank
    rank_map = {w["id"]: w["new_rank"] for w in needs_freq if "new_rank" in w}

    # Rewrite the words.sql file with updated frequency_rank
    content = WORDS_FILE.read_text(encoding="utf-8")
    updated = 0
    new_lines = []
    for line in content.splitlines(keepends=True):
        if line.strip().startswith("INSERT INTO public.words"):
            m = re.search(r"VALUES \((\d+),", line)
            if m:
                word_id = int(m.group(1))
                if word_id in rank_map:
                    rank = rank_map[word_id]
                    # Replace NULL frequency_rank with the assigned value
                    # Pattern: ..., root, NULL, level_id, ...
                    # We need to find the frequency_rank position (10th field)
                    line = re.sub(
                        r"(, (?:'[^']*'|NULL), (?:'[^']*'|NULL), (?:'[^']*'|NULL), (?:'[^']*'|NULL), (?:'[^']*'|NULL), )NULL(, (?:\d+|NULL))",
                        lambda m: f"{m.group(1)}{rank}{m.group(2)}",
                        line,
                        count=1,
                    )
                    updated += 1
        new_lines.append(line)

    WORDS_FILE.write_text("".join(new_lines), encoding="utf-8")
    print(f"\n  Updated {updated} rows in {WORDS_FILE}")


if __name__ == "__main__":
    main()
