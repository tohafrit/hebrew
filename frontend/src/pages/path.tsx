import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useLearningPath, useCompleteStep, useRecommendedStep, type PathStep } from "@/hooks/use-path";
import { useLesson, useReadingText } from "@/hooks/use-lessons";
import { HebrewText } from "@/components/hebrew-text";
import { MarkdownContent } from "@/components/markdown-content";
import { ExerciseCard, exercise_type_label } from "@/components/exercise-card";
import { TTSControls } from "@/components/tts-controls";
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

// ── Inline step content views ──────────────────────────────────────────────

type StepPhase = "content" | "exercises" | "done";

function InlineLessonStep({
  contentId,
  onComplete,
}: {
  contentId: number;
  onComplete: () => void;
}) {
  const { data: lesson, isLoading } = useLesson(contentId);
  const [phase, setPhase] = useState<StepPhase>("content");
  const [currentExIdx, setCurrentExIdx] = useState(0);

  // Reset when contentId changes
  useEffect(() => {
    setPhase("content");
    setCurrentExIdx(0);
  }, [contentId]);

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-8">Загрузка урока...</p>;
  }

  if (!lesson) {
    return <p className="text-center text-muted-foreground py-8">Урок не найден</p>;
  }

  const hasContent = !!lesson.content_md;
  const hasExercises = lesson.exercises.length > 0;
  const effectivePhase = phase === "content" && !hasContent
    ? (hasExercises ? "exercises" : "done")
    : phase;

  const currentExercise = lesson.exercises[currentExIdx];

  const handleNext = () => {
    if (currentExIdx + 1 < lesson.exercises.length) {
      setCurrentExIdx((i) => i + 1);
    } else {
      setPhase("done");
    }
  };

  if (effectivePhase === "done") {
    onComplete();
    return (
      <Card>
        <CardContent className="p-8 text-center space-y-4">
          <p className="text-2xl font-bold">Шаг завершён!</p>
          <p className="text-muted-foreground">
            Вы выполнили {lesson.exercises.length} упражнений
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold">{lesson.title_ru}</h2>

      {/* Content phase */}
      {effectivePhase === "content" && hasContent && (
        <>
          <Card>
            <CardContent className="py-6">
              <MarkdownContent content={lesson.content_md!} />
            </CardContent>
          </Card>
          {hasExercises && (
            <Button onClick={() => { setCurrentExIdx(0); setPhase("exercises"); }} className="w-full">
              Начать упражнения ({lesson.exercises.length})
            </Button>
          )}
          {!hasExercises && (
            <Button onClick={onComplete} className="w-full">
              Далее
            </Button>
          )}
        </>
      )}

      {/* Exercise phase */}
      {effectivePhase === "exercises" && hasExercises && (
        <>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>{currentExIdx + 1} / {lesson.exercises.length}</span>
            <div className="flex-1 h-1.5 bg-secondary rounded-full overflow-hidden">
              <div
                className="h-full bg-primary rounded-full transition-all"
                style={{ width: `${((currentExIdx + 1) / lesson.exercises.length) * 100}%` }}
              />
            </div>
          </div>

          <Card>
            <CardHeader>
              <Badge variant="outline" className="self-start">
                {exercise_type_label(currentExercise!.type)}
              </Badge>
            </CardHeader>
            <CardContent>
              <ExerciseCard
                key={`${currentExercise!.id}-${currentExIdx}`}
                exercise={currentExercise!}
                onDone={handleNext}
              />
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}

function InlineReadingStep({
  contentId,
  onComplete,
}: {
  contentId: number;
  onComplete: () => void;
}) {
  const { data: text, isLoading } = useReadingText(contentId);

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-8">Загрузка текста...</p>;
  }

  if (!text) {
    return <p className="text-center text-muted-foreground py-8">Текст не найден</p>;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-bold">{text.title_ru}</h2>
        {text.title_he && (
          <HebrewText size="lg" className="font-bold">{text.title_he}</HebrewText>
        )}
      </div>

      <Card>
        <CardContent className="py-6 space-y-4">
          {/* Hebrew text */}
          <div dir="rtl" className="font-hebrew text-xl leading-relaxed space-y-2">
            {text.content_he.split("\n").map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
          <TTSControls text={text.content_he} size="lg" label="Прослушать" />

          {/* Translation */}
          <hr className="my-4" />
          <div className="text-base text-muted-foreground leading-relaxed space-y-2">
            {text.content_ru.split("\n").map((line, i) => (
              <p key={i}>{line}</p>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Vocabulary */}
      {text.vocabulary_json && text.vocabulary_json.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Словарь</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-2">
              {text.vocabulary_json.map((w, i) => (
                <div key={i} className="flex items-center justify-between p-2 rounded border">
                  <div className="flex items-center gap-3">
                    <HebrewText size="lg" className="font-bold">{w.he}</HebrewText>
                    {w.translit && (
                      <span className="text-xs text-muted-foreground">{w.translit}</span>
                    )}
                    <TTSControls text={w.he} size="sm" />
                  </div>
                  <span className="text-sm">{w.ru}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <Button onClick={onComplete} className="w-full">
        Далее
      </Button>
    </div>
  );
}

// ── Focused step view (stepper mode) ───────────────────────────────────────

function StepperView({
  steps,
  activeStepId,
  onExit,
  onAdvance,
}: {
  steps: PathStep[];
  activeStepId: number;
  onExit: () => void;
  onAdvance: () => void;
}) {
  const completeStep = useCompleteStep();
  const activeStep = steps.find((s) => s.id === activeStepId);
  const activeIndex = steps.findIndex((s) => s.id === activeStepId);
  const totalSteps = steps.length;

  if (!activeStep) {
    return (
      <div className="space-y-4">
        <p className="text-center text-muted-foreground py-8">Шаг не найден</p>
        <Button variant="outline" onClick={onExit}>Назад к пути</Button>
      </div>
    );
  }

  const handleComplete = () => {
    if (!activeStep.completed) {
      completeStep.mutate(activeStep.id);
    }
    onAdvance();
  };

  // For grammar, dialogue, srs_review — link out
  const isExternalStep =
    activeStep.step_type === "grammar" ||
    activeStep.step_type === "dialogue" ||
    activeStep.step_type === "srs_review";

  const isLessonStep =
    activeStep.step_type === "vocabulary" || activeStep.step_type === "exercise";

  const isReadingStep = activeStep.step_type === "reading";

  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <Button variant="ghost" size="sm" onClick={onExit}>
          ← Назад к пути
        </Button>
        <Badge variant="outline">
          {STEP_TYPE_LABELS[activeStep.step_type] || activeStep.step_type}
        </Badge>
      </div>

      {/* Progress bar */}
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <span>Шаг {activeIndex + 1} / {totalSteps}</span>
        <div className="flex-1 h-2 bg-secondary rounded-full overflow-hidden">
          <div
            className="h-full bg-green-500 rounded-full transition-all"
            style={{ width: `${((activeIndex + 1) / totalSteps) * 100}%` }}
          />
        </div>
      </div>

      {/* Step title */}
      <div>
        <h1 className="text-xl font-bold">{activeStep.title_ru}</h1>
        {activeStep.title_he && (
          <HebrewText size="sm" className="text-muted-foreground">
            {activeStep.title_he}
          </HebrewText>
        )}
        {activeStep.description_ru && (
          <p className="text-sm text-muted-foreground mt-1">{activeStep.description_ru}</p>
        )}
      </div>

      {/* Inline content */}
      {isLessonStep && activeStep.content_id && (
        <InlineLessonStep
          key={activeStep.id}
          contentId={activeStep.content_id}
          onComplete={handleComplete}
        />
      )}

      {isReadingStep && activeStep.content_id && (
        <InlineReadingStep
          key={activeStep.id}
          contentId={activeStep.content_id}
          onComplete={handleComplete}
        />
      )}

      {isExternalStep && (
        <Card>
          <CardContent className="p-8 text-center space-y-4">
            <p className="text-muted-foreground">
              {activeStep.step_type === "grammar" && "Этот шаг откроется на странице грамматики"}
              {activeStep.step_type === "dialogue" && "Этот шаг откроется на странице диалогов"}
              {activeStep.step_type === "srs_review" && "Перейдите к повторению карточек"}
            </p>
            <div className="flex gap-3 justify-center">
              <Button asChild>
                <Link to={getStepRoute(activeStep)}>Перейти</Link>
              </Button>
              <Button variant="outline" onClick={handleComplete}>
                Отметить выполненным
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* No content_id fallback */}
      {!isExternalStep && !activeStep.content_id && (
        <Card>
          <CardContent className="p-8 text-center space-y-4">
            <p className="text-muted-foreground">Нет контента для этого шага</p>
            <Button variant="outline" onClick={handleComplete}>
              Отметить выполненным
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

// ── Step node (path tree view) ─────────────────────────────────────────────

function StepNode({
  step,
  isNext,
  isLocked,
  onComplete,
  isPending,
  onStart,
}: {
  step: PathStep;
  isNext: boolean;
  isLocked: boolean;
  onComplete: () => void;
  isPending: boolean;
  onStart: () => void;
}) {
  const color = STEP_TYPE_COLORS[step.step_type] || "bg-gray-500";

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
            <Button size="sm" onClick={onStart}>
              Начать
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
          <Button size="sm" variant="ghost" onClick={onStart}>
            Повторить
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
  onStartStep,
}: {
  unit: number;
  steps: PathStep[];
  nextStepId: number | null;
  onComplete: (id: number) => void;
  isPending: boolean;
  levelId: number;
  onStartStep: (stepId: number) => void;
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
              onStart={() => onStartStep(step.id)}
            />
          );
        })}
      </div>
    </div>
  );
}

// ── Main page ──────────────────────────────────────────────────────────────

export function PathPage() {
  const [levelFilter, setLevelFilter] = useState<number | null>(null);
  const [activeStepId, setActiveStepId] = useState<number | null>(null);
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

  // ── Stepper mode ──
  if (activeStepId !== null) {
    const handleAdvance = () => {
      const currentIdx = data.steps.findIndex((s) => s.id === activeStepId);
      if (currentIdx >= 0 && currentIdx + 1 < data.steps.length) {
        setActiveStepId(data.steps[currentIdx + 1].id);
      } else {
        // Last step — exit stepper
        setActiveStepId(null);
      }
    };

    return (
      <StepperView
        steps={data.steps}
        activeStepId={activeStepId}
        onExit={() => setActiveStepId(null)}
        onAdvance={handleAdvance}
      />
    );
  }

  // ── Path tree mode ──

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
              <Button
                size="sm"
                onClick={() => setActiveStepId(recommended.step!.id)}
              >
                Начать
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
                onStartStep={(stepId) => setActiveStepId(stepId)}
              />
            ))}
          </div>
        ))}
      </div>
    </div>
  );
}
