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
  const isDrawingRef = useRef(false);
  const currentStrokeRef = useRef<StrokePoint[]>([]);
  const strokesRef = useRef<StrokePoint[][]>([]);
  const [strokeCount, setStrokeCount] = useState(0); // trigger re-render for button state
  const size = 300;

  const drawAll = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, size, size);

    // Draw template ghost
    if (showTemplate) {
      ctx.strokeStyle = "rgba(200, 200, 200, 0.4)";
      ctx.lineWidth = 8;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";
      for (const stroke of template.strokes) {
        ctx.beginPath();
        stroke.forEach((p, i) => {
          if (i === 0) ctx.moveTo(p.x * size, p.y * size);
          else ctx.lineTo(p.x * size, p.y * size);
        });
        ctx.stroke();
      }
    }

    // Draw completed strokes
    ctx.strokeStyle = "#2563eb";
    ctx.lineWidth = 4;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    for (const stroke of strokesRef.current) {
      if (stroke.length < 2) continue;
      ctx.beginPath();
      stroke.forEach((p, i) => {
        if (i === 0) ctx.moveTo(p.x * size, p.y * size);
        else ctx.lineTo(p.x * size, p.y * size);
      });
      ctx.stroke();
    }

    // Draw current in-progress stroke
    if (currentStrokeRef.current.length >= 2) {
      ctx.beginPath();
      currentStrokeRef.current.forEach((p, i) => {
        if (i === 0) ctx.moveTo(p.x * size, p.y * size);
        else ctx.lineTo(p.x * size, p.y * size);
      });
      ctx.stroke();
    }
  }, [template, showTemplate]);

  // Redraw when template/showTemplate changes or strokes are added/cleared
  useEffect(() => { drawAll(); }, [drawAll, strokeCount]);

  const getPos = (e: React.MouseEvent | React.TouchEvent): StrokePoint => {
    const canvas = canvasRef.current!;
    const rect = canvas.getBoundingClientRect();
    const scaleX = size / rect.width;
    const scaleY = size / rect.height;
    let clientX: number, clientY: number;
    if ("touches" in e && e.touches.length > 0) {
      clientX = e.touches[0].clientX;
      clientY = e.touches[0].clientY;
    } else if ("clientX" in e) {
      clientX = e.clientX;
      clientY = e.clientY;
    } else {
      return { x: 0, y: 0 };
    }
    return {
      x: (clientX - rect.left) * scaleX / size,
      y: (clientY - rect.top) * scaleY / size,
    };
  };

  const startDraw = (e: React.MouseEvent | React.TouchEvent) => {
    e.preventDefault();
    isDrawingRef.current = true;
    currentStrokeRef.current = [getPos(e)];
  };

  const moveDraw = (e: React.MouseEvent | React.TouchEvent) => {
    if (!isDrawingRef.current) return;
    e.preventDefault();
    const p = getPos(e);
    currentStrokeRef.current.push(p);

    // Draw just the new segment for performance
    const ctx = canvasRef.current?.getContext("2d");
    if (!ctx) return;
    const pts = currentStrokeRef.current;
    if (pts.length < 2) return;
    ctx.strokeStyle = "#2563eb";
    ctx.lineWidth = 4;
    ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(pts[pts.length - 2].x * size, pts[pts.length - 2].y * size);
    ctx.lineTo(p.x * size, p.y * size);
    ctx.stroke();
  };

  const endDraw = () => {
    if (!isDrawingRef.current) return;
    isDrawingRef.current = false;
    if (currentStrokeRef.current.length > 1) {
      strokesRef.current = [...strokesRef.current, currentStrokeRef.current];
      setStrokeCount(c => c + 1);
    }
    currentStrokeRef.current = [];
  };

  const handleClear = () => {
    strokesRef.current = [];
    currentStrokeRef.current = [];
    isDrawingRef.current = false;
    setStrokeCount(0);
    drawAll();
  };

  const handleCheck = () => {
    if (strokesRef.current.length === 0) return;
    const score = compareStrokes(strokesRef.current, template.strokes);
    onScore(score);
  };

  return (
    <div className="flex flex-col items-center gap-3">
      <canvas
        ref={canvasRef}
        width={size}
        height={size}
        className="border-2 border-border rounded-lg bg-background cursor-crosshair touch-none"
        style={{ width: size, height: size }}
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
        <Button onClick={handleCheck} disabled={strokeCount === 0}>Проверить</Button>
      </div>
    </div>
  );
}
