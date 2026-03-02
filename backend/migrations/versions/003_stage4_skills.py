"""Stage 4: Listening, Writing, Dialogue modules — seed data

Revision ID: 003
Revises: 002
Create Date: 2026-03-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ── Listening lessons & exercises ──────────────────────────────────────────

LISTENING_LESSONS = [
    # (level_id, unit, order, title_ru, title_he, description, type)
    (1, 5, 18, "Диктант: первые слова", "הכתבה: מילים ראשונות", "Послушайте и запишите слова", "listening"),
    (1, 5, 19, "Минимальные пары: согласные", "זוגות מינימליים", "Различайте похожие звуки", "listening"),
    (1, 5, 20, "Слушаем и понимаем: в ульпане", "שומעים ומבינים", "Прослушайте диалог и ответьте", "listening"),
    (2, 5, 21, "Диктант: предложения", "הכתבה: משפטים", "Запишите целые предложения", "listening"),
    (2, 5, 22, "Минимальные пары: гласные", "זוגות מינימליים: תנועות", "Различайте гласные звуки", "listening"),
]

LISTENING_EXERCISES = [
    # lesson_order 18: Dictation - first words
    (18, "dictation", 1,
     {"word_he": "שָׁלוֹם", "word_translit": "шалом", "hint": "Приветствие"},
     {"correct": "שלום", "accept": ["שלום", "שָׁלוֹם"]},
     {"text": "שָׁלוֹם (шалом) — привет, мир"}, 15),
    (18, "dictation", 1,
     {"word_he": "תּוֹדָה", "word_translit": "тодА", "hint": "Благодарность"},
     {"correct": "תודה", "accept": ["תודה", "תּוֹדָה"]},
     {"text": "תּוֹדָה (тодА) — спасибо"}, 15),
    (18, "dictation", 1,
     {"word_he": "סְלִיחָה", "word_translit": "слихА", "hint": "Извинение"},
     {"correct": "סליחה", "accept": ["סליחה", "סְלִיחָה"]},
     {"text": "סְלִיחָה (слихА) — извините"}, 15),
    (18, "dictation", 1,
     {"word_he": "בְּבַקָּשָׁה", "word_translit": "бевакашА", "hint": "Вежливость"},
     {"correct": "בבקשה", "accept": ["בבקשה", "בְּבַקָּשָׁה"]},
     {"text": "בְּבַקָּשָׁה (бевакашА) — пожалуйста"}, 15),
    (18, "dictation", 1,
     {"word_he": "כֵּן", "word_translit": "кен", "hint": "Согласие"},
     {"correct": "כן", "accept": ["כן", "כֵּן"]},
     {"text": "כֵּן (кен) — да"}, 15),
    (18, "dictation", 1,
     {"word_he": "לֹא", "word_translit": "ло", "hint": "Отрицание"},
     {"correct": "לא", "accept": ["לא", "לֹא"]},
     {"text": "לֹא (ло) — нет"}, 15),
    # lesson_order 19: Minimal pairs
    (19, "minimal_pairs", 1,
     {"pair_a": {"he": "בַּת", "translit": "бат", "meaning": "дочь"},
      "pair_b": {"he": "בֵּית", "translit": "бейт", "meaning": "дом"},
      "question": "Какое слово вы слышите?", "correct_pair": "a"},
     {"correct": "a"},
     {"text": "בַּת (бат) — дочь, בֵּית (бейт) — дом. Различие в гласной."}, 15),
    (19, "minimal_pairs", 1,
     {"pair_a": {"he": "כֶּלֶב", "translit": "кЕлев", "meaning": "собака"},
      "pair_b": {"he": "חָלָב", "translit": "халАв", "meaning": "молоко"},
      "question": "Какое слово вы слышите?", "correct_pair": "a"},
     {"correct": "a"},
     {"text": "כ (каф) — обычное 'к'; ח (хет) — гортанное 'х'"}, 15),
    (19, "minimal_pairs", 1,
     {"pair_a": {"he": "סֵפֶר", "translit": "сЕфер", "meaning": "книга"},
      "pair_b": {"he": "שָׂפָה", "translit": "сафА", "meaning": "язык/губа"},
      "question": "Какое слово вы слышите?", "correct_pair": "b"},
     {"correct": "b"},
     {"text": "ס (самех) = 'с'; שׂ (син) = тоже 'с'. В современном иврите звучат одинаково!"}, 15),
    (19, "minimal_pairs", 1,
     {"pair_a": {"he": "דָּג", "translit": "даг", "meaning": "рыба"},
      "pair_b": {"he": "דַּק", "translit": "дак", "meaning": "тонкий"},
      "question": "Какое слово вы слышите?", "correct_pair": "a"},
     {"correct": "a"},
     {"text": "ג (гимель) — звонкий 'г'; ק (куф) — глухой 'к'"}, 15),
    # lesson_order 20: Listening comprehension
    (20, "listening_comprehension", 2,
     {"text_he": "שלום! אני דני. אני לומד עברית בּאולפּן. המורה שלנו שמה רות.",
      "text_translit": "шалОм! анИ дАни. анИ ломЕд иврИт беульпАн. hа-морА шелАну шмА рут.",
      "questions": [
          {"question": "Как зовут говорящего?", "options": ["Рут", "Дэни", "Давид"], "correct": "Дэни"},
          {"question": "Где он учит иврит?", "options": ["в школе", "в ульпане", "дома"], "correct": "в ульпане"},
          {"question": "Как зовут учительницу?", "options": ["Дэни", "Сара", "Рут"], "correct": "Рут"}
      ]},
     {"correct_answers": ["Дэни", "в ульпане", "Рут"]},
     {"text": "Простой текст о студенте в ульпане"}, 30),
    # lesson_order 21: Dictation - sentences (Bet level)
    (21, "dictation", 2,
     {"word_he": "אני לומד עברית", "word_translit": "анИ ломЕд иврИт", "hint": "Я учу иврит"},
     {"correct": "אני לומד עברית", "accept": ["אני לומד עברית", "אֲנִי לוֹמֵד עִבְרִית"]},
     {"text": "אֲנִי לוֹמֵד עִבְרִית — Я учу иврит"}, 20),
    (21, "dictation", 2,
     {"word_he": "היא גרה בתל אביב", "word_translit": "hи гарА бетЕль авИв", "hint": "Она живёт в Тель-Авиве"},
     {"correct": "היא גרה בתל אביב", "accept": ["היא גרה בתל אביב"]},
     {"text": "הִיא גָּרָה בְּתֵל אָבִיב — Она живёт в Тель-Авиве"}, 20),
    (21, "dictation", 2,
     {"word_he": "אנחנו אוהבים ללמוד", "word_translit": "анАхну оhавИм лилмОд", "hint": "Мы любим учиться"},
     {"correct": "אנחנו אוהבים ללמוד", "accept": ["אנחנו אוהבים ללמוד"]},
     {"text": "אֲנַחְנוּ אוֹהֲבִים לִלְמֹד — Мы любим учиться"}, 20),
    # lesson_order 22: Minimal pairs - vowels (Bet level)
    (22, "minimal_pairs", 2,
     {"pair_a": {"he": "אוֹר", "translit": "ор", "meaning": "свет"},
      "pair_b": {"he": "אִיר", "translit": "ир", "meaning": "город"},
      "question": "Какое слово вы слышите?", "correct_pair": "a"},
     {"correct": "a"},
     {"text": "Различие в гласных: оо/о vs и"}, 15),
    (22, "minimal_pairs", 2,
     {"pair_a": {"he": "סוּס", "translit": "сус", "meaning": "лошадь"},
      "pair_b": {"he": "סִיס", "translit": "сис", "meaning": "(нет значения)"},
      "question": "Какое слово вы слышите?", "correct_pair": "a"},
     {"correct": "a"},
     {"text": "וּ (шурук) = 'у'; ִי (хирик+йуд) = 'и'"}, 15),
]

# ── Writing lessons & exercises ────────────────────────────────────────────

WRITING_LESSONS = [
    (1, 6, 23, "Пишем первые слова", "כותבים מילים ראשונות", "Напечатайте слова на иврите", "writing"),
    (1, 6, 24, "Перевод: русский → иврит", "תרגום: רוסית → עברית", "Переведите слова на иврит", "writing"),
    (2, 6, 25, "Пишем предложения", "כותבים משפטים", "Переведите предложения на иврит", "writing"),
    (2, 6, 26, "Свободное письмо", "כתיבה חופשית", "Напишите текст на иврите", "writing"),
]

WRITING_EXERCISES = [
    # lesson_order 23: Type first words
    (23, "hebrew_typing", 1,
     {"prompt": "Напечатайте слово: шалом (привет)", "target_he": "שלום", "transliteration": "шалом"},
     {"correct": "שלום", "accept": ["שלום", "שָׁלוֹם"]},
     {"text": "שָׁלוֹם (шалом) — привет, мир"}, 10),
    (23, "hebrew_typing", 1,
     {"prompt": "Напечатайте слово: тодА (спасибо)", "target_he": "תודה", "transliteration": "тодА"},
     {"correct": "תודה", "accept": ["תודה", "תּוֹדָה"]},
     {"text": "תּוֹדָה (тодА) — спасибо"}, 10),
    (23, "hebrew_typing", 1,
     {"prompt": "Напечатайте слово: йЕлед (мальчик)", "target_he": "ילד", "transliteration": "йЕлед"},
     {"correct": "ילד", "accept": ["ילד", "יֶלֶד"]},
     {"text": "יֶלֶד (йЕлед) — мальчик"}, 10),
    (23, "hebrew_typing", 1,
     {"prompt": "Напечатайте слово: ялдА (девочка)", "target_he": "ילדה", "transliteration": "ялдА"},
     {"correct": "ילדה", "accept": ["ילדה", "יַלְדָּה"]},
     {"text": "יַלְדָּה (ялдА) — девочка"}, 10),
    (23, "hebrew_typing", 1,
     {"prompt": "Напечатайте слово: сЕфер (книга)", "target_he": "ספר", "transliteration": "сЕфер"},
     {"correct": "ספר", "accept": ["ספר", "סֵפֶר"]},
     {"text": "סֵפֶר (сЕфер) — книга"}, 10),
    # lesson_order 24: Translation RU→HE
    (24, "translate_ru_he", 1,
     {"prompt_ru": "привет", "hint": "שׁ.ל.ם", "target_he": "שלום"},
     {"correct": "שלום", "accept": ["שלום", "שָׁלוֹם"]},
     {"text": "שָׁלוֹם (шалом) — привет"}, 15),
    (24, "translate_ru_he", 1,
     {"prompt_ru": "книга", "hint": "с.ф.р", "target_he": "ספר"},
     {"correct": "ספר", "accept": ["ספר", "סֵפֶר"]},
     {"text": "סֵפֶר (сЕфер) — книга"}, 15),
    (24, "translate_ru_he", 1,
     {"prompt_ru": "дом", "hint": "б.й.т", "target_he": "בית"},
     {"correct": "בית", "accept": ["בית", "בַּיִת"]},
     {"text": "בַּיִת (бАйит) — дом"}, 15),
    (24, "translate_ru_he", 1,
     {"prompt_ru": "вода", "hint": "м.й.м", "target_he": "מים"},
     {"correct": "מים", "accept": ["מים", "מַיִם"]},
     {"text": "מַיִם (мАйим) — вода"}, 15),
    (24, "translate_ru_he", 1,
     {"prompt_ru": "хлеб", "hint": "л.х.м", "target_he": "לחם"},
     {"correct": "לחם", "accept": ["לחם", "לֶחֶם"]},
     {"text": "לֶחֶם (лЕхем) — хлеб"}, 15),
    # lesson_order 25: Sentences RU→HE (Bet level)
    (25, "translate_ru_he", 2,
     {"prompt_ru": "Я учу иврит", "hint": "אני + לומד + עברית", "target_he": "אני לומד עברית"},
     {"correct": "אני לומד עברית", "accept": ["אני לומד עברית", "אני לומדת עברית"]},
     {"text": "אֲנִי לוֹמֵד/לוֹמֶדֶת עִבְרִית"}, 20),
    (25, "translate_ru_he", 2,
     {"prompt_ru": "Она живёт в Иерусалиме", "hint": "היא + גרה + ב + ירושלים", "target_he": "היא גרה בירושלים"},
     {"correct": "היא גרה בירושלים", "accept": ["היא גרה בירושלים"]},
     {"text": "הִיא גָּרָה בִּירוּשָׁלַיִם"}, 20),
    (25, "translate_ru_he", 2,
     {"prompt_ru": "Мы любим учиться", "hint": "אנחנו + אוהבים + ללמוד", "target_he": "אנחנו אוהבים ללמוד"},
     {"correct": "אנחנו אוהבים ללמוד", "accept": ["אנחנו אוהבים ללמוד", "אנחנו אוהבות ללמוד"]},
     {"text": "אֲנַחְנוּ אוֹהֲבִים לִלְמֹד"}, 20),
]

# ── Dialogues ──────────────────────────────────────────────────────────────

DIALOGUES = [
    # (level_id, title, situation_ru, lines_json, vocabulary_json)
    # Level 1 dialogues
    (1, "В ульпане: знакомство", "Первый день в ульпане. Познакомьтесь с другим студентом.",
     [{"speaker": "א", "speaker_name": "Дан", "text_he": "שלום! אני דן. מה שמך?", "text_ru": "Привет! Я Дан. Как тебя зовут?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Привет! Меня зовут...",
       "is_user": True, "options": ["שלום! שמי אלכס.", "שלום! אני סטודנט.", "שלום! מה שלומך?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Дан", "text_he": "נעים מאוד! מאיפה אתה?", "text_ru": "Очень приятно! Откуда ты?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Я из России.",
       "is_user": True, "options": ["אני מרוסיה.", "אני לומד עברית.", "אני גר פה."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Дан", "text_he": "מגניב! גם אני חדש כאן. בהצלחה!", "text_ru": "Здорово! Я тоже тут новый. Удачи!",
       "is_user": False}],
     [{"he": "מה שמך", "ru": "как тебя зовут", "translit": "ма шимхА"},
      {"he": "נעים מאוד", "ru": "очень приятно", "translit": "наИм меОд"},
      {"he": "מאיפה", "ru": "откуда", "translit": "меЭйфо"},
      {"he": "בהצלחה", "ru": "удачи", "translit": "беhацлахА"}]),

    (1, "В кафе: заказ", "Вы в кафе. Закажите напиток и еду.",
     [{"speaker": "א", "speaker_name": "Официант", "text_he": "שלום! מה תרצה לשתות?", "text_ru": "Привет! Что хотите выпить?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Кофе, пожалуйста.",
       "is_user": True, "options": ["קפה, בבקשה.", "אני רוצה מים.", "תה, בבקשה."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Официант", "text_he": "ועוגה? יש לנו עוגת שוקולד מעולה!", "text_ru": "И пирожное? У нас отличный шоколадный торт!",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Да, пожалуйста!",
       "is_user": True, "options": ["כן, בבקשה!", "לא, תודה.", "כמה זה עולה?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Официант", "text_he": "בסדר! זה יהיה ארבעים שקלים.", "text_ru": "Хорошо! Это будет сорок шекелей.",
       "is_user": False}],
     [{"he": "קפה", "ru": "кофе", "translit": "кафЕ"},
      {"he": "עוגה", "ru": "пирожное/торт", "translit": "угА"},
      {"he": "שוקולד", "ru": "шоколад", "translit": "шоколАд"},
      {"he": "שקלים", "ru": "шекели", "translit": "шкалИм"}]),

    (1, "На улице: дорога", "Вы заблудились. Спросите дорогу у прохожего.",
     [{"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Извините, как пройти к автобусной остановке?",
       "is_user": True, "options": ["סליחה, איך מגיעים לתחנת האוטובוס?", "סליחה, מה השעה?", "סליחה, איפה השירותים?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Прохожий", "text_he": "ישר, ואז שמאלה ברמזור.", "text_ru": "Прямо, потом налево на светофоре.",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Спасибо большое!",
       "is_user": True, "options": ["תודה רבה!", "סליחה, לא הבנתי.", "בסדר, תודה."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Прохожий", "text_he": "בבקשה! בהצלחה!", "text_ru": "Пожалуйста! Удачи!",
       "is_user": False}],
     [{"he": "תחנת האוטובוס", "ru": "автобусная остановка", "translit": "таханАт hа-отобУс"},
      {"he": "ישר", "ru": "прямо", "translit": "яшАр"},
      {"he": "שמאלה", "ru": "налево", "translit": "смОла"},
      {"he": "רמזור", "ru": "светофор", "translit": "рамзОр"}]),

    (1, "В магазине: покупки", "Вы в продуктовом магазине.",
     [{"speaker": "א", "speaker_name": "Продавец", "text_he": "שלום! אפשר לעזור?", "text_ru": "Привет! Могу помочь?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Да, где молоко?",
       "is_user": True, "options": ["כן, איפה החלב?", "כן, כמה עולה הלחם?", "לא, תודה."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Продавец", "text_he": "במקרר, בסוף המעבר.", "text_ru": "В холодильнике, в конце прохода.",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Спасибо! А сколько стоит хлеб?",
       "is_user": True, "options": ["תודה! וכמה עולה הלחם?", "תודה, להתראות!", "אני לא מבין."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Продавец", "text_he": "שבעה שקלים.", "text_ru": "Семь шекелей.",
       "is_user": False}],
     [{"he": "חלב", "ru": "молоко", "translit": "халАв"},
      {"he": "מקרר", "ru": "холодильник", "translit": "мекарЕр"},
      {"he": "מעבר", "ru": "проход", "translit": "маавАр"},
      {"he": "לחם", "ru": "хлеб", "translit": "лЕхем"}]),

    (1, "У врача: запись", "Запишитесь на приём к врачу.",
     [{"speaker": "א", "speaker_name": "Регистратор", "text_he": "שלום, קופת חולים. במה אוכל לעזור?", "text_ru": "Здравствуйте, больничная касса. Чем могу помочь?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Я хочу записаться к врачу.",
       "is_user": True, "options": ["אני רוצה לקבוע תור לרופא.", "אני חולה.", "מה השעה?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Регистратор", "text_he": "יש תור ביום שלישי בשעה עשר. מתאים?", "text_ru": "Есть запись на вторник в 10. Подходит?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Да, подходит. Спасибо.",
       "is_user": True, "options": ["כן, מתאים. תודה.", "לא, יש משהו אחר?", "אני לא יודע."],
       "correct_option": 0}],
     [{"he": "קופת חולים", "ru": "больничная касса", "translit": "купАт холИм"},
      {"he": "תור", "ru": "очередь/запись", "translit": "тор"},
      {"he": "רופא", "ru": "врач", "translit": "рофЕ"},
      {"he": "מתאים", "ru": "подходит", "translit": "матъИм"}]),

    (1, "По телефону: звонок", "Вы звоните другу.",
     [{"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Алло, привет! Это (ваше имя).",
       "is_user": True, "options": ["הלו, שלום! זה אלכס.", "שלום, מה נשמע?", "הלו?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Друг", "text_he": "היי! מה נשמע? לא דיברנו הרבה זמן!", "text_ru": "Привет! Как дела? Давно не разговаривали!",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Всё хорошо! Хочешь встретиться?",
       "is_user": True, "options": ["הכול טוב! רוצה להיפגש?", "אני עסוק.", "מתי אתה פנוי?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Друг", "text_he": "כן, בטח! מחר בערב?", "text_ru": "Да, конечно! Завтра вечером?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Отлично! До завтра!",
       "is_user": True, "options": ["מצוין! להתראות מחר!", "אני לא יכול.", "בסדר, נדבר."],
       "correct_option": 0}],
     [{"he": "מה נשמע", "ru": "как дела", "translit": "ма нишмА"},
      {"he": "להיפגש", "ru": "встретиться", "translit": "леhипагЕш"},
      {"he": "מחר", "ru": "завтра", "translit": "махАр"},
      {"he": "להתראות", "ru": "до свидания", "translit": "леhитраОт"}]),

    # Level 2 dialogues
    (2, "В банке: открытие счёта", "Вы открываете счёт в израильском банке.",
     [{"speaker": "א", "speaker_name": "Клерк", "text_he": "שלום! במה אני יכול לעזור?", "text_ru": "Здравствуйте! Чем могу помочь?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Я хочу открыть счёт.",
       "is_user": True, "options": ["אני רוצה לפתוח חשבון.", "אני רוצה להפקיד כסף.", "כמה הריבית?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Клерк", "text_he": "בוודאי. אני צריך את התעודת זהות שלך ואישור כתובת.", "text_ru": "Конечно. Мне нужно ваше удостоверение личности и подтверждение адреса.",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Вот, пожалуйста. Вот мой паспорт.",
       "is_user": True, "options": ["הנה, בבקשה. הנה הדרכון שלי.", "אין לי תעודת זהות.", "רגע, אני אחפש."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Клерк", "text_he": "תודה. תמלא את הטופס הזה בבקשה.", "text_ru": "Спасибо. Заполните эту форму, пожалуйста.",
       "is_user": False}],
     [{"he": "חשבון", "ru": "счёт", "translit": "хешбОн"},
      {"he": "תעודת זהות", "ru": "удостоверение личности", "translit": "теудАт зеhУт"},
      {"he": "דרכון", "ru": "паспорт", "translit": "даркОн"},
      {"he": "טופס", "ru": "форма/бланк", "translit": "тОфес"}]),

    (2, "На почте", "Вы отправляете посылку на почте.",
     [{"speaker": "א", "speaker_name": "Работник", "text_he": "שלום! מה ברצונך לשלוח?", "text_ru": "Привет! Что хотите отправить?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Я хочу отправить посылку в Россию.",
       "is_user": True, "options": ["אני רוצה לשלוח חבילה לרוסיה.", "אני צריך בולים.", "יש לי מכתב."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Работник", "text_he": "כמה שוקל החבילה?", "text_ru": "Сколько весит посылка?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Около двух килограммов.",
       "is_user": True, "options": ["בערך שני קילו.", "אני לא יודע.", "זה לא כבד."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Работник", "text_he": "זה יעלה שמונים שקלים. רגיל או מהיר?", "text_ru": "Это будет стоить 80 шекелей. Обычная или быстрая доставка?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Обычная, пожалуйста.",
       "is_user": True, "options": ["רגיל, בבקשה.", "מהיר, בבקשה.", "כמה ההבדל?"],
       "correct_option": 0}],
     [{"he": "חבילה", "ru": "посылка", "translit": "хавилА"},
      {"he": "לשלוח", "ru": "отправить", "translit": "лишлОах"},
      {"he": "שוקל", "ru": "весит", "translit": "шокЕль"},
      {"he": "מהיר", "ru": "быстрый", "translit": "маhИр"}]),

    (2, "В аэропорту: регистрация", "Вы регистрируетесь на рейс в аэропорту Бен-Гурион.",
     [{"speaker": "א", "speaker_name": "Агент", "text_he": "שלום! הדרכון והכרטיס בבקשה.", "text_ru": "Здравствуйте! Паспорт и билет, пожалуйста.",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Вот, пожалуйста.",
       "is_user": True, "options": ["הנה, בבקשה.", "רגע, אני מחפש.", "איפה הצ'ק-אין?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Агент", "text_he": "יש לך מזוודות?", "text_ru": "У вас есть чемоданы?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Да, один чемодан.",
       "is_user": True, "options": ["כן, מזוודה אחת.", "לא, רק תיק יד.", "שתי מזוודות."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Агент", "text_he": "חלון או מעבר?", "text_ru": "Окно или проход?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "У окна, пожалуйста.",
       "is_user": True, "options": ["חלון, בבקשה.", "מעבר, בבקשה.", "לא משנה."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Агент", "text_he": "הנה כרטיס ההעלייה. שער שלוש. טיסה נעימה!", "text_ru": "Вот посадочный талон. Выход три. Приятного полёта!",
       "is_user": False}],
     [{"he": "דרכון", "ru": "паспорт", "translit": "даркОн"},
      {"he": "מזוודה", "ru": "чемодан", "translit": "мизвадА"},
      {"he": "חלון", "ru": "окно", "translit": "халОн"},
      {"he": "שער", "ru": "ворота/выход", "translit": "шАар"},
      {"he": "טיסה", "ru": "полёт", "translit": "тисА"}]),

    (2, "На работе: собеседование", "Вы на собеседовании на новую работу.",
     [{"speaker": "א", "speaker_name": "HR", "text_he": "שלום! ספר לי קצת על עצמך.", "text_ru": "Здравствуйте! Расскажите немного о себе.",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Я программист с опытом 5 лет.",
       "is_user": True, "options": ["אני מתכנת עם ניסיון של חמש שנים.", "אני מחפש עבודה.", "אני אוהב לעבוד."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "HR", "text_he": "מעניין! למה אתה רוצה לעבוד אצלנו?", "text_ru": "Интересно! Почему хотите работать у нас?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Мне нравится ваша компания.",
       "is_user": True, "options": ["אני אוהב את החברה שלכם.", "המשכורת טובה.", "זה קרוב לבית."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "HR", "text_he": "מצוין! אנחנו נחזור אליך השבוע.", "text_ru": "Отлично! Мы свяжемся с вами на этой неделе.",
       "is_user": False}],
     [{"he": "מתכנת", "ru": "программист", "translit": "метахнЕт"},
      {"he": "ניסיון", "ru": "опыт", "translit": "нисайОн"},
      {"he": "חברה", "ru": "компания", "translit": "хеврА"},
      {"he": "משכורת", "ru": "зарплата", "translit": "маскОрет"}]),

    (2, "В ресторане: ужин", "Вы ужинаете в ресторане.",
     [{"speaker": "א", "speaker_name": "Официант", "text_he": "ערב טוב! הנה התפריט.", "text_ru": "Добрый вечер! Вот меню.",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Спасибо. Что вы порекомендуете?",
       "is_user": True, "options": ["תודה. מה אתה ממליץ?", "אני רוצה סטייק.", "יש תפריט בערבית?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Официант", "text_he": "הדג שלנו מצוין! ויש סלט ירושלמי מיוחד.", "text_ru": "Наша рыба отличная! И есть особый иерусалимский салат.",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Я возьму рыбу и салат.",
       "is_user": True, "options": ["אני אקח את הדג ואת הסלט.", "רק מים, תודה.", "אני צמחוני."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Официант", "text_he": "ומה לשתות?", "text_ru": "А что пить?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Красное вино, пожалуйста.",
       "is_user": True, "options": ["יין אדום, בבקשה.", "מים, בבקשה.", "בירה, בבקשה."],
       "correct_option": 0}],
     [{"he": "תפריט", "ru": "меню", "translit": "тафрИт"},
      {"he": "ממליץ", "ru": "рекомендует", "translit": "мамлИц"},
      {"he": "דג", "ru": "рыба", "translit": "даг"},
      {"he": "סלט", "ru": "салат", "translit": "салАт"},
      {"he": "יין", "ru": "вино", "translit": "яин"}]),

    (2, "В аптеке", "У вас болит голова. Вы идёте в аптеку.",
     [{"speaker": "א", "speaker_name": "Фармацевт", "text_he": "שלום! איך אני יכול לעזור?", "text_ru": "Привет! Чем могу помочь?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "У меня болит голова.",
       "is_user": True, "options": ["כואב לי הראש.", "אני צריך תרופות.", "יש לך אקמול?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Фармацевт", "text_he": "יש לנו אקמול ונורופן. מה אתה מעדיף?", "text_ru": "У нас есть акамол и нурофен. Что предпочитаете?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Акамол, пожалуйста.",
       "is_user": True, "options": ["אקמול, בבקשה.", "נורופן, בבקשה.", "מה ההבדל?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Фармацевт", "text_he": "בבקשה. קח כדור כל שש שעות. רפואה שלמה!", "text_ru": "Пожалуйста. Принимай таблетку каждые шесть часов. Выздоравливай!",
       "is_user": False}],
     [{"he": "כואב", "ru": "болит", "translit": "коЭв"},
      {"he": "ראש", "ru": "голова", "translit": "рош"},
      {"he": "תרופות", "ru": "лекарства", "translit": "труфОт"},
      {"he": "כדור", "ru": "таблетка", "translit": "кадУр"},
      {"he": "רפואה שלמה", "ru": "выздоравливай", "translit": "рефуА шлемА"}]),

    (2, "Съём квартиры", "Вы ищете квартиру для аренды.",
     [{"speaker": "א", "speaker_name": "Хозяин", "text_he": "שלום! אתה מחפש דירה?", "text_ru": "Привет! Ищете квартиру?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Да, двухкомнатную.",
       "is_user": True, "options": ["כן, דירת שני חדרים.", "כן, דירה גדולה.", "כמה עולה?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Хозяин", "text_he": "יש לי דירה ברחוב הרצל. שלושת אלפים שקלים בחודש.", "text_ru": "У меня есть квартира на улице Герцля. 3000 шекелей в месяц.",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Можно посмотреть квартиру?",
       "is_user": True, "options": ["אפשר לראות את הדירה?", "זה יקר מדי.", "יש מרפסת?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Хозяин", "text_he": "כן, בוא מחר בארבע אחרי הצהריים.", "text_ru": "Да, приходи завтра в четыре дня.",
       "is_user": False}],
     [{"he": "דירה", "ru": "квартира", "translit": "дирА"},
      {"he": "חדרים", "ru": "комнаты", "translit": "хадарИм"},
      {"he": "רחוב", "ru": "улица", "translit": "рехОв"},
      {"he": "מרפסת", "ru": "балкон", "translit": "мирпЕсет"}]),

    (1, "В автобусе", "Вы едете на автобусе в первый раз.",
     [{"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Извините, этот автобус едет в центр?",
       "is_user": True, "options": ["סליחה, האוטובוס הזה נוסע למרכז?", "סליחה, מתי האוטובוס?", "כמה עולה כרטיס?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Пассажир", "text_he": "כן, הוא עוצר בתחנה המרכזית.", "text_ru": "Да, он останавливается на центральной станции.",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Спасибо! Сколько стоит проезд?",
       "is_user": True, "options": ["תודה! כמה עולה נסיעה?", "תודה רבה!", "מתי הוא מגיע?"],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Пассажир", "text_he": "חמישה שקלים וחמישים אגורות. אתה צריך רב-קו.", "text_ru": "5.50 шекелей. Тебе нужен Рав-Кав.",
       "is_user": False}],
     [{"he": "אוטובוס", "ru": "автобус", "translit": "отобУс"},
      {"he": "מרכז", "ru": "центр", "translit": "меркАз"},
      {"he": "תחנה", "ru": "станция", "translit": "таханА"},
      {"he": "נסיעה", "ru": "поездка", "translit": "несиА"},
      {"he": "רב-קו", "ru": "Рав-Кав (проездной)", "translit": "рав-кав"}]),

    (2, "В поликлинике: приём", "Вы на приёме у врача.",
     [{"speaker": "א", "speaker_name": "Врач", "text_he": "שלום! מה הבעיה?", "text_ru": "Здравствуйте! Что вас беспокоит?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "У меня болит горло и температура.",
       "is_user": True, "options": ["כואב לי הגרון ויש לי חום.", "כואב לי הראש.", "אני לא מרגיש טוב."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Врач", "text_he": "מתי זה התחיל?", "text_ru": "Когда это началось?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Два дня назад.",
       "is_user": True, "options": ["לפני יומיים.", "אתמול.", "לא זוכר."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Врач", "text_he": "אני כותב לך מרשם לאנטיביוטיקה. תרגיש יותר טוב בעוד כמה ימים.", "text_ru": "Я выписываю рецепт на антибиотик. Через несколько дней тебе станет лучше.",
       "is_user": False}],
     [{"he": "גרון", "ru": "горло", "translit": "гарОн"},
      {"he": "חום", "ru": "температура/жар", "translit": "хом"},
      {"he": "מרשם", "ru": "рецепт", "translit": "миршАм"},
      {"he": "אנטיביוטיקה", "ru": "антибиотик", "translit": "антибиОтика"}]),

    (1, "Знакомство на вечеринке", "Вы на вечеринке и знакомитесь с новыми людьми.",
     [{"speaker": "א", "speaker_name": "Гость", "text_he": "היי! מה שמך? אני לא מכיר אותך.", "text_ru": "Привет! Как тебя зовут? Я тебя не знаю.",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Привет! Я (имя). Я друг хозяина.",
       "is_user": True, "options": ["שלום! אני אלכס. אני חבר של בעל הבית.", "שלום! אני חדש פה.", "היי! נעים מאוד."],
       "correct_option": 0},
      {"speaker": "א", "speaker_name": "Гость", "text_he": "נעים מאוד! מה אתה עושה?", "text_ru": "Очень приятно! Чем ты занимаешься?",
       "is_user": False},
      {"speaker": "ב", "speaker_name": "Вы", "text_he": "", "text_ru": "Я программист. А ты?",
       "is_user": True, "options": ["אני מתכנת. ואתה?", "אני עובד. ואתה?", "אני לומד עברית."],
       "correct_option": 0}],
     [{"he": "מכיר", "ru": "знаю/знаком", "translit": "макИр"},
      {"he": "חבר", "ru": "друг", "translit": "хавЕр"},
      {"he": "בעל הבית", "ru": "хозяин дома", "translit": "бАаль hа-бАйит"},
      {"he": "מה אתה עושה", "ru": "чем занимаешься", "translit": "ма атА осЕ"}]),
]


def upgrade() -> None:
    # ── Seed listening lessons ──
    lessons_t = sa.table("lessons",
        sa.column("level_id", sa.Integer), sa.column("unit", sa.Integer),
        sa.column("order", sa.Integer), sa.column("title_ru", sa.String),
        sa.column("title_he", sa.String), sa.column("description", sa.Text),
        sa.column("type", sa.String))
    op.bulk_insert(lessons_t, [
        {"level_id": l[0], "unit": l[1], "order": l[2], "title_ru": l[3],
         "title_he": l[4], "description": l[5], "type": l[6]}
        for l in LISTENING_LESSONS
    ])

    # ── Seed writing lessons ──
    op.bulk_insert(lessons_t, [
        {"level_id": l[0], "unit": l[1], "order": l[2], "title_ru": l[3],
         "title_he": l[4], "description": l[5], "type": l[6]}
        for l in WRITING_LESSONS
    ])

    # We need to get lesson IDs by order since they're auto-incremented.
    # Exercises reference lesson_id. Since lessons are ordered, we use a mapping.
    # lesson_order -> lesson_id will be resolved by finding lessons by order.
    conn = op.get_bind()

    # Build lesson order->id map
    result = conn.execute(sa.text("SELECT id, \"order\" FROM lessons"))
    order_to_id = {row[1]: row[0] for row in result}

    # ── Seed listening exercises ──
    exercises_t = sa.table("exercises",
        sa.column("lesson_id", sa.Integer), sa.column("type", sa.String),
        sa.column("difficulty", sa.Integer), sa.column("prompt_json", postgresql.JSONB),
        sa.column("answer_json", postgresql.JSONB), sa.column("explanation_json", postgresql.JSONB),
        sa.column("points", sa.Integer))

    all_exercises = LISTENING_EXERCISES + WRITING_EXERCISES
    exercise_rows = []
    for e in all_exercises:
        lesson_order = e[0]
        lesson_id = order_to_id.get(lesson_order)
        if lesson_id is None:
            continue
        exercise_rows.append({
            "lesson_id": lesson_id,
            "type": e[1], "difficulty": e[2],
            "prompt_json": e[3], "answer_json": e[4],
            "explanation_json": e[5], "points": e[6]
        })

    if exercise_rows:
        op.bulk_insert(exercises_t, exercise_rows)

    # ── Seed dialogues ──
    dialogues_t = sa.table("dialogues",
        sa.column("level_id", sa.Integer), sa.column("title", sa.String),
        sa.column("situation_ru", sa.Text), sa.column("lines_json", postgresql.JSONB),
        sa.column("vocabulary_json", postgresql.JSONB))
    op.bulk_insert(dialogues_t, [
        {"level_id": d[0], "title": d[1], "situation_ru": d[2],
         "lines_json": d[3], "vocabulary_json": d[4]}
        for d in DIALOGUES
    ])


def downgrade() -> None:
    op.execute("DELETE FROM dialogues")
    op.execute("DELETE FROM exercises WHERE type IN ('dictation','minimal_pairs','listening_comprehension','hebrew_typing','translate_ru_he')")
    op.execute("DELETE FROM lessons WHERE type IN ('listening','writing')")
