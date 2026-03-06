import { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { useVerbs, useConjugations, useBinyanim } from "@/hooks/use-grammar";
import type { Conjugation } from "@/hooks/use-grammar";
import type { WordBrief } from "@/hooks/use-words";
import { HebrewText } from "@/components/hebrew-text";
import { useTTS } from "@/components/tts-controls";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { LEVEL_LABELS } from "@/lib/constants";

const FREQ_GROUPS: Record<number, string> = {
  1: "Частотные",
  2: "Средние",
  3: "Редкие",
  4: "Очень редкие",
};

const TENSE_ORDER = ["present", "past", "future", "imperative"] as const;
const TENSE_LABELS: Record<string, string> = {
  present: "Настоящее",
  past: "Прошедшее",
  future: "Будущее",
  imperative: "Повелительное",
};

const PERSON_NUMBER_LABELS: Record<string, string> = {
  "1-singular": "Я (ед.)",
  "2-singular": "Ты",
  "3-singular": "Он / Она",
  "1-plural": "Мы",
  "2-plural": "Вы",
  "3-plural": "Они",
};

// Present tense uses gender+number instead of person
const PRESENT_LABELS: Record<string, string> = {
  "masculine-singular": "Ед. муж.",
  "feminine-singular": "Ед. жен.",
  "masculine-plural": "Мн. муж.",
  "feminine-plural": "Мн. жен.",
};

function groupByFrequency(verbs: WordBrief[]) {
  const groups: Record<number, WordBrief[]> = {};
  for (const v of verbs) {
    const rank = v.frequency_rank ?? 4;
    if (!groups[rank]) groups[rank] = [];
    groups[rank].push(v);
  }
  return groups;
}

function SpeakButton({ text, className }: { text: string; className?: string }) {
  const { speak } = useTTS();
  return (
    <button
      type="button"
      onClick={(e) => { e.stopPropagation(); speak(text); }}
      className={cn("text-muted-foreground hover:text-foreground transition-colors", className)}
      title="Слушать"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none"
        stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
        <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
      </svg>
    </button>
  );
}

function TenseTable({ conjugations, tense }: { conjugations: Conjugation[]; tense: string }) {
  const forms = conjugations.filter((c) => c.tense === tense);
  if (forms.length === 0) return null;

  const isPresent = tense === "present";

  if (isPresent) {
    // Present tense: rows by gender+number
    const order = ["masculine-singular", "feminine-singular", "masculine-plural", "feminine-plural"];
    const formMap = new Map(forms.map((f) => [`${f.gender}-${f.number}`, f]));

    return (
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="border-b">
            <th className="p-2 text-left text-muted-foreground">Форма</th>
            <th className="p-2 text-right text-muted-foreground">Иврит</th>
            <th className="p-2 text-left text-muted-foreground">Транслит.</th>
            <th className="p-2 w-8" />
          </tr>
        </thead>
        <tbody>
          {order.map((key) => {
            const f = formMap.get(key);
            if (!f) return null;
            return (
              <tr key={key} className="border-b last:border-0">
                <td className="p-2 text-muted-foreground">{PRESENT_LABELS[key]}</td>
                <td className="p-2 text-right">
                  <HebrewText size="lg">{f.form_nikkud || f.form_he}</HebrewText>
                </td>
                <td className="p-2 text-muted-foreground">{f.transliteration || "—"}</td>
                <td className="p-2">
                  <SpeakButton text={f.form_he} />
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    );
  }

  // Past/Future/Imperative: rows by person+number, columns masc/fem
  const rowOrder = ["1-singular", "2-singular", "3-singular", "1-plural", "2-plural", "3-plural"];
  const rowMap = new Map<string, { m?: Conjugation; f?: Conjugation }>();
  for (const f of forms) {
    const key = `${f.person}-${f.number}`;
    if (!rowMap.has(key)) rowMap.set(key, {});
    const entry = rowMap.get(key)!;
    if (f.gender === "masculine" || f.gender === "m") entry.m = f;
    else if (f.gender === "feminine" || f.gender === "f") entry.f = f;
    else {
      // common gender — put in both
      entry.m = entry.m || f;
      entry.f = entry.f || f;
    }
  }

  return (
    <table className="w-full text-sm border-collapse">
      <thead>
        <tr className="border-b">
          <th className="p-2 text-left text-muted-foreground">Лицо</th>
          <th className="p-2 text-center text-muted-foreground">Муж.</th>
          <th className="p-2 text-center text-muted-foreground">Жен.</th>
        </tr>
      </thead>
      <tbody>
        {rowOrder.map((key) => {
          const row = rowMap.get(key);
          if (!row) return null;
          const renderForm = (f?: Conjugation) => {
            if (!f) return <td className="p-2 text-center text-muted-foreground">—</td>;
            return (
              <td className="p-2 text-center">
                <div className="flex items-center justify-center gap-1">
                  <div>
                    <HebrewText size="lg">{f.form_nikkud || f.form_he}</HebrewText>
                    {f.transliteration && (
                      <p className="text-xs text-muted-foreground">{f.transliteration}</p>
                    )}
                  </div>
                  <SpeakButton text={f.form_he} />
                </div>
              </td>
            );
          };
          return (
            <tr key={key} className="border-b last:border-0">
              <td className="p-2 text-muted-foreground text-xs">{PERSON_NUMBER_LABELS[key]}</td>
              {renderForm(row.m)}
              {renderForm(row.f)}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

function ConjugationView({ wordId, verb }: { wordId: number; verb: WordBrief }) {
  const { data: conjugations, isLoading } = useConjugations(wordId);
  const { data: binyanim } = useBinyanim();
  const [activeTense, setActiveTense] = useState<string>("present");
  const { speak } = useTTS();

  const binyanName = useMemo(() => {
    if (!conjugations?.length || !binyanim?.length) return null;
    const bid = conjugations[0].binyan_id;
    const b = binyanim.find((x) => x.id === bid);
    return b ? `${b.name_he} — ${b.name_ru}` : null;
  }, [conjugations, binyanim]);

  const availableTenses = useMemo(() => {
    if (!conjugations) return [];
    const tenses = new Set(conjugations.map((c) => c.tense));
    return TENSE_ORDER.filter((t) => tenses.has(t));
  }, [conjugations]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-48">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
      </div>
    );
  }

  if (!conjugations?.length) {
    return (
      <div className="text-center text-muted-foreground py-12">
        Нет данных о спряжении для этого глагола
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Verb header */}
      <div className="flex items-center gap-3 flex-wrap">
        <HebrewText size="2xl" nikkud={verb.nikkud} className="font-bold">
          {verb.hebrew}
        </HebrewText>
        <button type="button" onClick={() => speak(verb.hebrew)} className="hover:text-primary">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
            <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
            <path d="M19.07 4.93a10 10 0 0 1 0 14.14" />
          </svg>
        </button>
        <span className="text-lg text-muted-foreground">{verb.translation_ru}</span>
      </div>

      <div className="flex items-center gap-2 flex-wrap">
        {verb.transliteration && (
          <span className="text-sm text-muted-foreground">{verb.transliteration}</span>
        )}
        {verb.root && <Badge variant="outline">שורש: {verb.root}</Badge>}
        {binyanName && <Badge variant="secondary">{binyanName}</Badge>}
      </div>

      {/* Tense tabs */}
      <div className="flex gap-1 border-b overflow-x-auto">
        {availableTenses.map((t) => (
          <button
            key={t}
            className={cn(
              "px-3 py-2 text-sm font-medium border-b-2 transition-colors whitespace-nowrap",
              activeTense === t
                ? "border-primary text-primary"
                : "border-transparent text-muted-foreground hover:text-foreground"
            )}
            onClick={() => setActiveTense(t)}
          >
            {TENSE_LABELS[t]}
          </button>
        ))}
      </div>

      {/* Conjugation table */}
      <Card>
        <CardContent className="p-0">
          <TenseTable conjugations={conjugations} tense={activeTense} />
        </CardContent>
      </Card>

      {/* Link to drill */}
      <Button variant="outline" asChild>
        <Link to={`/conjugation-drill?word_id=${wordId}`}>
          Тренировать спряжение
        </Link>
      </Button>
    </div>
  );
}

export function VerbsPage() {
  const [levelFilter, setLevelFilter] = useState<number | undefined>();
  const [page, setPage] = useState(1);
  const { data, isLoading } = useVerbs({
    ...(levelFilter ? { level_id: levelFilter } : {}),
    page,
  });
  const [selectedId, setSelectedId] = useState<number | null>(null);

  const verbs = data?.items;
  const total = data?.total ?? 0;
  const totalPages = Math.ceil(total / 100);
  const selectedVerb = verbs?.find((v) => v.id === selectedId) ?? null;
  const grouped = useMemo(() => (verbs ? groupByFrequency(verbs) : {}), [verbs]);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Глаголы</h1>

      {/* Level filter */}
      <div className="flex gap-1 flex-wrap">
        <Button
          variant={levelFilter === undefined ? "default" : "outline"}
          size="sm"
          onClick={() => { setLevelFilter(undefined); setPage(1); }}
        >
          Все
        </Button>
        {Object.entries(LEVEL_LABELS).map(([id, label]) => (
          <Button
            key={id}
            variant={levelFilter === Number(id) ? "default" : "outline"}
            size="sm"
            onClick={() => { setLevelFilter(Number(id)); setPage(1); }}
          >
            {label}
          </Button>
        ))}
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center h-48">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary" />
        </div>
      ) : (
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Left: verb list */}
          <div className="lg:w-80 lg:shrink-0 lg:max-h-[calc(100vh-12rem)] lg:overflow-y-auto space-y-4">
            {[1, 2, 3, 4].map((rank) => {
              const group = grouped[rank];
              if (!group?.length) return null;
              return (
                <div key={rank}>
                  <h2 className="text-sm font-semibold text-muted-foreground mb-2">
                    {FREQ_GROUPS[rank]} ({group.length})
                  </h2>
                  <div className="space-y-0.5">
                    {group.map((v) => (
                      <button
                        key={v.id}
                        className={cn(
                          "w-full text-left rounded-md px-3 py-2 text-sm transition-colors hover:bg-accent",
                          selectedId === v.id && "bg-accent font-medium"
                        )}
                        onClick={() => setSelectedId(v.id)}
                      >
                        <div className="flex items-center gap-2">
                          <HebrewText size="md" nikkud={v.nikkud} className="font-medium shrink-0">
                            {v.hebrew}
                          </HebrewText>
                          {v.transliteration && (
                            <span className="text-muted-foreground text-xs truncate">
                              {v.transliteration}
                            </span>
                          )}
                        </div>
                        <div className="flex items-center gap-1.5 mt-0.5">
                          <span className="text-muted-foreground text-xs truncate">
                            {v.translation_ru}
                          </span>
                          {v.root && (
                            <Badge variant="outline" className="text-[10px] px-1 py-0 shrink-0">
                              {v.root}
                            </Badge>
                          )}
                        </div>
                      </button>
                    ))}
                  </div>
                </div>
              );
            })}
            {!verbs?.length && (
              <p className="text-muted-foreground text-center py-8">Глаголы не найдены</p>
            )}
            {totalPages > 1 && (
              <div className="flex items-center justify-between pt-2">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page <= 1}
                  onClick={() => setPage((p) => p - 1)}
                >
                  Назад
                </Button>
                <span className="text-xs text-muted-foreground">
                  {page} / {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={page >= totalPages}
                  onClick={() => setPage((p) => p + 1)}
                >
                  Далее
                </Button>
              </div>
            )}
          </div>

          {/* Right: conjugation view */}
          <div className="flex-1 min-w-0">
            {selectedVerb ? (
              <ConjugationView wordId={selectedVerb.id} verb={selectedVerb} />
            ) : (
              <Card>
                <CardContent className="flex items-center justify-center h-48 text-muted-foreground">
                  Выберите глагол из списка
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
