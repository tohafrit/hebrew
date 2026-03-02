import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";

export interface AchievementDef {
  id: number;
  code: string;
  title_ru: string;
  description_ru: string;
  icon: string | null;
  category: string;
  condition_json: Record<string, unknown> | null;
}

export interface UserAchievement {
  id: string;
  type: string;
  unlocked_at: string;
}

export interface DailyActivity {
  date: string;
  xp_earned: number;
  exercises_done: number;
  reviews_done: number;
  time_minutes: number;
}

export interface StatsOverview {
  total_xp: number;
  current_level: number;
  level_name: string;
  xp_to_next_level: number;
  streak_days: number;
  total_words: number;
  total_cards: number;
  total_reviews: number;
  total_exercises: number;
  total_texts_read: number;
  total_dialogues: number;
  daily_activity: DailyActivity[];
  achievements_unlocked: number;
  achievements_total: number;
  skills: Record<string, number>;
}

export interface LevelInfo {
  level: number;
  xp_required: number;
  name: string;
}

export interface CultureArticleBrief {
  id: number;
  category: string;
  title_ru: string;
  title_he: string | null;
  level_id: number | null;
}

export interface CultureArticleDetail extends CultureArticleBrief {
  content_md: string;
}

export function useAchievementDefs() {
  return useQuery<AchievementDef[]>({
    queryKey: ["achievement-defs"],
    queryFn: async () => {
      const { data } = await api.get("/achievements/definitions");
      return data;
    },
  });
}

export function useMyAchievements() {
  return useQuery<UserAchievement[]>({
    queryKey: ["my-achievements"],
    queryFn: async () => {
      const { data } = await api.get("/achievements/mine");
      return data;
    },
  });
}

export function useCheckAchievements() {
  const qc = useQueryClient();
  return useMutation<string[]>({
    mutationFn: async () => {
      const { data } = await api.post("/achievements/check");
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["my-achievements"] });
      qc.invalidateQueries({ queryKey: ["stats-overview"] });
    },
  });
}

export function useStatsOverview() {
  return useQuery<StatsOverview>({
    queryKey: ["stats-overview"],
    queryFn: async () => {
      const { data } = await api.get("/stats/overview");
      return data;
    },
  });
}

export function useLevels() {
  return useQuery<LevelInfo[]>({
    queryKey: ["levels"],
    queryFn: async () => {
      const { data } = await api.get("/stats/levels");
      return data;
    },
  });
}

export function useCultureArticles(category?: string) {
  return useQuery<CultureArticleBrief[]>({
    queryKey: ["culture-articles", category],
    queryFn: async () => {
      const params = category ? { category } : {};
      const { data } = await api.get("/culture", { params });
      return data;
    },
  });
}

export function useCultureArticle(id: number | null) {
  return useQuery<CultureArticleDetail>({
    queryKey: ["culture-article", id],
    queryFn: async () => {
      const { data } = await api.get(`/culture/${id}`);
      return data;
    },
    enabled: id !== null,
  });
}
