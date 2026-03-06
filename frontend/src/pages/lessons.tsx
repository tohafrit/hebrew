import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useLessons, useLesson, useLessonStats } from "@/hooks/use-lessons";
import { useAutoCompleteStep } from "@/hooks/use-path";
import { HebrewText } from "@/components/hebrew-text";
import { MarkdownContent } from "@/components/markdown-content";
import { ExerciseCard, exercise_type_label } from "@/components/exercise-card";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const TYPE_LABELS: Record<string, string> = {
  alphabet: "Алфавит",
  grammar: "Грамматика",
  reading: "Чтение",
};

const TYPE_COLORS: Record<string, string> = {
  alphabet: "bg-blue-100 text-blue-800",
  grammar: "bg-purple-100 text-purple-800",
  reading: "bg-green-100 text-green-800",
};

// ── Main page ──────────────────────────────────────────────────────────────

type Phase = "content" | "exercises" | "done";

export function LessonsPage() {
  const { lessonId: lessonIdParam } = useParams<{ lessonId: string }>();
  const navigate = useNavigate();
  const { data: lessons, isLoading } = useLessons();
  const selectedLessonId = lessonIdParam ? Number(lessonIdParam) : null;
  const { data: lessonDetail } = useLesson(selectedLessonId);
  const [currentExIdx, setCurrentExIdx] = useState(0);
  const [typeFilter, setTypeFilter] = useState<string | null>(null);
  const [phase, setPhase] = useState<Phase>("content");

  // Reset exercise state when navigating to a different lesson via URL
  useEffect(() => {
    setCurrentExIdx(0);
    setPhase("content");
  }, [lessonIdParam]);

  // Auto-complete learning path step when lesson is done
  useAutoCompleteStep("exercise", selectedLessonId, phase === "done");
  useAutoCompleteStep("vocabulary", selectedLessonId, phase === "done");

  // Fetch stats when lesson is done
  const { data: lessonStats } = useLessonStats(phase === "done" ? selectedLessonId : null);

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-12">Загрузка...</p>;
  }

  const filteredLessons = typeFilter
    ? lessons?.filter((l) => l.type === typeFilter)
    : lessons;

  const currentExercise = lessonDetail?.exercises[currentExIdx];

  const handleNext = () => {
    if (lessonDetail && currentExIdx + 1 < lessonDetail.exercises.length) {
      setCurrentExIdx((i) => i + 1);
    } else {
      setPhase("done");
    }
  };

  const handleSelectLesson = (id: number) => {
    navigate(`/lessons/${id}`);
    setCurrentExIdx(0);
    setPhase("content");
  };

  const handleBackToList = () => {
    navigate("/lessons");
    setCurrentExIdx(0);
    setPhase("content");
  };

  const handleStartExercises = () => {
    setCurrentExIdx(0);
    setPhase("exercises");
  };

  // ── Lesson view ──
  if (selectedLessonId && lessonDetail) {
    const hasContent = !!lessonDetail.content_md;
    const hasExercises = lessonDetail.exercises.length > 0;

    // Auto-skip content phase if no content_md
    const effectivePhase = phase === "content" && !hasContent
      ? (hasExercises ? "exercises" : "done")
      : phase;

    return (
      <div className="space-y-6">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={effectivePhase === "exercises" && hasContent ? () => setPhase("content") : handleBackToList}>
            ← {effectivePhase === "exercises" && hasContent ? "К материалу" : "Назад"}
          </Button>
          <div>
            <h1 className="text-xl font-bold">{lessonDetail.title_ru}</h1>
            {lessonDetail.title_he && (
              <HebrewText size="sm" className="text-muted-foreground">
                {lessonDetail.title_he}
              </HebrewText>
            )}
          </div>
          <Badge variant="secondary" className={TYPE_COLORS[lessonDetail.type]}>
            {TYPE_LABELS[lessonDetail.type] || lessonDetail.type}
          </Badge>
        </div>

        {/* Content phase — read the lesson material */}
        {effectivePhase === "content" && hasContent && (
          <>
            <Card>
              <CardContent className="py-6">
                <MarkdownContent content={lessonDetail.content_md!} />
              </CardContent>
            </Card>
            <div className="flex gap-3 justify-center">
              <Button variant="outline" onClick={handleBackToList}>
                К урокам
              </Button>
              {hasExercises && (
                <Button onClick={handleStartExercises}>
                  Начать упражнения ({lessonDetail.exercises.length})
                </Button>
              )}
            </div>
          </>
        )}

        {/* Done phase */}
        {effectivePhase === "done" && (
          <Card>
            <CardContent className="p-12 text-center space-y-4">
              <p className="text-3xl font-bold">Урок завершён!</p>
              {lessonStats && lessonStats.total > 0 ? (
                <div className="space-y-3">
                  <div className="flex justify-center gap-6 text-sm">
                    <span>
                      Правильно: <strong>{lessonStats.correct}/{lessonStats.total}</strong>
                    </span>
                    {lessonStats.time_ms > 0 && (
                      <span className="text-muted-foreground">
                        Время: {Math.round(lessonStats.time_ms / 1000)}с
                      </span>
                    )}
                  </div>
                  <div className="w-48 mx-auto h-3 bg-secondary rounded-full overflow-hidden">
                    <div
                      className={cn(
                        "h-full rounded-full transition-all",
                        lessonStats.accuracy_pct >= 80 ? "bg-green-500" :
                        lessonStats.accuracy_pct >= 50 ? "bg-yellow-500" : "bg-red-500"
                      )}
                      style={{ width: `${lessonStats.accuracy_pct}%` }}
                    />
                  </div>
                  <p className={cn(
                    "text-lg font-bold",
                    lessonStats.accuracy_pct >= 80 ? "text-green-600" :
                    lessonStats.accuracy_pct >= 50 ? "text-yellow-600" : "text-red-600"
                  )}>
                    {lessonStats.accuracy_pct}%
                  </p>
                </div>
              ) : (
                <p className="text-muted-foreground">
                  Вы выполнили {lessonDetail.exercises.length} упражнений
                </p>
              )}
              <div className="flex gap-2 justify-center flex-wrap">
                {hasContent && (
                  <Button variant="outline" onClick={() => setPhase("content")}>
                    Перечитать материал
                  </Button>
                )}
                <Button variant="outline" onClick={handleBackToList}>
                  К урокам
                </Button>
                {hasExercises && (
                  <Button onClick={() => { setCurrentExIdx(0); setPhase("exercises"); }}>
                    Повторить
                  </Button>
                )}
              </div>
              <div className="flex gap-2 justify-center pt-2">
                <Button variant="ghost" size="sm" asChild>
                  <Link to="/reading">Чтение</Link>
                </Button>
                <Button variant="ghost" size="sm" asChild>
                  <Link to="/dialogues">Диалоги</Link>
                </Button>
                <Button variant="ghost" size="sm" asChild>
                  <Link to="/dictionary">Словарь</Link>
                </Button>
                <Button variant="ghost" size="sm" asChild>
                  <Link to="/srs">SRS-карточки</Link>
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Exercise phase */}
        {effectivePhase === "exercises" && hasExercises && (
          <>
            {/* Progress */}
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span>{currentExIdx + 1} / {lessonDetail.exercises.length}</span>
              <div className="flex-1 h-1.5 bg-secondary rounded-full overflow-hidden">
                <div
                  className="h-full bg-primary rounded-full transition-all"
                  style={{
                    width: `${((currentExIdx + 1) / lessonDetail.exercises.length) * 100}%`,
                  }}
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

        {/* No exercises and no content */}
        {!hasContent && !hasExercises && effectivePhase !== "done" && (
          <Card>
            <CardContent className="p-12 text-center text-muted-foreground">
              Нет материалов в этом уроке
            </CardContent>
          </Card>
        )}
      </div>
    );
  }

  // ── Lesson list view ──
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Уроки</h1>
        <div className="flex gap-1">
          <Button
            variant={typeFilter === null ? "default" : "ghost"}
            size="sm"
            onClick={() => setTypeFilter(null)}
          >
            Все ({lessons?.length ?? 0})
          </Button>
          {["alphabet", "grammar", "reading"].map((t) => {
            const count = lessons?.filter((l) => l.type === t).length ?? 0;
            return (
              <Button
                key={t}
                variant={typeFilter === t ? "default" : "ghost"}
                size="sm"
                onClick={() => setTypeFilter(t)}
              >
                {TYPE_LABELS[t]} ({count})
              </Button>
            );
          })}
        </div>
      </div>

      <div className="space-y-2">
        {filteredLessons?.map((lesson) => (
          <Card
            key={lesson.id}
            className="cursor-pointer hover:bg-accent/50 transition-colors"
            onClick={() => handleSelectLesson(lesson.id)}
          >
            <CardHeader className="py-3">
              <div className="flex items-center gap-3">
                <Badge variant="secondary" className={cn("text-xs", TYPE_COLORS[lesson.type])}>
                  {TYPE_LABELS[lesson.type] || lesson.type}
                </Badge>
                <CardTitle className="text-base flex-1">
                  {lesson.title_ru}
                </CardTitle>
                {lesson.title_he && (
                  <HebrewText size="sm" className="text-muted-foreground">
                    {lesson.title_he}
                  </HebrewText>
                )}
              </div>
              {lesson.description && (
                <CardDescription className="ml-[70px]">
                  {lesson.description}
                </CardDescription>
              )}
            </CardHeader>
          </Card>
        ))}
      </div>
    </div>
  );
}

