import { useQuery, useMutation } from "@tanstack/react-query";
import api from "@/lib/api";

export interface MinimalPairOption {
  letter: string;
  word: string;
  translation: string;
}

export interface MinimalPairQuestion {
  pair_id: string;
  target_word: string;
  target_translation: string;
  correct_letter: string;
  option1: MinimalPairOption;
  option2: MinimalPairOption;
}

export function useMinimalPairsDrill(count = 10) {
  return useQuery<{ questions: MinimalPairQuestion[] }>({
    queryKey: ["minimal-pairs-drill", count],
    queryFn: async () => {
      const { data } = await api.get("/minimal-pairs/drill", { params: { count } });
      return data;
    },
  });
}

export function useCheckMinimalPair() {
  return useMutation<{ correct: boolean; xp_earned: number }, Error, {
    pair_id: string;
    answer_letter: string;
    correct_letter: string;
  }>({
    mutationFn: async (body) => {
      const { data } = await api.post("/minimal-pairs/check", body);
      return data;
    },
  });
}
