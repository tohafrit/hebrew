import { useState } from "react";
import { useWords, useDictionaryStats, useRootFamilies } from "@/hooks/use-words";
import { useUrlParam, useUrlNumParam, useSetUrlParams } from "@/hooks/use-url-state";
import type { RootFamilyOut } from "@/hooks/use-words";
import { WordCard } from "@/components/word-card";
import { WordDetailPanel } from "@/components/word-detail-panel";
import { HebrewText } from "@/components/hebrew-text";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
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
  const [tab, setTab] = useUrlParam("tab", "words") as [Tab, (v: string) => void];
  const [search, setSearch] = useUrlParam("search");
  const [pos, setPos] = useUrlParam("pos");
  const [frequency, setFrequency] = useUrlParam("freq");
  const [level, setLevel] = useUrlParam("level");
  const [pageStr, setPageStr] = useUrlParam("page", "1");
  const [rootsPageStr, setRootsPageStr] = useUrlParam("rp", "1");
  const [wordIdStr, setWordIdStr] = useUrlParam("word");
  const setUrlParams = useSetUrlParams();

  const page = Number(pageStr) || 1;
  const rootsPage = Number(rootsPageStr) || 1;
  const selectedWordId = wordIdStr ? Number(wordIdStr) : null;
  const setPage = (p: number) => setPageStr(String(p));
  const setRootsPage = (p: number) => setRootsPageStr(String(p));
  const setSelectedWordId = (id: number | null) => setWordIdStr(id ? String(id) : "");
  const perPage = 24;

  const { data, isLoading } = useWords({
    page,
    per_page: perPage,
    search: search || undefined,
    pos: pos || undefined,
    frequency: frequency ? Number(frequency) : undefined,
    level_id: level ? Number(level) : undefined,
  });

  const { data: rootsData, isLoading: rootsLoading } = useRootFamilies({
    page: rootsPage,
    per_page: 20,
  });

  const { data: stats } = useDictionaryStats();

  const totalPages = data ? Math.ceil(data.total / perPage) : 0;
  const rootsTotalPages = rootsData ? Math.ceil(rootsData.total / 20) : 0;

  const handleRootClick = (root: string) => {
    setUrlParams({ tab: "words", search: root, page: "1" });
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
                setUrlParams({ search: e.target.value || null, page: null });
              }}
              className="max-w-xs"
            />
            <Select
              value={pos || "all"}
              onValueChange={(v) => {
                setUrlParams({ pos: v === "all" ? null : v, page: null });
              }}
            >
              <SelectTrigger className="w-44">
                <SelectValue placeholder="Все ч. речи" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Все ч. речи</SelectItem>
                <SelectItem value="noun">Существительное</SelectItem>
                <SelectItem value="verb">Глагол</SelectItem>
                <SelectItem value="adj">Прилагательное</SelectItem>
                <SelectItem value="adv">Наречие</SelectItem>
                <SelectItem value="prep">Предлог</SelectItem>
                <SelectItem value="pron">Местоимение</SelectItem>
              </SelectContent>
            </Select>
            <Select
              value={frequency || "all"}
              onValueChange={(v) => {
                setUrlParams({ freq: v === "all" ? null : v, page: null });
              }}
            >
              <SelectTrigger className="w-44">
                <SelectValue placeholder="Частотность" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Частотность</SelectItem>
                <SelectItem value="1">Высокая</SelectItem>
                <SelectItem value="2">Средняя</SelectItem>
                <SelectItem value="3">Низкая</SelectItem>
                <SelectItem value="4">Редкая</SelectItem>
              </SelectContent>
            </Select>
            <Select
              value={level || "all"}
              onValueChange={(v) => {
                setUrlParams({ level: v === "all" ? null : v, page: null });
              }}
            >
              <SelectTrigger className="w-44">
                <SelectValue placeholder="Уровень" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Все уровни</SelectItem>
                <SelectItem value="1">Алеф (א) · A1</SelectItem>
                <SelectItem value="2">Бет (ב) · A2</SelectItem>
                <SelectItem value="3">Гимель (ג) · B1</SelectItem>
                <SelectItem value="4">Далет (ד) · B2</SelectItem>
                <SelectItem value="5">Хей (ה) · C1</SelectItem>
                <SelectItem value="6">Вав (ו) · C2</SelectItem>
              </SelectContent>
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

            {/* Detail panel — desktop sidebar */}
            {selectedWordId && (
              <div className="w-80 shrink-0 hidden lg:block">
                <WordDetailPanel
                  wordId={selectedWordId}
                  onClose={() => setSelectedWordId(null)}
                />
              </div>
            )}

            {/* Detail panel — mobile overlay */}
            {selectedWordId && (
              <div className="lg:hidden fixed inset-0 z-50 bg-background/80 backdrop-blur-sm"
                onClick={() => setSelectedWordId(null)}
              >
                <div
                  className="absolute bottom-0 left-0 right-0 max-h-[85vh] overflow-y-auto bg-background border-t rounded-t-xl shadow-lg"
                  onClick={(e) => e.stopPropagation()}
                >
                  <div className="w-12 h-1 rounded-full bg-muted-foreground/30 mx-auto mt-2 mb-1" />
                  <WordDetailPanel
                    wordId={selectedWordId}
                    onClose={() => setSelectedWordId(null)}
                  />
                </div>
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
