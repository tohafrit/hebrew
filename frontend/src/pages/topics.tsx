import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTopics } from "@/hooks/use-topics";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const LEVEL_NAMES = [
  { id: undefined, label: "Все" },
  { id: 1, label: "Алеф" },
  { id: 2, label: "Бет" },
  { id: 3, label: "Гимель" },
  { id: 4, label: "Далет" },
  { id: 5, label: "Хей" },
  { id: 6, label: "Вав" },
];

export function TopicsPage() {
  const navigate = useNavigate();
  const [selectedLevel, setSelectedLevel] = useState<number | undefined>(undefined);
  const { data: topics, isLoading } = useTopics(selectedLevel);

  if (isLoading) {
    return <p className="text-center py-12 text-muted-foreground">Загрузка...</p>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Темы</h1>
      </div>

      {/* Level filter tabs */}
      <div className="flex flex-wrap gap-1">
        {LEVEL_NAMES.map((lvl) => (
          <Button
            key={lvl.label}
            variant={selectedLevel === lvl.id ? "default" : "ghost"}
            size="sm"
            onClick={() => setSelectedLevel(lvl.id)}
          >
            {lvl.label}
          </Button>
        ))}
      </div>

      {/* Topics grid */}
      <div className="grid gap-3 grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
        {topics?.map((topic) => (
          <Card
            key={topic.id}
            className="hover:shadow-md transition-shadow cursor-pointer"
            onClick={() => navigate(`/dictionary?search=&topic=${topic.id}`)}
          >
            <CardContent className="pt-4 pb-3 px-3 text-center space-y-2">
              <span className="text-2xl block">{topic.icon || "📘"}</span>
              <p className="font-medium text-sm leading-tight">{topic.name_ru}</p>
              {topic.name_he && (
                <p className="text-xs text-muted-foreground" dir="rtl">
                  {topic.name_he}
                </p>
              )}
              {/* Stats */}
              <div className="flex justify-center gap-2 text-[10px] text-muted-foreground">
                <span>{topic.words_learned} слов</span>
                <span>{topic.exercises_done} упр.</span>
              </div>
              {/* Mastery progress bar */}
              <div className="space-y-1">
                <div className="h-1.5 rounded-full bg-muted overflow-hidden">
                  <div
                    className={cn(
                      "h-full rounded-full transition-all",
                      topic.mastery_pct >= 80
                        ? "bg-green-500"
                        : topic.mastery_pct >= 40
                        ? "bg-yellow-500"
                        : "bg-primary"
                    )}
                    style={{ width: `${Math.min(100, topic.mastery_pct)}%` }}
                  />
                </div>
                <p className="text-[10px] text-muted-foreground">
                  {Math.round(topic.mastery_pct)}%
                </p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {topics?.length === 0 && (
        <p className="text-center text-muted-foreground py-8">
          Нет тем для этого уровня
        </p>
      )}
    </div>
  );
}
