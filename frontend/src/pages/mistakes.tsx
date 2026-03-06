import { useState } from "react";
import { Link } from "react-router-dom";
import { useMistakes } from "@/hooks/use-mistakes";
import { HebrewText } from "@/components/hebrew-text";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const EXERCISE_TYPE_LABELS: Record<string, string> = {
  multiple_choice: "Выбор ответа",
  fill_blank: "Заполнить пропуск",
  match_pairs: "Сопоставление",
  word_order: "Порядок слов",
  dictation: "Диктант",
  hebrew_typing: "Набор на иврите",
  translate_ru_he: "Перевод RU→HE",
  minimal_pairs: "Минимальные пары",
  listening_comprehension: "Аудирование",
};

const DAYS_OPTIONS = [7, 14, 30, 90];

type Tab = "exercises" | "srs";

function formatDate(iso: string) {
  const d = new Date(iso);
  return d.toLocaleDateString("ru-RU", { day: "numeric", month: "short" });
}

function extractText(json: Record<string, unknown> | null): string {
  if (!json) return "—";
  // Try common fields
  for (const key of ["text", "answer", "hebrew", "translation", "correct", "selected"]) {
    if (json[key] && typeof json[key] === "string") return json[key] as string;
  }
  if (json["correct_index"] !== undefined) return `Вариант ${json["correct_index"]}`;
  return JSON.stringify(json).slice(0, 60);
}

export function MistakesPage() {
  const [days, setDays] = useState(30);
  const [tab, setTab] = useState<Tab>("exercises");
  const { data, isLoading } = useMistakes(days);

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-12">Загрузка...</p>;
  }

  const exerciseCount = data?.exercise_mistakes.length ?? 0;
  const srsCount = data?.srs_failures.length ?? 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Журнал ошибок</h1>
        <div className="flex gap-1">
          {DAYS_OPTIONS.map((d) => (
            <Button
              key={d}
              variant={days === d ? "default" : "ghost"}
              size="sm"
              onClick={() => setDays(d)}
            >
              {d}д
            </Button>
          ))}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b">
        <button
          className={cn(
            "px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px",
            tab === "exercises"
              ? "border-primary text-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          )}
          onClick={() => setTab("exercises")}
        >
          Упражнения ({exerciseCount})
        </button>
        <button
          className={cn(
            "px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px",
            tab === "srs"
              ? "border-primary text-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          )}
          onClick={() => setTab("srs")}
        >
          SRS-карточки ({srsCount})
        </button>
      </div>

      {/* Exercise mistakes */}
      {tab === "exercises" && (
        <div className="space-y-2">
          {exerciseCount === 0 ? (
            <Card>
              <CardContent className="p-8 text-center text-muted-foreground">
                Нет ошибок за этот период
              </CardContent>
            </Card>
          ) : (
            data!.exercise_mistakes.map((m, i) => (
              <Card key={i}>
                <CardContent className="py-3 px-4">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0 space-y-1">
                      <div className="flex items-center gap-2">
                        <Badge variant="outline" className="text-xs shrink-0">
                          {EXERCISE_TYPE_LABELS[m.exercise_type] || m.exercise_type}
                        </Badge>
                        <span className="text-xs text-muted-foreground">{formatDate(m.created_at)}</span>
                      </div>
                      {m.prompt && (
                        <p className="text-sm">{extractText(m.prompt)}</p>
                      )}
                      <div className="flex gap-4 text-sm">
                        <span className="text-red-500">
                          {extractText(m.user_answer)}
                        </span>
                        <span className="text-green-600 font-medium">
                          {extractText(m.correct_answer)}
                        </span>
                      </div>
                    </div>
                    <Button variant="ghost" size="sm" asChild>
                      <Link to="/lessons">Повторить</Link>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}

      {/* SRS failures */}
      {tab === "srs" && (
        <div className="space-y-2">
          {srsCount === 0 ? (
            <Card>
              <CardContent className="p-8 text-center text-muted-foreground">
                Нет ошибок за этот период
              </CardContent>
            </Card>
          ) : (
            data!.srs_failures.map((f) => (
              <Card key={f.card_id}>
                <CardContent className="py-3 px-4">
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex-1 min-w-0 space-y-1">
                      <div className="flex items-center gap-2">
                        <Badge variant="outline" className="text-xs">
                          {f.card_type === "word_he_ru"
                            ? "HE→RU"
                            : f.card_type === "word_ru_he"
                            ? "RU→HE"
                            : f.card_type}
                        </Badge>
                        <span className="text-xs text-muted-foreground">{formatDate(f.reviewed_at)}</span>
                        <Badge variant={f.quality === 0 ? "destructive" : "secondary"} className="text-xs">
                          {f.quality === 0 ? "Не помню" : "Еле вспомнил"}
                        </Badge>
                      </div>
                      <div className="flex items-center gap-3 text-sm">
                        {f.front?.hebrew && (
                          <HebrewText size="lg" className="font-medium">
                            {String(f.front.hebrew)}
                          </HebrewText>
                        )}
                        {f.front?.translation && (
                          <span>{String(f.front.translation)}</span>
                        )}
                      </div>
                      <div className="text-sm text-green-600">
                        {f.back?.hebrew && (
                          <HebrewText size="sm" className="font-medium mr-2">
                            {String(f.back.hebrew)}
                          </HebrewText>
                        )}
                        {f.back?.translation && (
                          <span>{String(f.back.translation)}</span>
                        )}
                      </div>
                    </div>
                    <Button variant="ghost" size="sm" asChild>
                      <Link to="/srs">Повторить</Link>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}
    </div>
  );
}
