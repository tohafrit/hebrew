"""Add 40 dialogues for levels 1-2 (20 each, bringing totals to 30 per level)

Revision ID: 088
Revises: 087
Create Date: 2026-03-02

"""
from typing import Sequence, Union
import json

from alembic import op
import sqlalchemy as sa

revision: str = "088"
down_revision: Union[str, None] = "087"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ══════════════════════════════════════════════════════════════════════════════
# Table reference
# ══════════════════════════════════════════════════════════════════════════════

dialogues_table = sa.table(
    "dialogues",
    sa.column("level_id", sa.Integer),
    sa.column("title", sa.String),
    sa.column("situation_ru", sa.Text),
    sa.column("lines_json", sa.Text),
    sa.column("vocabulary_json", sa.Text),
    sa.column("audio_url", sa.String),
)

# ══════════════════════════════════════════════════════════════════════════════
# Level 1: 20 new dialogues (4-6 lines, 5-8 vocab)
# ══════════════════════════════════════════════════════════════════════════════

L1_DIALOGUES = [
    # 1. В магазине: покупка фруктов
    {
        "level_id": 1,
        "title": "В магазине: покупка фруктов",
        "situation_ru": "Вы покупаете фрукты на рынке.",
        "lines_json": json.dumps([
            {"speaker": "מוכר", "text_he": "בוקר טוב! מה אתה רוצה?", "text_ru": "Доброе утро! Что вы хотите?"},
            {"speaker": "לקוח", "text_he": "אני רוצה תפוחים ובננות, בבקשה.", "text_ru": "Я хочу яблоки и бананы, пожалуйста."},
            {"speaker": "מוכר", "text_he": "כמה תפוחים?", "text_ru": "Сколько яблок?"},
            {"speaker": "לקוח", "text_he": "חמישה תפוחים ושלוש בננות.", "text_ru": "Пять яблок и три банана."},
            {"speaker": "מוכר", "text_he": "הנה. זה עשרים שקלים.", "text_ru": "Вот. Это двадцать шекелей."},
            {"speaker": "לקוח", "text_he": "תודה רבה! להתראות.", "text_ru": "Большое спасибо! До свидания."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "תפוח", "translation": "яблоко", "transliteration": "тапУах"},
            {"word": "בננה", "translation": "банан", "transliteration": "банАна"},
            {"word": "שקל", "translation": "шекель", "transliteration": "шЕкель"},
            {"word": "כמה", "translation": "сколько", "transliteration": "кАма"},
            {"word": "מוכר", "translation": "продавец", "transliteration": "мохЕр"},
            {"word": "לקוח", "translation": "покупатель", "transliteration": "лакОах"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 2. В школе: на уроке математики
    {
        "level_id": 1,
        "title": "В школе: на уроке математики",
        "situation_ru": "Вы на уроке математики и спрашиваете учителя.",
        "lines_json": json.dumps([
            {"speaker": "מורה", "text_he": "בוקר טוב, ילדים! פתחו את המחברות.", "text_ru": "Доброе утро, дети! Откройте тетради."},
            {"speaker": "תלמיד", "text_he": "מורה, אני לא מבין את התרגיל.", "text_ru": "Учитель, я не понимаю упражнение."},
            {"speaker": "מורה", "text_he": "איזה תרגיל? תראה לי.", "text_ru": "Какое упражнение? Покажи мне."},
            {"speaker": "תלמיד", "text_he": "תרגיל מספר שלוש.", "text_ru": "Упражнение номер три."},
            {"speaker": "מורה", "text_he": "אה, זה קל! שלוש ועוד ארבע זה שבע.", "text_ru": "А, это легко! Три плюс четыре — это семь."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "מורה", "translation": "учитель", "transliteration": "морЕ"},
            {"word": "תרגיל", "translation": "упражнение", "transliteration": "таргИль"},
            {"word": "מחברת", "translation": "тетрадь", "transliteration": "махбЕрет"},
            {"word": "מספר", "translation": "номер", "transliteration": "миспАр"},
            {"word": "קל", "translation": "легко", "transliteration": "каль"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 3. Телефонный звонок другу
    {
        "level_id": 1,
        "title": "Телефонный звонок другу",
        "situation_ru": "Вы звоните другу по телефону.",
        "lines_json": json.dumps([
            {"speaker": "דוד", "text_he": "הלו?", "text_ru": "Алло?"},
            {"speaker": "יוסי", "text_he": "הלו, דוד? זה יוסי. מה שלומך?", "text_ru": "Алло, Давид? Это Йоси. Как дела?"},
            {"speaker": "דוד", "text_he": "הי, יוסי! אני בסדר, תודה. ואתה?", "text_ru": "Привет, Йоси! Я в порядке, спасибо. А ты?"},
            {"speaker": "יוסי", "text_he": "גם אני בסדר. אתה רוצה לבוא היום?", "text_ru": "Я тоже в порядке. Ты хочешь прийти сегодня?"},
            {"speaker": "דוד", "text_he": "כן, מתי?", "text_ru": "Да, когда?"},
            {"speaker": "יוסי", "text_he": "בשעה ארבע. בסדר?", "text_ru": "В четыре часа. Ладно?"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "הלו", "translation": "алло", "transliteration": "алО"},
            {"word": "שלום", "translation": "привет / мир", "transliteration": "шалОм"},
            {"word": "בסדר", "translation": "в порядке", "transliteration": "бесЕдер"},
            {"word": "היום", "translation": "сегодня", "transliteration": "hайОм"},
            {"word": "שעה", "translation": "час", "transliteration": "шаА"},
            {"word": "מתי", "translation": "когда", "transliteration": "матАй"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 4. Встреча с соседом
    {
        "level_id": 1,
        "title": "Встреча с соседом на лестничной клетке",
        "situation_ru": "Вы встречаете нового соседа у входа в дом.",
        "lines_json": json.dumps([
            {"speaker": "שכן", "text_he": "שלום! אתה גר פה?", "text_ru": "Привет! Ты живёшь здесь?"},
            {"speaker": "אתה", "text_he": "כן, אני גר בקומה שנייה. ואתה?", "text_ru": "Да, я живу на втором этаже. А ты?"},
            {"speaker": "שכן", "text_he": "אני גר בקומה שלישית. אני דני.", "text_ru": "Я живу на третьем этаже. Я Дани."},
            {"speaker": "אתה", "text_he": "נעים מאוד! אני אלכס.", "text_ru": "Очень приятно! Я Алекс."},
            {"speaker": "שכן", "text_he": "מאיפה אתה, אלכס?", "text_ru": "Откуда ты, Алекс?"},
            {"speaker": "אתה", "text_he": "אני מרוסיה. אני כאן חודש.", "text_ru": "Я из России. Я здесь месяц."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "שכן", "translation": "сосед", "transliteration": "шахЕн"},
            {"word": "קומה", "translation": "этаж", "transliteration": "комА"},
            {"word": "נעים מאוד", "translation": "очень приятно", "transliteration": "наИм меОд"},
            {"word": "חודש", "translation": "месяц", "transliteration": "хОдеш"},
            {"word": "כאן", "translation": "здесь", "transliteration": "кан"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 5. В банке: открытие счёта
    {
        "level_id": 1,
        "title": "В банке: открытие счёта",
        "situation_ru": "Вы хотите открыть счёт в банке.",
        "lines_json": json.dumps([
            {"speaker": "פקיד", "text_he": "שלום, במה אני יכול לעזור?", "text_ru": "Здравствуйте, чем я могу помочь?"},
            {"speaker": "לקוח", "text_he": "אני רוצה לפתוח חשבון, בבקשה.", "text_ru": "Я хочу открыть счёт, пожалуйста."},
            {"speaker": "פקיד", "text_he": "בוודאי. יש לך תעודת זהות?", "text_ru": "Конечно. У вас есть удостоверение личности?"},
            {"speaker": "לקוח", "text_he": "כן, הנה התעודה שלי.", "text_ru": "Да, вот моё удостоверение."},
            {"speaker": "פקיד", "text_he": "תודה. תחתום פה, בבקשה.", "text_ru": "Спасибо. Подпишите здесь, пожалуйста."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "בנק", "translation": "банк", "transliteration": "банк"},
            {"word": "חשבון", "translation": "счёт", "transliteration": "хешбОн"},
            {"word": "תעודת זהות", "translation": "удостоверение личности", "transliteration": "теудАт зеhУт"},
            {"word": "לפתוח", "translation": "открыть", "transliteration": "лифтОах"},
            {"word": "לחתום", "translation": "подписать", "transliteration": "лахтОм"},
            {"word": "פקיד", "translation": "служащий", "transliteration": "пакИд"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 6. В такси
    {
        "level_id": 1,
        "title": "В такси",
        "situation_ru": "Вы едете на такси в центр города.",
        "lines_json": json.dumps([
            {"speaker": "נוסע", "text_he": "שלום! אני צריך לנסוע למרכז העיר.", "text_ru": "Привет! Мне нужно ехать в центр города."},
            {"speaker": "נהג", "text_he": "בסדר. לאיזה רחוב?", "text_ru": "Ладно. На какую улицу?"},
            {"speaker": "נוסע", "text_he": "רחוב דיזנגוף, מספר עשר.", "text_ru": "Улица Дизенгоф, номер десять."},
            {"speaker": "נהג", "text_he": "טוב. זה בערך עשר דקות.", "text_ru": "Хорошо. Это примерно десять минут."},
            {"speaker": "נוסע", "text_he": "כמה זה עולה?", "text_ru": "Сколько это стоит?"},
            {"speaker": "נהג", "text_he": "שלושים שקלים.", "text_ru": "Тридцать шекелей."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "נהג", "translation": "водитель", "transliteration": "наhАг"},
            {"word": "נוסע", "translation": "пассажир", "transliteration": "носЕа"},
            {"word": "רחוב", "translation": "улица", "transliteration": "рехОв"},
            {"word": "מרכז", "translation": "центр", "transliteration": "меркАз"},
            {"word": "דקה", "translation": "минута", "transliteration": "дакА"},
            {"word": "עולה", "translation": "стоит", "transliteration": "олЕ"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 7. В аптеке
    {
        "level_id": 1,
        "title": "В аптеке",
        "situation_ru": "Вы покупаете лекарство в аптеке.",
        "lines_json": json.dumps([
            {"speaker": "לקוח", "text_he": "שלום, יש לי כאב ראש.", "text_ru": "Здравствуйте, у меня болит голова."},
            {"speaker": "רוקח", "text_he": "יש לך מרשם מרופא?", "text_ru": "У вас есть рецепт от врача?"},
            {"speaker": "לקוח", "text_he": "לא, אין לי מרשם.", "text_ru": "Нет, у меня нет рецепта."},
            {"speaker": "רוקח", "text_he": "בסדר. קח אקמול. כדור אחד כל שש שעות.", "text_ru": "Ладно. Возьмите акамол. Одна таблетка каждые шесть часов."},
            {"speaker": "לקוח", "text_he": "תודה. כמה זה עולה?", "text_ru": "Спасибо. Сколько это стоит?"},
            {"speaker": "רוקח", "text_he": "חמישה עשר שקלים.", "text_ru": "Пятнадцать шекелей."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "רוקח", "translation": "фармацевт", "transliteration": "рокЕах"},
            {"word": "כאב ראש", "translation": "головная боль", "transliteration": "кеЭв рош"},
            {"word": "מרשם", "translation": "рецепт", "transliteration": "миршАм"},
            {"word": "כדור", "translation": "таблетка", "transliteration": "кадУр"},
            {"word": "רופא", "translation": "врач", "transliteration": "рофЕ"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 8. В прачечной
    {
        "level_id": 1,
        "title": "В прачечной",
        "situation_ru": "Вы отдаёте вещи в прачечную.",
        "lines_json": json.dumps([
            {"speaker": "לקוח", "text_he": "שלום, אני רוצה לכבס בגדים.", "text_ru": "Здравствуйте, я хочу постирать одежду."},
            {"speaker": "עובד", "text_he": "כמה פריטים יש לך?", "text_ru": "Сколько у вас вещей?"},
            {"speaker": "לקוח", "text_he": "חמש חולצות ושני מכנסיים.", "text_ru": "Пять рубашек и двое брюк."},
            {"speaker": "עובד", "text_he": "זה יהיה מוכן ביום שלישי.", "text_ru": "Будет готово во вторник."},
            {"speaker": "לקוח", "text_he": "תודה רבה!", "text_ru": "Большое спасибо!"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "לכבס", "translation": "стирать", "transliteration": "лехабЕс"},
            {"word": "בגדים", "translation": "одежда", "transliteration": "бгадИм"},
            {"word": "חולצה", "translation": "рубашка", "transliteration": "хульцА"},
            {"word": "מכנסיים", "translation": "брюки", "transliteration": "михнасАим"},
            {"word": "מוכן", "translation": "готов", "transliteration": "мухАн"},
            {"word": "פריט", "translation": "предмет / вещь", "transliteration": "прИт"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 9. На детской площадке
    {
        "level_id": 1,
        "title": "На детской площадке",
        "situation_ru": "Вы разговариваете с другим родителем на детской площадке.",
        "lines_json": json.dumps([
            {"speaker": "אמא", "text_he": "שלום! הילד שלך חמוד. מה שמו?", "text_ru": "Привет! Ваш ребёнок милый. Как его зовут?"},
            {"speaker": "אבא", "text_he": "תודה! שמו דניאל. הוא בן שלוש.", "text_ru": "Спасибо! Его зовут Даниэль. Ему три года."},
            {"speaker": "אמא", "text_he": "הבת שלי מיכל. היא בת ארבע.", "text_ru": "Мою дочь зовут Михаль. Ей четыре года."},
            {"speaker": "אבא", "text_he": "הם יכולים לשחק ביחד!", "text_ru": "Они могут играть вместе!"},
            {"speaker": "אמא", "text_he": "כן, רעיון טוב!", "text_ru": "Да, хорошая идея!"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "ילד", "translation": "ребёнок / мальчик", "transliteration": "йЕлед"},
            {"word": "בת", "translation": "дочь", "transliteration": "бат"},
            {"word": "חמוד", "translation": "милый", "transliteration": "хамУд"},
            {"word": "לשחק", "translation": "играть", "transliteration": "лесахЕк"},
            {"word": "ביחד", "translation": "вместе", "transliteration": "бейАхад"},
            {"word": "רעיון", "translation": "идея", "transliteration": "раайОн"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 10. День рождения
    {
        "level_id": 1,
        "title": "День рождения",
        "situation_ru": "Вы поздравляете друга с днём рождения.",
        "lines_json": json.dumps([
            {"speaker": "חבר", "text_he": "יום הולדת שמח, דוד!", "text_ru": "С днём рождения, Давид!"},
            {"speaker": "דוד", "text_he": "תודה רבה! בוא, יש עוגה.", "text_ru": "Большое спасибо! Заходи, есть торт."},
            {"speaker": "חבר", "text_he": "הנה, מתנה בשבילך!", "text_ru": "Вот, подарок для тебя!"},
            {"speaker": "דוד", "text_he": "וואו, תודה! מה זה?", "text_ru": "Вау, спасибо! Что это?"},
            {"speaker": "חבר", "text_he": "זה ספר חדש. אני מקווה שתאהב.", "text_ru": "Это новая книга. Надеюсь, тебе понравится."},
            {"speaker": "דוד", "text_he": "אני אוהב ספרים! תודה, חבר!", "text_ru": "Я люблю книги! Спасибо, друг!"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "יום הולדת", "translation": "день рождения", "transliteration": "йом hулЕдет"},
            {"word": "עוגה", "translation": "торт", "transliteration": "угА"},
            {"word": "מתנה", "translation": "подарок", "transliteration": "матанА"},
            {"word": "ספר", "translation": "книга", "transliteration": "сЕфер"},
            {"word": "לאהוב", "translation": "любить", "transliteration": "лееhОв"},
            {"word": "חבר", "translation": "друг", "transliteration": "хавЕр"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 11. В кафе: заказ завтрака
    {
        "level_id": 1,
        "title": "В кафе: заказ завтрака",
        "situation_ru": "Вы заказываете завтрак в кафе.",
        "lines_json": json.dumps([
            {"speaker": "מלצר", "text_he": "בוקר טוב! מה תרצה לשתות?", "text_ru": "Доброе утро! Что вы хотите выпить?"},
            {"speaker": "לקוח", "text_he": "קפה עם חלב, בבקשה.", "text_ru": "Кофе с молоком, пожалуйста."},
            {"speaker": "מלצר", "text_he": "ומה לאכול?", "text_ru": "А поесть?"},
            {"speaker": "לקוח", "text_he": "ארוחת בוקר ישראלית.", "text_ru": "Израильский завтрак."},
            {"speaker": "מלצר", "text_he": "מצוין. רגע אחד.", "text_ru": "Отлично. Одну минуту."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "מלצר", "translation": "официант", "transliteration": "мельцАр"},
            {"word": "קפה", "translation": "кофе", "transliteration": "кафЕ"},
            {"word": "חלב", "translation": "молоко", "transliteration": "халАв"},
            {"word": "ארוחת בוקר", "translation": "завтрак", "transliteration": "арухАт бОкер"},
            {"word": "לשתות", "translation": "пить", "transliteration": "лиштОт"},
            {"word": "לאכול", "translation": "есть", "transliteration": "леехОль"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 12. На автобусной остановке
    {
        "level_id": 1,
        "title": "На автобусной остановке",
        "situation_ru": "Вы спрашиваете, как доехать до моря.",
        "lines_json": json.dumps([
            {"speaker": "נוסע", "text_he": "סליחה, איזה אוטובוס נוסע לים?", "text_ru": "Извините, какой автобус едет к морю?"},
            {"speaker": "אדם", "text_he": "אוטובוס מספר חמש.", "text_ru": "Автобус номер пять."},
            {"speaker": "נוסע", "text_he": "מתי הוא בא?", "text_ru": "Когда он приходит?"},
            {"speaker": "אדם", "text_he": "כל עשר דקות.", "text_ru": "Каждые десять минут."},
            {"speaker": "נוסע", "text_he": "תודה רבה!", "text_ru": "Большое спасибо!"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "אוטובוס", "translation": "автобус", "transliteration": "отобУс"},
            {"word": "ים", "translation": "море", "transliteration": "ям"},
            {"word": "סליחה", "translation": "извините", "transliteration": "слихА"},
            {"word": "כל", "translation": "каждый", "transliteration": "коль"},
            {"word": "לבוא", "translation": "приходить", "transliteration": "лавО"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 13. В магазине одежды
    {
        "level_id": 1,
        "title": "В магазине одежды",
        "situation_ru": "Вы покупаете рубашку в магазине одежды.",
        "lines_json": json.dumps([
            {"speaker": "לקוח", "text_he": "שלום, אני מחפש חולצה.", "text_ru": "Здравствуйте, я ищу рубашку."},
            {"speaker": "מוכרת", "text_he": "איזה צבע אתה רוצה?", "text_ru": "Какой цвет вы хотите?"},
            {"speaker": "לקוח", "text_he": "כחול, בבקשה.", "text_ru": "Синий, пожалуйста."},
            {"speaker": "מוכרת", "text_he": "איזה מידה?", "text_ru": "Какой размер?"},
            {"speaker": "לקוח", "text_he": "מידה בינונית.", "text_ru": "Средний размер."},
            {"speaker": "מוכרת", "text_he": "הנה. אתה רוצה למדוד?", "text_ru": "Вот. Хотите примерить?"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "חולצה", "translation": "рубашка", "transliteration": "хульцА"},
            {"word": "צבע", "translation": "цвет", "transliteration": "цЕва"},
            {"word": "כחול", "translation": "синий", "transliteration": "кахОль"},
            {"word": "מידה", "translation": "размер", "transliteration": "мидА"},
            {"word": "למדוד", "translation": "примерить / измерить", "transliteration": "лимдОд"},
            {"word": "מוכרת", "translation": "продавщица", "transliteration": "мохЕрет"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 14. У врача
    {
        "level_id": 1,
        "title": "У врача",
        "situation_ru": "Вы пришли к врачу, потому что плохо себя чувствуете.",
        "lines_json": json.dumps([
            {"speaker": "רופא", "text_he": "שלום, מה הבעיה?", "text_ru": "Здравствуйте, в чём проблема?"},
            {"speaker": "חולה", "text_he": "אני לא מרגיש טוב. יש לי חום.", "text_ru": "Я плохо себя чувствую. У меня температура."},
            {"speaker": "רופא", "text_he": "מאז מתי?", "text_ru": "С каких пор?"},
            {"speaker": "חולה", "text_he": "מאתמול בערב.", "text_ru": "Со вчерашнего вечера."},
            {"speaker": "רופא", "text_he": "תשתה הרבה מים ותנוח. קח תרופה.", "text_ru": "Пейте много воды и отдыхайте. Примите лекарство."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "רופא", "translation": "врач", "transliteration": "рофЕ"},
            {"word": "חולה", "translation": "больной", "transliteration": "холЕ"},
            {"word": "חום", "translation": "температура / жар", "transliteration": "хом"},
            {"word": "תרופה", "translation": "лекарство", "transliteration": "труфА"},
            {"word": "לנוח", "translation": "отдыхать", "transliteration": "ланУах"},
            {"word": "מים", "translation": "вода", "transliteration": "мАим"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 15. В парке
    {
        "level_id": 1,
        "title": "Прогулка в парке",
        "situation_ru": "Вы гуляете в парке и разговариваете с незнакомцем.",
        "lines_json": json.dumps([
            {"speaker": "אדם", "text_he": "שלום! יום יפה היום, נכון?", "text_ru": "Привет! Красивый день сегодня, правда?"},
            {"speaker": "אתה", "text_he": "כן, מאוד יפה! אני אוהב את הפארק הזה.", "text_ru": "Да, очень красиво! Я люблю этот парк."},
            {"speaker": "אדם", "text_he": "גם אני. אני בא לפה כל יום.", "text_ru": "Я тоже. Я прихожу сюда каждый день."},
            {"speaker": "אתה", "text_he": "יש פה עצים גדולים ופרחים.", "text_ru": "Здесь большие деревья и цветы."},
            {"speaker": "אדם", "text_he": "כן. ויש גם גן משחקים לילדים.", "text_ru": "Да. И ещё есть детская площадка."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "פארק", "translation": "парк", "transliteration": "парк"},
            {"word": "עץ", "translation": "дерево", "transliteration": "эц"},
            {"word": "פרח", "translation": "цветок", "transliteration": "пЕрах"},
            {"word": "גדול", "translation": "большой", "transliteration": "гадОль"},
            {"word": "יפה", "translation": "красивый", "transliteration": "яфЕ"},
            {"word": "גן משחקים", "translation": "детская площадка", "transliteration": "ган мисхакИм"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 16. На почте
    {
        "level_id": 1,
        "title": "На почте",
        "situation_ru": "Вы хотите отправить письмо на почте.",
        "lines_json": json.dumps([
            {"speaker": "לקוח", "text_he": "שלום, אני רוצה לשלוח מכתב.", "text_ru": "Здравствуйте, я хочу отправить письмо."},
            {"speaker": "פקיד", "text_he": "לאן?", "text_ru": "Куда?"},
            {"speaker": "לקוח", "text_he": "לרוסיה.", "text_ru": "В Россию."},
            {"speaker": "פקיד", "text_he": "דואר רגיל או דואר מהיר?", "text_ru": "Обычная почта или срочная?"},
            {"speaker": "לקוח", "text_he": "דואר רגיל. כמה זה עולה?", "text_ru": "Обычная. Сколько это стоит?"},
            {"speaker": "פקיד", "text_he": "שבעה שקלים.", "text_ru": "Семь шекелей."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "מכתב", "translation": "письмо", "transliteration": "михтАв"},
            {"word": "דואר", "translation": "почта", "transliteration": "дОар"},
            {"word": "לשלוח", "translation": "отправить", "transliteration": "лишлОах"},
            {"word": "רגיל", "translation": "обычный", "transliteration": "рагИль"},
            {"word": "מהיר", "translation": "быстрый / срочный", "transliteration": "маhИр"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 17. В ресторане: заказ обеда
    {
        "level_id": 1,
        "title": "В ресторане: заказ обеда",
        "situation_ru": "Вы заказываете обед в ресторане.",
        "lines_json": json.dumps([
            {"speaker": "מלצר", "text_he": "שלום! הנה התפריט.", "text_ru": "Здравствуйте! Вот меню."},
            {"speaker": "לקוח", "text_he": "תודה. מה אתה ממליץ?", "text_ru": "Спасибо. Что вы рекомендуете?"},
            {"speaker": "מלצר", "text_he": "השניצל שלנו מאוד טעים.", "text_ru": "Наш шницель очень вкусный."},
            {"speaker": "לקוח", "text_he": "טוב, שניצל עם סלט, בבקשה.", "text_ru": "Хорошо, шницель с салатом, пожалуйста."},
            {"speaker": "מלצר", "text_he": "ולשתות?", "text_ru": "А пить?"},
            {"speaker": "לקוח", "text_he": "מים, בבקשה.", "text_ru": "Воду, пожалуйста."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "תפריט", "translation": "меню", "transliteration": "тафрИт"},
            {"word": "שניצל", "translation": "шницель", "transliteration": "шнИцель"},
            {"word": "סלט", "translation": "салат", "transliteration": "салАт"},
            {"word": "טעים", "translation": "вкусный", "transliteration": "таИм"},
            {"word": "להמליץ", "translation": "рекомендовать", "transliteration": "леhамлИц"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 18. В библиотеке
    {
        "level_id": 1,
        "title": "В библиотеке",
        "situation_ru": "Вы хотите взять книгу в библиотеке.",
        "lines_json": json.dumps([
            {"speaker": "לקוח", "text_he": "שלום, אני רוצה לקחת ספר.", "text_ru": "Здравствуйте, я хочу взять книгу."},
            {"speaker": "ספרנית", "text_he": "יש לך כרטיס ספרייה?", "text_ru": "У вас есть читательский билет?"},
            {"speaker": "לקוח", "text_he": "כן, הנה.", "text_ru": "Да, вот."},
            {"speaker": "ספרנית", "text_he": "איזה ספר אתה מחפש?", "text_ru": "Какую книгу вы ищете?"},
            {"speaker": "לקוח", "text_he": "ספר על ההיסטוריה של ישראל.", "text_ru": "Книгу об истории Израиля."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "ספרייה", "translation": "библиотека", "transliteration": "сифрийА"},
            {"word": "ספרנית", "translation": "библиотекарь (ж.)", "transliteration": "сафранИт"},
            {"word": "כרטיס", "translation": "карточка / билет", "transliteration": "картИс"},
            {"word": "לקחת", "translation": "взять", "transliteration": "лакАхат"},
            {"word": "היסטוריה", "translation": "история", "transliteration": "hисторья"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 19. На пляже
    {
        "level_id": 1,
        "title": "На пляже",
        "situation_ru": "Вы на пляже и разговариваете со спасателем.",
        "lines_json": json.dumps([
            {"speaker": "מציל", "text_he": "שלום! הים היום רגוע.", "text_ru": "Привет! Море сегодня спокойное."},
            {"speaker": "נופש", "text_he": "מצוין! אפשר לשחות?", "text_ru": "Отлично! Можно плавать?"},
            {"speaker": "מציל", "text_he": "כן, אבל רק עד הדגל האדום.", "text_ru": "Да, но только до красного флага."},
            {"speaker": "נופש", "text_he": "בסדר, תודה.", "text_ru": "Хорошо, спасибо."},
            {"speaker": "מציל", "text_he": "בבקשה. תיהנה!", "text_ru": "Пожалуйста. Наслаждайтесь!"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "מציל", "translation": "спасатель", "transliteration": "мацИль"},
            {"word": "ים", "translation": "море", "transliteration": "ям"},
            {"word": "לשחות", "translation": "плавать", "transliteration": "лисхОт"},
            {"word": "דגל", "translation": "флаг", "transliteration": "дЕгель"},
            {"word": "אדום", "translation": "красный", "transliteration": "адОм"},
            {"word": "רגוע", "translation": "спокойный", "transliteration": "рагУа"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 20. На рынке: покупка овощей
    {
        "level_id": 1,
        "title": "На рынке: покупка овощей",
        "situation_ru": "Вы покупаете овощи на рынке Кармель в Тель-Авиве.",
        "lines_json": json.dumps([
            {"speaker": "מוכר", "text_he": "בואו, בואו! עגבניות טריות!", "text_ru": "Подходите, подходите! Свежие помидоры!"},
            {"speaker": "לקוח", "text_he": "כמה עולה קילו עגבניות?", "text_ru": "Сколько стоит килограмм помидоров?"},
            {"speaker": "מוכר", "text_he": "שישה שקלים לקילו.", "text_ru": "Шесть шекелей за кило."},
            {"speaker": "לקוח", "text_he": "ומלפפונים?", "text_ru": "А огурцы?"},
            {"speaker": "מוכר", "text_he": "חמישה שקלים. תקח גם גזר?", "text_ru": "Пять шекелей. Возьмёте ещё морковь?"},
            {"speaker": "לקוח", "text_he": "כן, חצי קילו גזר. תודה!", "text_ru": "Да, полкило моркови. Спасибо!"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "עגבנייה", "translation": "помидор", "transliteration": "агванийА"},
            {"word": "מלפפון", "translation": "огурец", "transliteration": "мелафефОн"},
            {"word": "גזר", "translation": "морковь", "transliteration": "гЕзер"},
            {"word": "טרי", "translation": "свежий", "transliteration": "тарИ"},
            {"word": "קילו", "translation": "килограмм", "transliteration": "кИло"},
            {"word": "שוק", "translation": "рынок", "transliteration": "шук"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# Level 2: 20 new dialogues (6-8 lines, 5-8 vocab)
# ══════════════════════════════════════════════════════════════════════════════

L2_DIALOGUES = [
    # 1. Собеседование на работу
    {
        "level_id": 2,
        "title": "Собеседование на работу",
        "situation_ru": "Вы пришли на собеседование на должность официанта.",
        "lines_json": json.dumps([
            {"speaker": "מנהל", "text_he": "שלום, שב בבקשה. ספר לי על עצמך.", "text_ru": "Здравствуйте, присаживайтесь. Расскажите о себе."},
            {"speaker": "מועמד", "text_he": "שלום. אני בן עשרים וחמש. אני גר בתל אביב.", "text_ru": "Здравствуйте. Мне двадцать пять лет. Я живу в Тель-Авиве."},
            {"speaker": "מנהל", "text_he": "יש לך ניסיון בעבודה במסעדה?", "text_ru": "У вас есть опыт работы в ресторане?"},
            {"speaker": "מועמד", "text_he": "כן, עבדתי שנה במסעדה בחיפה.", "text_ru": "Да, я работал год в ресторане в Хайфе."},
            {"speaker": "מנהל", "text_he": "טוב. אתה יכול לעבוד בערבים?", "text_ru": "Хорошо. Вы можете работать по вечерам?"},
            {"speaker": "מועמד", "text_he": "כן, אני יכול לעבוד כל יום חוץ משבת.", "text_ru": "Да, я могу работать каждый день, кроме субботы."},
            {"speaker": "מנהל", "text_he": "מצוין. המשכורת היא ארבעים שקל לשעה. מתאים לך?", "text_ru": "Отлично. Зарплата — сорок шекелей в час. Вам подходит?"},
            {"speaker": "מועמד", "text_he": "כן, מתאים. מתי אני יכול להתחיל?", "text_ru": "Да, подходит. Когда я могу начать?"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "ניסיון", "translation": "опыт", "transliteration": "нисайОн"},
            {"word": "מועמד", "translation": "кандидат", "transliteration": "моамАд"},
            {"word": "משכורת", "translation": "зарплата", "transliteration": "маскОрет"},
            {"word": "מנהל", "translation": "менеджер / директор", "transliteration": "менаhЕль"},
            {"word": "להתחיל", "translation": "начать", "transliteration": "леhатхИль"},
            {"word": "ערב", "translation": "вечер", "transliteration": "Эрев"},
            {"word": "מתאים", "translation": "подходит", "transliteration": "матъИм"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 2. У врача: осмотр
    {
        "level_id": 2,
        "title": "У врача: осмотр",
        "situation_ru": "Вы пришли к врачу на осмотр из-за боли в животе.",
        "lines_json": json.dumps([
            {"speaker": "רופא", "text_he": "שלום, מה מפריע לך?", "text_ru": "Здравствуйте, что вас беспокоит?"},
            {"speaker": "חולה", "text_he": "יש לי כאב בטן כבר שלושה ימים.", "text_ru": "У меня болит живот уже три дня."},
            {"speaker": "רופא", "text_he": "איפה בדיוק הכאב?", "text_ru": "Где именно боль?"},
            {"speaker": "חולה", "text_he": "בצד ימין, למטה.", "text_ru": "В правой стороне, внизу."},
            {"speaker": "רופא", "text_he": "אתה מרגיש בחילה?", "text_ru": "Вы чувствуете тошноту?"},
            {"speaker": "חולה", "text_he": "כן, ולפעמים יש לי גם חום.", "text_ru": "Да, и иногда у меня ещё и температура."},
            {"speaker": "רופא", "text_he": "אני רוצה לשלוח אותך לבדיקת דם ואולטרסאונד.", "text_ru": "Я хочу направить вас на анализ крови и УЗИ."},
            {"speaker": "חולה", "text_he": "בסדר, תודה רבה, דוקטור.", "text_ru": "Хорошо, большое спасибо, доктор."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "כאב בטן", "translation": "боль в животе", "transliteration": "кеЭв бЕтен"},
            {"word": "בחילה", "translation": "тошнота", "transliteration": "бехилА"},
            {"word": "בדיקת דם", "translation": "анализ крови", "transliteration": "бдикАт дам"},
            {"word": "צד ימין", "translation": "правая сторона", "transliteration": "цад ямИн"},
            {"word": "להפריע", "translation": "беспокоить", "transliteration": "леhафрИа"},
            {"word": "חום", "translation": "температура / жар", "transliteration": "хом"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 3. В туристическом агентстве
    {
        "level_id": 2,
        "title": "В туристическом агентстве",
        "situation_ru": "Вы планируете поездку в Эйлат в туристическом агентстве.",
        "lines_json": json.dumps([
            {"speaker": "סוכן", "text_he": "שלום, במה אני יכול לעזור?", "text_ru": "Здравствуйте, чем я могу помочь?"},
            {"speaker": "לקוח", "text_he": "אנחנו רוצים לנסוע לאילת בחופשה.", "text_ru": "Мы хотим поехать в Эйлат на отдых."},
            {"speaker": "סוכן", "text_he": "מתי אתם רוצים לנסוע?", "text_ru": "Когда вы хотите поехать?"},
            {"speaker": "לקוח", "text_he": "בשבוע הבא, לארבעה ימים.", "text_ru": "На следующей неделе, на четыре дня."},
            {"speaker": "סוכן", "text_he": "יש לי חבילת נופש נהדרת. מלון עם בריכה ליד הים.", "text_ru": "У меня есть отличный пакет. Отель с бассейном у моря."},
            {"speaker": "לקוח", "text_he": "כמה זה עולה?", "text_ru": "Сколько это стоит?"},
            {"speaker": "סוכן", "text_he": "אלפיים שקל לזוג, כולל ארוחת בוקר.", "text_ru": "Две тысячи шекелей за пару, включая завтрак."},
            {"speaker": "לקוח", "text_he": "נשמע טוב! אנחנו רוצים להזמין.", "text_ru": "Звучит хорошо! Мы хотим забронировать."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "חופשה", "translation": "отпуск / каникулы", "transliteration": "хуфшА"},
            {"word": "חבילת נופש", "translation": "пакет отдыха", "transliteration": "хавилАт нОфеш"},
            {"word": "מלון", "translation": "отель", "transliteration": "малОн"},
            {"word": "בריכה", "translation": "бассейн", "transliteration": "брехА"},
            {"word": "להזמין", "translation": "забронировать / заказать", "transliteration": "леhазмИн"},
            {"word": "זוג", "translation": "пара", "transliteration": "зуг"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 4. Аренда автомобиля
    {
        "level_id": 2,
        "title": "Аренда автомобиля",
        "situation_ru": "Вы арендуете машину в прокате.",
        "lines_json": json.dumps([
            {"speaker": "פקיד", "text_he": "שלום, אתה רוצה לשכור רכב?", "text_ru": "Здравствуйте, вы хотите арендовать машину?"},
            {"speaker": "לקוח", "text_he": "כן, לשלושה ימים.", "text_ru": "Да, на три дня."},
            {"speaker": "פקיד", "text_he": "יש לנו רכב קטן או רכב גדול. מה אתה מעדיף?", "text_ru": "У нас есть маленькая или большая машина. Что вы предпочитаете?"},
            {"speaker": "לקוח", "text_he": "רכב קטן מספיק. כמה עולה ליום?", "text_ru": "Маленькая машина достаточно. Сколько стоит в день?"},
            {"speaker": "פקיד", "text_he": "מאה וחמישים שקל ליום, כולל ביטוח.", "text_ru": "Сто пятьдесят шекелей в день, включая страховку."},
            {"speaker": "לקוח", "text_he": "יש מקום חניה בחינם?", "text_ru": "Есть бесплатная парковка?"},
            {"speaker": "פקיד", "text_he": "כן, אתה מחזיר את הרכב עם מכל מלא, בבקשה.", "text_ru": "Да, вы возвращаете машину с полным баком, пожалуйста."},
            {"speaker": "לקוח", "text_he": "מצוין, אני לוקח.", "text_ru": "Отлично, я беру."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "לשכור", "translation": "арендовать", "transliteration": "лисхОр"},
            {"word": "רכב", "translation": "автомобиль", "transliteration": "рЕхев"},
            {"word": "ביטוח", "translation": "страховка", "transliteration": "битУах"},
            {"word": "חניה", "translation": "парковка", "transliteration": "ханайА"},
            {"word": "מכל", "translation": "бак", "transliteration": "мехАль"},
            {"word": "להחזיר", "translation": "вернуть", "transliteration": "леhахзИр"},
            {"word": "להעדיף", "translation": "предпочитать", "transliteration": "леhаадИф"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 5. В спортзале
    {
        "level_id": 2,
        "title": "В спортзале",
        "situation_ru": "Вы записываетесь в спортзал.",
        "lines_json": json.dumps([
            {"speaker": "מדריך", "text_he": "שלום! אתה רוצה להירשם למכון כושר?", "text_ru": "Привет! Вы хотите записаться в фитнес-зал?"},
            {"speaker": "לקוח", "text_he": "כן, מה יש לכם?", "text_ru": "Да, что у вас есть?"},
            {"speaker": "מדריך", "text_he": "יש מנוי חודשי ב-двести שקל או שנתי ב-אלפיים.", "text_ru": "Есть месячный абонемент за двести шекелей или годовой за две тысячи."},
            {"speaker": "לקוח", "text_he": "מה כולל המנוי?", "text_ru": "Что включает абонемент?"},
            {"speaker": "מדריך", "text_he": "חדר כושר, שיעורי יוגה, בריכה וסאונה.", "text_ru": "Тренажёрный зал, занятия йогой, бассейн и сауна."},
            {"speaker": "לקוח", "text_he": "מתי אתם פתוחים?", "text_ru": "Когда вы открыты?"},
            {"speaker": "מדריך", "text_he": "כל יום מהשעה שש בבוקר עד עשר בלילה.", "text_ru": "Каждый день с шести утра до десяти вечера."},
            {"speaker": "לקוח", "text_he": "אני רוצה מנוי חודשי, בבקשה.", "text_ru": "Я хочу месячный абонемент, пожалуйста."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "מכון כושר", "translation": "фитнес-зал", "transliteration": "махОн кОшер"},
            {"word": "מנוי", "translation": "абонемент", "transliteration": "мануй"},
            {"word": "מדריך", "translation": "инструктор", "transliteration": "мадрИх"},
            {"word": "שיעור", "translation": "урок / занятие", "transliteration": "шиУр"},
            {"word": "חודשי", "translation": "месячный", "transliteration": "ходшИ"},
            {"word": "שנתי", "translation": "годовой", "transliteration": "шнатИ"},
            {"word": "להירשם", "translation": "записаться", "transliteration": "леhирашЕм"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 6. Родительское собрание
    {
        "level_id": 2,
        "title": "Родительское собрание",
        "situation_ru": "Вы пришли на родительское собрание в школе.",
        "lines_json": json.dumps([
            {"speaker": "מורה", "text_he": "שלום, ערב טוב. אתה אבא של דניאל?", "text_ru": "Здравствуйте, добрый вечер. Вы папа Даниэля?"},
            {"speaker": "אבא", "text_he": "כן, נעים להכיר. איך דניאל לומד?", "text_ru": "Да, приятно познакомиться. Как учится Даниэль?"},
            {"speaker": "מורה", "text_he": "דניאל תלמיד טוב. הוא חכם ושקט.", "text_ru": "Даниэль хороший ученик. Он умный и тихий."},
            {"speaker": "אבא", "text_he": "אני שמח לשמוע. ומה עם מתמטיקה?", "text_ru": "Рад слышать. А что с математикой?"},
            {"speaker": "מורה", "text_he": "במתמטיקה הוא צריך לתרגל יותר. הציונים שלו ממוצעים.", "text_ru": "В математике ему нужно больше тренироваться. Его оценки средние."},
            {"speaker": "אבא", "text_he": "אני מבין. אולי הוא צריך מורה פרטי?", "text_ru": "Понимаю. Может быть, ему нужен частный учитель?"},
            {"speaker": "מורה", "text_he": "רעיון טוב. ויש לנו גם חוגים אחרי הצהריים.", "text_ru": "Хорошая идея. И у нас ещё есть кружки после обеда."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "ציון", "translation": "оценка", "transliteration": "циЮн"},
            {"word": "ממוצע", "translation": "средний", "transliteration": "мемуцА"},
            {"word": "מורה פרטי", "translation": "частный учитель", "transliteration": "морЕ пратИ"},
            {"word": "חוג", "translation": "кружок", "transliteration": "хуг"},
            {"word": "לתרגל", "translation": "тренировать(ся)", "transliteration": "летаргЕль"},
            {"word": "אחרי הצהריים", "translation": "после обеда", "transliteration": "ахарЕй hацоhорАим"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 7. Разговор с хозяином квартиры
    {
        "level_id": 2,
        "title": "Разговор с хозяином квартиры",
        "situation_ru": "Вы звоните хозяину квартиры из-за поломки.",
        "lines_json": json.dumps([
            {"speaker": "שוכר", "text_he": "שלום, אני מתקשר בגלל בעיה בדירה.", "text_ru": "Здравствуйте, я звоню из-за проблемы в квартире."},
            {"speaker": "בעלים", "text_he": "מה קרה?", "text_ru": "Что случилось?"},
            {"speaker": "שוכר", "text_he": "המזגן לא עובד ויש נזילה במקלחת.", "text_ru": "Кондиционер не работает и есть протечка в душе."},
            {"speaker": "בעלים", "text_he": "מתי זה התחיל?", "text_ru": "Когда это началось?"},
            {"speaker": "שוכר", "text_he": "המזגן נשבר אתמול, והנזילה כבר שבוע.", "text_ru": "Кондиционер сломался вчера, а протечка уже неделю."},
            {"speaker": "בעלים", "text_he": "אני אשלח טכנאי מחר בבוקר. מתאים?", "text_ru": "Я пришлю техника завтра утром. Подходит?"},
            {"speaker": "שוכר", "text_he": "כן, תודה רבה. בשעה כמה?", "text_ru": "Да, большое спасибо. Во сколько?"},
            {"speaker": "בעלים", "text_he": "בסביבות תשע. תהיה בבית?", "text_ru": "Около девяти. Вы будете дома?"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "דירה", "translation": "квартира", "transliteration": "дирА"},
            {"word": "מזגן", "translation": "кондиционер", "transliteration": "мазгАн"},
            {"word": "נזילה", "translation": "протечка", "transliteration": "незилА"},
            {"word": "מקלחת", "translation": "душ", "transliteration": "миклАхат"},
            {"word": "טכנאי", "translation": "техник", "transliteration": "технАй"},
            {"word": "בעלים", "translation": "хозяин / владелец", "transliteration": "бъалИм"},
            {"word": "שוכר", "translation": "арендатор", "transliteration": "сохЕр"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 8. Жалоба в ресторане
    {
        "level_id": 2,
        "title": "Жалоба в ресторане",
        "situation_ru": "Вы жалуетесь официанту на качество блюда.",
        "lines_json": json.dumps([
            {"speaker": "לקוח", "text_he": "סליחה, יש בעיה עם האוכל.", "text_ru": "Извините, есть проблема с едой."},
            {"speaker": "מלצר", "text_he": "מה הבעיה?", "text_ru": "Какая проблема?"},
            {"speaker": "לקוח", "text_he": "הסטייק קר ולא מבושל מספיק.", "text_ru": "Стейк холодный и недостаточно приготовлен."},
            {"speaker": "מלצר", "text_he": "אני מצטער מאוד. אני אחליף לך מיד.", "text_ru": "Мне очень жаль. Я вам сейчас заменю."},
            {"speaker": "לקוח", "text_he": "תודה. ואפשר גם לדבר עם המנהל?", "text_ru": "Спасибо. И можно также поговорить с менеджером?"},
            {"speaker": "מלצר", "text_he": "בוודאי, רגע אחד.", "text_ru": "Конечно, одну минуту."},
            {"speaker": "מנהל", "text_he": "שלום, אני המנהל. אני מתנצל. נעשה לך הנחה של עשרים אחוז.", "text_ru": "Здравствуйте, я менеджер. Прошу прощения. Мы сделаем вам скидку двадцать процентов."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "סטייק", "translation": "стейк", "transliteration": "стейк"},
            {"word": "מבושל", "translation": "приготовленный", "transliteration": "мевушАль"},
            {"word": "להחליף", "translation": "заменить", "transliteration": "леhахлИф"},
            {"word": "הנחה", "translation": "скидка", "transliteration": "hанахА"},
            {"word": "להתנצל", "translation": "извиняться", "transliteration": "леhитнацЕль"},
            {"word": "אחוז", "translation": "процент", "transliteration": "ахУз"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 9. Открытие банковского счёта
    {
        "level_id": 2,
        "title": "Открытие банковского счёта",
        "situation_ru": "Вы открываете банковский счёт и обсуждаете условия.",
        "lines_json": json.dumps([
            {"speaker": "בנקאי", "text_he": "שלום, איך אני יכול לעזור?", "text_ru": "Здравствуйте, как я могу помочь?"},
            {"speaker": "לקוח", "text_he": "אני רוצה לפתוח חשבון עובר ושב.", "text_ru": "Я хочу открыть текущий счёт."},
            {"speaker": "בנקאי", "text_he": "בוודאי. יש לך תעודת זהות ואישור כתובת?", "text_ru": "Конечно. У вас есть удостоверение личности и подтверждение адреса?"},
            {"speaker": "לקוח", "text_he": "כן, הנה. אני רוצה גם כרטיס אשראי.", "text_ru": "Да, вот. Я хочу ещё кредитную карту."},
            {"speaker": "בנקאי", "text_he": "עמלת ניהול החשבון היא שלושים שקל בחודש.", "text_ru": "Комиссия за ведение счёта — тридцать шекелей в месяц."},
            {"speaker": "לקוח", "text_he": "אפשר לקבל אפליקציה לטלפון?", "text_ru": "Можно получить приложение для телефона?"},
            {"speaker": "בנקאי", "text_he": "כן, אתה יכול להוריד את האפליקציה של הבנק בחינם.", "text_ru": "Да, вы можете скачать банковское приложение бесплатно."},
            {"speaker": "לקוח", "text_he": "מצוין, תודה רבה.", "text_ru": "Отлично, большое спасибо."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "חשבון עובר ושב", "translation": "текущий счёт", "transliteration": "хешбОн овЕр вашАв"},
            {"word": "כרטיס אשראי", "translation": "кредитная карта", "transliteration": "картИс ашрАй"},
            {"word": "עמלה", "translation": "комиссия", "transliteration": "амлА"},
            {"word": "אישור כתובת", "translation": "подтверждение адреса", "transliteration": "ишУр ктОвет"},
            {"word": "להוריד", "translation": "скачать", "transliteration": "леhорИд"},
            {"word": "בנקאי", "translation": "банкир", "transliteration": "банкАй"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 10. В автосервисе
    {
        "level_id": 2,
        "title": "В автосервисе",
        "situation_ru": "Вы привезли машину в автосервис.",
        "lines_json": json.dumps([
            {"speaker": "לקוח", "text_he": "שלום, יש לי בעיה עם האוטו.", "text_ru": "Здравствуйте, у меня проблема с машиной."},
            {"speaker": "מכונאי", "text_he": "מה קורה?", "text_ru": "Что случилось?"},
            {"speaker": "לקוח", "text_he": "המנוע עושה רעש מוזר ויש נורה דולקת.", "text_ru": "Мотор издаёт странный шум и горит лампочка."},
            {"speaker": "מכונאי", "text_he": "אני צריך לבדוק. זה ייקח בערך שעה.", "text_ru": "Мне нужно проверить. Это займёт примерно час."},
            {"speaker": "לקוח", "text_he": "בסדר. כמה בערך עולה תיקון?", "text_ru": "Ладно. Сколько примерно стоит ремонт?"},
            {"speaker": "מכונאי", "text_he": "תלוי בבעיה. אחרי הבדיקה אני אגיד לך.", "text_ru": "Зависит от проблемы. После проверки я вам скажу."},
            {"speaker": "לקוח", "text_he": "טוב, אני אחכה.", "text_ru": "Хорошо, я подожду."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "מכונאי", "translation": "механик", "transliteration": "мехонАй"},
            {"word": "מנוע", "translation": "мотор / двигатель", "transliteration": "манОа"},
            {"word": "רעש", "translation": "шум", "transliteration": "рАаш"},
            {"word": "תיקון", "translation": "ремонт", "transliteration": "тикУн"},
            {"word": "נורה", "translation": "лампочка", "transliteration": "нурА"},
            {"word": "בדיקה", "translation": "проверка", "transliteration": "бдикА"},
            {"word": "תלוי", "translation": "зависит", "transliteration": "талУй"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 11. В супермаркете
    {
        "level_id": 2,
        "title": "Покупки в супермаркете",
        "situation_ru": "Вы делаете покупки в супермаркете и спрашиваете сотрудника.",
        "lines_json": json.dumps([
            {"speaker": "לקוח", "text_he": "סליחה, איפה מוצרי החלב?", "text_ru": "Извините, где молочные продукты?"},
            {"speaker": "עובד", "text_he": "בסוף המעבר, בצד שמאל.", "text_ru": "В конце прохода, слева."},
            {"speaker": "לקוח", "text_he": "ואיפה הלחם?", "text_ru": "А где хлеб?"},
            {"speaker": "עובד", "text_he": "הלחם במעבר השלישי.", "text_ru": "Хлеб в третьем проходе."},
            {"speaker": "לקוח", "text_he": "יש לכם הנחות היום?", "text_ru": "У вас есть скидки сегодня?"},
            {"speaker": "עובד", "text_he": "כן, יש אחד ועוד אחד חינם על שוקולד.", "text_ru": "Да, один плюс один бесплатно на шоколад."},
            {"speaker": "לקוח", "text_he": "מצוין, תודה!", "text_ru": "Отлично, спасибо!"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "מוצרי חלב", "translation": "молочные продукты", "transliteration": "муцрЕй халАв"},
            {"word": "מעבר", "translation": "проход", "transliteration": "маавАр"},
            {"word": "לחם", "translation": "хлеб", "transliteration": "лЕхем"},
            {"word": "הנחה", "translation": "скидка", "transliteration": "hанахА"},
            {"word": "חינם", "translation": "бесплатно", "transliteration": "хинАм"},
            {"word": "שמאל", "translation": "лево", "transliteration": "смОль"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 12. Запись к стоматологу
    {
        "level_id": 2,
        "title": "Запись к стоматологу",
        "situation_ru": "Вы записываетесь на приём к стоматологу по телефону.",
        "lines_json": json.dumps([
            {"speaker": "מזכירה", "text_he": "מרפאת שיניים, שלום.", "text_ru": "Стоматологическая клиника, здравствуйте."},
            {"speaker": "לקוח", "text_he": "שלום, אני רוצה לקבוע תור לרופא שיניים.", "text_ru": "Здравствуйте, я хочу записаться к стоматологу."},
            {"speaker": "מזכירה", "text_he": "מה הבעיה?", "text_ru": "Какая проблема?"},
            {"speaker": "לקוח", "text_he": "יש לי כאב שן כבר יומיים.", "text_ru": "У меня болит зуб уже два дня."},
            {"speaker": "מזכירה", "text_he": "אתה יכול לבוא מחר בשעה עשר?", "text_ru": "Вы можете прийти завтра в десять?"},
            {"speaker": "לקוח", "text_he": "כן, מתאים לי. כמה עולה הביקור?", "text_ru": "Да, мне подходит. Сколько стоит визит?"},
            {"speaker": "מזכירה", "text_he": "בדיקה ראשונה — מאתיים שקל.", "text_ru": "Первичный осмотр — двести шекелей."},
            {"speaker": "לקוח", "text_he": "בסדר, תודה. להתראות.", "text_ru": "Хорошо, спасибо. До свидания."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "רופא שיניים", "translation": "стоматолог", "transliteration": "рофЕ шинАим"},
            {"word": "תור", "translation": "очередь / запись", "transliteration": "тор"},
            {"word": "כאב שן", "translation": "зубная боль", "transliteration": "кеЭв шен"},
            {"word": "מרפאה", "translation": "клиника", "transliteration": "мирпаА"},
            {"word": "לקבוע", "translation": "назначить / установить", "transliteration": "ликбОа"},
            {"word": "ביקור", "translation": "визит", "transliteration": "бикУр"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 13. В гостинице
    {
        "level_id": 2,
        "title": "В гостинице: заселение",
        "situation_ru": "Вы заселяетесь в гостиницу.",
        "lines_json": json.dumps([
            {"speaker": "פקיד", "text_he": "שלום, ברוכים הבאים למלון. יש לך הזמנה?", "text_ru": "Здравствуйте, добро пожаловать в отель. У вас есть бронь?"},
            {"speaker": "אורח", "text_he": "כן, על שם אלכסנדר. הזמנתי חדר לשלושה לילות.", "text_ru": "Да, на имя Александр. Я забронировал номер на три ночи."},
            {"speaker": "פקיד", "text_he": "כן, מצאתי. חדר עם מרפסת ונוף לים.", "text_ru": "Да, нашёл. Номер с балконом и видом на море."},
            {"speaker": "אורח", "text_he": "מצוין! מתי ארוחת הבוקר?", "text_ru": "Отлично! Когда завтрак?"},
            {"speaker": "פקיד", "text_he": "מהשעה שבע עד עשר. בקומה הראשונה.", "text_ru": "С семи до десяти. На первом этаже."},
            {"speaker": "אורח", "text_he": "יש וויי-פיי בחדר?", "text_ru": "Есть вай-фай в номере?"},
            {"speaker": "פקיד", "text_he": "כן, הסיסמה כתובה בחדר. הנה המפתח שלך. חדר 405.", "text_ru": "Да, пароль написан в номере. Вот ваш ключ. Номер 405."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "הזמנה", "translation": "бронь / заказ", "transliteration": "hазманА"},
            {"word": "חדר", "translation": "комната / номер", "transliteration": "хЕдер"},
            {"word": "מרפסת", "translation": "балкон", "transliteration": "мирпЕсет"},
            {"word": "נוף", "translation": "вид / пейзаж", "transliteration": "ноф"},
            {"word": "מפתח", "translation": "ключ", "transliteration": "мафтЕах"},
            {"word": "סיסמה", "translation": "пароль", "transliteration": "сисмА"},
            {"word": "אורח", "translation": "гость", "transliteration": "орЕах"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 14. Покупка мебели
    {
        "level_id": 2,
        "title": "Покупка мебели",
        "situation_ru": "Вы покупаете мебель для новой квартиры.",
        "lines_json": json.dumps([
            {"speaker": "לקוח", "text_he": "שלום, אנחנו מחפשים ספה חדשה.", "text_ru": "Здравствуйте, мы ищем новый диван."},
            {"speaker": "מוכר", "text_he": "באיזה סגנון? מודרני או קלאסי?", "text_ru": "В каком стиле? Современный или классический?"},
            {"speaker": "לקוח", "text_he": "מודרני, בצבע אפור.", "text_ru": "Современный, серого цвета."},
            {"speaker": "מוכר", "text_he": "יש לנו כמה דגמים. בוא, אני אראה לך.", "text_ru": "У нас есть несколько моделей. Пойдём, я покажу вам."},
            {"speaker": "לקוח", "text_he": "הספה הזאת נראית טוב. כמה היא עולה?", "text_ru": "Этот диван выглядит хорошо. Сколько он стоит?"},
            {"speaker": "מוכר", "text_he": "שלושת אלפים שקל. ויש משלוח חינם.", "text_ru": "Три тысячи шекелей. И бесплатная доставка."},
            {"speaker": "לקוח", "text_he": "אפשר לשלם בתשלומים?", "text_ru": "Можно платить в рассрочку?"},
            {"speaker": "מוכר", "text_he": "כן, עד שנים עשר תשלומים ללא ריבית.", "text_ru": "Да, до двенадцати платежей без процентов."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "ספה", "translation": "диван", "transliteration": "сапА"},
            {"word": "סגנון", "translation": "стиль", "transliteration": "сигнОн"},
            {"word": "דגם", "translation": "модель", "transliteration": "дЕгем"},
            {"word": "משלוח", "translation": "доставка", "transliteration": "мишлОах"},
            {"word": "תשלום", "translation": "платёж", "transliteration": "ташлУм"},
            {"word": "ריבית", "translation": "процент (фин.)", "transliteration": "рибИт"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 15. В ветеринарной клинике
    {
        "level_id": 2,
        "title": "В ветеринарной клинике",
        "situation_ru": "Вы привели кошку к ветеринару.",
        "lines_json": json.dumps([
            {"speaker": "בעלים", "text_he": "שלום, החתולה שלי לא אוכלת כבר יומיים.", "text_ru": "Здравствуйте, моя кошка не ест уже два дня."},
            {"speaker": "וטרינר", "text_he": "בואי נבדוק אותה. בת כמה היא?", "text_ru": "Давайте её осмотрим. Сколько ей лет?"},
            {"speaker": "בעלים", "text_he": "היא בת שלוש. בדרך כלל היא אוכלת טוב.", "text_ru": "Ей три года. Обычно она хорошо ест."},
            {"speaker": "וטרינר", "text_he": "היא שותה מים?", "text_ru": "Она пьёт воду?"},
            {"speaker": "בעלים", "text_he": "כן, אבל מעט.", "text_ru": "Да, но мало."},
            {"speaker": "וטרינר", "text_he": "אני חושב שזו בעיה בבטן. אני אתן לה תרופה.", "text_ru": "Я думаю, что это проблема с животом. Я дам ей лекарство."},
            {"speaker": "בעלים", "text_he": "תודה, דוקטור. מתי לחזור לבדיקה?", "text_ru": "Спасибо, доктор. Когда вернуться на проверку?"},
            {"speaker": "וטרינר", "text_he": "בעוד שבוע. אם יש שינוי, תתקשרי.", "text_ru": "Через неделю. Если будут изменения, позвоните."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "חתולה", "translation": "кошка", "transliteration": "хатулА"},
            {"word": "וטרינר", "translation": "ветеринар", "transliteration": "ветеринАр"},
            {"word": "תרופה", "translation": "лекарство", "transliteration": "труфА"},
            {"word": "שינוי", "translation": "изменение", "transliteration": "шинУй"},
            {"word": "לבדוק", "translation": "проверить", "transliteration": "ливдОк"},
            {"word": "בדרך כלל", "translation": "обычно", "transliteration": "бедЕрех клаль"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 16. На вокзале
    {
        "level_id": 2,
        "title": "На железнодорожном вокзале",
        "situation_ru": "Вы покупаете билет на поезд.",
        "lines_json": json.dumps([
            {"speaker": "נוסע", "text_he": "שלום, אני צריך כרטיס לירושלים.", "text_ru": "Здравствуйте, мне нужен билет до Иерусалима."},
            {"speaker": "קופאי", "text_he": "הלוך בלבד או הלוך ושוב?", "text_ru": "Только туда или туда и обратно?"},
            {"speaker": "נוסע", "text_he": "הלוך ושוב, בבקשה.", "text_ru": "Туда и обратно, пожалуйста."},
            {"speaker": "קופאי", "text_he": "ארבעים ושמונה שקלים. הרכבת הבאה בעוד עשרים דקות.", "text_ru": "Сорок восемь шекелей. Следующий поезд через двадцать минут."},
            {"speaker": "נוסע", "text_he": "מאיזה רציף?", "text_ru": "С какой платформы?"},
            {"speaker": "קופאי", "text_he": "רציף שלוש. תעלה במדרגות הנעות.", "text_ru": "Платформа три. Поднимитесь на эскалаторе."},
            {"speaker": "נוסע", "text_he": "כמה זמן הנסיעה?", "text_ru": "Сколько времени длится поездка?"},
            {"speaker": "קופאי", "text_he": "כחמישים דקות.", "text_ru": "Около пятидесяти минут."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "רכבת", "translation": "поезд", "transliteration": "ракЕвет"},
            {"word": "כרטיס", "translation": "билет", "transliteration": "картИс"},
            {"word": "רציף", "translation": "платформа", "transliteration": "рацИф"},
            {"word": "הלוך ושוב", "translation": "туда и обратно", "transliteration": "hалОх вашОв"},
            {"word": "נסיעה", "translation": "поездка", "transliteration": "несиА"},
            {"word": "קופאי", "translation": "кассир", "transliteration": "купАй"},
            {"word": "מדרגות נעות", "translation": "эскалатор", "transliteration": "мадрегОт наОт"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 17. В парикмахерской
    {
        "level_id": 2,
        "title": "В парикмахерской",
        "situation_ru": "Вы пришли в парикмахерскую на стрижку.",
        "lines_json": json.dumps([
            {"speaker": "ספר", "text_he": "שלום! מה תרצה לעשות היום?", "text_ru": "Привет! Что вы хотите сделать сегодня?"},
            {"speaker": "לקוח", "text_he": "אני רוצה תספורת. קצר מהצדדים ויותר ארוך למעלה.", "text_ru": "Я хочу стрижку. Коротко по бокам и длиннее сверху."},
            {"speaker": "ספר", "text_he": "בסדר. גם לשטוף?", "text_ru": "Ладно. Помыть тоже?"},
            {"speaker": "לקוח", "text_he": "כן, בבקשה.", "text_ru": "Да, пожалуйста."},
            {"speaker": "ספר", "text_he": "ככה מספיק קצר?", "text_ru": "Достаточно коротко?"},
            {"speaker": "לקוח", "text_he": "עוד קצת יותר קצר, בבקשה.", "text_ru": "Ещё немного короче, пожалуйста."},
            {"speaker": "ספר", "text_he": "מוכן! זה שישים שקל.", "text_ru": "Готово! Это шестьдесят шекелей."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "ספר", "translation": "парикмахер", "transliteration": "сапАр"},
            {"word": "תספורת", "translation": "стрижка", "transliteration": "тиспОрет"},
            {"word": "קצר", "translation": "короткий", "transliteration": "кацАр"},
            {"word": "ארוך", "translation": "длинный", "transliteration": "арОх"},
            {"word": "לשטוף", "translation": "мыть / ополоснуть", "transliteration": "лиштОф"},
            {"word": "צד", "translation": "сторона / бок", "transliteration": "цад"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 18. Вызов электрика
    {
        "level_id": 2,
        "title": "Вызов электрика",
        "situation_ru": "Вы вызываете электрика домой.",
        "lines_json": json.dumps([
            {"speaker": "לקוח", "text_he": "שלום, אני צריך חשמלאי. יש בעיה עם החשמל.", "text_ru": "Здравствуйте, мне нужен электрик. У меня проблема с электричеством."},
            {"speaker": "חשמלאי", "text_he": "מה הבעיה?", "text_ru": "Какая проблема?"},
            {"speaker": "לקוח", "text_he": "הנקע בסלון לא עובד, ובמטבח יש קצר.", "text_ru": "Розетка в гостиной не работает, и на кухне короткое замыкание."},
            {"speaker": "חשמלאי", "text_he": "אני יכול לבוא היום בשעה חמש. מתאים?", "text_ru": "Я могу прийти сегодня в пять. Подходит?"},
            {"speaker": "לקוח", "text_he": "כן, מצוין. כמה זה עולה?", "text_ru": "Да, отлично. Сколько это стоит?"},
            {"speaker": "חשמלאי", "text_he": "ביקור בית — מאה חמישים שקל ועוד עלות חומרים.", "text_ru": "Вызов на дом — сто пятьдесят шекелей плюс стоимость материалов."},
            {"speaker": "לקוח", "text_he": "בסדר, אני מחכה לך.", "text_ru": "Хорошо, я жду вас."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "חשמלאי", "translation": "электрик", "transliteration": "хашмалАй"},
            {"word": "חשמל", "translation": "электричество", "transliteration": "хашмАль"},
            {"word": "שקע", "translation": "розетка", "transliteration": "шЕка"},
            {"word": "קצר", "translation": "короткое замыкание", "transliteration": "кЕцер"},
            {"word": "סלון", "translation": "гостиная", "transliteration": "салОн"},
            {"word": "חומרים", "translation": "материалы", "transliteration": "хомарИм"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 19. В мобильном магазине
    {
        "level_id": 2,
        "title": "Покупка телефона",
        "situation_ru": "Вы покупаете новый мобильный телефон.",
        "lines_json": json.dumps([
            {"speaker": "לקוח", "text_he": "שלום, אני מחפש טלפון חדש.", "text_ru": "Здравствуйте, я ищу новый телефон."},
            {"speaker": "מוכר", "text_he": "מה התקציב שלך?", "text_ru": "Какой у вас бюджет?"},
            {"speaker": "לקוח", "text_he": "עד שלושת אלפים שקל.", "text_ru": "До трёх тысяч шекелей."},
            {"speaker": "מוכר", "text_he": "יש לי כמה אפשרויות טובות. מה חשוב לך? מצלמה? סוללה?", "text_ru": "У меня есть несколько хороших вариантов. Что вам важно? Камера? Батарея?"},
            {"speaker": "לקוח", "text_he": "מצלמה טובה וזיכרון גדול.", "text_ru": "Хорошая камера и большая память."},
            {"speaker": "מוכר", "text_he": "אני ממליץ על הדגם הזה. יש בו 128 גיגה.", "text_ru": "Я рекомендую эту модель. В ней 128 гигабайт."},
            {"speaker": "לקוח", "text_he": "אפשר לנסות אותו?", "text_ru": "Можно его попробовать?"},
            {"speaker": "מוכר", "text_he": "בוודאי, הנה.", "text_ru": "Конечно, вот."}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "טלפון", "translation": "телефон", "transliteration": "телефОн"},
            {"word": "תקציב", "translation": "бюджет", "transliteration": "такцИв"},
            {"word": "מצלמה", "translation": "камера", "transliteration": "мацлемА"},
            {"word": "סוללה", "translation": "батарея", "transliteration": "солелА"},
            {"word": "זיכרון", "translation": "память", "transliteration": "зикарОн"},
            {"word": "אפשרות", "translation": "вариант / возможность", "transliteration": "эфшарУт"},
            {"word": "לנסות", "translation": "попробовать", "transliteration": "ленасОт"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
    # 20. Соседский спор
    {
        "level_id": 2,
        "title": "Соседский спор из-за шума",
        "situation_ru": "Вы жалуетесь соседу на шум поздно вечером.",
        "lines_json": json.dumps([
            {"speaker": "שכן", "text_he": "שלום, סליחה שאני מפריע. יש הרבה רעש מהדירה שלך.", "text_ru": "Привет, извини, что беспокою. Из твоей квартиры очень шумно."},
            {"speaker": "שכן ב", "text_he": "מצטער, יש לנו מסיבה קטנה.", "text_ru": "Извини, у нас небольшая вечеринка."},
            {"speaker": "שכן", "text_he": "אבל השעה כבר אחת עשרה בלילה. הילדים שלי ישנים.", "text_ru": "Но уже одиннадцать ночи. Мои дети спят."},
            {"speaker": "שכן ב", "text_he": "אתה צודק, אני מצטער. אנחנו נוריד את המוזיקה.", "text_ru": "Ты прав, прости. Мы приглушим музыку."},
            {"speaker": "שכן", "text_he": "תודה רבה. אני מעריך את זה.", "text_ru": "Большое спасибо. Я ценю это."},
            {"speaker": "שכן ב", "text_he": "בסדר גמור. לילה טוב!", "text_ru": "Конечно. Спокойной ночи!"}
        ], ensure_ascii=False),
        "vocabulary_json": json.dumps([
            {"word": "רעש", "translation": "шум", "transliteration": "рАаш"},
            {"word": "מסיבה", "translation": "вечеринка", "transliteration": "месибА"},
            {"word": "מוזיקה", "translation": "музыка", "transliteration": "мУзика"},
            {"word": "להוריד", "translation": "приглушить / снизить", "transliteration": "леhорИд"},
            {"word": "להעריך", "translation": "ценить", "transliteration": "леhаарИх"},
            {"word": "צודק", "translation": "прав", "transliteration": "цодЕк"},
            {"word": "להפריע", "translation": "беспокоить", "transliteration": "леhафрИа"}
        ], ensure_ascii=False),
        "audio_url": None,
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# Combined list & title list for downgrade
# ══════════════════════════════════════════════════════════════════════════════

ALL_DIALOGUES = L1_DIALOGUES + L2_DIALOGUES
TITLE_LIST = [d["title"] for d in ALL_DIALOGUES]


def upgrade() -> None:
    op.execute(
        "SELECT setval('dialogues_id_seq', "
        "GREATEST(COALESCE((SELECT MAX(id) FROM dialogues), 0), 1))"
    )
    op.bulk_insert(dialogues_table, ALL_DIALOGUES)


def downgrade() -> None:
    titles = ", ".join(f"'{t}'" for t in TITLE_LIST)
    op.execute(f"DELETE FROM dialogues WHERE title IN ({titles})")
