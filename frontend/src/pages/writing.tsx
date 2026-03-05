import { useState, useCallback } from "react";
import { useLessons, useLesson, useCheckExercise, type Exercise, type ExerciseCheckResponse } from "@/hooks/use-lessons";
import { HebrewText } from "@/components/hebrew-text";
import { TTSControls } from "@/components/tts-controls";
import { HebrewKeyboard } from "@/components/hebrew-keyboard";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

// ── Hebrew typing exercise ────────────────────────────────────────────────

function HebrewTypingExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const [value, setValue] = useState("");
  const prompt = exercise.prompt_json as {
    prompt: string;
    target_he: string;
    transliteration: string;
  };

  const targetChars = new Set(prompt.target_he.split(""));

  return (
    <div className="space-y-4">
      <p className="font-medium">{prompt.prompt}</p>
      <p className="text-sm text-muted-foreground">
        Транслитерация: <span className="font-medium">{prompt.transliteration}</span>
      </p>

      <div className="flex gap-2">
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          dir="rtl"
          className="font-hebrew text-xl"
          placeholder="..."
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
        highlightKeys={[...targetChars]}
      />
    </div>
  );
}

// ── Translation RU→HE exercise ────────────────────────────────────────────

function TranslateExercise({ exercise, onAnswer }: {
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

      <HebrewKeyboard
        onKey={(key) => setValue((v) => v + key)}
        onBackspace={() => setValue((v) => v.slice(0, -1))}
        onSpace={() => setValue((v) => v + " ")}
      />
    </div>
  );
}

// ── Free writing ──────────────────────────────────────────────────────────

function FreeWritingExercise() {
  const [text, setText] = useState("");
  const wordCount = text.trim().split(/\s+/).filter(Boolean).length;

  return (
    <div className="space-y-4">
      <p className="font-medium">Напишите что-нибудь на иврите</p>
      <p className="text-sm text-muted-foreground">
        Попробуйте рассказать о себе, описать свой день или написать несколько предложений
      </p>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        dir="rtl"
        className="w-full h-32 font-hebrew text-lg p-3 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary"
        placeholder="...כתוב כאן"
      />

      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <span>{wordCount} слов</span>
        <span>{text.length} символов</span>
      </div>

      <HebrewKeyboard
        onKey={(key) => setText((v) => v + key)}
        onBackspace={() => setText((v) => v.slice(0, -1))}
        onSpace={() => setText((v) => v + " ")}
      />
    </div>
  );
}

// ── Exercise wrapper ──────────────────────────────────────────────────────

function WritingExerciseCard({ exercise, onDone }: {
  exercise: Exercise;
  onDone: () => void;
}) {
  const checkExercise = useCheckExercise();
  const [result, setResult] = useState<ExerciseCheckResponse | null>(null);

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
            <div className="text-sm mt-1 space-y-1">
              <span>Правильный ответ:{" "}</span>
              <HebrewText size="lg" className="font-bold">
                {String(result.correct_answer)}
              </HebrewText>
              {/[\u0590-\u05FF]/.test(String(result.correct_answer)) && (
                <TTSControls text={String(result.correct_answer)} size="sm" />
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
    case "hebrew_typing":
      return <HebrewTypingExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "translate_ru_he":
      return <TranslateExercise exercise={exercise} onAnswer={handleAnswer} />;
    default:
      return <p className="text-muted-foreground">Тип: {exercise.type}</p>;
  }
}

// ── Main page ──────────────────────────────────────────────────────────────

export function WritingPage() {
  const { data: lessons, isLoading } = useLessons(undefined, "writing");
  const [selectedLessonId, setSelectedLessonId] = useState<number | null>(null);
  const { data: lessonDetail } = useLesson(selectedLessonId);
  const [currentExIdx, setCurrentExIdx] = useState(0);
  const [lessonDone, setLessonDone] = useState(false);
  const [freeWriteMode, setFreeWriteMode] = useState(false);

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
    setFreeWriteMode(false);
  };

  const handleBack = () => {
    setSelectedLessonId(null);
    setCurrentExIdx(0);
    setLessonDone(false);
    setFreeWriteMode(false);
  };

  // ── Free writing mode ──
  if (freeWriteMode) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={() => setFreeWriteMode(false)}>
            ← Назад
          </Button>
          <h1 className="text-xl font-bold">Свободное письмо</h1>
        </div>
        <Card>
          <CardContent className="pt-6">
            <FreeWritingExercise />
          </CardContent>
        </Card>
      </div>
    );
  }

  // ── Exercise view ──
  if (selectedLessonId && lessonDetail) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" onClick={handleBack}>← Назад</Button>
          <h1 className="text-xl font-bold">{lessonDetail.title_ru}</h1>
        </div>

        {lessonDetail.exercises.length === 0 ? (
          // Free writing lesson (no exercises)
          <Card>
            <CardContent className="pt-6">
              <FreeWritingExercise />
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
                <WritingExerciseCard
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
      <h1 className="text-2xl font-bold">Письмо</h1>
      <p className="text-muted-foreground">
        Учитесь писать на иврите: набор букв, перевод слов и предложений
      </p>

      {/* Free writing button */}
      <Card
        className="cursor-pointer hover:bg-accent/50 transition-colors border-dashed"
        onClick={() => setFreeWriteMode(true)}
      >
        <CardHeader className="py-3">
          <div className="flex items-center gap-3">
            <Badge variant="outline">Свободный</Badge>
            <CardTitle className="text-base">Свободное письмо</CardTitle>
          </div>
          <CardDescription className="ml-[85px]">
            Пишите что угодно на иврите с экранной клавиатурой
          </CardDescription>
        </CardHeader>
      </Card>

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
    case "hebrew_typing": return "Набор текста";
    case "translate_ru_he": return "Перевод RU→HE";
    case "multiple_choice": return "Выбор ответа";
    case "fill_blank": return "Заполните пропуск";
    case "match_pairs": return "Соединить пары";
    case "word_order": return "Порядок слов";
    case "dictation": return "Диктант";
    case "minimal_pairs": return "Минимальные пары";
    case "listening_comprehension": return "Аудирование";
    default: return type;
  }
}
