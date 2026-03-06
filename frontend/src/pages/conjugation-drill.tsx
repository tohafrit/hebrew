import { useState, useCallback } from "react";
import { useConjugationDrill, useCheckDrillAnswer, useTableDrill, useCheckTableDrill } from "@/hooks/use-conjugation-drill";
import { ConjugationTable } from "@/components/conjugation-table";
import { useBinyanim } from "@/hooks/use-grammar";
import { HebrewText } from "@/components/hebrew-text";
import { HebrewKeyboard } from "@/components/hebrew-keyboard";
import { useTTS } from "@/components/tts-controls";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const TENSE_LABELS: Record<string, string> = {
  past: "Прошедшее",
  present: "Настоящее",
  future: "Будущее",
  imperative: "Повелительное",
};

const PERSON_LABELS: Record<string, string> = {
  "1s": "я",
  "2ms": "ты (м)",
  "2fs": "ты (ж)",
  "3ms": "он",
  "3fs": "она",
  "1p": "мы",
  "2mp": "вы (м)",
  "2fp": "вы (ж)",
  "3mp": "они (м)",
  "3fp": "они (ж)",
  ms: "м.р. ед.ч.",
  fs: "ж.р. ед.ч.",
  mp: "м.р. мн.ч.",
  fp: "ж.р. мн.ч.",
};

const LEVEL_LABELS: Record<number, string> = {
  1: "Алеф",
  2: "Бет",
  3: "Гимель",
  4: "Далет",
  5: "Хей",
  6: "Вав",
};

type DrillMode = "choice" | "typing" | "table";

export function ConjugationDrillPage() {
  const { data: binyanim } = useBinyanim();
  const checkAnswer = useCheckDrillAnswer();
  const { speak } = useTTS();

  // Filters
  const [levelFilter, setLevelFilter] = useState<number | undefined>();
  const [binyanFilter, setBinyanFilter] = useState<number | undefined>();
  const [tenseFilter, setTenseFilter] = useState<string | undefined>();
  const [mode, setMode] = useState<DrillMode>("choice");

  const { data: questions, isLoading, refetch } = useConjugationDrill({
    level_id: levelFilter,
    binyan_id: binyanFilter,
    tense: tenseFilter,
    count: 10,
  });

  // Drill state
  const [currentIndex, setCurrentIndex] = useState(0);
  const [score, setScore] = useState({ correct: 0, total: 0 });
  const [answered, setAnswered] = useState(false);
  const [lastResult, setLastResult] = useState<{ correct: boolean; correctAnswer: string; correctNikkud: string | null } | null>(null);
  const [typedAnswer, setTypedAnswer] = useState("");
  const [done, setDone] = useState(false);

  const currentQ = questions?.[currentIndex];

  const handleAnswer = useCallback(
    async (answer: string) => {
      if (!currentQ || answered) return;

      const result = await checkAnswer.mutateAsync({
        word_id: currentQ.word_id,
        binyan_id: currentQ.binyan_id,
        tense: currentQ.tense,
        person: currentQ.person,
        answer,
      });

      setAnswered(true);
      setLastResult({
        correct: result.correct,
        correctAnswer: result.correct_answer,
        correctNikkud: result.correct_nikkud,
      });
      setScore((s) => ({
        correct: s.correct + (result.correct ? 1 : 0),
        total: s.total + 1,
      }));
    },
    [currentQ, answered, checkAnswer]
  );

  const handleNext = useCallback(() => {
    if (questions && currentIndex + 1 < questions.length) {
      setCurrentIndex((i) => i + 1);
      setAnswered(false);
      setLastResult(null);
      setTypedAnswer("");
    } else {
      setDone(true);
    }
  }, [currentIndex, questions]);

  const handleRestart = useCallback(() => {
    setCurrentIndex(0);
    setScore({ correct: 0, total: 0 });
    setAnswered(false);
    setLastResult(null);
    setTypedAnswer("");
    setDone(false);
    refetch();
  }, [refetch]);

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-12">Загрузка...</p>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Тренировка спряжений</h1>
        <Badge variant="secondary">
          {score.correct}/{score.total}
        </Badge>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        <select
          className="text-sm border rounded px-2 py-1 bg-background"
          value={levelFilter ?? ""}
          onChange={(e) => {
            setLevelFilter(e.target.value ? Number(e.target.value) : undefined);
            handleRestart();
          }}
        >
          <option value="">Все уровни</option>
          {[1, 2, 3, 4, 5, 6].map((l) => (
            <option key={l} value={l}>{LEVEL_LABELS[l]}</option>
          ))}
        </select>
        <select
          className="text-sm border rounded px-2 py-1 bg-background"
          value={binyanFilter ?? ""}
          onChange={(e) => {
            setBinyanFilter(e.target.value ? Number(e.target.value) : undefined);
            handleRestart();
          }}
        >
          <option value="">Все биньяны</option>
          {binyanim?.map((b) => (
            <option key={b.id} value={b.id}>{b.name_ru}</option>
          ))}
        </select>
        <select
          className="text-sm border rounded px-2 py-1 bg-background"
          value={tenseFilter ?? ""}
          onChange={(e) => {
            setTenseFilter(e.target.value || undefined);
            handleRestart();
          }}
        >
          <option value="">Все времена</option>
          {Object.entries(TENSE_LABELS).map(([k, v]) => (
            <option key={k} value={k}>{v}</option>
          ))}
        </select>
        <div className="flex gap-1">
          <Button
            variant={mode === "choice" ? "default" : "outline"}
            size="sm"
            onClick={() => setMode("choice")}
          >
            Выбор
          </Button>
          <Button
            variant={mode === "typing" ? "default" : "outline"}
            size="sm"
            onClick={() => setMode("typing")}
          >
            Ввод
          </Button>
          <Button
            variant={mode === "table" ? "default" : "outline"}
            size="sm"
            onClick={() => setMode("table")}
          >
            Таблица
          </Button>
        </div>
      </div>

      {/* Table mode */}
      {mode === "table" && <TableDrillSection levelFilter={levelFilter} binyanFilter={binyanFilter} tenseFilter={tenseFilter} />}

      {/* No questions */}
      {mode !== "table" && (!questions || questions.length === 0) && !done && (
        <Card>
          <CardContent className="p-12 text-center text-muted-foreground">
            Нет данных для тренировки. Попробуйте изменить фильтры.
          </CardContent>
        </Card>
      )}

      {/* Done */}
      {mode !== "table" && done && (
        <Card>
          <CardContent className="p-12 text-center space-y-4">
            <p className="text-3xl font-bold">Готово!</p>
            <p className="text-lg">
              Результат: {score.correct} из {score.total}
              {score.total > 0 && (
                <span className="text-muted-foreground ml-2">
                  ({Math.round((score.correct / score.total) * 100)}%)
                </span>
              )}
            </p>
            <Button onClick={handleRestart}>Начать заново</Button>
          </CardContent>
        </Card>
      )}

      {/* Active question */}
      {mode !== "table" && currentQ && !done && (
        <>
          {/* Progress */}
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>{currentIndex + 1} / {questions!.length}</span>
            <div className="flex-1 h-1.5 bg-secondary rounded-full overflow-hidden">
              <div
                className="h-full bg-primary rounded-full transition-all"
                style={{ width: `${((currentIndex + 1) / questions!.length) * 100}%` }}
              />
            </div>
          </div>

          <Card>
            <CardHeader className="text-center space-y-2">
              <div className="flex justify-center gap-2">
                <Badge variant="outline">{currentQ.binyan_name}</Badge>
                <Badge variant="secondary">{TENSE_LABELS[currentQ.tense] || currentQ.tense}</Badge>
              </div>
              <div className="flex items-center justify-center gap-2">
                <HebrewText size="2xl" className="font-bold" nikkud={currentQ.word_nikkud}>
                  {currentQ.word_hebrew}
                </HebrewText>
                <button
                  className="text-muted-foreground hover:text-primary text-sm"
                  onClick={() => speak(currentQ.word_nikkud || currentQ.word_hebrew)}
                >
                  ▶
                </button>
              </div>
              <p className="text-muted-foreground">{currentQ.translation_ru}</p>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <p className="font-medium">
                {PERSON_LABELS[currentQ.person] || currentQ.person},{" "}
                {TENSE_LABELS[currentQ.tense] || currentQ.tense}
              </p>

              {/* Multiple choice */}
              {mode === "choice" && currentQ.options && (
                <div className="grid grid-cols-2 gap-2 max-w-md mx-auto">
                  {currentQ.options.map((opt, i) => {
                    let variant: "outline" | "default" | "destructive" = "outline";
                    if (answered && lastResult) {
                      if (opt === lastResult.correctAnswer) variant = "default";
                      else if (opt === typedAnswer && !lastResult.correct) variant = "destructive";
                    }
                    return (
                      <Button
                        key={i}
                        variant={variant}
                        className={cn(
                          "h-auto py-3",
                          answered && opt === lastResult?.correctAnswer && "bg-green-500 hover:bg-green-600 text-white border-green-500",
                          answered && opt === typedAnswer && !lastResult?.correct && "bg-red-500 hover:bg-red-600 text-white border-red-500",
                        )}
                        disabled={answered}
                        onClick={() => {
                          setTypedAnswer(opt);
                          handleAnswer(opt);
                        }}
                      >
                        <HebrewText size="lg">{opt}</HebrewText>
                      </Button>
                    );
                  })}
                </div>
              )}

              {/* Typing mode */}
              {mode === "typing" && (
                <div className="max-w-md mx-auto space-y-3">
                  <div className="flex gap-2">
                    <input
                      dir="rtl"
                      value={typedAnswer}
                      onChange={(e) => setTypedAnswer(e.target.value)}
                      placeholder="הקלד כאן..."
                      className="flex-1 h-12 border rounded-md px-3 font-hebrew text-xl text-right bg-background"
                    />
                  </div>
                  {!answered && (
                    <>
                      <HebrewKeyboard
                        onKey={(k) => setTypedAnswer((v) => v + k)}
                        onBackspace={() => setTypedAnswer((v) => v.slice(0, -1))}
                        onSpace={() => setTypedAnswer((v) => v + " ")}
                      />
                      <Button
                        className="w-full"
                        disabled={!typedAnswer.trim()}
                        onClick={() => handleAnswer(typedAnswer)}
                      >
                        Проверить
                      </Button>
                    </>
                  )}
                </div>
              )}

              {/* Result feedback */}
              {answered && lastResult && (
                <div className={cn(
                  "p-4 rounded-lg",
                  lastResult.correct
                    ? "bg-green-50 dark:bg-green-950/30 border border-green-200 dark:border-green-800"
                    : "bg-red-50 dark:bg-red-950/30 border border-red-200 dark:border-red-800"
                )}>
                  <p className="font-medium mb-1">
                    {lastResult.correct ? "Правильно!" : "Неправильно"}
                  </p>
                  <div className="flex items-center justify-center gap-2">
                    <HebrewText size="xl" className="font-bold" nikkud={lastResult.correctNikkud}>
                      {lastResult.correctAnswer}
                    </HebrewText>
                    <button
                      className="text-muted-foreground hover:text-primary text-sm"
                      onClick={() => speak(lastResult.correctNikkud || lastResult.correctAnswer)}
                    >
                      ▶
                    </button>
                  </div>
                  {currentQ.transliteration && (
                    <p className="text-sm text-muted-foreground mt-1">{currentQ.transliteration}</p>
                  )}
                </div>
              )}

              {answered && (
                <Button onClick={handleNext} className="mt-4">
                  {currentIndex + 1 < questions!.length ? "Следующий" : "Завершить"}
                </Button>
              )}
            </CardContent>
          </Card>
        </>
      )}
    </div>
  );
}

function TableDrillSection({ levelFilter, binyanFilter, tenseFilter }: {
  levelFilter?: number;
  binyanFilter?: number;
  tenseFilter?: string;
}) {
  const { data: tableDrill, isLoading, refetch } = useTableDrill({
    level_id: levelFilter,
    binyan_id: binyanFilter,
    tense: tenseFilter,
  });
  const checkTableDrill = useCheckTableDrill();
  const [results, setResults] = useState<Record<string, boolean> | undefined>();
  const [tableScore, setTableScore] = useState<{ score: number; total: number } | null>(null);

  if (isLoading) return <p className="text-center py-6 text-muted-foreground">Загрузка...</p>;
  if (!tableDrill) return <p className="text-center py-6 text-muted-foreground">Нет данных для таблицы</p>;

  const handleSubmit = async (answers: Record<string, string>) => {
    // We need word_id and binyan_id from the drill data — for now extract from the query
    // The table drill endpoint should return these; using a simplified check
    const res = await checkTableDrill.mutateAsync({
      word_id: 0, // The backend will use the session data
      binyan_id: 0,
      tense: tableDrill.tense,
      answers,
    });
    const resultMap: Record<string, boolean> = {};
    res.results.forEach(r => { resultMap[r.key] = r.correct; });
    setResults(resultMap);
    setTableScore({ score: res.score, total: res.total });
  };

  const handleNewTable = () => {
    setResults(undefined);
    setTableScore(null);
    refetch();
  };

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader className="text-center space-y-2">
          <div className="flex justify-center gap-2">
            <Badge variant="outline">{tableDrill.binyan_name}</Badge>
            <Badge variant="secondary">{tableDrill.tense}</Badge>
          </div>
          <HebrewText size="2xl" className="font-bold" nikkud={tableDrill.word_nikkud}>
            {tableDrill.word_hebrew}
          </HebrewText>
          <p className="text-muted-foreground">{tableDrill.translation_ru}</p>
        </CardHeader>
        <CardContent>
          <ConjugationTable
            cells={tableDrill.cells}
            onSubmit={handleSubmit}
            results={results}
            disabled={!!results}
          />
          {tableScore && (
            <div className="text-center mt-4 space-y-2">
              <p className="font-medium">{tableScore.score} из {tableScore.total}</p>
              <Button onClick={handleNewTable}>Новая таблица</Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
