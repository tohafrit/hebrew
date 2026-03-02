import { useQuery } from "@tanstack/react-query";
import api from "@/lib/api";

interface HealthStatus {
  status: string;
  db: boolean;
  redis: boolean;
}

export function useHealth() {
  return useQuery<HealthStatus>({
    queryKey: ["health"],
    queryFn: async () => {
      const { data } = await api.get("/health");
      return data;
    },
    refetchInterval: 30000,
  });
}
