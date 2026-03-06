import { useState } from "react";
import { HebrewText } from "@/components/hebrew-text";

export function InteractiveReader({ contentHe, vocabulary }: {
  contentHe: string;
  vocabulary: Array<{ he: string; ru: string; translit?: string }>;
}) {
  const [hoveredWord, setHoveredWord] = useState<string | null>(null);
  const vocabMap = new Map(vocabulary.map((v) => [v.he, v]));

  // Split text into words while preserving spaces and punctuation
  const tokens = contentHe.split(/(\s+)/);

  const tooltip = hoveredWord ? vocabMap.get(hoveredWord) : null;

  return (
    <div className="relative">
      <div className="leading-loose text-xl" dir="rtl">
        {tokens.map((token, i) => {
          // Check if this token matches any vocabulary word
          const cleanToken = token.replace(/[.,!?"״:;]/g, "");
          const match = vocabMap.get(cleanToken);

          if (match) {
            return (
              <span
                key={i}
                className="relative cursor-pointer border-b-2 border-dashed border-primary/30 hover:border-primary hover:bg-primary/10 rounded px-0.5 font-hebrew transition-colors"
                onMouseEnter={() => setHoveredWord(cleanToken)}
                onMouseLeave={() => setHoveredWord(null)}
              >
                {token}
              </span>
            );
          }

          return (
            <span key={i} className="font-hebrew">
              {token}
            </span>
          );
        })}
      </div>

      {tooltip && (
        <div className="mt-3 p-3 bg-muted rounded-lg border text-sm">
          <HebrewText size="lg" className="font-bold block">
            {tooltip.he}
          </HebrewText>
          {tooltip.translit && (
            <span className="text-muted-foreground">{tooltip.translit}</span>
          )}
          <span className="ms-2">— {tooltip.ru}</span>
        </div>
      )}
    </div>
  );
}
