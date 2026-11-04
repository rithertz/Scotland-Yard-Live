import { useEffect, useState } from 'react';
import type { BoardFixture } from '../types.js';
import { BoardSvg } from './BoardSvg.js';

export type ViewTransform = { scale: number; x: number; y: number };
const DEFAULT_VIEW: ViewTransform = { scale: 1, x: 0, y: 0 };

export function BoardViewport({
  fixture,
  selectedId,
  onSelect,
}: {
  fixture: BoardFixture;
  selectedId: string | null;
  onSelect: (id: string) => void;
}) {
  const [view, setView] = useState(DEFAULT_VIEW);
  const [drag, setDrag] = useState<{ x: number; y: number; view: ViewTransform } | null>(null);
  const zoom = (factor: number) =>
    setView((current) => ({
      ...current,
      scale: Math.min(2.5, Math.max(0.72, current.scale * factor)),
    }));
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === '+' || event.key === '=') zoom(1.12);
      if (event.key === '-') zoom(0.89);
      if (event.key === '0') setView(DEFAULT_VIEW);
      if (event.key === 'Escape') onSelect('');
      if (event.key.startsWith('Arrow')) {
        event.preventDefault();
        const dx = event.key === 'ArrowLeft' ? 18 : event.key === 'ArrowRight' ? -18 : 0;
        const dy = event.key === 'ArrowUp' ? 18 : event.key === 'ArrowDown' ? -18 : 0;
        setView((current) => ({ ...current, x: current.x + dx, y: current.y + dy }));
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });
  return (
    <section className="board-panel" aria-label="Synthetic board visual prototype">
      <div className="board-panel-head">
        <div>
          <span className="section-kicker">METROPOLITAN GRID</span>
          <h2>London pursuit board</h2>
        </div>
        <span className="demo-stamp">DEMO BOARD · NOT CANONICAL</span>
      </div>
      <div
        className="board-stage"
        tabIndex={0}
        role="application"
        aria-label="Interactive synthetic board. Use plus and minus to zoom, arrow keys to pan."
        onWheel={(event) => {
          event.preventDefault();
          zoom(event.deltaY > 0 ? 0.92 : 1.09);
        }}
        onPointerDown={(event) => {
          if ((event.target as Element).closest('[data-station]')) return;
          setDrag({ x: event.clientX, y: event.clientY, view });
          (event.currentTarget as HTMLElement).setPointerCapture(event.pointerId);
        }}
        onPointerMove={(event) => {
          if (drag)
            setView({
              ...drag.view,
              x: drag.view.x + (event.clientX - drag.x) / 2,
              y: drag.view.y + (event.clientY - drag.y) / 2,
            });
        }}
        onPointerUp={() => setDrag(null)}
      >
        <BoardSvg fixture={fixture} view={view} selectedId={selectedId} onSelect={onSelect} />
        <div className="board-controls">
          <button onClick={() => zoom(1.16)} aria-label="Zoom in">
            +
          </button>
          <button onClick={() => zoom(0.86)} aria-label="Zoom out">
            −
          </button>
          <button onClick={() => setView(DEFAULT_VIEW)} aria-label="Reset board view">
            ↺
          </button>
        </div>
        <div className="map-legend">
          <span>
            <i className="legend-line taxi" /> TAXI
          </span>
          <span>
            <i className="legend-line bus" /> BUS
          </span>
          <span>
            <i className="legend-line underground" /> UNDERGROUND
          </span>
        </div>
      </div>
    </section>
  );
}
