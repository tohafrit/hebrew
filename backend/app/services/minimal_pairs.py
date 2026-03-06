"""Minimal pairs drill — audio discrimination of similar Hebrew sounds."""

import random

# Curated minimal pairs: (pair_id, letter1, letter2, word1_he, word1_ru, word2_he, word2_ru)
MINIMAL_PAIRS = [
    ("kaf_khet", "כ", "ח", "כלב", "собака", "חלב", "молоко"),
    ("kuf_kaf", "ק", "כ", "קר", "холодный", "כר", "подушка"),
    ("tet_tav", "ט", "ת", "טוב", "хороший", "תוב", "очередь"),
    ("samekh_shin", "ס", "שׂ", "סוס", "лошадь", "שׂוש", "радость"),
    ("alef_ayin", "א", "ע", "אור", "свет", "עור", "кожа"),
    ("bet_vet", "ב", "ו", "בית", "дом", "וית", "ведь"),
    ("khet_heh", "ח", "ה", "חם", "горячий", "הם", "они"),
    ("shin_sin", "שׁ", "שׂ", "שׁמש", "солнце", "שׂמח", "радостный"),
    ("dalet_resh", "ד", "ר", "דם", "кровь", "רם", "высокий"),
    ("zayin_samekh", "ז", "ס", "זר", "чужой", "סר", "свернул"),
    ("pe_fe", "פּ", "פ", "פּה", "рот", "פה", "здесь"),
    ("gimel_kaf", "ג", "כ", "גל", "волна", "כל", "всё"),
    ("tet_dalet", "ט", "ד", "טל", "роса", "דל", "бедный"),
    ("tsadi_samekh", "צ", "ס", "צר", "узкий", "סר", "свернул"),
    ("bet_pe", "ב", "פ", "בר", "зерно", "פר", "бык"),
    ("tav_tet", "ת", "ט", "תם", "невинный", "טם", "запечатан"),
    ("kuf_khet", "ק", "ח", "קם", "встал", "חם", "горячий"),
    ("nun_mem", "נ", "מ", "נר", "свеча", "מר", "горький"),
    ("lamed_resh", "ל", "ר", "לב", "сердце", "רב", "много"),
    ("vav_bet", "ו", "ב", "ור", "и-", "בר", "зерно"),
]


def get_minimal_pairs_drill(count: int = 10) -> list[dict]:
    """Generate a minimal pairs drill session."""
    sampled = random.sample(MINIMAL_PAIRS, min(count, len(MINIMAL_PAIRS)))

    questions = []
    for pair_id, letter1, letter2, word1_he, word1_ru, word2_he, word2_ru in sampled:
        # Randomly choose which word to play
        if random.random() < 0.5:
            target_word = word1_he
            target_translation = word1_ru
            correct_letter = letter1
        else:
            target_word = word2_he
            target_translation = word2_ru
            correct_letter = letter2

        questions.append({
            "pair_id": pair_id,
            "target_word": target_word,
            "target_translation": target_translation,
            "correct_letter": correct_letter,
            "option1": {"letter": letter1, "word": word1_he, "translation": word1_ru},
            "option2": {"letter": letter2, "word": word2_he, "translation": word2_ru},
        })

    return questions


def check_minimal_pair(pair_id: str, answer_letter: str, correct_letter: str) -> bool:
    """Check if the answer is correct."""
    return answer_letter.strip() == correct_letter.strip()
