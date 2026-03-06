import { useQuery, useMutation } from "@tanstack/react-query";
import api from "@/lib/api";

export interface PlacementQuestion {
  index: number;
  level: number;
  type: string;
  prompt_he: string | null;
  prompt_ru: string | null;
  hint: string | null;
  options: string[] | null;
}

export interface PlacementResult {
  assigned_level: number;
  total_questions: number;
  total_correct: number;
  per_level: Record<string, { correct: number; total: number }>;
}

export function usePlacementTest() {
  return useQuery<{ questions: PlacementQuestion[] }>({
    queryKey: ["placement-test"],
    queryFn: async () => {
      const { data } = await api.get("/placement/test");
      return data;
    },
    enabled: false, // manual trigger
  });
}

export function useSubmitPlacement() {
  return useMutation<PlacementResult, Error, { answers: { index: number; answer: string }[] }>({
    mutationFn: async (body) => {
      const { data } = await api.post("/placement/submit", body);
      return data;
    },
  });
}
