import { cn } from "@/lib/utils";
import { useShowNikkud } from "@/components/nikkud-provider";

interface HebrewTextProps {
  children: React.ReactNode;
  className?: string;
  size?: "sm" | "base" | "md" | "lg" | "xl" | "2xl";
  nikkud?: string | null;
}

const sizeClasses = {
  sm: "text-sm",
  base: "text-base",
  md: "text-base",
  lg: "text-lg",
  xl: "text-xl",
  "2xl": "text-2xl",
};

export function HebrewText({ children, className, size = "md", nikkud }: HebrewTextProps) {
  const showNikkud = useShowNikkud();
  const display = showNikkud && nikkud ? nikkud : children;

  return (
    <span dir="rtl" lang="he" className={cn("font-hebrew", sizeClasses[size], className)}>
      {display}
    </span>
  );
}
