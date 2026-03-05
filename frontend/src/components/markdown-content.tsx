export function MarkdownContent({ content }: { content: string }) {
  const lines = content.split("\n");
  const elements: JSX.Element[] = [];
  let tableRows: string[][] = [];
  let inTable = false;

  const processInline = (text: string) => {
    return text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  };

  const flushTable = (key: string) => {
    if (tableRows.length === 0) return;
    elements.push(
      <div key={key} className="overflow-x-auto my-3">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr>
              {tableRows[0].map((h, j) => (
                <th key={j} className="border px-3 py-1.5 bg-muted text-left font-medium">
                  <span dangerouslySetInnerHTML={{ __html: processInline(h) }} />
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {tableRows.slice(1).map((row, ri) => (
              <tr key={ri}>
                {row.map((cell, ci) => (
                  <td key={ci} className="border px-3 py-1.5">
                    <span dangerouslySetInnerHTML={{ __html: processInline(cell) }} />
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
      elements.push(<div key={i} className="h-2" />);
    } else if (line.startsWith("#### ")) {
      elements.push(
        <h4 key={i} className="text-sm font-semibold mt-3 mb-1">
          <span dangerouslySetInnerHTML={{ __html: processInline(line.slice(5)) }} />
        </h4>
      );
    } else if (line.startsWith("### ")) {
      elements.push(
        <h3 key={i} className="text-base font-semibold mt-4 mb-1">
          <span dangerouslySetInnerHTML={{ __html: processInline(line.slice(4)) }} />
        </h3>
      );
    } else if (line.startsWith("## ")) {
      elements.push(
        <h2 key={i} className="text-lg font-bold mt-5 mb-2">
          <span dangerouslySetInnerHTML={{ __html: processInline(line.slice(3)) }} />
        </h2>
      );
    } else if (line.startsWith("- ")) {
      elements.push(
        <li key={i} className="ml-4 text-sm list-disc">
          <span dangerouslySetInnerHTML={{ __html: processInline(line.slice(2)) }} />
        </li>
      );
    } else {
      elements.push(
        <p key={i} className="text-sm">
          <span dangerouslySetInnerHTML={{ __html: processInline(line) }} />
        </p>
      );
    }
  }

  flushTable("table-end");

  return <div className="space-y-1">{elements}</div>;
}
