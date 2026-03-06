import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface LeaderboardEntry {
  rank: number;
  user_id: string;
  display_name: string;
  level: number;
  xp: number;
}

export interface ChallengeProgress {
  id: number;
  title_ru: string;
  description_ru: string;
  challenge_type: string;
  target_count: number;
  xp_reward: number;
  current: number;
  completed: boolean;
}

export function useLeaderboard(period: string = "all_time") {
  return useQuery<{ entries: LeaderboardEntry[]; period: string }>({
    queryKey: ["leaderboard", period],
    queryFn: async () => {
      const { data } = await api.get("/leaderboard", { params: { period } });
      return data;
    },
  });
}

export function useUserRank(period: string = "all_time") {
  return useQuery<LeaderboardEntry>({
    queryKey: ["leaderboard-rank", period],
    queryFn: async () => {
      const { data } = await api.get("/leaderboard/rank", { params: { period } });
      return data;
    },
  });
}

export function useChallenges() {
  return useQuery<ChallengeProgress[]>({
    queryKey: ["challenges-progress"],
    queryFn: async () => {
      const { data } = await api.get("/challenges/progress");
      return data;
    },
  });
}
