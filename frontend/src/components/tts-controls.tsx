import { useState, useCallback, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const SPEEDS = [0.5, 0.75, 1, 1.25] as const;

interface TTSControlsProps {
  text: string;
  lang?: string;
  className?: string;
  size?: "sm" | "default" | "lg";
  label?: string;
}

export function TTSControls({
  text,
  lang = "he-IL",
  className,
  size = "default",
  label,
}: TTSControlsProps) {
  const [speed, setSpeed] = useState<number>(1);
  const [isPlaying, setIsPlaying] = useState(false);
  const utteranceRef = useRef<SpeechSynthesisUtterance | null>(null);

  const speak = useCallback(() => {
    if (!("speechSynthesis" in window)) return;

    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    utterance.rate = speed;
    utterance.onstart = () => setIsPlaying(true);
    utterance.onend = () => setIsPlaying(false);
    utterance.onerror = () => setIsPlaying(false);
    utteranceRef.current = utterance;
    window.speechSynthesis.speak(utterance);
  }, [text, lang, speed]);

  const stop = useCallback(() => {
    window.speechSynthesis.cancel();
    setIsPlaying(false);
  }, []);

  useEffect(() => {
    return () => {
      window.speechSynthesis.cancel();
    };
  }, []);

  return (
    <div className={cn("flex items-center gap-2", className)}>
      <Button
        type="button"
        variant={isPlaying ? "destructive" : "outline"}
        size={size}
        onClick={isPlaying ? stop : speak}
      >
        {isPlaying ? "■ Стоп" : `▶ ${label || "Слушать"}`}
      </Button>
      <div className="flex gap-0.5">
        {SPEEDS.map((s) => (
          <button
            key={s}
            type="button"
            className={cn(
              "px-1.5 py-0.5 text-xs rounded transition-colors",
              speed === s
                ? "bg-primary text-primary-foreground"
                : "bg-secondary text-secondary-foreground hover:bg-secondary/80"
            )}
            onClick={() => setSpeed(s)}
          >
            {s}x
          </button>
        ))}
      </div>
    </div>
  );
}

// Hook for TTS
export function useTTS(lang = "he-IL") {
  const speak = useCallback(
    (text: string, rate = 1) => {
      if (!("speechSynthesis" in window)) return;
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(text);
      u.lang = lang;
      u.rate = rate;
      window.speechSynthesis.speak(u);
    },
    [lang]
  );

  const stop = useCallback(() => {
    window.speechSynthesis.cancel();
  }, []);

  return { speak, stop };
}
