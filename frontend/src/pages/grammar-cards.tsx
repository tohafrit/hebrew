import { useState } from "react";
import { useGrammarCards, useGrammarCardDetail, useGrammarTags } from "@/hooks/use-grammar-cards";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export function GrammarCardsPage() {
  const [levelFilter, setLevelFilter] = useState<number | undefined>();
  const [tagFilter, setTagFilter] = useState<string | undefined>();
  const [selectedTopicId, setSelectedTopicId] = useState<number | null>(null);

  const { data: cards, isLoading } = useGrammarCards({ level_id: levelFilter, tag: tagFilter });
  const { data: tags } = useGrammarTags();
  const { data: detail } = useGrammarCardDetail(selectedTopicId);

  if (isLoading) return <p className="text-center py-12 text-muted-foreground">Загрузка...</p>;

  if (selectedTopicId && detail) {
    return (
      <div className="max-w-2xl mx-auto space-y-6">
        <button className="text-sm text-primary hover:underline" onClick={() => setSelectedTopicId(null)}>
          ← Назад к карточкам
        </button>
        <Card>
          <CardHeader>
            <CardTitle>{detail.title_ru}</CardTitle>
            {detail.title_he && <p className="font-hebrew text-lg">{detail.title_he}</p>}
            <div className="flex gap-1 flex-wrap">
              <Badge variant="outline">Уровень {detail.level_id}</Badge>
              {detail.tags.map(t => <Badge key={t} variant="secondary">{t}</Badge>)}
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {detail.summary && <p className="text-muted-foreground">{detail.summary}</p>}
            {detail.content_md && (
              <div className="prose dark:prose-invert max-w-none text-sm whitespace-pre-wrap">
                {detail.content_md}
              </div>
            )}
            {detail.rules.map(rule => (
              <div key={rule.id} className="border rounded-lg p-4 space-y-2">
                <p>{rule.rule_text_ru}</p>
                {rule.examples_json != null && (
                  <div className="text-sm text-muted-foreground">
                    <p className="font-medium">Примеры:</p>
                    <pre className="text-xs mt-1 whitespace-pre-wrap">{String(JSON.stringify(rule.examples_json, null, 2))}</pre>
                  </div>
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Грамматика</h1>

      {/* Filters */}
      <div className="space-y-3">
        <div className="flex gap-2 flex-wrap">
          <Button variant={!levelFilter ? "default" : "outline"} size="sm" onClick={() => setLevelFilter(undefined)}>Все</Button>
          {[1, 2, 3, 4, 5, 6, 7].map(l => (
            <Button key={l} variant={levelFilter === l ? "default" : "outline"} size="sm" onClick={() => setLevelFilter(l)}>
              Ур. {l}
            </Button>
          ))}
        </div>
        {tags && tags.length > 0 && (
          <div className="flex gap-1.5 flex-wrap">
            <Badge
              variant={!tagFilter ? "default" : "outline"}
              className="cursor-pointer"
              onClick={() => setTagFilter(undefined)}
            >
              Все теги
            </Badge>
            {tags.map(t => (
              <Badge
                key={t.tag}
                variant={tagFilter === t.tag ? "default" : "outline"}
                className="cursor-pointer"
                onClick={() => setTagFilter(t.tag)}
              >
                {t.tag} ({t.count})
              </Badge>
            ))}
          </div>
        )}
      </div>

      {/* Cards grid */}
      <div className="grid gap-3 sm:grid-cols-2">
        {cards?.map(card => (
          <Card key={card.id} className="cursor-pointer hover:bg-accent/50" onClick={() => setSelectedTopicId(card.id)}>
            <CardContent className="py-4 space-y-2">
              <p className="font-medium">{card.title_ru}</p>
              {card.title_he && <p className="font-hebrew text-muted-foreground">{card.title_he}</p>}
              <div className="flex gap-1 flex-wrap">
                <Badge variant="outline" className="text-xs">Ур. {card.level_id}</Badge>
                {card.tags.map(t => <Badge key={t} variant="secondary" className="text-xs">{t}</Badge>)}
              </div>
              {card.summary && <p className="text-xs text-muted-foreground line-clamp-2">{card.summary}</p>}
            </CardContent>
          </Card>
        ))}
        {cards?.length === 0 && (
          <p className="col-span-2 text-center py-6 text-muted-foreground">Нет карточек по выбранным фильтрам</p>
        )}
      </div>
    </div>
  );
}
