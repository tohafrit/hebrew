import { createContext, useContext } from "react";
import { useSettings } from "@/hooks/use-settings";

const NikkudContext = createContext<boolean>(true);

export function useShowNikkud() {
  return useContext(NikkudContext);
}

export function NikkudProvider({ children }: { children: React.ReactNode }) {
  const { data: settings } = useSettings();
  const showNikkud = settings?.show_nikkud ?? true;

  return (
    <NikkudContext.Provider value={showNikkud}>
      {children}
    </NikkudContext.Provider>
  );
}
