import { useState, useCallback } from "react";
import { useMinimalPairsDrill, useCheckMinimalPair } from "@/hooks/use-minimal-pairs";
import { useTTS } from "@/components/tts-controls";
import { HebrewText } from "@/components/hebrew-text";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export function MinimalPairsPage() {
  const { data, isLoading, refetch } = useMinimalPairsDrill(10);
  const checkMutation = useCheckMinimalPair();
  const { speak } = useTTS();

  const [currentIndex, setCurrentIndex] = useState(0);
  const [score, setScore] = useState({ correct: 0, total: 0 });
  const [answered, setAnswered] = useState(false);
  const [lastCorrect, setLastCorrect] = useState<boolean | null>(null);
  const [done, setDone] = useState(false);

  const questions = data?.questions ?? [];
  const currentQ = questions[currentIndex];

  const handleAnswer = useCallback(async (letter: string) => {
    if (!currentQ || answered) return;

    const result = await checkMutation.mutateAsync({
      pair_id: currentQ.pair_id,
      answer_letter: letter,
      correct_letter: currentQ.correct_letter,
    });

    setAnswered(true);
    setLastCorrect(result.correct);
    setScore(s => ({
      correct: s.correct + (result.correct ? 1 : 0),
      total: s.total + 1,
    }));
  }, [currentQ, answered, checkMutation]);

  const handleNext = () => {
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(i => i + 1);
      setAnswered(false);
      setLastCorrect(null);
    } else {
      setDone(true);
    }
  };

  const handleRestart = () => {
    setCurrentIndex(0);
    setScore({ correct: 0, total: 0 });
    setAnswered(false);
    setLastCorrect(null);
    setDone(false);
    refetch();
  };

  if (isLoading) return <p className="text-center py-12 text-muted-foreground">Загрузка...</p>;

  if (done) {
    return (
      <div className="max-w-lg mx-auto space-y-6">
        <h1 className="text-2xl font-bold text-center">Минимальные пары</h1>
        <Card>
          <CardContent className="p-12 text-center space-y-4">
            <p className="text-3xl font-bold">Готово!</p>
            <p className="text-lg">
              {score.correct} из {score.total}
              {score.total > 0 && (
                <span className="text-muted-foreground ml-2">
                  ({Math.round((score.correct / score.total) * 100)}%)
                </span>
              )}
            </p>
            <Button onClick={handleRestart}>Заново</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!currentQ) return <p className="text-center py-12 text-muted-foreground">Нет данных</p>;

  return (
    <div className="max-w-lg mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Минимальные пары</h1>
        <Badge variant="secondary">{score.correct}/{score.total}</Badge>
      </div>

      {/* Progress */}
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <span>{currentIndex + 1} / {questions.length}</span>
        <div className="flex-1 h-1.5 bg-secondary rounded-full overflow-hidden">
          <div className="h-full bg-primary rounded-full transition-all" style={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }} />
        </div>
      </div>

      <Card>
        <CardHeader className="text-center">
          <p className="text-sm text-muted-foreground">Прослушайте слово и выберите букву</p>
        </CardHeader>
        <CardContent className="text-center space-y-6">
          <Button size="lg" variant="outline" onClick={() => speak(currentQ.target_word)} className="h-20 w-20 rounded-full text-3xl">
            ▶
          </Button>

          <div className="grid grid-cols-2 gap-4">
            {[currentQ.option1, currentQ.option2].map((opt) => {
              let btnClass = "";
              if (answered) {
                if (opt.letter === currentQ.correct_letter) {
                  btnClass = "bg-green-500 hover:bg-green-600 text-white border-green-500";
                } else if (opt.letter !== currentQ.correct_letter && lastCorrect === false) {
                  btnClass = "bg-red-500 hover:bg-red-600 text-white border-red-500";
                }
              }
              return (
                <Button
                  key={opt.letter}
                  variant="outline"
                  className={cn("h-auto py-6 flex-col gap-2", btnClass)}
                  disabled={answered}
                  onClick={() => handleAnswer(opt.letter)}
                >
                  <HebrewText size="2xl" className="font-bold text-3xl">{opt.letter}</HebrewText>
                  <span className="text-xs text-muted-foreground">
                    <HebrewText size="sm">{opt.word}</HebrewText> — {opt.translation}
                  </span>
                </Button>
              );
            })}
          </div>

          {answered && (
            <div className={cn(
              "p-4 rounded-lg",
              lastCorrect ? "bg-green-50 dark:bg-green-950/30" : "bg-red-50 dark:bg-red-950/30"
            )}>
              <p className="font-medium">{lastCorrect ? "Правильно!" : "Неправильно"}</p>
              <p className="text-sm text-muted-foreground mt-1">
                Слово: <HebrewText size="sm" className="font-bold">{currentQ.target_word}</HebrewText> — {currentQ.target_translation}
              </p>
            </div>
          )}

          {answered && <Button onClick={handleNext}>{currentIndex + 1 < questions.length ? "Далее" : "Завершить"}</Button>}
        </CardContent>
      </Card>
    </div>
  );
}
