import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

export interface Recommendation {
  type: string;
  priority: number;
  title: string;
  description: string;
  link: string;
  icon: string;
}

export function useRecommendations() {
  return useQuery<Recommendation[]>({
    queryKey: ["recommendations"],
    queryFn: async () => {
      const { data } = await api.get("/recommendations");
      return data;
    },
  });
}
