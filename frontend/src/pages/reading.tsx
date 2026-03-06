import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useReadingTexts, useReadingText } from "@/hooks/use-lessons";
import { useAutoCompleteStep } from "@/hooks/use-path";
import { useCreateSentenceCards } from "@/hooks/use-srs";
import { toast } from "@/hooks/use-toast";
import { useUrlNumParam } from "@/hooks/use-url-state";
import { HebrewText } from "@/components/hebrew-text";
import { InteractiveReader } from "@/components/interactive-reader";
import { TTSControls, useTTS } from "@/components/tts-controls";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { LEVEL_LABELS } from "@/lib/constants";

const CAT_LABELS: Record<string, string> = {
  story: "Рассказ",
  dialog: "Диалог",
};

function VocabWord({ word }: {
  word: { he: string; ru: string; translit?: string };
}) {
  const { speak } = useTTS();
  return (
    <div className="flex items-center gap-2 p-2 rounded border text-sm hover:bg-accent hover:border-primary/30 transition-colors">
      <button
        className="shrink-0 text-muted-foreground hover:text-primary transition-colors"
        onClick={() => speak(word.he)}
        title="Прослушать"
      >
        ▶
      </button>
      <Link
        to={`/dictionary?search=${encodeURIComponent(word.he)}`}
        className="flex items-center gap-2 flex-1 min-w-0"
        title="Найти в словаре"
      >
        <HebrewText size="sm" className="font-bold">
          {word.he}
        </HebrewText>
        {word.translit && (
          <span className="text-muted-foreground text-xs">{word.translit}</span>
        )}
        <span className="text-xs">— {word.ru}</span>
        <span className="text-xs text-muted-foreground ml-auto shrink-0">→</span>
      </Link>
    </div>
  );
}


export function ReadingPage() {
  const { textId: textIdParam } = useParams<{ textId: string }>();
  const navigate = useNavigate();
  const { data: texts, isLoading } = useReadingTexts();
  const selectedTextId = textIdParam ? Number(textIdParam) : null;
  const { data: textDetail } = useReadingText(selectedTextId);
  const [showTranslation, setShowTranslation] = useState(false);
  const [levelFilter, setLevelFilter] = useUrlNumParam("level");
  const createSentenceCards = useCreateSentenceCards();

  // Persist read texts in localStorage
  const readTextsKey = "hebrew-read-texts";
  const isAlreadyRead = (() => {
    if (!selectedTextId) return false;
    try {
      const stored = JSON.parse(localStorage.getItem(readTextsKey) || "[]");
      return stored.includes(selectedTextId);
    } catch { return false; }
  })();
  const [readingDone, setReadingDone] = useState(isAlreadyRead);

  const markAsRead = () => {
    setReadingDone(true);
    if (selectedTextId) {
      try {
        const stored: number[] = JSON.parse(localStorage.getItem(readTextsKey) || "[]");
        if (!stored.includes(selectedTextId)) {
          stored.push(selectedTextId);
          localStorage.setItem(readTextsKey, JSON.stringify(stored));
        }
      } catch { /* ignore */ }
    }
  };

  // Auto-complete learning path step when text is marked as read
  useAutoCompleteStep("reading", selectedTextId, readingDone);

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-12">Загрузка...</p>;
  }

  const filteredTexts = levelFilter !== null
    ? texts?.filter((t) => t.level_id === levelFilter)
    : texts;

  // ── Text detail view ──
  if (selectedTextId && textDetail) {
    return (
      <div className="space-y-6">
        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => { navigate("/reading"); setShowTranslation(false); }}
          >
            ← Назад
          </Button>
          <div>
            <h1 className="text-xl font-bold">{textDetail.title_ru}</h1>
            <HebrewText size="sm" className="text-muted-foreground">
              {textDetail.title_he}
            </HebrewText>
          </div>
          <Badge variant="secondary">
            {LEVEL_LABELS[textDetail.level_id]}
          </Badge>
          <Badge variant="outline">
            {CAT_LABELS[textDetail.category] || textDetail.category}
          </Badge>
        </div>

        {/* Play entire text */}
        <TTSControls text={textDetail.content_he} size="default" label="Прослушать текст" />

        {/* Vocabulary */}
        {textDetail.vocabulary_json && (
          <div>
            <h2 className="text-sm font-medium text-muted-foreground mb-2">
              Словарь к тексту ({(textDetail.vocabulary_json as any[]).length} слов)
            </h2>
            <div className="grid gap-1 sm:grid-cols-2 md:grid-cols-3">
              {(textDetail.vocabulary_json as Array<{ he: string; ru: string; translit?: string }>).map(
                (w, i) => <VocabWord key={i} word={w} />
              )}
            </div>
          </div>
        )}

        {/* Interactive text */}
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-base">Текст</CardTitle>
            <CardDescription>Нажмите на любое слово для перевода и произношения</CardDescription>
          </CardHeader>
          <CardContent>
            <InteractiveReader
              contentHe={textDetail.content_he}
              vocabulary={(textDetail.vocabulary_json as Array<{ he: string; ru: string; translit?: string }>) ?? []}
            />
          </CardContent>
        </Card>

        {/* Translation toggle */}
        <div>
          <Button
            variant="outline"
            className="w-full"
            onClick={() => setShowTranslation(!showTranslation)}
          >
            {showTranslation ? "Скрыть перевод" : "Показать перевод"}
          </Button>
          {showTranslation && (
            <Card className="mt-3">
              <CardContent className="py-4">
                <p className="leading-relaxed">{textDetail.content_ru}</p>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Mark as read */}
        {!readingDone && (
          <Button className="w-full" onClick={markAsRead}>
            Прочитано
          </Button>
        )}
        {readingDone && (
          <p className="text-center text-sm text-green-600 font-medium">Отмечено как прочитанное</p>
        )}

        {/* SRS sentence cards */}
        <Button
          variant="outline"
          className="w-full"
          disabled={createSentenceCards.isPending}
          onClick={async () => {
            try {
              const result = await createSentenceCards.mutateAsync({ text_id: selectedTextId! });
              toast({ title: "SRS карточки", description: `Создано ${result.created} карточек из предложений` });
            } catch {
              toast({ title: "Ошибка", description: "Не удалось создать карточки", variant: "destructive" });
            }
          }}
        >
          {createSentenceCards.isPending ? "Создание..." : "В SRS карточки (из предложений)"}
        </Button>

        {/* Cross-links */}
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" size="sm" asChild>
            <Link to={`/cloze/${selectedTextId}`}>
              Пропуски
            </Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link to={`/dictionary?level=${textDetail.level_id}`}>
              Словарь · {LEVEL_LABELS[textDetail.level_id]}
            </Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link to={`/dialogues`}>
              Диалоги
            </Link>
          </Button>
          <Button variant="outline" size="sm" asChild>
            <Link to={`/lessons`}>
              Уроки
            </Link>
          </Button>
        </div>
      </div>
    );
  }

  // Read texts from localStorage for list badges
  const readTextIds = new Set<number>((() => {
    try { return JSON.parse(localStorage.getItem(readTextsKey) || "[]"); }
    catch { return []; }
  })());

  // ── Text list view ──
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Чтение</h1>
        <div className="flex gap-1">
          <Button
            variant={levelFilter === null ? "default" : "ghost"}
            size="sm"
            onClick={() => setLevelFilter(null)}
          >
            Все ({texts?.length ?? 0})
          </Button>
          {[1, 2, 3, 4, 5, 6].map((lvl) => {
            const count = texts?.filter((t) => t.level_id === lvl).length ?? 0;
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

      <div className="grid gap-3 sm:grid-cols-2">
        {filteredTexts?.map((text) => (
          <Card
            key={text.id}
            className="cursor-pointer hover:bg-accent/50 transition-colors"
            onClick={() => navigate(`/reading/${text.id}`)}
          >
            <CardHeader className="pb-3">
              <div className="flex items-center gap-2 mb-1">
                <Badge variant="secondary">{LEVEL_LABELS[text.level_id]}</Badge>
                <Badge variant="outline">{CAT_LABELS[text.category] || text.category}</Badge>
              </div>
              <CardTitle className="text-base flex items-center gap-2">
                {text.title_ru}
                {readTextIds.has(text.id) && (
                  <Badge variant="secondary" className="text-green-700 text-[10px]">Прочитано</Badge>
                )}
              </CardTitle>
              <HebrewText size="sm" className="text-muted-foreground">
                {text.title_he}
              </HebrewText>
            </CardHeader>
          </Card>
        ))}
      </div>
    </div>
  );
}
