import { useQuery, useMutation } from "@tanstack/react-query";
import api from "@/lib/api";

export interface DialogueBrief {
  id: number;
  level_id: number;
  title: string;
  situation_ru: string | null;
}

export interface DialogueLine {
  speaker: string;
  speaker_name: string;
  text_he: string;
  text_ru: string;
  is_user: boolean;
  options?: string[];
  correct_option?: number;
}

export interface DialogueDetail extends DialogueBrief {
  lines_json: DialogueLine[];
  vocabulary_json: Array<{ he: string; ru: string; translit?: string }> | null;
  audio_url: string | null;
}

export interface DialogueCheckResponse {
  correct: boolean;
  correct_option: number;
  correct_text_he: string;
}

export function useDialogues(levelId?: number) {
  return useQuery<DialogueBrief[]>({
    queryKey: ["dialogues", levelId],
    queryFn: async () => {
      const params = levelId ? { level_id: levelId } : {};
      const { data } = await api.get("/dialogues", { params });
      return data;
    },
  });
}

export function useDialogue(dialogueId: number | null) {
  return useQuery<DialogueDetail>({
    queryKey: ["dialogue", dialogueId],
    queryFn: async () => {
      const { data } = await api.get(`/dialogues/${dialogueId}`);
      return data;
    },
    enabled: dialogueId !== null,
  });
}

export function useCheckDialogue() {
  return useMutation<DialogueCheckResponse, Error, { dialogue_id: number; line_index: number; selected_option: number }>({
    mutationFn: async (req) => {
      const { data } = await api.post("/dialogues/check", req);
      return data;
    },
  });
}
