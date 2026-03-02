"""Stage 5: Gamification definitions, culture articles, user activity tracking

Revision ID: 004
Revises: 003
Create Date: 2026-03-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ── Achievement definitions ────────────────────────────────────────────────
# Stored in a new table so backend can check them
ACHIEVEMENT_DEFS = [
    # (code, title_ru, description_ru, icon, category, condition_json)
    # First steps
    ("first_login", "Первый вход", "Зайдите в приложение", "🎉", "general", {"type": "login", "count": 1}),
    ("first_word", "Первое слово", "Изучите первое слово", "📖", "vocabulary", {"type": "words_learned", "count": 1}),
    ("first_card", "Первая карточка", "Создайте первую SRS-карточку", "🃏", "srs", {"type": "cards_created", "count": 1}),
    ("first_review", "Первый повтор", "Повторите первую карточку", "✅", "srs", {"type": "reviews", "count": 1}),
    ("first_exercise", "Первое упражнение", "Выполните первое упражнение", "✏️", "exercises", {"type": "exercises_done", "count": 1}),
    ("first_text", "Первый текст", "Прочитайте первый текст", "📄", "reading", {"type": "texts_read", "count": 1}),
    ("first_dialogue", "Первый диалог", "Пройдите первый диалог", "💬", "dialogues", {"type": "dialogues_done", "count": 1}),
    # Vocabulary milestones
    ("words_10", "10 слов", "Изучите 10 слов", "📗", "vocabulary", {"type": "words_learned", "count": 10}),
    ("words_50", "50 слов", "Изучите 50 слов", "📘", "vocabulary", {"type": "words_learned", "count": 50}),
    ("words_100", "100 слов", "Изучите 100 слов", "📙", "vocabulary", {"type": "words_learned", "count": 100}),
    ("words_250", "250 слов", "Изучите 250 слов", "📕", "vocabulary", {"type": "words_learned", "count": 250}),
    ("words_500", "500 слов", "Изучите 500 слов", "🏅", "vocabulary", {"type": "words_learned", "count": 500}),
    ("words_1000", "1000 слов", "Изучите 1000 слов", "🥇", "vocabulary", {"type": "words_learned", "count": 1000}),
    # SRS milestones
    ("reviews_10", "10 повторов", "Повторите 10 карточек", "🔁", "srs", {"type": "reviews", "count": 10}),
    ("reviews_50", "50 повторов", "Повторите 50 карточек", "🔄", "srs", {"type": "reviews", "count": 50}),
    ("reviews_100", "100 повторов", "Повторите 100 карточек", "💯", "srs", {"type": "reviews", "count": 100}),
    ("reviews_500", "500 повторов", "Повторите 500 карточек", "🌟", "srs", {"type": "reviews", "count": 500}),
    ("perfect_session", "Идеальная сессия", "Ответьте на все карточки правильно за сессию", "⭐", "srs", {"type": "perfect_session", "count": 1}),
    # Exercises
    ("exercises_10", "10 упражнений", "Выполните 10 упражнений", "📝", "exercises", {"type": "exercises_done", "count": 10}),
    ("exercises_50", "50 упражнений", "Выполните 50 упражнений", "📋", "exercises", {"type": "exercises_done", "count": 50}),
    ("exercises_100", "100 упражнений", "Выполните 100 упражнений", "🎯", "exercises", {"type": "exercises_done", "count": 100}),
    ("exercises_correct_10", "10 правильных", "Ответьте правильно 10 раз подряд", "🎯", "exercises", {"type": "correct_streak", "count": 10}),
    # Streaks
    ("streak_3", "3 дня подряд", "Занимайтесь 3 дня подряд", "🔥", "streak", {"type": "streak", "count": 3}),
    ("streak_7", "Неделя!", "Занимайтесь 7 дней подряд", "🔥", "streak", {"type": "streak", "count": 7}),
    ("streak_14", "2 недели!", "Занимайтесь 14 дней подряд", "🔥", "streak", {"type": "streak", "count": 14}),
    ("streak_30", "Месяц!", "Занимайтесь 30 дней подряд", "🔥", "streak", {"type": "streak", "count": 30}),
    ("streak_60", "2 месяца!", "Занимайтесь 60 дней подряд", "🔥", "streak", {"type": "streak", "count": 60}),
    ("streak_100", "100 дней!", "Занимайтесь 100 дней подряд", "🏆", "streak", {"type": "streak", "count": 100}),
    ("streak_365", "Год иврита!", "Занимайтесь 365 дней подряд", "👑", "streak", {"type": "streak", "count": 365}),
    # Alphabet
    ("all_letters", "Все буквы", "Изучите все 27 букв алфавита", "🔤", "alphabet", {"type": "letters_learned", "count": 27}),
    ("all_nikkud", "Все огласовки", "Изучите все 12 огласовок", "🅰️", "alphabet", {"type": "nikkud_learned", "count": 12}),
    # Grammar
    ("grammar_topic_1", "Первая тема", "Изучите первую тему грамматики", "📐", "grammar", {"type": "grammar_topics", "count": 1}),
    ("grammar_topics_6", "Алеф грамматика", "Изучите все 6 тем уровня Алеф", "📏", "grammar", {"type": "grammar_topics", "count": 6}),
    ("grammar_topics_12", "Мастер грамматики", "Изучите все 12 тем грамматики", "🏛️", "grammar", {"type": "grammar_topics", "count": 12}),
    # Reading
    ("texts_3", "3 текста", "Прочитайте 3 текста", "📰", "reading", {"type": "texts_read", "count": 3}),
    ("texts_5", "Все тексты", "Прочитайте все 5 текстов", "📚", "reading", {"type": "texts_read", "count": 5}),
    # Listening
    ("dictation_5", "5 диктантов", "Пройдите 5 диктантов", "🎧", "listening", {"type": "dictations_done", "count": 5}),
    ("dictation_20", "20 диктантов", "Пройдите 20 диктантов", "🎵", "listening", {"type": "dictations_done", "count": 20}),
    # Writing
    ("writing_5", "5 письменных", "Выполните 5 письменных упражнений", "✍️", "writing", {"type": "writing_done", "count": 5}),
    ("writing_20", "20 письменных", "Выполните 20 письменных упражнений", "📝", "writing", {"type": "writing_done", "count": 20}),
    # Dialogues
    ("dialogues_5", "5 диалогов", "Пройдите 5 диалогов", "🗣️", "dialogues", {"type": "dialogues_done", "count": 5}),
    ("dialogues_10", "10 диалогов", "Пройдите 10 диалогов", "💬", "dialogues", {"type": "dialogues_done", "count": 10}),
    ("dialogues_all", "Все диалоги", "Пройдите все 16 диалогов", "🌍", "dialogues", {"type": "dialogues_done", "count": 16}),
    # XP milestones
    ("xp_100", "100 XP", "Наберите 100 очков опыта", "⚡", "xp", {"type": "xp", "count": 100}),
    ("xp_500", "500 XP", "Наберите 500 очков опыта", "⚡", "xp", {"type": "xp", "count": 500}),
    ("xp_1000", "1000 XP", "Наберите 1000 очков опыта", "💎", "xp", {"type": "xp", "count": 1000}),
    ("xp_5000", "5000 XP", "Наберите 5000 очков опыта", "💎", "xp", {"type": "xp", "count": 5000}),
    # Level milestones
    ("level_2", "Уровень Бет", "Достигните уровня Бет", "🆙", "level", {"type": "level", "count": 2}),
    ("level_3", "Уровень Гимель", "Достигните уровня Гимель", "🆙", "level", {"type": "level", "count": 3}),
    ("level_4", "Уровень Далет", "Достигните уровня Далет", "🎖️", "level", {"type": "level", "count": 4}),
    # Culture
    ("culture_1", "Первая статья", "Прочитайте первую статью о культуре", "🕎", "culture", {"type": "culture_read", "count": 1}),
    ("culture_5", "5 статей", "Прочитайте 5 статей о культуре", "🇮🇱", "culture", {"type": "culture_read", "count": 5}),
    ("culture_all", "Знаток культуры", "Прочитайте все статьи о культуре", "🏛️", "culture", {"type": "culture_read", "count": 15}),
]

# ── Culture articles ───────────────────────────────────────────────────────
CULTURE_ARTICLES = [
    # (category, title_ru, title_he, content_md, level_id)
    # Holidays
    ("holiday", "Шаббат", "שַׁבָּת",
     "**Шаббат** (שַׁבָּת) — еженедельный день отдыха, с захода солнца в пятницу до выхода трёх звёзд в субботу.\n\n"
     "Традиции:\n"
     "- Зажигание свечей (הַדְלָקַת נֵרוֹת)\n"
     "- Кидуш над вином (קִידוּשׁ)\n"
     "- Хала — субботний хлеб (חַלָּה)\n"
     "- Субботняя трапеза с семьёй\n"
     "- Запрет на работу и использование электричества (у религиозных)\n\n"
     "Полезные фразы:\n"
     "- שַׁבָּת שָׁלוֹם! (шабАт шалОм!) — Мирной субботы!\n"
     "- שָׁבוּעַ טוֹב (шавУа тов) — Хорошей недели! (после шаббата)", 1),

    ("holiday", "Песах", "פֶּסַח",
     "**Песах** (פֶּסַח) — праздник весны и исхода из Египта. Длится 7 дней (8 в диаспоре).\n\n"
     "Традиции:\n"
     "- Седер Песах (סֵדֶר פֶּסַח) — праздничная трапеза с чтением Агады\n"
     "- Маца (מַצָּה) — пресный хлеб\n"
     "- Четыре бокала вина\n"
     "- Четыре вопроса (מַה נִשְׁתַּנָּה)\n"
     "- Запрет на хамец (квасное)\n\n"
     "Фразы: חַג פֶּסַח שָׂמֵחַ! (хаг пЕсах самЕах!) — Весёлого Песаха!", 1),

    ("holiday", "Ханука", "חֲנוּכָּה",
     "**Ханука** (חֲנוּכָּה) — праздник света, 8 дней в декабре.\n\n"
     "История: маккавеи отвоевали Храм, маленький кувшин масла горел 8 дней.\n\n"
     "Традиции:\n"
     "- Зажигание ханукии (חֲנוּכִּיָּה) — по свече каждый день\n"
     "- Суфганиёт (סוּפְגָנִיּוֹת) — пончики\n"
     "- Латкес (לְבִיבוֹת) — картофельные оладьи\n"
     "- Дрейдл (סְבִיבוֹן) — волчок\n\n"
     "Фразы: חַג חֲנוּכָּה שָׂמֵחַ! (хаг ханукА самЕах!)", 1),

    ("holiday", "Пурим", "פּוּרִים",
     "**Пурим** (פּוּרִים) — весёлый праздник в марте.\n\n"
     "История: царица Эстер спасла евреев от плана Амана.\n\n"
     "Традиции:\n"
     "- Чтение Мегилат Эстер (מְגִלַּת אֶסְתֵּר)\n"
     "- Маскарад и костюмы (תַּחְפֹּשֶׂת)\n"
     "- Мишлоах манот (מִשְׁלוֹחַ מָנוֹת) — подарки друг другу\n"
     "- Гоменташен / озней Аман (אוזני המן) — треугольные печенья\n\n"
     "Фразы: חַג פּוּרִים שָׂמֵחַ! (хаг пурИм самЕах!)", 1),

    ("holiday", "Рош ха-Шана и Йом Кипур", "רֹאשׁ הַשָּׁנָה וְיוֹם כִּפּוּר",
     "**Рош ха-Шана** (רֹאשׁ הַשָּׁנָה) — еврейский Новый год (сентябрь-октябрь).\n\n"
     "Традиции: шофар (бараний рог), яблоки с мёдом, гранат.\n"
     "Фраза: !שָׁנָה טוֹבָה (шанА товА!) — Хорошего года!\n\n"
     "**Йом Кипур** (יוֹם כִּפּוּר) — День Искупления, через 10 дней после Рош ха-Шана.\n"
     "Самый святой день: 25-часовой пост, молитвы, белая одежда.\n"
     "В Израиле: нет машин на дорогах, дети катаются на велосипедах.\n\n"
     "Фраза: גְּמַר חֲתִימָה טוֹבָה (гмар хатимА товА) — Хорошей записи (в Книге Жизни)!", 1),

    # Daily life
    ("daily_life", "Ульпан — школа иврита", "אוּלְפָּן",
     "**Ульпан** (אוּלְפָּן) — интенсивные курсы иврита для репатриантов.\n\n"
     "- 5 уровней: от Алеф (начинающий) до Хей (продвинутый)\n"
     "- Обычно 5 дней в неделю, 4-5 часов в день\n"
     "- Первый ульпан открылся в 1949 году\n"
     "- Новые репатрианты имеют право на бесплатный ульпан\n\n"
     "Полезные слова:\n"
     "- מוֹרָה/מוֹרֶה (морА/морЕ) — учительница/учитель\n"
     "- תַּלְמִיד/תַּלְמִידָה (талмИд/талмидА) — ученик/ученица\n"
     "- שִׁעוּר (шиУр) — урок", 1),

    ("daily_life", "Армия (ЦАХАЛ)", "צָה\"ל",
     "**ЦАХАЛ** (צָה\"ל — צְבָא הַהֲגָנָה לְיִשְׂרָאֵל) — Армия Обороны Израиля.\n\n"
     "- Обязательная служба: 32 мес. (мужчины), 24 мес. (женщины)\n"
     "- Служат с 18 лет\n"
     "- После армии многие путешествуют (обычно в Индию или Южную Америку)\n\n"
     "Слова:\n"
     "- חַיָּל/חַיֶּלֶת (хайЯл/хайЕлет) — солдат/солдатка\n"
     "- קַצִין (кацИн) — офицер\n"
     "- מִילוּאִים (милуИм) — резервная служба\n"
     "- יוֹם הַזִּכָּרוֹן (йом hа-зикарОн) — День памяти", 2),

    ("daily_life", "Кибуц и мошав", "קִיבּוּץ וּמוֹשָׁב",
     "**Кибуц** (קִיבּוּץ) — коллективное поселение, основанное на идеях социализма.\n\n"
     "- Первый кибуц: Дгания (1910)\n"
     "- Сегодня ~270 кибуцев\n"
     "- Многие приватизировались, но сохранили общинный дух\n\n"
     "**Мошав** (מוֹשָׁב) — сельское поселение с индивидуальными хозяйствами.\n"
     "- Более 400 мошавов\n"
     "- Каждая семья ведёт своё хозяйство\n\n"
     "Слова:\n"
     "- חָבֵר קִיבּוּץ (хавЕр кибУц) — член кибуца\n"
     "- חַקְלָאוּת (хаклаУт) — сельское хозяйство", 2),

    ("daily_life", "Шук (рынок)", "שׁוּק",
     "**Шук** (שׁוּק) — восточный рынок, важная часть израильской культуры.\n\n"
     "Известные рынки:\n"
     "- שׁוּק מַחֲנֵה יְהוּדָה (шук маханЕ еhудА) — Иерусалим\n"
     "- שׁוּק הַכַּרְמֶל (шук hа-кармЕль) — Тель-Авив\n\n"
     "Культура торга: на шуке принято торговаться!\n\n"
     "Полезные фразы:\n"
     "- כַּמָּה זֶה עוֹלֶה? (кАма зе олЕ?) — Сколько это стоит?\n"
     "- יָקָר מִדַּי! (якАр мидАй!) — Слишком дорого!\n"
     "- תַּעֲשֶׂה לִי הַנָּחָה (таасЕ ли hанахА) — Сделай мне скидку", 1),

    ("daily_life", "Купат Холим", "קוּפַּת חוֹלִים",
     "**Купат Холим** (קוּפַּת חוֹלִים) — организация медицинского обслуживания (ОМО).\n\n"
     "В Израиле 4 купот холим:\n"
     "- כְּלָלִית (клалИт) — крупнейшая\n"
     "- מַכַּבִּי (маккАби)\n"
     "- מְאוּחֶדֶת (меухЕдет)\n"
     "- לְאוּמִּית (леумИт)\n\n"
     "Каждый житель обязан состоять в одной из них.\n\n"
     "Слова:\n"
     "- רוֹפֵא מִשְׁפָּחָה (рофЕ мишпахА) — семейный врач\n"
     "- מִרְשָׁם (миршАм) — рецепт\n"
     "- תוֹר (тор) — очередь / запись к врачу", 1),

    # Abbreviations
    ("abbreviations", "Популярные аббревиатуры", "ר\"ת נפוצים",
     "В иврите аббревиатуры обозначаются знаком \" (гершаим) перед последней буквой.\n\n"
     "| Аббр. | Полная форма | Значение |\n|-------|-------------|----------|\n"
     "| ת\"ז | תְּעוּדַת זֶהוּת | Удостоверение личности |\n"
     "| צה\"ל | צְבָא הַהֲגָנָה לְיִשְׂרָאֵל | ЦАХАЛ (армия) |\n"
     "| בג\"ץ | בֵּית מִשְׁפָּט גָּבוֹהַּ לְצֶדֶק | БАГАЦ (Верховный суд) |\n"
     "| ב\"ל | בִּטּוּחַ לְאוּמִי | Битуах Леуми (соцстрах) |\n"
     "| מע\"מ | מַס עֵרֶךְ מוּסָף | НДС |\n"
     "| ד\"ר | דוֹקְטוֹר | Доктор |\n"
     "| ח\"כ | חֲבֵר כְּנֶסֶת | Депутат Кнессета |\n"
     "| רה\"מ | רֹאשׁ הַמֶּמְשָׁלָה | Премьер-министр |\n"
     "| עו\"ד | עוֹרֵךְ דִּין | Адвокат |\n"
     "| ת\"א | תֵּל אָבִיב | Тель-Авив |", 2),

    # Slang
    ("slang", "Сленг и разговорные выражения", "סלנג",
     "Израильский иврит богат сленгом из арабского, английского и русского.\n\n"
     "| Слово | Произн. | Значение |\n|-------|---------|----------|\n"
     "| יַאללָה | яАлла | Давай! / Пошли! (из арабского) |\n"
     "| סַבָּבָה | сабАба | Круто! / Ок! (из арабского) |\n"
     "| אַחְלָה | ахлА | Супер! / Отлично! (из арабского) |\n"
     "| חָבַל עַל הַזְּמַן | хавАль аль hа-зман | Нереально круто! (букв. «жаль на время») |\n"
     "| מַה קוֹרֶה | ма корЕ | Что нового? / Как дела? |\n"
     "| כָּפָרָה | капарА | Дорогой/дорогая (ласково) |\n"
     "| פְרֶייֶר | фрайЕр | Простак / лох |\n"
     "| חַיָּים שֶׁלִּי | хайИм шелИ | Моя жизнь (обращение к любимому) |\n"
     "| מַגְנִיב | магнИв | Круто! |\n"
     "| בָּלָאגָן | балагАн | Бардак / хаос (из русского!) |\n"
     "| לְסַדֵּר | лесадЕр | Уладить / устроить |\n"
     "| דַּוְקָא | дАвка | Именно / назло / как раз |", 1),

    ("slang", "Полезные разговорные фразы", "ביטויים שימושיים",
     "Фразы, которые вы услышите каждый день в Израиле:\n\n"
     "| Фраза | Произн. | Значение |\n|-------|---------|----------|\n"
     "| מַה שְׁלוֹמְךָ? | ма шломхА? | Как дела? (м.) |\n"
     "| מַה נִשְׁמָע? | ма нишмА? | Что слышно? (= как дела?) |\n"
     "| אֵין בְּעָיָה | эйн беайА | Нет проблем |\n"
     "| בְּכֵיף | бекЕйф | С удовольствием |\n"
     "| אֶפְשָׁר | эфшАр | Можно |\n"
     "| אִי אֶפְשָׁר | и эфшАр | Нельзя |\n"
     "| כָּל הַכָּבוֹד | коль hа-кавОд | Молодец! (букв. «вся честь») |\n"
     "| לְאַט לְאַט | леАт леАт | Потихоньку / постепенно |\n"
     "| רֶגַע | рЕга | Подожди секунду |\n"
     "| סְלִיחָה | слихА | Извините / Простите |", 1),
]


def upgrade() -> None:
    # -- Achievement definitions table --
    op.create_table(
        "achievement_definitions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(50), unique=True, nullable=False),
        sa.Column("title_ru", sa.String(100), nullable=False),
        sa.Column("description_ru", sa.String(300), nullable=False),
        sa.Column("icon", sa.String(10), nullable=True),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("condition_json", postgresql.JSONB, nullable=True),
    )

    # -- Culture articles table --
    op.create_table(
        "culture_articles",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("category", sa.String(30), nullable=False),
        sa.Column("title_ru", sa.String(200), nullable=False),
        sa.Column("title_he", sa.String(200), nullable=True),
        sa.Column("content_md", sa.Text(), nullable=False),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("levels.id"), nullable=True),
    )

    # -- User daily activity tracking --
    op.create_table(
        "user_daily_activity",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("xp_earned", sa.Integer(), server_default="0"),
        sa.Column("exercises_done", sa.Integer(), server_default="0"),
        sa.Column("reviews_done", sa.Integer(), server_default="0"),
        sa.Column("time_minutes", sa.Integer(), server_default="0"),
        sa.UniqueConstraint("user_id", "date", name="uq_user_daily"),
    )

    # ── Seed achievement definitions ──
    defs_t = sa.table("achievement_definitions",
        sa.column("code", sa.String), sa.column("title_ru", sa.String),
        sa.column("description_ru", sa.String), sa.column("icon", sa.String),
        sa.column("category", sa.String), sa.column("condition_json", postgresql.JSONB))
    op.bulk_insert(defs_t, [
        {"code": a[0], "title_ru": a[1], "description_ru": a[2],
         "icon": a[3], "category": a[4], "condition_json": a[5]}
        for a in ACHIEVEMENT_DEFS
    ])

    # ── Seed culture articles ──
    articles_t = sa.table("culture_articles",
        sa.column("category", sa.String), sa.column("title_ru", sa.String),
        sa.column("title_he", sa.String), sa.column("content_md", sa.Text),
        sa.column("level_id", sa.Integer))
    op.bulk_insert(articles_t, [
        {"category": a[0], "title_ru": a[1], "title_he": a[2],
         "content_md": a[3], "level_id": a[4]}
        for a in CULTURE_ARTICLES
    ])


def downgrade() -> None:
    op.drop_table("user_daily_activity")
    op.drop_table("culture_articles")
    op.drop_table("achievement_definitions")
