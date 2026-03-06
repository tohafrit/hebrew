import { useRegisterSW } from "virtual:pwa-register/react";
import { Button } from "@/components/ui/button";

export function PWAUpdatePrompt() {
  const {
    needRefresh: [needRefresh],
    updateServiceWorker,
  } = useRegisterSW();

  if (!needRefresh) return null;

  return (
    <div className="fixed bottom-4 left-4 right-4 z-50 flex items-center justify-between bg-primary text-primary-foreground p-4 rounded-lg shadow-lg max-w-md mx-auto">
      <span className="text-sm">Доступно обновление</span>
      <Button size="sm" variant="secondary" onClick={() => updateServiceWorker(true)}>
        Обновить
      </Button>
    </div>
  );
}
