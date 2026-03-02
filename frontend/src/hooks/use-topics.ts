import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface TopicWithProgress {
  id: number;
  name_ru: string;
  name_he: string | null;
  icon: string | null;
  level_id: number | null;
  order: number;
  words_learned: number;
  exercises_done: number;
  mastery_pct: number;
}

export function useTopics(levelId?: number) {
  return useQuery<TopicWithProgress[]>({
    queryKey: ["topics", levelId],
    queryFn: async () => {
      const params = levelId ? { level_id: levelId } : {};
      const { data } = await api.get("/topics", { params });
      return data;
    },
  });
}
