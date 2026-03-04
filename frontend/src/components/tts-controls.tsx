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
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const speakServer = useCallback(
    async (rate: number) => {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) throw new Error("No auth token");

        const url = `/api/tts/speak?text=${encodeURIComponent(text)}&rate=${rate}`;
        const resp = await fetch(url, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!resp.ok) throw new Error(`TTS error ${resp.status}`);

        const blob = await resp.blob();
        const audioUrl = URL.createObjectURL(blob);
        const audio = new Audio(audioUrl);
        audioRef.current = audio;

        audio.onplay = () => setIsPlaying(true);
        audio.onended = () => {
          setIsPlaying(false);
          URL.revokeObjectURL(audioUrl);
        };
        audio.onerror = () => {
          setIsPlaying(false);
          URL.revokeObjectURL(audioUrl);
        };

        await audio.play();
        return true;
      } catch {
        return false;
      }
    },
    [text]
  );

  const speakFallback = useCallback(
    (rate: number) => {
      if (!("speechSynthesis" in window)) return;
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = lang;
      utterance.rate = rate;
      utterance.onstart = () => setIsPlaying(true);
      utterance.onend = () => setIsPlaying(false);
      utterance.onerror = () => setIsPlaying(false);
      window.speechSynthesis.speak(utterance);
    },
    [text, lang]
  );

  const speak = useCallback(async () => {
    const ok = await speakServer(speed);
    if (!ok) {
      speakFallback(speed);
    }
  }, [speakServer, speakFallback, speed]);

  const stop = useCallback(() => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      audioRef.current = null;
    }
    window.speechSynthesis.cancel();
    setIsPlaying(false);
  }, []);

  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
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
    async (text: string, rate = 1) => {
      // Try server TTS first
      try {
        const token = localStorage.getItem("access_token");
        if (token) {
          const url = `/api/tts/speak?text=${encodeURIComponent(text)}&rate=${rate}`;
          const resp = await fetch(url, {
            headers: { Authorization: `Bearer ${token}` },
          });
          if (resp.ok) {
            const blob = await resp.blob();
            const audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);
            audio.onended = () => URL.revokeObjectURL(audioUrl);
            await audio.play();
            return;
          }
        }
      } catch {
        // Fall through to Web Speech API
      }

      // Fallback to Web Speech API
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
