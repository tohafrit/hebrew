import { useState } from "react";
import { useLeaderboard, useUserRank, useChallenges } from "@/hooks/use-leaderboard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export function LeaderboardPage() {
  const [period, setPeriod] = useState<"weekly" | "all_time">("weekly");
  const { data: board, isLoading } = useLeaderboard(period);
  const { data: rank } = useUserRank(period);
  const { data: challenges } = useChallenges();

  if (isLoading) return <p className="text-center py-12 text-muted-foreground">Загрузка...</p>;

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Рейтинг</h1>

      {/* Period tabs */}
      <div className="flex gap-2">
        <Button variant={period === "weekly" ? "default" : "outline"} size="sm" onClick={() => setPeriod("weekly")}>
          За неделю
        </Button>
        <Button variant={period === "all_time" ? "default" : "outline"} size="sm" onClick={() => setPeriod("all_time")}>
          За всё время
        </Button>
      </div>

      {/* User rank */}
      {rank && (
        <Card>
          <CardContent className="py-4 flex items-center justify-between">
            <span className="text-muted-foreground">Ваше место</span>
            <span className="text-2xl font-bold">#{rank.rank}</span>
          </CardContent>
        </Card>
      )}

      {/* Leaderboard table */}
      <Card>
        <CardHeader><CardTitle>Таблица лидеров</CardTitle></CardHeader>
        <CardContent>
          <div className="divide-y">
            {board?.entries.map((entry, i) => (
              <div
                key={entry.user_id}
                className={cn(
                  "flex items-center justify-between py-3 px-2 rounded",
                  entry.is_current_user && "bg-primary/5"
                )}
              >
                <div className="flex items-center gap-3">
                  <span className={cn(
                    "w-8 text-center font-bold",
                    i < 3 && "text-lg",
                    i === 0 && "text-yellow-500",
                    i === 1 && "text-gray-400",
                    i === 2 && "text-amber-600",
                  )}>
                    {i + 1}
                  </span>
                  <span className={cn("font-medium", entry.is_current_user && "text-primary")}>
                    {entry.display_name}
                    {entry.is_current_user && <Badge variant="secondary" className="ml-2">Вы</Badge>}
                  </span>
                </div>
                <span className="font-mono text-sm">{entry.xp} XP</span>
              </div>
            ))}
            {(!board?.entries.length) && (
              <p className="text-center py-6 text-muted-foreground">Пока нет данных</p>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Challenges */}
      {challenges && challenges.length > 0 && (
        <Card>
          <CardHeader><CardTitle>Недельные задания</CardTitle></CardHeader>
          <CardContent className="space-y-4">
            {challenges.map(ch => (
              <div key={ch.id} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-medium">{ch.title_ru}</span>
                  <Badge variant="outline">+{ch.xp_reward} XP</Badge>
                </div>
                <p className="text-sm text-muted-foreground">{ch.description_ru}</p>
                {ch.progress !== undefined && (
                  <div className="space-y-1">
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>{ch.progress} / {ch.target_count}</span>
                      <span>{Math.min(100, Math.round((ch.progress / ch.target_count) * 100))}%</span>
                    </div>
                    <div className="h-2 bg-secondary rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary rounded-full transition-all"
                        style={{ width: `${Math.min(100, (ch.progress / ch.target_count) * 100)}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
