import { useState, useRef, useCallback } from "react";
import { Link } from "react-router-dom";
import { useAnalyzeText, type TokenAnnotation } from "@/hooks/use-reader";
import { useCreateCards } from "@/hooks/use-srs";
import { HebrewText } from "@/components/hebrew-text";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { toast } from "@/hooks/use-toast";
import { cn } from "@/lib/utils";

const POS_LABELS: Record<string, string> = {
  noun: "сущ.",
  verb: "гл.",
  adj: "прил.",
  adv: "нар.",
  prep: "предл.",
  conj: "союз",
  pron: "мест.",
  num: "числ.",
  particle: "част.",
  interj: "межд.",
  phrase: "выр.",
};

const MATCH_LABELS: Record<string, string> = {
  exact: "словарь",
  form: "форма",
  conjugation: "спряжение",
  prefix: "с приставкой",
  number: "число",
  proper_noun: "имя собств.",
};

const LEVEL_LABELS: Record<number, string> = {
  1: "א A1",
  2: "ב A2",
  3: "ג B1",
  4: "ד B2",
  5: "ה C1",
  6: "ו C2",
};

const LEVEL_COLORS: Record<number, string> = {
  1: "bg-green-100 text-green-800",
  2: "bg-blue-100 text-blue-800",
  3: "bg-yellow-100 text-yellow-800",
  4: "bg-orange-100 text-orange-800",
  5: "bg-red-100 text-red-800",
  6: "bg-purple-100 text-purple-800",
};

const SAMPLE_TEXTS = [
  {
    label: "Берешит 1:1-3",
    text: `בראשית ברא אלוהים את השמיים ואת הארץ. והארץ הייתה תוהו ובוהו, וחושך על פני תהום, ורוח אלוהים מרחפת על פני המים. ויאמר אלוהים יהי אור, ויהי אור.`,
  },
  {
    label: "Новости",
    text: `ממשלת ישראל אישרה היום תוכנית חדשה לפיתוח הנגב. התוכנית כוללת השקעה של מיליארד שקלים בתשתיות, חינוך ותעסוקה. ראש הממשלה אמר כי מדובר בצעד חשוב לעתיד המדינה.`,
  },
  {
    label: "Разговорный",
    text: `היי, מה נשמע? רציתי לשאול אותך משהו. אתה רוצה לבוא איתי לקניון מחר? יש שם מבצעים טובים ואני צריך לקנות מתנה ליום הולדת של אמא שלי.`,
  },
];

// ── Inline hover tooltip ──────────────────────────────────────────────────

function AnnotatedWord({ token, isSelected, onSelect, onHover, onLeave }: {
  token: TokenAnnotation;
  isSelected: boolean;
  onSelect: (token: TokenAnnotation) => void;
  onHover: (token: TokenAnnotation, el: HTMLElement) => void;
  onLeave: () => void;
}) {
  const isKnown = token.word_id !== null;
  const isNumber = token.match_type === "number";
  const isProperNoun = token.match_type === "proper_noun";
  const isSpecial = isNumber || isProperNoun;

  return (
    <span
      className={cn(
        "font-hebrew cursor-pointer transition-all duration-150 rounded px-0.5 relative",
        isKnown
          ? "border-b-2 border-dashed border-primary/40 hover:border-primary hover:bg-primary/10"
          : isSpecial
            ? "text-muted-foreground/90 hover:bg-muted/50"
            : "text-muted-foreground/70 hover:text-foreground hover:bg-muted",
        isProperNoun && "italic",
        isSelected && "bg-primary/20 border-primary"
      )}
      onClick={() => onSelect(token)}
      onMouseEnter={(e) => onHover(token, e.currentTarget)}
      onMouseLeave={onLeave}
    >
      {token.token}
    </span>
  );
}

function InlineTooltip({ token, style }: {
  token: TokenAnnotation;
  style: React.CSSProperties;
}) {
  if (!token.word_id) {
    const isNumber = token.match_type === "number";
    const isProperNoun = token.match_type === "proper_noun";
    return (
      <div
        className="absolute z-50 bg-popover border rounded-lg shadow-lg p-3 text-sm max-w-[250px]"
        style={style}
      >
        <HebrewText size="sm" className={cn("font-bold block", isProperNoun && "italic")}>
          {token.clean}
        </HebrewText>
        <p className="text-muted-foreground text-xs mt-1">
          {isNumber ? "מספר (число)" : isProperNoun ? "שם פרטי (имя собств.)" : "Не найдено в словаре"}
        </p>
      </div>
    );
  }

  return (
    <div
      className="absolute z-50 bg-popover border rounded-lg shadow-lg p-3 text-sm max-w-[280px]"
      style={style}
    >
      <div className="flex items-start gap-2 justify-between">
        <HebrewText size="lg" className="font-bold">{token.hebrew}</HebrewText>
        {token.pos && (
          <span className="text-xs text-muted-foreground shrink-0">
            {POS_LABELS[token.pos] || token.pos}
          </span>
        )}
      </div>
      <p className="font-medium mt-0.5">{token.translation_ru}</p>
      {token.transliteration && (
        <p className="text-xs text-muted-foreground">{token.transliteration}</p>
      )}
      <div className="flex gap-2 mt-1 text-xs text-muted-foreground">
        {token.root && (
          <span>
            <HebrewText size="sm">{token.root}</HebrewText>
          </span>
        )}
        {token.match_type && token.match_type !== "exact" && (
          <span className="text-primary/70">{MATCH_LABELS[token.match_type]}</span>
        )}
      </div>
    </div>
  );
}

// ── Sidebar detail panel ──────────────────────────────────────────────────

function WordDetailSidebar({ token }: { token: TokenAnnotation }) {
  if (!token.word_id) {
    const isNumber = token.match_type === "number";
    const isProperNoun = token.match_type === "proper_noun";
    return (
      <Card>
        <CardContent className="p-4 text-center">
          <HebrewText size="xl" className={cn("block font-bold mb-1", isProperNoun && "italic")}>
            {token.clean}
          </HebrewText>
          <p className="text-sm text-muted-foreground">
            {isNumber ? "מספר (число)" : isProperNoun ? "שם פרטי (имя собственное)" : "Слово не найдено в словаре"}
          </p>
          {!isNumber && !isProperNoun && (
            <Button variant="outline" size="sm" className="mt-2" asChild>
              <Link to={`/dictionary?search=${encodeURIComponent(token.clean)}`}>
                Искать в словаре
              </Link>
            </Button>
          )}
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-3">
          <div>
            <HebrewText size="2xl" className="block font-bold">
              {token.hebrew}
            </HebrewText>
            {token.transliteration && (
              <p className="text-sm text-muted-foreground">{token.transliteration}</p>
            )}
          </div>
          <div className="flex flex-col items-end gap-1">
            {token.pos && (
              <Badge variant="secondary" className="text-xs">
                {POS_LABELS[token.pos] || token.pos}
              </Badge>
            )}
            {token.match_type && (
              <Badge variant="outline" className="text-xs">
                {MATCH_LABELS[token.match_type] || token.match_type}
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <p className="text-lg">{token.translation_ru}</p>

        <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
          {token.root && (
            <span>
              Корень: <HebrewText size="sm" className="font-medium">{token.root}</HebrewText>
            </span>
          )}
          {token.level_id && (
            <Badge variant="outline" className={cn("text-xs", LEVEL_COLORS[token.level_id])}>
              {LEVEL_LABELS[token.level_id]}
            </Badge>
          )}
        </div>

        <div className="flex gap-2">
          <Button variant="outline" size="sm" className="flex-1" asChild>
            <Link to={`/dictionary?search=${encodeURIComponent(token.hebrew!)}`}>
              Словарь
            </Link>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

// ── Stats breakdown ───────────────────────────────────────────────────────

function StatsBreakdown({ tokens }: { tokens: TokenAnnotation[] }) {
  const wordTokens = tokens.filter((t) => !t.is_space && t.clean);
  const known = wordTokens.filter((t) => t.word_id !== null || t.match_type === "number" || t.match_type === "proper_noun");
  const unknown = wordTokens.filter((t) => t.word_id === null && t.match_type !== "number" && t.match_type !== "proper_noun");

  // Count by level
  const byLevel: Record<number, number> = {};
  known.forEach((t) => {
    if (t.level_id) {
      byLevel[t.level_id] = (byLevel[t.level_id] || 0) + 1;
    }
  });

  // Count by match type
  const byMatch: Record<string, number> = {};
  known.forEach((t) => {
    if (t.match_type) {
      byMatch[t.match_type] = (byMatch[t.match_type] || 0) + 1;
    }
  });

  // Unique unknown words
  const uniqueUnknown = [...new Set(unknown.map((t) => t.clean))];

  return (
    <div className="space-y-3">
      {/* Level distribution */}
      {Object.keys(byLevel).length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-muted-foreground mb-1">По уровням</h4>
          <div className="flex flex-wrap gap-1">
            {Object.entries(byLevel)
              .sort(([a], [b]) => Number(a) - Number(b))
              .map(([lvl, count]) => (
                <Badge key={lvl} variant="outline" className={cn("text-xs", LEVEL_COLORS[Number(lvl)])}>
                  {LEVEL_LABELS[Number(lvl)]}: {count}
                </Badge>
              ))}
          </div>
        </div>
      )}

      {/* Match types */}
      {Object.keys(byMatch).length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-muted-foreground mb-1">Тип совпадения</h4>
          <div className="flex flex-wrap gap-1">
            {Object.entries(byMatch).map(([type, count]) => (
              <Badge key={type} variant="outline" className="text-xs">
                {MATCH_LABELS[type] || type}: {count}
              </Badge>
            ))}
          </div>
        </div>
      )}

      {/* Unknown words list */}
      {uniqueUnknown.length > 0 && (
        <div>
          <h4 className="text-xs font-medium text-muted-foreground mb-1">
            Неизвестные слова ({uniqueUnknown.length})
          </h4>
          <div className="flex flex-wrap gap-1" dir="rtl">
            {uniqueUnknown.slice(0, 30).map((w, i) => (
              <Link
                key={i}
                to={`/dictionary?search=${encodeURIComponent(w)}`}
                className="text-xs px-1.5 py-0.5 rounded bg-muted hover:bg-accent transition-colors font-hebrew"
              >
                {w}
              </Link>
            ))}
            {uniqueUnknown.length > 30 && (
              <span className="text-xs text-muted-foreground">
                +{uniqueUnknown.length - 30}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

// ── Main page ─────────────────────────────────────────────────────────────

type Tab = "input" | "results";

export function ReaderPage() {
  const [text, setText] = useState("");
  const analyze = useAnalyzeText();
  const createCards = useCreateCards();
  const [selectedToken, setSelectedToken] = useState<TokenAnnotation | null>(null);
  const [hoverToken, setHoverToken] = useState<TokenAnnotation | null>(null);
  const [hoverStyle, setHoverStyle] = useState<React.CSSProperties>({});
  const [showStats, setShowStats] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleAnalyze = () => {
    if (text.trim()) {
      analyze.mutate(text);
      setSelectedToken(null);
    }
  };

  const handleClear = () => {
    setText("");
    analyze.reset();
    setSelectedToken(null);
    setHoverToken(null);
    setShowStats(false);
  };

  const handleFileUpload = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (evt) => {
      const content = evt.target?.result as string;
      setText(content);
    };
    reader.readAsText(file);
    // Reset file input so same file can be selected again
    e.target.value = "";
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && (file.type === "text/plain" || file.name.endsWith(".txt"))) {
      const reader = new FileReader();
      reader.onload = (evt) => {
        setText(evt.target?.result as string);
      };
      reader.readAsText(file);
    }
  }, []);

  const handleHover = useCallback((token: TokenAnnotation, el: HTMLElement) => {
    if (!containerRef.current) return;
    const containerRect = containerRef.current.getBoundingClientRect();
    const elRect = el.getBoundingClientRect();

    // Position tooltip below the word
    setHoverStyle({
      top: elRect.bottom - containerRect.top + 4,
      right: containerRect.right - elRect.right,
    });
    setHoverToken(token);
  }, []);

  const handleAddKnownToSRS = async () => {
    if (!analyze.data) return;
    const wordIds = [
      ...new Set(
        analyze.data.tokens
          .filter((t) => t.word_id !== null)
          .map((t) => t.word_id as number)
      ),
    ];
    if (wordIds.length === 0) return;

    try {
      const result = await createCards.mutateAsync({ word_ids: wordIds });
      toast({
        title: "Добавлено в SRS",
        description: `Создано ${result.created} карточек из ${wordIds.length} слов`,
      });
    } catch {
      toast({
        title: "Ошибка",
        description: "Не удалось создать карточки",
        variant: "destructive",
      });
    }
  };

  const tokens = analyze.data?.tokens;
  const stats = analyze.data?.stats;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Интерактивный чтец</h1>
        <p className="text-muted-foreground text-sm mt-1">
          Вставьте или загрузите текст на иврите — наведите на слово, чтобы увидеть перевод
        </p>
      </div>

      {/* Input area */}
      {!tokens && (
        <div className="space-y-3">
          <div
            className="relative"
            onDrop={handleDrop}
            onDragOver={(e) => e.preventDefault()}
          >
            <textarea
              ref={textareaRef}
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Вставьте текст на иврите или перетащите .txt файл..."
              className="w-full min-h-[200px] p-4 rounded-lg border bg-background text-lg leading-loose font-hebrew resize-y"
              dir="rtl"
            />
          </div>

          <div className="flex items-center gap-2 flex-wrap">
            <Button
              onClick={handleAnalyze}
              disabled={!text.trim() || analyze.isPending}
            >
              {analyze.isPending ? "Анализ..." : "Анализировать"}
            </Button>

            <Button
              variant="outline"
              onClick={() => fileInputRef.current?.click()}
            >
              Загрузить файл
            </Button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".txt,text/plain"
              onChange={handleFileUpload}
              className="hidden"
            />

            <div className="flex gap-1 ml-auto">
              {SAMPLE_TEXTS.map((s, i) => (
                <Button
                  key={i}
                  variant="ghost"
                  size="sm"
                  onClick={() => setText(s.text)}
                >
                  {s.label}
                </Button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {tokens && (
        <>
          {/* Stats bar */}
          {stats && (
            <div className="flex items-center gap-4 flex-wrap">
              <div className="flex items-center gap-4">
                <span className="text-sm">
                  <strong>{stats.known_count}</strong>
                  <span className="text-muted-foreground"> известных</span>
                </span>
                <span className="text-sm">
                  <strong>{stats.unknown_count}</strong>
                  <span className="text-muted-foreground"> неизвестных</span>
                </span>
                {stats.total_words > 0 && (
                  <Badge
                    variant="secondary"
                    className={cn(
                      "text-sm",
                      stats.known_count / stats.total_words >= 0.8
                        ? "bg-green-100 text-green-800"
                        : stats.known_count / stats.total_words >= 0.5
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-red-100 text-red-800"
                    )}
                  >
                    {Math.round((stats.known_count / stats.total_words) * 100)}%
                  </Badge>
                )}
              </div>

              <div className="flex gap-1 ml-auto">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowStats(!showStats)}
                >
                  {showStats ? "Скрыть" : "Подробнее"}
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleAddKnownToSRS}
                  disabled={createCards.isPending}
                >
                  В SRS
                </Button>
                <Button variant="outline" size="sm" onClick={handleClear}>
                  Новый текст
                </Button>
              </div>
            </div>
          )}

          {/* Stats breakdown */}
          {showStats && tokens && (
            <Card>
              <CardContent className="p-4">
                <StatsBreakdown tokens={tokens} />
              </CardContent>
            </Card>
          )}

          <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
            {/* Annotated text */}
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-base">Текст</CardTitle>
                <CardDescription>
                  Наведите на слово для быстрого перевода, нажмите — подробности справа
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="relative" ref={containerRef}>
                  <div className="leading-loose text-xl" dir="rtl">
                    {tokens.map((t, i) => {
                      if (t.is_space) {
                        if (t.token.includes("\n")) {
                          return <br key={i} />;
                        }
                        return <span key={i}>{t.token}</span>;
                      }
                      if (!t.clean) {
                        return <span key={i} className="font-hebrew">{t.token}</span>;
                      }
                      return (
                        <AnnotatedWord
                          key={i}
                          token={t}
                          isSelected={selectedToken === t}
                          onSelect={setSelectedToken}
                          onHover={handleHover}
                          onLeave={() => setHoverToken(null)}
                        />
                      );
                    })}
                  </div>

                  {/* Inline hover tooltip */}
                  {hoverToken && hoverToken.clean && (
                    <InlineTooltip token={hoverToken} style={hoverStyle} />
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Word detail sidebar */}
            <div className="lg:sticky lg:top-20 lg:self-start">
              {selectedToken && selectedToken.clean ? (
                <WordDetailSidebar token={selectedToken} />
              ) : (
                <Card>
                  <CardContent className="p-8 text-center text-muted-foreground text-sm">
                    Нажмите на слово в тексте для подробностей
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
