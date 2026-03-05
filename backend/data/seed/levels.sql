INSERT INTO public.levels (id, code, name_ru, name_he, description, "order", cefr_equivalent) VALUES (1, 'alef', 'Алеф', 'אלף', 'Начальный уровень: алфавит, базовые слова, простые фразы', 1, 'A1');
INSERT INTO public.levels (id, code, name_ru, name_he, description, "order", cefr_equivalent) VALUES (2, 'bet', 'Бет', 'בית', 'Элементарный: повседневные темы, простые предложения, настоящее время', 2, 'A2');
INSERT INTO public.levels (id, code, name_ru, name_he, description, "order", cefr_equivalent) VALUES (3, 'gimel', 'Гимель', 'גימל', 'Средний: все времена, биньяны, чтение адаптированных текстов', 3, 'B1');
INSERT INTO public.levels (id, code, name_ru, name_he, description, "order", cefr_equivalent) VALUES (4, 'dalet', 'Далет', 'דלת', 'Выше среднего: сложные тексты, деловой иврит, СМИ', 4, 'B2');
INSERT INTO public.levels (id, code, name_ru, name_he, description, "order", cefr_equivalent) VALUES (5, 'he', 'Хей', 'הא', 'Продвинутый: литературный иврит, академические тексты, идиомы', 5, 'C1');
INSERT INTO public.levels (id, code, name_ru, name_he, description, "order", cefr_equivalent) VALUES (6, 'vav', 'Вав', 'ואו', 'Свободное владение: носительский уровень, все стили речи', 6, 'C2');
SELECT pg_catalog.setval('public.levels_id_seq', 7, false);
