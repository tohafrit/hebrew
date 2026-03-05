import { useState, useCallback, useRef, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useDialogues, useDialogue, useCheckDialogue, type DialogueLine } from "@/hooks/use-dialogues";
import { HebrewText } from "@/components/hebrew-text";
import { TTSControls, useTTS } from "@/components/tts-controls";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { LEVEL_LABELS } from "@/lib/constants";

// ── Dialogue bubble ───────────────────────────────────────────────────────

function DialogueBubble({ line, isRevealed, result }: {
  line: DialogueLine;
  isRevealed: boolean;
  result?: { correct: boolean; correctText: string } | null;
}) {
  const { speak } = useTTS();
  const isUser = line.is_user;

  return (
    <div className={cn("flex gap-3", isUser ? "flex-row-reverse" : "flex-row")}>
      {/* Avatar */}
      <div className={cn(
        "w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold shrink-0",
        isUser ? "bg-primary text-primary-foreground" : "bg-secondary text-secondary-foreground"
      )}>
        {line.speaker}
      </div>

      {/* Bubble */}
      <div className={cn(
        "max-w-[75%] rounded-lg p-3 space-y-1",
        isUser ? "bg-primary/10 border border-primary/20" : "bg-muted",
        result && !result.correct && "border-red-300 bg-red-50"
      )}>
        <p className="text-xs text-muted-foreground font-medium">{line.speaker_name}</p>

        {isRevealed && line.text_he && (
          <div className="flex items-start gap-2">
            <HebrewText size="sm" className="font-medium leading-relaxed">
              {line.text_he}
            </HebrewText>
            {line.text_he && (
              <button
                className="shrink-0 text-xs text-muted-foreground hover:text-primary"
                onClick={() => speak(line.text_he)}
              >
                ▶
              </button>
            )}
          </div>
        )}

        {result && !result.correct && (
          <div className="flex items-start gap-2 border-t pt-1 mt-1">
            <HebrewText size="sm" className="font-medium text-green-700">
              {result.correctText}
            </HebrewText>
          </div>
        )}

        <p className="text-sm text-muted-foreground">{line.text_ru}</p>
      </div>
    </div>
  );
}

// ── Dialogue player ───────────────────────────────────────────────────────

function DialoguePlayer({ dialogueId, onBack }: {
  dialogueId: number;
  onBack: () => void;
}) {
  const { data: dialogue } = useDialogue(dialogueId);
  const checkDialogue = useCheckDialogue();
  const { speak } = useTTS();
  const [currentLine, setCurrentLine] = useState(0);
  const [revealedLines, setRevealedLines] = useState<Set<number>>(new Set());
  const [results, setResults] = useState<Map<number, { correct: boolean; correctText: string }>>(new Map());
  const [dialogueDone, setDialogueDone] = useState(false);
  const [score, setScore] = useState({ correct: 0, total: 0 });
  const scrollRef = useRef<HTMLDivElement>(null);

  const [localLines, setLocalLines] = useState<any[]>([]);
  const ttsTimerRef = useRef<ReturnType<typeof setTimeout>>();
  const advanceTimerRef = useRef<ReturnType<typeof setTimeout>>();

  // Clean up timers on unmount
  useEffect(() => {
    return () => {
      clearTimeout(ttsTimerRef.current);
      clearTimeout(advanceTimerRef.current);
    };
  }, []);

  // Clone lines from query data to avoid mutating React Query cache
  useEffect(() => {
    if (dialogue?.lines_json) {
      setLocalLines(dialogue.lines_json.map((l: any) => ({ ...l })));
    }
  }, [dialogue?.id]);

  const lines = localLines;
  const currentLineData = lines[currentLine] as DialogueLine | undefined;

  // Auto-scroll to bottom when new lines appear
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [revealedLines.size]);

  // Auto-advance non-user lines
  useEffect(() => {
    if (!currentLineData) return;
    if (!currentLineData.is_user) {
      // Reveal NPC line immediately
      setRevealedLines((prev) => new Set(prev).add(currentLine));
      // Auto-play TTS for NPC line
      if (currentLineData.text_he) {
        clearTimeout(ttsTimerRef.current);
        ttsTimerRef.current = setTimeout(() => speak(currentLineData.text_he), 300);
      }
    }
  }, [currentLine, currentLineData, speak]);

  const handleSelectOption = useCallback(
    async (optionIdx: number) => {
      if (!dialogue || !currentLineData) return;

      let res;
      try {
        res = await checkDialogue.mutateAsync({
          dialogue_id: dialogue.id,
          line_index: currentLine,
          selected_option: optionIdx,
        });
      } catch {
        // On error, treat as incorrect and continue
        res = { correct: false, correct_text_he: currentLineData.options?.[0] ?? "" };
      }

      const selectedText = currentLineData.options?.[optionIdx] ?? "";
      // Update line with selected text (using local copy, not React Query cache)
      setLocalLines((prev) => {
        const updated = [...prev];
        updated[currentLine] = { ...prev[currentLine], text_he: selectedText };
        return updated;
      });

      setRevealedLines((prev) => new Set(prev).add(currentLine));
      setResults((prev) => new Map(prev).set(currentLine, {
        correct: res.correct,
        correctText: res.correct_text_he,
      }));
      setScore((prev) => ({
        correct: prev.correct + (res.correct ? 1 : 0),
        total: prev.total + 1,
      }));

      // Speak the selected/correct option
      speak(res.correct ? selectedText : res.correct_text_he);

      // Advance to next line after a delay
      advanceTimerRef.current = setTimeout(() => {
        if (currentLine + 1 < lines.length) {
          setCurrentLine((i) => i + 1);
        } else {
          setDialogueDone(true);
        }
      }, 1200);
    },
    [dialogue, currentLine, currentLineData, checkDialogue, speak]
  );

  const handleContinue = useCallback(() => {
    if (currentLine + 1 < localLines.length) {
      setCurrentLine((i) => i + 1);
    } else {
      setDialogueDone(true);
    }
  }, [currentLine, localLines.length]);

  if (!dialogue) {
    return <p className="text-center text-muted-foreground py-12">Загрузка...</p>;
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <Button variant="ghost" size="sm" onClick={onBack}>← Назад</Button>
        <div>
          <h1 className="text-xl font-bold">{dialogue.title}</h1>
          <p className="text-sm text-muted-foreground">{dialogue.situation_ru}</p>
        </div>
        <Badge variant="secondary">{LEVEL_LABELS[dialogue.level_id]}</Badge>
      </div>

      {/* Vocabulary */}
      {dialogue.vocabulary_json && dialogue.vocabulary_json.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {dialogue.vocabulary_json.map((w, i) => (
            <Link key={i} to={`/dictionary?search=${encodeURIComponent(w.he)}`}>
              <Badge variant="outline" className="text-xs hover:bg-accent cursor-pointer transition-colors">
                <HebrewText size="sm">{w.he}</HebrewText>
                <span className="mx-1">—</span>
                {w.ru}
              </Badge>
            </Link>
          ))}
        </div>
      )}

      {/* Chat area */}
      <Card>
        <CardContent className="p-4">
          <div ref={scrollRef} className="space-y-4 max-h-[400px] overflow-y-auto">
            {lines.map((line, i) => {
              if (!revealedLines.has(i)) return null;
              return (
                <DialogueBubble
                  key={i}
                  line={line as DialogueLine}
                  isRevealed={true}
                  result={results.get(i)}
                />
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* User options / continue button */}
      {!dialogueDone && currentLineData && (
        <>
          {currentLineData.is_user && currentLineData.options && !revealedLines.has(currentLine) ? (
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">{currentLineData.text_ru}</p>
              <div className="grid gap-2">
                {currentLineData.options.map((opt, i) => (
                  <Button
                    key={i}
                    variant="outline"
                    className="justify-start h-auto py-3 text-right"
                    dir="rtl"
                    onClick={() => handleSelectOption(i)}
                    disabled={checkDialogue.isPending}
                  >
                    <HebrewText size="sm">{opt}</HebrewText>
                  </Button>
                ))}
              </div>
            </div>
          ) : !currentLineData.is_user && revealedLines.has(currentLine) ? (
            <Button className="w-full" onClick={handleContinue}>
              Продолжить
            </Button>
          ) : null}
        </>
      )}

      {/* Dialogue complete */}
      {dialogueDone && (
        <Card>
          <CardContent className="p-8 text-center space-y-4">
            <p className="text-2xl font-bold">Диалог завершён!</p>
            <p className="text-muted-foreground">
              Правильных ответов: {score.correct} из {score.total}
            </p>
            <div className="flex gap-2 justify-center">
              <Button variant="outline" onClick={onBack}>К диалогам</Button>
              <Button onClick={() => {
                setCurrentLine(0);
                setRevealedLines(new Set());
                setResults(new Map());
                setDialogueDone(false);
                setScore({ correct: 0, total: 0 });
              }}>
                Повторить
              </Button>
            </div>
            <div className="flex gap-2 justify-center pt-2">
              <Button variant="ghost" size="sm" asChild>
                <Link to="/reading">Чтение</Link>
              </Button>
              <Button variant="ghost" size="sm" asChild>
                <Link to="/lessons">Уроки</Link>
              </Button>
              <Button variant="ghost" size="sm" asChild>
                <Link to="/dictionary">Словарь</Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

// ── Main page ──────────────────────────────────────────────────────────────

export function DialoguesPage() {
  const { dialogueId: dialogueIdParam } = useParams<{ dialogueId: string }>();
  const navigate = useNavigate();
  const { data: dialogues, isLoading } = useDialogues();
  const selectedId = dialogueIdParam ? Number(dialogueIdParam) : null;
  const [levelFilter, setLevelFilter] = useState<number | null>(null);

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-12">Загрузка...</p>;
  }

  if (selectedId !== null) {
    return <DialoguePlayer dialogueId={selectedId} onBack={() => navigate("/dialogues")} />;
  }

  const filtered = levelFilter
    ? dialogues?.filter((d) => d.level_id === levelFilter)
    : dialogues;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Диалоги</h1>
        <div className="flex gap-1">
          <Button
            variant={levelFilter === null ? "default" : "ghost"}
            size="sm"
            onClick={() => setLevelFilter(null)}
          >
            Все ({dialogues?.length ?? 0})
          </Button>
          {[1, 2, 3, 4, 5, 6].map((lvl) => {
            const count = dialogues?.filter((d) => d.level_id === lvl).length ?? 0;
            return (
              <Button
                key={lvl}
                variant={levelFilter === lvl ? "default" : "ghost"}
                size="sm"
                onClick={() => setLevelFilter(lvl)}
              >
                {LEVEL_LABELS[lvl]} ({count})
              </Button>
            );
          })}
        </div>
      </div>

      <p className="text-muted-foreground">
        Практикуйте иврит в реальных ситуациях: выбирайте реплики и участвуйте в диалоге
      </p>

      <div className="grid gap-3 sm:grid-cols-2">
        {filtered?.map((d) => (
          <Card
            key={d.id}
            className="cursor-pointer hover:bg-accent/50 transition-colors"
            onClick={() => navigate(`/dialogues/${d.id}`)}
          >
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2 mb-1">
                <Badge variant="secondary">{LEVEL_LABELS[d.level_id]}</Badge>
              </div>
              <CardTitle className="text-base">{d.title}</CardTitle>
              {d.situation_ru && (
                <CardDescription className="line-clamp-2">{d.situation_ru}</CardDescription>
              )}
            </CardHeader>
          </Card>
        ))}
      </div>
    </div>
  );
}
