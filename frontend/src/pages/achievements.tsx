import { useEffect } from "react";
import {
  useAchievementDefs,
  useMyAchievements,
  useCheckAchievements,
} from "@/hooks/use-gamification";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const CATEGORY_LABELS: Record<string, string> = {
  beginner: "Начало пути",
  vocabulary: "Словарный запас",
  grammar: "Грамматика",
  practice: "Практика",
  streak: "Серия",
  mastery: "Мастерство",
  social: "Социальные",
  culture: "Культура",
};

const CATEGORY_ORDER = [
  "beginner",
  "vocabulary",
  "grammar",
  "practice",
  "streak",
  "mastery",
  "social",
  "culture",
];

export function AchievementsPage() {
  const { data: defs, isLoading: defsLoading } = useAchievementDefs();
  const { data: mine, isLoading: mineLoading } = useMyAchievements();
  const checkMutation = useCheckAchievements();

  // Check for new achievements on page load
  useEffect(() => {
    checkMutation.mutate();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (defsLoading || mineLoading) {
    return <p className="text-center py-12 text-muted-foreground">Загрузка...</p>;
  }

  const unlockedCodes = new Set(mine?.map((a) => a.type) ?? []);
  const unlockedCount = unlockedCodes.size;
  const totalCount = defs?.length ?? 0;

  // Group by category
  const grouped = new Map<string, typeof defs>();
  for (const d of defs ?? []) {
    const cat = d.category;
    if (!grouped.has(cat)) grouped.set(cat, []);
    grouped.get(cat)!.push(d);
  }

  const sortedCategories = CATEGORY_ORDER.filter((c) => grouped.has(c));
  // Add any categories not in CATEGORY_ORDER
  for (const cat of grouped.keys()) {
    if (!sortedCategories.includes(cat)) sortedCategories.push(cat);
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Достижения</h1>
          <p className="text-muted-foreground">
            Разблокировано: {unlockedCount} / {totalCount}
          </p>
        </div>
        <Button
          variant="outline"
          size="sm"
          onClick={() => checkMutation.mutate()}
          disabled={checkMutation.isPending}
        >
          {checkMutation.isPending ? "Проверка..." : "Проверить"}
        </Button>
      </div>

      {/* Progress bar */}
      <div className="h-3 rounded-full bg-muted">
        <div
          className="h-3 rounded-full bg-gradient-to-r from-yellow-400 to-amber-500 transition-all"
          style={{ width: `${totalCount > 0 ? (unlockedCount / totalCount) * 100 : 0}%` }}
        />
      </div>

      {checkMutation.data && checkMutation.data.length > 0 && (
        <Card className="border-green-500/50 bg-green-500/5">
          <CardContent className="pt-4">
            <p className="font-medium text-green-700">
              Новые достижения: {checkMutation.data.join(", ")}
            </p>
          </CardContent>
        </Card>
      )}

      {sortedCategories.map((cat) => {
        const items = grouped.get(cat) ?? [];
        return (
          <div key={cat}>
            <h2 className="text-lg font-semibold mb-3">
              {CATEGORY_LABELS[cat] ?? cat}
            </h2>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {items.map((def) => {
                const unlocked = unlockedCodes.has(def.code);
                const unlockedAt = mine?.find((a) => a.type === def.code)?.unlocked_at;
                return (
                  <Card
                    key={def.id}
                    className={unlocked ? "border-amber-400/50" : "opacity-60"}
                  >
                    <CardHeader className="pb-2">
                      <CardTitle className="text-base flex items-center gap-2">
                        <span className="text-xl">{def.icon ?? (unlocked ? "🏆" : "🔒")}</span>
                        <span>{def.title_ru}</span>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-sm text-muted-foreground">{def.description_ru}</p>
                      {unlocked && unlockedAt && (
                        <p className="text-xs text-amber-600 mt-1">
                          Получено: {new Date(unlockedAt).toLocaleDateString("ru-RU")}
                        </p>
                      )}
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}
