import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface GrammarCardBrief {
  id: number;
  title_ru: string;
  title_he: string | null;
  level_id: number;
  summary: string | null;
  tags: string[];
}

export interface GrammarCardDetail extends GrammarCardBrief {
  content_md: string | null;
  rules: { id: number; rule_text_ru: string; examples_json: unknown; exceptions_json: unknown }[];
}

export function useGrammarCards(params: { level_id?: number; tag?: string; page?: number } = {}) {
  return useQuery<GrammarCardBrief[]>({
    queryKey: ["grammar-cards", params],
    queryFn: async () => {
      const { data } = await api.get("/grammar/cards", { params });
      return data;
    },
  });
}

export function useGrammarCardDetail(topicId: number | null) {
  return useQuery<GrammarCardDetail>({
    queryKey: ["grammar-card", topicId],
    queryFn: async () => {
      const { data } = await api.get(`/grammar/cards/${topicId}`);
      return data;
    },
    enabled: topicId !== null,
  });
}

export function useRelatedGrammar(context: { error_type?: string; binyan?: string; tense?: string }) {
  return useQuery<{ topics: GrammarCardBrief[] }>({
    queryKey: ["grammar-related", context],
    queryFn: async () => {
      const { data } = await api.get("/grammar/related", { params: context });
      return data;
    },
    enabled: !!(context.error_type || context.binyan || context.tense),
  });
}

export function useGrammarTags() {
  return useQuery<{ tag: string; count: number }[]>({
    queryKey: ["grammar-tags"],
    queryFn: async () => {
      const { data } = await api.get("/grammar/tags");
      return data;
    },
  });
}
