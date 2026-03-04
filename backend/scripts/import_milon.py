"""Import words from milon (gregarkhipov/milon) Hebrew-English dictionary.

Downloads dict-he-en.json (33K entries) and he_50k.txt (frequency data),
deduplicates against existing words, and bulk-inserts new entries.

Usage:
    python scripts/import_milon.py [--dry-run]
"""
import argparse
import json
import os
import re
import sys
import urllib.request

# --- Config ---
DICT_URL = "https://raw.githubusercontent.com/gregarkhipov/milon/gh-pages/dict-he-en.json"
FREQ_URL = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/he/he_50k.txt"
DICT_PATH = "/tmp/dict-he-en.json"
FREQ_PATH = "/tmp/he_freq_50k.txt"

# Nikkud (vowel marks) regex
NIKKUD_RE = re.compile(r'[\u0591-\u05C7]')

# Hebrew POS tag → our POS tag
POS_MAP = {
    "שֵם ז'": "noun",
    "שֵם נ'": "noun",
    "שֵם": "noun",
    "שֵם ז\"ר": "noun",
    "שֵם נ\"ר": "noun",
    "שֵם ז\"ר (בצורת זוגי)": "noun",
    "שֵם נ\"ר (בצורת זוגי)": "noun",
    "שֵם זו\"נ": "noun",
    "שֵם זנ\"ר": "noun",
    "שֵם זנ\"ר (בצורת זוגי)": "noun",
    "שֵם כמות": "noun",
    "תואר": "adj",
    "תואר הפועל": "adv",
    "פ' קל": "verb",
    "פ' פיעל": "verb",
    "פ' פועל": "verb",
    "פ' הפעיל": "verb",
    "פ' התפעל": "verb",
    "פ' נפעל": "verb",
    "פ' הופעל": "verb",
    "פ' פיעל (פעלל)": "verb",
    "פ' פיעל (שפעל)": "verb",
    "פ' פועל (פועלל)": "verb",
    "פ' פועל (שופעל)": "verb",
    "פ' התפעל (השתפעל)": "verb",
    "פ' התפעל (התפעלל)": "verb",
    "מילת יחס": "prep",
    "מילת קישור": "conj",
    "מילת קריאה": "interj",
    "מילת שאלה": "pron",
    "מילת הסבר": "adv",
    "כינוי נפרד": "pron",
    "כינוי סתמי": "pron",
    "כינוי רומז לקרוב": "pron",
    "כינוי רומז לרחוק": "pron",
    "כינוי שאלה": "pron",
    "מספר מונה": "num",
    "מספר סודר": "num",
    "מספר מחלק": "num",
}

# Skip these POS types
POS_SKIP = {"תחילית", "סופית"}  # prefixes, suffixes


def strip_nikkud(s: str) -> str:
    return NIKKUD_RE.sub('', s).strip()


def download_if_missing(url: str, path: str):
    if not os.path.exists(path):
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, path)
    else:
        print(f"Using cached {path}")


def load_frequency(path: str) -> dict[str, int]:
    """Load frequency data: word → rank (1 = most common)."""
    freq = {}
    with open(path) as f:
        for rank, line in enumerate(f, 1):
            parts = line.strip().split()
            if len(parts) >= 1:
                word = parts[0]
                freq[word] = rank
    return freq


def freq_to_level(rank: int | None) -> int:
    """Map frequency rank to level_id (1-6)."""
    if rank is None:
        return 4  # unknown frequency → intermediate
    if rank <= 500:
        return 1
    if rank <= 2000:
        return 2
    if rank <= 5000:
        return 3
    if rank <= 15000:
        return 4
    if rank <= 30000:
        return 5
    return 6


def freq_to_rank(rank: int | None) -> int:
    """Map frequency rank to our frequency_rank (1-4)."""
    if rank is None:
        return 3
    if rank <= 2000:
        return 1
    if rank <= 10000:
        return 2
    if rank <= 30000:
        return 3
    return 4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Download data
    download_if_missing(DICT_URL, DICT_PATH)
    download_if_missing(FREQ_URL, FREQ_PATH)

    # Load frequency data
    freq = load_frequency(FREQ_PATH)
    print(f"Loaded {len(freq)} frequency entries")

    # Load dictionary
    with open(DICT_PATH) as f:
        entries = json.load(f)
    print(f"Loaded {len(entries)} dictionary entries")

    # Connect to DB
    import sqlalchemy as sa
    db_url = os.environ.get("DATABASE_URL", "postgresql://ulpan:change_me@localhost:5432/ulpan")
    engine = sa.create_engine(db_url)

    with engine.connect() as conn:
        # Get existing Hebrew words
        existing = set()
        rows = conn.execute(sa.text("SELECT hebrew FROM words"))
        for row in rows:
            existing.add(row[0])
        print(f"Existing words in DB: {len(existing)}")

        # Process entries
        to_insert = []
        skipped_exists = 0
        skipped_pos = 0
        skipped_empty = 0

        seen = set()  # track duplicates within the import

        for entry in entries:
            hebrew_nikkud = entry['translated'].strip()
            hebrew = strip_nikkud(hebrew_nikkud)

            # Skip empty or too short
            if not hebrew or len(hebrew) < 1:
                skipped_empty += 1
                continue

            # Skip phrases (contain spaces)
            if ' ' in hebrew and len(hebrew.split()) > 3:
                skipped_empty += 1
                continue

            # Skip if already exists in DB
            if hebrew in existing:
                skipped_exists += 1
                continue

            # Skip duplicates within import (keep first = often most common)
            if hebrew in seen:
                continue
            seen.add(hebrew)

            # Map POS
            pos_he = entry.get('part_of_speech', '').strip()
            if pos_he in POS_SKIP:
                skipped_pos += 1
                continue
            pos = POS_MAP.get(pos_he, None)
            if not pos and pos_he:
                # Try partial match for verb variants
                if pos_he.startswith("פ'"):
                    pos = "verb"
                else:
                    pos = None
            if not pos:
                pos = "noun"  # default for untagged

            # Build translation (English, semicolon-separated)
            translations = entry.get('translation', [])
            if not translations:
                skipped_empty += 1
                continue
            # Take first 3 translations, truncate
            translation = "; ".join(translations[:3])
            if len(translation) > 200:
                translation = translation[:197] + "..."

            # Frequency-based level
            rank = freq.get(hebrew)
            level_id = freq_to_level(rank)
            frequency_rank = freq_to_rank(rank)

            to_insert.append({
                "hebrew": hebrew,
                "translation_ru": translation,  # English for now
                "transliteration": None,
                "pos": pos,
                "root": None,
                "level_id": level_id,
                "frequency_rank": frequency_rank,
            })

        print(f"\nResults:")
        print(f"  To insert: {to_insert.__len__()}")
        print(f"  Skipped (exists): {skipped_exists}")
        print(f"  Skipped (POS): {skipped_pos}")
        print(f"  Skipped (empty): {skipped_empty}")

        # Show level distribution
        from collections import Counter
        level_dist = Counter(w['level_id'] for w in to_insert)
        print(f"\n  Level distribution:")
        for lvl in sorted(level_dist):
            print(f"    L{lvl}: {level_dist[lvl]}")

        if args.dry_run:
            print("\n  DRY RUN — no changes made")
            # Show sample
            print("\n  Sample entries:")
            for w in to_insert[:10]:
                print(f"    {w['hebrew']:15} ({w['pos']:5} L{w['level_id']}) {w['translation_ru'][:60]}")
            return

        # Bulk insert
        print(f"\n  Inserting {len(to_insert)} words...")
        words_table = sa.table(
            "words",
            sa.column("hebrew", sa.String),
            sa.column("translation_ru", sa.String),
            sa.column("transliteration", sa.String),
            sa.column("pos", sa.String),
            sa.column("root", sa.String),
            sa.column("level_id", sa.Integer),
            sa.column("frequency_rank", sa.Integer),
        )

        BATCH = 1000
        for i in range(0, len(to_insert), BATCH):
            batch = to_insert[i:i+BATCH]
            conn.execute(words_table.insert(), batch)
            conn.commit()
            print(f"    Inserted {min(i+BATCH, len(to_insert))}/{len(to_insert)}")

        print(f"\n  Done! Total words now: {len(existing) + len(to_insert)}")


if __name__ == "__main__":
    main()
