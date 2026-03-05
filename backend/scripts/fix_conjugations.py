#!/usr/bin/env python3
"""Fix verb conjugation issues in the seed SQL file.

Problems fixed:
1. Sofit (final) Hebrew letters used in non-final positions (e.g., ך before תי)
2. Duplicate conjugation rows: when a word has both old broken + new corrected entries,
   keep only the newer (higher ID) entries which have nikkud.

Usage:
    python scripts/fix_conjugations.py
"""

import re
import sys
from collections import defaultdict
from pathlib import Path

SEED_FILE = Path(__file__).parent.parent / "data" / "seed" / "verb_conjugations.sql"

# Sofit → regular letter mapping
SOFIT_TO_REGULAR = {
    "\u05da": "\u05db",  # ך → כ
    "\u05dd": "\u05de",  # ם → מ
    "\u05df": "\u05e0",  # ן → נ
    "\u05e3": "\u05e4",  # ף → פ
    "\u05e5": "\u05e6",  # ץ → צ
}

# Regular → sofit mapping
REGULAR_TO_SOFIT = {v: k for k, v in SOFIT_TO_REGULAR.items()}

# Set of all sofit letters
SOFIT_LETTERS = set(SOFIT_TO_REGULAR.keys())

# Hebrew letter range
HEBREW_RANGE = set(chr(c) for c in range(0x05D0, 0x05EB))


def has_sofit_mid_word(text: str) -> bool:
    """Check if any sofit letter appears before another Hebrew letter."""
    for i, ch in enumerate(text[:-1]):  # skip last char
        if ch in SOFIT_LETTERS:
            # Check if next char is a Hebrew letter or nikkud
            next_ch = text[i + 1]
            if next_ch in HEBREW_RANGE or ("\u0591" <= next_ch <= "\u05C7"):
                return True
    return False


def fix_sofit_in_text(text: str) -> str:
    """Fix sofit letters that appear in non-final positions."""
    if not text:
        return text

    chars = list(text)
    for i in range(len(chars) - 1):
        if chars[i] in SOFIT_LETTERS:
            # Next char is Hebrew letter or nikkud → should be regular form
            next_ch = chars[i + 1]
            if next_ch in HEBREW_RANGE or ("\u0591" <= next_ch <= "\u05C7"):
                chars[i] = SOFIT_TO_REGULAR[chars[i]]

    # Also ensure final Hebrew letter IS sofit if applicable
    for i in range(len(chars) - 1, -1, -1):
        if chars[i] in HEBREW_RANGE:
            if chars[i] in REGULAR_TO_SOFIT:
                chars[i] = REGULAR_TO_SOFIT[chars[i]]
            break

    return "".join(chars)


def parse_insert(line: str):
    """Parse a conjugation INSERT line into its values."""
    m = re.match(
        r"INSERT INTO public\.verb_conjugations "
        r"\(id, word_id, binyan_id, tense, person, gender, number, "
        r"form_he, form_nikkud, transliteration\) "
        r"VALUES \((\d+), (\d+), (\d+), '([^']*)', '([^']*)', "
        r"(?:'([^']*)'|NULL), '([^']*)', "
        r"'([^']*)', (?:'([^']*)'|NULL), (?:'([^']*)'|NULL)\);",
        line.strip(),
    )
    if not m:
        return None

    return {
        "id": int(m.group(1)),
        "word_id": int(m.group(2)),
        "binyan_id": int(m.group(3)),
        "tense": m.group(4),
        "person": m.group(5),
        "gender": m.group(6),  # may be None
        "number": m.group(7),
        "form_he": m.group(8),
        "form_nikkud": m.group(9),  # may be None
        "transliteration": m.group(10),  # may be None
        "raw": line.strip(),
    }


def rebuild_insert(row: dict) -> str:
    """Rebuild an INSERT statement from parsed values."""
    gender = f"'{row['gender']}'" if row["gender"] else "NULL"
    nikkud = f"'{row['form_nikkud']}'" if row["form_nikkud"] else "NULL"
    translit = f"'{row['transliteration']}'" if row["transliteration"] else "NULL"

    return (
        f"INSERT INTO public.verb_conjugations "
        f"(id, word_id, binyan_id, tense, person, gender, number, "
        f"form_he, form_nikkud, transliteration) VALUES "
        f"({row['id']}, {row['word_id']}, {row['binyan_id']}, "
        f"'{row['tense']}', '{row['person']}', {gender}, '{row['number']}', "
        f"'{row['form_he']}', {nikkud}, {translit});\n"
    )


def main():
    if not SEED_FILE.exists():
        print(f"ERROR: {SEED_FILE} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Reading {SEED_FILE}...")
    lines = SEED_FILE.read_text(encoding="utf-8").splitlines(keepends=True)
    print(f"  Total lines: {len(lines)}")

    # Parse all rows
    rows = []
    unparsed = []
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped or not line_stripped.startswith("INSERT"):
            unparsed.append(line)
            continue
        parsed = parse_insert(line_stripped)
        if parsed:
            rows.append(parsed)
        else:
            unparsed.append(line)

    print(f"  Parsed rows: {len(rows)}")
    print(f"  Unparsed lines: {len(unparsed)}")

    # Step 1: Fix sofit letters mid-word
    sofit_fixes = 0
    for row in rows:
        if has_sofit_mid_word(row["form_he"]):
            row["form_he"] = fix_sofit_in_text(row["form_he"])
            sofit_fixes += 1
        if row["form_nikkud"] and has_sofit_mid_word(row["form_nikkud"]):
            row["form_nikkud"] = fix_sofit_in_text(row["form_nikkud"])

    print(f"\n  Sofit fixes applied: {sofit_fixes}")

    # Step 2: Remove duplicates — for each (word_id, binyan_id, tense, person, number),
    # if there are multiple rows, keep the one with highest ID (newer = corrected)
    key_groups = defaultdict(list)
    for row in rows:
        key = (row["word_id"], row["binyan_id"], row["tense"], row["person"], row["number"])
        key_groups[key].append(row)

    deduped_rows = []
    duplicates_removed = 0
    for key, group in key_groups.items():
        if len(group) == 1:
            deduped_rows.append(group[0])
        else:
            # Keep the one with highest ID (most recent / corrected)
            best = max(group, key=lambda r: r["id"])
            deduped_rows.append(best)
            duplicates_removed += len(group) - 1

    print(f"  Duplicates removed: {duplicates_removed}")

    # Sort by ID for clean output
    deduped_rows.sort(key=lambda r: r["id"])

    # Write output
    output_lines = []
    for line in unparsed:
        if line.strip():
            output_lines.append(line)
    for row in deduped_rows:
        output_lines.append(rebuild_insert(row))

    SEED_FILE.write_text("".join(output_lines), encoding="utf-8")
    print(f"\n  Output rows: {len(deduped_rows)}")
    print(f"  Written to: {SEED_FILE}")


if __name__ == "__main__":
    main()
