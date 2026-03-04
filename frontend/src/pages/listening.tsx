import { useState, useCallback } from "react";
import { useLessons, useLesson, useCheckExercise, type Exercise, type ExerciseCheckResponse } from "@/hooks/use-lessons";
import { HebrewText } from "@/components/hebrew-text";
import { TTSControls, useTTS } from "@/components/tts-controls";
import { HebrewKeyboard } from "@/components/hebrew-keyboard";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

// ── Dictation exercise ────────────────────────────────────────────────────

function DictationExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const [value, setValue] = useState("");
  const prompt = exercise.prompt_json as {
    word_he: string;
    word_translit: string;
    hint: string;
  };

  const handleKey = (key: string) => setValue((v) => v + key);
  const handleBackspace = () => setValue((v) => v.slice(0, -1));
  const handleSpace = () => setValue((v) => v + " ");

  return (
    <div className="space-y-4">
      <p className="text-muted-foreground text-sm">Прослушайте и запишите на иврите</p>
      <p className="text-sm text-muted-foreground">Подсказка: {prompt.hint}</p>

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
          onKey={handleKey}
          onBackspace={handleBackspace}
          onSpace={handleSpace}
        />
      </div>
    </div>
  );
}

// ── Minimal pairs exercise ────────────────────────────────────────────────

function MinimalPairsExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const { speak } = useTTS();
  const prompt = exercise.prompt_json as {
    pair_a: { he: string; translit: string; meaning: string };
    pair_b: { he: string; translit: string; meaning: string };
    question: string;
    correct_pair: string;
  };

  const playTarget = useCallback(() => {
    const target = prompt.correct_pair === "a" ? prompt.pair_a.he : prompt.pair_b.he;
    speak(target);
  }, [prompt, speak]);

  return (
    <div className="space-y-4">
      <p className="font-medium">{prompt.question}</p>
      <Button variant="outline" size="lg" onClick={playTarget}>
        ▶ Прослушать слово
      </Button>

      <div className="grid grid-cols-2 gap-3">
        <Button
          variant="outline"
          className="h-auto py-4 flex-col gap-1"
          onClick={() => onAnswer("a")}
        >
          <HebrewText size="xl" className="font-bold">{prompt.pair_a.he}</HebrewText>
          <span className="text-xs text-muted-foreground">{prompt.pair_a.translit}</span>
          <span className="text-xs">{prompt.pair_a.meaning}</span>
        </Button>
        <Button
          variant="outline"
          className="h-auto py-4 flex-col gap-1"
          onClick={() => onAnswer("b")}
        >
          <HebrewText size="xl" className="font-bold">{prompt.pair_b.he}</HebrewText>
          <span className="text-xs text-muted-foreground">{prompt.pair_b.translit}</span>
          <span className="text-xs">{prompt.pair_b.meaning}</span>
        </Button>
      </div>
    </div>
  );
}

// ── Listening comprehension exercise ──────────────────────────────────────

function ListeningComprehensionExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const prompt = exercise.prompt_json as {
    text_he: string;
    text_translit: string;
    questions: Array<{ question: string; options: string[]; correct: string }>;
  };
  const [answers, setAnswers] = useState<string[]>([]);
  const currentQ = prompt.questions[answers.length];

  const handleSelect = (option: string) => {
    const updated = [...answers, option];
    setAnswers(updated);
    if (updated.length === prompt.questions.length) {
      onAnswer(updated);
    }
  };

  return (
    <div className="space-y-4">
      <TTSControls text={prompt.text_he} size="lg" label="Прослушать текст" />

      <div className="text-sm text-muted-foreground">
        Вопрос {answers.length + 1} из {prompt.questions.length}
      </div>

      {currentQ && (
        <div className="space-y-3">
          <p className="font-medium">{currentQ.question}</p>
          <div className="grid gap-2">
            {currentQ.options.map((opt, i) => (
              <Button
                key={i}
                variant="outline"
                className="justify-start h-auto py-3"
                onClick={() => handleSelect(opt)}
              >
                {opt}
              </Button>
            ))}
          </div>
        </div>
      )}

      {answers.length === prompt.questions.length && (
        <p className="text-sm text-muted-foreground">Все вопросы отвечены!</p>
      )}
    </div>
  );
}

// ── Exercise wrapper with result ──────────────────────────────────────────

function ListeningExerciseCard({ exercise, onDone }: {
  exercise: Exercise;
  onDone: () => void;
}) {
  const checkExercise = useCheckExercise();
  const [result, setResult] = useState<ExerciseCheckResponse | null>(null);
  const { speak } = useTTS();

  const handleAnswer = useCallback(
    async (answer: any) => {
      try {
        const res = await checkExercise.mutateAsync({
          exercise_id: exercise.id,
          answer,
        });
        setResult(res);
      } catch {
        setResult({ correct: false, correct_answer: null, explanation: "Ошибка сети. Попробуйте ещё раз.", points_earned: 0 } as ExerciseCheckResponse);
      }
    },
    [exercise.id, checkExercise]
  );

  if (result) {
    return (
      <div className="space-y-3">
        <div className={cn(
          "p-4 rounded-lg border",
          result.correct ? "bg-green-50 border-green-200" : "bg-red-50 border-red-200"
        )}>
          <p className="font-bold text-lg">
            {result.correct ? "Правильно!" : "Неправильно"}
            {result.correct && ` +${result.points_earned} XP`}
          </p>
          {!result.correct && result.correct_answer && (
            <div className="mt-1">
              <p className="text-sm">Правильный ответ:</p>
              {typeof result.correct_answer === "string" ? (
                <div className="flex items-center gap-2 mt-1">
                  <HebrewText size="lg" className="font-bold">{result.correct_answer}</HebrewText>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => speak(result.correct_answer as string)}
                  >
                    ▶
                  </Button>
                </div>
              ) : (
                <p className="text-sm font-medium">{JSON.stringify(result.correct_answer)}</p>
              )}
            </div>
          )}
          {result.explanation && (
            <p className="text-sm text-muted-foreground mt-2">{result.explanation}</p>
          )}
        </div>
        <Button onClick={onDone} className="w-full">Далее</Button>
      </div>
    );
  }

  switch (exercise.type) {
    case "dictation":
      return <DictationExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "minimal_pairs":
      return <MinimalPairsExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "listening_comprehension":
      return <ListeningComprehensionExercise exercise={exercise} onAnswer={handleAnswer} />;
    default:
      return <p className="text-muted-foreground">Тип: {exercise.type}</p>;
  }
}

// ── Main page ──────────────────────────────────────────────────────────────

export function ListeningPage() {
  const { data: lessons, isLoading } = useLessons(undefined, "listening");
  const [selectedLessonId, setSelectedLessonId] = useState<number | null>(null);
  const { data: lessonDetail } = useLesson(selectedLessonId);
  const [currentExIdx, setCurrentExIdx] = useState(0);
  const [lessonDone, setLessonDone] = useState(false);

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-12">Загрузка...</p>;
  }

  const currentExercise = lessonDetail?.exercises[currentExIdx];

  const handleNext = () => {
    if (lessonDetail && currentExIdx + 1 < lessonDetail.exercises.length) {
      setCurrentExIdx((i) => i + 1);
    } else {
      setLessonDone(true);
    }
  };

  const handleSelectLesson = (id: number) => {
    setSelectedLessonId(id);
    setCurrentExIdx(0);
    setLessonDone(false);
  };

  const handleBack = () => {
    setSelectedLessonId(null);
    setCurrentExIdx(0);
    setLessonDone(false);
  };

  // ── Exercise view ──
  if (selectedLessonId && lessonDetail) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={handleBack}>← Назад</Button>
          <h1 className="text-xl font-bold">{lessonDetail.title_ru}</h1>
        </div>

        {lessonDetail.exercises.length === 0 ? (
          <Card>
            <CardContent className="p-12 text-center text-muted-foreground">
              Нет упражнений
            </CardContent>
          </Card>
        ) : lessonDone ? (
          <Card>
            <CardContent className="p-12 text-center space-y-4">
              <p className="text-3xl font-bold">Отлично!</p>
              <p className="text-muted-foreground">
                Вы выполнили {lessonDetail.exercises.length} упражнений
              </p>
              <div className="flex gap-2 justify-center">
                <Button variant="outline" onClick={handleBack}>К урокам</Button>
                <Button onClick={() => { setCurrentExIdx(0); setLessonDone(false); }}>Повторить</Button>
              </div>
            </CardContent>
          </Card>
        ) : (
          <>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <span>{currentExIdx + 1} / {lessonDetail.exercises.length}</span>
              <div className="flex-1 h-1.5 bg-secondary rounded-full overflow-hidden">
                <div
                  className="h-full bg-primary rounded-full transition-all"
                  style={{ width: `${((currentExIdx + 1) / lessonDetail.exercises.length) * 100}%` }}
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
                <ListeningExerciseCard
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

  // ── Lesson list ──
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Аудирование</h1>
      <p className="text-muted-foreground">
        Тренируйте восприятие иврита на слух: диктанты, минимальные пары, понимание текста
      </p>

      <div className="space-y-2">
        {lessons?.map((lesson) => (
          <Card
            key={lesson.id}
            className="cursor-pointer hover:bg-accent/50 transition-colors"
            onClick={() => handleSelectLesson(lesson.id)}
          >
            <CardHeader className="py-3">
              <div className="flex items-center gap-3">
                <Badge variant="secondary">
                  {({1:"Алеф",2:"Бет",3:"Гимель",4:"Далет",5:"Хей",6:"Вав"} as Record<number,string>)[lesson.level_id] ?? `L${lesson.level_id}`}
                </Badge>
                <CardTitle className="text-base flex-1">{lesson.title_ru}</CardTitle>
                {lesson.title_he && (
                  <HebrewText size="sm" className="text-muted-foreground">
                    {lesson.title_he}
                  </HebrewText>
                )}
              </div>
              {lesson.description && (
                <CardDescription className="ml-[60px]">{lesson.description}</CardDescription>
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
    case "dictation": return "Диктант";
    case "minimal_pairs": return "Минимальные пары";
    case "listening_comprehension": return "Аудирование";
    default: return type;
  }
}
