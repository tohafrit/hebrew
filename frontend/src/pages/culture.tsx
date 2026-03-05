import { useState } from "react";
import { useCultureArticles, useCultureArticle } from "@/hooks/use-gamification";
import { MarkdownContent } from "@/components/markdown-content";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

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
