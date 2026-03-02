import { cn } from "@/lib/utils";

const ROWS = [
  ["/", "'", "ק", "ר", "א", "ט", "ו", "ן", "ם", "פ"],
  ["ש", "ד", "ג", "כ", "ע", "י", "ח", "ל", "ך", "ף"],
  ["ז", "ס", "ב", "ה", "נ", "מ", "צ", "ת", "ץ"],
];

interface HebrewKeyboardProps {
  onKey: (key: string) => void;
  onBackspace: () => void;
  onSpace: () => void;
  highlightKeys?: string[];
  className?: string;
}

export function HebrewKeyboard({
  onKey,
  onBackspace,
  onSpace,
  highlightKeys,
  className,
}: HebrewKeyboardProps) {
  const highlightSet = new Set(highlightKeys);

  return (
    <div className={cn("space-y-1.5", className)} dir="rtl">
      {ROWS.map((row, ri) => (
        <div key={ri} className="flex gap-1 justify-center">
          {row.map((key) => (
            <button
              key={key}
              type="button"
              className={cn(
                "w-9 h-10 rounded border text-lg font-hebrew transition-colors",
                "hover:bg-primary/10 active:bg-primary/20",
                highlightSet.has(key)
                  ? "bg-primary/20 border-primary text-primary font-bold"
                  : "bg-background border-border"
              )}
              onClick={() => onKey(key)}
            >
              {key}
            </button>
          ))}
        </div>
      ))}
      <div className="flex gap-1 justify-center">
        <button
          type="button"
          className="px-4 h-10 rounded border bg-background border-border hover:bg-primary/10 active:bg-primary/20 text-sm"
          onClick={onBackspace}
        >
          ← מחק
        </button>
        <button
          type="button"
          className="flex-1 max-w-[200px] h-10 rounded border bg-background border-border hover:bg-primary/10 active:bg-primary/20 text-sm"
          onClick={onSpace}
        >
          רווח
        </button>
      </div>
    </div>
  );
}
