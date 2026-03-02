import { cn } from "@/lib/utils";

interface HebrewTextProps {
  children: React.ReactNode;
  className?: string;
  size?: "sm" | "md" | "lg" | "xl" | "2xl";
}

const sizeClasses = {
  sm: "text-sm",
  md: "text-base",
  lg: "text-lg",
  xl: "text-xl",
  "2xl": "text-2xl",
};

export function HebrewText({ children, className, size = "md" }: HebrewTextProps) {
  return (
    <span dir="rtl" className={cn("font-hebrew", sizeClasses[size], className)}>
      {children}
    </span>
  );
}
