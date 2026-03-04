import { useState } from "react";
import { useGrammarTopics, useGrammarTopic, useBinyanim, usePrepositions } from "@/hooks/use-grammar";
import { useUrlParam, useUrlNumParam } from "@/hooks/use-url-state";
import type { Preposition } from "@/hooks/use-grammar";
import { HebrewText } from "@/components/hebrew-text";
import { MarkdownContent } from "@/components/markdown-content";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

const LEVEL_LABELS: Record<number, string> = {
  1: "Алеф (A1)",
  2: "Бет (A2)",
  3: "Гимель (B1)",
  4: "Далет (B2)",
  5: "Хей (C1)",
  6: "Вав (C2)",
};

const PERSON_ORDER = ["1s", "2ms", "2fs", "3ms", "3fs", "1p", "2mp", "2fp", "3mp", "3fp"];
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
};

function TopicCard({ topic, selected, onClick }: {
  topic: { id: number; title_ru: string; title_he: string | null; level_id: number; summary: string | null };
  selected: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "w-full text-left p-3 rounded-lg border transition-colors",
        "hover:bg-accent",
        selected && "bg-accent border-primary ring-1 ring-primary/20"
      )}
    >
      <div className="flex items-center gap-2 mb-1">
        <span className="font-medium text-sm">{topic.title_ru}</span>
        {topic.title_he && (
          <HebrewText size="sm" className="text-muted-foreground">
            {topic.title_he}
          </HebrewText>
        )}
      </div>
      {topic.summary && (
        <p className="text-xs text-muted-foreground line-clamp-2">{topic.summary}</p>
      )}
    </button>
  );
}

function PrepositionCard({ prep }: { prep: Preposition }) {
  const [expanded, setExpanded] = useState(false);
  const decl = prep.declension_json;

  return (
    <Card>
      <button className="w-full text-left" onClick={() => setExpanded(!expanded)}>
        <CardHeader className="flex flex-row items-center justify-between py-3 px-4">
          <div className="flex items-center gap-3">
            <HebrewText size="xl" className="font-bold">
              {prep.base_form}
            </HebrewText>
            <span className="text-sm text-muted-foreground">{prep.meaning_ru}</span>
          </div>
          <div className="flex items-center gap-2">
            {decl && <Badge variant="secondary">склоняется</Badge>}
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
      {expanded && decl && (
        <CardContent className="pt-0 pb-4 px-4">
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
            {PERSON_ORDER.map((person) => {
              const entry = decl[person];
              if (!entry) return null;
              return (
                <div key={person} className="flex items-center gap-2 text-sm">
                  <span className="text-xs text-muted-foreground w-14 shrink-0">
                    {PERSON_LABELS[person]}
                  </span>
                  <HebrewText size="sm" className="font-medium">
                    {entry.form}
                  </HebrewText>
                  <span className="text-xs text-muted-foreground">
                    {entry.translit}
                  </span>
                </div>
              );
            })}
          </div>
        </CardContent>
      )}
      {expanded && !decl && (
        <CardContent className="pt-0 pb-4 px-4">
          <p className="text-sm text-muted-foreground">
            Этот предлог не склоняется с местоимёнными суффиксами
          </p>
        </CardContent>
      )}
    </Card>
  );
}

type GrammarTab = "topics" | "prepositions";

export function GrammarPage() {
  const { data: topics, isLoading } = useGrammarTopics();
  const { data: binyanim } = useBinyanim();
  const { data: prepositions } = usePrepositions();
  const [selectedTopicId, setSelectedTopicId] = useUrlNumParam("topic");
  const { data: topicDetail } = useGrammarTopic(selectedTopicId);
  const [levelFilter, setLevelFilter] = useUrlNumParam("level");
  const [tab, setTab] = useUrlParam("tab", "topics") as [GrammarTab, (v: string) => void];

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-12">Загрузка...</p>;
  }

  const filteredTopics = levelFilter !== null
    ? topics?.filter((t) => t.level_id === levelFilter)
    : topics;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Грамматика</h1>
      </div>

      {/* Tab switcher */}
      <div className="flex gap-1 border-b">
        <button
          className={cn(
            "px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px",
            tab === "topics"
              ? "border-primary text-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          )}
          onClick={() => setTab("topics")}
        >
          Темы ({topics?.length ?? 0})
        </button>
        <button
          className={cn(
            "px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px",
            tab === "prepositions"
              ? "border-primary text-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          )}
          onClick={() => setTab("prepositions")}
        >
          Предлоги ({prepositions?.length ?? 0})
        </button>
      </div>

      {tab === "topics" && (
        <>
          <div className="flex gap-1 flex-wrap">
            <Button
              variant={levelFilter === null ? "default" : "ghost"}
              size="sm"
              onClick={() => setLevelFilter(null)}
            >
              Все
            </Button>
            {[1, 2, 3, 4, 5, 6].map((lvl) => (
              <Button
                key={lvl}
                variant={levelFilter === lvl ? "default" : "ghost"}
                size="sm"
                onClick={() => setLevelFilter(lvl)}
              >
                {LEVEL_LABELS[lvl].split(" ")[0]}
              </Button>
            ))}
          </div>

          <div className="grid gap-6 md:grid-cols-[280px_1fr]">
            {/* Topic list */}
            <div className="space-y-1 max-h-[70vh] overflow-y-auto">
              {filteredTopics?.map((t) => (
                <TopicCard
                  key={t.id}
                  topic={t}
                  selected={selectedTopicId === t.id}
                  onClick={() => setSelectedTopicId(t.id)}
                />
              ))}
            </div>

            {/* Topic detail */}
            <div>
              {topicDetail ? (
                <Card>
                  <CardHeader>
                    <div className="flex items-center gap-2">
                      <Badge variant="secondary">
                        {LEVEL_LABELS[topicDetail.level_id] || `Уровень ${topicDetail.level_id}`}
                      </Badge>
                    </div>
                    <CardTitle className="text-xl flex items-center gap-2">
                      {topicDetail.title_ru}
                      {topicDetail.title_he && (
                        <HebrewText size="lg" className="text-muted-foreground">
                          {topicDetail.title_he}
                        </HebrewText>
                      )}
                    </CardTitle>
                    {topicDetail.summary && (
                      <CardDescription>{topicDetail.summary}</CardDescription>
                    )}
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {topicDetail.content_md && (
                      <MarkdownContent content={topicDetail.content_md} />
                    )}

                    {topicDetail.rules.length > 0 && (
                      <div className="space-y-4">
                        <h3 className="font-medium text-sm text-muted-foreground uppercase tracking-wide">
                          Правила
                        </h3>
                        {topicDetail.rules.map((rule) => (
                          <div key={rule.id} className="border rounded-lg p-4 space-y-2">
                            <p className="font-medium text-sm">{rule.rule_text_ru}</p>
                            {rule.examples_json && (
                              <div className="space-y-1">
                                {(rule.examples_json as Array<{ he: string; ru: string; translit?: string }>).map(
                                  (ex, i) => (
                                    <div key={i} className="flex items-center gap-3 text-sm">
                                      <HebrewText size="sm" className="font-medium">
                                        {ex.he}
                                      </HebrewText>
                                      {ex.translit && (
                                        <span className="text-muted-foreground">{ex.translit}</span>
                                      )}
                                      <span>— {ex.ru}</span>
                                    </div>
                                  )
                                )}
                              </div>
                            )}
                            {rule.exceptions_json && (
                              <div className="bg-muted rounded p-2 text-xs">
                                <span className="font-medium">Исключения: </span>
                                {(rule.exceptions_json as Array<{ text: string }>).map(
                                  (exc, i) => (
                                    <span key={i}>{exc.text}</span>
                                  )
                                )}
                              </div>
                            )}
                          </div>
                        ))}
                      </div>
                    )}
                  </CardContent>
                </Card>
              ) : (
                <Card>
                  <CardContent className="p-12 text-center text-muted-foreground">
                    Выберите тему слева
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </>
      )}

      {tab === "prepositions" && (
        <div className="space-y-3">
          <p className="text-muted-foreground text-sm">
            Предлоги иврита с местоимёнными суффиксами. Нажмите на предлог, чтобы увидеть все формы склонения.
          </p>
          <div className="grid gap-2 sm:grid-cols-2">
            {prepositions?.map((p) => (
              <PrepositionCard key={p.id} prep={p} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
