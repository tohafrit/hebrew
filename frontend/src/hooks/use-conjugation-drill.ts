import { useQuery, useMutation } from "@tanstack/react-query";
import api from "@/lib/api";

export interface DrillQuestion {
  word_id: number;
  word_hebrew: string;
  word_nikkud: string | null;
  translation_ru: string;
  binyan_id: number;
  binyan_name: string;
  tense: string;
  person: string;
  gender: string | null;
  number: string;
  correct_answer: string;
  correct_nikkud: string | null;
  transliteration: string | null;
  options: string[] | null;
}

export interface DrillCheckResponse {
  correct: boolean;
  correct_answer: string;
  correct_nikkud: string | null;
  transliteration: string | null;
}

interface DrillParams {
  level_id?: number;
  binyan_id?: number;
  tense?: string;
  count?: number;
}

export function useConjugationDrill(params: DrillParams = {}) {
  return useQuery<DrillQuestion[]>({
    queryKey: ["conjugation-drill", params],
    queryFn: async () => {
      const { data } = await api.get("/grammar/conjugation-drill", { params });
      return data;
    },
  });
}

export function useCheckDrillAnswer() {
  return useMutation<DrillCheckResponse, Error, {
    word_id: number;
    binyan_id: number;
    tense: string;
    person: string;
    answer: string;
  }>({
    mutationFn: async (body) => {
      const { data } = await api.post("/grammar/conjugation-drill/check", body);
      return data;
    },
  });
}

export interface TableDrillCell {
  person: string;
  gender: string;
  number: string;
  form_he: string;
  form_nikkud: string | null;
  transliteration: string | null;
  is_blank: boolean;
}

export interface TableDrillData {
  word_id: number;
  binyan_id: number;
  word_hebrew: string;
  word_nikkud: string | null;
  translation_ru: string;
  binyan_name: string;
  tense: string;
  cells: TableDrillCell[];
}

export interface TableDrillCheckResult {
  key: string;
  correct: boolean;
  expected: string;
  given: string;
}

interface TableDrillParams {
  word_id?: number;
  binyan_id?: number;
  tense?: string;
  level_id?: number;
  blank_count?: number;
}

export function useTableDrill(params: TableDrillParams = {}) {
  return useQuery<TableDrillData>({
    queryKey: ["table-drill", params],
    queryFn: async () => {
      const { data } = await api.get("/grammar/conjugation-table-drill", { params });
      return data;
    },
  });
}

export function useCheckTableDrill() {
  return useMutation<{ results: TableDrillCheckResult[]; score: number; total: number }, Error, {
    word_id: number;
    binyan_id: number;
    tense: string;
    answers: Record<string, string>;
  }>({
    mutationFn: async (body) => {
      const { data } = await api.post("/grammar/conjugation-table-drill/check", body);
      return data;
    },
  });
}
