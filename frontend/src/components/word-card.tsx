import type { WordBrief } from "@/hooks/use-words";
import { HebrewText } from "@/components/hebrew-text";
import { useTTS } from "@/components/tts-controls";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
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
};

const FREQ_COLORS: Record<number, string> = {
  1: "bg-green-100 text-green-800",
  2: "bg-yellow-100 text-yellow-800",
  3: "bg-orange-100 text-orange-800",
  4: "bg-red-100 text-red-800",
};

const FREQ_LABELS: Record<number, string> = {
  1: "высокая",
  2: "средняя",
  3: "низкая",
  4: "редкая",
};

interface WordCardProps {
  word: WordBrief;
  onClick?: () => void;
  onRootClick?: (root: string) => void;
  selected?: boolean;
}

export function WordCard({ word, onClick, onRootClick, selected }: WordCardProps) {
  const { speak } = useTTS();

  return (
    <Card
      className={cn(
        "cursor-pointer hover:shadow-md transition-shadow",
        selected && "ring-2 ring-primary"
      )}
      onClick={onClick}
    >
      <CardContent className="p-4">
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-1.5">
              <HebrewText size="xl" className="block font-bold" nikkud={word.nikkud}>
                {word.hebrew}
              </HebrewText>
              <button
                className="shrink-0 text-muted-foreground hover:text-primary transition-colors text-sm"
                onClick={(e) => { e.stopPropagation(); speak(word.hebrew); }}
                title="Прослушать"
              >
                ▶
              </button>
            </div>
            {word.transliteration && (
              <p className="text-sm text-muted-foreground mt-0.5">
                {word.transliteration}
              </p>
            )}
            <p className="text-sm mt-1 truncate">{word.translation_ru}</p>
          </div>
          <div className="flex flex-col items-end gap-1 shrink-0">
            {word.pos && (
              <Badge variant="secondary" className="text-xs">
                {POS_LABELS[word.pos] || word.pos}
              </Badge>
            )}
            {word.frequency_rank && (
              <span className={cn("text-xs px-1.5 py-0.5 rounded", FREQ_COLORS[word.frequency_rank])}>
                {FREQ_LABELS[word.frequency_rank]}
              </span>
            )}
          </div>
        </div>
        {word.root && (
          <button
            className="text-xs text-muted-foreground mt-2 hover:text-primary transition-colors"
            onClick={(e) => {
              e.stopPropagation();
              onRootClick?.(word.root!);
            }}
          >
            <HebrewText size="sm">{word.root}</HebrewText>
          </button>
        )}
      </CardContent>
    </Card>
  );
}
