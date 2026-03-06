import { useState } from "react";
import { useRootExplorer, useRootSearch } from "@/hooks/use-root-explorer";
import { HebrewText } from "@/components/hebrew-text";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { HebrewKeyboard } from "@/components/hebrew-keyboard";

export function RootExplorerPage() {
  const [query, setQuery] = useState("");
  const [selectedRoot, setSelectedRoot] = useState<string | null>(null);
  const { data: searchResults } = useRootSearch(query);
  const { data: rootData, isLoading } = useRootExplorer(selectedRoot);

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold">Корни</h1>
      <p className="text-muted-foreground">Введите корень для поиска связанных слов</p>

      {/* Search input */}
      <div className="space-y-3">
        <div dir="rtl" className="min-h-[48px] border rounded-md px-3 py-2 font-hebrew text-xl text-right bg-background">
          {query || <span className="text-muted-foreground">חפש שורש...</span>}
        </div>
        <HebrewKeyboard
          onKey={(k) => setQuery(v => v + k)}
          onBackspace={() => setQuery(v => v.slice(0, -1))}
          onSpace={() => setQuery(v => v + " ")}
        />
      </div>

      {/* Search results */}
      {searchResults && searchResults.length > 0 && !selectedRoot && (
        <div className="grid gap-2">
          {searchResults.map(r => (
            <Card key={r.id} className="cursor-pointer hover:bg-accent/50" onClick={() => { setSelectedRoot(r.root); setQuery(""); }}>
              <CardContent className="py-3 flex items-center justify-between">
                <HebrewText size="xl" className="font-bold">{r.root}</HebrewText>
                <span className="text-sm text-muted-foreground">{r.meaning_ru}</span>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Root detail */}
      {selectedRoot && (
        <>
          <button
            className="text-sm text-primary hover:underline"
            onClick={() => setSelectedRoot(null)}
          >
            ← Назад к поиску
          </button>

          {isLoading ? (
            <p className="text-center py-6 text-muted-foreground">Загрузка...</p>
          ) : rootData ? (
            <Card>
              <CardHeader className="text-center">
                <HebrewText size="2xl" className="font-bold">{rootData.root}</HebrewText>
                {rootData.meaning_ru && (
                  <p className="text-muted-foreground">{rootData.meaning_ru}</p>
                )}
                <Badge variant="secondary">{rootData.total_words} слов</Badge>
              </CardHeader>
              <CardContent className="space-y-6">
                {Object.entries(rootData.words_by_pos).map(([pos, words]) => (
                  <div key={pos}>
                    <h3 className="font-medium text-sm text-muted-foreground mb-2 uppercase">{pos}</h3>
                    <div className="grid gap-2">
                      {words.map(w => (
                        <div key={w.id} className="flex items-center justify-between p-2 rounded border">
                          <div className="flex items-center gap-2">
                            <HebrewText size="lg" className="font-bold">{w.nikkud || w.hebrew}</HebrewText>
                            {w.transliteration && (
                              <span className="text-xs text-muted-foreground">{w.transliteration}</span>
                            )}
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="text-sm">{w.translation_ru}</span>
                            {w.level_id && <Badge variant="outline" className="text-xs">ур.{w.level_id}</Badge>}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          ) : (
            <p className="text-center py-6 text-muted-foreground">Корень не найден</p>
          )}
        </>
      )}
    </div>
  );
}
