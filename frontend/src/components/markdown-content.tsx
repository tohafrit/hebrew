import { Fragment } from "react";

function parseInline(text: string): (string | JSX.Element)[] {
  const parts: (string | JSX.Element)[] = [];
  const regex = /\*\*(.*?)\*\*/g;
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push(text.slice(lastIndex, match.index));
    }
    parts.push(<strong key={match.index}>{match[1]}</strong>);
    lastIndex = regex.lastIndex;
  }

  if (lastIndex < text.length) {
    parts.push(text.slice(lastIndex));
  }

  return parts.length > 0 ? parts : [text];
}

export function MarkdownContent({ content }: { content: string }) {
  const lines = content.split("\n");
  const elements: JSX.Element[] = [];
  let tableRows: string[][] = [];
  let inTable = false;

  const flushTable = (key: string) => {
    if (tableRows.length === 0) return;
    elements.push(
      <div key={key} className="overflow-x-auto my-3">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr>
              {tableRows[0].map((h, j) => (
                <th key={j} className="border px-3 py-1.5 bg-muted text-left font-medium">
                  {parseInline(h)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tableRows.slice(1).map((row, ri) => (
              <tr key={ri}>
                {row.map((cell, ci) => (
                  <td key={ci} className="border px-3 py-1.5">
                    {parseInline(cell)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
    tableRows = [];
    inTable = false;
  };

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (line.startsWith("|")) {
      const cells = line.split("|").filter((c) => c.trim() !== "").map((c) => c.trim());
      if (cells.some((c) => /^[-:]+$/.test(c))) {
        inTable = true;
        continue;
      }
      tableRows.push(cells);
      if (!inTable) inTable = true;
      continue;
    }

    if (inTable) {
      flushTable(`table-${i}`);
    }

    if (/^-{3,}$/.test(line.trim()) || /^\*{3,}$/.test(line.trim())) {
      elements.push(<hr key={i} className="my-4 border-border" />);
    } else if (line.trim() === "") {
      elements.push(<div key={i} className="h-4" />);
    } else if (line.startsWith("#### ")) {
      elements.push(
        <h4 key={i} className="text-sm font-semibold mt-4 mb-1.5">
          {parseInline(line.slice(5))}
        </h4>
      );
    } else if (line.startsWith("### ")) {
      elements.push(
        <h3 key={i} className="text-base font-semibold mt-5 mb-2">
          {parseInline(line.slice(4))}
        </h3>
      );
    } else if (line.startsWith("## ")) {
      elements.push(
        <h2 key={i} className="text-lg font-bold mt-6 mb-3">
          {parseInline(line.slice(3))}
        </h2>
      );
    } else if (line.startsWith("- ")) {
      elements.push(
        <li key={i} className="ml-4 text-base leading-relaxed list-disc">
          {parseInline(line.slice(2))}
        </li>
      );
    } else {
      elements.push(
        <p key={i} className="text-base leading-relaxed">
          {parseInline(line)}
        </p>
      );
    }
  }

  flushTable("table-end");

  return <div className="space-y-3">{elements}</div>;
}
