import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";

export interface SRSCard {
  id: string;
  card_type: string;
  content_id: number;
  front_json: Record<string, string | null>;
  back_json: Record<string, string | null>;
  next_review: string;
  interval_days: number;
  ease_factor: number;
  repetitions: number;
  lapses: number;
}

export interface SRSSession {
  cards: SRSCard[];
  total_due: number;
  new_cards: number;
}

export interface SRSStats {
  total_cards: number;
  due_today: number;
  new_cards: number;
  reviews_today: number;
  streak_days: number;
  average_ease: number | null;
}

export interface ReviewResult {
  card_id: string;
  next_review: string;
  interval_days: number;
  ease_factor: number;
  repetitions: number;
}

export function useSRSSession(limit = 20) {
  return useQuery<SRSSession>({
    queryKey: ["srs-session", limit],
    queryFn: async () => {
      const { data } = await api.get("/srs/session", { params: { limit } });
      return data;
    },
  });
}

export function useSRSStats() {
  return useQuery<SRSStats>({
    queryKey: ["srs-stats"],
    queryFn: async () => {
      const { data } = await api.get("/srs/stats");
      return data;
    },
  });
}

export function useReviewCard() {
  const queryClient = useQueryClient();

  return useMutation<ReviewResult, Error, { card_id: string; quality: number; response_time_ms?: number }>({
    mutationFn: async (body) => {
      const { data } = await api.post("/srs/review", body);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["srs-session"] });
      queryClient.invalidateQueries({ queryKey: ["srs-stats"] });
    },
  });
}

export interface LeechCard {
  id: string;
  card_type: string;
  content_id: number;
  front_json: Record<string, string | null>;
  back_json: Record<string, string | null>;
  lapses: number;
  ease_factor: number;
}

export interface LeechResponse {
  cards: LeechCard[];
  count: number;
}

export function useSRSLeeches(threshold = 5) {
  return useQuery<LeechResponse>({
    queryKey: ["srs-leeches", threshold],
    queryFn: async () => {
      const { data } = await api.get("/srs/leeches", { params: { threshold } });
      return data;
    },
  });
}

export function useCreateCards() {
  const queryClient = useQueryClient();

  return useMutation<{ created: number }, Error, { word_ids: number[]; card_types?: string[] }>({
    mutationFn: async (body) => {
      const { data } = await api.post("/srs/cards", {
        word_ids: body.word_ids,
        card_types: body.card_types || ["word_he_ru", "word_ru_he"],
      });
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["srs-session"] });
      queryClient.invalidateQueries({ queryKey: ["srs-stats"] });
    },
  });
}
