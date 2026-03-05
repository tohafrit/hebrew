import { useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useReadingTexts, useReadingText } from "@/hooks/use-lessons";
import { useAutoCompleteStep } from "@/hooks/use-path";
import { useUrlNumParam } from "@/hooks/use-url-state";
import { HebrewText } from "@/components/hebrew-text";
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

function InteractiveReader({ contentHe, vocabulary }: {
  contentHe: string;
  vocabulary: Array<{ he: string; ru: string; translit?: string }>;
}) {
  const [hoveredWord, setHoveredWord] = useState<string | null>(null);
  const vocabMap = new Map(vocabulary.map((v) => [v.he, v]));

  // Split text into words while preserving spaces and punctuation
  const tokens = contentHe.split(/(\s+)/);

  const tooltip = hoveredWord ? vocabMap.get(hoveredWord) : null;

  return (
    <div className="relative">
      <div className="leading-loose text-xl" dir="rtl">
        {tokens.map((token, i) => {
          // Check if this token matches any vocabulary word
          const cleanToken = token.replace(/[.,!?"״:;]/g, "");
          const match = vocabMap.get(cleanToken);

          if (match) {
            return (
              <span
                key={i}
                className="relative cursor-pointer border-b-2 border-dashed border-primary/30 hover:border-primary hover:bg-primary/10 rounded px-0.5 font-hebrew transition-colors"
                onMouseEnter={() => setHoveredWord(cleanToken)}
                onMouseLeave={() => setHoveredWord(null)}
              >
                {token}
              </span>
            );
          }

          return (
            <span key={i} className="font-hebrew">
              {token}
            </span>
          );
        })}
      </div>

      {tooltip && (
        <div className="mt-3 p-3 bg-muted rounded-lg border text-sm">
          <HebrewText size="lg" className="font-bold block">
            {tooltip.he}
          </HebrewText>
          {tooltip.translit && (
            <span className="text-muted-foreground">{tooltip.translit}</span>
          )}
          <span className="ms-2">— {tooltip.ru}</span>
        </div>
      )}
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
  const [readingDone, setReadingDone] = useState(false);
  const [levelFilter, setLevelFilter] = useUrlNumParam("level");

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
            <CardDescription>Наведите на подчёркнутые слова для перевода</CardDescription>
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
          <Button className="w-full" onClick={() => setReadingDone(true)}>
            Прочитано
          </Button>
        )}
        {readingDone && (
          <p className="text-center text-sm text-green-600 font-medium">Отмечено как прочитанное</p>
        )}

        {/* Cross-links */}
        <div className="flex flex-wrap gap-2">
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
              <CardTitle className="text-base">{text.title_ru}</CardTitle>
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
