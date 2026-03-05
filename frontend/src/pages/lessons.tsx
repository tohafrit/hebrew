import { useState, useCallback, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useLessons, useLesson, useCheckExercise, type Exercise, type ExerciseCheckResponse } from "@/hooks/use-lessons";
import { useAutoCompleteStep } from "@/hooks/use-path";
import { useSoundEffects } from "@/hooks/use-sound-effects";
import { HebrewText } from "@/components/hebrew-text";
import { MarkdownContent } from "@/components/markdown-content";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { TTSControls } from "@/components/tts-controls";
import { HebrewKeyboard } from "@/components/hebrew-keyboard";
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

// ── Exercise components ────────────────────────────────────────────────────

function MultipleChoiceExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const prompt = exercise.prompt_json as { question: string; options: string[] };
  return (
    <div className="space-y-3">
      <p className="font-medium">{prompt.question}</p>
      <div className="grid gap-2">
        {prompt.options.map((opt, i) => (
          <Button
            key={i}
            variant="outline"
            className="justify-start h-auto py-3 px-4 text-left"
            onClick={() => onAnswer(opt)}
          >
            <span className="text-xs text-muted-foreground mr-2 w-5">{i + 1}.</span>
            <span>{opt}</span>
          </Button>
        ))}
      </div>
    </div>
  );
}

function FillBlankExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const [value, setValue] = useState("");
  const prompt = exercise.prompt_json as { sentence_ru: string; context?: string; hint?: string };

  return (
    <div className="space-y-3">
      <p className="font-medium">{prompt.context || "Заполните пропуск"}</p>
      <p className="text-lg">{prompt.sentence_ru}</p>
      {prompt.hint && (
        <p className="text-sm text-muted-foreground">Подсказка: {prompt.hint}</p>
      )}
      <div className="flex gap-2">
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Ваш ответ..."
          onKeyDown={(e) => {
            if (e.key === "Enter" && value.trim()) onAnswer(value.trim());
          }}
        />
        <Button onClick={() => value.trim() && onAnswer(value.trim())}>OK</Button>
      </div>
    </div>
  );
}

function MatchPairsExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const prompt = exercise.prompt_json as { pairs_left: string[]; pairs_right: string[] };
  const [matches, setMatches] = useState<Record<string, string>>({});
  const [selectedLeft, setSelectedLeft] = useState<string | null>(null);

  const usedRight = new Set(Object.values(matches));

  const handleRightClick = (right: string) => {
    if (!selectedLeft) return;
    const updated = { ...matches, [selectedLeft]: right };
    setMatches(updated);
    setSelectedLeft(null);

    if (Object.keys(updated).length === prompt.pairs_left.length) {
      onAnswer(updated);
    }
  };

  return (
    <div className="space-y-3">
      <p className="font-medium">Соедините пары</p>
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          {prompt.pairs_left.map((left) => (
            <Button
              key={left}
              variant={selectedLeft === left ? "default" : matches[left] ? "secondary" : "outline"}
              className="w-full justify-start h-auto py-2"
              onClick={() => {
                if (matches[left]) {
                  const updated = { ...matches };
                  delete updated[left];
                  setMatches(updated);
                }
                setSelectedLeft(left);
              }}
            >
              {left}
              {matches[left] && (
                <span className="ml-auto text-xs text-muted-foreground">
                  → {matches[left]}
                </span>
              )}
            </Button>
          ))}
        </div>
        <div className="space-y-2">
          {prompt.pairs_right.map((right) => (
            <Button
              key={right}
              variant={usedRight.has(right) ? "secondary" : "outline"}
              className="w-full justify-start h-auto py-2"
              disabled={usedRight.has(right)}
              onClick={() => handleRightClick(right)}
            >
              {right}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
}

function WordOrderExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const prompt = exercise.prompt_json as {
    words_shuffled: string[];
    translation: string;
  };
  const [selected, setSelected] = useState<{ word: string; origIdx: number }[]>([]);
  const usedIndices = new Set(selected.map((s) => s.origIdx));
  const remaining = prompt.words_shuffled
    .map((w, i) => ({ word: w, origIdx: i }))
    .filter((item) => !usedIndices.has(item.origIdx));

  return (
    <div className="space-y-3">
      <p className="font-medium">Составьте предложение</p>
      <p className="text-sm text-muted-foreground">{prompt.translation}</p>

      <div className="min-h-[48px] border rounded-lg p-3 flex flex-wrap gap-2" dir="rtl">
        {selected.map((item, i) => (
          <Badge
            key={`${item.origIdx}-${i}`}
            variant="default"
            className="cursor-pointer text-sm"
            onClick={() => setSelected(selected.filter((_, j) => j !== i))}
          >
            {item.word}
          </Badge>
        ))}
      </div>

      <div className="flex flex-wrap gap-2" dir="rtl">
        {remaining.map((item) => (
          <Badge
            key={item.origIdx}
            variant="outline"
            className="cursor-pointer text-sm"
            onClick={() => {
              const updated = [...selected, item];
              setSelected(updated);
              if (updated.length === prompt.words_shuffled.length) {
                onAnswer(updated.map((s) => s.word));
              }
            }}
          >
            {item.word}
          </Badge>
        ))}
      </div>
    </div>
  );
}

function DictationExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const [value, setValue] = useState("");
  const prompt = exercise.prompt_json as {
    word_he: string;
    word_translit?: string;
    hint?: string;
  };

  return (
    <div className="space-y-4">
      <p className="text-muted-foreground text-sm">Прослушайте и запишите на иврите</p>
      {prompt.hint && <p className="text-sm text-muted-foreground">Подсказка: {prompt.hint}</p>}
      <TTSControls text={prompt.word_he} size="lg" label="Прослушать" />
      <div className="space-y-2">
        <div className="flex gap-2">
          <Input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Введите слово на иврите..."
            dir="rtl"
            className="font-hebrew text-lg"
            onKeyDown={(e) => {
              if (e.key === "Enter" && value.trim()) onAnswer(value.trim());
            }}
          />
          <Button
            onClick={() => value.trim() && onAnswer(value.trim())}
            disabled={!value.trim()}
          >
            Проверить
          </Button>
        </div>
        <HebrewKeyboard
          onKey={(key) => setValue((v) => v + key)}
          onBackspace={() => setValue((v) => v.slice(0, -1))}
          onSpace={() => setValue((v) => v + " ")}
        />
      </div>
    </div>
  );
}

function TranslateRuHeExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const [value, setValue] = useState("");
  const prompt = exercise.prompt_json as {
    prompt_ru: string;
    hint?: string;
    target_he: string;
  };

  return (
    <div className="space-y-4">
      <p className="font-medium">Переведите на иврит:</p>
      <p className="text-2xl font-bold">{prompt.prompt_ru}</p>
      {prompt.hint && (
        <p className="text-sm text-muted-foreground">
          Подсказка: <HebrewText size="sm">{prompt.hint}</HebrewText>
          <TTSControls text={prompt.hint} size="sm" className="inline-flex ml-2" />
        </p>
      )}
      <div className="flex gap-2">
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          dir="rtl"
          className="font-hebrew text-xl"
          placeholder="הקלד כאן..."
          onKeyDown={(e) => {
            if (e.key === "Enter" && value.trim()) onAnswer(value.trim());
          }}
        />
        <Button
          onClick={() => value.trim() && onAnswer(value.trim())}
          disabled={!value.trim()}
        >
          Проверить
        </Button>
      </div>
    </div>
  );
}

function ExerciseCard({ exercise, onDone }: {
  exercise: Exercise;
  onDone: () => void;
}) {
  const checkExercise = useCheckExercise();
  const [result, setResult] = useState<ExerciseCheckResponse | null>(null);
  const { play } = useSoundEffects();

  const handleAnswer = useCallback(
    async (answer: any) => {
      try {
        const res = await checkExercise.mutateAsync({
          exercise_id: exercise.id,
          answer,
        });
        setResult(res);
        play(res.correct ? "correct" : "wrong");
      } catch {
        setResult({ correct: false, correct_answer: null, explanation: "Ошибка сети. Попробуйте ещё раз.", points_earned: 0 } as ExerciseCheckResponse);
      }
    },
    [exercise.id, checkExercise, play]
  );

  if (result) {
    return (
      <div className="space-y-3">
        <div
          className={cn(
            "p-4 rounded-lg border",
            result.correct
              ? "bg-green-50 border-green-200"
              : "bg-red-50 border-red-200"
          )}
        >
          <p className="font-bold text-lg">
            {result.correct ? "Правильно!" : "Неправильно"}
            {result.correct && ` +${result.points_earned} XP`}
          </p>
          {!result.correct && result.correct_answer && (
            <div className="text-sm mt-1">
              <span>Правильный ответ:{" "}</span>
              <span className="font-medium">
                {typeof result.correct_answer === "string"
                  ? result.correct_answer
                  : JSON.stringify(result.correct_answer)}
              </span>
              {typeof result.correct_answer === "string" && /[\u0590-\u05FF]/.test(result.correct_answer) && (
                <TTSControls text={result.correct_answer} size="sm" className="inline-flex ml-2" />
              )}
            </div>
          )}
          {result.explanation && (
            <p className="text-sm text-muted-foreground mt-2">{result.explanation}</p>
          )}
        </div>
        <Button onClick={onDone} className="w-full">
          Далее
        </Button>
      </div>
    );
  }

  switch (exercise.type) {
    case "multiple_choice":
      return <MultipleChoiceExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "fill_blank":
      return <FillBlankExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "match_pairs":
      return <MatchPairsExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "word_order":
      return <WordOrderExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "translate_ru_he":
      return <TranslateRuHeExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "dictation":
      return <DictationExercise exercise={exercise} onAnswer={handleAnswer} />;
    default:
      return <p className="text-muted-foreground">Неизвестный тип упражнения: {exercise.type}</p>;
  }
}

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
              <p className="text-muted-foreground">
                Вы выполнили {lessonDetail.exercises.length} упражнений
              </p>
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

function exercise_type_label(type: string): string {
  switch (type) {
    case "multiple_choice": return "Выбор ответа";
    case "fill_blank": return "Заполните пропуск";
    case "match_pairs": return "Соединить пары";
    case "word_order": return "Порядок слов";
    case "translate_ru_he": return "Перевод на иврит";
    case "dictation": return "Диктант";
    case "hebrew_typing": return "Набор текста";
    case "minimal_pairs": return "Минимальные пары";
    case "listening_comprehension": return "Аудирование";
    default: return type;
  }
}
