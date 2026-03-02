import { useCallback, useRef } from "react";

type SoundType = "correct" | "wrong" | "achievement" | "levelUp";

function isMuted(): boolean {
  return localStorage.getItem("sound-muted") === "true";
}

export function toggleSoundMute(): boolean {
  const newVal = !isMuted();
  localStorage.setItem("sound-muted", String(newVal));
  return newVal;
}

export function isSoundMuted(): boolean {
  return isMuted();
}

function playTone(
  ctx: AudioContext,
  freq: number,
  startTime: number,
  duration: number,
  type: OscillatorType = "sine",
  gain = 0.15,
) {
  const osc = ctx.createOscillator();
  const g = ctx.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(freq, startTime);
  g.gain.setValueAtTime(gain, startTime);
  g.gain.exponentialRampToValueAtTime(0.001, startTime + duration);
  osc.connect(g);
  g.connect(ctx.destination);
  osc.start(startTime);
  osc.stop(startTime + duration);
}

const SOUNDS: Record<SoundType, (ctx: AudioContext) => void> = {
  correct: (ctx) => {
    const t = ctx.currentTime;
    playTone(ctx, 523.25, t, 0.15); // C5
    playTone(ctx, 659.25, t + 0.1, 0.2); // E5
  },
  wrong: (ctx) => {
    const t = ctx.currentTime;
    playTone(ctx, 220, t, 0.25, "sawtooth", 0.1); // A3
    playTone(ctx, 185, t + 0.15, 0.25, "sawtooth", 0.1); // F#3
  },
  achievement: (ctx) => {
    const t = ctx.currentTime;
    playTone(ctx, 523.25, t, 0.15); // C5
    playTone(ctx, 659.25, t + 0.12, 0.15); // E5
    playTone(ctx, 783.99, t + 0.24, 0.25); // G5
  },
  levelUp: (ctx) => {
    const t = ctx.currentTime;
    const notes = [523.25, 587.33, 659.25, 783.99, 880]; // C5 D5 E5 G5 A5
    notes.forEach((freq, i) => {
      playTone(ctx, freq, t + i * 0.1, 0.2);
    });
  },
};

export function useSoundEffects() {
  const ctxRef = useRef<AudioContext | null>(null);

  const play = useCallback((type: SoundType) => {
    if (isMuted()) return;
    try {
      if (!ctxRef.current) {
        ctxRef.current = new AudioContext();
      }
      const ctx = ctxRef.current;
      if (ctx.state === "suspended") {
        ctx.resume();
      }
      SOUNDS[type](ctx);
    } catch {
      // Web Audio not available
    }
  }, []);

  return { play };
}
