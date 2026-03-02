import { useState, useCallback, useRef } from "react";
import { useSRSSession, useSRSStats, useReviewCard, useSRSLeeches, type SRSCard } from "@/hooks/use-srs";
import { useSoundEffects } from "@/hooks/use-sound-effects";
import { HebrewText } from "@/components/hebrew-text";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

const QUALITY_LABELS = [
  { value: 0, label: "Забыл", color: "bg-red-500 hover:bg-red-600", key: "1" },
  { value: 1, label: "Трудно", color: "bg-orange-500 hover:bg-orange-600", key: "2" },
  { value: 2, label: "Нормально", color: "bg-yellow-500 hover:bg-yellow-600", key: "3" },
  { value: 3, label: "Легко", color: "bg-green-500 hover:bg-green-600", key: "4" },
];

export function SRSPage() {
  const { data: session, isLoading, refetch } = useSRSSession(20);
  const { data: stats } = useSRSStats();
  const { data: leeches } = useSRSLeeches();
  const reviewCard = useReviewCard();
  const { play } = useSoundEffects();

  const [currentIndex, setCurrentIndex] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [sessionDone, setSessionDone] = useState(false);
  const [reviewed, setReviewed] = useState(0);
  const startTimeRef = useRef<number>(Date.now());

  const currentCard = session?.cards[currentIndex];

  const handleReveal = useCallback(() => {
    setRevealed(true);
  }, []);

  const handleRate = useCallback(
    async (quality: number) => {
      if (!currentCard) return;

      const responseTime = Date.now() - startTimeRef.current;

      await reviewCard.mutateAsync({
        card_id: currentCard.id,
        quality,
        response_time_ms: responseTime,
      });

      // Play sound effect based on quality
      if (quality >= 2) {
        play("correct");
      } else {
        play("wrong");
      }

      setReviewed((r) => r + 1);
      setRevealed(false);
      startTimeRef.current = Date.now();

      if (session && currentIndex + 1 < session.cards.length) {
        setCurrentIndex((i) => i + 1);
      } else {
        setSessionDone(true);
      }
    },
    [currentCard, currentIndex, session, reviewCard]
  );

  const handleRestart = useCallback(() => {
    setCurrentIndex(0);
    setRevealed(false);
    setSessionDone(false);
    setReviewed(0);
    startTimeRef.current = Date.now();
    refetch();
  }, [refetch]);

  // Keyboard shortcuts
  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent) => {
      if (!revealed && (e.key === "Enter" || e.key === " ")) {
        e.preventDefault();
        handleReveal();
      } else if (revealed) {
        const idx = ["1", "2", "3", "4"].indexOf(e.key);
        if (idx >= 0) {
          e.preventDefault();
          handleRate(idx);
        }
      }
    },
    [revealed, handleReveal, handleRate]
  );

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-12">Загрузка карточек...</p>;
  }

  return (
    <div className="space-y-6" tabIndex={0} onKeyDown={handleKeyDown}>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">SRS-карточки</h1>
        {stats && (
          <div className="flex gap-3 text-sm">
            <Badge variant="secondary">Всего: {stats.total_cards}</Badge>
            <Badge variant={stats.due_today > 0 ? "default" : "secondary"}>
              К повторению: {stats.due_today}
            </Badge>
            <Badge variant="outline">Сегодня: {stats.reviews_today + reviewed}</Badge>
          </div>
        )}
      </div>

      {/* Leech warning */}
      {leeches && leeches.count > 0 && (
        <Card className="border-orange-300 bg-orange-50 dark:bg-orange-950/20 dark:border-orange-800">
          <CardContent className="py-3">
            <div className="flex items-center gap-2">
              <span className="text-lg">⚠️</span>
              <div>
                <p className="font-medium text-sm">
                  Проблемные карточки: {leeches.count}
                </p>
                <p className="text-xs text-muted-foreground">
                  Карточки с частыми ошибками. Попробуйте другой подход к запоминанию.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* No cards state */}
      {(!session || session.cards.length === 0) && !sessionDone && (
        <Card>
          <CardContent className="p-12 text-center space-y-4">
            <p className="text-lg text-muted-foreground">
              Нет карточек для повторения
            </p>
            <p className="text-sm text-muted-foreground">
              Добавьте слова из словаря в карточки
            </p>
          </CardContent>
        </Card>
      )}

      {/* Session complete */}
      {sessionDone && (
        <Card>
          <CardContent className="p-12 text-center space-y-4">
            <p className="text-3xl font-bold">Готово!</p>
            <p className="text-muted-foreground">
              Вы повторили {reviewed} карточек
            </p>
            <Button onClick={handleRestart}>Повторить ещё</Button>
          </CardContent>
        </Card>
      )}

      {/* Active card */}
      {currentCard && !sessionDone && (
        <>
          {/* Progress */}
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span>
              {currentIndex + 1} / {session!.cards.length}
            </span>
            <div className="flex-1 h-1.5 bg-secondary rounded-full overflow-hidden">
              <div
                className="h-full bg-primary rounded-full transition-all"
                style={{
                  width: `${((currentIndex + 1) / session!.cards.length) * 100}%`,
                }}
              />
            </div>
          </div>

          {/* Card */}
          <Card className="min-h-[300px]">
            <CardHeader className="text-center">
              <Badge variant="outline" className="self-center">
                {currentCard.card_type === "word_he_ru"
                  ? "Иврит → Русский"
                  : currentCard.card_type === "word_ru_he"
                  ? "Русский → Иврит"
                  : currentCard.card_type}
              </Badge>
            </CardHeader>
            <CardContent className="text-center space-y-6 pb-8">
              {/* Front */}
              <div className="space-y-2">
                {currentCard.front_json.hebrew && (
                  <HebrewText size="2xl" className="block font-bold text-3xl">
                    {currentCard.front_json.hebrew}
                  </HebrewText>
                )}
                {currentCard.front_json.transliteration && (
                  <p className="text-muted-foreground">
                    {currentCard.front_json.transliteration}
                  </p>
                )}
                {currentCard.front_json.translation && (
                  <p className="text-xl">{currentCard.front_json.translation}</p>
                )}
                {currentCard.front_json.pos && (
                  <Badge variant="secondary">{currentCard.front_json.pos}</Badge>
                )}
              </div>

              {/* Reveal button / Back */}
              {!revealed ? (
                <Button
                  size="lg"
                  variant="outline"
                  onClick={handleReveal}
                  className="mt-8"
                >
                  Показать ответ (Enter)
                </Button>
              ) : (
                <div className="space-y-4 pt-4 border-t">
                  {currentCard.back_json.hebrew && (
                    <HebrewText size="xl" className="block font-bold text-2xl">
                      {currentCard.back_json.hebrew}
                    </HebrewText>
                  )}
                  {currentCard.back_json.transliteration && (
                    <p className="text-muted-foreground">
                      {currentCard.back_json.transliteration}
                    </p>
                  )}
                  {currentCard.back_json.translation && (
                    <p className="text-lg">{currentCard.back_json.translation}</p>
                  )}
                  {currentCard.back_json.root && (
                    <p className="text-sm text-muted-foreground">
                      Корень: <HebrewText size="sm">{currentCard.back_json.root}</HebrewText>
                    </p>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Rating buttons */}
          {revealed && (
            <div className="grid grid-cols-4 gap-2">
              {QUALITY_LABELS.map((q) => (
                <Button
                  key={q.value}
                  className={cn("text-white", q.color)}
                  onClick={() => handleRate(q.value)}
                  disabled={reviewCard.isPending}
                >
                  <span className="text-xs opacity-70 mr-1">{q.key}</span>
                  {q.label}
                </Button>
              ))}
            </div>
          )}

          <p className="text-xs text-center text-muted-foreground">
            Нажмите Enter для показа ответа, 1-4 для оценки
          </p>
        </>
      )}
    </div>
  );
}
