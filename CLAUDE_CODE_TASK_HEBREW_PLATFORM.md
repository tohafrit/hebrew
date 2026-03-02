# 🇮🇱 Задача для Claude Code: Платформа изучения иврита «Ulpan AI»

## Контекст

Создать **локальную self-hosted веб-платформу** для изучения иврита от нуля до уровня носителя. Всё должно запускаться через `docker compose up` одной командой. Стек: **Python (FastAPI) + React/TypeScript + PostgreSQL + Redis**. Интерфейс на русском языке с элементами иврита.

Данный документ — исчерпывающее ТЗ. Реализуй его порционно: сначала каркас с Docker, затем модуль за модулем.

---

## Архитектура

```
docker-compose.yml
├── frontend/          # React + TypeScript + Vite + TailwindCSS
├── backend/           # Python FastAPI
├── db/                # PostgreSQL 16
├── redis/             # Redis (очереди, кеш, сессии)
├── nginx/             # reverse proxy + раздача статики
└── data/              # seed-данные (словарь, грамматика, тексты)
```

### Docker Compose сервисы:
- **db** — PostgreSQL 16 с volume для персистентности
- **redis** — Redis 7 для SRS-очередей, кеша и rate-limiting
- **backend** — FastAPI (uvicorn), порт 8000
- **frontend** — Node 20 (dev: Vite HMR, prod: nginx static build)
- **nginx** — reverse proxy: `/api/*` → backend, `/*` → frontend

### Backend (FastAPI):
- SQLAlchemy 2.0 + Alembic миграции
- Pydantic v2 для валидации
- JWT-аутентификация (access + refresh tokens)
- Background tasks (Celery + Redis) для генерации контента
- REST API + WebSocket для real-time упражнений

### Frontend (React):
- React 18 + TypeScript
- TailwindCSS + shadcn/ui компоненты
- React Router v6 (SPA)
- Zustand для state management
- React Query для серверного состояния
- Поддержка RTL-layout для ивритских блоков
- PWA-манифест (offline-режим для карточек)

---

## Модель данных (PostgreSQL)

### Пользователь и прогресс:
```sql
users (id, email, password_hash, display_name, native_lang, current_level, xp, streak_days, created_at)
user_settings (user_id, daily_goal_minutes, daily_new_cards, srs_algorithm, ui_theme, notifications)
user_sessions (id, user_id, started_at, ended_at, module, xp_earned)
achievements (id, user_id, type, unlocked_at, metadata)
```

### Уровневая система (6 уровней ульпана):
```sql
levels (id, code, name_ru, name_he, description, order, cefr_equivalent)
-- Алеф(A1), Бет(A2), Гимель(B1), Далет(B2), Хей(C1), Вав(C2)
```

### Словарь и лексика:
```sql
words (id, hebrew, nikkud, transliteration, translation_ru, pos, gender, number, root, frequency_rank, level_id, audio_url, image_url)
word_forms (id, word_id, form_type, hebrew, nikkud, transliteration, description)
-- form_type: singular, plural, construct, feminine, masculine...
root_families (id, root, meaning_ru, description)
root_family_members (root_family_id, word_id)
word_relations (word_id_1, word_id_2, relation_type)
-- relation_type: synonym, antonym, derivative, compound, collocate
example_sentences (id, word_id, hebrew, translation_ru, transliteration, audio_url, level_id)
collocations (id, word_id, phrase_he, phrase_ru, frequency)
```

### Грамматика:
```sql
grammar_topics (id, title_ru, title_he, level_id, order, content_md, summary)
grammar_rules (id, topic_id, rule_text_ru, examples_json, exceptions_json)

binyanim (id, name_he, name_ru, description, pattern, example_root, level_id)
verb_conjugations (id, word_id, binyan_id, tense, person, gender, number, form_he, form_nikkud, transliteration)
-- tense: past, present, future, imperative, infinitive

prepositions (id, base_form, meaning_ru, declension_json)
-- declension_json: {"1s":"שלי","2ms":"שלך",...}
```

### SRS (Spaced Repetition System):
```sql
srs_cards (id, user_id, card_type, content_id, front_json, back_json, created_at)
-- card_type: word, sentence, grammar, listening, cloze, conjugation

srs_reviews (id, card_id, reviewed_at, quality, response_time_ms)
-- quality: 0(забыл) 1(трудно) 2(нормально) 3(легко)

srs_schedule (id, card_id, next_review, interval_days, ease_factor, repetitions, lapses)
-- SM-2 алгоритм с модификациями
```

### Контент и упражнения:
```sql
lessons (id, level_id, unit, order, title_ru, title_he, description, type)
-- type: vocabulary, grammar, reading, listening, conversation, culture

exercises (id, lesson_id, type, difficulty, prompt_json, answer_json, explanation_json, points)
-- type: multiple_choice, fill_blank, translate_to_he, translate_to_ru,
--        match_pairs, word_order, dictation, cloze_delete,
--        conjugation_table, root_identification, listening_comprehension,
--        picture_word, sentence_builder, error_correction

exercise_results (id, user_id, exercise_id, answer_json, is_correct, time_ms, attempt, created_at)

reading_texts (id, level_id, title_he, title_ru, content_he, content_ru, vocabulary_json, audio_url, category)
-- category: news, story, dialog, letter, essay, culture

dialogues (id, level_id, title, situation_ru, lines_json, vocabulary_json, audio_url)
-- lines_json: [{"speaker":"א","text_he":"...","text_ru":"...","audio":"..."},...]
```

### Темы и навыки:
```sql
topics (id, name_ru, name_he, icon, level_id, order)
-- ~50 тем: приветствия, семья, еда, здоровье, работа, транспорт, банк, медицина,
-- армия, политика, религия, СМИ, технологии, природа, эмоции, шопинг, путешествия...

skills (id, name, description, max_level)
-- reading, writing, listening, speaking, grammar, vocabulary

user_skill_progress (user_id, skill_id, level, xp, last_practice)
user_topic_progress (user_id, topic_id, words_learned, exercises_done, mastery_pct)
```

---

## Модули платформы (реализовать по порядку)

### 1. 🔤 Модуль «Алфавит» (Алеф-Бет)
- Интерактивное изучение 22 букв + 5 конечных форм (софиёт)
- Каждая буква: печатная + прописная форма, произношение, числовое значение, мнемоника
- Упражнения: распознавание буквы → чтение слога → чтение слова
- Огласовки (никкуд): все гласные знаки с озвучкой
- Виджет «напиши букву» (canvas/SVG + распознавание)
- Прогресс: мини-тест после каждых 5 букв

### 2. 📖 Модуль «Словарь»
- Загрузить **весь Excel-словарь Бет-уровня** (1215 записей) как seed-данные
- Карточка слова: иврит (с никкуд и без) + транслитерация + перевод + часть речи + корень + биньян + перекрёстные ссылки + частотность + примеры
- Фильтры: по уровню, букве, теме, части речи, биньяну, корню, частотности
- Поиск: по ивриту, транслитерации, русскому переводу
- Семьи корней: визуализация дерева однокоренных слов (React Flow / D3.js)
- Ежедневные новые слова (настраиваемое количество: 5-30)
- Статистика: изучено / в процессе / новых / просрочено

### 3. 🧠 Модуль «SRS-карточки» (ядро системы)
- Реализация алгоритма **SM-2** (SuperMemo 2) с модификациями:
  ```
  if quality >= 2:  # правильный ответ
      if repetitions == 0: interval = 1
      elif repetitions == 1: interval = 6
      else: interval = round(interval * ease_factor)
      repetitions += 1
  else:  # ошибка
      repetitions = 0
      interval = 1
      lapses += 1
  ease_factor = max(1.3, ease_factor + 0.1 - (3-quality) * (0.08 + (3-quality) * 0.02))
  next_review = now + timedelta(days=interval)
  ```
- Типы карточек (генерируются автоматически из словаря):
  - **Иврит → Русский** (распознавание)
  - **Русский → Иврит** (воспроизведение, сложнее)
  - **Аудио → Значение** (аудирование)
  - **Предложение с пропуском** (cloze deletion)
  - **Спряжение глагола** (время + лицо → форма)
  - **Корень → Производные** (словообразование)
  - **Картинка → Слово** (визуальная ассоциация)
- Сессия: 20-50 карточек, миксуя новые + повторение
- Статистика: график запоминания, heat-map активности, прогноз нагрузки
- **Leech-detection**: автоматическое выявление слов-«пиявок» (>5 ошибок) с предложением мнемоники

### 4. 📝 Модуль «Грамматика»
- Структурированные уроки по темам:
  - **Алеф**: определённый артикль, род и число, местоимения, предлоги, смихут, настоящее время (паъаль)
  - **Бет**: все 7 биньянов, прошедшее/будущее время, степени сравнения, причастия, инфинитивы, повелительное наклонение, придаточные предложения, пассивные биньяны (пуъаль/hуфъаль), притяжательные суффиксы
  - **Гимель-Вав**: литературный иврит, идиомы, стили речи, деловой иврит, академический иврит
- Интерактивные таблицы спряжения (все биньяны × все времена × все лица)
- Конструктор предложений (drag-and-drop слов в правильный порядок)
- Склонение предлогов (интерактивная таблица с озвучкой)
- Упражнения на каждое правило с мгновенной обратной связью

### 5. 📚 Модуль «Чтение»
- Адаптированные тексты по уровням (5+ текстов на каждый уровень)
- **Интерактивный читатель**: клик по слову → всплывающая карточка (перевод, транслитерация, корень, добавить в SRS)
- Подсветка изученных / новых / незнакомых слов разными цветами
- Послетекстовые задания: вопросы на понимание, true/false, заполнение пропусков
- Категории: новости, рассказы, диалоги, письма, культура, юмор
- Параллельный текст (иврит + русский) с возможностью скрыть одну из сторон

### 6. 🎧 Модуль «Аудирование»
- Озвучка слов и предложений через Web Speech API / TTS
- Диктанты: прослушай → запиши (с проверкой посимвольно)
- Упражнения на минимальные пары (различение похожих звуков)
- Диалоги с аудио: слушай → отвечай на вопросы
- Скорость воспроизведения: 0.5x / 0.75x / 1x / 1.25x
- Режим «душ из иврита»: фоновое прослушивание слов/фраз с паузами

### 7. ✍️ Модуль «Письмо»
- Клавиатура иврита (on-screen) с подсветкой
- Упражнения: перевод RU→HE с проверкой (fuzzy-matching для мелких ошибок)
- Свободное письмо с подсветкой ошибок (базовая проверка орфографии)
- Прописные буквы: тренажёр начертания (canvas)

### 8. 💬 Модуль «Диалоги и ситуации»
- Готовые диалоги по ситуациям (магазин, врач, банк, аэропорт, ульпан, работа, ...)
- Ролевая игра: пользователь отвечает за одного из участников
- Выбор из вариантов ответа / свободный ввод
- ~30 ситуаций с 3-5 вариациями каждая

### 9. 🏆 Модуль «Геймификация»
- **XP**: за каждое действие (карточка, упражнение, текст, вход)
- **Streak**: дни подряд (визуальный огонёк, как в Duolingo)
- **Уровни**: от «Олэ Хадаш» до «Сабра» (12 уровней)
- **Достижения/бейджи**: 50+ достижений (первое слово, 100 слов, все буквы, первый текст, ...)
- **Ежедневные цели**: настраиваемые (5/10/15/20 минут)
- **Еженедельный отчёт**: email-дайджест с прогрессом

### 10. 📊 Модуль «Аналитика и дашборд»
- **Главный дашборд**: 
  - Текущий уровень и прогресс до следующего
  - Streak и XP
  - Слова: изучено / в процессе / новых сегодня / просрочено
  - Навыки-радар (чтение/письмо/аудирование/говорение/грамматика/словарь)
  - Рекомендация: что учить сегодня (умный алгоритм)
- **Статистика**: 
  - График активности (heat-map календарь GitHub-style)
  - Кривая запоминания
  - Время по модулям
  - Топ-проблемные слова (leech list)
  - Прогресс по биньянам
  - Покрытие по буквам алфавита

### 11. 🌍 Модуль «Культура и реалии Израиля»
- Статьи о праздниках (Шаббат, Песах, Ханука, Пурим, Йом Кипур, ...)
- Бытовые реалии: армия, ульпан, кибуц, шук, шерут, купат холим, ...
- Полезные аббревиатуры: ת"ז, ב"ל, צה"ל, בג"ץ, ...
- Сленг и разговорные выражения (יאללה, סבבה, אחלה, ...)

---

## Seed-данные (начальная загрузка)

### Из Excel-файла (уже есть: `hebrew_bet_smart_dictionary.xlsx`):
- 1215 слов с транслитерацией, переводом, корнями, биньянами, перекрёстными ссылками
- 256 семей корней (708 связанных слов)
- Написать скрипт парсинга Excel → PostgreSQL seed

### Генерировать программно:
- Таблицы спряжения для всех биньянов (7 × 3 времени × 10 лиц)
- Склонение 20+ предлогов
- Примеры предложений: по 3-5 на каждое слово
- Упражнения: по 5-10 на каждый грамматический топик
- Тексты для чтения: минимум 3 на каждый уровень
- Диалоги: минимум 5 на каждый уровень

---

## Технические требования

### Performance:
- Первая загрузка < 3 сек
- SRS-ответ → следующая карточка < 200ms
- Поиск по словарю < 100ms (PostgreSQL full-text search + trigram index)

### Безопасность:
- bcrypt для паролей
- JWT с refresh-token rotation
- CORS настроен только на localhost
- SQL injection protection (SQLAlchemy ORM)
- Rate limiting на API (Redis)

### UX/UI:
- RTL-поддержка для ивритских блоков (CSS `direction: rtl`)
- Шрифт иврита: David Libre или Frank Ruhl Libre (Google Fonts)
- Тёмная/светлая тема
- Mobile-first responsive (≥320px)
- Keyboard shortcuts для SRS (1-4 для оценки, Enter для показа)
- Звуковые эффекты (правильно/неправильно/достижение)

### DevOps:
- `docker compose up` — единственная команда для запуска
- `.env` файл для конфигурации (DB пароль, JWT secret, ...)
- Авто-миграции при первом запуске
- Seed-скрипт заполняет БД при пустой базе
- Healthcheck для всех сервисов
- Логирование в stdout (docker logs)

---

## Порядок реализации (этапы)

### Этап 1: Инфраструктура
1. `docker-compose.yml` со всеми сервисами
2. Backend каркас: FastAPI + SQLAlchemy + Alembic + JWT auth
3. Frontend каркас: React + Router + TailwindCSS + RTL
4. Nginx конфигурация
5. Модели данных + миграции
6. Auth: регистрация / вход / JWT

### Этап 2: Ядро
7. Seed-скрипт (парсинг Excel словаря → БД)
8. API словаря (CRUD + поиск + фильтры)
9. UI словаря (карточки + фильтры + поиск + семьи корней)
10. SRS-движок (SM-2 + API + Redis-очередь)
11. UI карточек (сессия + анимации + статистика)

### Этап 3: Контент
12. Модуль «Алфавит» (уроки + упражнения)
13. Модуль «Грамматика» (уроки + таблицы + упражнения)
14. Генератор упражнений (все типы)
15. Модуль «Чтение» (интерактивный читатель)

### Этап 4: Навыки
16. Модуль «Аудирование» (TTS + диктанты)
17. Модуль «Письмо» (клавиатура + перевод)
18. Модуль «Диалоги» (ситуации + ролевая игра)

### Этап 5: Мотивация
19. Геймификация (XP, streak, достижения, уровни)
20. Дашборд и аналитика (графики, рекомендации)
21. Модуль «Культура»

---

## Критерии приёмки

- [ ] `docker compose up` запускает всё без ошибок
- [ ] Регистрация → вход → дашборд работает
- [ ] Словарь загружен (1215+ слов), поиск работает
- [ ] SRS-карточки: создание, сессия, SM-2 алгоритм корректен
- [ ] Минимум 3 типа упражнений функционируют
- [ ] Алфавит: все 27 букв с упражнениями
- [ ] Хотя бы 1 грамматический урок с таблицей спряжения
- [ ] Интерактивный читатель: 1+ текст с кликабельными словами
- [ ] Streak и XP считаются, бейджи выдаются
- [ ] Мобильная версия читаемая (responsive)
- [ ] RTL корректно работает для ивритских блоков

---

## Важные заметки

1. **Язык кода**: Python + TypeScript. Комментарии в коде — на английском. UI — на русском.
2. **Никаких внешних API** (кроме Google Fonts). Всё работает оффлайн после запуска.
3. **TTS**: использовать Web Speech API (браузерный) или edge-tts (Python) для озвучки иврита.
4. **Файл словаря** уже существует: `hebrew_bet_smart_dictionary.xlsx` — парсить через openpyxl.
5. **Не перфекционизм, а MVP**: лучше рабочие 60% фич, чем нерабочие 100%.
6. **Начинай с этапа 1**, жди подтверждения, затем следующий этап.
