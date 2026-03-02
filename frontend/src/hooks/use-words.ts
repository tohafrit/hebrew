import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface WordBrief {
  id: number;
  hebrew: string;
  nikkud: string | null;
  transliteration: string | null;
  translation_ru: string;
  pos: string | null;
  root: string | null;
  frequency_rank: number | null;
  level_id: number | null;
}

export interface WordDetail extends WordBrief {
  gender: string | null;
  number: string | null;
  audio_url: string | null;
  image_url: string | null;
  forms: WordForm[];
  examples: ExampleSentence[];
  root_family: RootFamilyWord[] | null;
}

export interface WordForm {
  id: number;
  form_type: string;
  hebrew: string;
  nikkud: string | null;
  transliteration: string | null;
  description: string | null;
}

export interface ExampleSentence {
  id: number;
  hebrew: string;
  translation_ru: string;
  transliteration: string | null;
}

export interface RootFamilyWord {
  id: number;
  hebrew: string;
  transliteration: string | null;
  translation_ru: string;
  pos: string | null;
}

export interface WordListResponse {
  items: WordBrief[];
  total: number;
  page: number;
  per_page: number;
}

export interface DictionaryStats {
  total_words: number;
  by_pos: Record<string, number>;
  by_frequency: Record<string, number>;
  root_families: number;
}

interface WordsParams {
  page?: number;
  per_page?: number;
  search?: string;
  pos?: string;
  frequency?: number;
  root?: string;
}

export function useWords(params: WordsParams = {}) {
  return useQuery<WordListResponse>({
    queryKey: ["words", params],
    queryFn: async () => {
      const { data } = await api.get("/words", { params });
      return data;
    },
  });
}

export function useWord(id: number | null) {
  return useQuery<WordDetail>({
    queryKey: ["word", id],
    queryFn: async () => {
      const { data } = await api.get(`/words/${id}`);
      return data;
    },
    enabled: id !== null,
  });
}

export function useDictionaryStats() {
  return useQuery<DictionaryStats>({
    queryKey: ["dictionary-stats"],
    queryFn: async () => {
      const { data } = await api.get("/words/stats");
      return data;
    },
  });
}

export interface RootFamilyOut {
  id: number;
  root: string;
  meaning_ru: string | null;
  words: RootFamilyWord[];
}

export interface RootFamiliesResponse {
  items: RootFamilyOut[];
  total: number;
  page: number;
  per_page: number;
}

export function useRootFamilies(params: { page?: number; per_page?: number } = {}) {
  return useQuery<RootFamiliesResponse>({
    queryKey: ["root-families", params],
    queryFn: async () => {
      const { data } = await api.get("/words/roots", { params });
      return data;
    },
  });
}

export function useRootFamily(root: string | null) {
  return useQuery<RootFamilyWord[]>({
    queryKey: ["root-family", root],
    queryFn: async () => {
      const { data } = await api.get(`/words/root/${root}`);
      return data;
    },
    enabled: root !== null,
  });
}
