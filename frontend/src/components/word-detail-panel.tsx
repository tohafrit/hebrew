import { useState } from "react";
import { Link } from "react-router-dom";
import { useWord } from "@/hooks/use-words";
import { useConjugations } from "@/hooks/use-grammar";
import { useCreateCards } from "@/hooks/use-srs";
import { HebrewText } from "@/components/hebrew-text";
import { TTSControls } from "@/components/tts-controls";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { toast } from "@/hooks/use-toast";

const POS_LABELS: Record<string, string> = {
  noun: "Существительное",
  verb: "Глагол",
  adj: "Прилагательное",
  adv: "Наречие",
  prep: "Предлог",
  conj: "Союз",
  pron: "Местоимение",
  num: "Числительное",
  particle: "Частица",
  interj: "Междометие",
};

const TENSE_LABELS: Record<string, string> = {
  past: "Прошедшее",
  present: "Настоящее",
  future: "Будущее",
  imperative: "Повелительное",
};

const PERSON_LABELS: Record<string, string> = {
  "1s": "я",
  "2ms": "ты (м)",
  "2fs": "ты (ж)",
  "3ms": "он",
  "3fs": "она",
  "1p": "мы",
  "2mp": "вы (м)",
  "2fp": "вы (ж)",
  "3mp": "они (м)",
  "3fp": "они (ж)",
  ms: "м.р. ед.ч.",
  fs: "ж.р. ед.ч.",
  mp: "м.р. мн.ч.",
  fp: "ж.р. мн.ч.",
};

function ConjugationTable({ wordId }: { wordId: number }) {
  const { data: conjugations } = useConjugations(wordId);
  const [activeTense, setActiveTense] = useState("present");

  if (!conjugations || conjugations.length === 0) return null;

  const tenses = [...new Set(conjugations.map((c) => c.tense))];
  const filtered = conjugations.filter((c) => c.tense === activeTense);

  return (
    <div>
      <h4 className="text-sm font-semibold mb-2">Спряжение</h4>
      <div className="flex gap-1 mb-2 flex-wrap">
        {tenses.map((t) => (
          <button
            key={t}
            className={cn(
              "text-xs px-2 py-1 rounded-md transition-colors",
              activeTense === t
                ? "bg-primary text-primary-foreground"
                : "bg-muted hover:bg-accent"
            )}
            onClick={() => setActiveTense(t)}
          >
            {TENSE_LABELS[t] || t}
          </button>
        ))}
      </div>
      <div className="space-y-0.5">
        {filtered.map((c) => (
          <div key={c.id} className="flex items-center gap-2 text-sm">
            <span className="text-xs text-muted-foreground w-16 shrink-0">
              {PERSON_LABELS[c.person] || c.person}
            </span>
            <HebrewText size="sm" className="font-medium">
              {c.form_he}
            </HebrewText>
            {c.transliteration && (
              <span className="text-xs text-muted-foreground">
                {c.transliteration}
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

interface WordDetailPanelProps {
  wordId: number;
  onClose: () => void;
}

export function WordDetailPanel({ wordId, onClose }: WordDetailPanelProps) {
  const { data: word, isLoading } = useWord(wordId);
  const createCards = useCreateCards();

  if (isLoading) {
    return (
      <Card>
        <CardContent className="p-6 text-center text-muted-foreground">
          Загрузка...
        </CardContent>
      </Card>
    );
  }

  if (!word) return null;

  const hasExamples = word.examples.length > 0;

  const handleAddToSRS = async () => {
    try {
      const result = await createCards.mutateAsync({ word_ids: [word.id] });
      const desc = hasExamples
        ? `Создано ${result.created} карточек (включая предложения)`
        : `Создано ${result.created} карточек`;
      toast({
        title: "Добавлено в карточки",
        description: desc,
      });
    } catch {
      toast({
        title: "Ошибка",
        description: "Не удалось создать карточки",
        variant: "destructive",
      });
    }
  };

  return (
    <Card>
      <CardHeader className="flex flex-row items-start justify-between">
        <div className="space-y-1">
          <HebrewText size="2xl" className="block font-bold">
            {word.hebrew}
          </HebrewText>
          {word.transliteration && (
            <p className="text-muted-foreground">{word.transliteration}</p>
          )}
          <TTSControls text={word.hebrew} size="sm" />
        </div>
        <Button variant="ghost" size="sm" onClick={onClose}>
          &times;
        </Button>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <p className="text-lg">{word.translation_ru}</p>
          <div className="flex gap-2 mt-2 flex-wrap">
            {word.pos && (
              <Badge variant="secondary">
                {POS_LABELS[word.pos] || word.pos}
              </Badge>
            )}
            {word.gender && <Badge variant="outline">{word.gender}</Badge>}
            {word.number && <Badge variant="outline">{word.number}</Badge>}
          </div>
        </div>

        {word.root && (
          <div>
            <h4 className="text-sm font-semibold mb-1">Корень</h4>
            <HebrewText size="lg">{word.root}</HebrewText>
          </div>
        )}

        {word.root_family && word.root_family.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold mb-2">Однокоренные слова</h4>
            <div className="space-y-1">
              {word.root_family.map((w) => (
                <Link
                  key={w.id}
                  to={`/dictionary?search=${encodeURIComponent(w.hebrew)}`}
                  className="flex items-center gap-2 text-sm hover:bg-accent rounded px-1 py-0.5 -mx-1 transition-colors"
                >
                  <HebrewText size="sm" className="font-medium">
                    {w.hebrew}
                  </HebrewText>
                  <span className="text-muted-foreground">—</span>
                  <span>{w.translation_ru}</span>
                </Link>
              ))}
            </div>
          </div>
        )}

        {word.forms.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold mb-2">Формы</h4>
            <div className="space-y-1">
              {word.forms.map((f) => (
                <div key={f.id} className="flex items-center gap-2 text-sm">
                  <Badge variant="outline" className="text-xs">
                    {f.form_type}
                  </Badge>
                  <HebrewText size="sm">{f.hebrew}</HebrewText>
                  {f.transliteration && (
                    <span className="text-muted-foreground">
                      {f.transliteration}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {word.pos === "verb" && <ConjugationTable wordId={word.id} />}

        {word.examples.length > 0 && (
          <div>
            <h4 className="text-sm font-semibold mb-2">Примеры</h4>
            <div className="space-y-2">
              {word.examples.map((ex) => (
                <div key={ex.id} className="text-sm border-s-2 ps-3">
                  <HebrewText className="block">{ex.hebrew}</HebrewText>
                  <p className="text-muted-foreground">{ex.translation_ru}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="space-y-2">
          <Button onClick={handleAddToSRS} className="w-full" disabled={createCards.isPending}>
            {createCards.isPending ? "Добавление..." : "Добавить в SRS-карточки"}
          </Button>
          <div className="flex gap-2">
            {word.pos === "verb" && (
              <Button variant="outline" size="sm" className="flex-1" asChild>
                <Link to="/grammar?tab=topics">Грамматика</Link>
              </Button>
            )}
            {word.level_id && (
              <Button variant="outline" size="sm" className="flex-1" asChild>
                <Link to={`/reading?level=${word.level_id}`}>Тексты</Link>
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
