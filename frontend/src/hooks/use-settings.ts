import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";

export interface UserSettings {
  daily_goal_minutes: number;
  daily_new_cards: number;
  srs_algorithm: string;
  ui_theme: string;
  notifications: boolean;
}

export function useSettings() {
  return useQuery<UserSettings>({
    queryKey: ["settings"],
    queryFn: async () => {
      const { data } = await api.get("/settings");
      return data;
    },
  });
}

export function useUpdateSettings() {
  const qc = useQueryClient();
  return useMutation<UserSettings, Error, Partial<UserSettings>>({
    mutationFn: async (body) => {
      const { data } = await api.put("/settings", body);
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["settings"] });
    },
  });
}
