interface ProgressDataPoint {
  review_count: number;
  last_known_pct: number;
}

interface ReadingProgressChartProps {
  data: ProgressDataPoint[];
}

export function ReadingProgressChart({ data }: ReadingProgressChartProps) {
  if (!data.length) return <p className="text-sm text-muted-foreground">Нет данных</p>;

  const maxPct = 100;
  const barWidth = 100 / Math.max(data.length, 1);

  return (
    <div className="space-y-2">
      <div className="flex items-end gap-1 h-24">
        {data.map((d, i) => (
          <div key={i} className="flex-1 flex flex-col items-center gap-1">
            <span className="text-xs text-muted-foreground">{d.last_known_pct}%</span>
            <div
              className="w-full bg-primary/80 rounded-t transition-all"
              style={{ height: `${(d.last_known_pct / maxPct) * 80}px` }}
            />
            <span className="text-xs text-muted-foreground">#{d.review_count}</span>
          </div>
        ))}
      </div>
      <p className="text-xs text-muted-foreground text-center">Повторение →</p>
    </div>
  );
}
