import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "@/hooks/use-auth";
import { useTheme } from "@/components/theme-provider";
import { Button } from "@/components/ui/button";
import { HebrewText } from "@/components/hebrew-text";
import { cn } from "@/lib/utils";

interface NavItem {
  path: string;
  label: string;
}

interface NavGroup {
  title: string;
  items: NavItem[];
}

const NAV_GROUPS: NavGroup[] = [
  {
    title: "Учить",
    items: [
      { path: "/path", label: "Путь" },
      { path: "/alphabet", label: "Алфавит" },
      { path: "/grammar", label: "Грамматика" },
      { path: "/lessons", label: "Уроки" },
      { path: "/topics", label: "Темы" },
    ],
  },
  {
    title: "Практика",
    items: [
      { path: "/reading", label: "Чтение" },
      { path: "/reader", label: "Свой текст" },
      { path: "/listening", label: "Аудирование" },
      { path: "/writing", label: "Письмо" },
      { path: "/dialogues", label: "Диалоги" },
      { path: "/pronunciation", label: "Произношение" },
      { path: "/handwriting", label: "Письмо (буквы)" },
      { path: "/minimal-pairs", label: "Мин. пары" },
      { path: "/cloze", label: "Пропуски" },
      { path: "/verbs", label: "Глаголы" },
      { path: "/conjugation-drill", label: "Спряжения" },
    ],
  },
  {
    title: "Словарь",
    items: [
      { path: "/dictionary", label: "Словарь" },
      { path: "/root-explorer", label: "Корни" },
      { path: "/srs", label: "Карточки SRS" },
    ],
  },
  {
    title: "Прогресс",
    items: [
      { path: "/dashboard", label: "Дашборд" },
      { path: "/leaderboard", label: "Рейтинг" },
      { path: "/achievements", label: "Достижения" },
      { path: "/culture", label: "Культура" },
    ],
  },
];

function ChevronDown({ className }: { className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <path d="m6 9 6 6 6-6" />
    </svg>
  );
}

function MenuIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="4" x2="20" y1="12" y2="12" /><line x1="4" x2="20" y1="6" y2="6" /><line x1="4" x2="20" y1="18" y2="18" />
    </svg>
  );
}

function CloseIcon() {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
      stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M18 6 6 18" /><path d="m6 6 12 12" />
    </svg>
  );
}

function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={() => setTheme(resolvedTheme === "dark" ? "light" : "dark")}
      className="h-8 w-8 p-0"
      title={resolvedTheme === "dark" ? "Светлая тема" : "Тёмная тема"}
    >
      {resolvedTheme === "dark" ? (
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
      ) : (
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
      )}
    </Button>
  );
}

function DesktopDropdown({ group, pathname, search }: { group: NavGroup; pathname: string; search: string }) {
  const fullPath = pathname + search;
  const isActive = group.items.some((item) => pathname === item.path || fullPath === item.path);

  return (
    <div className="relative group">
      <button
        className={cn(
          "flex items-center gap-1 rounded-md px-3 py-1.5 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground",
          isActive && "bg-accent text-accent-foreground"
        )}
      >
        {group.title}
        <ChevronDown className="transition-transform group-hover:rotate-180" />
      </button>
      <div className="hidden group-hover:block absolute left-0 top-full pt-1 z-50">
        <div className="rounded-md border bg-background p-1 shadow-md min-w-[160px]">
          {group.items.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                "block rounded-sm px-3 py-2 text-sm transition-colors hover:bg-accent hover:text-accent-foreground",
                (pathname === item.path || fullPath === item.path) && "bg-accent/50 font-medium"
              )}
            >
              {item.label}
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

function MobileDrawer({ open, onClose }: { open: boolean; onClose: () => void }) {
  const location = useLocation();

  useEffect(() => {
    onClose();
  }, [location.pathname]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!open) return null;

  return (
    <>
      <div className="fixed inset-0 bg-black/50 z-40" onClick={onClose} />
      <div className="fixed inset-y-0 left-0 w-72 bg-background border-r z-50 overflow-y-auto">
        <div className="flex items-center justify-between p-4 border-b">
          <Link to="/" className="flex items-center gap-2 font-semibold" onClick={onClose}>
            <HebrewText size="lg">עברית</HebrewText>
            <span>Ulpan AI</span>
          </Link>
          <button onClick={onClose} className="p-1 rounded-md hover:bg-accent">
            <CloseIcon />
          </button>
        </div>
        <nav className="p-4 space-y-6">
          {NAV_GROUPS.map((group) => (
            <div key={group.title}>
              <h3 className="text-sm font-semibold text-muted-foreground mb-2">
                {group.title}
              </h3>
              <div className="space-y-1">
                {group.items.map((item) => (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={cn(
                      "block rounded-md px-3 py-2 text-sm transition-colors hover:bg-accent",
                      (location.pathname === item.path || location.pathname + location.search === item.path) && "bg-accent font-medium"
                    )}
                  >
                    {item.label}
                  </Link>
                ))}
              </div>
            </div>
          ))}
        </nav>
      </div>
    </>
  );
}

export function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="border-b bg-background">
      <div className="w-full max-w-6xl mx-auto flex h-14 items-center justify-between px-4">
        <div className="flex items-center gap-4">
          {/* Mobile hamburger */}
          {isAuthenticated && (
            <button
              className="sm:hidden p-1 rounded-md hover:bg-accent"
              onClick={() => setMobileOpen(true)}
            >
              <MenuIcon />
            </button>
          )}

          <Link to="/" className="flex items-center gap-2 font-semibold">
            <HebrewText size="lg">עברית</HebrewText>
            <span>Ulpan AI</span>
          </Link>

          {/* Desktop dropdown nav */}
          {isAuthenticated && (
            <div className="hidden sm:flex items-center gap-1">
              {NAV_GROUPS.map((group) => (
                <DesktopDropdown key={group.title} group={group} pathname={location.pathname} search={location.search} />
              ))}
            </div>
          )}
        </div>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          {isAuthenticated && user ? (
            <>
              <span className="text-sm text-muted-foreground hidden sm:inline">
                {user.display_name} · {user.xp} XP
              </span>
              <Button variant="ghost" size="sm" asChild className="h-8 w-8 p-0" title="Настройки">
                <Link to="/settings">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>
                </Link>
              </Button>
              <Button variant="ghost" size="sm" onClick={() => logout()}>
                Выйти
              </Button>
            </>
          ) : (
            <div className="flex gap-2">
              <Button variant="ghost" size="sm" asChild>
                <Link to="/login">Войти</Link>
              </Button>
              <Button size="sm" asChild>
                <Link to="/register">Регистрация</Link>
              </Button>
            </div>
          )}
        </div>
      </div>

      {/* Mobile drawer */}
      {isAuthenticated && (
        <MobileDrawer open={mobileOpen} onClose={() => setMobileOpen(false)} />
      )}
    </nav>
  );
}
