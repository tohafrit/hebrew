import { useEffect, useRef } from "react";
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

/**
 * Auto-complete a learning path step when content is finished.
 * Finds the step matching (stepType, contentId) and marks it complete.
 * @param stepType - e.g. "vocabulary", "exercise", "reading", "dialogue"
 * @param contentId - the content_id of the completed content
 * @param isDone - trigger: set to true when the content is done
 */
export function useAutoCompleteStep(
  stepType: string,
  contentId: number | null,
  isDone: boolean,
) {
  const { data } = useLearningPath();
  const completeStep = useCompleteStep();
  const completedRef = useRef(false);

  useEffect(() => {
    if (!isDone || !contentId || !data || completedRef.current) return;

    const step = data.steps.find(
      (s) => s.step_type === stepType && s.content_id === contentId && !s.completed,
    );
    if (step) {
      completedRef.current = true;
      completeStep.mutate(step.id);
    }
  }, [isDone, contentId, data, stepType, completeStep]);
}
