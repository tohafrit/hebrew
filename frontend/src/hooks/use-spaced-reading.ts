import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";

export interface DueReading {
  schedule_id: string;
  text_id: number;
  title_he: string;
  title_ru: string;
  level_id: number;
  review_count: number;
  last_known_pct: number;
  interval_days: number;
  next_review: string;
}

export function useDueReadings() {
  return useQuery<DueReading[]>({
    queryKey: ["spaced-reading-due"],
    queryFn: async () => {
      const { data } = await api.get("/reader/spaced-reading/due");
      return data;
    },
  });
}

export function useEnrollReading() {
  const queryClient = useQueryClient();
  return useMutation<{ enrolled: boolean }, Error, { text_id: number }>({
    mutationFn: async (body) => {
      const { data } = await api.post("/reader/spaced-reading/enroll", body);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["spaced-reading-due"] });
    },
  });
}

export function useRecordReview() {
  const queryClient = useQueryClient();
  return useMutation<unknown, Error, { text_id: number; known_pct: number }>({
    mutationFn: async (body) => {
      const { data } = await api.post("/reader/spaced-reading/review", body);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["spaced-reading-due"] });
    },
  });
}

export function useReadingImprovement(textId?: number) {
  return useQuery<{ text_id: number; review_count: number; last_known_pct: number }[]>({
    queryKey: ["reading-improvement", textId],
    queryFn: async () => {
      const params = textId ? { text_id: textId } : {};
      const { data } = await api.get("/reader/spaced-reading/improvement", { params });
      return data;
    },
  });
}
