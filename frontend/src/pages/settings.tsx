import { useState, useEffect } from "react";
import { useSettings, useUpdateSettings } from "@/hooks/use-settings";
import { useTheme } from "@/components/theme-provider";
import { isSoundMuted, toggleSoundMute } from "@/hooks/use-sound-effects";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function SettingsPage() {
  const { data: settings, isLoading } = useSettings();
  const updateSettings = useUpdateSettings();
  const { theme, setTheme } = useTheme();
  const [muted, setMuted] = useState(isSoundMuted());

  const [goalMinutes, setGoalMinutes] = useState(15);
  const [newCards, setNewCards] = useState(10);
  const [notifications, setNotifications] = useState(true);
  const [showNikkud, setShowNikkud] = useState(true);

  useEffect(() => {
    if (settings) {
      setGoalMinutes(settings.daily_goal_minutes);
      setNewCards(settings.daily_new_cards);
      setNotifications(settings.notifications);
      setShowNikkud(settings.show_nikkud);
    }
  }, [settings]);

  const handleSave = () => {
    updateSettings.mutate({
      daily_goal_minutes: goalMinutes,
      daily_new_cards: newCards,
      notifications,
      show_nikkud: showNikkud,
      ui_theme: theme === "system" ? "system" : theme,
    });
  };

  if (isLoading) {
    return <p className="text-center py-12 text-muted-foreground">Загрузка...</p>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Настройки</h1>

      {/* Learning */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Обучение</CardTitle>
          <CardDescription>Настройте темп изучения</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="goal">Дневная цель (минуты)</Label>
            <Input
              id="goal"
              type="number"
              min={5}
              max={120}
              value={goalMinutes}
              onChange={(e) => setGoalMinutes(Number(e.target.value))}
            />
            <p className="text-xs text-muted-foreground">от 5 до 120 минут</p>
          </div>
          <div className="space-y-2">
            <Label htmlFor="cards">Новых карточек в день</Label>
            <Input
              id="cards"
              type="number"
              min={1}
              max={50}
              value={newCards}
              onChange={(e) => setNewCards(Number(e.target.value))}
            />
            <p className="text-xs text-muted-foreground">от 1 до 50 карточек</p>
          </div>
        </CardContent>
      </Card>

      {/* Appearance */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Оформление</CardTitle>
          <CardDescription>Внешний вид и звуки</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>Тема</Label>
            <div className="flex gap-2">
              {(["light", "dark", "system"] as const).map((t) => (
                <Button
                  key={t}
                  variant={theme === t ? "default" : "outline"}
                  size="sm"
                  onClick={() => setTheme(t)}
                >
                  {t === "light" ? "Светлая" : t === "dark" ? "Тёмная" : "Системная"}
                </Button>
              ))}
            </div>
          </div>
          <div className="flex items-center justify-between">
            <div>
              <Label>Огласовки (никуд)</Label>
              <p className="text-xs text-muted-foreground">Показывать огласовки в ивритских словах</p>
            </div>
            <Button
              variant={showNikkud ? "default" : "outline"}
              size="sm"
              onClick={() => setShowNikkud(!showNikkud)}
            >
              {showNikkud ? "Вкл" : "Выкл"}
            </Button>
          </div>
          <div className="flex items-center justify-between">
            <div>
              <Label>Звуки</Label>
              <p className="text-xs text-muted-foreground">Звуковые эффекты при ответах</p>
            </div>
            <Button
              variant={muted ? "outline" : "default"}
              size="sm"
              onClick={() => {
                const newMuted = toggleSoundMute();
                setMuted(newMuted);
              }}
            >
              {muted ? "Включить" : "Выключить"}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Notifications */}
      <Card>
        <CardHeader>
          <CardTitle className="text-lg">Уведомления</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div>
              <Label>Напоминания</Label>
              <p className="text-xs text-muted-foreground">Напоминать о занятиях</p>
            </div>
            <Button
              variant={notifications ? "default" : "outline"}
              size="sm"
              onClick={() => setNotifications(!notifications)}
            >
              {notifications ? "Вкл" : "Выкл"}
            </Button>
          </div>
        </CardContent>
      </Card>

      <Button onClick={handleSave} disabled={updateSettings.isPending} className="w-full">
        {updateSettings.isPending ? "Сохранение..." : "Сохранить"}
      </Button>

      {updateSettings.isSuccess && (
        <p className="text-center text-sm text-green-600">Настройки сохранены</p>
      )}
    </div>
  );
}
