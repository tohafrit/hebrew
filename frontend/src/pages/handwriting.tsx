import { useState } from "react";
import { LETTER_TEMPLATES } from "@/data/letter-templates";
import { HandwritingCanvas } from "@/components/handwriting-canvas";
import { HebrewText } from "@/components/hebrew-text";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function HandwritingPage() {
  const [selectedIndex, setSelectedIndex] = useState<number | null>(null);
  const [lastScore, setLastScore] = useState<number | null>(null);
  const [showTemplate, setShowTemplate] = useState(true);

  const template = selectedIndex !== null ? LETTER_TEMPLATES[selectedIndex] : null;

  const scoreColor = (s: number) =>
    s >= 70 ? "text-green-600 dark:text-green-400" :
    s >= 40 ? "text-yellow-600 dark:text-yellow-400" :
    "text-red-600 dark:text-red-400";

  const scoreBg = (s: number) =>
    s >= 70 ? "bg-green-50 dark:bg-green-950/30" :
    s >= 40 ? "bg-yellow-50 dark:bg-yellow-950/30" :
    "bg-red-50 dark:bg-red-950/30";

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Письмо</h1>
      <p className="text-muted-foreground">Выберите букву и нарисуйте её на холсте</p>

      {/* Letter grid */}
      <div className="grid grid-cols-9 gap-1.5">
        {LETTER_TEMPLATES.map((t, i) => (
          <Button
            key={t.letter}
            variant={selectedIndex === i ? "default" : "outline"}
            className="h-12 w-full text-xl font-hebrew p-0"
            onClick={() => { setSelectedIndex(i); setLastScore(null); }}
          >
            {t.letter}
          </Button>
        ))}
      </div>

      {template && (
        <Card>
          <CardContent className="pt-6 space-y-4">
            <div className="text-center space-y-1">
              <HebrewText size="2xl" className="font-bold">{template.letter}</HebrewText>
              <p className="text-sm text-muted-foreground">{template.name_ru} ({template.name})</p>
            </div>

            <div className="flex items-center justify-center gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowTemplate(!showTemplate)}
              >
                {showTemplate ? "Скрыть шаблон" : "Показать шаблон"}
              </Button>
            </div>

            <HandwritingCanvas
              key={template.letter}
              template={template}
              showTemplate={showTemplate}
              onScore={(s) => setLastScore(s)}
            />

            {lastScore !== null && (
              <div className={cn("p-4 rounded-lg text-center", scoreBg(lastScore))}>
                <p className={cn("text-3xl font-bold", scoreColor(lastScore))}>{lastScore}%</p>
                <p className="text-sm text-muted-foreground mt-1">
                  {lastScore >= 70 ? "Отлично!" : lastScore >= 40 ? "Неплохо, попробуйте ещё" : "Попробуйте ещё раз"}
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
