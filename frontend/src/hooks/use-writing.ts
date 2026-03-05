import { useMutation } from "@tanstack/react-query";
import api from "@/lib/api";

export interface UnknownWord {
  token: string;
  suggestion: string | null;
  dictionary_url: string | null;
}

export interface WritingFeedback {
  word_count: number;
  sentence_count: number;
  known_count: number;
  unknown_count: number;
  known_pct: number;
  level_breakdown: Record<string, number>;
  unknown_words: UnknownWord[];
  feedback: string[];
}

export function useCheckWriting() {
  return useMutation<WritingFeedback, Error, string>({
    mutationFn: async (text) => {
      const { data } = await api.post("/reader/check-writing", { text });
      return data;
    },
  });
}
