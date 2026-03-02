import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface GrammarTopicBrief {
  id: number;
  title_ru: string;
  title_he: string | null;
  level_id: number;
  order: number;
  summary: string | null;
}

export interface GrammarRule {
  id: number;
  rule_text_ru: string;
  examples_json: Array<{ he: string; ru: string; translit?: string }> | null;
  exceptions_json: Array<{ text: string }> | null;
}

export interface GrammarTopicDetail extends GrammarTopicBrief {
  content_md: string | null;
  rules: GrammarRule[];
}

export interface Binyan {
  id: number;
  name_he: string;
  name_ru: string;
  description: string | null;
  pattern: string | null;
  example_root: string | null;
  level_id: number | null;
}

export function useGrammarTopics(levelId?: number) {
  return useQuery<GrammarTopicBrief[]>({
    queryKey: ["grammar-topics", levelId],
    queryFn: async () => {
      const params = levelId ? { level_id: levelId } : {};
      const { data } = await api.get("/grammar/topics", { params });
      return data;
    },
  });
}

export function useGrammarTopic(topicId: number | null) {
  return useQuery<GrammarTopicDetail>({
    queryKey: ["grammar-topic", topicId],
    queryFn: async () => {
      const { data } = await api.get(`/grammar/topics/${topicId}`);
      return data;
    },
    enabled: topicId !== null,
  });
}

export interface Conjugation {
  id: number;
  word_id: number;
  binyan_id: number;
  tense: string;
  person: string;
  gender: string;
  number: string;
  form_he: string;
  form_nikkud: string | null;
  transliteration: string | null;
}

export function useConjugations(wordId: number | null) {
  return useQuery<Conjugation[]>({
    queryKey: ["conjugations", wordId],
    queryFn: async () => {
      const { data } = await api.get(`/grammar/conjugations/${wordId}`);
      return data;
    },
    enabled: wordId !== null,
  });
}

export interface Preposition {
  id: number;
  base_form: string;
  meaning_ru: string;
  declension_json: Record<string, { form: string; translit: string }> | null;
}

export function usePrepositions() {
  return useQuery<Preposition[]>({
    queryKey: ["prepositions"],
    queryFn: async () => {
      const { data } = await api.get("/grammar/prepositions");
      return data;
    },
  });
}

export function useBinyanim() {
  return useQuery<Binyan[]>({
    queryKey: ["binyanim"],
    queryFn: async () => {
      const { data } = await api.get("/grammar/binyanim");
      return data;
    },
  });
}
