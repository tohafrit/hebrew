import { useState } from "react";
import { useAlphabet, type AlphabetLetter, type NikkudMark } from "@/hooks/use-alphabet";
import { HebrewText } from "@/components/hebrew-text";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

function LetterCard({ letter, selected, onClick }: {
  letter: AlphabetLetter;
  selected: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "flex flex-col items-center gap-1 p-3 rounded-lg border transition-colors",
        "hover:bg-accent hover:border-primary/50",
        selected && "bg-accent border-primary ring-2 ring-primary/20",
        letter.is_sofit && "border-dashed"
      )}
    >
      <HebrewText size="2xl" className="text-3xl font-bold">
        {letter.letter}
      </HebrewText>
      <span className="text-xs text-muted-foreground">{letter.name_ru}</span>
      <span className="text-xs text-muted-foreground font-mono">{letter.translit}</span>
    </button>
  );
}

function LetterDetail({ letter }: { letter: AlphabetLetter }) {
  return (
    <Card>
      <CardHeader className="text-center pb-3">
        <HebrewText size="2xl" className="text-6xl font-bold block">
          {letter.letter}
        </HebrewText>
        <CardTitle className="text-xl mt-2">{letter.name_ru}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div className="text-muted-foreground">Транслитерация</div>
          <div className="font-mono font-medium">{letter.translit}</div>

          <div className="text-muted-foreground">Произношение</div>
          <div>{letter.sound_description}</div>

          <div className="text-muted-foreground">Числовое значение</div>
          <div className="font-mono">{letter.numeric_value}</div>

          <div className="text-muted-foreground">Порядок</div>
          <div className="font-mono">{letter.order}</div>
        </div>

        {letter.is_sofit && (
          <Badge variant="outline" className="w-full justify-center">
            Конечная форма буквы {letter.sofit_of}
          </Badge>
        )}
      </CardContent>
    </Card>
  );
}

function NikkudCard({ mark }: { mark: NikkudMark }) {
  return (
    <div className="flex items-center gap-3 p-3 rounded-lg border">
      <HebrewText size="xl" className="text-2xl font-bold w-8 text-center">
        {mark.symbol}
      </HebrewText>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="font-medium">{mark.name_ru}</span>
          <HebrewText size="sm" className="text-muted-foreground">
            {mark.name_he}
          </HebrewText>
        </div>
        <div className="text-sm text-muted-foreground">
          Звук: <span className="font-medium">{mark.sound}</span>
        </div>
        {mark.example_word && (
          <div className="text-sm text-muted-foreground">
            Пример: <HebrewText size="sm">{mark.example_word}</HebrewText>
            {mark.example_translit && ` (${mark.example_translit})`}
          </div>
        )}
      </div>
    </div>
  );
}

export function AlphabetPage() {
  const { data, isLoading } = useAlphabet();
  const [selectedLetter, setSelectedLetter] = useState<AlphabetLetter | null>(null);
  const [tab, setTab] = useState<"letters" | "nikkud">("letters");

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-12">Загрузка...</p>;
  }

  const mainLetters = data?.letters.filter((l) => !l.is_sofit) ?? [];
  const sofitLetters = data?.letters.filter((l) => l.is_sofit) ?? [];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Алфавит</h1>
        <div className="flex gap-1">
          <Button
            variant={tab === "letters" ? "default" : "ghost"}
            size="sm"
            onClick={() => setTab("letters")}
          >
            Буквы (27)
          </Button>
          <Button
            variant={tab === "nikkud" ? "default" : "ghost"}
            size="sm"
            onClick={() => setTab("nikkud")}
          >
            Огласовки (12)
          </Button>
        </div>
      </div>

      {tab === "letters" && (
        <div className="grid gap-6 md:grid-cols-[1fr_280px]">
          <div className="space-y-4">
            <div>
              <h2 className="text-sm font-medium text-muted-foreground mb-2">
                Основные буквы (22)
              </h2>
              <div className="grid grid-cols-6 sm:grid-cols-8 md:grid-cols-6 lg:grid-cols-8 gap-2">
                {mainLetters.map((l) => (
                  <LetterCard
                    key={l.id}
                    letter={l}
                    selected={selectedLetter?.id === l.id}
                    onClick={() => setSelectedLetter(l)}
                  />
                ))}
              </div>
            </div>

            <div>
              <h2 className="text-sm font-medium text-muted-foreground mb-2">
                Конечные формы — софиёт (5)
              </h2>
              <div className="grid grid-cols-5 gap-2">
                {sofitLetters.map((l) => (
                  <LetterCard
                    key={l.id}
                    letter={l}
                    selected={selectedLetter?.id === l.id}
                    onClick={() => setSelectedLetter(l)}
                  />
                ))}
              </div>
            </div>
          </div>

          <div className="hidden md:block">
            {selectedLetter ? (
              <div className="sticky top-20">
                <LetterDetail letter={selectedLetter} />
              </div>
            ) : (
              <Card>
                <CardContent className="p-8 text-center text-muted-foreground">
                  Нажмите на букву для подробностей
                </CardContent>
              </Card>
            )}
          </div>

          {/* Mobile detail */}
          {selectedLetter && (
            <div className="md:hidden">
              <LetterDetail letter={selectedLetter} />
            </div>
          )}
        </div>
      )}

      {tab === "nikkud" && (
        <div className="space-y-2">
          {data?.nikkud.map((n) => <NikkudCard key={n.id} mark={n} />)}
        </div>
      )}
    </div>
  );
}
