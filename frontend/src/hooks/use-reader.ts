import { useMutation } from "@tanstack/react-query";
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
  match_type: string | null; // "exact" | "form" | "conjugation" | "prefix"
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
