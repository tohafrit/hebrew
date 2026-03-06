import { useQuery, useMutation } from "@tanstack/react-query";
import api from "@/lib/api";

export interface LessonBrief {
  id: number;
  level_id: number;
  unit: number;
  order: number;
  title_ru: string;
  title_he: string | null;
  description: string | null;
  content_md: string | null;
  type: string;
}

export interface Exercise {
  id: number;
  lesson_id: number;
  type: string;
  difficulty: number;
  prompt_json: Record<string, any> | null;
  answer_json: Record<string, any> | null;
  explanation_json: Record<string, any> | null;
  points: number;
}

export interface LessonDetail extends LessonBrief {
  exercises: Exercise[];
}

export interface ExerciseCheckResponse {
  correct: boolean;
  correct_answer: any;
  explanation: string | null;
  points_earned: number;
}

export interface ReadingTextBrief {
  id: number;
  level_id: number;
  title_he: string;
  title_ru: string;
  category: string;
}

export interface ReadingTextDetail extends ReadingTextBrief {
  content_he: string;
  content_ru: string;
  vocabulary_json: Array<{ he: string; ru: string; translit?: string }> | null;
  audio_url: string | null;
}

export function useLessons(levelId?: number, type?: string) {
  return useQuery<LessonBrief[]>({
    queryKey: ["lessons", levelId, type],
    queryFn: async () => {
      const params: Record<string, any> = {};
      if (levelId) params.level_id = levelId;
      if (type) params.type = type;
      const { data } = await api.get("/lessons", { params });
      return data;
    },
  });
}

export function useLesson(lessonId: number | null) {
  return useQuery<LessonDetail>({
    queryKey: ["lesson", lessonId],
    queryFn: async () => {
      const { data } = await api.get(`/lessons/${lessonId}`);
      return data;
    },
    enabled: lessonId !== null,
  });
}

export function useCheckExercise() {
  return useMutation<ExerciseCheckResponse, Error, { exercise_id: number; answer: any }>({
    mutationFn: async (req) => {
      const { data } = await api.post("/exercises/check", req);
      return data;
    },
  });
}

export interface LessonStats {
  total: number;
  correct: number;
  accuracy_pct: number;
  time_ms: number;
}

export function useLessonStats(lessonId: number | null) {
  return useQuery<LessonStats>({
    queryKey: ["lesson-stats", lessonId],
    queryFn: async () => {
      const { data } = await api.get(`/lessons/${lessonId}/stats`);
      return data;
    },
    enabled: lessonId !== null,
  });
}

export function useReadingTexts(levelId?: number, category?: string) {
  return useQuery<ReadingTextBrief[]>({
    queryKey: ["reading-texts", levelId, category],
    queryFn: async () => {
      const params: Record<string, any> = {};
      if (levelId) params.level_id = levelId;
      if (category) params.category = category;
      const { data } = await api.get("/reading", { params });
      return data;
    },
  });
}

export function useReadingText(textId: number | null) {
  return useQuery<ReadingTextDetail>({
    queryKey: ["reading-text", textId],
    queryFn: async () => {
      const { data } = await api.get(`/reading/${textId}`);
      return data;
    },
    enabled: textId !== null,
  });
}
