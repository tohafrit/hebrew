import { useState, useRef } from "react";
import { Link } from "react-router-dom";
import { useAnalyzeText, type TokenAnnotation } from "@/hooks/use-reader";
import { HebrewText } from "@/components/hebrew-text";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
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
};

const LEVEL_LABELS: Record<number, string> = {
  1: "א",
  2: "ב",
  3: "ג",
  4: "ד",
  5: "ה",
  6: "ו",
};

const SAMPLE_TEXT = `בראשית ברא אלוהים את השמיים ואת הארץ. והארץ הייתה תוהו ובוהו, וחושך על פני תהום, ורוח אלוהים מרחפת על פני המים. ויאמר אלוהים יהי אור, ויהי אור.`;

function AnnotatedWord({ token, onSelect }: {
  token: TokenAnnotation;
  onSelect: (token: TokenAnnotation) => void;
}) {
  const isKnown = token.word_id !== null;

  return (
    <span
      className={cn(
        "font-hebrew cursor-pointer transition-all duration-150 rounded px-0.5",
        isKnown
          ? "border-b-2 border-dashed border-primary/40 hover:border-primary hover:bg-primary/10"
          : "text-muted-foreground/70 hover:text-foreground hover:bg-muted"
      )}
      onClick={() => onSelect(token)}
    >
      {token.token}
    </span>
  );
}

function WordTooltip({ token }: { token: TokenAnnotation }) {
  if (!token.word_id) {
    return (
      <Card>
        <CardContent className="p-4 text-center">
          <HebrewText size="xl" className="block font-bold mb-1">{token.clean}</HebrewText>
          <p className="text-sm text-muted-foreground">Слово не найдено в словаре</p>
          <Button variant="outline" size="sm" className="mt-2" asChild>
            <Link to={`/dictionary?search=${encodeURIComponent(token.clean)}`}>
              Искать в словаре
            </Link>
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-3">
          <div>
            <HebrewText size="xl" className="block font-bold">
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
      <CardContent className="space-y-2">
        <p className="text-lg">{token.translation_ru}</p>

        <div className="flex flex-wrap gap-2 text-xs text-muted-foreground">
          {token.root && (
            <span>
              Корень: <HebrewText size="sm" className="font-medium">{token.root}</HebrewText>
            </span>
          )}
          {token.level_id && (
            <span>Ур. {LEVEL_LABELS[token.level_id]}</span>
          )}
        </div>

        <div className="flex gap-2 pt-1">
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

export function ReaderPage() {
  const [text, setText] = useState("");
  const analyze = useAnalyzeText();
  const [selectedToken, setSelectedToken] = useState<TokenAnnotation | null>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleAnalyze = () => {
    if (text.trim()) {
      analyze.mutate(text);
      setSelectedToken(null);
    }
  };

  const handleUseSample = () => {
    setText(SAMPLE_TEXT);
  };

  const handleClear = () => {
    setText("");
    analyze.reset();
    setSelectedToken(null);
  };

  const tokens = analyze.data?.tokens;
  const stats = analyze.data?.stats;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Интерактивный чтец</h1>
        <p className="text-muted-foreground text-sm mt-1">
          Вставьте любой текст на иврите — система найдёт знакомые слова и покажет перевод
        </p>
      </div>

      {/* Input area */}
      {!tokens && (
        <div className="space-y-3">
          <textarea
            ref={textareaRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Вставьте текст на иврите..."
            className="w-full min-h-[200px] p-4 rounded-lg border bg-background text-lg leading-loose font-hebrew resize-y"
            dir="rtl"
          />
          <div className="flex gap-2">
            <Button
              onClick={handleAnalyze}
              disabled={!text.trim() || analyze.isPending}
            >
              {analyze.isPending ? "Анализ..." : "Анализировать"}
            </Button>
            <Button variant="outline" onClick={handleUseSample}>
              Пример
            </Button>
          </div>
        </div>
      )}

      {/* Results */}
      {tokens && (
        <>
          {/* Stats bar */}
          {stats && (
            <div className="flex items-center gap-4 flex-wrap">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-primary/50" />
                <span className="text-sm">
                  Известных: <strong>{stats.known_count}</strong>
                </span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-muted-foreground/30" />
                <span className="text-sm">
                  Неизвестных: <strong>{stats.unknown_count}</strong>
                </span>
              </div>
              <span className="text-sm text-muted-foreground">
                {stats.total_words > 0
                  ? `${Math.round((stats.known_count / stats.total_words) * 100)}% понимание`
                  : ""}
              </span>
              <Button variant="outline" size="sm" onClick={handleClear} className="ml-auto">
                Новый текст
              </Button>
            </div>
          )}

          <div className="grid gap-6 lg:grid-cols-[1fr_320px]">
            {/* Annotated text */}
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-base">Текст</CardTitle>
                <CardDescription>
                  Нажмите на слово для перевода
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="leading-loose text-xl" dir="rtl">
                  {tokens.map((t, i) => {
                    if (t.is_space) {
                      // Preserve newlines
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
                        onSelect={setSelectedToken}
                      />
                    );
                  })}
                </div>
              </CardContent>
            </Card>

            {/* Word detail sidebar */}
            <div className="lg:sticky lg:top-20 lg:self-start">
              {selectedToken && selectedToken.clean ? (
                <WordTooltip token={selectedToken} />
              ) : (
                <Card>
                  <CardContent className="p-8 text-center text-muted-foreground">
                    Нажмите на слово в тексте
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
