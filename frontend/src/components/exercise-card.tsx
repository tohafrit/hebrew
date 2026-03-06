import { useState, useCallback, useEffect } from "react";
import { useCheckExercise, type Exercise, type ExerciseCheckResponse } from "@/hooks/use-lessons";
import { useSoundEffects } from "@/hooks/use-sound-effects";
import { HebrewText } from "@/components/hebrew-text";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { TTSControls } from "@/components/tts-controls";
import { HebrewKeyboard } from "@/components/hebrew-keyboard";
import { cn } from "@/lib/utils";

// ── Exercise components ────────────────────────────────────────────────────

export function MultipleChoiceExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const prompt = exercise.prompt_json as { question?: string; options?: string[] };
  const question = prompt.question || "";
  const options = prompt.options || [];

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const idx = parseInt(e.key, 10) - 1;
      if (idx >= 0 && idx < options.length) {
        onAnswer(options[idx]);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [options, onAnswer]);

  return (
    <div className="space-y-3">
      {question && <p className="font-medium">{question}</p>}
      <div className="grid gap-2">
        {options.map((opt, i) => (
          <Button
            key={i}
            variant="outline"
            className="justify-start h-auto py-3 px-4 text-left"
            onClick={() => onAnswer(opt)}
          >
            <span className="text-xs text-muted-foreground mr-2 w-5">{i + 1}.</span>
            <span>{opt}</span>
          </Button>
        ))}
      </div>
    </div>
  );
}

export function FillBlankExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const [value, setValue] = useState("");
  const prompt = exercise.prompt_json as { sentence_ru?: string; context?: string; hint?: string };

  return (
    <div className="space-y-3">
      <p className="font-medium">{prompt.context || "Заполните пропуск"}</p>
      {prompt.sentence_ru && <p className="text-lg">{prompt.sentence_ru}</p>}
      {prompt.hint && (
        <p className="text-sm text-muted-foreground">Подсказка: {prompt.hint}</p>
      )}
      <div className="flex gap-2">
        <Input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="Ваш ответ..."
          onKeyDown={(e) => {
            if (e.key === "Enter" && value.trim()) onAnswer(value.trim());
          }}
        />
        <Button onClick={() => value.trim() && onAnswer(value.trim())}>OK</Button>
      </div>
    </div>
  );
}

/**
 * match_pairs: backend expects dict {"left_text": "right_text", ...}
 * answer_json.matches = {"א": "Алеф", "ב": "Бет", ...}
 */
export function MatchPairsExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const prompt = exercise.prompt_json as { pairs_left?: string[]; pairs_right?: string[] };
  const pairsLeft = prompt.pairs_left || [];
  const pairsRight = prompt.pairs_right || [];
  const [matches, setMatches] = useState<Record<string, string>>({});
  const [selectedLeft, setSelectedLeft] = useState<string | null>(null);

  const usedRight = new Set(Object.values(matches));

  const handleRightClick = (right: string) => {
    if (!selectedLeft) return;
    const updated = { ...matches, [selectedLeft]: right };
    setMatches(updated);
    setSelectedLeft(null);

    if (Object.keys(updated).length === pairsLeft.length) {
      onAnswer(updated);
    }
  };

  return (
    <div className="space-y-3">
      <p className="font-medium">Соедините пары</p>
      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          {pairsLeft.map((left) => (
            <Button
              key={left}
              variant={selectedLeft === left ? "default" : matches[left] ? "secondary" : "outline"}
              className="w-full justify-start h-auto py-2"
              onClick={() => {
                if (matches[left]) {
                  const updated = { ...matches };
                  delete updated[left];
                  setMatches(updated);
                }
                setSelectedLeft(left);
              }}
            >
              {left}
              {matches[left] && (
                <span className="ml-auto text-xs text-muted-foreground">
                  → {matches[left]}
                </span>
              )}
            </Button>
          ))}
        </div>
        <div className="space-y-2">
          {pairsRight.map((right) => (
            <Button
              key={right}
              variant={usedRight.has(right) ? "secondary" : "outline"}
              className="w-full justify-start h-auto py-2"
              disabled={usedRight.has(right)}
              onClick={() => handleRightClick(right)}
            >
              {right}
            </Button>
          ))}
        </div>
      </div>
    </div>
  );
}

export function WordOrderExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const prompt = exercise.prompt_json as {
    words_shuffled?: string[];
    translation?: string;
  };
  const wordsShuffled = prompt.words_shuffled || [];
  const [selected, setSelected] = useState<{ word: string; origIdx: number }[]>([]);
  const usedIndices = new Set(selected.map((s) => s.origIdx));
  const remaining = wordsShuffled
    .map((w, i) => ({ word: w, origIdx: i }))
    .filter((item) => !usedIndices.has(item.origIdx));

  return (
    <div className="space-y-3">
      <p className="font-medium">Составьте предложение</p>
      {prompt.translation && (
        <p className="text-sm text-muted-foreground">{prompt.translation}</p>
      )}

      <div className="min-h-[48px] border rounded-lg p-3 flex flex-wrap gap-2" dir="rtl">
        {selected.map((item, i) => (
          <Badge
            key={`${item.origIdx}-${i}`}
            variant="default"
            className="cursor-pointer text-sm"
            onClick={() => setSelected(selected.filter((_, j) => j !== i))}
          >
            {item.word}
          </Badge>
        ))}
      </div>

      <div className="flex flex-wrap gap-2" dir="rtl">
        {remaining.map((item) => (
          <Badge
            key={item.origIdx}
            variant="outline"
            className="cursor-pointer text-sm"
            onClick={() => {
              const updated = [...selected, item];
              setSelected(updated);
              if (updated.length === wordsShuffled.length) {
                onAnswer(updated.map((s) => s.word));
              }
            }}
          >
            {item.word}
          </Badge>
        ))}
      </div>
    </div>
  );
}

export function DictationExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const [value, setValue] = useState("");
  const prompt = exercise.prompt_json as {
    word_he?: string;
    audio_text?: string;
    word_translit?: string;
    hint?: string;
    instruction?: string;
  };

  const hebrewText = prompt.word_he || prompt.audio_text || "";
  const hintText = prompt.hint || prompt.instruction;

  return (
    <div className="space-y-4">
      <p className="text-muted-foreground text-sm">Прослушайте и запишите на иврите</p>
      {hintText && <p className="text-sm text-muted-foreground">Подсказка: {hintText}</p>}
      {hebrewText && <TTSControls text={hebrewText} size="lg" label="Прослушать" />}
      <div className="space-y-2">
        <div className="flex gap-2">
          <Input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Введите слово на иврите..."
            dir="rtl"
            className="font-hebrew text-lg"
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
    </div>
  );
}

export function TranslateRuHeExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const [value, setValue] = useState("");
  const prompt = exercise.prompt_json as {
    prompt_ru?: string;
    hint?: string;
    target_he?: string;
  };

  return (
    <div className="space-y-4">
      <p className="font-medium">Переведите на иврит:</p>
      {prompt.prompt_ru && <p className="text-2xl font-bold">{prompt.prompt_ru}</p>}
      {prompt.hint && (
        <p className="text-sm text-muted-foreground">
          Подсказка: <HebrewText size="sm">{prompt.hint}</HebrewText>
          <TTSControls text={prompt.hint} size="sm" className="inline-flex ml-2" />
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
    </div>
  );
}

/**
 * hebrew_typing: type Hebrew word from prompt
 * prompt_json: { prompt: string, target_he: string, transliteration?: string }
 */
export function HebrewTypingExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const [value, setValue] = useState("");
  const prompt = exercise.prompt_json as {
    prompt?: string;
    target_he?: string;
    transliteration?: string;
  };

  return (
    <div className="space-y-4">
      {prompt.prompt && <p className="font-medium">{prompt.prompt}</p>}
      {prompt.target_he && (
        <TTSControls text={prompt.target_he} size="lg" label="Прослушать" />
      )}
      <div className="space-y-2">
        <div className="flex gap-2">
          <Input
            value={value}
            onChange={(e) => setValue(e.target.value)}
            placeholder="Введите на иврите..."
            dir="rtl"
            className="font-hebrew text-lg"
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
    </div>
  );
}

/**
 * minimal_pairs: listen to two words, pick which one you heard
 * prompt_json: { pair_a: {he, meaning, translit}, pair_b: {he, meaning, translit}, question, correct_pair }
 * answer: "a" or "b"
 */
export function MinimalPairsExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const prompt = exercise.prompt_json as {
    pair_a?: { he?: string; meaning?: string; translit?: string };
    pair_b?: { he?: string; meaning?: string; translit?: string };
    question?: string;
    correct_pair?: string;
  };

  const pairA = prompt.pair_a || {};
  const pairB = prompt.pair_b || {};
  const correctHe = prompt.correct_pair === "a" ? pairA.he : pairB.he;

  return (
    <div className="space-y-4">
      {prompt.question && <p className="font-medium">{prompt.question}</p>}

      {/* Play the correct word */}
      {correctHe && (
        <TTSControls text={correctHe} size="lg" label="Прослушать слово" />
      )}

      <div className="grid grid-cols-2 gap-3">
        {/* Option A */}
        <Button
          variant="outline"
          className="h-auto py-4 flex flex-col gap-1"
          onClick={() => onAnswer("a")}
        >
          {pairA.he && <HebrewText size="xl" className="font-bold">{pairA.he}</HebrewText>}
          {pairA.translit && <span className="text-xs text-muted-foreground">{pairA.translit}</span>}
          {pairA.meaning && <span className="text-sm">{pairA.meaning}</span>}
        </Button>

        {/* Option B */}
        <Button
          variant="outline"
          className="h-auto py-4 flex flex-col gap-1"
          onClick={() => onAnswer("b")}
        >
          {pairB.he && <HebrewText size="xl" className="font-bold">{pairB.he}</HebrewText>}
          {pairB.translit && <span className="text-xs text-muted-foreground">{pairB.translit}</span>}
          {pairB.meaning && <span className="text-sm">{pairB.meaning}</span>}
        </Button>
      </div>
    </div>
  );
}

/**
 * listening_comprehension: listen to text, answer multiple questions
 * prompt_json: { text_he, text_translit, questions: [{question, options, correct}] }
 * answer: list of selected answers (one per question)
 */
export function ListeningComprehensionExercise({ exercise, onAnswer }: {
  exercise: Exercise;
  onAnswer: (answer: any) => void;
}) {
  const prompt = exercise.prompt_json as {
    text_he?: string;
    text_translit?: string;
    questions?: Array<{ question?: string; options?: string[]; correct?: string }>;
  };

  const questions = prompt.questions || [];
  const [answers, setAnswers] = useState<(string | null)[]>(
    new Array(questions.length).fill(null)
  );

  const handleSelect = (qIdx: number, option: string) => {
    const updated = [...answers];
    updated[qIdx] = option;
    setAnswers(updated);

    // Auto-submit when all questions answered
    if (updated.every((a) => a !== null)) {
      onAnswer(updated);
    }
  };

  return (
    <div className="space-y-4">
      {/* Audio text */}
      {prompt.text_he && (
        <div className="space-y-2">
          <TTSControls text={prompt.text_he} size="lg" label="Прослушать текст" />
          <div dir="rtl" className="font-hebrew text-lg leading-relaxed p-3 bg-muted rounded-lg">
            {prompt.text_he}
          </div>
        </div>
      )}

      {/* Questions */}
      <div className="space-y-4">
        {questions.map((q, qIdx) => (
          <div key={qIdx} className="space-y-2">
            <p className="font-medium">{q.question}</p>
            <div className="grid gap-2">
              {(q.options || []).map((opt, oIdx) => (
                <Button
                  key={oIdx}
                  variant={answers[qIdx] === opt ? "default" : "outline"}
                  className="justify-start h-auto py-2 px-4 text-left"
                  onClick={() => handleSelect(qIdx, opt)}
                >
                  {opt}
                </Button>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ── Main ExerciseCard ──────────────────────────────────────────────────────

export function ExerciseCard({ exercise, onDone }: {
  exercise: Exercise;
  onDone: () => void;
}) {
  const checkExercise = useCheckExercise();
  const [result, setResult] = useState<ExerciseCheckResponse | null>(null);
  const { play } = useSoundEffects();

  const handleAnswer = useCallback(
    async (answer: any) => {
      try {
        const res = await checkExercise.mutateAsync({
          exercise_id: exercise.id,
          answer,
        });
        setResult(res);
        play(res.correct ? "correct" : "wrong");
      } catch {
        setResult({ correct: false, correct_answer: null, explanation: "Ошибка сети. Попробуйте ещё раз.", points_earned: 0 } as ExerciseCheckResponse);
      }
    },
    [exercise.id, checkExercise, play]
  );

  // Enter key to advance after result is shown
  useEffect(() => {
    if (!result) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Enter") onDone();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [result, onDone]);

  if (result) {
    return (
      <div className="space-y-3">
        <div
          className={cn(
            "p-4 rounded-lg border",
            result.correct
              ? "bg-green-50 border-green-200"
              : "bg-red-50 border-red-200"
          )}
        >
          <p className="font-bold text-lg">
            {result.correct ? "Правильно!" : "Неправильно"}
            {result.correct && ` +${result.points_earned} XP`}
          </p>
          {!result.correct && result.correct_answer && (
            <div className="text-sm mt-1">
              <span>Правильный ответ:{" "}</span>
              <span className="font-medium">
                {typeof result.correct_answer === "string"
                  ? result.correct_answer
                  : JSON.stringify(result.correct_answer)}
              </span>
              {typeof result.correct_answer === "string" && /[\u0590-\u05FF]/.test(result.correct_answer) && (
                <TTSControls text={result.correct_answer} size="sm" className="inline-flex ml-2" />
              )}
            </div>
          )}
          {result.explanation && (
            <p className="text-sm text-muted-foreground mt-2">{result.explanation}</p>
          )}
        </div>
        <Button onClick={onDone} className="w-full">
          Далее
        </Button>
      </div>
    );
  }

  switch (exercise.type) {
    case "multiple_choice":
      return <MultipleChoiceExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "fill_blank":
      return <FillBlankExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "match_pairs":
      return <MatchPairsExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "word_order":
      return <WordOrderExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "translate_ru_he":
      return <TranslateRuHeExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "dictation":
      return <DictationExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "hebrew_typing":
      return <HebrewTypingExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "minimal_pairs":
      return <MinimalPairsExercise exercise={exercise} onAnswer={handleAnswer} />;
    case "listening_comprehension":
      return <ListeningComprehensionExercise exercise={exercise} onAnswer={handleAnswer} />;
    default:
      return <p className="text-muted-foreground">Неизвестный тип упражнения: {exercise.type}</p>;
  }
}

export function exercise_type_label(type: string): string {
  switch (type) {
    case "multiple_choice": return "Выбор ответа";
    case "fill_blank": return "Заполните пропуск";
    case "match_pairs": return "Соединить пары";
    case "word_order": return "Порядок слов";
    case "translate_ru_he": return "Перевод на иврит";
    case "dictation": return "Диктант";
    case "hebrew_typing": return "Набор текста";
    case "minimal_pairs": return "Минимальные пары";
    case "listening_comprehension": return "Аудирование";
    default: return type;
  }
}
