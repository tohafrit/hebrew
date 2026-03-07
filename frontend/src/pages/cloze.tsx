import { useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useClozeExercises } from "@/hooks/use-cloze";
import { useReadingTexts } from "@/hooks/use-lessons";
import { HebrewText } from "@/components/hebrew-text";
import { HebrewKeyboard } from "@/components/hebrew-keyboard";
import { TTSControls } from "@/components/tts-controls";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export function ClozePage() {
  const { textId: textIdParam } = useParams<{ textId: string }>();
  const navigate = useNavigate();
  const { data: texts } = useReadingTexts();
  const selectedTextId = textIdParam ? Number(textIdParam) : null;
  const { data: clozeData, isLoading } = useClozeExercises(selectedTextId);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [checked, setChecked] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [score, setScore] = useState({ correct: 0, total: 0 });
  const [done, setDone] = useState(false);

  const exercises = clozeData?.exercises ?? [];
  const currentEx = exercises[currentIndex];

  const normalizeAnswer = (t: string) =>
    t.replace(/[\u0591-\u05C7]/g, "")  // strip nikkud
      .replace("\u05BE", "-")
      .normalize("NFC")
      .trim()
      .toLowerCase()
      .replace(/\s+/g, " ")            // collapse whitespace
      .replace(/^[.,!?;: ]+|[.,!?;: ]+$/g, "");  // strip edge punctuation

  const handleCheck = useCallback(() => {
    if (!currentEx) return;
    const correct = normalizeAnswer(answer) === normalizeAnswer(currentEx.answer);
    setChecked(true);
    setIsCorrect(correct);
    setScore(s => ({
      correct: s.correct + (correct ? 1 : 0),
      total: s.total + 1,
    }));
  }, [currentEx, answer]);

  const handleNext = () => {
    if (currentIndex + 1 < exercises.length) {
      setCurrentIndex(i => i + 1);
      setAnswer("");
      setChecked(false);
      setIsCorrect(false);
    } else {
      setDone(true);
    }
  };

  // Text selector
  if (!selectedTextId) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Заполни пропуск</h1>
        <p className="text-muted-foreground">Выберите текст для упражнений:</p>
        <div className="grid gap-3 sm:grid-cols-2">
          {texts?.map(t => (
            <Card key={t.id} className="cursor-pointer hover:bg-accent/50" onClick={() => navigate(`/cloze/${t.id}`)}>
              <CardContent className="py-4">
                <p className="font-medium">{t.title_ru}</p>
                <HebrewText size="sm" className="text-muted-foreground">{t.title_he}</HebrewText>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (isLoading) return <p className="text-center py-12 text-muted-foreground">Загрузка...</p>;

  if (done) {
    return (
      <div className="max-w-lg mx-auto space-y-6">
        <Card>
          <CardContent className="p-12 text-center space-y-4">
            <p className="text-3xl font-bold">Готово!</p>
            <p className="text-lg">
              {score.correct} из {score.total}
              {score.total > 0 && <span className="text-muted-foreground ml-2">({Math.round((score.correct / score.total) * 100)}%)</span>}
            </p>
            <div className="flex gap-2 justify-center">
              <Button onClick={() => { setCurrentIndex(0); setScore({ correct: 0, total: 0 }); setDone(false); setAnswer(""); setChecked(false); }}>
                Заново
              </Button>
              <Button variant="outline" onClick={() => navigate("/cloze")}>Другой текст</Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!currentEx) return <p className="text-center py-12 text-muted-foreground">Нет упражнений для этого текста</p>;

  return (
    <div className="max-w-lg mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Заполни пропуск</h1>
        <Badge variant="secondary">{score.correct}/{score.total}</Badge>
      </div>

      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <span>{currentIndex + 1} / {exercises.length}</span>
        <div className="flex-1 h-1.5 bg-secondary rounded-full overflow-hidden">
          <div className="h-full bg-primary rounded-full transition-all" style={{ width: `${((currentIndex + 1) / exercises.length) * 100}%` }} />
        </div>
      </div>

      <Card>
        <CardContent className="space-y-4 pt-6">
          {/* Blanked sentence */}
          <div dir="rtl" className="text-xl leading-relaxed font-hebrew text-center">
            {currentEx.sentence_he_blanked}
          </div>

          {/* Russian translation */}
          <p className="text-center text-muted-foreground">{currentEx.sentence_ru}</p>

          {/* Hint */}
          <div className="text-center">
            <Badge variant="outline">Подсказка: {currentEx.hint}</Badge>
          </div>

          <TTSControls text={currentEx.sentence_he} size="sm" />

          {/* Input */}
          <div className="space-y-3">
            <input
              dir="rtl"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="הקלד כאן..."
              className="w-full h-12 border rounded-md px-3 font-hebrew text-xl text-right bg-background"
            />

            {!checked && (
              <>
                <HebrewKeyboard
                  onKey={(k) => setAnswer(v => v + k)}
                  onBackspace={() => setAnswer(v => v.slice(0, -1))}
                  onSpace={() => setAnswer(v => v + " ")}
                />
                <Button className="w-full" disabled={!answer.trim()} onClick={handleCheck}>
                  Проверить
                </Button>
              </>
            )}

            {checked && (
              <div className={cn(
                "p-4 rounded-lg text-center",
                isCorrect ? "bg-green-50 dark:bg-green-950/30" : "bg-red-50 dark:bg-red-950/30"
              )}>
                <p className="font-medium">{isCorrect ? "Правильно!" : "Неправильно"}</p>
                <HebrewText size="xl" className="font-bold block mt-1">{currentEx.answer}</HebrewText>
                {currentEx.transliteration && (
                  <p className="text-sm text-muted-foreground">{currentEx.transliteration}</p>
                )}
              </div>
            )}

            {checked && <Button className="w-full" onClick={handleNext}>
              {currentIndex + 1 < exercises.length ? "Далее" : "Завершить"}
            </Button>}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
