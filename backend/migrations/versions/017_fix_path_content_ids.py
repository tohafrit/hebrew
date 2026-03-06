"""fix learning_path content_id mismatches and add missing lessons

Revision ID: 017
Revises: 016
Create Date: 2026-03-06

Fixes:
- Step 6 "Числа и цвета" pointed to lesson 7 (Определённый артикль)
  → create dedicated lesson 219 and point to it
- Step 45 "Биньян Хифъиль" pointed to grammar topic 7 (обзор всех биньянов)
  → topic 7 does cover Хифъиль, acceptable for now
- Exercise translate_ru_he prompt field inconsistency is handled in frontend
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text as sa_text

revision: str = '017'
down_revision: Union[str, None] = '016'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


NUMBERS_COLORS_LESSON = {
    "id": 219,
    "level_id": 1,
    "unit": 2,
    "order": 219,
    "title_ru": "Числа и цвета",
    "title_he": "מִסְפָּרִים וּצְבָעִים",
    "description": "Счёт от 1 до 20 и основные цвета на иврите",
    "type": "vocabulary",
    "content_md": r"""## Числа и цвета (מִסְפָּרִים וּצְבָעִים)

В этом уроке вы выучите числа от 1 до 20 и основные цвета. Это базовая лексика, необходимая для покупок, описания предметов и повседневного общения.

### Числа 1–10

В иврите числительные имеют **мужскую** и **женскую** формы.

| Число | Мужской род | Женский род | Транслитерация (м/ж) |
|---|---|---|---|
| 1 | אֶחָד | אַחַת | эхАд / ахАт |
| 2 | שְׁנַיִם | שְׁתַּיִם | шнАим / штАим |
| 3 | שְׁלוֹשָׁה | שָׁלוֹשׁ | шлошА / шалОш |
| 4 | אַרְבָּעָה | אַרְבַּע | арбаА / Арба |
| 5 | חֲמִשָּׁה | חָמֵשׁ | хамишА / хамЕш |
| 6 | שִׁשָּׁה | שֵׁשׁ | шишА / шЕш |
| 7 | שִׁבְעָה | שֶׁבַע | шивъА / шЕва |
| 8 | שְׁמוֹנָה | שְׁמוֹנֶה | шмонА / шмОне |
| 9 | תִּשְׁעָה | תֵּשַׁע | тишъА / тЕша |
| 10 | עֲשָׂרָה | עֶשֶׂר | асарА / Эсер |

> **Правило перекрёстного рода:** С мужскими существительными используется форма на **-ָה**, а с женскими — короткая форма. Например: שְׁלוֹשָׁה יְלָדִים (три мальчика), שָׁלוֹשׁ יְלָדוֹת (три девочки).

### Числа 11–20

| Число | Мужской род | Женский род |
|---|---|---|
| 11 | אַחַד עָשָׂר | אַחַת עֶשְׂרֵה |
| 12 | שְׁנֵים עָשָׂר | שְׁתֵּים עֶשְׂרֵה |
| 13 | שְׁלוֹשָׁה עָשָׂר | שְׁלוֹשׁ עֶשְׂרֵה |
| 14 | אַרְבָּעָה עָשָׂר | אַרְבַּע עֶשְׂרֵה |
| 15 | חֲמִשָּׁה עָשָׂר | חָמֵשׁ עֶשְׂרֵה |
| 16 | שִׁשָּׁה עָשָׂר | שֵׁשׁ עֶשְׂרֵה |
| 17 | שִׁבְעָה עָשָׂר | שְׁבַע עֶשְׂרֵה |
| 18 | שְׁמוֹנָה עָשָׂר | שְׁמוֹנֶה עֶשְׂרֵה |
| 19 | תִּשְׁעָה עָשָׂר | תְּשַׁע עֶשְׂרֵה |
| 20 | עֶשְׂרִים | עֶשְׂרִים |

### Основные цвета (צְבָעִים)

Прилагательные-цвета согласуются с существительным в роде и числе.

| Цвет | Мужской род | Женский род | Транслитерация |
|---|---|---|---|
| красный | אָדֹם | אֲדֻמָּה | адОм / адумА |
| синий | כָּחֹל | כְּחֻלָּה | кахОль / кхулА |
| зелёный | יָרֹק | יְרֻקָּה | ярОк / ерукА |
| жёлтый | צָהֹב | צְהֻבָּה | цаhОв / цеhувА |
| белый | לָבָן | לְבָנָה | лавАн / леванА |
| чёрный | שָׁחֹר | שְׁחוֹרָה | шахОр / шхорА |
| оранжевый | כָּתֹם | כְּתֻמָּה | катОм / ктумА |
| розовый | וָרֹד | וְרֻדָּה | варОд / верудА |

### Примеры

- **שְׁלוֹשָׁה תַּפּוּחִים אֲדֻמִּים** — три красных яблока
- **עֶשֶׂר פְּרָחִים צְהֻבִּים** — десять жёлтых цветов
- **הַשָּׁמַיִם כְּחֻלִּים** — небо голубое
- **שְׁנֵי כְּלָבִים שְׁחוֹרִים** — две чёрные собаки
- **אַרְבַּע חֲתוּלוֹת לְבָנוֹת** — четыре белые кошки

### Полезные фразы

- **אֵיזֶה צֶבַע?** — Какой цвет?
- **כַּמָּה?** — Сколько?
- **יֵשׁ בְּצֶבַע אַחֵר?** — Есть в другом цвете?
- **אֲנִי רוֹצֶה שְׁנַיִם** — Я хочу два
""",
}


def upgrade() -> None:
    conn = op.get_bind()

    # 1. Create the missing "Числа и цвета" lesson
    conn.execute(sa_text("""
        INSERT INTO lessons (id, level_id, unit, "order", title_ru, title_he, description, content_md, type)
        VALUES (:id, :level_id, :unit, :order, :title_ru, :title_he, :description, :content_md, :type)
        ON CONFLICT (id) DO NOTHING
    """), NUMBERS_COLORS_LESSON)

    # Update sequence
    conn.execute(sa_text(
        "SELECT setval('lessons_id_seq', GREATEST((SELECT MAX(id) FROM lessons), 219), true)"
    ))

    # 2. Fix learning_paths step 6: point "Числа и цвета" to the new lesson
    conn.execute(sa_text("""
        UPDATE learning_paths
        SET content_id = 219
        WHERE id = 6 AND title_ru = 'Числа и цвета'
    """))


def downgrade() -> None:
    conn = op.get_bind()

    # Revert learning_paths step 6
    conn.execute(sa_text("""
        UPDATE learning_paths
        SET content_id = 7
        WHERE id = 6 AND title_ru = 'Числа и цвета'
    """))

    # Remove the lesson
    conn.execute(sa_text("DELETE FROM lessons WHERE id = 219"))
