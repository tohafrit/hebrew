"""Shared Hebrew text utilities."""

import re
import unicodedata


def strip_nikkud(text: str) -> str:
    """Remove Hebrew nikkud (vowel marks) and cantillation marks from text.
    Preserves maqaf (U+05BE, Hebrew hyphen) to keep compound words intact.
    """
    return "".join(
        c for c in text
        if not ('\u0591' <= c <= '\u05BD' or '\u05BF' <= c <= '\u05C7')
    )


def normalize_answer(text: str) -> str:
    """Normalize answer for flexible comparison:
    - NFC unicode normalization
    - strip nikkud
    - lowercase
    - collapse whitespace
    - remove trailing/leading punctuation
    """
    text = unicodedata.normalize("NFC", text)
    text = strip_nikkud(text)
    text = text.strip().lower()
    text = re.sub(r'\s+', ' ', text)
    text = text.strip('.,!?;: \t\n')
    return text


def answers_match(user_str: str, accept_list: list) -> bool:
    """Check if user answer matches any accepted answer using flexible normalization."""
    user_norm = normalize_answer(user_str)
    for a in accept_list:
        if normalize_answer(str(a)) == user_norm:
            return True
    return False
