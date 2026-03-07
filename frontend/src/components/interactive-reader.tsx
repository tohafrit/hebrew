import { useState, useCallback, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import { HebrewText } from "@/components/hebrew-text";
import { Button } from "@/components/ui/button";
import { useTTS } from "@/components/tts-controls";
import { useCreateCards } from "@/hooks/use-srs";
import api from "@/lib/api";

interface VocabEntry {
  he: string;
  ru: string;
  translit?: string;
}

interface WordInfo {
  hebrew: string;
  translation_ru: string;
  transliteration: string | null;
  nikkud: string | null;
  pos: string | null;
  id: number | null;
}

const NIKKUD_RE = /[\u0591-\u05C7]/g;
const stripNikkud = (s: string) => s.replace(NIKKUD_RE, "");

// Remove matres lectionis (ו, י used as vowels) to get consonantal skeleton
// This helps match defective spelling "לאכל" with plene "לאכול"
const toSkeleton = (s: string) => stripNikkud(s).replace(/[וי]/g, "");

// Cache for word lookups to avoid repeated API calls
const wordCache = new Map<string, WordInfo | null>();

function toWordInfo(w: any): WordInfo {
  return {
    hebrew: w.hebrew,
    translation_ru: w.translation_ru,
    transliteration: w.transliteration,
    nikkud: w.nikkud,
    pos: w.pos,
    id: w.id,
  };
}

async function lookupWord(hebrew: string): Promise<WordInfo | null> {
  const clean = stripNikkud(hebrew);
  if (wordCache.has(clean)) return wordCache.get(clean)!;

  try {
    // 1. Try /words/lookup — checks words, forms, AND conjugations
    // Send original (with nikkud) so backend can disambiguate homographs
    const { data: lookup } = await api.get("/words/lookup", { params: { q: hebrew } });
    if (lookup && lookup.word_id) {
      const info: WordInfo = {
        hebrew: lookup.hebrew,
        translation_ru: lookup.translation_ru,
        transliteration: lookup.transliteration,
        nikkud: null,
        pos: lookup.pos,
        id: lookup.word_id,
      };
      wordCache.set(clean, info);
      return info;
    }
  } catch { /* ignore */ }

  try {
    // 2. Fallback: search /words for skeleton match (handles defective/plene spelling)
    const { data } = await api.get("/words", { params: { search: clean, per_page: 20 } });
    if (data.items && data.items.length > 0) {
      const exact = data.items.find((w: any) => stripNikkud(w.hebrew) === clean);
      if (exact) {
        const info = toWordInfo(exact);
        wordCache.set(clean, info);
        return info;
      }
      const skeleton = toSkeleton(clean);
      const skelMatch = data.items.find((w: any) => toSkeleton(w.hebrew) === skeleton);
      if (skelMatch) {
        const info = toWordInfo(skelMatch);
        wordCache.set(clean, info);
        return info;
      }
    }
  } catch { /* ignore */ }

  wordCache.set(clean, null);
  return null;
}

function WordTooltip({ word, vocabEntry, onClose }: {
  word: string;
  vocabEntry?: VocabEntry;
  onClose: () => void;
}) {
  const { speak } = useTTS();
  const [info, setInfo] = useState<WordInfo | null>(null);
  const [loading, setLoading] = useState(false);
  const [looked, setLooked] = useState(false);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const createCards = useCreateCards();
  const [srsAdded, setSrsAdded] = useState(false);

  // If we have a vocab entry, use it directly
  const hasVocab = !!vocabEntry;

  // Always look up in dictionary to get wordId (needed for SRS + dictionary link)
  useEffect(() => {
    if (!hasVocab) setLoading(true);
    lookupWord(word).then((result) => {
      setInfo(result);
      if (!hasVocab) {
        setLoading(false);
        setLooked(true);
      }
    });
  }, [word, hasVocab]);

  // Close on click outside
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (tooltipRef.current && !tooltipRef.current.contains(e.target as Node)) {
        onClose();
      }
    };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, [onClose]);

  const displayHe = vocabEntry?.he || info?.hebrew || stripNikkud(word);
  const displayRu = vocabEntry?.ru || info?.translation_ru;
  const displayTranslit = vocabEntry?.translit || info?.transliteration;
  const displayNikkud = info?.nikkud;
  const wordId = info?.id;

  return (
    <div
      ref={tooltipRef}
      className="mt-3 p-3 bg-muted rounded-lg border text-sm animate-in fade-in-0 slide-in-from-top-1 duration-150"
    >
      <div className="flex items-center gap-2">
        <button
          className="shrink-0 text-muted-foreground hover:text-primary transition-colors text-base"
          onClick={() => speak(word)}
          title="Прослушать"
        >
          ▶
        </button>
        <HebrewText size="lg" className="font-bold">
          {displayNikkud || word}
        </HebrewText>
        {displayTranslit && (
          <span className="text-muted-foreground text-xs">{displayTranslit}</span>
        )}
      </div>

      {loading && (
        <p className="text-xs text-muted-foreground mt-1">Поиск...</p>
      )}

      {displayRu && (
        <p className="mt-1">— {displayRu}</p>
      )}

      {!loading && looked && !displayRu && !hasVocab && (
        <p className="text-xs text-muted-foreground mt-1">Не найдено в словаре</p>
      )}

      {info?.pos && (
        <span className="text-xs text-muted-foreground">{info.pos}</span>
      )}

      {wordId && (
        <div className="flex items-center gap-3 mt-1">
          <Link
            to={`/dictionary?search=${encodeURIComponent(stripNikkud(word))}`}
            className="text-xs text-primary hover:underline"
          >
            Открыть в словаре →
          </Link>
          <Button
            variant="ghost"
            size="sm"
            className="h-auto py-0.5 px-1.5 text-xs"
            disabled={createCards.isPending || srsAdded}
            onClick={() => {
              createCards.mutate({ word_ids: [wordId] }, {
                onSuccess: () => setSrsAdded(true),
              });
            }}
          >
            {srsAdded ? "Добавлено!" : createCards.isPending ? "..." : "+ В SRS"}
          </Button>
        </div>
      )}
    </div>
  );
}

export function InteractiveReader({ contentHe, vocabulary }: {
  contentHe: string;
  vocabulary: Array<{ he: string; ru: string; translit?: string }>;
}) {
  const [selectedToken, setSelectedToken] = useState<string | null>(null);
  const vocabMap = new Map(vocabulary.map((v) => [stripNikkud(v.he), v]));

  // Split text into words while preserving spaces and punctuation
  const tokens = contentHe.split(/(\s+)/);

  const handleClick = useCallback((token: string) => {
    const clean = token.replace(/[.,!?"״:;()\u05BE]/g, "");
    if (!clean.trim()) return;
    setSelectedToken((prev) => (prev === clean ? null : clean));
  }, []);

  const cleanSelected = selectedToken ? stripNikkud(selectedToken) : null;
  const vocabEntry = cleanSelected ? vocabMap.get(cleanSelected) : undefined;

  return (
    <div className="relative">
      <div className="leading-loose text-xl" dir="rtl">
        {tokens.map((token, i) => {
          const cleanToken = token.replace(/[.,!?"״:;()\u05BE]/g, "");
          if (!cleanToken.trim()) {
            return <span key={i} className="font-hebrew">{token}</span>;
          }

          const cleanNoNikkud = stripNikkud(cleanToken);
          const isVocab = vocabMap.has(cleanNoNikkud);
          const isSelected = selectedToken && stripNikkud(selectedToken) === cleanNoNikkud;

          return (
            <span
              key={i}
              className={[
                "cursor-pointer rounded px-0.5 font-hebrew transition-colors",
                isVocab
                  ? "border-b-2 border-dashed border-primary/30 hover:border-primary hover:bg-primary/10"
                  : "hover:bg-accent/50 border-b border-transparent hover:border-muted-foreground/30",
                isSelected ? "bg-primary/15 border-primary" : "",
              ].join(" ")}
              onClick={() => handleClick(token)}
            >
              {token}
            </span>
          );
        })}
      </div>

      {selectedToken && (
        <WordTooltip
          key={selectedToken}
          word={selectedToken}
          vocabEntry={vocabEntry}
          onClose={() => setSelectedToken(null)}
        />
      )}
    </div>
  );
}
