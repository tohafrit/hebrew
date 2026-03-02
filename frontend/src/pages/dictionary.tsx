import { useState } from "react";
import { useWords, useDictionaryStats, useRootFamilies } from "@/hooks/use-words";
import type { RootFamilyOut } from "@/hooks/use-words";
import { WordCard } from "@/components/word-card";
import { WordDetailPanel } from "@/components/word-detail-panel";
import { HebrewText } from "@/components/hebrew-text";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
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

function RootFamilyCard({ family }: { family: RootFamilyOut }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <Card>
      <button
        className="w-full text-left"
        onClick={() => setExpanded(!expanded)}
      >
        <CardHeader className="flex flex-row items-center justify-between py-3 px-4">
          <div className="flex items-center gap-3">
            <HebrewText size="lg" className="font-bold">
              {family.root}
            </HebrewText>
            {family.meaning_ru && (
              <span className="text-sm text-muted-foreground">{family.meaning_ru}</span>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="secondary">{family.words.length}</Badge>
            <svg
              xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
              fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
              className={cn("transition-transform", expanded && "rotate-180")}
            >
              <path d="m6 9 6 6 6-6" />
            </svg>
          </div>
        </CardHeader>
      </button>
      {expanded && (
        <CardContent className="pt-0 pb-4 px-4">
          <div className="grid gap-2 sm:grid-cols-2">
            {family.words.map((w) => (
              <div key={w.id} className="flex items-center gap-2 text-sm">
                <HebrewText size="sm" className="font-medium">
                  {w.hebrew}
                </HebrewText>
                {w.pos && (
                  <Badge variant="outline" className="text-xs">
                    {POS_LABELS[w.pos] || w.pos}
                  </Badge>
                )}
                <span className="text-muted-foreground truncate">{w.translation_ru}</span>
              </div>
            ))}
          </div>
        </CardContent>
      )}
    </Card>
  );
}

type Tab = "words" | "roots";

export function DictionaryPage() {
  const [tab, setTab] = useState<Tab>("words");
  const [search, setSearch] = useState("");
  const [pos, setPos] = useState("");
  const [frequency, setFrequency] = useState("");
  const [page, setPage] = useState(1);
  const [rootsPage, setRootsPage] = useState(1);
  const [selectedWordId, setSelectedWordId] = useState<number | null>(null);
  const perPage = 24;

  const { data, isLoading } = useWords({
    page,
    per_page: perPage,
    search: search || undefined,
    pos: pos || undefined,
    frequency: frequency ? Number(frequency) : undefined,
  });

  const { data: rootsData, isLoading: rootsLoading } = useRootFamilies({
    page: rootsPage,
    per_page: 20,
  });

  const { data: stats } = useDictionaryStats();

  const totalPages = data ? Math.ceil(data.total / perPage) : 0;
  const rootsTotalPages = rootsData ? Math.ceil(rootsData.total / 20) : 0;

  const handleRootClick = (root: string) => {
    setTab("words");
    setSearch(root);
    setPage(1);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Словарь</h1>
        {stats && (
          <p className="text-sm text-muted-foreground">
            {stats.total_words} слов · {stats.root_families} корней
          </p>
        )}
      </div>

      {/* Tab switcher */}
      <div className="flex gap-1 border-b">
        <button
          className={cn(
            "px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px",
            tab === "words"
              ? "border-primary text-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          )}
          onClick={() => setTab("words")}
        >
          Слова
        </button>
        <button
          className={cn(
            "px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px",
            tab === "roots"
              ? "border-primary text-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          )}
          onClick={() => setTab("roots")}
        >
          Корни
        </button>
      </div>

      {tab === "words" && (
        <>
          {/* Filters */}
          <div className="flex flex-wrap gap-3">
            <Input
              placeholder="Поиск..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              className="max-w-xs"
            />
            <Select
              value={pos}
              onChange={(e) => {
                setPos(e.target.value);
                setPage(1);
              }}
              className="w-40"
            >
              <option value="">Все ч. речи</option>
              <option value="noun">Существительное</option>
              <option value="verb">Глагол</option>
              <option value="adj">Прилагательное</option>
              <option value="adv">Наречие</option>
              <option value="prep">Предлог</option>
              <option value="pron">Местоимение</option>
            </Select>
            <Select
              value={frequency}
              onChange={(e) => {
                setFrequency(e.target.value);
                setPage(1);
              }}
              className="w-40"
            >
              <option value="">Частотность</option>
              <option value="1">Высокая</option>
              <option value="2">Средняя</option>
              <option value="3">Низкая</option>
              <option value="4">Редкая</option>
            </Select>
          </div>

          {/* Stats bar */}
          {stats && (
            <div className="flex gap-4 text-sm text-muted-foreground">
              {Object.entries(stats.by_pos)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5)
                .map(([key, count]) => (
                  <span key={key}>
                    {key}: {count}
                  </span>
                ))}
            </div>
          )}

          <div className="flex gap-6">
            {/* Word grid */}
            <div className="flex-1">
              {isLoading ? (
                <p className="text-center text-muted-foreground py-8">Загрузка...</p>
              ) : data && data.items.length > 0 ? (
                <>
                  <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                    {data.items.map((word) => (
                      <WordCard
                        key={word.id}
                        word={word}
                        selected={word.id === selectedWordId}
                        onClick={() => setSelectedWordId(word.id)}
                        onRootClick={handleRootClick}
                      />
                    ))}
                  </div>

                  {/* Pagination */}
                  <div className="flex items-center justify-center gap-2 mt-6">
                    <Button
                      variant="outline"
                      size="sm"
                      disabled={page <= 1}
                      onClick={() => setPage(page - 1)}
                    >
                      Назад
                    </Button>
                    <span className="text-sm text-muted-foreground">
                      {page} / {totalPages} ({data.total} слов)
                    </span>
                    <Button
                      variant="outline"
                      size="sm"
                      disabled={page >= totalPages}
                      onClick={() => setPage(page + 1)}
                    >
                      Далее
                    </Button>
                  </div>
                </>
              ) : (
                <Card>
                  <CardContent className="p-8 text-center text-muted-foreground">
                    Слова не найдены
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Detail panel */}
            {selectedWordId && (
              <div className="w-80 shrink-0 hidden lg:block">
                <WordDetailPanel
                  wordId={selectedWordId}
                  onClose={() => setSelectedWordId(null)}
                />
              </div>
            )}
          </div>
        </>
      )}

      {tab === "roots" && (
        <div className="space-y-3">
          {rootsLoading ? (
            <p className="text-center text-muted-foreground py-8">Загрузка...</p>
          ) : rootsData && rootsData.items.length > 0 ? (
            <>
              <div className="space-y-2">
                {rootsData.items.map((family) => (
                  <RootFamilyCard key={family.id} family={family} />
                ))}
              </div>

              {/* Pagination */}
              <div className="flex items-center justify-center gap-2 mt-6">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={rootsPage <= 1}
                  onClick={() => setRootsPage(rootsPage - 1)}
                >
                  Назад
                </Button>
                <span className="text-sm text-muted-foreground">
                  {rootsPage} / {rootsTotalPages} ({rootsData.total} корней)
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={rootsPage >= rootsTotalPages}
                  onClick={() => setRootsPage(rootsPage + 1)}
                >
                  Далее
                </Button>
              </div>
            </>
          ) : (
            <Card>
              <CardContent className="p-8 text-center text-muted-foreground">
                Корни не найдены
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
