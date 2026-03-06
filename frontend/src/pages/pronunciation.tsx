import { useState, useCallback, useRef } from "react";
import { useSRSSession } from "@/hooks/use-srs";
import { HebrewText } from "@/components/hebrew-text";
import { TTSControls, useTTS } from "@/components/tts-controls";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { levenshtein } from "@/lib/levenshtein";

type Score = "great" | "good" | "poor" | null;

function getScore(distance: number, expected: string): Score {
  if (distance === 0) return "great";
  const ratio = distance / expected.length;
  if (ratio <= 0.3) return "good";
  return "poor";
}

const SCORE_CONFIG: Record<string, { label: string; color: string; bg: string }> = {
  great: { label: "Отлично!", color: "text-green-600", bg: "bg-green-100 border-green-200" },
  good: { label: "Хорошо", color: "text-yellow-600", bg: "bg-yellow-100 border-yellow-200" },
  poor: { label: "Попробуйте ещё", color: "text-red-600", bg: "bg-red-100 border-red-200" },
};

// Check if SpeechRecognition is available
const SpeechRecognition =
  typeof window !== "undefined"
    ? (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    : null;

export function PronunciationPage() {
  const { data: session } = useSRSSession(50);
  const { speak } = useTTS();

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [score, setScore] = useState<Score>(null);
  const [distance, setDistance] = useState(0);
  const recognitionRef = useRef<any>(null);

  // Get words from SRS deck (hebrew words only)
  const words = (session?.cards || [])
    .filter((c) => c.front_json.hebrew || c.back_json.hebrew)
    .map((c) => ({
      hebrew: (c.front_json.hebrew || c.back_json.hebrew)!,
      translation: c.front_json.translation || c.back_json.translation || "",
      transliteration: c.front_json.transliteration || c.back_json.transliteration || "",
    }));

  const currentWord = words[currentIndex];

  const handleListen = useCallback(() => {
    if (currentWord) {
      speak(currentWord.hebrew);
    }
  }, [currentWord, speak]);

  const handleSpeak = useCallback(() => {
    if (!SpeechRecognition || !currentWord) return;

    const recognition = new SpeechRecognition();
    recognition.lang = "he-IL";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognitionRef.current = recognition;

    recognition.onstart = () => setIsListening(true);

    recognition.onresult = (event: any) => {
      const result = event.results[0][0].transcript;
      setTranscript(result);

      // Strip nikkud for comparison
      const clean = (s: string) => s.replace(/[\u0591-\u05C7]/g, "").trim();
      const dist = levenshtein(clean(result), clean(currentWord.hebrew));
      setDistance(dist);
      setScore(getScore(dist, currentWord.hebrew));
    };

    recognition.onerror = () => {
      setIsListening(false);
      setTranscript("");
      setScore(null);
    };

    recognition.onend = () => setIsListening(false);

    setTranscript("");
    setScore(null);
    recognition.start();
  }, [currentWord]);

  const handleNext = useCallback(() => {
    setCurrentIndex((i) => (i + 1) % Math.max(1, words.length));
    setTranscript("");
    setScore(null);
    setDistance(0);
  }, [words.length]);

  if (!SpeechRecognition) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-bold">Произношение</h1>
        <Card>
          <CardContent className="p-12 text-center space-y-4">
            <p className="text-lg text-muted-foreground">
              Ваш браузер не поддерживает распознавание речи.
            </p>
            <p className="text-sm text-muted-foreground">
              Попробуйте Chrome или Edge для использования этой функции.
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Произношение</h1>
        {words.length > 0 && (
          <span className="text-sm text-muted-foreground">
            {currentIndex + 1} / {words.length}
          </span>
        )}
      </div>

      {words.length === 0 ? (
        <Card>
          <CardContent className="p-12 text-center space-y-4">
            <p className="text-lg text-muted-foreground">
              Добавьте слова в SRS-карточки, чтобы начать тренировку произношения
            </p>
            <Button asChild variant="outline">
              <a href="/dictionary">Перейти в словарь</a>
            </Button>
          </CardContent>
        </Card>
      ) : currentWord && (
        <>
          <Card className="min-h-[280px]">
            <CardHeader className="text-center">
              <Badge variant="outline" className="self-center">Произношение</Badge>
            </CardHeader>
            <CardContent className="text-center space-y-6 pb-8">
              {/* Word */}
              <div className="space-y-2">
                <HebrewText size="2xl" className="block font-bold text-4xl">
                  {currentWord.hebrew}
                </HebrewText>
                {currentWord.transliteration && (
                  <p className="text-muted-foreground">{currentWord.transliteration}</p>
                )}
                {currentWord.translation && (
                  <p className="text-lg">{currentWord.translation}</p>
                )}
              </div>

              {/* Listen button */}
              <div className="flex justify-center gap-3">
                <Button variant="outline" onClick={handleListen}>
                  Послушать
                </Button>
                <Button
                  onClick={handleSpeak}
                  disabled={isListening}
                  className={cn(
                    isListening && "animate-pulse bg-red-500 hover:bg-red-600"
                  )}
                >
                  {isListening ? "Слушаю..." : "Говорить"}
                </Button>
              </div>

              {/* Result */}
              {score && (
                <div className={cn("p-4 rounded-lg border", SCORE_CONFIG[score].bg)}>
                  <p className={cn("text-lg font-bold", SCORE_CONFIG[score].color)}>
                    {SCORE_CONFIG[score].label}
                  </p>
                  {transcript && (
                    <p className="text-sm mt-1">
                      Вы сказали: <HebrewText size="sm" className="font-medium">{transcript}</HebrewText>
                    </p>
                  )}
                  {distance > 0 && (
                    <p className="text-xs text-muted-foreground mt-1">
                      Расстояние: {distance}
                    </p>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          <div className="flex justify-center gap-3">
            <Button variant="outline" onClick={handleSpeak} disabled={isListening}>
              Попробовать снова
            </Button>
            <Button onClick={handleNext}>
              Следующее слово
            </Button>
          </div>
        </>
      )}
    </div>
  );
}
