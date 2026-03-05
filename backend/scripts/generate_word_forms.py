#!/usr/bin/env python3
"""Generate systematic word forms for nouns and adjectives.

Rules:
- Masculine nouns: +ים plural
- Feminine nouns ending in ה: replace ה with ות
- Feminine nouns ending in ת: +ות
- Adjectives: all 4 forms (ms base, fs +ה, mp +ים, fp +ות)
- Construct state (smichut): ms drop final ה, mp ים→י, fp ות→ות (same)

Appends new forms to word_forms.sql, skipping words that already have forms.

Usage:
    python3 scripts/generate_word_forms.py
"""

import re
import sys
from pathlib import Path

SEED_DIR = Path(__file__).parent.parent / "data" / "seed"
WORDS_FILE = SEED_DIR / "words.sql"
FORMS_FILE = SEED_DIR / "word_forms.sql"

# Sofit letters
SOFIT_MAP = {
    "\u05db": "\u05da",  # כ → ך
    "\u05de": "\u05dd",  # מ → ם
    "\u05e0": "\u05df",  # נ → ן
    "\u05e4": "\u05e3",  # פ → ף
    "\u05e6": "\u05e5",  # צ → ץ
}
REGULAR_FROM_SOFIT = {v: k for k, v in SOFIT_MAP.items()}


def desofit(ch: str) -> str:
    """Convert a sofit letter to its regular form."""
    return REGULAR_FROM_SOFIT.get(ch, ch)


def sofit(ch: str) -> str:
    """Convert a regular letter to its sofit form if applicable."""
    return SOFIT_MAP.get(ch, ch)


def make_sofit_final(word: str) -> str:
    """Ensure the last Hebrew letter is sofit if applicable."""
    if not word:
        return word
    chars = list(word)
    for i in range(len(chars) - 1, -1, -1):
        if "\u05D0" <= chars[i] <= "\u05EA":
            chars[i] = sofit(chars[i])
            break
    return "".join(chars)


def strip_final_sofit(word: str) -> str:
    """Convert final sofit letter to regular form (for suffix addition)."""
    if not word:
        return word
    chars = list(word)
    for i in range(len(chars) - 1, -1, -1):
        if "\u05D0" <= chars[i] <= "\u05EA":
            chars[i] = desofit(chars[i])
            break
    return "".join(chars)


def generate_noun_forms(hebrew: str, gender: str | None) -> list[tuple[str, str]]:
    """Generate plural forms for a noun. Returns [(form_type, form_he)]."""
    forms = []

    if gender == "m":
        # Masculine plural: +ים
        base = strip_final_sofit(hebrew)
        plural = base + "\u05d9\u05dd"  # ים
        forms.append(("mp", plural))

        # Construct singular: if ends in ה, drop it
        if hebrew.endswith("\u05d4"):  # ה
            forms.append(("cs", hebrew[:-1]))
        # Construct plural: ים → י
        forms.append(("cp", base + "\u05d9"))  # י

    elif gender == "f":
        # Feminine plural
        if hebrew.endswith("\u05d4"):  # ends in ה
            # Replace ה with ות
            plural = hebrew[:-1] + "\u05d5\u05ea"  # ות
            forms.append(("fp", plural))
            # Construct singular: drop ה, add ת
            forms.append(("cs", hebrew[:-1] + "\u05ea"))  # ת
        elif hebrew.endswith("\u05ea"):  # ends in ת
            plural = hebrew + "\u05d5\u05ea"  # +ות
            forms.append(("fp", plural))
        else:
            # Irregular — try +ות
            base = strip_final_sofit(hebrew)
            plural = base + "\u05d5\u05ea"  # ות
            forms.append(("fp", plural))

        # Construct plural is same as absolute plural for feminine
        # (ות stays ות in construct)

    return forms


def generate_adj_forms(hebrew: str) -> list[tuple[str, str]]:
    """Generate all 4 adjective forms from masculine singular base."""
    forms = []
    base = strip_final_sofit(hebrew)

    # fs: +ה
    fs = base + "\u05d4"  # ה
    forms.append(("fs", fs))

    # mp: +ים
    mp = base + "\u05d9\u05dd"  # ים
    forms.append(("mp", mp))

    # fp: +ות
    fp = base + "\u05d5\u05ea"  # ות
    forms.append(("fp", fp))

    return forms


def parse_words(filepath: Path) -> list[dict]:
    """Parse words from SQL."""
    words = []
    for line in filepath.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("INSERT INTO public.words"):
            continue
        m = re.search(
            r"VALUES \((\d+), '([^']*)', (?:'[^']*'|NULL), (?:'[^']*'|NULL), "
            r"(?:'[^']*'|NULL), (?:'([^']*)'|NULL), (?:'([^']*)'|NULL)",
            line,
        )
        if m:
            words.append({
                "id": int(m.group(1)),
                "hebrew": m.group(2),
                "pos": m.group(3),
                "gender": m.group(4),
            })
    return words


def get_existing_form_word_ids(filepath: Path) -> set[int]:
    """Get word IDs that already have forms."""
    if not filepath.exists():
        return set()
    ids = set()
    for line in filepath.read_text(encoding="utf-8").splitlines():
        m = re.search(r"VALUES \(\d+, (\d+),", line)
        if m:
            ids.add(int(m.group(1)))
    return ids


def get_max_form_id(filepath: Path) -> int:
    """Get the maximum form ID from existing data."""
    if not filepath.exists():
        return 0
    max_id = 0
    for line in filepath.read_text(encoding="utf-8").splitlines():
        m = re.search(r"VALUES \((\d+),", line)
        if m:
            max_id = max(max_id, int(m.group(1)))
    return max_id


def main():
    if not WORDS_FILE.exists():
        print(f"ERROR: {WORDS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    print("Loading words...")
    words = parse_words(WORDS_FILE)
    existing_ids = get_existing_form_word_ids(FORMS_FILE)
    max_id = get_max_form_id(FORMS_FILE)
    print(f"  Total words: {len(words)}")
    print(f"  Words with existing forms: {len(existing_ids)}")
    print(f"  Max form ID: {max_id}")

    # Filter to nouns and adjectives without existing forms
    nouns = [w for w in words if w["pos"] == "noun" and w["id"] not in existing_ids]
    adjs = [w for w in words if w["pos"] == "adj" and w["id"] not in existing_ids]
    print(f"  Nouns without forms: {len(nouns)}")
    print(f"  Adjectives without forms: {len(adjs)}")

    # Generate forms
    new_forms = []
    next_id = max_id + 1

    for word in nouns:
        generated = generate_noun_forms(word["hebrew"], word["gender"])
        for form_type, form_he in generated:
            form_he = make_sofit_final(form_he)
            new_forms.append((next_id, word["id"], form_type, form_he))
            next_id += 1

    for word in adjs:
        generated = generate_adj_forms(word["hebrew"])
        for form_type, form_he in generated:
            form_he = make_sofit_final(form_he)
            new_forms.append((next_id, word["id"], form_type, form_he))
            next_id += 1

    print(f"\n  Generated {len(new_forms)} new forms")

    # Append to SQL file
    with open(FORMS_FILE, "a", encoding="utf-8") as f:
        for fid, word_id, form_type, form_he in new_forms:
            f.write(
                f"INSERT INTO public.word_forms "
                f"(id, word_id, form_type, hebrew, nikkud, transliteration, description) "
                f"VALUES ({fid}, {word_id}, '{form_type}', '{form_he}', NULL, NULL, NULL);\n"
            )

    total = len(existing_ids) + len(set(w["id"] for w in nouns + adjs))
    print(f"  Words with forms now: {total}")
    print(f"  Written to: {FORMS_FILE}")


if __name__ == "__main__":
    main()
