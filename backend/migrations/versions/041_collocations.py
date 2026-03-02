"""Populate collocations table with 200 common Hebrew word combinations.

Each collocation links a common phrase to a word in the dictionary,
demonstrating natural Hebrew usage patterns and fixed expressions.

Revision ID: 041
Revises: 040
Create Date: 2026-03-02
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "041"
down_revision: Union[str, None] = "040"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

collocations_table = sa.table(
    "collocations",
    sa.column("word_id", sa.Integer),
    sa.column("phrase_he", sa.String),
    sa.column("phrase_ru", sa.String),
    sa.column("frequency", sa.Integer),
)

# ==============================================================================
# LEVEL 1 VERBS — ~80 collocations (5-7 per verb)
# ==============================================================================

LEVEL_1_VERB_COLLOCATIONS = [
    # --- 1279: לאכול (есть) ---
    {"word_id": 1279, "phrase_he": "לאכול ארוחת בוקר", "phrase_ru": "завтракать (есть завтрак)", "frequency": 1},
    {"word_id": 1279, "phrase_he": "לאכול ארוחת צהריים", "phrase_ru": "обедать (есть обед)", "frequency": 1},
    {"word_id": 1279, "phrase_he": "לאכול ארוחת ערב", "phrase_ru": "ужинать (есть ужин)", "frequency": 1},
    {"word_id": 1279, "phrase_he": "לאכול במסעדה", "phrase_ru": "есть в ресторане", "frequency": 1},
    {"word_id": 1279, "phrase_he": "לאכול חטיף", "phrase_ru": "перекусить (есть снэк)", "frequency": 2},
    {"word_id": 1279, "phrase_he": "לאכול בחוץ", "phrase_ru": "есть на улице / вне дома", "frequency": 2},
    {"word_id": 1279, "phrase_he": "לאכול כמו ציפור", "phrase_ru": "есть как птичка (мало)", "frequency": 3},

    # --- 1280: לשתות (пить) ---
    {"word_id": 1280, "phrase_he": "לשתות קפה", "phrase_ru": "пить кофе", "frequency": 1},
    {"word_id": 1280, "phrase_he": "לשתות מים", "phrase_ru": "пить воду", "frequency": 1},
    {"word_id": 1280, "phrase_he": "לשתות תה", "phrase_ru": "пить чай", "frequency": 1},
    {"word_id": 1280, "phrase_he": "לשתות לחיים", "phrase_ru": "выпить за здоровье (лехаим)", "frequency": 2},
    {"word_id": 1280, "phrase_he": "לשתות בירה", "phrase_ru": "пить пиво", "frequency": 2},
    {"word_id": 1280, "phrase_he": "לשתות מיץ", "phrase_ru": "пить сок", "frequency": 2},
    {"word_id": 1280, "phrase_he": "לשתות עד הסוף", "phrase_ru": "допить до конца", "frequency": 3},

    # --- 1282: ללכת (идти) ---
    {"word_id": 1282, "phrase_he": "ללכת הביתה", "phrase_ru": "идти домой", "frequency": 1},
    {"word_id": 1282, "phrase_he": "ללכת לעבודה", "phrase_ru": "идти на работу", "frequency": 1},
    {"word_id": 1282, "phrase_he": "ללכת לישון", "phrase_ru": "идти спать", "frequency": 1},
    {"word_id": 1282, "phrase_he": "ללכת ברגל", "phrase_ru": "идти пешком", "frequency": 1},
    {"word_id": 1282, "phrase_he": "ללכת לקניות", "phrase_ru": "идти за покупками", "frequency": 2},
    {"word_id": 1282, "phrase_he": "ללכת לאיבוד", "phrase_ru": "потеряться (пойти к потере)", "frequency": 2},
    {"word_id": 1282, "phrase_he": "ללכת על הקצה", "phrase_ru": "ходить по краю (рисковать)", "frequency": 3},

    # --- 1284: לכתוב (писать) ---
    {"word_id": 1284, "phrase_he": "לכתוב מכתב", "phrase_ru": "писать письмо", "frequency": 1},
    {"word_id": 1284, "phrase_he": "לכתוב ספר", "phrase_ru": "писать книгу", "frequency": 2},
    {"word_id": 1284, "phrase_he": "לכתוב הודעה", "phrase_ru": "писать сообщение", "frequency": 1},
    {"word_id": 1284, "phrase_he": "לכתוב מייל", "phrase_ru": "писать электронное письмо", "frequency": 1},
    {"word_id": 1284, "phrase_he": "לכתוב ביומן", "phrase_ru": "писать в дневнике", "frequency": 2},
    {"word_id": 1284, "phrase_he": "לכתוב שיר", "phrase_ru": "писать стихотворение", "frequency": 3},

    # --- 1285: לקרוא (читать) ---
    {"word_id": 1285, "phrase_he": "לקרוא ספר", "phrase_ru": "читать книгу", "frequency": 1},
    {"word_id": 1285, "phrase_he": "לקרוא עיתון", "phrase_ru": "читать газету", "frequency": 1},
    {"word_id": 1285, "phrase_he": "לקרוא חדשות", "phrase_ru": "читать новости", "frequency": 1},
    {"word_id": 1285, "phrase_he": "לקרוא בקול רם", "phrase_ru": "читать вслух", "frequency": 2},
    {"word_id": 1285, "phrase_he": "לקרוא מייל", "phrase_ru": "читать электронную почту", "frequency": 1},
    {"word_id": 1285, "phrase_he": "לקרוא סיפור", "phrase_ru": "читать рассказ", "frequency": 2},
    {"word_id": 1285, "phrase_he": "לקרוא בין השורות", "phrase_ru": "читать между строк", "frequency": 3},

    # --- 1286: לדבר (говорить) ---
    {"word_id": 1286, "phrase_he": "לדבר עברית", "phrase_ru": "говорить на иврите", "frequency": 1},
    {"word_id": 1286, "phrase_he": "לדבר בטלפון", "phrase_ru": "говорить по телефону", "frequency": 1},
    {"word_id": 1286, "phrase_he": "לדבר עם חברים", "phrase_ru": "разговаривать с друзьями", "frequency": 1},
    {"word_id": 1286, "phrase_he": "לדבר לעניין", "phrase_ru": "говорить по делу", "frequency": 2},
    {"word_id": 1286, "phrase_he": "לדבר מהלב", "phrase_ru": "говорить от сердца", "frequency": 2},
    {"word_id": 1286, "phrase_he": "לדבר בשקט", "phrase_ru": "говорить тихо", "frequency": 2},
    {"word_id": 1286, "phrase_he": "לדבר תכל'ס", "phrase_ru": "говорить конкретно / по существу", "frequency": 2},

    # --- 1287: לשמוע (слышать) ---
    {"word_id": 1287, "phrase_he": "לשמוע מוזיקה", "phrase_ru": "слушать музыку", "frequency": 1},
    {"word_id": 1287, "phrase_he": "לשמוע חדשות", "phrase_ru": "слушать новости", "frequency": 1},
    {"word_id": 1287, "phrase_he": "לשמוע רדיו", "phrase_ru": "слушать радио", "frequency": 2},
    {"word_id": 1287, "phrase_he": "לשמוע שיר", "phrase_ru": "слышать/слушать песню", "frequency": 2},
    {"word_id": 1287, "phrase_he": "לשמוע הרצאה", "phrase_ru": "слушать лекцию", "frequency": 2},
    {"word_id": 1287, "phrase_he": "לשמוע בקול", "phrase_ru": "слушаться (слышать голос)", "frequency": 2},

    # --- 1288: לראות (видеть) ---
    {"word_id": 1288, "phrase_he": "לראות סרט", "phrase_ru": "смотреть фильм", "frequency": 1},
    {"word_id": 1288, "phrase_he": "לראות חלום", "phrase_ru": "видеть сон", "frequency": 2},
    {"word_id": 1288, "phrase_he": "לראות רופא", "phrase_ru": "видеть врача (навестить)", "frequency": 2},
    {"word_id": 1288, "phrase_he": "לראות את העולם", "phrase_ru": "увидеть мир", "frequency": 2},
    {"word_id": 1288, "phrase_he": "לראות עין בעין", "phrase_ru": "видеть глаза в глаза (соглашаться)", "frequency": 3},
    {"word_id": 1288, "phrase_he": "לראות תוצאות", "phrase_ru": "видеть результаты", "frequency": 2},

    # --- 1289: לתת (давать) ---
    {"word_id": 1289, "phrase_he": "לתת מתנה", "phrase_ru": "дарить подарок", "frequency": 1},
    {"word_id": 1289, "phrase_he": "לתת תשובה", "phrase_ru": "дать ответ", "frequency": 1},
    {"word_id": 1289, "phrase_he": "לתת עצה", "phrase_ru": "дать совет", "frequency": 2},
    {"word_id": 1289, "phrase_he": "לתת יד", "phrase_ru": "подать руку (помочь)", "frequency": 2},
    {"word_id": 1289, "phrase_he": "לתת דוגמה", "phrase_ru": "привести пример", "frequency": 2},
    {"word_id": 1289, "phrase_he": "לתת הזדמנות", "phrase_ru": "дать возможность / шанс", "frequency": 2},
    {"word_id": 1289, "phrase_he": "לתת את הדעת", "phrase_ru": "обратить внимание", "frequency": 3},

    # --- 1290: לקחת (брать) ---
    {"word_id": 1290, "phrase_he": "לקחת אחריות", "phrase_ru": "взять ответственность", "frequency": 1},
    {"word_id": 1290, "phrase_he": "לקחת הפסקה", "phrase_ru": "взять перерыв", "frequency": 1},
    {"word_id": 1290, "phrase_he": "לקחת מקלחת", "phrase_ru": "принять душ", "frequency": 1},
    {"word_id": 1290, "phrase_he": "לקחת מונית", "phrase_ru": "взять такси", "frequency": 1},
    {"word_id": 1290, "phrase_he": "לקחת ללב", "phrase_ru": "принять близко к сердцу", "frequency": 2},
    {"word_id": 1290, "phrase_he": "לקחת חלק", "phrase_ru": "принять участие", "frequency": 2},
    {"word_id": 1290, "phrase_he": "לקחת בחשבון", "phrase_ru": "принять во внимание", "frequency": 2},

    # --- 1292: ללמוד (учиться) ---
    {"word_id": 1292, "phrase_he": "ללמוד עברית", "phrase_ru": "учить иврит", "frequency": 1},
    {"word_id": 1292, "phrase_he": "ללמוד באוניברסיטה", "phrase_ru": "учиться в университете", "frequency": 1},
    {"word_id": 1292, "phrase_he": "ללמוד למבחן", "phrase_ru": "готовиться к экзамену", "frequency": 1},
    {"word_id": 1292, "phrase_he": "ללמוד בעל פה", "phrase_ru": "учить наизусть", "frequency": 2},
    {"word_id": 1292, "phrase_he": "ללמוד מטעויות", "phrase_ru": "учиться на ошибках", "frequency": 2},
    {"word_id": 1292, "phrase_he": "ללמוד שיעור", "phrase_ru": "выучить урок", "frequency": 2},

    # --- 1293: לעבוד (работать) ---
    {"word_id": 1293, "phrase_he": "לעבוד קשה", "phrase_ru": "работать тяжело / усердно", "frequency": 1},
    {"word_id": 1293, "phrase_he": "לעבוד מהבית", "phrase_ru": "работать из дома", "frequency": 1},
    {"word_id": 1293, "phrase_he": "לעבוד שעות נוספות", "phrase_ru": "работать сверхурочно", "frequency": 2},
    {"word_id": 1293, "phrase_he": "לעבוד במשמרות", "phrase_ru": "работать посменно", "frequency": 2},
    {"word_id": 1293, "phrase_he": "לעבוד על עצמו", "phrase_ru": "работать над собой", "frequency": 2},
    {"word_id": 1293, "phrase_he": "לעבוד בצוות", "phrase_ru": "работать в команде", "frequency": 2},
    {"word_id": 1293, "phrase_he": "לעבוד על פרויקט", "phrase_ru": "работать над проектом", "frequency": 2},
]

# ==============================================================================
# LEVEL 2 VERBS — ~50 collocations (6-8 per verb)
# ==============================================================================

LEVEL_2_VERB_COLLOCATIONS = [
    # --- 108: לפעול (действовать) ---
    {"word_id": 108, "phrase_he": "לפעול בהתאם", "phrase_ru": "действовать в соответствии", "frequency": 1},
    {"word_id": 108, "phrase_he": "לפעול במהירות", "phrase_ru": "действовать быстро", "frequency": 1},
    {"word_id": 108, "phrase_he": "לפעול לפי חוק", "phrase_ru": "действовать по закону", "frequency": 2},
    {"word_id": 108, "phrase_he": "לפעול בשיתוף פעולה", "phrase_ru": "действовать сообща", "frequency": 2},
    {"word_id": 108, "phrase_he": "לפעול מיד", "phrase_ru": "действовать немедленно", "frequency": 2},
    {"word_id": 108, "phrase_he": "לפעול בזהירות", "phrase_ru": "действовать осторожно", "frequency": 2},
    {"word_id": 108, "phrase_he": "לפעול נגד", "phrase_ru": "действовать против", "frequency": 2},
    {"word_id": 108, "phrase_he": "לפעול למען", "phrase_ru": "действовать ради / во имя", "frequency": 2},

    # --- 131: לנהל (управлять) ---
    {"word_id": 131, "phrase_he": "לנהל משא ומתן", "phrase_ru": "вести переговоры", "frequency": 1},
    {"word_id": 131, "phrase_he": "לנהל עסק", "phrase_ru": "управлять бизнесом", "frequency": 1},
    {"word_id": 131, "phrase_he": "לנהל שיחה", "phrase_ru": "вести разговор / беседу", "frequency": 1},
    {"word_id": 131, "phrase_he": "לנהל חשבון", "phrase_ru": "вести счёт / управлять аккаунтом", "frequency": 2},
    {"word_id": 131, "phrase_he": "לנהל צוות", "phrase_ru": "управлять командой", "frequency": 2},
    {"word_id": 131, "phrase_he": "לנהל ישיבה", "phrase_ru": "вести собрание", "frequency": 2},
    {"word_id": 131, "phrase_he": "לנהל יומן", "phrase_ru": "вести ежедневник", "frequency": 3},
    {"word_id": 131, "phrase_he": "לנהל מלחמה", "phrase_ru": "вести войну", "frequency": 3},

    # --- 142: להשפיע (влиять) ---
    {"word_id": 142, "phrase_he": "להשפיע על ההחלטה", "phrase_ru": "влиять на решение", "frequency": 1},
    {"word_id": 142, "phrase_he": "להשפיע לטובה", "phrase_ru": "влиять положительно", "frequency": 2},
    {"word_id": 142, "phrase_he": "להשפיע לרעה", "phrase_ru": "влиять негативно", "frequency": 2},
    {"word_id": 142, "phrase_he": "להשפיע על דעת הקהל", "phrase_ru": "влиять на общественное мнение", "frequency": 2},
    {"word_id": 142, "phrase_he": "להשפיע על התוצאה", "phrase_ru": "влиять на результат", "frequency": 2},
    {"word_id": 142, "phrase_he": "להשפיע על הסביבה", "phrase_ru": "влиять на окружающую среду", "frequency": 2},
    {"word_id": 142, "phrase_he": "להשפיע על הבריאות", "phrase_ru": "влиять на здоровье", "frequency": 2},
    {"word_id": 142, "phrase_he": "להשפיע על העתיד", "phrase_ru": "влиять на будущее", "frequency": 2},

    # --- 149: להוסיף (добавлять) ---
    {"word_id": 149, "phrase_he": "להוסיף תבלין", "phrase_ru": "добавить специю", "frequency": 2},
    {"word_id": 149, "phrase_he": "להוסיף מלח", "phrase_ru": "добавить соль", "frequency": 1},
    {"word_id": 149, "phrase_he": "להוסיף סוכר", "phrase_ru": "добавить сахар", "frequency": 1},
    {"word_id": 149, "phrase_he": "להוסיף הערה", "phrase_ru": "добавить замечание / комментарий", "frequency": 2},
    {"word_id": 149, "phrase_he": "להוסיף פרטים", "phrase_ru": "добавить подробности", "frequency": 2},
    {"word_id": 149, "phrase_he": "להוסיף שמן למדורה", "phrase_ru": "подливать масло в огонь", "frequency": 3},
    {"word_id": 149, "phrase_he": "להוסיף ערך", "phrase_ru": "добавить ценность", "frequency": 2},
    {"word_id": 149, "phrase_he": "להוסיף חבר", "phrase_ru": "добавить друга (в соцсети)", "frequency": 2},

    # --- 736: לתקן (чинить) ---
    {"word_id": 736, "phrase_he": "לתקן עולם", "phrase_ru": "исправлять мир (тикун олам)", "frequency": 2},
    {"word_id": 736, "phrase_he": "לתקן טעות", "phrase_ru": "исправить ошибку", "frequency": 1},
    {"word_id": 736, "phrase_he": "לתקן מכונית", "phrase_ru": "починить машину", "frequency": 1},
    {"word_id": 736, "phrase_he": "לתקן תקלה", "phrase_ru": "устранить неисправность", "frequency": 2},
    {"word_id": 736, "phrase_he": "לתקן את המצב", "phrase_ru": "исправить ситуацию", "frequency": 2},
    {"word_id": 736, "phrase_he": "לתקן יחסים", "phrase_ru": "наладить отношения", "frequency": 2},
    {"word_id": 736, "phrase_he": "לתקן חוק", "phrase_ru": "внести поправку в закон", "frequency": 3},

    # --- 938: לאשר (утверждать) ---
    {"word_id": 938, "phrase_he": "לאשר חוק", "phrase_ru": "утвердить закон", "frequency": 1},
    {"word_id": 938, "phrase_he": "לאשר תקציב", "phrase_ru": "утвердить бюджет", "frequency": 2},
    {"word_id": 938, "phrase_he": "לאשר בקשה", "phrase_ru": "одобрить заявку / просьбу", "frequency": 1},
    {"word_id": 938, "phrase_he": "לאשר עסקה", "phrase_ru": "утвердить сделку", "frequency": 2},
    {"word_id": 938, "phrase_he": "לאשר הסכם", "phrase_ru": "утвердить соглашение", "frequency": 2},
    {"word_id": 938, "phrase_he": "לאשר קבלה", "phrase_ru": "подтвердить получение", "frequency": 2},
    {"word_id": 938, "phrase_he": "לאשר נוכחות", "phrase_ru": "подтвердить присутствие", "frequency": 2},
]

# ==============================================================================
# LEVEL 3+ VERBS — ~40 collocations (5-6 per verb)
# ==============================================================================

LEVEL_3_VERB_COLLOCATIONS = [
    # --- 113: ליצור (создавать) ---
    {"word_id": 113, "phrase_he": "ליצור קשר", "phrase_ru": "связаться (создать связь)", "frequency": 1},
    {"word_id": 113, "phrase_he": "ליצור אמנות", "phrase_ru": "создавать искусство", "frequency": 2},
    {"word_id": 113, "phrase_he": "ליצור רושם", "phrase_ru": "произвести впечатление", "frequency": 1},
    {"word_id": 113, "phrase_he": "ליצור אווירה", "phrase_ru": "создать атмосферу", "frequency": 2},
    {"word_id": 113, "phrase_he": "ליצור הזדמנות", "phrase_ru": "создать возможность", "frequency": 2},
    {"word_id": 113, "phrase_he": "ליצור שינוי", "phrase_ru": "создать перемену", "frequency": 2},

    # --- 147: להעלות (поднимать) ---
    {"word_id": 147, "phrase_he": "להעלות נושא", "phrase_ru": "поднять тему", "frequency": 1},
    {"word_id": 147, "phrase_he": "להעלות מחיר", "phrase_ru": "поднять цену", "frequency": 1},
    {"word_id": 147, "phrase_he": "להעלות שאלה", "phrase_ru": "задать вопрос (поднять вопрос)", "frequency": 2},
    {"word_id": 147, "phrase_he": "להעלות רמה", "phrase_ru": "повысить уровень", "frequency": 2},
    {"word_id": 147, "phrase_he": "להעלות זיכרונות", "phrase_ru": "вызвать воспоминания", "frequency": 2},
    {"word_id": 147, "phrase_he": "להעלות חיוך", "phrase_ru": "вызвать улыбку", "frequency": 3},

    # --- 156: להציל (спасать) ---
    {"word_id": 156, "phrase_he": "להציל חיים", "phrase_ru": "спасти жизнь", "frequency": 1},
    {"word_id": 156, "phrase_he": "להציל מצב", "phrase_ru": "спасти ситуацию", "frequency": 2},
    {"word_id": 156, "phrase_he": "להציל את העולם", "phrase_ru": "спасти мир", "frequency": 2},
    {"word_id": 156, "phrase_he": "להציל כסף", "phrase_ru": "сэкономить деньги", "frequency": 2},
    {"word_id": 156, "phrase_he": "להציל מטביעה", "phrase_ru": "спасти от утопления", "frequency": 3},

    # --- 729: להתמודד (справляться) ---
    {"word_id": 729, "phrase_he": "להתמודד עם אתגר", "phrase_ru": "справляться с вызовом", "frequency": 1},
    {"word_id": 729, "phrase_he": "להתמודד עם בעיה", "phrase_ru": "справляться с проблемой", "frequency": 1},
    {"word_id": 729, "phrase_he": "להתמודד עם לחץ", "phrase_ru": "справляться с давлением / стрессом", "frequency": 2},
    {"word_id": 729, "phrase_he": "להתמודד עם קושי", "phrase_ru": "справляться с трудностью", "frequency": 2},
    {"word_id": 729, "phrase_he": "להתמודד עם שינוי", "phrase_ru": "справляться с переменами", "frequency": 2},
    {"word_id": 729, "phrase_he": "להתמודד לבד", "phrase_ru": "справляться в одиночку", "frequency": 2},

    # --- 405: להשלים (завершать) ---
    {"word_id": 405, "phrase_he": "להשלים משימה", "phrase_ru": "завершить задание", "frequency": 1},
    {"word_id": 405, "phrase_he": "להשלים עם המצב", "phrase_ru": "смириться с ситуацией", "frequency": 2},
    {"word_id": 405, "phrase_he": "להשלים פרויקט", "phrase_ru": "завершить проект", "frequency": 1},
    {"word_id": 405, "phrase_he": "להשלים לימודים", "phrase_ru": "завершить учёбу", "frequency": 2},
    {"word_id": 405, "phrase_he": "להשלים תהליך", "phrase_ru": "завершить процесс", "frequency": 2},

    # --- 945: להגן (защищать) ---
    {"word_id": 945, "phrase_he": "להגן על זכויות", "phrase_ru": "защищать права", "frequency": 1},
    {"word_id": 945, "phrase_he": "להגן על הסביבה", "phrase_ru": "защищать окружающую среду", "frequency": 1},
    {"word_id": 945, "phrase_he": "להגן על המשפחה", "phrase_ru": "защищать семью", "frequency": 2},
    {"word_id": 945, "phrase_he": "להגן על הילדים", "phrase_ru": "защищать детей", "frequency": 1},
    {"word_id": 945, "phrase_he": "להגן על המולדת", "phrase_ru": "защищать родину", "frequency": 2},
    {"word_id": 945, "phrase_he": "להגן מפני סכנה", "phrase_ru": "защищать от опасности", "frequency": 2},

    # --- 947: להציע (предлагать) ---
    {"word_id": 947, "phrase_he": "להציע הצעה", "phrase_ru": "сделать предложение", "frequency": 1},
    {"word_id": 947, "phrase_he": "להציע עזרה", "phrase_ru": "предложить помощь", "frequency": 1},
    {"word_id": 947, "phrase_he": "להציע פתרון", "phrase_ru": "предложить решение", "frequency": 1},
    {"word_id": 947, "phrase_he": "להציע רעיון", "phrase_ru": "предложить идею", "frequency": 2},
    {"word_id": 947, "phrase_he": "להציע מחיר", "phrase_ru": "предложить цену", "frequency": 2},
    {"word_id": 947, "phrase_he": "להציע שיתוף פעולה", "phrase_ru": "предложить сотрудничество", "frequency": 2},
]

# ==============================================================================
# COMMON NOUNS (L2, word IDs 1-90) — ~30 collocations
# ==============================================================================

NOUN_COLLOCATIONS = [
    # Time-related nouns
    {"word_id": 1, "phrase_he": "חיי יום-יום", "phrase_ru": "повседневная жизнь", "frequency": 1},
    {"word_id": 1, "phrase_he": "חיים טובים", "phrase_ru": "хорошая жизнь", "frequency": 1},
    {"word_id": 1, "phrase_he": "חיים קשים", "phrase_ru": "тяжёлая жизнь", "frequency": 2},

    {"word_id": 3, "phrase_he": "זמן חופשי", "phrase_ru": "свободное время", "frequency": 1},
    {"word_id": 3, "phrase_he": "זמן רב", "phrase_ru": "много времени / долгое время", "frequency": 1},
    {"word_id": 3, "phrase_he": "חוסר זמן", "phrase_ru": "нехватка времени", "frequency": 2},

    {"word_id": 5, "phrase_he": "מקום עבודה", "phrase_ru": "рабочее место", "frequency": 1},
    {"word_id": 5, "phrase_he": "מקום מגורים", "phrase_ru": "место жительства", "frequency": 1},
    {"word_id": 5, "phrase_he": "מקום חניה", "phrase_ru": "парковочное место", "frequency": 2},

    # People-related nouns
    {"word_id": 10, "phrase_he": "איש עסקים", "phrase_ru": "бизнесмен (деловой человек)", "frequency": 1},
    {"word_id": 10, "phrase_he": "איש מקצוע", "phrase_ru": "профессионал (человек профессии)", "frequency": 2},

    {"word_id": 15, "phrase_he": "בני משפחה", "phrase_ru": "члены семьи", "frequency": 1},
    {"word_id": 15, "phrase_he": "משפחה גדולה", "phrase_ru": "большая семья", "frequency": 1},
    {"word_id": 15, "phrase_he": "משפחה חמה", "phrase_ru": "тёплая (дружная) семья", "frequency": 2},

    # Action/state-related nouns
    {"word_id": 20, "phrase_he": "עבודת צוות", "phrase_ru": "командная работа", "frequency": 1},
    {"word_id": 20, "phrase_he": "עבודה קשה", "phrase_ru": "тяжёлая работа", "frequency": 1},
    {"word_id": 20, "phrase_he": "עבודת בית", "phrase_ru": "домашнее задание / работа по дому", "frequency": 1},

    {"word_id": 25, "phrase_he": "דרך ארוכה", "phrase_ru": "длинный путь / дорога", "frequency": 1},
    {"word_id": 25, "phrase_he": "דרך חיים", "phrase_ru": "образ жизни (путь жизни)", "frequency": 2},
    {"word_id": 25, "phrase_he": "בדרך כלל", "phrase_ru": "обычно (как правило)", "frequency": 1},

    {"word_id": 30, "phrase_he": "שאלה טובה", "phrase_ru": "хороший вопрос", "frequency": 1},
    {"word_id": 30, "phrase_he": "שאלה קשה", "phrase_ru": "трудный вопрос", "frequency": 2},

    {"word_id": 35, "phrase_he": "מצב ביטחוני", "phrase_ru": "ситуация с безопасностью", "frequency": 2},
    {"word_id": 35, "phrase_he": "מצב רוח", "phrase_ru": "настроение (состояние духа)", "frequency": 1},
    {"word_id": 35, "phrase_he": "מצב חירום", "phrase_ru": "чрезвычайное положение", "frequency": 2},

    {"word_id": 40, "phrase_he": "כוח רצון", "phrase_ru": "сила воли", "frequency": 2},
    {"word_id": 40, "phrase_he": "כוח אדם", "phrase_ru": "рабочая сила / кадры", "frequency": 2},
    {"word_id": 40, "phrase_he": "בכוח", "phrase_ru": "силой / насильно", "frequency": 2},

    {"word_id": 45, "phrase_he": "חלק גדול", "phrase_ru": "большая часть", "frequency": 1},
    {"word_id": 45, "phrase_he": "חלק בלתי נפרד", "phrase_ru": "неотъемлемая часть", "frequency": 2},

    {"word_id": 50, "phrase_he": "תוכנית עבודה", "phrase_ru": "рабочий план / программа", "frequency": 1},
    {"word_id": 50, "phrase_he": "תוכנית לימודים", "phrase_ru": "учебная программа", "frequency": 2},

    {"word_id": 55, "phrase_he": "בעיה קשה", "phrase_ru": "серьёзная проблема", "frequency": 1},
    {"word_id": 55, "phrase_he": "בעיה טכנית", "phrase_ru": "техническая проблема", "frequency": 2},
]


def upgrade() -> None:
    op.execute(
        "SELECT setval('collocations_id_seq', GREATEST((SELECT COALESCE(MAX(id), 0) FROM collocations), 1))"
    )

    all_collocations = (
        LEVEL_1_VERB_COLLOCATIONS
        + LEVEL_2_VERB_COLLOCATIONS
        + LEVEL_3_VERB_COLLOCATIONS
        + NOUN_COLLOCATIONS
    )

    op.bulk_insert(collocations_table, all_collocations)


def downgrade() -> None:
    op.execute("DELETE FROM collocations")
