import { useState } from "react";
import { useCultureArticles, useCultureArticle, useCultureArticleWords } from "@/hooks/use-gamification";
import { useCreateCards } from "@/hooks/use-srs";
import { MarkdownContent } from "@/components/markdown-content";
import { HebrewText } from "@/components/hebrew-text";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { toast } from "@/hooks/use-toast";

const CATEGORIES = [
  { value: "", label: "Все" },
  { value: "holidays", label: "Праздники" },
  { value: "daily_life", label: "Быт" },
  { value: "slang", label: "Сленг" },
  { value: "abbreviations", label: "Аббревиатуры" },
];

export function CulturePage() {
  const [category, setCategory] = useState("");
  const [selectedId, setSelectedId] = useState<number | null>(null);

  const { data: articles, isLoading } = useCultureArticles(category || undefined);
  const { data: article } = useCultureArticle(selectedId);
  const { data: articleWords } = useCultureArticleWords(selectedId);
  const createCards = useCreateCards();

  if (selectedId && article) {
    return (
      <div className="space-y-4">
        <Button variant="ghost" size="sm" onClick={() => setSelectedId(null)}>
          &larr; Назад к списку
        </Button>
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              {article.title_ru}
              {article.title_he && (
                <span className="font-hebrew text-lg text-muted-foreground">
                  {article.title_he}
                </span>
              )}
            </CardTitle>
            <p className="text-sm text-muted-foreground">
              {CATEGORIES.find((c) => c.value === article.category)?.label ?? article.category}
            </p>
          </CardHeader>
          <CardContent>
            <MarkdownContent content={article.content_md} />
          </CardContent>
        </Card>

        {/* Words from article */}
        {articleWords && articleWords.length > 0 && (
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Слова из статьи</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-1.5">
                {articleWords.slice(0, 30).map((w) => (
                  <div key={w.word_id} className="flex items-center justify-between text-sm p-1.5 rounded hover:bg-accent/50">
                    <div className="flex items-center gap-2">
                      <HebrewText size="sm" className="font-medium">{w.hebrew}</HebrewText>
                      <span className="text-muted-foreground">{w.translation_ru}</span>
                      {w.pos && <Badge variant="outline" className="text-xs">{w.pos}</Badge>}
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      className="h-6 text-xs"
                      onClick={async () => {
                        try {
                          const result = await createCards.mutateAsync({ word_ids: [w.word_id] });
                          toast({
                            title: "В SRS",
                            description: result.created > 0 ? `Создано ${result.created} карточек` : "Уже существуют",
                          });
                        } catch {
                          toast({ title: "Ошибка", variant: "destructive" });
                        }
                      }}
                    >
                      + SRS
                    </Button>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Культура Израиля</h1>

      {/* Category filters */}
      <div className="flex flex-wrap gap-2">
        {CATEGORIES.map((cat) => (
          <Button
            key={cat.value}
            variant={category === cat.value ? "default" : "outline"}
            size="sm"
            onClick={() => {
              setCategory(cat.value);
              setSelectedId(null);
            }}
          >
            {cat.label}
          </Button>
        ))}
      </div>

      {isLoading ? (
        <p className="text-center py-8 text-muted-foreground">Загрузка...</p>
      ) : !articles || articles.length === 0 ? (
        <p className="text-center py-8 text-muted-foreground">Нет статей в этой категории</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {articles.map((a) => (
            <Card
              key={a.id}
              className="cursor-pointer hover:border-primary/50 transition-colors"
              onClick={() => setSelectedId(a.id)}
            >
              <CardHeader>
                <CardTitle className="text-base">{a.title_ru}</CardTitle>
                {a.title_he && (
                  <p className="font-hebrew text-muted-foreground">{a.title_he}</p>
                )}
              </CardHeader>
              <CardContent>
                <span className="text-xs px-2 py-0.5 rounded-full bg-muted text-muted-foreground">
                  {CATEGORIES.find((c) => c.value === a.category)?.label ?? a.category}
                </span>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
