import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";

export function PWAUpdatePrompt() {
  const [needRefresh, setNeedRefresh] = useState(false);
  const [updateFn, setUpdateFn] = useState<((reloadPage?: boolean) => Promise<void>) | null>(null);

  useEffect(() => {
    // Dynamically import to avoid crash if vite-plugin-pwa is not available
    import("virtual:pwa-register").then(({ registerSW }) => {
      const update = registerSW({
        onNeedRefresh() {
          setNeedRefresh(true);
          setUpdateFn(() => update);
        },
      });
    }).catch(() => {
      // PWA not available (dev mode without plugin, etc.)
    });
  }, []);

  if (!needRefresh || !updateFn) return null;

  return (
    <div className="fixed bottom-4 left-4 right-4 z-50 flex items-center justify-between bg-primary text-primary-foreground p-4 rounded-lg shadow-lg max-w-md mx-auto">
      <span className="text-sm">Доступно обновление</span>
      <Button size="sm" variant="secondary" onClick={() => updateFn(true)}>
        Обновить
      </Button>
    </div>
  );
}
