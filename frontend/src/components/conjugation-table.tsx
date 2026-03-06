import { useState } from "react";
import { HebrewText } from "@/components/hebrew-text";
import { cn } from "@/lib/utils";

export interface TableCell {
  person: string;
  gender: string;
  number: string;
  form_he: string;
  form_nikkud: string | null;
  transliteration: string | null;
  is_blank: boolean;
}

interface ConjugationTableProps {
  cells: TableCell[];
  onSubmit: (answers: Record<string, string>) => void;
  results?: Record<string, boolean>;
  disabled?: boolean;
}

const PERSON_LABELS: Record<string, string> = {
  "1": "Я / Мы",
  "2": "Ты / Вы",
  "3": "Он/Она / Они",
};

export function ConjugationTable({ cells, onSubmit, results, disabled }: ConjugationTableProps) {
  const [answers, setAnswers] = useState<Record<string, string>>({});

  const cellKey = (c: TableCell) => `${c.person}-${c.gender}-${c.number}`;

  const handleChange = (key: string, value: string) => {
    setAnswers(prev => ({ ...prev, [key]: value }));
  };

  const handleSubmit = () => {
    onSubmit(answers);
  };

  const rows = cells.reduce<Record<string, TableCell[]>>((acc, cell) => {
    const key = `${cell.person}-${cell.number}`;
    if (!acc[key]) acc[key] = [];
    acc[key].push(cell);
    return acc;
  }, {});

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr className="border-b">
            <th className="p-2 text-left text-muted-foreground">Лицо</th>
            <th className="p-2 text-center text-muted-foreground">Муж.</th>
            <th className="p-2 text-center text-muted-foreground">Жен.</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(rows).map(([rowKey, rowCells]) => {
            const person = rowCells[0].person;
            const number = rowCells[0].number;
            const masc = rowCells.find(c => c.gender === "masculine" || c.gender === "m");
            const fem = rowCells.find(c => c.gender === "feminine" || c.gender === "f");

            const renderCell = (cell: TableCell | undefined) => {
              if (!cell) return <td className="p-2 text-center text-muted-foreground">—</td>;
              const key = cellKey(cell);
              if (!cell.is_blank) {
                return (
                  <td className="p-2 text-center">
                    <HebrewText size="lg">{cell.form_nikkud || cell.form_he}</HebrewText>
                    {cell.transliteration && (
                      <p className="text-xs text-muted-foreground">{cell.transliteration}</p>
                    )}
                  </td>
                );
              }
              return (
                <td className="p-2 text-center">
                  {results ? (
                    <div className={cn(
                      "p-1.5 rounded",
                      results[key] ? "bg-green-50 dark:bg-green-950/30" : "bg-red-50 dark:bg-red-950/30"
                    )}>
                      <HebrewText size="lg" className="font-bold">{cell.form_nikkud || cell.form_he}</HebrewText>
                      {!results[key] && answers[key] && (
                        <p className="text-xs text-red-500 line-through font-hebrew">{answers[key]}</p>
                      )}
                    </div>
                  ) : (
                    <input
                      dir="rtl"
                      className="w-full text-center font-hebrew text-lg border rounded px-2 py-1 bg-background"
                      value={answers[key] || ""}
                      onChange={e => handleChange(key, e.target.value)}
                      disabled={disabled}
                      placeholder="?"
                    />
                  )}
                </td>
              );
            };

            return (
              <tr key={rowKey} className="border-b">
                <td className="p-2 text-muted-foreground text-xs">
                  {PERSON_LABELS[person] || person} ({number === "singular" || number === "s" ? "ед." : "мн."})
                </td>
                {renderCell(masc)}
                {renderCell(fem)}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
