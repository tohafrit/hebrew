import { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import { useVerbs, useConjugations, useBinyanim } from "@/hooks/use-grammar";
import type { Conjugation } from "@/hooks/use-grammar";
import type { WordBrief } from "@/hooks/use-words";
import { HebrewText } from "@/components/hebrew-text";
import { useTTS } from "@/components/tts-controls";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { LEVEL_LABELS } from "@/lib/constants";

/* ── Constants ─────────────────────────────────────────────── */

const FREQ_LABELS: Record<string, string> = {
  "1": "Частотные",
  "2": "Средние",
  "3": "Редкие",
  "4": "Очень редкие",
};

const TENSE_ORDER = ["present", "past", "future", "imperative", "infinitive"] as const;
const TENSE_LABELS: Record<string, string> = {
  present: "Настоящее",
  past: "Прошедшее",
  future: "Будущее",
  imperative: "Повелительное",
  infinitive: "Инфинитив",
};

// DB person codes → human labels
const PERSON_LABEL: Record<string, string> = {
  "1s": "Я",
  "2ms": "Ты (м)",
  "2fs": "Ты (ж)",
  "3ms": "Он",
  "3fs": "Она",
  "1p": "Мы",
  "2mp": "Вы (м)",
  "2fp": "Вы (ж)",
  "3mp": "Они (м)",
  "3fp": "Они (ж)",
  "3p": "Они",
  "ms": "Муж. ед.",
  "fs": "Жен. ед.",
  "mp": "Муж. мн.",
  "fp": "Жен. мн.",
};

const PERSON_ORDER = [
  "1s", "2ms", "2fs", "3ms", "3fs",
  "1p", "2mp", "2fp", "3mp", "3fp", "3p",
  "ms", "fs", "mp", "fp",
  "-",
];

/* ── Conjugation table for one tense ──────────────────────── */

function TenseSection({ forms, tense }: { forms: Conjugation[]; tense: string }) {
  const { speak } = useTTS();

  if (!forms.length) return null;

  // Infinitive / single-form tenses
  if (tense === "infinitive" || forms.length <= 2) {
    return (
      <div className="space-y-1">
        {forms.map((f) => (
          <div key={f.id} className="flex items-center gap-3">
            <HebrewText size="lg" className="font-medium">
              {f.form_nikkud || f.form_he}
            </HebrewText>
            {f.transliteration && (
              <span className="text-sm text-muted-foreground">{f.transliteration}</span>
            )}
            <button
              type="button"
              onClick={() => speak(f.form_he)}
              className="text-muted-foreground hover:text-foreground"
              title="Слушать"
            >
              <SpeakerIcon size={14} />
            </button>
          </div>
        ))}
      </div>
    );
  }

  // Sort by person order
  const sorted = [...forms].sort(
    (a, b) => PERSON_ORDER.indexOf(a.person) - PERSON_ORDER.indexOf(b.person)
  );

  return (
    <div className="overflow-x-auto -mx-3">
      <table className="w-full text-sm">
        <tbody>
          {sorted.map((f) => (
            <tr key={f.id} className="border-b last:border-0 hover:bg-muted/50">
              <td className="px-3 py-1.5 text-muted-foreground w-24">
                {PERSON_LABEL[f.person] || f.person}
              </td>
              <td className="px-3 py-1.5 text-right" dir="rtl">
                <HebrewText size="md" className="font-medium">
                  {f.form_nikkud || f.form_he}
                </HebrewText>
              </td>
              <td className="px-3 py-1.5 text-muted-foreground text-xs">
                {f.transliteration || ""}
              </td>
              <td className="px-1 py-1.5 w-8">
                <button
                  type="button"
                  onClick={() => speak(f.form_he)}
                  className="text-muted-foreground hover:text-foreground p-0.5"
                >
                  <SpeakerIcon size={12} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function SpeakerIcon({ size = 16 }: { size?: number }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24"
      fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />
      <path d="M15.54 8.46a5 5 0 0 1 0 7.07" />
    </svg>
  );
}

/* ── Right panel: conjugation view ────────────────────────── */

function ConjugationView({ wordId, verb }: { wordId: number; verb: WordBrief }) {
  const { data: conjugations, isLoading } = useConjugations(wordId);
  const { data: binyanim } = useBinyanim();
  const { speak } = useTTS();

  const binyanName = useMemo(() => {
    if (!conjugations?.length || !binyanim?.length) return null;
    const bid = conjugations[0].binyan_id;
    const b = binyanim.find((x) => x.id === bid);
    return b ? `${b.name_he} — ${b.name_ru}` : null;
  }, [conjugations, binyanim]);

  const byTense = useMemo(() => {
    if (!conjugations) return {};
    const m: Record<string, Conjugation[]> = {};
    for (const c of conjugations) {
      if (!m[c.tense]) m[c.tense] = [];
      m[c.tense].push(c);
    }
    return m;
  }, [conjugations]);

  const tenses = TENSE_ORDER.filter((t) => byTense[t]?.length);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-16">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary" />
      </div>
    );
  }

  return (
    <div className="space-y-5">
      {/* Header */}
      <div>
        <div className="flex items-center gap-3">
          <HebrewText size="2xl" nikkud={verb.nikkud} className="font-bold">
            {verb.hebrew}
          </HebrewText>
          <button type="button" onClick={() => speak(verb.hebrew)}
            className="text-muted-foreground hover:text-foreground">
            <SpeakerIcon size={18} />
          </button>
        </div>
        <p className="text-muted-foreground mt-0.5">
          {verb.transliteration && <span>{verb.transliteration} · </span>}
          {verb.translation_ru}
        </p>
        <div className="flex gap-2 mt-2 flex-wrap">
          {verb.root && <Badge variant="outline">{verb.root}</Badge>}
          {binyanName && <Badge variant="secondary">{binyanName}</Badge>}
        </div>
      </div>

      {/* Conjugation tables — all tenses visible */}
      {tenses.length === 0 ? (
        <p className="text-muted-foreground text-sm py-4">
          Нет данных о спряжении
        </p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {tenses.map((t) => (
            <Card key={t}>
              <CardContent className="p-3">
                <h3 className="text-sm font-semibold mb-2">{TENSE_LABELS[t] || t}</h3>
                <TenseSection forms={byTense[t]} tense={t} />
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Drill link */}
      <Button variant="outline" size="sm" asChild>
        <Link to={`/conjugation-drill?word_id=${wordId}`}>
          Тренировать спряжение
        </Link>
      </Button>
    </div>
  );
}

/* ── Main page ────────────────────────────────────────────── */

export function VerbsPage() {
  const [levelFilter, setLevelFilter] = useState<string>("all");
  const [freqFilter, setFreqFilter] = useState<string>("all");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [selectedId, setSelectedId] = useState<number | null>(null);

  const levelId = levelFilter !== "all" ? Number(levelFilter) : undefined;
  const { data, isLoading } = useVerbs({
    ...(levelId ? { level_id: levelId } : {}),
    page,
  });

  const verbs = data?.items;
  const total = data?.total ?? 0;
  const totalPages = Math.ceil(total / 100);

  // Client-side filtering by search + frequency
  const filtered = useMemo(() => {
    if (!verbs) return [];
    let list = verbs;
    if (freqFilter !== "all") {
      const rank = Number(freqFilter);
      list = list.filter((v) => v.frequency_rank === rank);
    }
    if (search.trim()) {
      const q = search.trim().toLowerCase();
      list = list.filter(
        (v) =>
          v.hebrew.includes(q) ||
          v.translation_ru.toLowerCase().includes(q) ||
          (v.transliteration?.toLowerCase().includes(q)) ||
          (v.root?.includes(q))
      );
    }
    return list;
  }, [verbs, freqFilter, search]);

  const selectedVerb = verbs?.find((v) => v.id === selectedId) ?? null;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Глаголы</h1>

      {/* Filters row */}
      <div className="flex gap-2 flex-wrap items-center">
        <Input
          placeholder="Поиск..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-40 h-9"
        />
        <Select value={levelFilter} onValueChange={(v) => { setLevelFilter(v); setPage(1); }}>
          <SelectTrigger className="w-32 h-9">
            <SelectValue placeholder="Уровень" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Все уровни</SelectItem>
            {Object.entries(LEVEL_LABELS).map(([id, label]) => (
              <SelectItem key={id} value={id}>{label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select value={freqFilter} onValueChange={setFreqFilter}>
          <SelectTrigger className="w-36 h-9">
            <SelectValue placeholder="Частотность" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">Все частоты</SelectItem>
            {Object.entries(FREQ_LABELS).map(([id, label]) => (
              <SelectItem key={id} value={id}>{label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        {total > 0 && (
          <span className="text-xs text-muted-foreground ml-auto">
            {filtered.length} из {total}
          </span>
        )}
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-16">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary" />
        </div>
      ) : (
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Left: verb list */}
          <div className="lg:w-72 lg:shrink-0 space-y-1">
            <div className="lg:max-h-[calc(100vh-14rem)] lg:overflow-y-auto space-y-0.5 pr-1">
              {filtered.map((v) => (
                <button
                  key={v.id}
                  className={cn(
                    "w-full text-left rounded-md px-3 py-1.5 text-sm transition-colors hover:bg-accent",
                    selectedId === v.id && "bg-accent"
                  )}
                  onClick={() => setSelectedId(v.id)}
                >
                  <span className="flex items-baseline gap-2">
                    <HebrewText size="md" nikkud={v.nikkud} className="shrink-0">
                      {v.hebrew}
                    </HebrewText>
                    <span className="text-muted-foreground text-xs truncate">
                      {v.translation_ru}
                    </span>
                  </span>
                </button>
              ))}
              {filtered.length === 0 && (
                <p className="text-muted-foreground text-center text-sm py-8">
                  Глаголы не найдены
                </p>
              )}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex items-center justify-between pt-2">
                <Button variant="ghost" size="sm" disabled={page <= 1}
                  onClick={() => setPage((p) => p - 1)}>
                  &larr;
                </Button>
                <span className="text-xs text-muted-foreground">{page} / {totalPages}</span>
                <Button variant="ghost" size="sm" disabled={page >= totalPages}
                  onClick={() => setPage((p) => p + 1)}>
                  &rarr;
                </Button>
              </div>
            )}
          </div>

          {/* Right: conjugation */}
          <div className="flex-1 min-w-0">
            {selectedVerb ? (
              <ConjugationView wordId={selectedVerb.id} verb={selectedVerb} />
            ) : (
              <div className="text-center text-muted-foreground py-16 text-sm">
                Выберите глагол из списка
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
