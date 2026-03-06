import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { usePlacementTest, useSubmitPlacement, type PlacementQuestion, type PlacementResult } from "@/hooks/use-placement";
import { HebrewText } from "@/components/hebrew-text";
import { HebrewKeyboard } from "@/components/hebrew-keyboard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const LEVEL_LABELS: Record<number, string> = {
  1: "Алеф (A1)", 2: "Бет (A2)", 3: "Гимель (B1)", 4: "Далет (B2)",
  5: "Хей (C1)", 6: "Вав (C2)", 7: "Продвинутый",
};

type Phase = "intro" | "testing" | "result";

export function PlacementPage() {
  const navigate = useNavigate();
  const { data: testData, refetch, isLoading } = usePlacementTest();
  const submitMutation = useSubmitPlacement();

  const [phase, setPhase] = useState<Phase>("intro");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [typedAnswer, setTypedAnswer] = useState("");
  const [result, setResult] = useState<PlacementResult | null>(null);

  const questions = testData?.questions ?? [];
  const currentQ = questions[currentIndex];

  const handleStart = async () => {
    await refetch();
    setPhase("testing");
    setCurrentIndex(0);
    setAnswers({});
  };

  const handleAnswer = useCallback((answer: string) => {
    if (!currentQ) return;
    const newAnswers = { ...answers, [currentQ.index]: answer };
    setAnswers(newAnswers);
    setTypedAnswer("");

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(i => i + 1);
    } else {
      // Submit
      const answerList = Object.entries(newAnswers).map(([idx, ans]) => ({
        index: Number(idx),
        answer: ans,
      }));
      submitMutation.mutate({ answers: answerList }, {
        onSuccess: (res) => {
          setResult(res);
          setPhase("result");
        },
      });
    }
  }, [currentQ, currentIndex, questions.length, answers, submitMutation]);

  const handleSubmitTyped = () => {
    if (typedAnswer.trim()) {
      handleAnswer(typedAnswer.trim());
    }
  };

  // ── Intro ──
  if (phase === "intro") {
    return (
      <div className="max-w-lg mx-auto space-y-6 py-12">
        <div className="text-center space-y-3">
          <h1 className="text-3xl font-bold">Тест на определение уровня</h1>
          <p className="text-muted-foreground">
            28 вопросов по 4 на каждый уровень (1-7). Тест определит ваш стартовый уровень.
          </p>
        </div>
        <Card>
          <CardContent className="p-6 space-y-4">
            <ul className="text-sm space-y-2 text-muted-foreground">
              <li>- Выбор перевода (иврит → русский)</li>
              <li>- Написание слова на иврите</li>
              <li>- Перевод с русского на иврит</li>
            </ul>
            <Button className="w-full" size="lg" onClick={handleStart} disabled={isLoading}>
              {isLoading ? "Загрузка..." : "Начать тест"}
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // ── Result ──
  if (phase === "result" && result) {
    return (
      <div className="max-w-lg mx-auto space-y-6 py-12">
        <div className="text-center space-y-3">
          <h1 className="text-3xl font-bold">Результат</h1>
          <p className="text-5xl font-bold text-primary">
            {LEVEL_LABELS[result.assigned_level] || `Уровень ${result.assigned_level}`}
          </p>
          <p className="text-muted-foreground">
            {result.total_correct} из {result.total_questions} правильных
          </p>
        </div>

        {/* Per-level accuracy bars */}
        <Card>
          <CardHeader>
            <CardTitle className="text-base">Результаты по уровням</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {Object.entries(result.per_level)
              .sort(([a], [b]) => Number(a) - Number(b))
              .map(([lvl, stats]) => {
                const pct = stats.total > 0 ? Math.round((stats.correct / stats.total) * 100) : 0;
                const passed = pct >= 70;
                return (
                  <div key={lvl} className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span className={cn(passed ? "font-medium" : "text-muted-foreground")}>
                        Уровень {lvl}
                      </span>
                      <span className={cn(passed ? "text-green-600" : "text-muted-foreground")}>
                        {stats.correct}/{stats.total} ({pct}%)
                      </span>
                    </div>
                    <div className="h-2 rounded-full bg-muted">
                      <div
                        className={cn(
                          "h-2 rounded-full transition-all",
                          passed ? "bg-green-500" : "bg-orange-400"
                        )}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                );
              })}
          </CardContent>
        </Card>

        <div className="flex gap-2">
          <Button className="flex-1" onClick={() => navigate("/dashboard")}>
            Перейти к обучению
          </Button>
          <Button variant="outline" onClick={() => { setPhase("intro"); setResult(null); }}>
            Пройти заново
          </Button>
        </div>
      </div>
    );
  }

  // ── Testing ──
  if (!currentQ) {
    return <p className="text-center py-12 text-muted-foreground">Загрузка вопросов...</p>;
  }

  return (
    <div className="max-w-lg mx-auto space-y-6">
      {/* Progress */}
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <span>{currentIndex + 1} / {questions.length}</span>
        <div className="flex-1 h-1.5 bg-secondary rounded-full overflow-hidden">
          <div
            className="h-full bg-primary rounded-full transition-all"
            style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
          />
        </div>
        <Badge variant="outline">Ур. {currentQ.level}</Badge>
      </div>

      <Card>
        <CardHeader className="text-center space-y-2">
          <Badge variant="secondary" className="self-center">
            {currentQ.type === "multiple_choice"
              ? "Выберите перевод"
              : currentQ.type === "fill_blank"
              ? "Напишите на иврите"
              : "Переведите на иврит"}
          </Badge>
        </CardHeader>
        <CardContent className="text-center space-y-6">
          {/* Prompt */}
          {currentQ.prompt_he && (
            <HebrewText size="2xl" className="block font-bold text-3xl">
              {currentQ.prompt_he}
            </HebrewText>
          )}
          {currentQ.prompt_ru && (
            <p className="text-xl font-medium">{currentQ.prompt_ru}</p>
          )}
          {currentQ.hint && (
            <p className="text-sm text-muted-foreground">{currentQ.hint}</p>
          )}

          {/* Multiple choice options */}
          {currentQ.options && (
            <div className="grid grid-cols-2 gap-2 max-w-md mx-auto">
              {currentQ.options.map((opt, i) => (
                <Button
                  key={i}
                  variant="outline"
                  className="h-auto py-3"
                  onClick={() => handleAnswer(opt)}
                >
                  {currentQ.type === "translate_ru_he" ? (
                    <HebrewText size="lg">{opt}</HebrewText>
                  ) : (
                    <span>{opt}</span>
                  )}
                </Button>
              ))}
            </div>
          )}

          {/* Fill blank (typing) */}
          {currentQ.type === "fill_blank" && !currentQ.options && (
            <div className="max-w-md mx-auto space-y-3">
              <div
                dir="rtl"
                className="min-h-[48px] border rounded-md px-3 py-2 font-hebrew text-xl text-right bg-background"
              >
                {typedAnswer || <span className="text-muted-foreground">הקלד כאן...</span>}
              </div>
              <HebrewKeyboard
                onKey={(k) => setTypedAnswer(v => v + k)}
                onBackspace={() => setTypedAnswer(v => v.slice(0, -1))}
                onSpace={() => setTypedAnswer(v => v + " ")}
              />
              <Button
                className="w-full"
                disabled={!typedAnswer.trim()}
                onClick={handleSubmitTyped}
              >
                Ответить
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
