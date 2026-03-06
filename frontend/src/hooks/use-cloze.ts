import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface ClozeExercise {
  sentence_he: string;
  sentence_he_blanked: string;
  sentence_ru: string;
  hint: string;
  answer: string;
  transliteration: string | null;
}

export function useClozeExercises(textId: number | null, count = 10) {
  return useQuery<{ exercises: ClozeExercise[]; text_id: number }>({
    queryKey: ["cloze", textId, count],
    queryFn: async () => {
      const { data } = await api.get(`/reading/${textId}/cloze`, { params: { count } });
      return data;
    },
    enabled: textId !== null,
  });
}
