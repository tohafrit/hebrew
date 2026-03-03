"""Add 20 dialogues for levels 1-2 (10 per level).

L1: cafe, post office, pharmacy, doctor, market, taxi, hotel check-in,
    complaint, pizza order, beach.
L2: job interview, bank, apartment repair, complaint letter, course signup,
    neighbor dispute, wedding, car workshop, travel planning, notary.

Revision ID: 144
Revises: 143
"""

import json
from alembic import op
import sqlalchemy as sa

revision = "144"
down_revision = "143"
branch_labels = None
depends_on = None

_j = lambda d: json.dumps(d, ensure_ascii=False)

dialogues_table = sa.table(
    "dialogues",
    sa.column("level_id", sa.Integer),
    sa.column("title", sa.String),
    sa.column("situation_ru", sa.Text),
    sa.column("lines_json", sa.Text),
    sa.column("vocabulary_json", sa.Text),
    sa.column("audio_url", sa.String),
)

DIALOGUES = [
    # ═══════════════════════════════════════════════════════════════
    # LEVEL 1 — 10 dialogues
    # ═══════════════════════════════════════════════════════════════

    # L1-1: В кафе
    {"level_id": 1, "title": "בבית קפה: הזמנה",
     "situation_ru": "Вы заказываете кофе и пирожное в кафе.",
     "lines_json": _j([
         {"speaker": "מלצר", "text_he": "שלום! מה תרצה להזמין?", "text_ru": "Здравствуйте! Что хотите заказать?"},
         {"speaker": "לקוח", "text_he": "אני רוצה קפה עם חלב, בבקשה.", "text_ru": "Я хочу кофе с молоком, пожалуйста."},
         {"speaker": "מלצר", "text_he": "קפה גדול או קטן?", "text_ru": "Большой кофе или маленький?"},
         {"speaker": "לקוח", "text_he": "גדול, בבקשה. ויש לכם עוגה?", "text_ru": "Большой, пожалуйста. А у вас есть торт?"},
         {"speaker": "מלצר", "text_he": "כן! יש עוגת שוקולד ועוגת גבינה.", "text_ru": "Да! Есть шоколадный торт и чизкейк."},
         {"speaker": "לקוח", "text_he": "עוגת שוקולד, בבקשה.", "text_ru": "Шоколадный, пожалуйста."},
         {"speaker": "מלצר", "text_he": "בסדר. זה ארבעים שקלים.", "text_ru": "Хорошо. Это сорок шекелей."},
         {"speaker": "לקוח", "text_he": "הנה. תודה רבה!", "text_ru": "Вот. Большое спасибо!"},
     ]),
     "vocabulary_json": _j([
         {"word": "מלצר", "translation": "официант", "transliteration": "мельцАр"},
         {"word": "להזמין", "translation": "заказать", "transliteration": "лехазмИн"},
         {"word": "עוגה", "translation": "торт/пирожное", "transliteration": "угА"},
         {"word": "שוקולד", "translation": "шоколад", "transliteration": "шоколАд"},
         {"word": "גבינה", "translation": "сыр/творог", "transliteration": "гвинА"},
     ]),
     "audio_url": None},

    # L1-2: На почте
    {"level_id": 1, "title": "בדואר: לשלוח חבילה",
     "situation_ru": "Вы отправляете посылку на почте.",
     "lines_json": _j([
         {"speaker": "פקיד", "text_he": "שלום, איך אפשר לעזור?", "text_ru": "Здравствуйте, чем могу помочь?"},
         {"speaker": "לקוח", "text_he": "אני רוצה לשלוח חבילה.", "text_ru": "Я хочу отправить посылку."},
         {"speaker": "פקיד", "text_he": "לאן?", "text_ru": "Куда?"},
         {"speaker": "לקוח", "text_he": "לחיפה.", "text_ru": "В Хайфу."},
         {"speaker": "פקיד", "text_he": "מה יש בחבילה?", "text_ru": "Что в посылке?"},
         {"speaker": "לקוח", "text_he": "ספר ומתנה קטנה.", "text_ru": "Книга и маленький подарок."},
         {"speaker": "פקיד", "text_he": "בסדר. זה חמישה עשר שקלים.", "text_ru": "Хорошо. Это пятнадцать шекелей."},
         {"speaker": "לקוח", "text_he": "תודה! מתי החבילה מגיעה?", "text_ru": "Спасибо! Когда посылка приедет?"},
         {"speaker": "פקיד", "text_he": "בעוד יומיים.", "text_ru": "Через два дня."},
     ]),
     "vocabulary_json": _j([
         {"word": "דואר", "translation": "почта", "transliteration": "дОар"},
         {"word": "חבילה", "translation": "посылка", "transliteration": "хавилА"},
         {"word": "לשלוח", "translation": "отправить", "transliteration": "лишлОах"},
         {"word": "מתנה", "translation": "подарок", "transliteration": "матанА"},
         {"word": "פקיד", "translation": "служащий", "transliteration": "пакИд"},
     ]),
     "audio_url": None},

    # L1-3: В аптеке
    {"level_id": 1, "title": "בבית מרקחת: כאב ראש",
     "situation_ru": "Вы покупаете лекарство от головной боли в аптеке.",
     "lines_json": _j([
         {"speaker": "רוקח", "text_he": "שלום, מה קורה?", "text_ru": "Здравствуйте, что случилось?"},
         {"speaker": "לקוח", "text_he": "יש לי כאב ראש חזק.", "text_ru": "У меня сильная головная боль."},
         {"speaker": "רוקח", "text_he": "מזה כמה זמן?", "text_ru": "С какого времени?"},
         {"speaker": "לקוח", "text_he": "מהבוקר.", "text_ru": "С утра."},
         {"speaker": "רוקח", "text_he": "קח אקמול. כדור אחד כל שש שעות.", "text_ru": "Возьмите акамол. Одну таблетку каждые шесть часов."},
         {"speaker": "לקוח", "text_he": "כמה זה עולה?", "text_ru": "Сколько это стоит?"},
         {"speaker": "רוקח", "text_he": "עשרים שקלים.", "text_ru": "Двадцать шекелей."},
         {"speaker": "לקוח", "text_he": "תודה רבה!", "text_ru": "Большое спасибо!"},
     ]),
     "vocabulary_json": _j([
         {"word": "בית מרקחת", "translation": "аптека", "transliteration": "бейт миркАхат"},
         {"word": "כאב ראש", "translation": "головная боль", "transliteration": "кеЭв рош"},
         {"word": "כדור", "translation": "таблетка", "transliteration": "кадУр"},
         {"word": "רוקח", "translation": "фармацевт", "transliteration": "рокЕах"},
         {"word": "חזק", "translation": "сильный", "transliteration": "хазАк"},
     ]),
     "audio_url": None},

    # L1-4: У врача
    {"level_id": 1, "title": "אצל הרופא: בדיקה",
     "situation_ru": "Вы на приёме у врача — жалуетесь на боль в горле.",
     "lines_json": _j([
         {"speaker": "רופא", "text_he": "שלום! מה כואב לך?", "text_ru": "Здравствуйте! Что у вас болит?"},
         {"speaker": "מטופל", "text_he": "כואב לי הגרון כבר יומיים.", "text_ru": "У меня болит горло уже два дня."},
         {"speaker": "רופא", "text_he": "יש לך חום?", "text_ru": "У вас есть температура?"},
         {"speaker": "מטופל", "text_he": "כן, קצת. שלושים ושבע וחצי.", "text_ru": "Да, немного. Тридцать семь с половиной."},
         {"speaker": "רופא", "text_he": "תפתח את הפה. אני רואה שהגרון אדום.", "text_ru": "Откройте рот. Я вижу, что горло красное."},
         {"speaker": "מטופל", "text_he": "מה אני צריך לעשות?", "text_ru": "Что мне нужно делать?"},
         {"speaker": "רופא", "text_he": "לשתות הרבה מים ולנוח. אני כותב לך מרשם.", "text_ru": "Пить много воды и отдыхать. Я выпишу вам рецепт."},
         {"speaker": "מטופל", "text_he": "תודה, רופא!", "text_ru": "Спасибо, доктор!"},
     ]),
     "vocabulary_json": _j([
         {"word": "רופא", "translation": "врач", "transliteration": "рофЕ"},
         {"word": "גרון", "translation": "горло", "transliteration": "гарОн"},
         {"word": "חום", "translation": "температура", "transliteration": "хом"},
         {"word": "מרשם", "translation": "рецепт", "transliteration": "миршАм"},
         {"word": "לנוח", "translation": "отдыхать", "transliteration": "ланУах"},
     ]),
     "audio_url": None},

    # L1-5: На рынке
    {"level_id": 1, "title": "בשוק: ירקות ופירות",
     "situation_ru": "Вы покупаете овощи и фрукты на рынке.",
     "lines_json": _j([
         {"speaker": "מוכר", "text_he": "בואו, בואו! ירקות טריים!", "text_ru": "Подходите, подходите! Свежие овощи!"},
         {"speaker": "קונה", "text_he": "כמה עולים העגבניות?", "text_ru": "Сколько стоят помидоры?"},
         {"speaker": "מוכר", "text_he": "שמונה שקלים לקילו.", "text_ru": "Восемь шекелей за кило."},
         {"speaker": "קונה", "text_he": "יקר! אפשר בשבעה?", "text_ru": "Дорого! Можно за семь?"},
         {"speaker": "מוכר", "text_he": "בשבילך — שבע וחצי. וקח גם מלפפונים!", "text_ru": "Для тебя — семь с половиной. И возьми ещё огурцы!"},
         {"speaker": "קונה", "text_he": "טוב. קילו עגבניות וקילו מלפפונים.", "text_ru": "Хорошо. Кило помидоров и кило огурцов."},
         {"speaker": "מוכר", "text_he": "הנה, בבקשה. חמישה עשר שקלים.", "text_ru": "Вот, пожалуйста. Пятнадцать шекелей."},
     ]),
     "vocabulary_json": _j([
         {"word": "שוק", "translation": "рынок", "transliteration": "шук"},
         {"word": "ירקות", "translation": "овощи", "transliteration": "йеракОт"},
         {"word": "טרי", "translation": "свежий", "transliteration": "тарИ"},
         {"word": "קילו", "translation": "кило", "transliteration": "кИло"},
         {"word": "יקר", "translation": "дорогой", "transliteration": "якАр"},
     ]),
     "audio_url": None},

    # L1-6: Такси
    {"level_id": 1, "title": "במונית: נסיעה לתחנה",
     "situation_ru": "Вы берёте такси до автовокзала.",
     "lines_json": _j([
         {"speaker": "נוסע", "text_he": "שלום! לתחנה המרכזית, בבקשה.", "text_ru": "Здравствуйте! На центральный автовокзал, пожалуйста."},
         {"speaker": "נהג", "text_he": "בסדר. תשים חגורה.", "text_ru": "Хорошо. Пристегните ремень."},
         {"speaker": "נוסע", "text_he": "כמה זמן הנסיעה?", "text_ru": "Сколько времени ехать?"},
         {"speaker": "נהג", "text_he": "עשר דקות, אם אין פקק.", "text_ru": "Десять минут, если нет пробки."},
         {"speaker": "נוסע", "text_he": "כמה זה עולה?", "text_ru": "Сколько это стоит?"},
         {"speaker": "נהג", "text_he": "בערך שלושים שקלים. נוסעים עם מונה.", "text_ru": "Примерно тридцать шекелей. Едем по счётчику."},
         {"speaker": "נוסע", "text_he": "טוב, יאללה!", "text_ru": "Хорошо, поехали!"},
         {"speaker": "נהג", "text_he": "הגענו. שלושים ושניים שקלים.", "text_ru": "Приехали. Тридцать два шекеля."},
     ]),
     "vocabulary_json": _j([
         {"word": "מונית", "translation": "такси", "transliteration": "монИт"},
         {"word": "תחנה מרכזית", "translation": "центральный автовокзал", "transliteration": "таханА мерказИт"},
         {"word": "חגורה", "translation": "ремень безопасности", "transliteration": "хагорА"},
         {"word": "פקק", "translation": "пробка (дорожная)", "transliteration": "пкАк"},
         {"word": "מונה", "translation": "счётчик", "transliteration": "монЕ"},
     ]),
     "audio_url": None},

    # L1-7: Заселение в отель
    {"level_id": 1, "title": "במלון: צ'ק-אין",
     "situation_ru": "Вы заселяетесь в гостиницу.",
     "lines_json": _j([
         {"speaker": "פקיד", "text_he": "שלום, ברוכים הבאים! שם, בבקשה?", "text_ru": "Здравствуйте, добро пожаловать! Имя, пожалуйста?"},
         {"speaker": "אורח", "text_he": "דניאל כהן. יש לי הזמנה לשלושה לילות.", "text_ru": "Даниэль Коэн. У меня бронь на три ночи."},
         {"speaker": "פקיד", "text_he": "כן, אני רואה. חדר 205, קומה שנייה.", "text_ru": "Да, вижу. Комната 205, второй этаж."},
         {"speaker": "אורח", "text_he": "יש מעלית?", "text_ru": "Есть лифт?"},
         {"speaker": "פקיד", "text_he": "כן, שם בצד ימין.", "text_ru": "Да, там справа."},
         {"speaker": "אורח", "text_he": "מתי ארוחת הבוקר?", "text_ru": "Когда завтрак?"},
         {"speaker": "פקיד", "text_he": "משבע עד עשר. הנה המפתח. נסיעה נעימה!", "text_ru": "С семи до десяти. Вот ключ. Приятного отдыха!"},
     ]),
     "vocabulary_json": _j([
         {"word": "מלון", "translation": "гостиница", "transliteration": "малОн"},
         {"word": "הזמנה", "translation": "бронь", "transliteration": "хазманА"},
         {"word": "חדר", "translation": "комната", "transliteration": "хЕдер"},
         {"word": "מעלית", "translation": "лифт", "transliteration": "маалИт"},
         {"word": "ארוחת בוקר", "translation": "завтрак", "transliteration": "арухАт бОкер"},
     ]),
     "audio_url": None},

    # L1-8: Жалоба (шумный сосед)
    {"level_id": 1, "title": "תלונה: השכן רועש",
     "situation_ru": "Вы жалуетесь соседу на шум.",
     "lines_json": _j([
         {"speaker": "שכן א", "text_he": "סליחה, אפשר לדבר?", "text_ru": "Извините, можно поговорить?"},
         {"speaker": "שכן ב", "text_he": "כן, בטח. מה קרה?", "text_ru": "Да, конечно. Что случилось?"},
         {"speaker": "שכן א", "text_he": "המוזיקה מאוד חזקה. אני לא יכול לישון.", "text_ru": "Музыка очень громкая. Я не могу спать."},
         {"speaker": "שכן ב", "text_he": "אוי, סליחה! לא ידעתי.", "text_ru": "Ой, простите! Я не знал."},
         {"speaker": "שכן א", "text_he": "אפשר להנמיך אחרי עשר בלילה?", "text_ru": "Можно потише после десяти вечера?"},
         {"speaker": "שכן ב", "text_he": "בטח! מצטער. זה לא יקרה שוב.", "text_ru": "Конечно! Извините. Это больше не повторится."},
         {"speaker": "שכן א", "text_he": "תודה! לילה טוב.", "text_ru": "Спасибо! Спокойной ночи."},
     ]),
     "vocabulary_json": _j([
         {"word": "שכן", "translation": "сосед", "transliteration": "шахЕн"},
         {"word": "רועש", "translation": "шумный", "transliteration": "роЭш"},
         {"word": "לישון", "translation": "спать", "transliteration": "лишОн"},
         {"word": "להנמיך", "translation": "убавить (звук)", "transliteration": "леханмИх"},
         {"word": "מצטער", "translation": "извините", "transliteration": "мицтаЭр"},
     ]),
     "audio_url": None},

    # L1-9: Заказ пиццы
    {"level_id": 1, "title": "הזמנת פיצה בטלפון",
     "situation_ru": "Вы заказываете пиццу по телефону.",
     "lines_json": _j([
         {"speaker": "עובד", "text_he": "פיצה טובה, שלום!", "text_ru": "Пицца Това, здравствуйте!"},
         {"speaker": "לקוח", "text_he": "שלום, אני רוצה להזמין פיצה.", "text_ru": "Здравствуйте, я хочу заказать пиццу."},
         {"speaker": "עובד", "text_he": "איזה גודל? גדולה או משפחתית?", "text_ru": "Какой размер? Большая или семейная?"},
         {"speaker": "לקוח", "text_he": "גדולה. חצי זיתים וחצי פטריות.", "text_ru": "Большую. Половину с оливками, половину с грибами."},
         {"speaker": "עובד", "text_he": "עם גבינה נוספת?", "text_ru": "С дополнительным сыром?"},
         {"speaker": "לקוח", "text_he": "כן, בבקשה. מה הכתובת שלכם?", "text_ru": "Да, пожалуйста. Какой у вас адрес?"},
         {"speaker": "עובד", "text_he": "אנחנו מביאים! מה הכתובת שלך?", "text_ru": "Мы доставляем! Какой у вас адрес?"},
         {"speaker": "לקוח", "text_he": "רחוב הרצל 15, דירה 3.", "text_ru": "Улица Герцля 15, квартира 3."},
         {"speaker": "עובד", "text_he": "ארבעים וחמישה שקלים. בעוד חצי שעה!", "text_ru": "Сорок пять шекелей. Через полчаса!"},
     ]),
     "vocabulary_json": _j([
         {"word": "פיצה", "translation": "пицца", "transliteration": "пИца"},
         {"word": "זיתים", "translation": "оливки", "transliteration": "зейтИм"},
         {"word": "פטריות", "translation": "грибы", "transliteration": "питриЙот"},
         {"word": "כתובת", "translation": "адрес", "transliteration": "ктОвет"},
         {"word": "משלוח", "translation": "доставка", "transliteration": "мишлОах"},
     ]),
     "audio_url": None},

    # L1-10: На пляже
    {"level_id": 1, "title": "בחוף הים: יום חם",
     "situation_ru": "Вы на пляже в жаркий день.",
     "lines_json": _j([
         {"speaker": "דנה", "text_he": "איזה חם היום! בוא נלך לים.", "text_ru": "Как жарко сегодня! Пойдём на море."},
         {"speaker": "יוסי", "text_he": "רעיון טוב! אתה לוקח מגבת?", "text_ru": "Хорошая идея! Ты берёшь полотенце?"},
         {"speaker": "דנה", "text_he": "כן, ובקבוק מים. אל תשכח קרם שמש!", "text_ru": "Да, и бутылку воды. Не забудь крем от солнца!"},
         {"speaker": "יוסי", "text_he": "המים נראים יפים. נכנסים?", "text_ru": "Вода выглядит красиво. Заходим?"},
         {"speaker": "דנה", "text_he": "רגע, אני שמה את הדברים על החול.", "text_ru": "Секунду, я положу вещи на песок."},
         {"speaker": "יוסי", "text_he": "איזה כיף! המים קרירים!", "text_ru": "Как здорово! Вода прохладная!"},
         {"speaker": "דנה", "text_he": "בוא נשחה עד שם ובחזרה.", "text_ru": "Давай поплаваем туда и обратно."},
         {"speaker": "יוסי", "text_he": "אחר כך נאכל גלידה?", "text_ru": "Потом съедим мороженое?"},
     ]),
     "vocabulary_json": _j([
         {"word": "חוף", "translation": "пляж", "transliteration": "хоф"},
         {"word": "מגבת", "translation": "полотенце", "transliteration": "магЕвет"},
         {"word": "קרם שמש", "translation": "солнцезащитный крем", "transliteration": "крем шЕмеш"},
         {"word": "חול", "translation": "песок", "transliteration": "хол"},
         {"word": "לשחות", "translation": "плавать", "transliteration": "лисхОт"},
         {"word": "גלידה", "translation": "мороженое", "transliteration": "глидА"},
     ]),
     "audio_url": None},

    # ═══════════════════════════════════════════════════════════════
    # LEVEL 2 — 10 dialogues
    # ═══════════════════════════════════════════════════════════════

    # L2-1: Собеседование
    {"level_id": 2, "title": "ראיון עבודה: מזכירה",
     "situation_ru": "Вы пришли на собеседование на должность секретаря в офисе.",
     "lines_json": _j([
         {"speaker": "מנהל", "text_he": "שלום, שבי בבקשה. ספרי לי קצת על עצמך.", "text_ru": "Здравствуйте, садитесь. Расскажите немного о себе."},
         {"speaker": "מועמדת", "text_he": "שמי מיכל. אני בת עשרים ושמונה. גרתי בחיפה.", "text_ru": "Меня зовут Михаль. Мне двадцать восемь. Я жила в Хайфе."},
         {"speaker": "מנהל", "text_he": "יש לך ניסיון במשרד?", "text_ru": "У вас есть опыт офисной работы?"},
         {"speaker": "מועמדת", "text_he": "כן, עבדתי שנתיים כמזכירה בחברת הייטק.", "text_ru": "Да, я два года работала секретарём в хайтек-компании."},
         {"speaker": "מנהל", "text_he": "את יודעת לעבוד עם מחשב?", "text_ru": "Вы умеете работать с компьютером?"},
         {"speaker": "מועמדת", "text_he": "בטח, אקסל, וורד ואאוטלוק.", "text_ru": "Конечно, Excel, Word и Outlook."},
         {"speaker": "מנהל", "text_he": "מצוין. המשרה היא מתשע עד חמש. המשכורת שמונת אלפים שקלים.", "text_ru": "Отлично. Работа с девяти до пяти. Зарплата восемь тысяч шекелей."},
         {"speaker": "מועמדת", "text_he": "נשמע טוב. מתי אני יכולה להתחיל?", "text_ru": "Звучит хорошо. Когда я могу начать?"},
         {"speaker": "מנהל", "text_he": "ביום ראשון הבא. ברוכה הבאה!", "text_ru": "В следующее воскресенье. Добро пожаловать!"},
     ]),
     "vocabulary_json": _j([
         {"word": "ראיון עבודה", "translation": "собеседование", "transliteration": "реайОн аводА"},
         {"word": "ניסיון", "translation": "опыт", "transliteration": "нисайОн"},
         {"word": "משרד", "translation": "офис", "transliteration": "мисрАд"},
         {"word": "משכורת", "translation": "зарплата", "transliteration": "маскОрет"},
         {"word": "מועמדת", "translation": "кандидат (ж.)", "transliteration": "моамЕдет"},
     ]),
     "audio_url": None},

    # L2-2: В банке
    {"level_id": 2, "title": "בבנק: פתיחת חשבון",
     "situation_ru": "Вы открываете банковский счёт.",
     "lines_json": _j([
         {"speaker": "פקידה", "text_he": "שלום, אני יכולה לעזור?", "text_ru": "Здравствуйте, я могу помочь?"},
         {"speaker": "לקוח", "text_he": "כן, אני רוצה לפתוח חשבון בנק.", "text_ru": "Да, я хочу открыть банковский счёт."},
         {"speaker": "פקידה", "text_he": "חשבון עובר ושב או חיסכון?", "text_ru": "Текущий счёт или сберегательный?"},
         {"speaker": "לקוח", "text_he": "עובר ושב, בבקשה. עם כרטיס אשראי.", "text_ru": "Текущий, пожалуйста. С кредитной картой."},
         {"speaker": "פקידה", "text_he": "אני צריכה תעודת זהות ואישור כתובת.", "text_ru": "Мне нужно удостоверение личности и подтверждение адреса."},
         {"speaker": "לקוח", "text_he": "הנה התעודה. ואת האישור אני אביא מחר.", "text_ru": "Вот удостоверение. А подтверждение я принесу завтра."},
         {"speaker": "פקידה", "text_he": "בסדר. תחתום כאן ופה.", "text_ru": "Хорошо. Подпишите здесь и тут."},
         {"speaker": "לקוח", "text_he": "מתי אקבל את הכרטיס?", "text_ru": "Когда я получу карту?"},
         {"speaker": "פקידה", "text_he": "בעוד שבוע בדואר.", "text_ru": "Через неделю по почте."},
     ]),
     "vocabulary_json": _j([
         {"word": "חשבון", "translation": "счёт", "transliteration": "хешбОн"},
         {"word": "כרטיס אשראי", "translation": "кредитная карта", "transliteration": "картИс ашрАй"},
         {"word": "תעודת זהות", "translation": "удостоверение личности", "transliteration": "теудАт зехУт"},
         {"word": "לחתום", "translation": "подписать", "transliteration": "лахтОм"},
         {"word": "חיסכון", "translation": "сбережение", "transliteration": "хисахОн"},
     ]),
     "audio_url": None},

    # L2-3: Ремонт квартиры
    {"level_id": 2, "title": "שיפוץ דירה: שרברב",
     "situation_ru": "Вы вызвали сантехника починить протечку в ванной.",
     "lines_json": _j([
         {"speaker": "דייר", "text_he": "תודה שבאת. יש בעיה בצינור בחדר האמבטיה.", "text_ru": "Спасибо, что пришли. Проблема с трубой в ванной."},
         {"speaker": "שרברב", "text_he": "בוא נראה. כמה זמן זה כבר נוזל?", "text_ru": "Давайте посмотрим. Сколько времени уже течёт?"},
         {"speaker": "דייר", "text_he": "מאתמול בלילה. כל הרצפה רטובה.", "text_ru": "Со вчерашнего вечера. Весь пол мокрый."},
         {"speaker": "שרברב", "text_he": "אני רואה. צריך להחליף את הברז. זה ישן.", "text_ru": "Вижу. Нужно заменить кран. Он старый."},
         {"speaker": "דייר", "text_he": "כמה זה יעלה?", "text_ru": "Сколько это будет стоить?"},
         {"speaker": "שרברב", "text_he": "שלוש מאות שקלים עם חומרים.", "text_ru": "Триста шекелей с материалами."},
         {"speaker": "דייר", "text_he": "בסדר. כמה זמן לוקח?", "text_ru": "Хорошо. Сколько времени займёт?"},
         {"speaker": "שרברב", "text_he": "שעה בערך. אתחיל עכשיו.", "text_ru": "Примерно час. Начну сейчас."},
     ]),
     "vocabulary_json": _j([
         {"word": "שרברב", "translation": "сантехник", "transliteration": "шравлАв"},
         {"word": "צינור", "translation": "труба", "transliteration": "цинОр"},
         {"word": "נוזל", "translation": "течёт/жидкость", "transliteration": "нозЕль"},
         {"word": "ברז", "translation": "кран", "transliteration": "бЕрез"},
         {"word": "להחליף", "translation": "заменить", "transliteration": "лехахлИф"},
     ]),
     "audio_url": None},

    # L2-4: Рекламация
    {"level_id": 2, "title": "רקלמציה: מוצר פגום",
     "situation_ru": "Вы возвращаете бракованный товар в магазин.",
     "lines_json": _j([
         {"speaker": "לקוח", "text_he": "סליחה, קניתי את הטוסטר הזה שלשום והוא לא עובד.", "text_ru": "Извините, я купил этот тостер позавчера, и он не работает."},
         {"speaker": "מוכרת", "text_he": "יש לך קבלה?", "text_ru": "У вас есть чек?"},
         {"speaker": "לקוח", "text_he": "כן, הנה.", "text_ru": "Да, вот."},
         {"speaker": "מוכרת", "text_he": "מה בדיוק הבעיה?", "text_ru": "Какая именно проблема?"},
         {"speaker": "לקוח", "text_he": "הוא לא מתחמם. לחצתי על כל הכפתורים.", "text_ru": "Он не нагревается. Я нажимал на все кнопки."},
         {"speaker": "מוכרת", "text_he": "אתה רוצה החלפה או החזר כספי?", "text_ru": "Хотите замену или возврат денег?"},
         {"speaker": "לקוח", "text_he": "החלפה, בבקשה. אותו דגם.", "text_ru": "Замену, пожалуйста. Ту же модель."},
         {"speaker": "מוכרת", "text_he": "בסדר, הנה טוסטר חדש. בדוק אותו בבית.", "text_ru": "Хорошо, вот новый тостер. Проверьте его дома."},
     ]),
     "vocabulary_json": _j([
         {"word": "קבלה", "translation": "чек/квитанция", "transliteration": "кабалА"},
         {"word": "פגום", "translation": "бракованный", "transliteration": "пагУм"},
         {"word": "החלפה", "translation": "замена", "transliteration": "хахлафА"},
         {"word": "החזר כספי", "translation": "возврат денег", "transliteration": "хехзЕр каспИ"},
         {"word": "דגם", "translation": "модель", "transliteration": "дЕгем"},
     ]),
     "audio_url": None},

    # L2-5: Запись на курс
    {"level_id": 2, "title": "הרשמה לקורס עברית",
     "situation_ru": "Вы записываетесь на курс иврита в ульпане.",
     "lines_json": _j([
         {"speaker": "מזכירה", "text_he": "שלום! רוצה להירשם לקורס?", "text_ru": "Здравствуйте! Хотите записаться на курс?"},
         {"speaker": "תלמיד", "text_he": "כן. אני רוצה ללמוד עברית. אני מתחיל.", "text_ru": "Да. Я хочу учить иврит. Я начинающий."},
         {"speaker": "מזכירה", "text_he": "יש לנו קורס לרמה א׳. שלוש פעמים בשבוע.", "text_ru": "У нас есть курс для уровня Алеф. Три раза в неделю."},
         {"speaker": "תלמיד", "text_he": "באיזה ימים?", "text_ru": "В какие дни?"},
         {"speaker": "מזכירה", "text_he": "ראשון, שלישי וחמישי. מארבע עד שש.", "text_ru": "Воскресенье, вторник и четверг. С четырёх до шести."},
         {"speaker": "תלמיד", "text_he": "מתאים לי. כמה עולה?", "text_ru": "Мне подходит. Сколько стоит?"},
         {"speaker": "מזכירה", "text_he": "אלף שקלים לשלושה חודשים. כולל ספרים.", "text_ru": "Тысяча шекелей за три месяца. Включая книги."},
         {"speaker": "תלמיד", "text_he": "מצוין! אני נרשם.", "text_ru": "Отлично! Я записываюсь."},
     ]),
     "vocabulary_json": _j([
         {"word": "הרשמה", "translation": "регистрация/запись", "transliteration": "хершамА"},
         {"word": "קורס", "translation": "курс", "transliteration": "курс"},
         {"word": "רמה", "translation": "уровень", "transliteration": "рамА"},
         {"word": "מתחיל", "translation": "начинающий", "transliteration": "матхИль"},
         {"word": "כולל", "translation": "включая", "transliteration": "колЕль"},
     ]),
     "audio_url": None},

    # L2-6: Спор с соседом
    {"level_id": 2, "title": "ריב עם השכן: חנייה",
     "situation_ru": "Вы спорите с соседом, который занял ваше парковочное место.",
     "lines_json": _j([
         {"speaker": "שכן א", "text_he": "סליחה, אתה חונה במקום שלי.", "text_ru": "Извините, вы паркуетесь на моём месте."},
         {"speaker": "שכן ב", "text_he": "מה? זה לא שלך. אין פה שם.", "text_ru": "Что? Это не ваше. Тут нет имени."},
         {"speaker": "שכן א", "text_he": "יש! תסתכל — כתוב דירה 7. זאת הדירה שלי.", "text_ru": "Есть! Посмотрите — написано квартира 7. Это моя квартира."},
         {"speaker": "שכן ב", "text_he": "אה, סליחה. לא שמתי לב.", "text_ru": "А, извините. Не заметил."},
         {"speaker": "שכן א", "text_he": "אפשר להזיז את האוטו?", "text_ru": "Можно передвинуть машину?"},
         {"speaker": "שכן ב", "text_he": "כן, רגע. אני מזיז עכשיו. באמת סליחה.", "text_ru": "Да, секунду. Передвигаю. Правда, извините."},
         {"speaker": "שכן א", "text_he": "תודה. בפעם הבאה תשים לב, בבקשה.", "text_ru": "Спасибо. В следующий раз обратите внимание, пожалуйста."},
     ]),
     "vocabulary_json": _j([
         {"word": "חנייה", "translation": "парковка", "transliteration": "ханайА"},
         {"word": "לחנות", "translation": "парковаться", "transliteration": "лаханОт"},
         {"word": "להזיז", "translation": "передвигать", "transliteration": "лехазИз"},
         {"word": "לשים לב", "translation": "обратить внимание", "transliteration": "ласИм лев"},
         {"word": "מקום", "translation": "место", "transliteration": "макОм"},
     ]),
     "audio_url": None},

    # L2-7: На свадьбе
    {"level_id": 2, "title": "בחתונה: מזל טוב!",
     "situation_ru": "Вы на свадьбе друга и общаетесь с другими гостями.",
     "lines_json": _j([
         {"speaker": "אורח א", "text_he": "שלום! את מכירה את החתן או את הכלה?", "text_ru": "Привет! Вы знакомы с женихом или невестой?"},
         {"speaker": "אורחת ב", "text_he": "את הכלה. אנחנו חברות מהצבא.", "text_ru": "С невестой. Мы подруги по армии."},
         {"speaker": "אורח א", "text_he": "אני חבר של דוד מהעבודה. איזה חתונה יפה!", "text_ru": "Я друг Давида по работе. Какая красивая свадьба!"},
         {"speaker": "אורחת ב", "text_he": "כן, המקום נהדר. ואיזה אוכל!", "text_ru": "Да, место великолепное. И какая еда!"},
         {"speaker": "אורח א", "text_he": "בוא נלך לאחל מזל טוב.", "text_ru": "Давайте пойдём поздравим."},
         {"speaker": "אורחת ב", "text_he": "כן! הם נראים כל כך שמחים!", "text_ru": "Да! Они выглядят такими счастливыми!"},
         {"speaker": "אורח א", "text_he": "מזל טוב, דוד ומיכל! שתהיה לכם חיים יפים!", "text_ru": "Мазаль тов, Давид и Михаль! Пусть у вас будет прекрасная жизнь!"},
         {"speaker": "חתן", "text_he": "תודה רבה! בואו לרקוד!", "text_ru": "Большое спасибо! Пойдёмте танцевать!"},
     ]),
     "vocabulary_json": _j([
         {"word": "חתונה", "translation": "свадьба", "transliteration": "хатунА"},
         {"word": "חתן", "translation": "жених", "transliteration": "хатАн"},
         {"word": "כלה", "translation": "невеста", "transliteration": "калА"},
         {"word": "לאחל", "translation": "пожелать", "transliteration": "леахЕль"},
         {"word": "לרקוד", "translation": "танцевать", "transliteration": "лиркОд"},
     ]),
     "audio_url": None},

    # L2-8: В мастерской (автосервис)
    {"level_id": 2, "title": "במוסך: תקלה ברכב",
     "situation_ru": "Вы привезли машину в автосервис.",
     "lines_json": _j([
         {"speaker": "מכונאי", "text_he": "שלום, מה הבעיה?", "text_ru": "Здравствуйте, какая проблема?"},
         {"speaker": "נהג", "text_he": "המנוע עושה רעש מוזר. ויש אור אדום בלוח.", "text_ru": "Мотор издаёт странный шум. И красная лампочка на панели."},
         {"speaker": "מכונאי", "text_he": "מתי התחיל?", "text_ru": "Когда началось?"},
         {"speaker": "נהג", "text_he": "לפני יומיים. גם הבלמים לא טובים.", "text_ru": "Два дня назад. И тормоза не в порядке."},
         {"speaker": "מכונאי", "text_he": "אני אבדוק. תשאיר את המפתח.", "text_ru": "Я проверю. Оставьте ключ."},
         {"speaker": "נהג", "text_he": "כמה זמן ייקח?", "text_ru": "Сколько времени займёт?"},
         {"speaker": "מכונאי", "text_he": "אני צריך לבדוק. אתקשר אליך בצהריים.", "text_ru": "Мне нужно проверить. Позвоню вам днём."},
         {"speaker": "נהג", "text_he": "בסדר. הנה המספר שלי.", "text_ru": "Хорошо. Вот мой номер."},
     ]),
     "vocabulary_json": _j([
         {"word": "מוסך", "translation": "автосервис", "transliteration": "мусАх"},
         {"word": "מנוע", "translation": "мотор/двигатель", "transliteration": "манОа"},
         {"word": "בלמים", "translation": "тормоза", "transliteration": "баламИм"},
         {"word": "מכונאי", "translation": "механик", "transliteration": "мехонАй"},
         {"word": "לבדוק", "translation": "проверить", "transliteration": "ливдОк"},
     ]),
     "audio_url": None},

    # L2-9: Планирование путешествия
    {"level_id": 2, "title": "תכנון טיול לאילת",
     "situation_ru": "Вы с другом планируете поездку в Эйлат.",
     "lines_json": _j([
         {"speaker": "רונית", "text_he": "בוא נסע לאילת בחופש! מה דעתך?", "text_ru": "Поехали в Эйлат на каникулах! Что думаешь?"},
         {"speaker": "אלון", "text_he": "רעיון מעולה! מתי?", "text_ru": "Прекрасная идея! Когда?"},
         {"speaker": "רונית", "text_he": "בשבוע הבא? משני עד חמישי.", "text_ru": "На следующей неделе? С понедельника до четверга."},
         {"speaker": "אלון", "text_he": "שלושה לילות — מושלם. נוסעים ברכבת או באוטו?", "text_ru": "Три ночи — идеально. Едем на поезде или на машине?"},
         {"speaker": "רונית", "text_he": "באוטו. ארבע שעות, אבל יותר נוח.", "text_ru": "На машине. Четыре часа, но удобнее."},
         {"speaker": "אלון", "text_he": "צריך להזמין מלון. יש משהו לא יקר?", "text_ru": "Нужно забронировать отель. Есть что-нибудь недорогое?"},
         {"speaker": "רונית", "text_he": "מצאתי אכסנייה ב-200 שקלים ללילה.", "text_ru": "Я нашла хостел за 200 шекелей за ночь."},
         {"speaker": "אלון", "text_he": "מעולה! מזמינים. אני כל כך רוצה לצלול!", "text_ru": "Отлично! Бронируем. Я так хочу понырять!"},
     ]),
     "vocabulary_json": _j([
         {"word": "טיול", "translation": "поездка/поход", "transliteration": "тиУль"},
         {"word": "חופש", "translation": "каникулы/отпуск", "transliteration": "хОфеш"},
         {"word": "להזמין", "translation": "забронировать", "transliteration": "лехазмИн"},
         {"word": "אכסנייה", "translation": "хостел", "transliteration": "ахсанийА"},
         {"word": "לצלול", "translation": "нырять", "transliteration": "лицлОль"},
     ]),
     "audio_url": None},

    # L2-10: У нотариуса
    {"level_id": 2, "title": "אצל עורך דין: חוזה שכירות",
     "situation_ru": "Вы у адвоката для подписания договора аренды квартиры.",
     "lines_json": _j([
         {"speaker": "עו״ד", "text_he": "שלום. אתם מוכנים לחתום על החוזה?", "text_ru": "Здравствуйте. Вы готовы подписать договор?"},
         {"speaker": "שוכר", "text_he": "כמעט. יש לי כמה שאלות.", "text_ru": "Почти. У меня несколько вопросов."},
         {"speaker": "עו״ד", "text_he": "בבקשה, שאל.", "text_ru": "Пожалуйста, спрашивайте."},
         {"speaker": "שוכר", "text_he": "מה קורה אם משהו נשבר בדירה?", "text_ru": "Что будет, если что-то сломается в квартире?"},
         {"speaker": "עו״ד", "text_he": "לפי החוזה, תיקונים גדולים — על בעל הדירה. קטנים — עליך.", "text_ru": "По договору, крупный ремонт — за хозяином. Мелкий — за вами."},
         {"speaker": "שוכר", "text_he": "ומה לגבי הפיקדון?", "text_ru": "А что насчёт залога?"},
         {"speaker": "עו״ד", "text_he": "שלושת אלפים שקלים. מוחזרים בסוף השכירות.", "text_ru": "Три тысячи шекелей. Возвращаются в конце аренды."},
         {"speaker": "שוכר", "text_he": "בסדר. אני חותם.", "text_ru": "Хорошо. Подписываю."},
     ]),
     "vocabulary_json": _j([
         {"word": "חוזה", "translation": "договор", "transliteration": "хозЕ"},
         {"word": "שכירות", "translation": "аренда", "transliteration": "схирУт"},
         {"word": "פיקדון", "translation": "залог/депозит", "transliteration": "пикадОн"},
         {"word": "בעל דירה", "translation": "хозяин квартиры", "transliteration": "бАаль дирА"},
         {"word": "תיקון", "translation": "ремонт/починка", "transliteration": "тикУн"},
     ]),
     "audio_url": None},
]

TITLE_LIST = [d["title"] for d in DIALOGUES]


def upgrade() -> None:
    op.execute(
        "SELECT setval('dialogues_id_seq', "
        "GREATEST(COALESCE((SELECT MAX(id) FROM dialogues), 0), 1))"
    )
    op.bulk_insert(dialogues_table, DIALOGUES)
    print(f"Inserted {len(DIALOGUES)} dialogues for L1-L2")


def downgrade() -> None:
    for title in TITLE_LIST:
        op.execute(
            sa.text("DELETE FROM dialogues WHERE title = :t"),
            {"t": title},
        )
