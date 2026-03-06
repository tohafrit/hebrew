import { useRef, useState, useCallback, useEffect } from "react";
import { Button } from "@/components/ui/button";
import type { StrokePoint, LetterTemplate } from "@/data/letter-templates";

interface HandwritingCanvasProps {
  template: LetterTemplate;
  onScore: (score: number) => void;
  showTemplate?: boolean;
}

function resampleStroke(points: StrokePoint[], n: number): StrokePoint[] {
  if (points.length < 2) return points;
  const totalLen = points.reduce((sum, p, i) => {
    if (i === 0) return 0;
    const dx = p.x - points[i - 1].x;
    const dy = p.y - points[i - 1].y;
    return sum + Math.sqrt(dx * dx + dy * dy);
  }, 0);
  if (totalLen === 0) return Array(n).fill(points[0]);

  const step = totalLen / (n - 1);
  const result: StrokePoint[] = [points[0]];
  let dist = 0;
  let j = 1;

  for (let i = 1; i < n; i++) {
    const target = i * step;
    while (j < points.length) {
      const dx = points[j].x - points[j - 1].x;
      const dy = points[j].y - points[j - 1].y;
      const segLen = Math.sqrt(dx * dx + dy * dy);
      if (dist + segLen >= target) {
        const t = (target - dist) / segLen;
        result.push({
          x: points[j - 1].x + t * dx,
          y: points[j - 1].y + t * dy,
        });
        break;
      }
      dist += segLen;
      j++;
    }
    if (result.length <= i) result.push(points[points.length - 1]);
  }
  return result;
}

function normalizeBBox(strokes: StrokePoint[][]): StrokePoint[][] {
  const all = strokes.flat();
  if (all.length === 0) return strokes;
  const minX = Math.min(...all.map(p => p.x));
  const maxX = Math.max(...all.map(p => p.x));
  const minY = Math.min(...all.map(p => p.y));
  const maxY = Math.max(...all.map(p => p.y));
  const w = maxX - minX || 1;
  const h = maxY - minY || 1;
  const scale = Math.max(w, h);
  return strokes.map(s => s.map(p => ({
    x: (p.x - minX) / scale,
    y: (p.y - minY) / scale,
  })));
}

function compareStrokes(drawn: StrokePoint[][], template: StrokePoint[][]): number {
  const N = 32;
  const drawnNorm = normalizeBBox(drawn);
  const templateNorm = normalizeBBox(template);

  const drawnPoints = drawnNorm.flatMap(s => resampleStroke(s, N));
  const templatePoints = templateNorm.flatMap(s => resampleStroke(s, N));

  const len = Math.min(drawnPoints.length, templatePoints.length);
  if (len === 0) return 0;

  let totalDist = 0;
  for (let i = 0; i < len; i++) {
    const dx = drawnPoints[i].x - templatePoints[i].x;
    const dy = drawnPoints[i].y - templatePoints[i].y;
    totalDist += Math.sqrt(dx * dx + dy * dy);
  }
  const avgDist = totalDist / len;
  const score = Math.max(0, Math.min(100, Math.round((1 - avgDist / 0.5) * 100)));
  return score;
}

export function HandwritingCanvas({ template, onScore, showTemplate = true }: HandwritingCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [strokes, setStrokes] = useState<StrokePoint[][]>([]);
  const currentStroke = useRef<StrokePoint[]>([]);
  const size = 300;

  const drawTemplate = useCallback((ctx: CanvasRenderingContext2D) => {
    if (!showTemplate) return;
    ctx.strokeStyle = "rgba(200, 200, 200, 0.4)";
    ctx.lineWidth = 8;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    for (const stroke of template.strokes) {
      ctx.beginPath();
      stroke.forEach((p, i) => {
        const x = p.x * size;
        const y = p.y * size;
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.stroke();
    }
  }, [template, showTemplate]);

  const redraw = useCallback(() => {
    const ctx = canvasRef.current?.getContext("2d");
    if (!ctx) return;
    ctx.clearRect(0, 0, size, size);
    drawTemplate(ctx);

    ctx.strokeStyle = "#2563eb";
    ctx.lineWidth = 4;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    for (const stroke of strokes) {
      ctx.beginPath();
      stroke.forEach((p, i) => {
        if (i === 0) ctx.moveTo(p.x * size, p.y * size);
        else ctx.lineTo(p.x * size, p.y * size);
      });
      ctx.stroke();
    }
  }, [strokes, drawTemplate]);

  useEffect(() => { redraw(); }, [redraw]);

  const getPos = (e: React.MouseEvent | React.TouchEvent): StrokePoint => {
    const rect = canvasRef.current!.getBoundingClientRect();
    const clientX = "touches" in e ? e.touches[0].clientX : e.clientX;
    const clientY = "touches" in e ? e.touches[0].clientY : e.clientY;
    return { x: (clientX - rect.left) / size, y: (clientY - rect.top) / size };
  };

  const startDraw = (e: React.MouseEvent | React.TouchEvent) => {
    e.preventDefault();
    setIsDrawing(true);
    currentStroke.current = [getPos(e)];
  };

  const moveDraw = (e: React.MouseEvent | React.TouchEvent) => {
    if (!isDrawing) return;
    e.preventDefault();
    const p = getPos(e);
    currentStroke.current.push(p);
    const ctx = canvasRef.current?.getContext("2d");
    if (!ctx) return;
    const pts = currentStroke.current;
    ctx.strokeStyle = "#2563eb";
    ctx.lineWidth = 4;
    ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(pts[pts.length - 2].x * size, pts[pts.length - 2].y * size);
    ctx.lineTo(p.x * size, p.y * size);
    ctx.stroke();
  };

  const endDraw = () => {
    if (!isDrawing) return;
    setIsDrawing(false);
    if (currentStroke.current.length > 1) {
      setStrokes(prev => [...prev, currentStroke.current]);
    }
    currentStroke.current = [];
  };

  const handleClear = () => {
    setStrokes([]);
  };

  const handleCheck = () => {
    if (strokes.length === 0) return;
    const score = compareStrokes(strokes, template.strokes);
    onScore(score);
  };

  return (
    <div className="flex flex-col items-center gap-3">
      <canvas
        ref={canvasRef}
        width={size}
        height={size}
        className="border-2 border-border rounded-lg bg-background cursor-crosshair touch-none"
        onMouseDown={startDraw}
        onMouseMove={moveDraw}
        onMouseUp={endDraw}
        onMouseLeave={endDraw}
        onTouchStart={startDraw}
        onTouchMove={moveDraw}
        onTouchEnd={endDraw}
      />
      <div className="flex gap-2">
        <Button variant="outline" onClick={handleClear}>Очистить</Button>
        <Button onClick={handleCheck} disabled={strokes.length === 0}>Проверить</Button>
      </div>
    </div>
  );
}
