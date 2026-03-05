INSERT INTO public.binyanim (id, name_he, name_ru, description, pattern, example_root, level_id) VALUES (1, 'פָּעַל', 'Пааль', 'Основной активный биньян, простое действие', 'קָטַל', 'כ.ת.ב', 1);
INSERT INTO public.binyanim (id, name_he, name_ru, description, pattern, example_root, level_id) VALUES (2, 'נִפְעַל', 'Нифъаль', 'Пассив от Пааль или возвратное действие', 'נִקְטַל', 'כ.ת.ב', 2);
INSERT INTO public.binyanim (id, name_he, name_ru, description, pattern, example_root, level_id) VALUES (3, 'פִּיעֵל', 'Пиэль', 'Интенсивное действие, каузатив', 'קִטֵּל', 'ד.ב.ר', 2);
INSERT INTO public.binyanim (id, name_he, name_ru, description, pattern, example_root, level_id) VALUES (4, 'פּוּעַל', 'Пуаль', 'Пассив от Пиэль', 'קֻטַּל', 'ד.ב.ר', 2);
INSERT INTO public.binyanim (id, name_he, name_ru, description, pattern, example_root, level_id) VALUES (5, 'הִפְעִיל', 'Хифъиль', 'Каузатив, побуждение к действию', 'הִקְטִיל', 'ז.כ.ר', 2);
INSERT INTO public.binyanim (id, name_he, name_ru, description, pattern, example_root, level_id) VALUES (6, 'הוּפְעַל', 'Хуфъаль', 'Пассив от Хифъиль', 'הוּקְטַל', 'ז.כ.ר', 3);
INSERT INTO public.binyanim (id, name_he, name_ru, description, pattern, example_root, level_id) VALUES (7, 'הִתְפַּעֵל', 'Хитпаэль', 'Возвратное действие, взаимное действие', 'הִתְקַטֵּל', 'ל.ב.ש', 2);
SELECT pg_catalog.setval('public.binyanim_id_seq', 8, false);
