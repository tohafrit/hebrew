import { useState } from "react";
import { Link } from "react-router-dom";
import { useLearningPath, useCompleteStep, useRecommendedStep, type PathStep } from "@/hooks/use-path";
import { HebrewText } from "@/components/hebrew-text";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { LEVEL_LABELS } from "@/lib/constants";

const STEP_TYPE_ICONS: Record<string, string> = {
  vocabulary: "A",
  grammar: "G",
  exercise: "E",
  reading: "R",
  dialogue: "D",
  srs_review: "S",
};

const STEP_TYPE_LABELS: Record<string, string> = {
  vocabulary: "Словарь",
  grammar: "Грамматика",
  exercise: "Упражнения",
  reading: "Чтение",
  dialogue: "Диалог",
  srs_review: "Повторение",
};

const STEP_TYPE_COLORS: Record<string, string> = {
  vocabulary: "bg-blue-500",
  grammar: "bg-purple-500",
  exercise: "bg-orange-500",
  reading: "bg-green-500",
  dialogue: "bg-pink-500",
  srs_review: "bg-yellow-500",
};

function getStepRoute(step: PathStep): string {
  const id = step.content_id;
  switch (step.step_type) {
    case "vocabulary":
      return id ? `/lessons/${id}` : "/dictionary";
    case "grammar":
      return id ? `/grammar?topic=${id}` : "/grammar";
    case "exercise":
      return id ? `/lessons/${id}` : "/lessons";
    case "reading":
      return id ? `/reading/${id}` : "/reading";
    case "dialogue":
      return id ? `/dialogues/${id}` : "/dialogues";
    case "srs_review":
      return "/srs";
    default:
      return "/";
  }
}

function StepNode({
  step,
  isNext,
  isLocked,
  onComplete,
  isPending,
}: {
  step: PathStep;
  isNext: boolean;
  isLocked: boolean;
  onComplete: () => void;
  isPending: boolean;
}) {
  const color = STEP_TYPE_COLORS[step.step_type] || "bg-gray-500";
  const route = getStepRoute(step);

  return (
    <div
      className={cn(
        "relative flex items-center gap-4 p-4 rounded-xl border-2 transition-all",
        step.completed && "border-green-300 bg-green-50/50 dark:bg-green-950/20",
        isNext && !step.completed && "border-primary bg-primary/5 ring-2 ring-primary/20",
        isLocked && "opacity-50 border-muted",
        !step.completed && !isNext && !isLocked && "border-border hover:border-primary/30"
      )}
    >
      {/* Step icon */}
      <div
        className={cn(
          "w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg shrink-0",
          step.completed ? "bg-green-500" : isLocked ? "bg-muted-foreground/30" : color
        )}
      >
        {step.completed ? "\u2713" : STEP_TYPE_ICONS[step.step_type] || "?"}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="text-xs shrink-0">
            {STEP_TYPE_LABELS[step.step_type] || step.step_type}
          </Badge>
          {isNext && !step.completed && (
            <Badge variant="default" className="text-xs">Следующий</Badge>
          )}
        </div>
        <p className="font-medium mt-1">{step.title_ru}</p>
        {step.title_he && (
          <HebrewText size="sm" className="text-muted-foreground">
            {step.title_he}
          </HebrewText>
        )}
        {step.description_ru && (
          <p className="text-sm text-muted-foreground mt-0.5">{step.description_ru}</p>
        )}
      </div>

      {/* Action */}
      <div className="shrink-0 flex flex-col gap-1">
        {!isLocked && !step.completed && (
          <>
            <Button size="sm" asChild>
              <Link to={route}>Начать</Link>
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={onComplete}
              disabled={isPending}
            >
              Готово
            </Button>
          </>
        )}
        {step.completed && (
          <Button size="sm" variant="ghost" asChild>
            <Link to={route}>Повторить</Link>
          </Button>
        )}
      </div>
    </div>
  );
}

function UnitGroup({
  unit,
  steps,
  nextStepId,
  onComplete,
  isPending,
  levelId,
}: {
  unit: number;
  steps: PathStep[];
  nextStepId: number | null;
  onComplete: (id: number) => void;
  isPending: boolean;
  levelId: number;
}) {
  const allCompleted = steps.every((s) => s.completed);
  const someCompleted = steps.some((s) => s.completed);

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <div
          className={cn(
            "w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold",
            allCompleted
              ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
              : someCompleted
              ? "bg-primary/10 text-primary"
              : "bg-muted text-muted-foreground"
          )}
        >
          {unit}
        </div>
        <h3 className="font-semibold">
          {LEVEL_LABELS[levelId]} · Блок {unit}
        </h3>
        {allCompleted && (
          <Badge variant="secondary" className="text-green-700">Пройден</Badge>
        )}
      </div>

      <div className="space-y-2 ml-4 border-l-2 border-muted pl-6">
        {steps.map((step, i) => {
          // A step is locked if the previous step in this unit isn't completed
          const prevStep = i > 0 ? steps[i - 1] : null;
          const isLocked = prevStep ? !prevStep.completed && step.id !== nextStepId : false;

          return (
            <StepNode
              key={step.id}
              step={step}
              isNext={step.id === nextStepId}
              isLocked={isLocked}
              onComplete={() => onComplete(step.id)}
              isPending={isPending}
            />
          );
        })}
      </div>
    </div>
  );
}

export function PathPage() {
  const [levelFilter, setLevelFilter] = useState<number | null>(null);
  const { data, isLoading } = useLearningPath(levelFilter ?? undefined);
  const completeStep = useCompleteStep();
  const { data: recommended } = useRecommendedStep();

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-12">Загрузка пути...</p>;
  }

  if (!data || data.steps.length === 0) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Путь обучения</h1>
        <Card>
          <CardContent className="p-12 text-center text-muted-foreground">
            Путь обучения пока не настроен
          </CardContent>
        </Card>
      </div>
    );
  }

  // Group steps by level and unit
  const levels = new Map<number, Map<number, PathStep[]>>();
  for (const step of data.steps) {
    if (!levels.has(step.level_id)) levels.set(step.level_id, new Map());
    const units = levels.get(step.level_id)!;
    if (!units.has(step.unit)) units.set(step.unit, []);
    units.get(step.unit)!.push(step);
  }

  // Progress stats
  const totalSteps = data.steps.length;
  const completedSteps = data.steps.filter((s) => s.completed).length;
  const progressPct = totalSteps > 0 ? Math.round((completedSteps / totalSteps) * 100) : 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Путь обучения</h1>
        <div className="text-sm text-muted-foreground">
          {completedSteps} / {totalSteps} шагов ({progressPct}%)
        </div>
      </div>

      {/* Recommended step banner */}
      {recommended?.step && (
        <Card className="border-primary/50 bg-primary/5">
          <CardContent className="py-3">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium">Рекомендованный урок</p>
                <p className="text-xs text-muted-foreground">{recommended.step.label}</p>
              </div>
              <Button size="sm" asChild>
                <Link to={getStepRoute({
                  step_type: recommended.step.step_type,
                  content_id: recommended.step.content_id,
                } as PathStep)}>
                  Начать
                </Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Progress bar */}
      <div className="h-2 bg-secondary rounded-full overflow-hidden">
        <div
          className="h-full bg-green-500 rounded-full transition-all"
          style={{ width: `${progressPct}%` }}
        />
      </div>

      {/* Level filter */}
      <div className="flex gap-1 flex-wrap">
        <Button
          variant={levelFilter === null ? "default" : "ghost"}
          size="sm"
          onClick={() => setLevelFilter(null)}
        >
          Все уровни
        </Button>
        {[1, 2, 3, 4, 5, 6].map((lvl) => (
          <Button
            key={lvl}
            variant={levelFilter === lvl ? "default" : "ghost"}
            size="sm"
            onClick={() => setLevelFilter(lvl)}
          >
            {LEVEL_LABELS[lvl]}
          </Button>
        ))}
      </div>

      {/* Path tree */}
      <div className="space-y-8">
        {[...levels.entries()].map(([levelId, units]) => (
          <div key={levelId} className="space-y-6">
            {levelFilter === null && (
              <div className="flex items-center gap-3 pt-4 border-t">
                <h2 className="text-xl font-bold">
                  {LEVEL_LABELS[levelId]}
                </h2>
                <Badge variant="secondary">
                  {[...units.values()].flat().filter((s) => s.completed).length} /{" "}
                  {[...units.values()].flat().length}
                </Badge>
              </div>
            )}

            {[...units.entries()].map(([unit, steps]) => (
              <UnitGroup
                key={`${levelId}-${unit}`}
                unit={unit}
                steps={steps}
                nextStepId={data.next_step_id}
                onComplete={(id) => completeStep.mutate(id)}
                isPending={completeStep.isPending}
                levelId={levelId}
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
