import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import api from "@/lib/api";

export interface PathStep {
  id: number;
  level_id: number;
  unit: number;
  step: number;
  step_type: string;
  content_id: number | null;
  title_ru: string;
  title_he: string | null;
  description_ru: string | null;
  icon: string | null;
  completed: boolean;
}

export interface PathResponse {
  steps: PathStep[];
  next_step_id: number | null;
}

export function useLearningPath(levelId?: number) {
  return useQuery<PathResponse>({
    queryKey: ["learning-path", levelId],
    queryFn: async () => {
      const params: Record<string, any> = {};
      if (levelId) params.level_id = levelId;
      const { data } = await api.get("/path", { params });
      return data;
    },
  });
}

export function useCompleteStep() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (stepId: number) => {
      const { data } = await api.post("/path/complete", { step_id: stepId });
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["learning-path"] });
    },
  });
}
