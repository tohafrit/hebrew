import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface ExerciseMistake {
  exercise_id: number;
  exercise_type: string;
  prompt: Record<string, unknown> | null;
  user_answer: Record<string, unknown> | null;
  correct_answer: Record<string, unknown> | null;
  created_at: string;
}

export interface SRSCardJson {
  hebrew?: string;
  nikkud?: string;
  translation?: string;
  transliteration?: string;
  pos?: string;
  root?: string;
  [key: string]: unknown;
}

export interface SRSFailure {
  card_id: string;
  card_type: string;
  front: SRSCardJson | null;
  back: SRSCardJson | null;
  quality: number;
  reviewed_at: string;
}

export interface MistakesData {
  exercise_mistakes: ExerciseMistake[];
  srs_failures: SRSFailure[];
}

export function useMistakes(days: number = 30) {
  return useQuery<MistakesData>({
    queryKey: ["mistakes", days],
    queryFn: async () => {
      const { data } = await api.get("/stats/mistakes", { params: { days } });
      return data;
    },
  });
}

export interface ErrorPattern {
  type: string;
  count: number;
  pct: number;
  tip: string;
  examples: { expected: string; got: string }[];
}

export interface ErrorPatternsData {
  patterns: ErrorPattern[];
  total_mistakes: number;
  top_pattern: string | null;
}

export function useErrorPatterns(days: number = 30) {
  return useQuery<ErrorPatternsData>({
    queryKey: ["error-patterns", days],
    queryFn: async () => {
      const { data } = await api.get("/stats/error-patterns", { params: { days } });
      return data;
    },
  });
}
