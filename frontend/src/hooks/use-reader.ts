import { useMutation, useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface TokenAnnotation {
  token: string;
  clean: string;
  word_id: number | null;
  hebrew: string | null;
  translation_ru: string | null;
  transliteration: string | null;
  pos: string | null;
  root: string | null;
  level_id: number | null;
  match_type: string | null; // "exact" | "form" | "conjugation" | "prefix" | "number" | "proper_noun"
  is_space: boolean;
}

export interface AnalyzeResponse {
  tokens: TokenAnnotation[];
  stats: {
    known_count: number;
    unknown_count: number;
    total_words: number;
  };
}

export function useAnalyzeText() {
  return useMutation<AnalyzeResponse, Error, string>({
    mutationFn: async (text: string) => {
      const { data } = await api.post("/reader/analyze", { text });
      return data;
    },
  });
}

export interface ReadingSession {
  id: string;
  text_snippet: string;
  word_count: number;
  known_pct: number;
  level_breakdown_json: Record<string, number> | null;
  created_at: string;
}

export interface RecommendedText {
  id: number;
  level_id: number;
  title_he: string;
  title_ru: string;
  category: string;
}

export function useReaderHistory() {
  return useQuery<ReadingSession[]>({
    queryKey: ["reader-history"],
    queryFn: async () => {
      const { data } = await api.get("/reader/history");
      return data;
    },
  });
}

export function useReaderRecommendations() {
  return useQuery<RecommendedText[]>({
    queryKey: ["reader-recommendations"],
    queryFn: async () => {
      const { data } = await api.get("/reader/recommendations");
      return data;
    },
  });
}
