"""Generate Hebrew verb conjugation data for migration.

Connects to DB, reads verbs needing conjugations, generates forms
using template-based rules for each binyan and root class.
"""

import re
import sys

# ─── Root extraction ─────────────────────────────────────────────────────────

def parse_root(root_str: str) -> list[str] | None:
    """Parse root string into list of root letters."""
    if not root_str:
        return None
    if '.' in root_str:
        parts = root_str.replace(' ', '').split('.')
        parts = [p for p in parts if p]
        if len(parts) >= 3:
            return parts[:3]
    letters = [ch for ch in root_str if ch not in ' .\t']
    if len(letters) >= 3:
        return letters[:3]
    return None


# ─── Root classification ─────────────────────────────────────────────────────

GUTTURALS = set('אהעח')

def classify_root(root: list[str]) -> str:
    p, e, l = root[0], root[1], root[2]
    if e == l:
        return 'ayin_ayin'
    if e in ('ו', 'י'):
        return 'hollow'
    if l == 'ה':
        return 'lamed_he'
    if l == 'א':
        return 'lamed_alef'
    if p == 'נ':
        return 'pe_nun'
    if p == 'י':
        return 'pe_yod'
    return 'regular'


# ─── Binyan identification ───────────────────────────────────────────────────

def identify_binyan(hebrew: str, root: list[str]) -> int:
    """Identify binyan from infinitive + root. Returns binyan_id 1-7."""
    # Hitpa'el: including sibilant metathesis forms
    # להת... (standard), להסת... (ס root), להצט... (צ root), להזד... (ז root)
    # להשת... (ש root: השתתף, השתמש), להזד... (ז root)
    if (hebrew.startswith('להת') or hebrew.startswith('להסת') or
            hebrew.startswith('להצט') or hebrew.startswith('להזד') or
            hebrew.startswith('להשת')):
        return 7  # Hitpa'el
    if hebrew.startswith('להי') or hebrew.startswith('להינ') or hebrew.startswith('להיפ'):
        return 2  # Nif'al
    if hebrew.startswith('לה') and not hebrew.startswith('להת') and not hebrew.startswith('להי'):
        return 5  # Hif'il
    # Pa'al vs Pi'el: check if infinitive has ו vowel letter not in root
    remaining = hebrew[1:]  # after ל
    root_str = ''.join(root)
    root_class = classify_root(root)

    # Pe-yod roots: infinitive drops the yod (לדעת not לידעת, לשבת not לישבת)
    # The remaining after ל starts with the SECOND root letter
    # Check root[0] directly since classify_root may return lamed_alef/lamed_he instead
    if root[0] == 'י' and len(remaining) >= 2 and remaining[0] == root[1]:
        return 1  # Pa'al pe-yod

    # Hollow roots (middle ו/י) are always Pa'al when they keep the weak letter
    if root_class == 'hollow':
        return 1  # Pa'al hollow

    if 'ו' in remaining and 'ו' not in root:
        return 1  # Pa'al (the ו is a mater lectionis)
    if len(remaining) == 3 and remaining == root_str:
        return 3  # Pi'el (ל + exact root: לדבר, לשחק)
    # Short forms (3-letter after ל) — could be Pi'el or Pa'al
    if len(remaining) == 3:
        return 3  # Pi'el (more common for this pattern)
    return 1  # Default Pa'al


# ─── Final form (sofit) handling ──────────────────────────────────────────────

SOFIT_MAP = {'כ': 'ך', 'מ': 'ם', 'נ': 'ן', 'פ': 'ף', 'צ': 'ץ'}

def apply_sofit(form: str) -> str:
    """Apply final letter forms (sofit) to Hebrew word."""
    if form and form[-1] in SOFIT_MAP:
        return form[:-1] + SOFIT_MAP[form[-1]]
    return form


def _row(word_id, binyan_id, tense, person, gender, number, form):
    return {
        "word_id": word_id, "binyan_id": binyan_id,
        "tense": tense, "person": person,
        "gender": gender, "number": number,
        "form_he": apply_sofit(form), "form_nikkud": None, "transliteration": None,
    }


# ─── Pa'al Regular ──────────────────────────────────────────────────────────

def conj_paal_regular(root, word_id):
    p, e, l = root
    R = lambda t, pe, g, n, f: _row(word_id, 1, t, pe, g, n, f)
    rows = []

    # Past: PaEaL-ti etc.
    rows += [
        R("past", "1s", "mf", "s", f"{p}{e}{l}תי"),
        R("past", "2ms", "m", "s", f"{p}{e}{l}ת"),
        R("past", "2fs", "f", "s", f"{p}{e}{l}ת"),
        R("past", "3ms", "m", "s", f"{p}{e}{l}"),
        R("past", "3fs", "f", "s", f"{p}{e}{l}ה"),
        R("past", "1p", "mf", "p", f"{p}{e}{l}נו"),
        R("past", "2mp", "m", "p", f"{p}{e}{l}תם"),
        R("past", "2fp", "f", "p", f"{p}{e}{l}תן"),
        R("past", "3p", "mf", "p", f"{p}{e}{l}ו"),
    ]
    # Present: KoTeV (with ו between P and E)
    rows += [
        R("present", "ms", "m", "s", f"{p}ו{e}{l}"),
        R("present", "fs", "f", "s", f"{p}ו{e}{l}ת"),
        R("present", "mp", "m", "p", f"{p}ו{e}{l}ים"),
        R("present", "fp", "f", "p", f"{p}ו{e}{l}ות"),
    ]
    # Future: yiPEoL (NO ו in unvoweled spelling for most)
    rows += [
        R("future", "1s", "mf", "s", f"א{p}{e}{l}"),
        R("future", "2ms", "m", "s", f"ת{p}{e}{l}"),
        R("future", "2fs", "f", "s", f"ת{p}{e}{l}י"),
        R("future", "3ms", "m", "s", f"י{p}{e}{l}"),
        R("future", "3fs", "f", "s", f"ת{p}{e}{l}"),
        R("future", "1p", "mf", "p", f"נ{p}{e}{l}"),
        R("future", "2mp", "m", "p", f"ת{p}{e}{l}ו"),
        R("future", "2fp", "f", "p", f"ת{p}{e}{l}נה"),
        R("future", "3mp", "m", "p", f"י{p}{e}{l}ו"),
        R("future", "3fp", "f", "p", f"ת{p}{e}{l}נה"),
    ]
    # Imperative
    rows += [
        R("imperative", "2ms", "m", "s", f"{p}{e}{l}"),
        R("imperative", "2fs", "f", "s", f"{p}{e}{l}י"),
        R("imperative", "2mp", "m", "p", f"{p}{e}{l}ו"),
        R("imperative", "2fp", "f", "p", f"{p}{e}{l}נה"),
    ]
    return rows


# ─── Pa'al Pe-Yod (initial י drops in future/imperative) ──────────────────

def conj_paal_pe_yod(root, word_id):
    """Pa'al for pe-yod roots (e.g., י.ד.ע → לדעת, י.ש.ב → לשבת)."""
    p, e, l = root  # p is always י
    R = lambda t, pe, g, n, f: _row(word_id, 1, t, pe, g, n, f)
    rows = []

    # Past: same as regular (yod retained: ידעתי, ישבתי)
    rows += [
        R("past", "1s", "mf", "s", f"{p}{e}{l}תי"),
        R("past", "2ms", "m", "s", f"{p}{e}{l}ת"),
        R("past", "2fs", "f", "s", f"{p}{e}{l}ת"),
        R("past", "3ms", "m", "s", f"{p}{e}{l}"),
        R("past", "3fs", "f", "s", f"{p}{e}{l}ה"),
        R("past", "1p", "mf", "p", f"{p}{e}{l}נו"),
        R("past", "2mp", "m", "p", f"{p}{e}{l}תם"),
        R("past", "2fp", "f", "p", f"{p}{e}{l}תן"),
        R("past", "3p", "mf", "p", f"{p}{e}{l}ו"),
    ]
    # Present: yoXeX pattern (יודע, יושב, יוצא, יורד)
    rows += [
        R("present", "ms", "m", "s", f"{p}ו{e}{l}"),
        R("present", "fs", "f", "s", f"{p}ו{e}{l}ת"),
        R("present", "mp", "m", "p", f"{p}ו{e}{l}ים"),
        R("present", "fp", "f", "p", f"{p}ו{e}{l}ות"),
    ]
    # Future: yod drops — prefix + EL (אדע, אשב, אצא, ארד)
    rows += [
        R("future", "1s", "mf", "s", f"א{e}{l}"),
        R("future", "2ms", "m", "s", f"ת{e}{l}"),
        R("future", "2fs", "f", "s", f"ת{e}{l}י"),
        R("future", "3ms", "m", "s", f"י{e}{l}"),
        R("future", "3fs", "f", "s", f"ת{e}{l}"),
        R("future", "1p", "mf", "p", f"נ{e}{l}"),
        R("future", "2mp", "m", "p", f"ת{e}{l}ו"),
        R("future", "2fp", "f", "p", f"ת{e}{l}נה"),
        R("future", "3mp", "m", "p", f"י{e}{l}ו"),
        R("future", "3fp", "f", "p", f"ת{e}{l}נה"),
    ]
    # Imperative: short stem (דע, שב, צא, רד)
    rows += [
        R("imperative", "2ms", "m", "s", f"{e}{l}"),
        R("imperative", "2fs", "f", "s", f"{e}{l}י"),
        R("imperative", "2mp", "m", "p", f"{e}{l}ו"),
        R("imperative", "2fp", "f", "p", f"{e}{l}נה"),
    ]
    return rows


# ─── Pa'al Hollow (middle ו/י) ─────────────────────────────────────────────

def conj_paal_hollow(root, word_id):
    p, v, l = root  # v is ו or י
    R = lambda t, pe, g, n, f: _row(word_id, 1, t, pe, g, n, f)
    rows = []

    # Past: short stem P-L (no middle letter)
    rows += [
        R("past", "1s", "mf", "s", f"{p}{l}תי"),
        R("past", "2ms", "m", "s", f"{p}{l}ת"),
        R("past", "2fs", "f", "s", f"{p}{l}ת"),
        R("past", "3ms", "m", "s", f"{p}{l}"),
        R("past", "3fs", "f", "s", f"{p}{l}ה"),
        R("past", "1p", "mf", "p", f"{p}{l}נו"),
        R("past", "2mp", "m", "p", f"{p}{l}תם"),
        R("past", "2fp", "f", "p", f"{p}{l}תן"),
        R("past", "3p", "mf", "p", f"{p}{l}ו"),
    ]
    # Present: short P-L
    rows += [
        R("present", "ms", "m", "s", f"{p}{l}"),
        R("present", "fs", "f", "s", f"{p}{l}ה"),
        R("present", "mp", "m", "p", f"{p}{l}ים"),
        R("present", "fp", "f", "p", f"{p}{l}ות"),
    ]
    # Future: with vowel letter (yaPVL → יגור, יבוא)
    rows += [
        R("future", "1s", "mf", "s", f"א{p}{v}{l}"),
        R("future", "2ms", "m", "s", f"ת{p}{v}{l}"),
        R("future", "2fs", "f", "s", f"ת{p}{v}{l}י"),
        R("future", "3ms", "m", "s", f"י{p}{v}{l}"),
        R("future", "3fs", "f", "s", f"ת{p}{v}{l}"),
        R("future", "1p", "mf", "p", f"נ{p}{v}{l}"),
        R("future", "2mp", "m", "p", f"ת{p}{v}{l}ו"),
        R("future", "2fp", "f", "p", f"ת{p}{v}{l}נה"),
        R("future", "3mp", "m", "p", f"י{p}{v}{l}ו"),
        R("future", "3fp", "f", "p", f"ת{p}{v}{l}נה"),
    ]
    # Imperative
    rows += [
        R("imperative", "2ms", "m", "s", f"{p}{v}{l}"),
        R("imperative", "2fs", "f", "s", f"{p}{v}{l}י"),
        R("imperative", "2mp", "m", "p", f"{p}{v}{l}ו"),
        R("imperative", "2fp", "f", "p", f"{p}{v}{l}נה"),
    ]
    return rows


# ─── Pa'al Lamed-He ─────────────────────────────────────────────────────────

def conj_paal_lamed_he(root, word_id):
    p, e = root[0], root[1]
    R = lambda t, pe, g, n, f: _row(word_id, 1, t, pe, g, n, f)
    rows = []

    # Past
    rows += [
        R("past", "1s", "mf", "s", f"{p}{e}יתי"),
        R("past", "2ms", "m", "s", f"{p}{e}ית"),
        R("past", "2fs", "f", "s", f"{p}{e}ית"),
        R("past", "3ms", "m", "s", f"{p}{e}ה"),
        R("past", "3fs", "f", "s", f"{p}{e}תה"),
        R("past", "1p", "mf", "p", f"{p}{e}ינו"),
        R("past", "2mp", "m", "p", f"{p}{e}יתם"),
        R("past", "2fp", "f", "p", f"{p}{e}יתן"),
        R("past", "3p", "mf", "p", f"{p}{e}ו"),
    ]
    # Present
    rows += [
        R("present", "ms", "m", "s", f"{p}ו{e}ה"),
        R("present", "fs", "f", "s", f"{p}ו{e}ה"),
        R("present", "mp", "m", "p", f"{p}ו{e}ים"),
        R("present", "fp", "f", "p", f"{p}ו{e}ות"),
    ]
    # Future
    rows += [
        R("future", "1s", "mf", "s", f"א{p}{e}ה"),
        R("future", "2ms", "m", "s", f"ת{p}{e}ה"),
        R("future", "2fs", "f", "s", f"ת{p}{e}י"),
        R("future", "3ms", "m", "s", f"י{p}{e}ה"),
        R("future", "3fs", "f", "s", f"ת{p}{e}ה"),
        R("future", "1p", "mf", "p", f"נ{p}{e}ה"),
        R("future", "2mp", "m", "p", f"ת{p}{e}ו"),
        R("future", "2fp", "f", "p", f"ת{p}{e}ינה"),
        R("future", "3mp", "m", "p", f"י{p}{e}ו"),
        R("future", "3fp", "f", "p", f"ת{p}{e}ינה"),
    ]
    # Imperative
    rows += [
        R("imperative", "2ms", "m", "s", f"{p}{e}ה"),
        R("imperative", "2fs", "f", "s", f"{p}{e}י"),
        R("imperative", "2mp", "m", "p", f"{p}{e}ו"),
        R("imperative", "2fp", "f", "p", f"{p}{e}ינה"),
    ]
    return rows


# ─── Pi'el Regular ──────────────────────────────────────────────────────────

def conj_piel_regular(root, word_id):
    p, e, l = root
    R = lambda t, pe, g, n, f: _row(word_id, 3, t, pe, g, n, f)
    rows = []

    # Past: XiXeX
    rows += [
        R("past", "1s", "mf", "s", f"{p}י{e}{l}תי"),
        R("past", "2ms", "m", "s", f"{p}י{e}{l}ת"),
        R("past", "2fs", "f", "s", f"{p}י{e}{l}ת"),
        R("past", "3ms", "m", "s", f"{p}י{e}{l}"),
        R("past", "3fs", "f", "s", f"{p}י{e}{l}ה"),
        R("past", "1p", "mf", "p", f"{p}י{e}{l}נו"),
        R("past", "2mp", "m", "p", f"{p}י{e}{l}תם"),
        R("past", "2fp", "f", "p", f"{p}י{e}{l}תן"),
        R("past", "3p", "mf", "p", f"{p}י{e}{l}ו"),
    ]
    # Present: meXaXeX
    rows += [
        R("present", "ms", "m", "s", f"מ{p}{e}{l}"),
        R("present", "fs", "f", "s", f"מ{p}{e}{l}ת"),
        R("present", "mp", "m", "p", f"מ{p}{e}{l}ים"),
        R("present", "fp", "f", "p", f"מ{p}{e}{l}ות"),
    ]
    # Future: aXaXeX
    rows += [
        R("future", "1s", "mf", "s", f"א{p}{e}{l}"),
        R("future", "2ms", "m", "s", f"ת{p}{e}{l}"),
        R("future", "2fs", "f", "s", f"ת{p}{e}{l}י"),
        R("future", "3ms", "m", "s", f"י{p}{e}{l}"),
        R("future", "3fs", "f", "s", f"ת{p}{e}{l}"),
        R("future", "1p", "mf", "p", f"נ{p}{e}{l}"),
        R("future", "2mp", "m", "p", f"ת{p}{e}{l}ו"),
        R("future", "2fp", "f", "p", f"ת{p}{e}{l}נה"),
        R("future", "3mp", "m", "p", f"י{p}{e}{l}ו"),
        R("future", "3fp", "f", "p", f"ת{p}{e}{l}נה"),
    ]
    # Imperative
    rows += [
        R("imperative", "2ms", "m", "s", f"{p}{e}{l}"),
        R("imperative", "2fs", "f", "s", f"{p}{e}{l}י"),
        R("imperative", "2mp", "m", "p", f"{p}{e}{l}ו"),
        R("imperative", "2fp", "f", "p", f"{p}{e}{l}נה"),
    ]
    return rows


# ─── Pi'el Lamed-He ─────────────────────────────────────────────────────────

def conj_piel_lamed_he(root, word_id):
    """Pi'el for lamed-he roots (e.g., צ.פ.ה → לצפות, ק.נ.ה → Pi'el)."""
    p, e = root[0], root[1]
    R = lambda t, pe, g, n, f: _row(word_id, 3, t, pe, g, n, f)
    rows = []

    # Past: XiXa
    rows += [
        R("past", "1s", "mf", "s", f"{p}י{e}יתי"),
        R("past", "2ms", "m", "s", f"{p}י{e}ית"),
        R("past", "2fs", "f", "s", f"{p}י{e}ית"),
        R("past", "3ms", "m", "s", f"{p}י{e}ה"),
        R("past", "3fs", "f", "s", f"{p}י{e}תה"),
        R("past", "1p", "mf", "p", f"{p}י{e}ינו"),
        R("past", "2mp", "m", "p", f"{p}י{e}יתם"),
        R("past", "2fp", "f", "p", f"{p}י{e}יתן"),
        R("past", "3p", "mf", "p", f"{p}י{e}ו"),
    ]
    # Present
    rows += [
        R("present", "ms", "m", "s", f"מ{p}{e}ה"),
        R("present", "fs", "f", "s", f"מ{p}{e}ה"),
        R("present", "mp", "m", "p", f"מ{p}{e}ים"),
        R("present", "fp", "f", "p", f"מ{p}{e}ות"),
    ]
    # Future
    rows += [
        R("future", "1s", "mf", "s", f"א{p}{e}ה"),
        R("future", "2ms", "m", "s", f"ת{p}{e}ה"),
        R("future", "2fs", "f", "s", f"ת{p}{e}י"),
        R("future", "3ms", "m", "s", f"י{p}{e}ה"),
        R("future", "3fs", "f", "s", f"ת{p}{e}ה"),
        R("future", "1p", "mf", "p", f"נ{p}{e}ה"),
        R("future", "2mp", "m", "p", f"ת{p}{e}ו"),
        R("future", "2fp", "f", "p", f"ת{p}{e}ינה"),
        R("future", "3mp", "m", "p", f"י{p}{e}ו"),
        R("future", "3fp", "f", "p", f"ת{p}{e}ינה"),
    ]
    rows += [
        R("imperative", "2ms", "m", "s", f"{p}{e}ה"),
        R("imperative", "2fs", "f", "s", f"{p}{e}י"),
        R("imperative", "2mp", "m", "p", f"{p}{e}ו"),
        R("imperative", "2fp", "f", "p", f"{p}{e}ינה"),
    ]
    return rows


# ─── Hif'il Regular ─────────────────────────────────────────────────────────

def conj_hifil_regular(root, word_id):
    """Hif'il for regular roots and pe-yod roots."""
    p, e, l = root
    R = lambda t, pe, g, n, f: _row(word_id, 5, t, pe, g, n, f)
    rows = []

    # Pe-yod roots: first letter drops, ו appears (הוסיף not הידעתי)
    # Pe-nun roots: first letter assimilates (הציל not הנצלתי)
    is_pe_yod = (p == 'י')
    is_pe_nun = (p == 'נ')

    if is_pe_yod:
        # Past: הו-E-L-ti (e.g., הוספתי, הודעתי)
        past_stem = f"הו{e}{l}"
        pres_stem = f"מו{e}י{l}"  # מוסיף, מודיע
        fut_inner = f"ו{e}י{l}"  # יוסיף, יודיע
    elif is_pe_nun:
        # Past: הP-E-L-ti but nun drops (הצלתי not הנצלתי)
        past_stem = f"ה{e}{l}"
        pres_stem = f"מ{e}י{l}"  # מציל
        fut_inner = f"{e}י{l}"   # יציל
    else:
        past_stem = f"ה{p}{e}{l}"
        pres_stem = f"מ{p}{e}י{l}"  # משפיע
        fut_inner = f"{p}{e}י{l}"    # ישפיע

    # Past
    rows += [
        R("past", "1s", "mf", "s", f"{past_stem}תי"),
        R("past", "2ms", "m", "s", f"{past_stem}ת"),
        R("past", "2fs", "f", "s", f"{past_stem}ת"),
        R("past", "3ms", "m", "s", f"ה{p}{e}י{l}" if not is_pe_yod and not is_pe_nun else (f"הו{e}י{l}" if is_pe_yod else f"ה{e}י{l}")),
        R("past", "3fs", "f", "s", f"ה{p}{e}י{l}ה" if not is_pe_yod and not is_pe_nun else (f"הו{e}י{l}ה" if is_pe_yod else f"ה{e}י{l}ה")),
        R("past", "1p", "mf", "p", f"{past_stem}נו"),
        R("past", "2mp", "m", "p", f"{past_stem}תם"),
        R("past", "2fp", "f", "p", f"{past_stem}תן"),
        R("past", "3p", "mf", "p", f"ה{p}{e}י{l}ו" if not is_pe_yod and not is_pe_nun else (f"הו{e}י{l}ו" if is_pe_yod else f"ה{e}י{l}ו")),
    ]
    # Present
    rows += [
        R("present", "ms", "m", "s", pres_stem),
        R("present", "fs", "f", "s", f"{pres_stem}ה"),
        R("present", "mp", "m", "p", f"{pres_stem}ים"),
        R("present", "fp", "f", "p", f"{pres_stem}ות"),
    ]
    # Future
    rows += [
        R("future", "1s", "mf", "s", f"א{fut_inner}"),
        R("future", "2ms", "m", "s", f"ת{fut_inner}"),
        R("future", "2fs", "f", "s", f"ת{fut_inner}י"),
        R("future", "3ms", "m", "s", f"י{fut_inner}"),
        R("future", "3fs", "f", "s", f"ת{fut_inner}"),
        R("future", "1p", "mf", "p", f"נ{fut_inner}"),
        R("future", "2mp", "m", "p", f"ת{fut_inner}ו"),
        R("future", "2fp", "f", "p", f"ת{fut_inner}נה"),
        R("future", "3mp", "m", "p", f"י{fut_inner}ו"),
        R("future", "3fp", "f", "p", f"ת{fut_inner}נה"),
    ]
    # Imperative
    rows += [
        R("imperative", "2ms", "m", "s", f"ה{fut_inner}" if not is_pe_yod else f"הו{e}{l}"),
        R("imperative", "2fs", "f", "s", f"ה{fut_inner}י" if not is_pe_yod else f"הו{e}י{l}י"),
        R("imperative", "2mp", "m", "p", f"ה{fut_inner}ו" if not is_pe_yod else f"הו{e}י{l}ו"),
        R("imperative", "2fp", "f", "p", f"ה{fut_inner}נה"),
    ]
    return rows


# ─── Hitpa'el ────────────────────────────────────────────────────────────────

def conj_hitpael_regular(root, word_id):
    p, e, l = root
    R = lambda t, pe, g, n, f: _row(word_id, 7, t, pe, g, n, f)
    rows = []

    # Handle sibilant metathesis
    if p == 'ש':
        prefix = "השת"
        root_part = f"{e}{l}"
    elif p == 'צ':
        prefix = "הצט"
        root_part = f"{e}{l}"
    elif p == 'ס':
        prefix = "הסת"
        root_part = f"{e}{l}"
    elif p == 'ז':
        prefix = "הזד"
        root_part = f"{e}{l}"
    else:
        prefix = "הת"
        root_part = f"{p}{e}{l}"

    # Handle ayin-ayin (doubled): insert ו between doubled letters
    if e == l:
        root_part = f"{p}ו{e}{l}"
        prefix = "הת"

    m_prefix = "מ" + prefix[1:]  # הת→מת, השת→משת
    fut_base = prefix[1:]         # הת→ת

    # Past
    rows += [
        R("past", "1s", "mf", "s", f"{prefix}{root_part}תי"),
        R("past", "2ms", "m", "s", f"{prefix}{root_part}ת"),
        R("past", "2fs", "f", "s", f"{prefix}{root_part}ת"),
        R("past", "3ms", "m", "s", f"{prefix}{root_part}"),
        R("past", "3fs", "f", "s", f"{prefix}{root_part}ה"),
        R("past", "1p", "mf", "p", f"{prefix}{root_part}נו"),
        R("past", "2mp", "m", "p", f"{prefix}{root_part}תם"),
        R("past", "2fp", "f", "p", f"{prefix}{root_part}תן"),
        R("past", "3p", "mf", "p", f"{prefix}{root_part}ו"),
    ]
    # Present
    rows += [
        R("present", "ms", "m", "s", f"{m_prefix}{root_part}"),
        R("present", "fs", "f", "s", f"{m_prefix}{root_part}ת"),
        R("present", "mp", "m", "p", f"{m_prefix}{root_part}ים"),
        R("present", "fp", "f", "p", f"{m_prefix}{root_part}ות"),
    ]
    # Future
    rows += [
        R("future", "1s", "mf", "s", f"א{fut_base}{root_part}"),
        R("future", "2ms", "m", "s", f"ת{fut_base}{root_part}"),
        R("future", "2fs", "f", "s", f"ת{fut_base}{root_part}י"),
        R("future", "3ms", "m", "s", f"י{fut_base}{root_part}"),
        R("future", "3fs", "f", "s", f"ת{fut_base}{root_part}"),
        R("future", "1p", "mf", "p", f"נ{fut_base}{root_part}"),
        R("future", "2mp", "m", "p", f"ת{fut_base}{root_part}ו"),
        R("future", "2fp", "f", "p", f"ת{fut_base}{root_part}נה"),
        R("future", "3mp", "m", "p", f"י{fut_base}{root_part}ו"),
        R("future", "3fp", "f", "p", f"ת{fut_base}{root_part}נה"),
    ]
    # Imperative
    rows += [
        R("imperative", "2ms", "m", "s", f"{prefix}{root_part}"),
        R("imperative", "2fs", "f", "s", f"{prefix}{root_part}י"),
        R("imperative", "2mp", "m", "p", f"{prefix}{root_part}ו"),
        R("imperative", "2fp", "f", "p", f"{prefix}{root_part}נה"),
    ]
    return rows


# ─── Nif'al ─────────────────────────────────────────────────────────────────

def conj_nifal_regular(root, word_id):
    p, e, l = root
    R = lambda t, pe, g, n, f: _row(word_id, 2, t, pe, g, n, f)
    rows = []

    # Past: niXXaX
    rows += [
        R("past", "1s", "mf", "s", f"נ{p}{e}{l}תי"),
        R("past", "2ms", "m", "s", f"נ{p}{e}{l}ת"),
        R("past", "2fs", "f", "s", f"נ{p}{e}{l}ת"),
        R("past", "3ms", "m", "s", f"נ{p}{e}{l}"),
        R("past", "3fs", "f", "s", f"נ{p}{e}{l}ה"),
        R("past", "1p", "mf", "p", f"נ{p}{e}{l}נו"),
        R("past", "2mp", "m", "p", f"נ{p}{e}{l}תם"),
        R("past", "2fp", "f", "p", f"נ{p}{e}{l}תן"),
        R("past", "3p", "mf", "p", f"נ{p}{e}{l}ו"),
    ]
    # Present: niXXaX
    rows += [
        R("present", "ms", "m", "s", f"נ{p}{e}{l}"),
        R("present", "fs", "f", "s", f"נ{p}{e}{l}ת"),
        R("present", "mp", "m", "p", f"נ{p}{e}{l}ים"),
        R("present", "fp", "f", "p", f"נ{p}{e}{l}ות"),
    ]
    # Future: yiPPaXeL (with yod after prefix)
    rows += [
        R("future", "1s", "mf", "s", f"אי{p}{e}{l}"),
        R("future", "2ms", "m", "s", f"תי{p}{e}{l}"),
        R("future", "2fs", "f", "s", f"תי{p}{e}{l}י"),
        R("future", "3ms", "m", "s", f"יי{p}{e}{l}"),
        R("future", "3fs", "f", "s", f"תי{p}{e}{l}"),
        R("future", "1p", "mf", "p", f"ני{p}{e}{l}"),
        R("future", "2mp", "m", "p", f"תי{p}{e}{l}ו"),
        R("future", "2fp", "f", "p", f"תי{p}{e}{l}נה"),
        R("future", "3mp", "m", "p", f"יי{p}{e}{l}ו"),
        R("future", "3fp", "f", "p", f"תי{p}{e}{l}נה"),
    ]
    # Imperative: hiPPaXeL
    rows += [
        R("imperative", "2ms", "m", "s", f"הי{p}{e}{l}"),
        R("imperative", "2fs", "f", "s", f"הי{p}{e}{l}י"),
        R("imperative", "2mp", "m", "p", f"הי{p}{e}{l}ו"),
        R("imperative", "2fp", "f", "p", f"הי{p}{e}{l}נה"),
    ]
    return rows


# ─── Main generator ──────────────────────────────────────────────────────────

def generate_conjugations(word_id: int, hebrew: str, root_str: str) -> list[dict]:
    root = parse_root(root_str)
    if not root or len(root) < 3:
        return []

    root_class = classify_root(root)
    binyan = identify_binyan(hebrew, root)

    if binyan == 1:  # Pa'al
        is_pe_yod = (root[0] == 'י')
        if root_class == 'hollow':
            return conj_paal_hollow(root, word_id)
        elif is_pe_yod:
            return conj_paal_pe_yod(root, word_id)
        elif root_class == 'lamed_he':
            return conj_paal_lamed_he(root, word_id)
        else:
            return conj_paal_regular(root, word_id)
    elif binyan == 3:  # Pi'el
        if root_class == 'lamed_he':
            return conj_piel_lamed_he(root, word_id)
        return conj_piel_regular(root, word_id)
    elif binyan == 5:  # Hif'il
        return conj_hifil_regular(root, word_id)
    elif binyan == 7:  # Hitpa'el
        return conj_hitpael_regular(root, word_id)
    elif binyan == 2:  # Nif'al
        return conj_nifal_regular(root, word_id)
    return []


if __name__ == "__main__":
    # Quick test
    tests = [
        (1283, "לכתוב", "כ.ת.ב", "כותב"),
        (1936, "לגור", "ג.ו.ר", "גר"),
        (1285, "לדבר", "ד.ב.ר", "מדבר"),
        (142, "להשפיע", "ש.פ.ע", "משפיע"),
        (999, "להתלבש", "ל.ב.ש", "מתלבש"),
        (729, "להתמודד", "מ.ד.ד", "מתמודד"),
        (954, "להיחשב", "ח.ש.ב", "נחשב"),
        # Pe-yod Pa'al:
        (1955, "לדעת", "י.ד.ע", "יודע"),
        (1939, "לשבת", "י.ש.ב", "יושב"),
        (1938, "לצאת", "י.צ.א", "יוצא"),
        (8260, "לרדת", "י.ר.ד", "יורד"),
    ]
    for wid, heb, root, expected_present in tests:
        forms = generate_conjugations(wid, heb, root)
        present_ms = [f for f in forms if f['tense'] == 'present' and f['person'] == 'ms']
        if present_ms:
            got = present_ms[0]['form_he']
            match = '✓' if got == expected_present else '✗'
            print(f"  {match} {heb} ({root}): {got} {'== ' + expected_present if match == '✓' else '!= ' + expected_present}")
        # Also show past 3p and future 1s for pe-yod verbs
        if root.startswith('י.'):
            past_3p = [f for f in forms if f['tense'] == 'past' and f['person'] == '3p']
            fut_1s = [f for f in forms if f['tense'] == 'future' and f['person'] == '1s']
            if past_3p:
                print(f"      past 3p: {past_3p[0]['form_he']}")
            if fut_1s:
                print(f"      future 1s: {fut_1s[0]['form_he']}")
