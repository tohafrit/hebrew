import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface RootExplorerWord {
  id: number;
  hebrew: string;
  nikkud: string | null;
  transliteration: string | null;
  translation_ru: string;
  pos: string | null;
  level_id: number | null;
  frequency_rank: number | null;
}

export interface RootExplorerData {
  root: string;
  meaning_ru: string | null;
  words_by_pos: Record<string, RootExplorerWord[]>;
  total_words: number;
}

export function useRootExplorer(root: string | null) {
  return useQuery<RootExplorerData>({
    queryKey: ["root-explorer", root],
    queryFn: async () => {
      const { data } = await api.get(`/words/roots/explore/${root}`);
      return data;
    },
    enabled: root !== null && root.length > 0,
  });
}

export function useRootSearch(query: string) {
  return useQuery<{ id: number; root: string; meaning_ru: string | null }[]>({
    queryKey: ["root-search", query],
    queryFn: async () => {
      const { data } = await api.get("/words/roots/search", { params: { q: query } });
      return data;
    },
    enabled: query.length > 0,
  });
}
