import { Link } from "react-router-dom";
import { useStatsOverview, useLevels, useAnalytics } from "@/hooks/use-gamification";
import { useRecommendations } from "@/hooks/use-recommendations";
import { useSettings } from "@/hooks/use-settings";
import { useLeaderboard, useChallenges } from "@/hooks/use-leaderboard";
import { useDueReadings } from "@/hooks/use-spaced-reading";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

function SkillBar({ label, value }: { label: string; value: number }) {
  return (
    <div className="space-y-1">
      <div className="flex justify-between text-sm">
        <span>{label}</span>
        <span className="text-muted-foreground">{Math.round(value)}%</span>
      </div>
      <div className="h-2 rounded-full bg-muted">
        <div
          className="h-2 rounded-full bg-primary transition-all"
          style={{ width: `${Math.min(100, value)}%` }}
        />
      </div>
    </div>
  );
}

const EXERCISE_TYPE_LABELS: Record<string, string> = {
  multiple_choice: "Выбор ответа",
  fill_blank: "Заполнить пропуск",
  match_pairs: "Сопоставление",
  word_order: "Порядок слов",
  dictation: "Диктант",
  hebrew_typing: "Набор на иврите",
  translate_ru_he: "Перевод RU→HE",
  minimal_pairs: "Мин. пары",
  listening_comprehension: "Аудирование",
};

const SKILL_LABELS: Record<string, string> = {
  reading: "Чтение",
  writing: "Письмо",
  listening: "Аудирование",
  grammar: "Грамматика",
  vocabulary: "Словарный запас",
  speaking: "Разговорная речь",
};

function ActivityHeatmap({ activity }: { activity: { date: string; xp_earned: number }[] }) {
  // Build a map of date -> xp for last 90 days
  const xpMap = new Map(activity.map((a) => [a.date, a.xp_earned]));

  const today = new Date();
  const days: { date: string; xp: number }[] = [];
  for (let i = 89; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
    days.push({ date: key, xp: xpMap.get(key) ?? 0 });
  }

  const maxXP = Math.max(1, ...days.map((d) => d.xp));

  return (
    <div>
      <div className="flex flex-wrap gap-[3px]">
        {days.map((d) => {
          const intensity = d.xp === 0 ? 0 : Math.max(0.2, d.xp / maxXP);
          return (
            <div
              key={d.date}
              className="w-3 h-3 rounded-sm border border-border"
              style={{
                backgroundColor: d.xp > 0 ? `rgba(34, 197, 94, ${intensity})` : undefined,
              }}
              title={`${d.date}: ${d.xp} XP`}
            />
          );
        })}
      </div>
      <div className="flex justify-between text-xs text-muted-foreground mt-1">
        <span>90 дней назад</span>
        <span>Сегодня</span>
      </div>
    </div>
  );
}

export function DashboardPage() {
  const { data: stats, isLoading } = useStatsOverview();
  const { data: levels } = useLevels();
  const { data: recommendations } = useRecommendations();
  const { data: settings } = useSettings();
  const { data: analytics } = useAnalytics();
  const { data: leaderboard } = useLeaderboard("weekly");
  const { data: challenges } = useChallenges();
  const { data: dueReadings } = useDueReadings();

  if (isLoading || !stats) {
    return <p className="text-center py-12 text-muted-foreground">Загрузка...</p>;
  }

  // Find current level info
  const currentLevelInfo = levels?.find((l) => l.level === stats.current_level);
  const nextLevelInfo = levels?.find((l) => l.level === stats.current_level + 1);
  const xpInCurrentLevel = nextLevelInfo
    ? (nextLevelInfo.xp_required - stats.xp_to_next_level - (currentLevelInfo?.xp_required ?? 0))
    : stats.total_xp;
  const xpNeededForLevel = nextLevelInfo
    ? nextLevelInfo.xp_required - (currentLevelInfo?.xp_required ?? 0)
    : 1;
  const levelProgress = nextLevelInfo
    ? Math.round((xpInCurrentLevel / xpNeededForLevel) * 100)
    : 100;

  // Daily goal progress
  const goalMinutes = settings?.daily_goal_minutes ?? 15;
  const todayStr = (() => {
    const d = new Date();
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  })();
  const todayActivity = stats.daily_activity.find((a) => a.date === todayStr);
  const todayMinutes = todayActivity?.time_minutes ?? 0;
  const goalPct = Math.min(100, Math.round((todayMinutes / goalMinutes) * 100));

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Панель управления</h1>

      {/* Recommendations widget */}
      {recommendations && recommendations.length > 0 && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-lg">Что изучать сегодня</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {recommendations.map((rec) => (
                <Button
                  key={rec.type}
                  variant="outline"
                  size="sm"
                  asChild
                  className={cn(
                    "h-auto py-2",
                    rec.type === "weak_area" && "border-orange-400 bg-orange-50 dark:bg-orange-950/20 hover:bg-orange-100"
                  )}
                >
                  <Link to={rec.link}>
                    <span className="mr-1">{rec.icon}</span>
                    <span className="flex flex-col items-start text-left">
                      <span className="font-medium text-xs">{rec.title}</span>
                      <span className="text-[10px] text-muted-foreground">{rec.description}</span>
                    </span>
                  </Link>
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Daily goal progress */}
      <Card>
        <CardContent className="pt-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium">Дневная цель</span>
            <span className="text-sm text-muted-foreground">
              {todayMinutes} / {goalMinutes} мин ({goalPct}%)
            </span>
          </div>
          <div className="h-2 rounded-full bg-muted">
            <div
              className="h-2 rounded-full bg-green-500 transition-all"
              style={{ width: `${goalPct}%` }}
            />
          </div>
        </CardContent>
      </Card>

      {/* Top stats */}
      <div className="grid gap-4 grid-cols-2 md:grid-cols-4">
        <Card>
          <CardContent className="pt-4 text-center">
            <p className="text-3xl font-bold">{stats.current_level}</p>
            <p className="text-sm text-muted-foreground">{stats.level_name}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-4 text-center">
            <p className="text-3xl font-bold">{stats.total_xp}</p>
            <p className="text-sm text-muted-foreground">XP</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-4 text-center">
            <p className="text-3xl font-bold">{stats.streak_days}</p>
            <p className="text-sm text-muted-foreground">Серия (дней)</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-4 text-center">
            <p className="text-3xl font-bold">
              {stats.achievements_unlocked}/{stats.achievements_total}
            </p>
            <p className="text-sm text-muted-foreground">Достижения</p>
          </CardContent>
        </Card>
      </div>

      {/* Level progress */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Прогресс уровня</CardTitle>
          <CardDescription>
            {nextLevelInfo
              ? `${stats.xp_to_next_level} XP до уровня ${stats.current_level + 1} (${nextLevelInfo.name})`
              : "Максимальный уровень достигнут!"}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-4 rounded-full bg-muted">
            <div
              className="h-4 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all"
              style={{ width: `${levelProgress}%` }}
            />
          </div>
          {levels && (
            <div className="flex flex-wrap gap-2 mt-3">
              {levels.map((l) => (
                <span
                  key={l.level}
                  className={`text-xs px-2 py-0.5 rounded-full ${
                    l.level <= stats.current_level
                      ? "bg-primary text-primary-foreground"
                      : "bg-muted text-muted-foreground"
                  }`}
                >
                  {l.level}. {l.name}
                </span>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-2">
        {/* Skills radar */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Навыки</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {Object.entries(stats.skills).map(([key, value]) => (
              <SkillBar key={key} label={SKILL_LABELS[key] ?? key} value={value} />
            ))}
          </CardContent>
        </Card>

        {/* Study stats */}
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Статистика</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-3">
              <StatItem label="Слов изучено" value={stats.total_words} />
              <StatItem label="Карточек создано" value={stats.total_cards} />
              <StatItem label="Повторений" value={stats.total_reviews} />
              <StatItem label="Упражнений" value={stats.total_exercises} />
              <StatItem label="Текстов прочитано" value={stats.total_texts_read} />
              <StatItem label="Диалогов пройдено" value={stats.total_dialogues} />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Activity heatmap */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Активность</CardTitle>
          <CardDescription>XP за последние 90 дней</CardDescription>
        </CardHeader>
        <CardContent>
          <ActivityHeatmap activity={stats.daily_activity} />
        </CardContent>
      </Card>

      {/* Analytics */}
      {analytics && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Аналитика</CardTitle>
            <CardDescription>Прогресс за последние 30 дней</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 grid-cols-2 md:grid-cols-4">
              {/* Weekly accuracy */}
              <div className="text-center p-3 rounded-lg bg-muted/50">
                <p className="text-2xl font-bold">
                  {analytics.accuracy_trend.length > 0
                    ? `${Math.round(analytics.accuracy_trend.reduce((s, p) => s + p.accuracy, 0) / analytics.accuracy_trend.length)}%`
                    : "—"}
                </p>
                <p className="text-xs text-muted-foreground">Точность</p>
              </div>
              {/* SRS retention */}
              <div className="text-center p-3 rounded-lg bg-muted/50">
                <p className="text-2xl font-bold">{analytics.srs_retention_rate}%</p>
                <p className="text-xs text-muted-foreground">Запоминание SRS</p>
              </div>
              {/* Vocab size */}
              <div className="text-center p-3 rounded-lg bg-muted/50">
                <p className="text-2xl font-bold">
                  {analytics.vocab_growth.length > 0
                    ? analytics.vocab_growth[analytics.vocab_growth.length - 1].cumulative
                    : 0}
                </p>
                <p className="text-xs text-muted-foreground">Карточек создано</p>
              </div>
              {/* Avg response time */}
              <div className="text-center p-3 rounded-lg bg-muted/50">
                <p className="text-2xl font-bold">
                  {analytics.response_time_avg_ms
                    ? `${(analytics.response_time_avg_ms / 1000).toFixed(1)}с`
                    : "—"}
                </p>
                <p className="text-xs text-muted-foreground">Ср. время ответа</p>
              </div>
            </div>

            {/* Accuracy bar chart */}
            {analytics.accuracy_trend.length > 0 && (
              <div>
                <p className="text-sm font-medium mb-2">Точность по дням</p>
                <div className="flex items-end gap-[2px] h-16">
                  {analytics.accuracy_trend.slice(-14).map((p) => (
                    <div
                      key={p.date}
                      className="flex-1 rounded-t bg-primary/70 min-w-[4px]"
                      style={{ height: `${Math.max(4, p.accuracy)}%` }}
                      title={`${p.date}: ${p.accuracy}% (${p.total})`}
                    />
                  ))}
                </div>
                <div className="flex justify-between text-xs text-muted-foreground mt-1">
                  <span>{analytics.accuracy_trend.slice(-14)[0]?.date.slice(5)}</span>
                  <span>{analytics.accuracy_trend[analytics.accuracy_trend.length - 1]?.date.slice(5)}</span>
                </div>
              </div>
            )}

            {/* Weakest areas */}
            {analytics.weakest_areas.length > 0 && (
              <div>
                <p className="text-sm font-medium mb-2">Слабые места</p>
                <div className="space-y-1">
                  {analytics.weakest_areas.map((a) => (
                    <div key={a.type} className="flex items-center justify-between text-sm">
                      <span>{EXERCISE_TYPE_LABELS[a.type] || a.type}</span>
                      <span className={a.accuracy < 50 ? "text-red-500 font-medium" : "text-muted-foreground"}>
                        {a.accuracy}% ({a.total})
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Vocab growth sparkline */}
            {analytics.vocab_growth.length > 1 && (
              <div>
                <p className="text-sm font-medium mb-2">Рост словаря</p>
                <div className="flex items-end gap-[2px] h-12">
                  {analytics.vocab_growth.slice(-30).map((p) => {
                    const max = analytics.vocab_growth[analytics.vocab_growth.length - 1].cumulative || 1;
                    return (
                      <div
                        key={p.date}
                        className="flex-1 rounded-t bg-green-500/60 min-w-[2px]"
                        style={{ height: `${Math.max(4, (p.cumulative / max) * 100)}%` }}
                        title={`${p.date}: ${p.cumulative}`}
                      />
                    );
                  })}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Spaced reading due */}
      {dueReadings && dueReadings.length > 0 && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-lg">Повторное чтение</CardTitle>
            <CardDescription>{dueReadings.length} текст(ов) к повторению</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            {dueReadings.slice(0, 3).map((r) => (
              <Link
                key={r.schedule_id}
                to={`/reading/${r.text_id}`}
                className="flex items-center justify-between p-2 rounded hover:bg-accent transition-colors text-sm"
              >
                <span className="font-medium">{r.title_ru}</span>
                <Badge variant="secondary" className="text-xs">{r.last_known_pct}%</Badge>
              </Link>
            ))}
            {dueReadings.length > 3 && (
              <p className="text-xs text-muted-foreground text-center">
                + ещё {dueReadings.length - 3}
              </p>
            )}
          </CardContent>
        </Card>
      )}

      {/* Leaderboard preview + challenges */}
      <div className="grid gap-4 md:grid-cols-2">
        {leaderboard && leaderboard.entries.length > 0 && (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg">Рейтинг (неделя)</CardTitle>
            </CardHeader>
            <CardContent className="space-y-1">
              {leaderboard.entries.slice(0, 5).map((e, i) => (
                <div key={e.user_id} className={cn("flex items-center justify-between text-sm py-1", e.is_current_user && "font-medium text-primary")}>
                  <span>#{i + 1} {e.display_name}</span>
                  <span className="text-muted-foreground">{e.xp} XP</span>
                </div>
              ))}
              <Button variant="ghost" size="sm" className="w-full mt-2" asChild>
                <Link to="/leaderboard">Все результаты</Link>
              </Button>
            </CardContent>
          </Card>
        )}

        {challenges && challenges.length > 0 && (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-lg">Задания недели</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {challenges.slice(0, 3).map((ch) => (
                <div key={ch.id} className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span>{ch.title_ru}</span>
                    <span className="text-muted-foreground">+{ch.xp_reward} XP</span>
                  </div>
                  {ch.progress !== undefined && (
                    <div className="h-1.5 bg-secondary rounded-full overflow-hidden">
                      <div className="h-full bg-primary rounded-full" style={{ width: `${Math.min(100, (ch.progress / ch.target_count) * 100)}%` }} />
                    </div>
                  )}
                </div>
              ))}
              <Button variant="ghost" size="sm" className="w-full" asChild>
                <Link to="/leaderboard">Все задания</Link>
              </Button>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Quick links */}
      <div className="flex flex-wrap gap-2">
        <Button asChild variant="outline" size="sm">
          <Link to="/path">Путь обучения</Link>
        </Button>
        <Button asChild variant="outline" size="sm">
          <Link to="/srs">SRS-карточки</Link>
        </Button>
        <Button asChild variant="outline" size="sm">
          <Link to="/mistakes">Журнал ошибок</Link>
        </Button>
        <Button asChild variant="outline" size="sm">
          <Link to="/writing">Письмо</Link>
        </Button>
        <Button asChild variant="outline" size="sm">
          <Link to="/achievements">Достижения</Link>
        </Button>
        <Button asChild variant="outline" size="sm">
          <Link to="/culture">Культура Израиля</Link>
        </Button>
      </div>
    </div>
  );
}

function StatItem({ label, value }: { label: string; value: number }) {
  return (
    <div className="text-center p-2 rounded bg-muted/50">
      <p className="text-xl font-bold">{value}</p>
      <p className="text-xs text-muted-foreground">{label}</p>
    </div>
  );
}
