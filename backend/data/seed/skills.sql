INSERT INTO public.skills (id, name, description, max_level) VALUES (1, 'reading', 'Чтение и понимание текстов', 10);
INSERT INTO public.skills (id, name, description, max_level) VALUES (2, 'writing', 'Письмо и составление текстов', 10);
INSERT INTO public.skills (id, name, description, max_level) VALUES (3, 'listening', 'Аудирование и понимание речи', 10);
INSERT INTO public.skills (id, name, description, max_level) VALUES (4, 'speaking', 'Говорение и произношение', 10);
INSERT INTO public.skills (id, name, description, max_level) VALUES (5, 'grammar', 'Грамматика и языковые структуры', 10);
INSERT INTO public.skills (id, name, description, max_level) VALUES (6, 'vocabulary', 'Словарный запас', 10);
SELECT pg_catalog.setval('public.skills_id_seq', 7, false);
