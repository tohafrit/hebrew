"""Add 18 L1 + 24 L2 reading texts = 42 total

Revision ID: 084
Revises: 083
Create Date: 2026-03-02
"""
import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "084"
down_revision: Union[str, None] = "083"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

reading_texts_table = sa.table(
    "reading_texts",
    sa.column("level_id", sa.Integer),
    sa.column("title_he", sa.String),
    sa.column("title_ru", sa.String),
    sa.column("content_he", sa.Text),
    sa.column("content_ru", sa.Text),
    sa.column("vocabulary_json", sa.Text),
    sa.column("audio_url", sa.String),
    sa.column("category", sa.String),
)

_j = lambda d: json.dumps(d, ensure_ascii=False)

TEXTS = [
    # 1. В школе
    {
        "level_id": 1,
        "title_he": "בבית ספר",
        "title_ru": "В школе",
        "content_he": "דני הולך לבית ספר כל יום. הוא לומד עברית, מתמטיקה ומדעים. המורה שלו טובה מאוד. היא מלמדת את התלמידים דברים חדשים. דני אוהב ללמוד.",
        "content_ru": "Дани ходит в школу каждый день. Он учит иврит, математику и естественные науки. Его учительница очень хорошая. Она учит учеников новым вещам. Дани любит учиться.",
        "vocabulary_json": _j([{"word": "בית ספר", "translation": "школа", "transliteration": "бейт сЕфер"}, {"word": "מתמטיקה", "translation": "математика", "transliteration": "матемАтика"}, {"word": "מדעים", "translation": "науки", "transliteration": "мадаИм"}, {"word": "מורה", "translation": "учитель", "transliteration": "морА"}, {"word": "תלמידים", "translation": "ученики", "transliteration": "талмидИм"}]),
        "audio_url": None,
        "category": "story",
    },
    # 2. Домашние питомцы
    {
        "level_id": 1,
        "title_he": "חיות מחמד",
        "title_ru": "Домашние питомцы",
        "content_he": "לשרה יש חתול. החתול שלה לבן וגדול. הוא אוהב לשחק בגינה. שרה נותנת לו אוכל כל יום. החתול ישן על המיטה שלה.",
        "content_ru": "У Сары есть кот. Её кот белый и большой. Он любит играть в саду. Сара даёт ему еду каждый день. Кот спит на её кровати.",
        "vocabulary_json": _j([{"word": "חתול", "translation": "кот", "transliteration": "хатУль"}, {"word": "גינה", "translation": "сад", "transliteration": "гинА"}, {"word": "אוכל", "translation": "еда", "transliteration": "Охель"}, {"word": "מיטה", "translation": "кровать", "transliteration": "митА"}, {"word": "לשחק", "translation": "играть", "transliteration": "лесахЕк"}]),
        "audio_url": None,
        "category": "story",
    },
    # 3. Времена года
    {
        "level_id": 1,
        "title_he": "עונות השנה",
        "title_ru": "Времена года",
        "content_he": "בישראל יש ארבע עונות. בקיץ חם מאוד. בחורף יורד גשם. באביב יש פרחים יפים. בסתיו העלים נופלים מהעצים.",
        "content_ru": "В Израиле четыре времени года. Летом очень жарко. Зимой идёт дождь. Весной красивые цветы. Осенью листья падают с деревьев.",
        "vocabulary_json": _j([{"word": "עונה", "translation": "сезон", "transliteration": "онА"}, {"word": "קיץ", "translation": "лето", "transliteration": "кАйиц"}, {"word": "חורף", "translation": "зима", "transliteration": "хОреф"}, {"word": "אביב", "translation": "весна", "transliteration": "авИв"}, {"word": "סתיו", "translation": "осень", "transliteration": "стАв"}]),
        "audio_url": None,
        "category": "story",
    },
    # 4. День рождения
    {
        "level_id": 1,
        "title_he": "יום הולדת",
        "title_ru": "День рождения",
        "content_he": "היום יום ההולדת של רון. הוא בן שבע. המשפחה עושה מסיבה. יש עוגה גדולה עם נרות. רון מקבל מתנות מהחברים.",
        "content_ru": "Сегодня день рождения Рона. Ему семь лет. Семья устраивает праздник. Есть большой торт со свечами. Рон получает подарки от друзей.",
        "vocabulary_json": _j([{"word": "יום הולדת", "translation": "день рождения", "transliteration": "йомhуледЕт"}, {"word": "מסיבה", "translation": "праздник/вечеринка", "transliteration": "месибА"}, {"word": "עוגה", "translation": "торт", "transliteration": "угА"}, {"word": "נרות", "translation": "свечи", "transliteration": "нерОт"}, {"word": "מתנה", "translation": "подарок", "transliteration": "матанА"}]),
        "audio_url": None,
        "category": "story",
    },
    # 5. Моя комната
    {
        "level_id": 1,
        "title_he": "החדר שלי",
        "title_ru": "Моя комната",
        "content_he": "יש לי חדר קטן אבל יפה. יש שם מיטה, שולחן וכיסא. על הקיר יש תמונות. ליד החלון יש צמח ירוק. אני אוהב את החדר שלי.",
        "content_ru": "У меня маленькая, но красивая комната. Там есть кровать, стол и стул. На стене картины. Рядом с окном зелёное растение. Я люблю свою комнату.",
        "vocabulary_json": _j([{"word": "חדר", "translation": "комната", "transliteration": "хЕдер"}, {"word": "שולחן", "translation": "стол", "transliteration": "шулхАн"}, {"word": "כיסא", "translation": "стул", "transliteration": "кисЕ"}, {"word": "קיר", "translation": "стена", "transliteration": "кир"}, {"word": "חלון", "translation": "окно", "transliteration": "халОн"}]),
        "audio_url": None,
        "category": "story",
    },
    # 6. В парке
    {
        "level_id": 1,
        "title_he": "בפארק",
        "title_ru": "В парке",
        "content_he": "ביום שבת אנחנו הולכים לפארק. הילדים משחקים במגרש. אני רץ ומשחק כדורגל. אמא יושבת על הספסל וקוראת ספר. אבא מכין פיקניק.",
        "content_ru": "В субботу мы ходим в парк. Дети играют на площадке. Я бегаю и играю в футбол. Мама сидит на скамейке и читает книгу. Папа готовит пикник.",
        "vocabulary_json": _j([{"word": "פארק", "translation": "парк", "transliteration": "парк"}, {"word": "מגרש", "translation": "площадка", "transliteration": "мигрАш"}, {"word": "כדורגל", "translation": "футбол", "transliteration": "кадурЕгель"}, {"word": "ספסל", "translation": "скамейка", "transliteration": "сафсАль"}, {"word": "פיקניק", "translation": "пикник", "transliteration": "пикнИк"}]),
        "audio_url": None,
        "category": "story",
    },
    # 7. На рынке
    {
        "level_id": 1,
        "title_he": "בשוק",
        "title_ru": "На рынке",
        "content_he": "אמא לוקחת אותי לשוק. יש שם הרבה פירות וירקות. אנחנו קונים תפוחים, בננות ועגבניות. המוכר נחמד ונותן לי תפוז. אני אוהב ללכת לשוק.",
        "content_ru": "Мама берёт меня на рынок. Там много фруктов и овощей. Мы покупаем яблоки, бананы и помидоры. Продавец приветливый и даёт мне апельсин. Я люблю ходить на рынок.",
        "vocabulary_json": _j([{"word": "שוק", "translation": "рынок", "transliteration": "шук"}, {"word": "פירות", "translation": "фрукты", "transliteration": "перОт"}, {"word": "ירקות", "translation": "овощи", "transliteration": "йеракОт"}, {"word": "מוכר", "translation": "продавец", "transliteration": "мохЕр"}, {"word": "תפוז", "translation": "апельсин", "transliteration": "тапУз"}]),
        "audio_url": None,
        "category": "story",
    },
    # 8. У врача
    {
        "level_id": 1,
        "title_he": "אצל הרופא",
        "title_ru": "У врача",
        "content_he": "אני לא מרגיש טוב. יש לי כאב ראש וחום. אמא לוקחת אותי לרופא. הרופא בודק אותי ונותן לי תרופה. אחרי יום אני מרגיש יותר טוב.",
        "content_ru": "Я плохо себя чувствую. У меня болит голова и температура. Мама ведёт меня к врачу. Врач осматривает меня и даёт мне лекарство. Через день мне лучше.",
        "vocabulary_json": _j([{"word": "רופא", "translation": "врач", "transliteration": "рофЕ"}, {"word": "כאב ראש", "translation": "головная боль", "transliteration": "кеЕв рош"}, {"word": "חום", "translation": "температура", "transliteration": "хом"}, {"word": "תרופה", "translation": "лекарство", "transliteration": "труфА"}, {"word": "בודק", "translation": "проверяет", "transliteration": "бодЕк"}]),
        "audio_url": None,
        "category": "story",
    },
    # 9. Доброе утро
    {
        "level_id": 1,
        "title_he": "בוקר טוב",
        "title_ru": "Доброе утро",
        "content_he": "אני קם בשבע בבוקר. אני מתלבש ואוכל ארוחת בוקר. אני שותה חלב ואוכל לחם עם גבינה. אחר כך אני הולך לבית ספר. אני אומר 'שלום' לחברים.",
        "content_ru": "Я встаю в семь утра. Я одеваюсь и ем завтрак. Пью молоко и ем хлеб с сыром. Потом иду в школу. Говорю «привет» друзьям.",
        "vocabulary_json": _j([{"word": "בוקר", "translation": "утро", "transliteration": "бОкер"}, {"word": "ארוחת בוקר", "translation": "завтрак", "transliteration": "арухАт бОкер"}, {"word": "חלב", "translation": "молоко", "transliteration": "халАв"}, {"word": "לחם", "translation": "хлеб", "transliteration": "лЕхем"}, {"word": "גבינה", "translation": "сыр", "transliteration": "гвинА"}]),
        "audio_url": None,
        "category": "story",
    },
    # 10. В автобусе
    {
        "level_id": 1,
        "title_he": "באוטובוס",
        "title_ru": "В автобусе",
        "content_he": "אני נוסע באוטובוס לבית ספר. האוטובוס מגיע בשמונה. אני עולה ויושב ליד החלון. הנסיעה לוקחת עשרים דקות. אני יורד בתחנה ליד בית הספר.",
        "content_ru": "Я еду в школу на автобусе. Автобус приходит в восемь. Я сажусь у окна. Поездка занимает двадцать минут. Я выхожу на остановке рядом со школой.",
        "vocabulary_json": _j([{"word": "אוטובוס", "translation": "автобус", "transliteration": "отобУс"}, {"word": "תחנה", "translation": "остановка", "transliteration": "таханА"}, {"word": "נסיעה", "translation": "поездка", "transliteration": "несиА"}, {"word": "דקות", "translation": "минуты", "transliteration": "дакОт"}, {"word": "חלון", "translation": "окно", "transliteration": "халОн"}]),
        "audio_url": None,
        "category": "story",
    },
    # 11. В библиотеке
    {
        "level_id": 1,
        "title_he": "בספריה",
        "title_ru": "В библиотеке",
        "content_he": "אני אוהב ללכת לספריה. יש שם הרבה ספרים. אני בוחר ספר ויושב לקרוא. הספרנית עוזרת לי למצוא ספרים. אני משאיל ספרים לשבוע.",
        "content_ru": "Я люблю ходить в библиотеку. Там много книг. Я выбираю книгу и сажусь читать. Библиотекарь помогает мне найти книги. Я беру книги на неделю.",
        "vocabulary_json": _j([{"word": "ספריה", "translation": "библиотека", "transliteration": "сифриЯ"}, {"word": "ספרים", "translation": "книги", "transliteration": "сфарИм"}, {"word": "ספרנית", "translation": "библиотекарь (ж)", "transliteration": "сафранИт"}, {"word": "לקרוא", "translation": "читать", "transliteration": "ликрО"}, {"word": "משאיל", "translation": "берёт взаймы", "transliteration": "машИль"}]),
        "audio_url": None,
        "category": "story",
    },
    # 12. На пляже
    {
        "level_id": 1,
        "title_he": "בחוף הים",
        "title_ru": "На пляже",
        "content_he": "בקיץ אנחנו הולכים לחוף הים. המים כחולים ויפים. אני שוחה ומשחק בחול. אבא בונה ארמון חול. אמא שוכבת בשמש. הים נפלא.",
        "content_ru": "Летом мы ходим на пляж. Вода голубая и красивая. Я плаваю и играю в песке. Папа строит замок из песка. Мама загорает. Море прекрасно.",
        "vocabulary_json": _j([{"word": "חוף", "translation": "пляж", "transliteration": "хоф"}, {"word": "ים", "translation": "море", "transliteration": "ям"}, {"word": "חול", "translation": "песок", "transliteration": "холь"}, {"word": "שוחה", "translation": "плавает", "transliteration": "сохЕ"}, {"word": "שמש", "translation": "солнце", "transliteration": "шЕмеш"}]),
        "audio_url": None,
        "category": "story",
    },
    # 13. В ресторане
    {
        "level_id": 1,
        "title_he": "במסעדה",
        "title_ru": "В ресторане",
        "content_he": "אנחנו הולכים למסעדה. אני מזמין שניצל עם אורז. אבא אוכל סלט. אמא שותה מיץ תפוזים. האוכל טעים מאוד. אנחנו משלמים ויוצאים.",
        "content_ru": "Мы идём в ресторан. Я заказываю шницель с рисом. Папа ест салат. Мама пьёт апельсиновый сок. Еда очень вкусная. Мы платим и выходим.",
        "vocabulary_json": _j([{"word": "מסעדה", "translation": "ресторан", "transliteration": "мисадА"}, {"word": "שניצל", "translation": "шницель", "transliteration": "шнИцель"}, {"word": "אורז", "translation": "рис", "transliteration": "Орез"}, {"word": "מיץ", "translation": "сок", "transliteration": "миц"}, {"word": "טעים", "translation": "вкусный", "transliteration": "таИм"}]),
        "audio_url": None,
        "category": "story",
    },
    # 14. Праздник Песах
    {
        "level_id": 1,
        "title_he": "חג פסח",
        "title_ru": "Праздник Песах",
        "content_he": "פסח הוא חג חשוב בישראל. אנחנו עושים סדר. אנחנו אוכלים מצות. סבא מספר את הסיפור של יציאת מצרים. כל המשפחה ביחד.",
        "content_ru": "Песах — важный праздник в Израиле. Мы проводим седер. Мы едим мацу. Дедушка рассказывает историю исхода из Египта. Вся семья вместе.",
        "vocabulary_json": _j([{"word": "חג", "translation": "праздник", "transliteration": "хаг"}, {"word": "סדר", "translation": "седер", "transliteration": "сЕдер"}, {"word": "מצות", "translation": "маца", "transliteration": "мацОт"}, {"word": "סבא", "translation": "дедушка", "transliteration": "сАба"}, {"word": "משפחה", "translation": "семья", "transliteration": "мишпахА"}]),
        "audio_url": None,
        "category": "story",
    },
    # 15. Мой друг
    {
        "level_id": 1,
        "title_he": "החבר שלי",
        "title_ru": "Мой друг",
        "content_he": "יש לי חבר טוב. שמו יוסי. אנחנו לומדים ביחד ומשחקים אחרי בית ספר. יוסי גר ליד הבית שלי. הוא אוהב כדורסל ואני אוהב כדורגל.",
        "content_ru": "У меня есть хороший друг. Его зовут Йоси. Мы учимся вместе и играем после школы. Йоси живёт рядом с моим домом. Он любит баскетбол, а я — футбол.",
        "vocabulary_json": _j([{"word": "חבר", "translation": "друг", "transliteration": "хавЕр"}, {"word": "ביחד", "translation": "вместе", "transliteration": "бейЯхад"}, {"word": "גר", "translation": "живёт", "transliteration": "гар"}, {"word": "כדורסל", "translation": "баскетбол", "transliteration": "кадурсАль"}, {"word": "אחרי", "translation": "после", "transliteration": "ахарЕй"}]),
        "audio_url": None,
        "category": "story",
    },
    # 16. На улице
    {
        "level_id": 1,
        "title_he": "ברחוב",
        "title_ru": "На улице",
        "content_he": "אני הולך ברחוב. יש הרבה מכוניות ואנשים. אני רואה חנות עם צעצועים. ליד החנות יש בית קפה. אנשים יושבים ושותים קפה.",
        "content_ru": "Я иду по улице. Много машин и людей. Я вижу магазин с игрушками. Рядом с магазином есть кафе. Люди сидят и пьют кофе.",
        "vocabulary_json": _j([{"word": "רחוב", "translation": "улица", "transliteration": "рехОв"}, {"word": "מכוניות", "translation": "машины", "transliteration": "мехонийОт"}, {"word": "חנות", "translation": "магазин", "transliteration": "ханУт"}, {"word": "צעצועים", "translation": "игрушки", "transliteration": "цаацуИм"}, {"word": "קפה", "translation": "кофе", "transliteration": "кафЕ"}]),
        "audio_url": None,
        "category": "story",
    },
    # 17. Погода
    {
        "level_id": 1,
        "title_he": "מזג אוויר",
        "title_ru": "Погода",
        "content_he": "היום חם בחוץ. השמש זורחת. אין עננים בשמיים. אני שם כובע על הראש. אני שותה הרבה מים כי חם. בערב יהיה קריר יותר.",
        "content_ru": "Сегодня жарко на улице. Солнце светит. В небе нет облаков. Я надеваю шапку. Пью много воды, потому что жарко. Вечером будет прохладнее.",
        "vocabulary_json": _j([{"word": "מזג אוויר", "translation": "погода", "transliteration": "мЕзег авИр"}, {"word": "שמש", "translation": "солнце", "transliteration": "шЕмеш"}, {"word": "עננים", "translation": "облака", "transliteration": "ананИм"}, {"word": "כובע", "translation": "шапка", "transliteration": "ковА"}, {"word": "קריר", "translation": "прохладный", "transliteration": "карИр"}]),
        "audio_url": None,
        "category": "story",
    },
    # 18. Наш сад
    {
        "level_id": 1,
        "title_he": "הגינה שלנו",
        "title_ru": "Наш сад",
        "content_he": "לבית שלנו יש גינה. בגינה יש עצים ופרחים. אמא שותלת ירקות. יש עגבניות, מלפפונים וחסה. אנחנו משקים את הגינה כל יום.",
        "content_ru": "У нашего дома есть сад. В саду деревья и цветы. Мама сажает овощи. Есть помидоры, огурцы и салат. Мы поливаем сад каждый день.",
        "vocabulary_json": _j([{"word": "גינה", "translation": "сад", "transliteration": "гинА"}, {"word": "עצים", "translation": "деревья", "transliteration": "эцИм"}, {"word": "פרחים", "translation": "цветы", "transliteration": "прахИм"}, {"word": "שותלת", "translation": "сажает", "transliteration": "шотЕлет"}, {"word": "משקים", "translation": "поливают", "transliteration": "машкИм"}]),
        "audio_url": None,
        "category": "story",
    },
    # 19. Мой отпуск
    {
        "level_id": 2,
        "title_he": "החופשה שלי",
        "title_ru": "Мой отпуск",
        "content_he": "בקיץ שעבר נסעתי עם המשפחה לאילת. טסנו במטוס ושהינו במלון ליד הים. כל יום שחינו בבריכה ובים. בערב אכלנו במסעדות שונות. זו הייתה חופשה נהדרת וכבר מתגעגעים.",
        "content_ru": "Прошлым летом я ездил с семьёй в Эйлат. Мы летели на самолёте и остановились в отеле у моря. Каждый день плавали в бассейне и море. Вечером ели в разных ресторанах. Это был отличный отпуск, уже скучаем.",
        "vocabulary_json": _j([{"word": "חופשה", "translation": "отпуск", "transliteration": "хуфшА"}, {"word": "מטוס", "translation": "самолёт", "transliteration": "матОс"}, {"word": "מלון", "translation": "отель", "transliteration": "малОн"}, {"word": "בריכה", "translation": "бассейн", "transliteration": "брехА"}, {"word": "מתגעגעים", "translation": "скучаем", "transliteration": "митгаагаИм"}]),
        "audio_url": None,
        "category": "story",
    },
    # 20. Новая квартира
    {
        "level_id": 2,
        "title_he": "הדירה החדשה",
        "title_ru": "Новая квартира",
        "content_he": "עברנו לדירה חדשה בתל אביב. הדירה גדולה ויפה. יש שלושה חדרים, מטבח ומרפסת. השכנים נחמדים מאוד. אנחנו עדיין מסדרים את הרהיטים. שמחים בבית החדש.",
        "content_ru": "Мы переехали в новую квартиру в Тель-Авиве. Квартира большая и красивая. Три комнаты, кухня и балкон. Соседи очень приветливые. Мы ещё расставляем мебель. Рады новому дому.",
        "vocabulary_json": _j([{"word": "דירה", "translation": "квартира", "transliteration": "дирА"}, {"word": "מטבח", "translation": "кухня", "transliteration": "митбАх"}, {"word": "מרפסת", "translation": "балкон", "transliteration": "мирпЕсет"}, {"word": "שכנים", "translation": "соседи", "transliteration": "шхенИм"}, {"word": "רהיטים", "translation": "мебель", "transliteration": "рахитИм"}]),
        "audio_url": None,
        "category": "story",
    },
    # 21. Собеседование
    {
        "level_id": 2,
        "title_he": "ראיון עבודה",
        "title_ru": "Собеседование",
        "content_he": "אתמול הלכתי לראיון עבודה. הגעתי למשרד בזמן. המנהלת שאלה אותי שאלות על הניסיון שלי. סיפרתי לה על העבודות הקודמות. אני מקווה שאקבל את המשרה.",
        "content_ru": "Вчера я ходил на собеседование. Пришёл в офис вовремя. Менеджер задала мне вопросы об опыте. Я рассказал ей о предыдущих работах. Надеюсь, получу эту должность.",
        "vocabulary_json": _j([{"word": "ראיון", "translation": "собеседование", "transliteration": "раайОн"}, {"word": "משרד", "translation": "офис", "transliteration": "мисрАд"}, {"word": "מנהלת", "translation": "менеджер (ж)", "transliteration": "менаhЕлет"}, {"word": "ניסיון", "translation": "опыт", "transliteration": "нисайОн"}, {"word": "משרה", "translation": "должность", "transliteration": "масрА"}]),
        "audio_url": None,
        "category": "story",
    },
    # 22. Домашняя готовка
    {
        "level_id": 2,
        "title_he": "בישול ביתי",
        "title_ru": "Домашняя готовка",
        "content_he": "אני אוהב לבשל. היום הכנתי עוף עם ירקות. קודם קניתי ירקות טריים בשוק. חתכתי בצל, גזר ותפוחי אדמה. שמתי הכול בתנור ואחרי שעה האוכל היה מוכן.",
        "content_ru": "Я люблю готовить. Сегодня приготовил курицу с овощами. Сначала купил свежие овощи на рынке. Нарезал лук, морковь и картофель. Всё поставил в духовку, и через час еда была готова.",
        "vocabulary_json": _j([{"word": "לבשל", "translation": "готовить", "transliteration": "левашЕль"}, {"word": "עוף", "translation": "курица", "transliteration": "оф"}, {"word": "ירקות", "translation": "овощи", "transliteration": "йеракОт"}, {"word": "תנור", "translation": "духовка", "transliteration": "танУр"}, {"word": "מוכן", "translation": "готовый", "transliteration": "мухАн"}]),
        "audio_url": None,
        "category": "story",
    },
    # 23. Спорт и фитнес
    {
        "level_id": 2,
        "title_he": "ספורט וכושר",
        "title_ru": "Спорт и фитнес",
        "content_he": "אני מתאמן שלוש פעמים בשבוע. הולך לחדר כושר ליד הבית. גם רץ בפארק בבקרים. ספורט חשוב לבריאות. אחרי אימון אני מרגיש מלא אנרגיה. שומר על אורח חיים בריא.",
        "content_ru": "Я тренируюсь три раза в неделю. Хожу в спортзал рядом с домом. Также бегаю в парке по утрам. Спорт важен для здоровья. После тренировки чувствую себя полным энергии. Веду здоровый образ жизни.",
        "vocabulary_json": _j([{"word": "מתאמן", "translation": "тренируюсь", "transliteration": "митамЕн"}, {"word": "חדר כושר", "translation": "спортзал", "transliteration": "хЕдер кОшер"}, {"word": "בריאות", "translation": "здоровье", "transliteration": "бриУт"}, {"word": "אימון", "translation": "тренировка", "transliteration": "имУн"}, {"word": "אנרגיה", "translation": "энергия", "transliteration": "энЕргия"}]),
        "audio_url": None,
        "category": "story",
    },
    # 24. Поход в музей
    {
        "level_id": 2,
        "title_he": "ביקור במוזיאון",
        "title_ru": "Поход в музей",
        "content_he": "ביום שישי ביקרנו במוזיאון ישראל בירושלים. ראינו אוספים של אמנות עתיקה ומודרנית. הילדים התרגשו מאוד מהתערוכה. קנינו מזכרות בחנות המוזיאון. זה היה יום מעניין.",
        "content_ru": "В пятницу мы посетили Музей Израиля в Иерусалиме. Видели коллекции древнего и современного искусства. Дети очень впечатлились выставкой. Купили сувениры в магазине музея. Это был интересный день.",
        "vocabulary_json": _j([{"word": "מוזיאון", "translation": "музей", "transliteration": "музеОн"}, {"word": "אמנות", "translation": "искусство", "transliteration": "оманУт"}, {"word": "תערוכה", "translation": "выставка", "transliteration": "тааруХА"}, {"word": "מזכרות", "translation": "сувениры", "transliteration": "мазкарОт"}, {"word": "עתיקה", "translation": "древняя", "transliteration": "атикА"}]),
        "audio_url": None,
        "category": "story",
    },
    # 25. Дождливый день
    {
        "level_id": 2,
        "title_he": "יום גשום",
        "title_ru": "Дождливый день",
        "content_he": "היום ירד גשם חזק. לקחתי מטריה ומעיל גשם. ברחוב היו שלוליות מים. מכוניות נסעו לאט. ישבתי בבית קפה ושתיתי שוקו חם. היום הגשום היה נעים בסוף.",
        "content_ru": "Сегодня шёл сильный дождь. Я взял зонт и дождевик. На улице были лужи. Машины ехали медленно. Сидел в кафе и пил горячее какао. Дождливый день в итоге оказался приятным.",
        "vocabulary_json": _j([{"word": "גשם", "translation": "дождь", "transliteration": "гЕшем"}, {"word": "מטריה", "translation": "зонт", "transliteration": "митриЯ"}, {"word": "מעיל", "translation": "куртка", "transliteration": "меИль"}, {"word": "שלוליות", "translation": "лужи", "transliteration": "шлулийОт"}, {"word": "שוקו", "translation": "какао", "transliteration": "шОко"}]),
        "audio_url": None,
        "category": "story",
    },
    # 26. Свадьба
    {
        "level_id": 2,
        "title_he": "חתונה",
        "title_ru": "Свадьба",
        "content_he": "היינו בחתונה של חברה. הטקס היה בגן אירועים יפה. הכלה לבשה שמלה לבנה. הם רקדו ושרו כל הלילה. האוכל היה מעולה. שמחנו איתם.",
        "content_ru": "Мы были на свадьбе подруги. Церемония была в красивом банкетном зале. Невеста была в белом платье. Они танцевали и пели всю ночь. Еда была отличная. Мы радовались вместе с ними.",
        "vocabulary_json": _j([{"word": "חתונה", "translation": "свадьба", "transliteration": "хатунА"}, {"word": "טקס", "translation": "церемония", "transliteration": "тЕкес"}, {"word": "כלה", "translation": "невеста", "transliteration": "калА"}, {"word": "שמלה", "translation": "платье", "transliteration": "симлА"}, {"word": "רקדו", "translation": "танцевали", "transliteration": "ракдУ"}]),
        "audio_url": None,
        "category": "story",
    },
    # 27. В торговом центре
    {
        "level_id": 2,
        "title_he": "בקניון",
        "title_ru": "В торговом центре",
        "content_he": "הלכנו לקניון ביום שישי. קניתי חולצה חדשה ונעליים. אשתי בחרה תיק. הילדים רצו לחנות צעצועים. אכלנו ביחד בקומה השלישית. הקניון היה מלא אנשים.",
        "content_ru": "Пошли в торговый центр в пятницу. Я купил новую рубашку и обувь. Жена выбрала сумку. Дети побежали в магазин игрушек. Вместе ели на третьем этаже. Центр был полон людей.",
        "vocabulary_json": _j([{"word": "קניון", "translation": "торговый центр", "transliteration": "каньОн"}, {"word": "חולצה", "translation": "рубашка", "transliteration": "хулцА"}, {"word": "נעליים", "translation": "обувь", "transliteration": "наалАйим"}, {"word": "תיק", "translation": "сумка", "transliteration": "тик"}, {"word": "קומה", "translation": "этаж", "transliteration": "комА"}]),
        "audio_url": None,
        "category": "story",
    },
    # 28. Вождение в Израиле
    {
        "level_id": 2,
        "title_he": "נהיגה בישראל",
        "title_ru": "Вождение в Израиле",
        "content_he": "קיבלתי רישיון נהיגה לפני חודש. נהגתי לראשונה לבד בכביש. בהתחלה היה קשה אבל עכשיו אני מרגיש בטוח. הכבישים בישראל עמוסים. צריך לנהוג בזהירות.",
        "content_ru": "Я получил водительские права месяц назад. Впервые ехал один по дороге. Сначала было сложно, но теперь чувствую себя уверенно. Дороги в Израиле загружены. Нужно водить осторожно.",
        "vocabulary_json": _j([{"word": "רישיון", "translation": "права/лицензия", "transliteration": "ришайОн"}, {"word": "נהיגה", "translation": "вождение", "transliteration": "неhигА"}, {"word": "כביש", "translation": "дорога", "transliteration": "квИш"}, {"word": "בטוח", "translation": "уверенный", "transliteration": "батУах"}, {"word": "זהירות", "translation": "осторожность", "transliteration": "зеhирУт"}]),
        "audio_url": None,
        "category": "story",
    },
    # 29. В саду
    {
        "level_id": 2,
        "title_he": "בגינה",
        "title_ru": "В саду",
        "content_he": "אני מטפל בגינה שלי. שתלתי עגבניות ומלפפונים. כל בוקר אני משקה את הצמחים. אחרי שבועיים ראיתי פרחים. בעוד חודש יהיו ירקות טריים. גינה זה תחביב נהדר.",
        "content_ru": "Я ухаживаю за своим садом. Посадил помидоры и огурцы. Каждое утро поливаю растения. Через две недели увидел цветы. Через месяц будут свежие овощи. Сад — отличное хобби.",
        "vocabulary_json": _j([{"word": "גינה", "translation": "сад", "transliteration": "гинА"}, {"word": "שתלתי", "translation": "я посадил", "transliteration": "шатАльти"}, {"word": "משקה", "translation": "поливает", "transliteration": "машкЕ"}, {"word": "צמחים", "translation": "растения", "transliteration": "цмахИм"}, {"word": "תחביב", "translation": "хобби", "transliteration": "тахбИв"}]),
        "audio_url": None,
        "category": "story",
    },
    # 30. В кинотеатре
    {
        "level_id": 2,
        "title_he": "בקולנוע",
        "title_ru": "В кинотеатре",
        "content_he": "ביום חמישי הלכנו לקולנוע. בחרנו סרט קומדיה ישראלי. קנינו פופקורן ושתייה. הסרט היה מצחיק מאוד. צחקנו כל הזמן. אחרי הסרט דיברנו עליו בבית קפה.",
        "content_ru": "В четверг пошли в кино. Выбрали израильскую комедию. Купили попкорн и напитки. Фильм был очень смешной. Мы смеялись всё время. После фильма обсуждали его в кафе.",
        "vocabulary_json": _j([{"word": "קולנוע", "translation": "кинотеатр", "transliteration": "кольнОа"}, {"word": "סרט", "translation": "фильм", "transliteration": "сЕрет"}, {"word": "קומדיה", "translation": "комедия", "transliteration": "комЕдия"}, {"word": "פופקורן", "translation": "попкорн", "transliteration": "попкОрн"}, {"word": "מצחיק", "translation": "смешной", "transliteration": "мацхИк"}]),
        "audio_url": None,
        "category": "story",
    },
    # 31. В банке
    {
        "level_id": 2,
        "title_he": "בבנק",
        "title_ru": "В банке",
        "content_he": "הלכתי לבנק לפתוח חשבון חדש. הפקידה הסבירה לי על סוגי החשבונות. בחרתי חשבון עם כרטיס אשראי. מילאתי טפסים ונתתי תעודת זהות. אחרי חצי שעה הכול היה מוכן.",
        "content_ru": "Пошёл в банк открыть новый счёт. Служащая объяснила мне виды счетов. Выбрал счёт с кредитной картой. Заполнил формы и дал удостоверение личности. Через полчаса всё было готово.",
        "vocabulary_json": _j([{"word": "בנק", "translation": "банк", "transliteration": "банк"}, {"word": "חשבון", "translation": "счёт", "transliteration": "хешбОн"}, {"word": "פקידה", "translation": "служащая", "transliteration": "пкидА"}, {"word": "כרטיס אשראי", "translation": "кредитная карта", "transliteration": "картИс ашрАй"}, {"word": "תעודת זהות", "translation": "удостоверение личности", "transliteration": "теудАт зеhУт"}]),
        "audio_url": None,
        "category": "story",
    },
    # 32. На почте
    {
        "level_id": 2,
        "title_he": "בדואר",
        "title_ru": "На почте",
        "content_he": "שלחתי חבילה לחברה בחו\"ל. עמדתי בתור עשר דקות. הפקיד שקל את החבילה. שילמתי שישים שקלים על המשלוח. החבילה תגיע בעוד שבוע. קיבלתי קבלה.",
        "content_ru": "Отправил посылку подруге за границу. Стоял в очереди десять минут. Служащий взвесил посылку. Заплатил шестьдесят шекелей за доставку. Посылка дойдёт через неделю. Получил квитанцию.",
        "vocabulary_json": _j([{"word": "חבילה", "translation": "посылка", "transliteration": "хавилА"}, {"word": "חו\"ל", "translation": "заграница", "transliteration": "хуль"}, {"word": "תור", "translation": "очередь", "transliteration": "тор"}, {"word": "משלוח", "translation": "доставка", "transliteration": "мишлОах"}, {"word": "קבלה", "translation": "квитанция", "transliteration": "каблА"}]),
        "audio_url": None,
        "category": "story",
    },
    # 33. Концерт
    {
        "level_id": 2,
        "title_he": "הופעה",
        "title_ru": "Концерт",
        "content_he": "הלכנו להופעה של זמר ישראלי מפורסם. האולם היה מלא. הוא שר את כל השירים הידועים. הקהל שר איתו ורקד. ההופעה נמשכה שעתיים. היה מדהים.",
        "content_ru": "Пошли на концерт известного израильского певца. Зал был полон. Он спел все известные песни. Публика пела с ним и танцевала. Концерт длился два часа. Было потрясающе.",
        "vocabulary_json": _j([{"word": "הופעה", "translation": "концерт/выступление", "transliteration": "hофаА"}, {"word": "זמר", "translation": "певец", "transliteration": "замАр"}, {"word": "מפורסם", "translation": "известный", "transliteration": "мефурсАм"}, {"word": "קהל", "translation": "публика", "transliteration": "каhАль"}, {"word": "מדהים", "translation": "потрясающий", "transliteration": "мадhИм"}]),
        "audio_url": None,
        "category": "story",
    },
    # 34. Кемпинг
    {
        "level_id": 2,
        "title_he": "קמפינג",
        "title_ru": "Кемпинг",
        "content_he": "בסוף שבוע נסענו לקמפינג בגליל. הקמנו אוהל ליד נחל. בישלנו על מדורה ואכלנו בחוץ. בלילה ראינו כוכבים רבים. בבוקר טיילנו בשביל ההר. חוויה יפה.",
        "content_ru": "В выходные поехали в кемпинг в Галилее. Поставили палатку у ручья. Готовили на костре и ели на природе. Ночью видели много звёзд. Утром гуляли по горной тропе. Красивый опыт.",
        "vocabulary_json": _j([{"word": "קמפינג", "translation": "кемпинг", "transliteration": "кЕмпинг"}, {"word": "אוהל", "translation": "палатка", "transliteration": "Оhель"}, {"word": "מדורה", "translation": "костёр", "transliteration": "медурА"}, {"word": "כוכבים", "translation": "звёзды", "transliteration": "кохавИм"}, {"word": "שביל", "translation": "тропа", "transliteration": "швиль"}]),
        "audio_url": None,
        "category": "story",
    },
    # 35. В аэропорту
    {
        "level_id": 2,
        "title_he": "בשדה התעופה",
        "title_ru": "В аэропорту",
        "content_he": "הגענו לשדה התעופה שלוש שעות לפני הטיסה. עברנו ביקורת ביטחון. הראינו דרכון וכרטיס טיסה. המזוודות נשלחו דרך הסרט. חיכינו בטרמינל ועלינו למטוס.",
        "content_ru": "Приехали в аэропорт за три часа до вылета. Прошли проверку безопасности. Показали паспорт и посадочный. Чемоданы отправили через ленту. Ждали в терминале и сели в самолёт.",
        "vocabulary_json": _j([{"word": "שדה תעופה", "translation": "аэропорт", "transliteration": "сдЕ теуфА"}, {"word": "ביטחון", "translation": "безопасность", "transliteration": "битахОн"}, {"word": "דרכון", "translation": "паспорт", "transliteration": "даркОн"}, {"word": "מזוודות", "translation": "чемоданы", "transliteration": "мизвадОт"}, {"word": "טיסה", "translation": "рейс/полёт", "transliteration": "тисА"}]),
        "audio_url": None,
        "category": "story",
    },
    # 36. Наш район
    {
        "level_id": 2,
        "title_he": "השכונה שלנו",
        "title_ru": "Наш район",
        "content_he": "אנחנו גרים בשכונה שקטה. יש פארק קטן עם עצים. ליד הבית יש מכולת ובית מרקחת. השכנים ידידותיים. בערב אנשים יוצאים לטייל. אני אוהב את השכונה.",
        "content_ru": "Мы живём в тихом районе. Есть маленький парк с деревьями. Рядом с домом продуктовый и аптека. Соседи дружелюбные. Вечером люди выходят гулять. Мне нравится район.",
        "vocabulary_json": _j([{"word": "שכונה", "translation": "район", "transliteration": "шхунА"}, {"word": "שקטה", "translation": "тихая", "transliteration": "шкетА"}, {"word": "מכולת", "translation": "продуктовый", "transliteration": "маколЕт"}, {"word": "בית מרקחת", "translation": "аптека", "transliteration": "бейт миркАхат"}, {"word": "ידידותיים", "translation": "дружелюбные", "transliteration": "йедидутийИм"}]),
        "audio_url": None,
        "category": "story",
    },
    # 37. Потерянная вещь
    {
        "level_id": 2,
        "title_he": "אבדה ומציאה",
        "title_ru": "Потерянная вещь",
        "content_he": "אתמול איבדתי את הארנק שלי באוטובוס. התקשרתי לחברת האוטובוסים. הם אמרו לבדוק במשרד אבדות ומציאות. הלכתי לשם ומצאתי את הארנק. שמחתי מאוד. כל הכסף היה בפנים.",
        "content_ru": "Вчера потерял кошелёк в автобусе. Позвонил в автобусную компанию. Сказали проверить в бюро находок. Пошёл туда и нашёл кошелёк. Очень обрадовался. Все деньги были на месте.",
        "vocabulary_json": _j([{"word": "ארנק", "translation": "кошелёк", "transliteration": "арнАк"}, {"word": "איבדתי", "translation": "я потерял", "transliteration": "ивАдти"}, {"word": "אבדות ומציאות", "translation": "бюро находок", "transliteration": "аведОт у-мециОт"}, {"word": "כסף", "translation": "деньги", "transliteration": "кЕсеф"}, {"word": "מצאתי", "translation": "я нашёл", "transliteration": "мацАти"}]),
        "audio_url": None,
        "category": "story",
    },
    # 38. Новый год
    {
        "level_id": 2,
        "title_he": "ראש השנה",
        "title_ru": "Новый год",
        "content_he": "ראש השנה הוא חג חשוב. אנחנו אוכלים תפוח בדבש לשנה מתוקה. הולכים לבית כנסת. אומרים 'שנה טובה' לכולם. בערב יש ארוחה גדולה עם המשפחה. מקווים לשנה טובה.",
        "content_ru": "Рош а-Шана — важный праздник. Мы едим яблоко в мёде для сладкого года. Ходим в синагогу. Говорим всем «шана това». Вечером большой ужин с семьёй. Надеемся на хороший год.",
        "vocabulary_json": _j([{"word": "ראש השנה", "translation": "Новый год", "transliteration": "рош hа-шанА"}, {"word": "דבש", "translation": "мёд", "transliteration": "двАш"}, {"word": "בית כנסת", "translation": "синагога", "transliteration": "бейт кнЕсет"}, {"word": "שנה טובה", "translation": "хорошего года", "transliteration": "шанА товА"}, {"word": "ארוחה", "translation": "трапеза", "transliteration": "арухА"}]),
        "audio_url": None,
        "category": "story",
    },
    # 39. Телефонный разговор
    {
        "level_id": 2,
        "title_he": "שיחת טלפון",
        "title_ru": "Телефонный разговор",
        "content_he": "התקשרתי לחבר לשאול אם הוא רוצה לבוא. הוא ענה ואמר שהוא עסוק. קבענו להיפגש מחר. דיברנו כמה דקות על העבודה. הוא סיפר לי חדשות מעניינות. סיימנו את השיחה.",
        "content_ru": "Позвонил другу спросить, хочет ли он прийти. Он ответил, что занят. Договорились встретиться завтра. Поговорили несколько минут о работе. Он рассказал мне интересные новости. Закончили разговор.",
        "vocabulary_json": _j([{"word": "התקשרתי", "translation": "я позвонил", "transliteration": "hиткашАрти"}, {"word": "עסוק", "translation": "занят", "transliteration": "асУк"}, {"word": "קבענו", "translation": "мы договорились", "transliteration": "кавАну"}, {"word": "שיחה", "translation": "разговор", "transliteration": "сихА"}, {"word": "חדשות", "translation": "новости", "transliteration": "хадашОт"}]),
        "audio_url": None,
        "category": "story",
    },
    # 40. Опоздавший автобус
    {
        "level_id": 2,
        "title_he": "אוטובוס מאחר",
        "title_ru": "Опоздавший автобус",
        "content_he": "חיכיתי לאוטובוס חצי שעה. הוא איחר בגלל פקקים. כשהגיע, היה מלא אנשים. עמדתי כל הדרך. הגעתי לעבודה מאוחר. אמרתי למנהל שהאוטובוס איחר והוא הבין.",
        "content_ru": "Ждал автобус полчаса. Он опоздал из-за пробок. Когда приехал, был полон людей. Стоял всю дорогу. Приехал на работу поздно. Сказал начальнику, что автобус опоздал, и он понял.",
        "vocabulary_json": _j([{"word": "חיכיתי", "translation": "я ждал", "transliteration": "хикИти"}, {"word": "איחר", "translation": "опоздал", "transliteration": "ихЕр"}, {"word": "פקקים", "translation": "пробки", "transliteration": "пкакИм"}, {"word": "מאוחר", "translation": "поздно", "transliteration": "меухАр"}, {"word": "מנהל", "translation": "начальник", "transliteration": "менаhЕль"}]),
        "audio_url": None,
        "category": "story",
    },
    # 41. Встреча с другом
    {
        "level_id": 2,
        "title_he": "פגישה עם חבר",
        "title_ru": "Встреча с другом",
        "content_he": "נפגשתי עם חבר ישן בקפה. לא ראינו אחד את השני שנתיים. הוא סיפר שהוא עובד בחברת הייטק. אני סיפרתי על המשפחה. שתינו קפה ואכלנו עוגה. הבטחנו להיפגש שוב.",
        "content_ru": "Встретился со старым другом в кафе. Не виделись два года. Он рассказал, что работает в хайтек-компании. Я рассказал о семье. Пили кофе и ели торт. Обещали встретиться снова.",
        "vocabulary_json": _j([{"word": "נפגשתי", "translation": "я встретился", "transliteration": "нифгАшти"}, {"word": "חבר ישן", "translation": "старый друг", "transliteration": "хавЕр яшАн"}, {"word": "הייטק", "translation": "хайтек", "transliteration": "hайтЕк"}, {"word": "הבטחנו", "translation": "мы обещали", "transliteration": "hивтАхну"}, {"word": "שוב", "translation": "снова", "transliteration": "шув"}]),
        "audio_url": None,
        "category": "story",
    },
    # 42. Переменчивая погода
    {
        "level_id": 2,
        "title_he": "מזג אוויר משתנה",
        "title_ru": "Переменчивая погода",
        "content_he": "הבוקר היה שמש ויצאתי בלי מעיל. אחר הצהריים התחיל גשם חזק. נרטבתי לגמרי. רצתי לחנות קרובה. קניתי מטריה זולה. למדתי שבישראל צריך תמיד לקחת מטריה בחורף.",
        "content_ru": "Утром было солнечно и я вышел без куртки. Днём начался сильный дождь. Промок насквозь. Забежал в ближайший магазин. Купил дешёвый зонт. Понял, что в Израиле зимой всегда нужен зонт.",
        "vocabulary_json": _j([{"word": "שמש", "translation": "солнце", "transliteration": "шЕмеш"}, {"word": "מעיל", "translation": "куртка", "transliteration": "меИль"}, {"word": "נרטבתי", "translation": "я промок", "transliteration": "ниртАвти"}, {"word": "מטריה", "translation": "зонт", "transliteration": "митриЯ"}, {"word": "חורף", "translation": "зима", "transliteration": "хОреф"}]),
        "audio_url": None,
        "category": "story",
    },
]


def upgrade() -> None:
    op.execute(
        "SELECT setval('reading_texts_id_seq', "
        "GREATEST(COALESCE((SELECT MAX(id) FROM reading_texts), 0), 1))"
    )
    op.bulk_insert(reading_texts_table, TEXTS)


def downgrade() -> None:
    _titles = ["В школе", "Домашние питомцы", "Времена года", "День рождения", "Моя комната", "В парке", "На рынке", "У врача", "Доброе утро", "В автобусе", "В библиотеке", "На пляже", "В ресторане", "Праздник Песах", "Мой друг", "На улице", "Погода", "Наш сад", "Мой отпуск", "Новая квартира", "Собеседование", "Домашняя готовка", "Спорт и фитнес", "Поход в музей", "Дождливый день", "Свадьба", "В торговом центре", "Вождение в Израиле", "В саду", "В кинотеатре", "В банке", "На почте", "Концерт", "Кемпинг", "В аэропорту", "Наш район", "Потерянная вещь", "Новый год", "Телефонный разговор", "Опоздавший автобус", "Встреча с другом", "Переменчивая погода"]
    for _t in _titles:
        op.execute(sa.text("DELETE FROM reading_texts WHERE title_ru = :t").bindparams(t=_t))
    op.execute(
        "SELECT setval('reading_texts_id_seq', "
        "GREATEST(COALESCE((SELECT MAX(id) FROM reading_texts), 0), 1))"
    )
