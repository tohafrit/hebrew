import { Link } from "react-router-dom";
import { useAuth } from "@/hooks/use-auth";
import { useHealth } from "@/hooks/use-health";
import { useSRSStats } from "@/hooks/use-srs";
import { useDictionaryStats } from "@/hooks/use-words";
import { useRecommendations } from "@/hooks/use-recommendations";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { HebrewText } from "@/components/hebrew-text";

interface SectionProps {
  title: string;
  children: React.ReactNode;
}

function Section({ title, children }: SectionProps) {
  return (
    <div className="space-y-3">
      <h2 className="text-lg font-semibold text-muted-foreground">{title}</h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {children}
      </div>
    </div>
  );
}

export function HomePage() {
  const { user } = useAuth();
  const { data: health } = useHealth();
  const { data: srsStats } = useSRSStats();
  const { data: dictStats } = useDictionaryStats();
  const { data: recommendations } = useRecommendations();

  return (
    <div className="space-y-6">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold">
          <HebrewText size="2xl">!שלום</HebrewText>
        </h1>
        {user && (
          <p className="text-muted-foreground">
            Добро пожаловать, {user.display_name}!
          </p>
        )}
      </div>

      {/* Recommendations bar */}
      {recommendations && recommendations.length > 0 && (
        <div className="flex flex-wrap gap-2 justify-center">
          {recommendations.slice(0, 3).map((rec) => (
            <Button key={rec.type} variant="outline" size="sm" asChild>
              <Link to={rec.link}>
                <span className="mr-1">{rec.icon}</span>
                {rec.title}
              </Link>
            </Button>
          ))}
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Уровень</CardTitle>
            <CardDescription>Ваш текущий прогресс</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{user?.current_level ?? 1}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">XP</CardTitle>
            <CardDescription>Опыт</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{user?.xp ?? 0}</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Серия</CardTitle>
            <CardDescription>Дней подряд</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold">{user?.streak_days ?? 0}</p>
          </CardContent>
        </Card>
      </div>

      {/* Учить */}
      <Section title="Учить">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Алфавит</CardTitle>
            <CardDescription>27 букв + огласовки</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/alphabet">Учить буквы</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Грамматика</CardTitle>
            <CardDescription>88 тем · биньяны · склонения</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/grammar">Открыть</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Уроки</CardTitle>
            <CardDescription>Алфавит, грамматика, упражнения</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/lessons">Начать урок</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Темы</CardTitle>
            <CardDescription>Тематические блоки</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/topics">Открыть</Link>
            </Button>
          </CardContent>
        </Card>
      </Section>

      {/* Практика */}
      <Section title="Практика">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Чтение</CardTitle>
            <CardDescription>Тексты с переводом</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/reading">Читать</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Свой текст</CardTitle>
            <CardDescription>Вставь иврит — увидишь перевод</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/reader">Открыть чтец</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Аудирование</CardTitle>
            <CardDescription>Диктанты · минимальные пары · TTS</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/listening">Слушать</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Письмо</CardTitle>
            <CardDescription>Клавиатура · перевод RU→HE</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/writing">Писать</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Диалоги</CardTitle>
            <CardDescription>Ситуации · ролевая игра</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/dialogues">Практика</Link>
            </Button>
          </CardContent>
        </Card>
      </Section>

      {/* Словарь и повторение */}
      <Section title="Словарь и повторение">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Словарь</CardTitle>
            <CardDescription>
              {dictStats
                ? `${dictStats.total_words} слов · ${dictStats.root_families} корней`
                : "Загрузка..."}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full">
              <Link to="/dictionary">Открыть словарь</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">SRS-карточки</CardTitle>
            <CardDescription>
              {srsStats
                ? `${srsStats.due_today} к повторению · ${srsStats.total_cards} всего`
                : "Загрузка..."}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant={srsStats && srsStats.due_today > 0 ? "default" : "secondary"}>
              <Link to="/srs">
                {srsStats && srsStats.due_today > 0
                  ? `Повторить (${srsStats.due_today})`
                  : "Карточки"}
              </Link>
            </Button>
          </CardContent>
        </Card>
      </Section>

      {/* Прогресс */}
      <Section title="Прогресс">
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Дашборд</CardTitle>
            <CardDescription>Навыки · активность</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/dashboard">Открыть</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Достижения</CardTitle>
            <CardDescription>Ачивки · уровни · серии</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/achievements">Смотреть</Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Культура</CardTitle>
            <CardDescription>Праздники · быт · сленг</CardDescription>
          </CardHeader>
          <CardContent>
            <Button asChild className="w-full" variant="secondary">
              <Link to="/culture">Читать</Link>
            </Button>
          </CardContent>
        </Card>
      </Section>

      {health && (
        <p className="text-xs text-center text-muted-foreground">
          Система: {health.status} | БД: {health.db ? "OK" : "---"} | Redis: {health.redis ? "OK" : "---"}
        </p>
      )}
    </div>
  );
}
