import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface AlphabetLetter {
  id: number;
  letter: string;
  name_ru: string;
  translit: string;
  sound_description: string | null;
  numeric_value: number | null;
  is_sofit: boolean;
  sofit_of: string | null;
  order: number;
}

export interface NikkudMark {
  id: number;
  symbol: string;
  name_he: string;
  name_ru: string;
  sound: string;
  example_word: string | null;
  example_translit: string | null;
}

export interface AlphabetResponse {
  letters: AlphabetLetter[];
  nikkud: NikkudMark[];
}

export function useAlphabet() {
  return useQuery<AlphabetResponse>({
    queryKey: ["alphabet"],
    queryFn: async () => {
      const { data } = await api.get("/alphabet");
      return data;
    },
  });
}
