"""Populate example_sentences table with 300+ sentences across all 6 levels.

Each sentence is linked to a specific word in the dictionary and demonstrates
natural Hebrew usage at the appropriate CEFR level.

Revision ID: 040
Revises: 039
Create Date: 2026-03-02
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "040"
down_revision: Union[str, None] = "039"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

example_sentences_table = sa.table(
    "example_sentences",
    sa.column("word_id", sa.Integer),
    sa.column("hebrew", sa.Text),
    sa.column("translation_ru", sa.Text),
    sa.column("transliteration", sa.Text),
    sa.column("audio_url", sa.String),
    sa.column("level_id", sa.Integer),
)

# ==============================================================================
# LEVEL 1 (A1) — Simple SVO, present tense, basic everyday sentences
# 8-10 sentences per word, ~50 total
# ==============================================================================

LEVEL_1_SENTENCES = [
    # --- 1279: לאכול (есть) ---
    {"word_id": 1279, "hebrew": "אני אוכל ארוחת בוקר", "translation_ru": "Я ем завтрак", "transliteration": "ани охЭль арухАт бОкер", "audio_url": None, "level_id": 1},
    {"word_id": 1279, "hebrew": "היא אוכלת תפוח", "translation_ru": "Она ест яблоко", "transliteration": "hи охЭлет тапУах", "audio_url": None, "level_id": 1},
    {"word_id": 1279, "hebrew": "אנחנו אוכלים ביחד", "translation_ru": "Мы едим вместе", "transliteration": "анАхну охлИм бэйАхад", "audio_url": None, "level_id": 1},
    {"word_id": 1279, "hebrew": "הילדים אוכלים גלידה", "translation_ru": "Дети едят мороженое", "transliteration": "hа-йеладИм охлИм глидА", "audio_url": None, "level_id": 1},
    {"word_id": 1279, "hebrew": "אתה אוכל בצהריים?", "translation_ru": "Ты ешь в обед?", "transliteration": "атА охЭль ба-цоhорАйим?", "audio_url": None, "level_id": 1},
    {"word_id": 1279, "hebrew": "הוא אוכל לחם עם חמאה", "translation_ru": "Он ест хлеб с маслом", "transliteration": "hу охЭль лЭхем им хэмА", "audio_url": None, "level_id": 1},
    {"word_id": 1279, "hebrew": "אני לא אוכל בשר", "translation_ru": "Я не ем мясо", "transliteration": "ани ло охЭль басАр", "audio_url": None, "level_id": 1},
    {"word_id": 1279, "hebrew": "את אוכלת סלט?", "translation_ru": "Ты ешь салат?", "transliteration": "ат охЭлет салАт?", "audio_url": None, "level_id": 1},
    {"word_id": 1279, "hebrew": "הם אוכלים ארוחת ערב", "translation_ru": "Они едят ужин", "transliteration": "hэм охлИм арухАт Эрев", "audio_url": None, "level_id": 1},

    # --- 1280: לשתות (пить) ---
    {"word_id": 1280, "hebrew": "אני שותה מים", "translation_ru": "Я пью воду", "transliteration": "ани шотЭ мАйим", "audio_url": None, "level_id": 1},
    {"word_id": 1280, "hebrew": "היא שותה קפה בבוקר", "translation_ru": "Она пьёт кофе утром", "transliteration": "hи шотА кафЭ ба-бОкер", "audio_url": None, "level_id": 1},
    {"word_id": 1280, "hebrew": "הילד שותה חלב", "translation_ru": "Ребёнок пьёт молоко", "transliteration": "hа-йЭлед шотЭ халАв", "audio_url": None, "level_id": 1},
    {"word_id": 1280, "hebrew": "אנחנו שותים תה", "translation_ru": "Мы пьём чай", "transliteration": "анАхну шотИм тэ", "audio_url": None, "level_id": 1},
    {"word_id": 1280, "hebrew": "אתה שותה מיץ תפוזים?", "translation_ru": "Ты пьёшь апельсиновый сок?", "transliteration": "атА шотЭ миц тапузИм?", "audio_url": None, "level_id": 1},
    {"word_id": 1280, "hebrew": "הם שותים בירה בערב", "translation_ru": "Они пьют пиво вечером", "transliteration": "hэм шотИм бИра ба-Эрев", "audio_url": None, "level_id": 1},
    {"word_id": 1280, "hebrew": "אני לא שותה אלכוהול", "translation_ru": "Я не пью алкоголь", "transliteration": "ани ло шотЭ алкоhОль", "audio_url": None, "level_id": 1},
    {"word_id": 1280, "hebrew": "את שותה מים קרים?", "translation_ru": "Ты пьёшь холодную воду?", "transliteration": "ат шотА мАйим карИм?", "audio_url": None, "level_id": 1},

    # --- 1281: לישון (спать) ---
    {"word_id": 1281, "hebrew": "אני ישן בלילה", "translation_ru": "Я сплю ночью", "transliteration": "ани яшЭн ба-лАйла", "audio_url": None, "level_id": 1},
    {"word_id": 1281, "hebrew": "הילדה ישנה על המיטה", "translation_ru": "Девочка спит на кровати", "transliteration": "hа-ялдА йешенА аль hа-митА", "audio_url": None, "level_id": 1},
    {"word_id": 1281, "hebrew": "התינוק ישן הרבה", "translation_ru": "Младенец много спит", "transliteration": "hа-тинОк яшЭн hарбЭ", "audio_url": None, "level_id": 1},
    {"word_id": 1281, "hebrew": "אנחנו ישנים שמונה שעות", "translation_ru": "Мы спим восемь часов", "transliteration": "анАхну йешенИм шмОнэ шаОт", "audio_url": None, "level_id": 1},
    {"word_id": 1281, "hebrew": "הוא לא ישן טוב", "translation_ru": "Он не спит хорошо", "transliteration": "hу ло яшЭн тов", "audio_url": None, "level_id": 1},
    {"word_id": 1281, "hebrew": "את ישנה מוקדם?", "translation_ru": "Ты ложишься спать рано?", "transliteration": "ат йешенА мукдАм?", "audio_url": None, "level_id": 1},
    {"word_id": 1281, "hebrew": "הילדים ישנים בחדר", "translation_ru": "Дети спят в комнате", "transliteration": "hа-йеладИм йешенИм ба-хЭдер", "audio_url": None, "level_id": 1},
    {"word_id": 1281, "hebrew": "החתול ישן על הספה", "translation_ru": "Кот спит на диване", "transliteration": "hа-хатУль яшЭн аль hа-сапА", "audio_url": None, "level_id": 1},

    # --- 1282: ללכת (идти) ---
    {"word_id": 1282, "hebrew": "אני הולך לבית הספר", "translation_ru": "Я иду в школу", "transliteration": "ани hолЭх лэ-бЭйт hа-сЭфер", "audio_url": None, "level_id": 1},
    {"word_id": 1282, "hebrew": "היא הולכת לעבודה", "translation_ru": "Она идёт на работу", "transliteration": "hи hолЭхет ла-аводА", "audio_url": None, "level_id": 1},
    {"word_id": 1282, "hebrew": "אנחנו הולכים לפארק", "translation_ru": "Мы идём в парк", "transliteration": "анАхну hолхИм ла-пАрк", "audio_url": None, "level_id": 1},
    {"word_id": 1282, "hebrew": "הילדים הולכים הביתה", "translation_ru": "Дети идут домой", "transliteration": "hа-йеладИм hолхИм hа-бАйта", "audio_url": None, "level_id": 1},
    {"word_id": 1282, "hebrew": "אתה הולך לחנות?", "translation_ru": "Ты идёшь в магазин?", "transliteration": "атА hолЭх ла-ханУт?", "audio_url": None, "level_id": 1},
    {"word_id": 1282, "hebrew": "הוא הולך לאט", "translation_ru": "Он идёт медленно", "transliteration": "hу hолЭх лэ-Ат", "audio_url": None, "level_id": 1},
    {"word_id": 1282, "hebrew": "אני הולך ברגל", "translation_ru": "Я иду пешком", "transliteration": "ани hолЭх бэ-рЭгель", "audio_url": None, "level_id": 1},
    {"word_id": 1282, "hebrew": "את הולכת איתי?", "translation_ru": "Ты идёшь со мной?", "transliteration": "ат hолЭхет итИ?", "audio_url": None, "level_id": 1},

    # --- 1284: לכתוב (писать) ---
    {"word_id": 1284, "hebrew": "אני כותב מכתב", "translation_ru": "Я пишу письмо", "transliteration": "ани котЭв михтАв", "audio_url": None, "level_id": 1},
    {"word_id": 1284, "hebrew": "היא כותבת בעברית", "translation_ru": "Она пишет на иврите", "transliteration": "hи котЭвет бэ-иврИт", "audio_url": None, "level_id": 1},
    {"word_id": 1284, "hebrew": "התלמידים כותבים מבחן", "translation_ru": "Ученики пишут контрольную", "transliteration": "hа-тальмидИм котвИм мивхАн", "audio_url": None, "level_id": 1},
    {"word_id": 1284, "hebrew": "אתה כותב יפה", "translation_ru": "Ты красиво пишешь", "transliteration": "атА котЭв яфЭ", "audio_url": None, "level_id": 1},
    {"word_id": 1284, "hebrew": "הוא כותב את השם שלו", "translation_ru": "Он пишет своё имя", "transliteration": "hу котЭв эт hа-шЭм шелО", "audio_url": None, "level_id": 1},
    {"word_id": 1284, "hebrew": "אני כותב במחברת", "translation_ru": "Я пишу в тетради", "transliteration": "ани котЭв бэ-махбЭрет", "audio_url": None, "level_id": 1},
    {"word_id": 1284, "hebrew": "את כותבת הודעה?", "translation_ru": "Ты пишешь сообщение?", "transliteration": "ат котЭвет hодаА?", "audio_url": None, "level_id": 1},
    {"word_id": 1284, "hebrew": "אנחנו כותבים סיפור", "translation_ru": "Мы пишем рассказ", "transliteration": "анАхну котвИм сипУр", "audio_url": None, "level_id": 1},

    # --- 1285: לקרוא (читать) ---
    {"word_id": 1285, "hebrew": "אני קורא ספר", "translation_ru": "Я читаю книгу", "transliteration": "ани корЭ сЭфер", "audio_url": None, "level_id": 1},
    {"word_id": 1285, "hebrew": "היא קוראת עיתון", "translation_ru": "Она читает газету", "transliteration": "hи корЭт итОн", "audio_url": None, "level_id": 1},
    {"word_id": 1285, "hebrew": "הילדים קוראים סיפור", "translation_ru": "Дети читают рассказ", "transliteration": "hа-йеладИм корИм сипУр", "audio_url": None, "level_id": 1},
    {"word_id": 1285, "hebrew": "אתה קורא בעברית?", "translation_ru": "Ты читаешь на иврите?", "transliteration": "атА корЭ бэ-иврИт?", "audio_url": None, "level_id": 1},
    {"word_id": 1285, "hebrew": "הוא קורא כל יום", "translation_ru": "Он читает каждый день", "transliteration": "hу корЭ коль йом", "audio_url": None, "level_id": 1},
    {"word_id": 1285, "hebrew": "אנחנו קוראים ביחד", "translation_ru": "Мы читаем вместе", "transliteration": "анАхну корИм бэйАхад", "audio_url": None, "level_id": 1},
    {"word_id": 1285, "hebrew": "את קוראת לפני השינה?", "translation_ru": "Ты читаешь перед сном?", "transliteration": "ат корЭт лифнЭй hа-шенА?", "audio_url": None, "level_id": 1},
    {"word_id": 1285, "hebrew": "אני אוהב לקרוא", "translation_ru": "Я люблю читать", "transliteration": "ани оhЭв ликрО", "audio_url": None, "level_id": 1},

    # --- 1286: לדבר (говорить) ---
    {"word_id": 1286, "hebrew": "אני מדבר עברית", "translation_ru": "Я говорю на иврите", "transliteration": "ани медабЭр иврИт", "audio_url": None, "level_id": 1},
    {"word_id": 1286, "hebrew": "היא מדברת בטלפון", "translation_ru": "Она говорит по телефону", "transliteration": "hи медабЭрет ба-тЭлефон", "audio_url": None, "level_id": 1},
    {"word_id": 1286, "hebrew": "הם מדברים מהר", "translation_ru": "Они говорят быстро", "transliteration": "hэм медабрИм маhЭр", "audio_url": None, "level_id": 1},
    {"word_id": 1286, "hebrew": "אנחנו מדברים על הסרט", "translation_ru": "Мы говорим о фильме", "transliteration": "анАхну медабрИм аль hа-сЭрет", "audio_url": None, "level_id": 1},
    {"word_id": 1286, "hebrew": "אתה מדבר רוסית?", "translation_ru": "Ты говоришь по-русски?", "transliteration": "атА медабЭр русИт?", "audio_url": None, "level_id": 1},
    {"word_id": 1286, "hebrew": "הוא מדבר בשקט", "translation_ru": "Он говорит тихо", "transliteration": "hу медабЭр бэ-шЭкет", "audio_url": None, "level_id": 1},
    {"word_id": 1286, "hebrew": "את מדברת אנגלית?", "translation_ru": "Ты говоришь по-английски?", "transliteration": "ат медабЭрет англИт?", "audio_url": None, "level_id": 1},
    {"word_id": 1286, "hebrew": "הילד עוד לא מדבר", "translation_ru": "Ребёнок ещё не говорит", "transliteration": "hа-йЭлед од ло медабЭр", "audio_url": None, "level_id": 1},

    # --- 1287: לשמוע (слышать) ---
    {"word_id": 1287, "hebrew": "אני שומע מוזיקה", "translation_ru": "Я слушаю музыку", "transliteration": "ани шомЭа мУзика", "audio_url": None, "level_id": 1},
    {"word_id": 1287, "hebrew": "את שומעת אותי?", "translation_ru": "Ты слышишь меня?", "transliteration": "ат шомАат отИ?", "audio_url": None, "level_id": 1},
    {"word_id": 1287, "hebrew": "הוא שומע רעש", "translation_ru": "Он слышит шум", "transliteration": "hу шомЭа рАаш", "audio_url": None, "level_id": 1},
    {"word_id": 1287, "hebrew": "אנחנו שומעים שירים", "translation_ru": "Мы слушаем песни", "transliteration": "анАхну шомИм ширИм", "audio_url": None, "level_id": 1},
    {"word_id": 1287, "hebrew": "הם לא שומעים כלום", "translation_ru": "Они ничего не слышат", "transliteration": "hэм ло шомИм клюм", "audio_url": None, "level_id": 1},
    {"word_id": 1287, "hebrew": "אתה שומע את הציפורים?", "translation_ru": "Ты слышишь птиц?", "transliteration": "атА шомЭа эт hа-ципорИм?", "audio_url": None, "level_id": 1},
    {"word_id": 1287, "hebrew": "אני שומע את המורה", "translation_ru": "Я слышу учителя", "transliteration": "ани шомЭа эт hа-морЭ", "audio_url": None, "level_id": 1},
    {"word_id": 1287, "hebrew": "היא שומעת רדיו", "translation_ru": "Она слушает радио", "transliteration": "hи шомАат рАдио", "audio_url": None, "level_id": 1},

    # --- 1288: לראות (видеть) ---
    {"word_id": 1288, "hebrew": "אני רואה את הים", "translation_ru": "Я вижу море", "transliteration": "ани роЭ эт hа-ям", "audio_url": None, "level_id": 1},
    {"word_id": 1288, "hebrew": "היא רואה את החברה שלה", "translation_ru": "Она видит свою подругу", "transliteration": "hи роА эт hа-хаверА шелА", "audio_url": None, "level_id": 1},
    {"word_id": 1288, "hebrew": "אתה רואה את ההר?", "translation_ru": "Ты видишь гору?", "transliteration": "атА роЭ эт hа-hар?", "audio_url": None, "level_id": 1},
    {"word_id": 1288, "hebrew": "אנחנו רואים כוכבים", "translation_ru": "Мы видим звёзды", "transliteration": "анАхну роИм кохавИм", "audio_url": None, "level_id": 1},
    {"word_id": 1288, "hebrew": "הוא לא רואה טוב", "translation_ru": "Он плохо видит", "transliteration": "hу ло роЭ тов", "audio_url": None, "level_id": 1},
    {"word_id": 1288, "hebrew": "אני רואה ילדים בפארק", "translation_ru": "Я вижу детей в парке", "transliteration": "ани роЭ йеладИм ба-пАрк", "audio_url": None, "level_id": 1},
    {"word_id": 1288, "hebrew": "את רואה את הכלב?", "translation_ru": "Ты видишь собаку?", "transliteration": "ат роА эт hа-кЭлев?", "audio_url": None, "level_id": 1},
    {"word_id": 1288, "hebrew": "הם רואים סרט", "translation_ru": "Они смотрят фильм", "transliteration": "hэм роИм сЭрет", "audio_url": None, "level_id": 1},

    # --- 1289: לתת (давать) ---
    {"word_id": 1289, "hebrew": "אני נותן לך מתנה", "translation_ru": "Я даю тебе подарок", "transliteration": "ани нотЭн лехА матанА", "audio_url": None, "level_id": 1},
    {"word_id": 1289, "hebrew": "היא נותנת לו ספר", "translation_ru": "Она даёт ему книгу", "transliteration": "hи нотЭнет ло сЭфер", "audio_url": None, "level_id": 1},
    {"word_id": 1289, "hebrew": "המורה נותנת שיעורי בית", "translation_ru": "Учительница задаёт домашнее задание", "transliteration": "hа-морА нотЭнет шиурЭй бАйит", "audio_url": None, "level_id": 1},
    {"word_id": 1289, "hebrew": "אנחנו נותנים עזרה", "translation_ru": "Мы оказываем помощь", "transliteration": "анАхну нотнИм эзрА", "audio_url": None, "level_id": 1},

    # --- 1290: לקחת (брать) ---
    {"word_id": 1290, "hebrew": "אני לוקח את המפתחות", "translation_ru": "Я беру ключи", "transliteration": "ани локЭах эт hа-мафтехОт", "audio_url": None, "level_id": 1},
    {"word_id": 1290, "hebrew": "היא לוקחת תיק", "translation_ru": "Она берёт сумку", "transliteration": "hи локАхат тик", "audio_url": None, "level_id": 1},
    {"word_id": 1290, "hebrew": "הוא לוקח מטריה", "translation_ru": "Он берёт зонт", "transliteration": "hу локЭах митрийА", "audio_url": None, "level_id": 1},
    {"word_id": 1290, "hebrew": "אתה לוקח את הילדים?", "translation_ru": "Ты забираешь детей?", "transliteration": "атА локЭах эт hа-йеладИм?", "audio_url": None, "level_id": 1},

    # --- 1292: ללמוד (учиться) ---
    {"word_id": 1292, "hebrew": "אני לומד עברית", "translation_ru": "Я учу иврит", "transliteration": "ани ломЭд иврИт", "audio_url": None, "level_id": 1},
    {"word_id": 1292, "hebrew": "היא לומדת באוניברסיטה", "translation_ru": "Она учится в университете", "transliteration": "hи ломЭдет ба-университА", "audio_url": None, "level_id": 1},
    {"word_id": 1292, "hebrew": "הילדים לומדים בבית הספר", "translation_ru": "Дети учатся в школе", "transliteration": "hа-йеладИм ломдИм бэ-бЭйт hа-сЭфер", "audio_url": None, "level_id": 1},
    {"word_id": 1292, "hebrew": "אנחנו לומדים כל יום", "translation_ru": "Мы учимся каждый день", "transliteration": "анАхну ломдИм коль йом", "audio_url": None, "level_id": 1},
    {"word_id": 1292, "hebrew": "אתה לומד מתמטיקה?", "translation_ru": "Ты учишь математику?", "transliteration": "атА ломЭд матемАтика?", "audio_url": None, "level_id": 1},
    {"word_id": 1292, "hebrew": "הוא לומד לבד", "translation_ru": "Он учится сам", "transliteration": "hу ломЭд левАд", "audio_url": None, "level_id": 1},

    # --- 1293: לעבוד (работать) ---
    {"word_id": 1293, "hebrew": "אני עובד במשרד", "translation_ru": "Я работаю в офисе", "transliteration": "ани овЭд ба-мисрАд", "audio_url": None, "level_id": 1},
    {"word_id": 1293, "hebrew": "היא עובדת בבית חולים", "translation_ru": "Она работает в больнице", "transliteration": "hи овЭдет бэ-бЭйт холИм", "audio_url": None, "level_id": 1},
    {"word_id": 1293, "hebrew": "הם עובדים קשה", "translation_ru": "Они работают усердно", "transliteration": "hэм овдИм кашЭ", "audio_url": None, "level_id": 1},
    {"word_id": 1293, "hebrew": "אנחנו עובדים מהבית", "translation_ru": "Мы работаем из дома", "transliteration": "анАхну овдИм мэ-hа-бАйит", "audio_url": None, "level_id": 1},
    {"word_id": 1293, "hebrew": "אתה עובד היום?", "translation_ru": "Ты работаешь сегодня?", "transliteration": "атА овЭд hа-йОм?", "audio_url": None, "level_id": 1},
    {"word_id": 1293, "hebrew": "הוא לא עובד בשבת", "translation_ru": "Он не работает в субботу", "transliteration": "hу ло овЭд бэ-шабАт", "audio_url": None, "level_id": 1},
]

# ==============================================================================
# LEVEL 2 (A2) — Past/future tense, more complex structures
# 4-6 sentences per word, ~50 total
# ==============================================================================

LEVEL_2_SENTENCES = [
    # --- 108: לפעול (действовать) ---
    {"word_id": 108, "hebrew": "הממשלה פעלה במהירות", "translation_ru": "Правительство действовало быстро", "transliteration": "hа-мемшалА паалА бэ-мэhирУт", "audio_url": None, "level_id": 2},
    {"word_id": 108, "hebrew": "אנחנו צריכים לפעול עכשיו", "translation_ru": "Нам нужно действовать сейчас", "transliteration": "анАхну црихИм лифОль ахшАв", "audio_url": None, "level_id": 2},
    {"word_id": 108, "hebrew": "הוא יפעל לפי התוכנית", "translation_ru": "Он будет действовать по плану", "transliteration": "hу йифАль лефИ hа-тохнИт", "audio_url": None, "level_id": 2},
    {"word_id": 108, "hebrew": "המשטרה פועלת נגד הפשע", "translation_ru": "Полиция действует против преступности", "transliteration": "hа-миштарА поЭлет нЭгед hа-пЭша", "audio_url": None, "level_id": 2},
    {"word_id": 108, "hebrew": "הארגון פעל במשך שנים", "translation_ru": "Организация действовала в течение многих лет", "transliteration": "hа-иргУн паАль бэ-мЭшех шанИм", "audio_url": None, "level_id": 2},

    # --- 124: לגדול (расти) ---
    {"word_id": 124, "hebrew": "גדלתי בתל אביב", "translation_ru": "Я вырос в Тель-Авиве", "transliteration": "гадАльти бэ-тЭль авИв", "audio_url": None, "level_id": 2},
    {"word_id": 124, "hebrew": "הילדים גדלים מהר", "translation_ru": "Дети растут быстро", "transliteration": "hа-йеладИм гдэлИм маhЭр", "audio_url": None, "level_id": 2},
    {"word_id": 124, "hebrew": "העץ יגדל ויהיה גבוה", "translation_ru": "Дерево вырастет и будет высоким", "transliteration": "hа-эц йигдАль вэ-йиhйЭ гавОа", "audio_url": None, "level_id": 2},
    {"word_id": 124, "hebrew": "היא גדלה במשפחה גדולה", "translation_ru": "Она выросла в большой семье", "transliteration": "hи гадлА бэ-мишпахА гдолА", "audio_url": None, "level_id": 2},
    {"word_id": 124, "hebrew": "הפרחים גדלים בגינה", "translation_ru": "Цветы растут в саду", "transliteration": "hа-прахИм гдэлИм ба-гинА", "audio_url": None, "level_id": 2},
    {"word_id": 124, "hebrew": "המספרים ימשיכו לגדול", "translation_ru": "Числа продолжат расти", "transliteration": "hа-миспарИм ямшИху лигдОль", "audio_url": None, "level_id": 2},

    # --- 131: לנהל (управлять) ---
    {"word_id": 131, "hebrew": "הוא ניהל את החברה עשר שנים", "translation_ru": "Он управлял компанией десять лет", "transliteration": "hу ниhЭль эт hа-хэврА Эсер шанИм", "audio_url": None, "level_id": 2},
    {"word_id": 131, "hebrew": "היא מנהלת את המסעדה", "translation_ru": "Она управляет рестораном", "transliteration": "hи менаhЭлет эт hа-мисадА", "audio_url": None, "level_id": 2},
    {"word_id": 131, "hebrew": "אני אנהל את הפרויקט הזה", "translation_ru": "Я буду управлять этим проектом", "transliteration": "ани анаhЭль эт hа-проЭкт hа-зЭ", "audio_url": None, "level_id": 2},
    {"word_id": 131, "hebrew": "קשה לנהל צוות גדול", "translation_ru": "Сложно управлять большой командой", "transliteration": "кашЭ ленаhЭль цЭвет гадОль", "audio_url": None, "level_id": 2},
    {"word_id": 131, "hebrew": "הם ניהלו משא ומתן", "translation_ru": "Они вели переговоры", "transliteration": "hэм ниhалУ масА у-матАн", "audio_url": None, "level_id": 2},

    # --- 142: להשפיע (влиять) ---
    {"word_id": 142, "hebrew": "המזג אוויר משפיע על מצב הרוח", "translation_ru": "Погода влияет на настроение", "transliteration": "мЭзег hа-авИр машпИа аль мацАв hа-рУах", "audio_url": None, "level_id": 2},
    {"word_id": 142, "hebrew": "ההורים השפיעו עליי מאוד", "translation_ru": "Родители очень повлияли на меня", "transliteration": "hа-hорИм hишпИу алАй мэОд", "audio_url": None, "level_id": 2},
    {"word_id": 142, "hebrew": "הספר הזה ישפיע על רבים", "translation_ru": "Эта книга повлияет на многих", "transliteration": "hа-сЭфер hа-зЭ яшпИа аль рабИм", "audio_url": None, "level_id": 2},
    {"word_id": 142, "hebrew": "הטכנולוגיה משפיעה על החיים שלנו", "translation_ru": "Технологии влияют на нашу жизнь", "transliteration": "hа-технолОгия машпИа аль hа-хайИм шелАну", "audio_url": None, "level_id": 2},
    {"word_id": 142, "hebrew": "אי אפשר להשפיע על הכל", "translation_ru": "Невозможно повлиять на всё", "transliteration": "и эфшАр лэhашпИа аль hа-коль", "audio_url": None, "level_id": 2},

    # --- 149: להוסיף (добавлять) ---
    {"word_id": 149, "hebrew": "הוסיפי מלח למרק", "translation_ru": "Добавь соль в суп", "transliteration": "hосИфи мЭлах ла-марАк", "audio_url": None, "level_id": 2},
    {"word_id": 149, "hebrew": "אני רוצה להוסיף עוד משפט", "translation_ru": "Я хочу добавить ещё предложение", "transliteration": "ани роцЭ лэhосИф од мишпАт", "audio_url": None, "level_id": 2},
    {"word_id": 149, "hebrew": "הם הוסיפו פרטים חדשים", "translation_ru": "Они добавили новые подробности", "transliteration": "hэм hосИфу пратИм хадашИм", "audio_url": None, "level_id": 2},
    {"word_id": 149, "hebrew": "נוסיף את זה לרשימה", "translation_ru": "Мы добавим это в список", "transliteration": "носИф эт зэ ла-решимА", "audio_url": None, "level_id": 2},
    {"word_id": 149, "hebrew": "היא הוסיפה הערה בסוף", "translation_ru": "Она добавила примечание в конце", "transliteration": "hи hосИфа hеарА ба-сОф", "audio_url": None, "level_id": 2},

    # --- 152: להודיע (сообщить) ---
    {"word_id": 152, "hebrew": "הודיעו לנו על השינוי", "translation_ru": "Нам сообщили об изменении", "transliteration": "hодИу лАну аль hа-шинУй", "audio_url": None, "level_id": 2},
    {"word_id": 152, "hebrew": "אני אודיע לך מחר", "translation_ru": "Я сообщу тебе завтра", "transliteration": "ани одИа лехА махАр", "audio_url": None, "level_id": 2},
    {"word_id": 152, "hebrew": "המנהל הודיע על הפגישה", "translation_ru": "Директор сообщил о собрании", "transliteration": "hа-менаhЭль hодИа аль hа-пгишА", "audio_url": None, "level_id": 2},
    {"word_id": 152, "hebrew": "צריך להודיע מראש", "translation_ru": "Нужно сообщать заранее", "transliteration": "царИх лэhодИа мэ-рОш", "audio_url": None, "level_id": 2},
    {"word_id": 152, "hebrew": "היא הודיעה שהיא עוזבת", "translation_ru": "Она сообщила, что уходит", "transliteration": "hи hодИа шэ-hи озЭвет", "audio_url": None, "level_id": 2},

    # --- 736: לתקן (чинить) ---
    {"word_id": 736, "hebrew": "הוא תיקן את המכונית", "translation_ru": "Он починил машину", "transliteration": "hу тикЭн эт hа-мехонИт", "audio_url": None, "level_id": 2},
    {"word_id": 736, "hebrew": "אני צריך לתקן את הברז", "translation_ru": "Мне нужно починить кран", "transliteration": "ани царИх летакЭн эт hа-бЭрез", "audio_url": None, "level_id": 2},
    {"word_id": 736, "hebrew": "הטכנאי יתקן את המזגן מחר", "translation_ru": "Техник починит кондиционер завтра", "transliteration": "hа-технАй йетакЭн эт hа-мазгАн махАр", "audio_url": None, "level_id": 2},
    {"word_id": 736, "hebrew": "היא תיקנה את המחשב בעצמה", "translation_ru": "Она починила компьютер сама", "transliteration": "hи тикнА эт hа-махшЭв бэ-ацмА", "audio_url": None, "level_id": 2},
    {"word_id": 736, "hebrew": "לא כדאי לתקן את זה, עדיף לקנות חדש", "translation_ru": "Не стоит это чинить, лучше купить новое", "transliteration": "ло кедАй летакЭн эт зэ, адИф ликнОт хадАш", "audio_url": None, "level_id": 2},

    # --- 912: להסתדר (устраиваться) ---
    {"word_id": 912, "hebrew": "הוא הסתדר במקום החדש", "translation_ru": "Он освоился на новом месте", "transliteration": "hу hистадЭр ба-макОм hэ-хадАш", "audio_url": None, "level_id": 2},
    {"word_id": 912, "hebrew": "איך אתה מסתדר בעבודה?", "translation_ru": "Как ты справляешься на работе?", "transliteration": "эйх атА мистадЭр ба-аводА?", "audio_url": None, "level_id": 2},
    {"word_id": 912, "hebrew": "אל תדאגי, אני אסתדר", "translation_ru": "Не волнуйся, я справлюсь", "transliteration": "аль тидаагИ, ани эстадЭр", "audio_url": None, "level_id": 2},
    {"word_id": 912, "hebrew": "הילדים הסתדרו טוב בגן", "translation_ru": "Дети хорошо устроились в садике", "transliteration": "hа-йеладИм hистадрУ тов ба-ган", "audio_url": None, "level_id": 2},
    {"word_id": 912, "hebrew": "היא תסתדר גם בלעדיך", "translation_ru": "Она справится и без тебя", "transliteration": "hи тистадЭр гам билъадЭха", "audio_url": None, "level_id": 2},

    # --- 938: לאשר (утверждать) ---
    {"word_id": 938, "hebrew": "הוועדה אישרה את התקציב", "translation_ru": "Комиссия утвердила бюджет", "transliteration": "hа-ваадА ишрА эт hа-такцИв", "audio_url": None, "level_id": 2},
    {"word_id": 938, "hebrew": "אנחנו מאשרים את ההזמנה", "translation_ru": "Мы подтверждаем заказ", "transliteration": "анАхну меашрИм эт hа-hазманА", "audio_url": None, "level_id": 2},
    {"word_id": 938, "hebrew": "המנהל יאשר את הבקשה", "translation_ru": "Начальник утвердит просьбу", "transliteration": "hа-менаhЭль йеашЭр эт hа-бакашА", "audio_url": None, "level_id": 2},
    {"word_id": 938, "hebrew": "אישרת את התנאים?", "translation_ru": "Ты утвердил условия?", "transliteration": "ишАрта эт hа-тнаИм?", "audio_url": None, "level_id": 2},
    {"word_id": 938, "hebrew": "הרופא אישר שהוא בריא", "translation_ru": "Врач подтвердил, что он здоров", "transliteration": "hа-рофЭ ишЭр шэ-hу барИ", "audio_url": None, "level_id": 2},
]

# ==============================================================================
# LEVEL 3 (B1) — Conditional, passive, subordinate clauses
# 3-4 sentences per word, ~20 total
# ==============================================================================

LEVEL_3_SENTENCES = [
    # --- 93: לנוע (двигаться) ---
    {"word_id": 93, "hebrew": "אם לא תנוע מהר, תאחר לרכבת", "translation_ru": "Если не будешь двигаться быстро, опоздаешь на поезд", "transliteration": "им ло танУа маhЭр, теахЭр ла-ракЭвет", "audio_url": None, "level_id": 3},
    {"word_id": 93, "hebrew": "העננים נעים לאט מעל העיר", "translation_ru": "Облака медленно движутся над городом", "transliteration": "hа-ананИм наИм лэ-Ат мэ-Аль hа-ир", "audio_url": None, "level_id": 3},
    {"word_id": 93, "hebrew": "התנועה לא נעה כבר שעה", "translation_ru": "Движение не двигается уже час", "transliteration": "hа-тнуА ло наА квар шаА", "audio_url": None, "level_id": 3},
    {"word_id": 93, "hebrew": "כשהאדמה נעה, כולם נבהלו", "translation_ru": "Когда земля двигалась, все испугались", "transliteration": "кшэ-hа-адамА наА, кулАм нивhалУ", "audio_url": None, "level_id": 3},

    # --- 97: ללחום (бороться) ---
    {"word_id": 97, "hebrew": "הם נלחמו על החופש שלהם במשך שנים", "translation_ru": "Они боролись за свою свободу в течение многих лет", "transliteration": "hэм нилхамУ аль hа-хОфеш шелаhЭм бэ-мЭшех шанИм", "audio_url": None, "level_id": 3},
    {"word_id": 97, "hebrew": "אם נלחם ביחד, נצליח", "translation_ru": "Если будем бороться вместе, победим", "transliteration": "им нилахЭм бэйАхад, нацлИах", "audio_url": None, "level_id": 3},
    {"word_id": 97, "hebrew": "היא נלחמת במחלה בגבורה", "translation_ru": "Она мужественно борется с болезнью", "transliteration": "hи нилхЭмет бэ-махалА бэ-гвурА", "audio_url": None, "level_id": 3},
    {"word_id": 97, "hebrew": "צריך ללחום על מה שחשוב לך", "translation_ru": "Нужно бороться за то, что тебе важно", "transliteration": "царИх лилхОм аль ма шэ-хашУв лехА", "audio_url": None, "level_id": 3},

    # --- 113: ליצור (создавать) ---
    {"word_id": 113, "hebrew": "האמן יצר פסל שמושך תשומת לב רבה", "translation_ru": "Художник создал скульптуру, которая привлекает много внимания", "transliteration": "hа-оман яцАр пЭсель шэ-мошЭх тсумАт лев рабА", "audio_url": None, "level_id": 3},
    {"word_id": 113, "hebrew": "אם תיצרי קשר עם הלקוח, נוכל להתקדם", "translation_ru": "Если ты свяжешься с клиентом, мы сможем продвинуться", "transliteration": "им тицрИ кЭшер им hа-лакОах, нухАль лэhиткадЭм", "audio_url": None, "level_id": 3},
    {"word_id": 113, "hebrew": "הטכנולוגיה יוצרת אפשרויות חדשות", "translation_ru": "Технология создаёт новые возможности", "transliteration": "hа-технолОгия йоцЭрет эфшарийОт хадашОт", "audio_url": None, "level_id": 3},
    {"word_id": 113, "hebrew": "נוצרה בעיה שלא צפינו אותה", "translation_ru": "Возникла проблема, которую мы не предвидели", "transliteration": "ноцрА бэайА шэ-ло цафИну отА", "audio_url": None, "level_id": 3},

    # --- 123: לצפות (смотреть, ожидать) ---
    {"word_id": 123, "hebrew": "צפיתי בסרט שהמלצת עליו", "translation_ru": "Я посмотрел фильм, который ты рекомендовал", "transliteration": "цафИти ба-сЭрет шэ-hимлАцта алАв", "audio_url": None, "level_id": 3},
    {"word_id": 123, "hebrew": "אנחנו צופים שהמצב ישתפר", "translation_ru": "Мы ожидаем, что ситуация улучшится", "transliteration": "анАхну цофИм шэ-hа-мацАв йиштапЭр", "audio_url": None, "level_id": 3},
    {"word_id": 123, "hebrew": "אם תצפה בחדשות, תבין מה קורה", "translation_ru": "Если будешь смотреть новости, поймёшь, что происходит", "transliteration": "им тицпЭ ба-хадашОт, тавИн ма корЭ", "audio_url": None, "level_id": 3},
    {"word_id": 123, "hebrew": "הם צפו בשקיעה מהמרפסת", "translation_ru": "Они смотрели закат с балкона", "transliteration": "hэм цафУ ба-шкиА мэ-hа-мирпЭсет", "audio_url": None, "level_id": 3},

    # --- 156: להציל (спасать) ---
    {"word_id": 156, "hebrew": "המציל הציל ילד שטבע בים", "translation_ru": "Спасатель спас ребёнка, который тонул в море", "transliteration": "hа-мацИль hицИль йЭлед шэ-тавА ба-ям", "audio_url": None, "level_id": 3},
    {"word_id": 156, "hebrew": "אם היינו מגיעים מוקדם יותר, יכולנו להציל אותו", "translation_ru": "Если бы мы пришли раньше, могли бы его спасти", "transliteration": "им hайИну магиИм мукдАм йотЭр, яхОльну лэhацИль отО", "audio_url": None, "level_id": 3},
    {"word_id": 156, "hebrew": "הכבאים הצילו אנשים מהבניין הבוער", "translation_ru": "Пожарные спасли людей из горящего здания", "transliteration": "hа-кабаИм hицИлу анашИм мэ-hа-биньЯн hа-боЭр", "audio_url": None, "level_id": 3},
    {"word_id": 156, "hebrew": "הרופאים עושים הכל כדי להציל חיים", "translation_ru": "Врачи делают всё, чтобы спасать жизни", "transliteration": "hа-рофИм осИм hа-коль кдЭй лэhацИль хайИм", "audio_url": None, "level_id": 3},

    # Additional Level 3 sentences for more coverage

    # --- 93: лнуа (ещё) ---
    {"word_id": 93, "hebrew": "הכדור נע במהירות שלא ניתן לעקוב אחריו", "translation_ru": "Мяч двигался так быстро, что за ним невозможно было уследить", "transliteration": "hа-кадУр на бэ-мэhирУт шэ-ло нитАн лааков ахарАв", "audio_url": None, "level_id": 3},

    # --- 97: ללחום (ещё) ---
    {"word_id": 97, "hebrew": "הנלחמים על זכויותיהם ראויים להערכה", "translation_ru": "Борющиеся за свои права заслуживают уважения", "transliteration": "hа-нилхамИм аль зхуйотэйhЭм реуйИм лэhаарахА", "audio_url": None, "level_id": 3},

    # --- 113: ליצור (ещё) ---
    {"word_id": 113, "hebrew": "המוזיקאי יצר יצירה שמשלבת מזרח ומערב", "translation_ru": "Музыкант создал произведение, сочетающее Восток и Запад", "transliteration": "hа-музикАй яцАр йецирА шэ-мешалЭвет мизрАх у-маарАв", "audio_url": None, "level_id": 3},

    # --- 123: לצפות (ещё) ---
    {"word_id": 123, "hebrew": "לא צפינו שהתוצאות יהיו כל כך טובות", "translation_ru": "Мы не ожидали, что результаты будут такими хорошими", "transliteration": "ло цафИну шэ-hа-тоцаОт йиhйУ коль ках товОт", "audio_url": None, "level_id": 3},

    # --- 156: להציל (ещё) ---
    {"word_id": 156, "hebrew": "הארגון פועל להציל בעלי חיים בסכנת הכחדה", "translation_ru": "Организация работает ради спасения животных на грани вымирания", "transliteration": "hа-иргУн поЭль лэhацИль баалЭй хайИм бэ-саканАт hаххадА", "audio_url": None, "level_id": 3},

    # More Level 3 sentences to reach ~40

    # --- 93: לנוע ---
    {"word_id": 93, "hebrew": "הקו נע בין שני הנקודות", "translation_ru": "Линия движется между двумя точками", "transliteration": "hа-кав на бэйн штЭй hа-некудОт", "audio_url": None, "level_id": 3},
    {"word_id": 93, "hebrew": "אחרי שנע אל המקום הנכון, נוכל להתחיל", "translation_ru": "После того как переместимся на правильное место, сможем начать", "transliteration": "ахарЭй шэ-нанУа эль hа-макОм hа-нахОн, нухАль лэhатхИль", "audio_url": None, "level_id": 3},
    {"word_id": 93, "hebrew": "מי שלא נע, נשאר מאחור", "translation_ru": "Кто не двигается, тот остаётся позади", "transliteration": "ми шэ-ло на, нишАр мэ-ахОр", "audio_url": None, "level_id": 3},

    # --- 97: ללחום ---
    {"word_id": 97, "hebrew": "כדי שנלחם ביעילות, עלינו להתאחד", "translation_ru": "Чтобы бороться эффективно, нам нужно объединиться", "transliteration": "кдЭй шэ-нилахЭм бэ-йиилУт, алЭйну лэhитахЭд", "audio_url": None, "level_id": 3},
    {"word_id": 97, "hebrew": "הוא נלחם בכל כוחו כדי להצליח", "translation_ru": "Он боролся изо всех сил, чтобы преуспеть", "transliteration": "hу нилхАм бэ-холь кохО кдЭй лэhацлИах", "audio_url": None, "level_id": 3},
    {"word_id": 97, "hebrew": "החיילים שנלחמו בקרב חזרו הביתה", "translation_ru": "Солдаты, сражавшиеся в бою, вернулись домой", "transliteration": "hа-хайялИм шэ-нилхамУ ба-крАв хазрУ hа-бАйта", "audio_url": None, "level_id": 3},

    # --- 113: ליצור ---
    {"word_id": 113, "hebrew": "כשיוצרים משהו חדש, תמיד יש סיכון", "translation_ru": "Когда создаёшь что-то новое, всегда есть риск", "transliteration": "кшэ-йоцрИм мАшеhу хадАш, тамИд йеш сикУн", "audio_url": None, "level_id": 3},
    {"word_id": 113, "hebrew": "החברה יצרה מוצר שפתר בעיה גדולה", "translation_ru": "Компания создала продукт, который решил большую проблему", "transliteration": "hа-хэврА яцрА муцАр шэ-патАр бэайА гдолА", "audio_url": None, "level_id": 3},
    {"word_id": 113, "hebrew": "אם ניצור שיתוף פעולה, נגיע רחוק", "translation_ru": "Если мы создадим сотрудничество, мы далеко продвинемся", "transliteration": "им ницОр шитУф пеулА, нагИа рахОк", "audio_url": None, "level_id": 3},

    # --- 123: לצפות ---
    {"word_id": 123, "hebrew": "הקהל צפה בהצגה שנמשכה שלוש שעות", "translation_ru": "Публика смотрела представление, которое длилось три часа", "transliteration": "hа-каhАль цафА ба-hацагА шэ-нимшехА шалОш шаОт", "audio_url": None, "level_id": 3},
    {"word_id": 123, "hebrew": "מצפים ממך שתסיים את העבודה בזמן", "translation_ru": "От тебя ожидают, что закончишь работу вовремя", "transliteration": "мецапИм мимхА шэ-тесайЭм эт hа-аводА ба-змАн", "audio_url": None, "level_id": 3},
    {"word_id": 123, "hebrew": "אני צופה שהמחירים יעלו בקרוב", "translation_ru": "Я ожидаю, что цены скоро вырастут", "transliteration": "ани цофЭ шэ-hа-мехирИм яалУ бэ-карОв", "audio_url": None, "level_id": 3},

    # --- 156: להציל ---
    {"word_id": 156, "hebrew": "המתנדבים הצילו כלב שננטש ברחוב", "translation_ru": "Волонтёры спасли собаку, которую бросили на улице", "transliteration": "hа-митнадвИм hицИлу кЭлев шэ-нинтАш ба-рехОв", "audio_url": None, "level_id": 3},
    {"word_id": 156, "hebrew": "אילו פעלנו מוקדם יותר, היינו מצילים עוד אנשים", "translation_ru": "Если бы мы действовали раньше, спасли бы ещё людей", "transliteration": "илУ паАльну мукдАм йотЭр, hайИну мацилИм од анашИм", "audio_url": None, "level_id": 3},
    {"word_id": 156, "hebrew": "הטכנולוגיה החדשה עשויה להציל מיליוני חיים", "translation_ru": "Новая технология может спасти миллионы жизней", "transliteration": "hа-технолОгия hа-хадашА асуйА лэhацИль мильонЭй хайИм", "audio_url": None, "level_id": 3},
]

# ==============================================================================
# LEVEL 4 (B2) — Complex sentences, formal register
# 3-4 sentences per word, ~40 total
# ==============================================================================

LEVEL_4_SENTENCES = [
    # --- 137: לפרש (истолковывать) ---
    {"word_id": 137, "hebrew": "החוקרים פירשו את הממצאים בצורה שונה מהמקובל", "translation_ru": "Исследователи истолковали результаты иначе, чем принято", "transliteration": "hа-хокрИм пирШу эт hа-мимцаИм бэ-цурА шонА мэ-hа-мекубАль", "audio_url": None, "level_id": 4},
    {"word_id": 137, "hebrew": "ניתן לפרש את הטקסט הזה במספר דרכים", "translation_ru": "Этот текст можно истолковать несколькими способами", "transliteration": "нитАн лефарЭш эт hа-тЭкст hа-зЭ бэ-миспАр драхИм", "audio_url": None, "level_id": 4},
    {"word_id": 137, "hebrew": "בית המשפט פירש את החוק באופן מרחיב", "translation_ru": "Суд истолковал закон в расширительном смысле", "transliteration": "бэйт hа-мишпАт пирЭш эт hа-хОк бэ-Офен мархИв", "audio_url": None, "level_id": 4},
    {"word_id": 137, "hebrew": "כל דור מפרש מחדש את המסורת", "translation_ru": "Каждое поколение заново интерпретирует традицию", "transliteration": "коль дор мефарЭш мэ-хадАш эт hа-масОрет", "audio_url": None, "level_id": 4},

    # --- 147: להעלות (поднимать) ---
    {"word_id": 147, "hebrew": "הנואם העלה נושא שלא נדון בעבר", "translation_ru": "Выступающий поднял тему, которую не обсуждали раньше", "transliteration": "hа-ноЭм hеэлА носЭ шэ-ло нидОн бэ-авАр", "audio_url": None, "level_id": 4},
    {"word_id": 147, "hebrew": "הממשלה החליטה להעלות את המיסים", "translation_ru": "Правительство решило повысить налоги", "transliteration": "hа-мемшалА hэхлИта лэhаалОт эт hа-мисИм", "audio_url": None, "level_id": 4},
    {"word_id": 147, "hebrew": "חשוב להעלות את הנושא הזה בדיון הבא", "translation_ru": "Важно поднять эту тему на следующем обсуждении", "transliteration": "хашУв лэhаалОт эт hа-носЭ hа-зЭ ба-диюн hа-бА", "audio_url": None, "level_id": 4},
    {"word_id": 147, "hebrew": "הם העלו את הדגל לראש התורן", "translation_ru": "Они подняли флаг на верхушку мачты", "transliteration": "hэм hеэлУ эт hа-дЭгель лэ-рОш hа-тОрен", "audio_url": None, "level_id": 4},

    # --- 151: להוכיח (доказывать) ---
    {"word_id": 151, "hebrew": "המחקר הוכיח שהתאוריה נכונה", "translation_ru": "Исследование доказало, что теория верна", "transliteration": "hа-мэхкАр hохИах шэ-hа-теорИя нехонА", "audio_url": None, "level_id": 4},
    {"word_id": 151, "hebrew": "עליו להוכיח את חפותו בפני השופט", "translation_ru": "Он должен доказать свою невиновность перед судьёй", "transliteration": "алАв лэhохИах эт хафутО бифнЭй hа-шофЭт", "audio_url": None, "level_id": 4},
    {"word_id": 151, "hebrew": "הם לא הצליחו להוכיח את הטענה שלהם", "translation_ru": "Им не удалось доказать своё утверждение", "transliteration": "hэм ло hицлИху лэhохИах эт hа-таанА шелаhЭм", "audio_url": None, "level_id": 4},
    {"word_id": 151, "hebrew": "העובדות מוכיחות שהגישה הזו יעילה", "translation_ru": "Факты доказывают, что этот подход эффективен", "transliteration": "hа-увдОт мохихОт шэ-hа-гишА hа-зОт йеилА", "audio_url": None, "level_id": 4},

    # --- 405: להשלים (завершать) ---
    {"word_id": 405, "hebrew": "הקבלן השלים את הבנייה לפני המועד", "translation_ru": "Подрядчик завершил строительство досрочно", "transliteration": "hа-каблАн hишлИм эт hа-бнийА лифнЭй hа-моЭд", "audio_url": None, "level_id": 4},
    {"word_id": 405, "hebrew": "עלינו להשלים את הפרויקט עד סוף החודש", "translation_ru": "Мы должны завершить проект до конца месяца", "transliteration": "алЭйну лэhашлИм эт hа-проЭкт ад соф hа-хОдеш", "audio_url": None, "level_id": 4},
    {"word_id": 405, "hebrew": "היא השלימה את הדוקטורט שלה בהצטיינות", "translation_ru": "Она завершила свою докторскую с отличием", "transliteration": "hи hишлИма эт hа-докторАт шелА бэ-hицтайнУт", "audio_url": None, "level_id": 4},
    {"word_id": 405, "hebrew": "הצוות השלים את כל המשימות בזמן", "translation_ru": "Команда завершила все задачи вовремя", "transliteration": "hа-цЭвет hишлИм эт коль hа-мэсимОт ба-змАн", "audio_url": None, "level_id": 4},

    # --- 729: להתמודד (справляться) ---
    {"word_id": 729, "hebrew": "הוא מתמודד עם אתגרים מורכבים בעבודה", "translation_ru": "Он справляется со сложными вызовами на работе", "transliteration": "hу митмодЭд им атгарИм муркавИм ба-аводА", "audio_url": None, "level_id": 4},
    {"word_id": 729, "hebrew": "כיצד ניתן להתמודד עם לחץ מתמשך?", "translation_ru": "Как можно справиться с постоянным давлением?", "transliteration": "кэйцАд нитАн лэhитмодЭд им лАхац митмашЭх?", "audio_url": None, "level_id": 4},
    {"word_id": 729, "hebrew": "המדינה התמודדה עם משבר כלכלי חמור", "translation_ru": "Страна справилась с тяжёлым экономическим кризисом", "transliteration": "hа-мединА hитмодедА им машбЭр калкалИ хамУр", "audio_url": None, "level_id": 4},
    {"word_id": 729, "hebrew": "לא קל להתמודד עם ביקורת, אך זה חלק מהצמיחה", "translation_ru": "Нелегко справляться с критикой, но это часть роста", "transliteration": "ло каль лэhитмодЭд им бикОрет, ах зэ хЭлек мэ-hа-цмихА", "audio_url": None, "level_id": 4},

    # Additional Level 4 sentences

    # --- 137: לפרש ---
    {"word_id": 137, "hebrew": "הפילוסופים פירשו את הרעיון הזה בדרכים מנוגדות", "translation_ru": "Философы интерпретировали эту идею противоположными способами", "transliteration": "hа-филосОфим пирШу эт hа-раайОн hа-зЭ бэ-драхИм менугадОт", "audio_url": None, "level_id": 4},
    {"word_id": 137, "hebrew": "אין לפרש את דבריו כהסכמה", "translation_ru": "Не следует истолковывать его слова как согласие", "transliteration": "эйн лефарЭш эт дварАв кэ-hаскамА", "audio_url": None, "level_id": 4},
    {"word_id": 137, "hebrew": "כיצד מפרשים את הסמל הזה בתרבויות שונות?", "translation_ru": "Как интерпретируют этот символ в разных культурах?", "transliteration": "кэйцАд мефаршИм эт hа-сЭмель hа-зЭ бэ-тарбуйОт шонОт?", "audio_url": None, "level_id": 4},

    # --- 147: להעלות ---
    {"word_id": 147, "hebrew": "העובדים דרשו להעלות את השכר המינימלי", "translation_ru": "Работники потребовали повысить минимальную зарплату", "transliteration": "hа-овдИм даршУ лэhаалОт эт hа-сахАр hа-минимАли", "audio_url": None, "level_id": 4},
    {"word_id": 147, "hebrew": "המחקר העלה שאלות חדשות שטרם נחקרו", "translation_ru": "Исследование подняло новые вопросы, которые ещё не изучались", "transliteration": "hа-мэхкАр hеэлА шеэлОт хадашОт шэ-тЭрем нэхкерУ", "audio_url": None, "level_id": 4},
    {"word_id": 147, "hebrew": "ההצעה מעלה חששות רציניים בקרב המומחים", "translation_ru": "Предложение вызывает серьёзные опасения среди экспертов", "transliteration": "hа-hацаА маалА хашашОт рецинийИм бэ-кЭрев hа-мумхИм", "audio_url": None, "level_id": 4},

    # --- 151: להוכיח ---
    {"word_id": 151, "hebrew": "התובע ניסה להוכיח את אשמתו של הנאשם", "translation_ru": "Обвинитель пытался доказать вину подсудимого", "transliteration": "hа-товЭа нисА лэhохИах эт ашматО шель hа-нээшАм", "audio_url": None, "level_id": 4},
    {"word_id": 151, "hebrew": "הנתונים הסטטיסטיים מוכיחים מגמה ברורה", "translation_ru": "Статистические данные доказывают чёткую тенденцию", "transliteration": "hа-нетунИм hа-статИстийим мохихИм мегамА берурА", "audio_url": None, "level_id": 4},
    {"word_id": 151, "hebrew": "הוכח מעל כל ספק שהשיטה עובדת", "translation_ru": "Было доказано вне всяких сомнений, что метод работает", "transliteration": "hухАх мэ-Аль коль сАфек шэ-hа-шитА овЭдет", "audio_url": None, "level_id": 4},

    # --- 405: להשלים ---
    {"word_id": 405, "hebrew": "הסטודנטים נדרשים להשלים את העבודה האקדמית עד תום הסמסטר", "translation_ru": "Студенты обязаны завершить академическую работу до конца семестра", "transliteration": "hа-студЭнтим нидрашИм лэhашлИм эт hа-аводА hа-акадЭмит ад том hа-сЭместер", "audio_url": None, "level_id": 4},
    {"word_id": 405, "hebrew": "החברה השלימה את תהליך המיזוג בהצלחה", "translation_ru": "Компания успешно завершила процесс слияния", "transliteration": "hа-хэврА hишлИма эт таhалИх hа-мизУг бэ-hацлахА", "audio_url": None, "level_id": 4},
    {"word_id": 405, "hebrew": "המדען השלים מחקר פורץ דרך בתחום הגנטיקה", "translation_ru": "Учёный завершил прорывное исследование в области генетики", "transliteration": "hа-мадАн hишлИм мэхкАр порЭц дЭрех бэ-тхУм hа-генЭтика", "audio_url": None, "level_id": 4},

    # --- 729: להתמודד ---
    {"word_id": 729, "hebrew": "מערכת החינוך מתמודדת עם אתגרי העידן הדיגיטלי", "translation_ru": "Система образования справляется с вызовами цифровой эпохи", "transliteration": "маарЭхет hа-хинУх митмодЭдет им атгарЭй hа-идАн hа-дигитАли", "audio_url": None, "level_id": 4},
    {"word_id": 729, "hebrew": "כל אחד מתמודד עם קשיים בדרכו שלו", "translation_ru": "Каждый справляется с трудностями по-своему", "transliteration": "коль эхАд митмодЭд им кшийИм бэ-даркО шелО", "audio_url": None, "level_id": 4},
    {"word_id": 729, "hebrew": "התמודדנו עם בעיות תקציביות מורכבות", "translation_ru": "Мы справились со сложными бюджетными проблемами", "transliteration": "hитмодАдну им бэайОт такцивийОт муркавОт", "audio_url": None, "level_id": 4},
]

# ==============================================================================
# LEVEL 5 (C1) — Academic/literary style
# 2-3 sentences per word, ~30 total
# ==============================================================================

LEVEL_5_SENTENCES = [
    # --- 944: להגביל (ограничивать) ---
    {"word_id": 944, "hebrew": "החקיקה החדשה נועדה להגביל את כוחן של חברות הטכנולוגיה", "translation_ru": "Новое законодательство призвано ограничить власть технологических компаний", "transliteration": "hа-хакикА hа-хадашА ноадА лэhагбИль эт кохАн шель хэврОт hа-технолОгия", "audio_url": None, "level_id": 5},
    {"word_id": 944, "hebrew": "אין להגביל את חופש הביטוי ללא הצדקה משפטית מוצקה", "translation_ru": "Нельзя ограничивать свободу слова без убедительного юридического обоснования", "transliteration": "эйн лэhагбИль эт хОфеш hа-битУй лелО hацдакА мишпатИт муцЭкет", "audio_url": None, "level_id": 5},
    {"word_id": 944, "hebrew": "הסכם הסחר מגביל את היבוא של מוצרים מסוימים", "translation_ru": "Торговое соглашение ограничивает импорт определённых товаров", "transliteration": "hэскЭм hа-сахАр магбИль эт hа-йевУ шель муцарИм месуямИм", "audio_url": None, "level_id": 5},
    {"word_id": 944, "hebrew": "המגבלות שהוטלו על התקשורת הגבילו את הדיווח העיתונאי", "translation_ru": "Ограничения, наложенные на СМИ, ограничили журналистскую деятельность", "transliteration": "hа-магбалОт шэ-hутлУ аль hа-тикшОрет hигбИлу эт hа-дивУах hа-итонаИ", "audio_url": None, "level_id": 5},
    {"word_id": 944, "hebrew": "ממשלות רבות מבקשות להגביל את פליטת גזי החממה", "translation_ru": "Многие правительства стремятся ограничить выбросы парниковых газов", "transliteration": "мемшалОт рабОт мевакшОт лэhагбИль эт плитАт газЭй hа-хамамА", "audio_url": None, "level_id": 5},

    # --- 945: להגן (защищать) ---
    {"word_id": 945, "hebrew": "תפקידו של בית המשפט העליון להגן על זכויות הפרט", "translation_ru": "Задача Верховного суда -- защищать права личности", "transliteration": "тафкидО шель бэйт hа-мишпАт hа-эльйОн лэhагЭн аль зхуйОт hа-прАт", "audio_url": None, "level_id": 5},
    {"word_id": 945, "hebrew": "הארגון נלחם להגן על הסביבה מפני זיהום תעשייתי", "translation_ru": "Организация борется за защиту окружающей среды от промышленного загрязнения", "transliteration": "hа-иргУн нилхАм лэhагЭн аль hа-свивА мипнЭй зиhУм таасийатИ", "audio_url": None, "level_id": 5},
    {"word_id": 945, "hebrew": "יש להגן על פרטיותם של אזרחים בעידן הדיגיטלי", "translation_ru": "Необходимо защищать частную жизнь граждан в цифровую эпоху", "transliteration": "йеш лэhагЭн аль пратиютАм шель эзрахИм бэ-идАн hа-дигитАли", "audio_url": None, "level_id": 5},
    {"word_id": 945, "hebrew": "החוק מגן על עובדים מפני פיטורים שרירותיים", "translation_ru": "Закон защищает работников от произвольного увольнения", "transliteration": "hа-хОк мэгЭн аль овдИм мипнЭй питурИм шрирутийИм", "audio_url": None, "level_id": 5},
    {"word_id": 945, "hebrew": "המדינה מחויבת להגן על אוכלוסייתה בעת חירום", "translation_ru": "Государство обязано защищать своё население в чрезвычайных ситуациях", "transliteration": "hа-мединА мехуйЭвет лэhагЭн аль охлусийатА бэ-эт хирУм", "audio_url": None, "level_id": 5},

    # --- 947: להציע (предлагать) ---
    {"word_id": 947, "hebrew": "החוקרים הציעו מודל תיאורטי חדש להסבר התופעה", "translation_ru": "Исследователи предложили новую теоретическую модель для объяснения явления", "transliteration": "hа-хокрИм hицИу модЭль теоретИ хадАш лэ-hэсбЭр hа-тофаА", "audio_url": None, "level_id": 5},
    {"word_id": 947, "hebrew": "הוועדה הציעה רפורמה מקיפה במערכת הבריאות", "translation_ru": "Комиссия предложила комплексную реформу системы здравоохранения", "transliteration": "hа-ваадА hицИа рефОрма макифА бэ-маарЭхет hа-бриУт", "audio_url": None, "level_id": 5},
    {"word_id": 947, "hebrew": "אני מציע לבחון את הנושא מנקודת מבט רב-תחומית", "translation_ru": "Я предлагаю рассмотреть вопрос с междисциплинарной точки зрения", "transliteration": "ани мацИа ливхОн эт hа-носЭ мэ-некудАт мабАт рав-тхумИт", "audio_url": None, "level_id": 5},

    # --- 949: להתחבר (присоединяться) ---
    {"word_id": 949, "hebrew": "ישראל התחברה לרשת התקשורת הבינלאומית בשלב מוקדם", "translation_ru": "Израиль присоединился к международной сети связи на раннем этапе", "transliteration": "исраЭль hитхабрА ла-рЭшет hа-тикшОрет hа-бэйнлеумИт бэ-шалАв мукдАм", "audio_url": None, "level_id": 5},
    {"word_id": 949, "hebrew": "הסטודנטים מתחברים לפלטפורמה האקדמית באמצעות סיסמה", "translation_ru": "Студенты подключаются к академической платформе с помощью пароля", "transliteration": "hа-студЭнтим митхабрИм ла-плАтформа hа-акадЭмит бэ-эмцаУт сисмА", "audio_url": None, "level_id": 5},
    {"word_id": 949, "hebrew": "קשה להתחבר לטקסט שנכתב בשפה ארכאית", "translation_ru": "Сложно проникнуться текстом, написанным на архаичном языке", "transliteration": "кашЭ лэhитхабЭр ла-тЭкст шэ-нихтАв бэ-сафА архАит", "audio_url": None, "level_id": 5},

    # --- 953: להיבנות (строиться) ---
    {"word_id": 953, "hebrew": "השכונה החדשה נבנית על שטח שהיה בעבר חקלאי", "translation_ru": "Новый район строится на территории, которая раньше была сельскохозяйственной", "transliteration": "hа-шхунА hа-хадашА нивнЭт аль шЭтах шэ-hайА бэ-авАр хаклаИ", "audio_url": None, "level_id": 5},
    {"word_id": 953, "hebrew": "האמון בין העמים נבנה לאורך שנים של שיתוף פעולה", "translation_ru": "Доверие между народами строилось на протяжении многих лет сотрудничества", "transliteration": "hа-эмУн бэйн hа-амИм нивнА лэ-Орех шанИм шель шитУф пеулА", "audio_url": None, "level_id": 5},
    {"word_id": 953, "hebrew": "הטיעון נבנה על בסיס ראיות מוצקות", "translation_ru": "Аргументация строилась на основе убедительных доказательств", "transliteration": "hа-тиУн нивнА аль басИс раайОт муцакОт", "audio_url": None, "level_id": 5},

    # --- 954: להיחשב (считаться) ---
    {"word_id": 954, "hebrew": "המחקר הזה נחשב לפריצת דרך בתחום הנוירולוגיה", "translation_ru": "Это исследование считается прорывом в области неврологии", "transliteration": "hа-мэхкАр hа-зЭ нэхшАв ли-прицАт дЭрех бэ-тхУм hа-нейролОгия", "audio_url": None, "level_id": 5},
    {"word_id": 954, "hebrew": "עמנואל קאנט נחשב לאחד הפילוסופים המשפיעים ביותר", "translation_ru": "Иммануил Кант считается одним из самых влиятельных философов", "transliteration": "иманУэль кант нэхшАв лэ-ахАд hа-филосОфим hа-машпиИм бэ-йотЭр", "audio_url": None, "level_id": 5},
    {"word_id": 954, "hebrew": "ההחלטה הזו עלולה להיחשב כתקדים משפטי", "translation_ru": "Это решение может считаться правовым прецедентом", "transliteration": "hа-hахлатА hа-зу алулА лэhэхашЭв кэ-такдИм мишпатИ", "audio_url": None, "level_id": 5},
]

# ==============================================================================
# LEVEL 6 (C2) — Poetry, legal, journalistic styles
# 2-3 sentences per word, ~25 total
# ==============================================================================

LEVEL_6_SENTENCES = [
    # --- 1035: לנצח (побеждать) ---
    {"word_id": 1035, "hebrew": "הספורטאי ניצח את יריבו בתחרות בינלאומית יוקרתית, למרות שנחשב לחלש מבין המתחרים", "translation_ru": "Спортсмен победил соперника в престижном международном соревновании, несмотря на то что считался слабейшим среди участников", "transliteration": "hа-спортАй ницЭах эт яривО бэ-тахарУт бэйнлеумИт йократИт, ламрОт шэ-нэхшАв лэ-халАш мибЭйн hа-митхарИм", "audio_url": None, "level_id": 6},
    {"word_id": 1035, "hebrew": "לנצח אינו רק עניין של כוח — זוהי אמנות הדורשת אסטרטגיה, משמעת ומסירות", "translation_ru": "Побеждать -- это не только вопрос силы; это искусство, требующее стратегии, дисциплины и преданности", "transliteration": "ленацЭах эйнО рак иньЯн шель кОах — зОhи оманУт hа-дорЭшет астратЭгия, масмаАт у-мсирУт", "audio_url": None, "level_id": 6},
    {"word_id": 1035, "hebrew": "\"מי שמנצח את יצרו — הוא הגיבור האמיתי\", כתב בן זומא במשנה", "translation_ru": "\"Кто побеждает своё влечение -- тот истинный герой\", написал Бен Зома в Мишне", "transliteration": "\"ми шэ-менацЭах эт ицрО — hу hа-гибОр hа-амитИ\", катАв бен зомА ба-мишнА", "audio_url": None, "level_id": 6},
    {"word_id": 1035, "hebrew": "צבא קטן ניצח צבא גדול ממנו פי כמה, בזכות תושייה וידע מקומי", "translation_ru": "Малая армия победила армию, в несколько раз превосходящую её, благодаря находчивости и знанию местности", "transliteration": "цавА катАн ницЭах цавА гадОль мимЭну пи кАма, бэ-зхУт тушийА вэ-йЭда мекомИ", "audio_url": None, "level_id": 6},
    {"word_id": 1035, "hebrew": "האמת תמיד תנצח, גם אם דרכה ארוכה ומפותלת", "translation_ru": "Правда всегда победит, даже если её путь долог и извилист", "transliteration": "hа-эмЭт тамИд тенацЭах, гам им даркА арукА у-мефуталЭт", "audio_url": None, "level_id": 6},
    {"word_id": 1035, "hebrew": "בגמר הטורניר, השחקנית ניצחה בשלושה סטים רצופים", "translation_ru": "В финале турнира шахматистка победила в трёх сетах подряд", "transliteration": "бэ-гмАр hа-турнИр, hа-сахканИт ницхА бэ-шлошА сэтИм рецуфИм", "audio_url": None, "level_id": 6},
    {"word_id": 1035, "hebrew": "המפלגה ניצחה בבחירות בזכות תוכנית כלכלית שכנעה את מעמד הביניים", "translation_ru": "Партия победила на выборах благодаря экономической программе, убедившей средний класс", "transliteration": "hа-мифлагА ницхА ба-бхирОт бэ-зхУт тохнИт калкалИт шэ-шихнА эт маамАд hа-бэйнАйим", "audio_url": None, "level_id": 6},

    # --- 1072: להגביר (усиливать) ---
    {"word_id": 1072, "hebrew": "הגופים הביטחוניים הגבירו את הפעילות בעקבות האיום ההולך וגובר", "translation_ru": "Органы безопасности усилили деятельность в связи с нарастающей угрозой", "transliteration": "hа-гуфИм hа-битхонийИм hигбИру эт hа-пеилУт бэ-иквОт hа-иЮм hа-hолЭх вэ-говЭр", "audio_url": None, "level_id": 6},
    {"word_id": 1072, "hebrew": "על התקשורת להגביר את המודעות הציבורית לסוגיות סביבתיות", "translation_ru": "СМИ должны усиливать общественную осведомлённость в экологических вопросах", "transliteration": "аль hа-тикшОрет лэhагбИр эт hа-мудаУт hа-цибурИт лэ-сугийОт свиватийОт", "audio_url": None, "level_id": 6},
    {"word_id": 1072, "hebrew": "המשבר הפוליטי הגביר את חוסר האמון של הציבור במוסדות", "translation_ru": "Политический кризис усилил недоверие общества к институтам", "transliteration": "hа-машбЭр hа-полИти hигбИр эт хОсер hа-эмУн шель hа-цибУр ба-мосадОт", "audio_url": None, "level_id": 6},
    {"word_id": 1072, "hebrew": "כדי להגביר את הביטחון, הותקנו מצלמות בכל רחבי העיר", "translation_ru": "Для усиления безопасности во всём городе были установлены камеры", "transliteration": "кдЭй лэhагбИр эт hа-битахОн, hуткенУ мацлемОт бэ-холь рахавЭй hа-ир", "audio_url": None, "level_id": 6},
    {"word_id": 1072, "hebrew": "השימוש בבינה מלאכותית מגביר את היעילות אך מעלה שאלות אתיות מורכבות", "translation_ru": "Использование искусственного интеллекта усиливает эффективность, но поднимает сложные этические вопросы", "transliteration": "hа-шимУш бэ-бинА малахутИт магбИр эт hа-йеилУт ах маалЭ шеэлОт этийОт муркавОт", "audio_url": None, "level_id": 6},
    {"word_id": 1072, "hebrew": "יש להגביר את המאמצים לצמצם פערים חברתיים-כלכליים", "translation_ru": "Необходимо усилить усилия по сокращению социально-экономических разрывов", "transliteration": "йеш лэhагбИр эт hа-маамацИм лецамцЭм пеарИм хэвратийИм-калкалийИм", "audio_url": None, "level_id": 6},

    # --- 1186: להתגרש (разводиться) ---
    {"word_id": 1186, "hebrew": "בית הדין הרבני הוא הגוף היחיד המוסמך לאשר גירושין בישראל, מציאות שמעוררת ויכוח ציבורי נרחב", "translation_ru": "Раввинский суд является единственным органом, уполномоченным утверждать разводы в Израиле, что вызывает широкую общественную дискуссию", "transliteration": "бэйт hа-дин hа-рабанИ hу hа-гуф hа-яхИд hа-мусмАх лэ-ашЭр гирушИн бэ-исраЭль, мециУт шэ-меорЭрет вику́ах цибурИ нирхАв", "audio_url": None, "level_id": 6},
    {"word_id": 1186, "hebrew": "הזוג התגרש לאחר עשרים שנות נישואין, אך שמר על יחסים תקינים למען ילדיהם", "translation_ru": "Пара развелась после двадцати лет брака, но сохранила нормальные отношения ради детей", "transliteration": "hа-зуг hитгарЭш лэ-ахАр эсрИм шнОт нисуИн, ах шамАр аль яхасИм текинИм лемАан йалдэйhЭм", "audio_url": None, "level_id": 6},
    {"word_id": 1186, "hebrew": "סוגיית הנשים המסורבות גט — נשים שבעליהן מסרבים להתגרש — נותרה אחד האתגרים החמורים ביותר בחברה הישראלית", "translation_ru": "Проблема женщин, которым отказывают в разводе -- чьи мужья отказываются разводиться -- остаётся одной из серьёзнейших проблем израильского общества", "transliteration": "сугийАт hа-нашИм hа-месуравОт гет — нашИм шэ-баалэйhЭн месарвИм лэhитгарЭш — нотрА эхАд hа-атгарИм hа-хамурИм бэ-йотЭр ба-хэврА hа-исраэлИт", "audio_url": None, "level_id": 6},
    {"word_id": 1186, "hebrew": "מחקר סוציולוגי מצא כי שיעורי ההתגרשות עולים ככל שהעצמאות הכלכלית של נשים גוברת", "translation_ru": "Социологическое исследование обнаружило, что уровень разводов растёт по мере усиления экономической независимости женщин", "transliteration": "мэхкАр социолОги мацА ки шиурЭй hа-hитгаршУт олИм кекОль шэ-hа-ацмаУт hа-калкалИт шель нашИм говЭрет", "audio_url": None, "level_id": 6},
    {"word_id": 1186, "hebrew": "בשירתו של יהודה עמיחי, הגירושין מתוארים כ\"רעידת אדמה שקטה שמחלקת את הבית לשניים\"", "translation_ru": "В поэзии Йегуды Амихая развод описывается как \"тихое землетрясение, разделяющее дом надвое\"", "transliteration": "бэ-ширатО шель йеhудА амихАй, hа-гирушИн метоарИм кэ-\"реидАт адамА шкетА шэ-мехалЭкет эт hа-бАйит лэ-шнАйим\"", "audio_url": None, "level_id": 6},
]


def upgrade() -> None:
    # Reset the sequence to avoid conflicts
    op.execute(
        "SELECT setval('example_sentences_id_seq', "
        "GREATEST((SELECT COALESCE(MAX(id), 0) FROM example_sentences), 1))"
    )

    op.bulk_insert(example_sentences_table, LEVEL_1_SENTENCES)
    op.bulk_insert(example_sentences_table, LEVEL_2_SENTENCES)
    op.bulk_insert(example_sentences_table, LEVEL_3_SENTENCES)
    op.bulk_insert(example_sentences_table, LEVEL_4_SENTENCES)
    op.bulk_insert(example_sentences_table, LEVEL_5_SENTENCES)
    op.bulk_insert(example_sentences_table, LEVEL_6_SENTENCES)


def downgrade() -> None:
    op.execute("DELETE FROM example_sentences")
