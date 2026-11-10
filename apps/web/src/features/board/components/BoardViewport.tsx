import { useEffect, useState } from 'react';
import { DEFAULT_BOARD_TRANSFORM, panBoardTransform, wheelZoomFactor, zoomBoardTransform, type BoardTransform } from '../board-transform.js';
import type { ReconstructedBoard } from '../types.js';
import { BoardSvg } from './BoardSvg.js';

export type ViewTransform = BoardTransform;

export function BoardViewport({
  board,
  selectedId,
  onSelect,
}: {
  board: ReconstructedBoard;
  selectedId: number | null;
  onSelect: (id: number) => void;
}) {
  const [view, setView] = useState(DEFAULT_BOARD_TRANSFORM);
  const [drag, setDrag] = useState<{ x: number; y: number; view: ViewTransform } | null>(null);
  const zoom = (factor: number) => setView((current) => zoomBoardTransform(current, factor));
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === '+' || event.key === '=') zoom(1.12);
      if (event.key === '-') zoom(0.89);
      if (event.key === '0') setView(DEFAULT_BOARD_TRANSFORM);
      if (event.key === 'Escape') onSelect(0);
      if (event.key.toLowerCase() === 'f') setView(DEFAULT_BOARD_TRANSFORM);
      if (event.key.startsWith('Arrow')) {
        event.preventDefault();
        const dx = event.key === 'ArrowLeft' ? 18 : event.key === 'ArrowRight' ? -18 : 0;
        const dy = event.key === 'ArrowUp' ? 18 : event.key === 'ArrowDown' ? -18 : 0;
        setView((current) => panBoardTransform(current, dx, dy));
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });
  return (
    <section className="board-panel" aria-label="Provisional Scotland Yard board preview">
      <div className="board-panel-head">
        <div>
          <span className="section-kicker">METROPOLITAN GRID</span>
          <h2>1985 London board / station evidence</h2>
        </div>
        <span className="demo-stamp">PROVISIONAL · NOT CANONICAL</span>
      </div>
      <div
        className="board-stage"
        tabIndex={0}
        role="application"
        aria-label="Interactive provisional board. Use plus and minus to zoom, F to fit, arrow keys to pan, and Escape to clear selection."
        onWheelCapture={(event) => {
          event.preventDefault();
          zoom(wheelZoomFactor(event.deltaY));
        }}
        onPointerDown={(event) => {
          if ((event.target as Element).closest('[data-station]')) return;
          setDrag({ x: event.clientX, y: event.clientY, view });
          (event.currentTarget as HTMLElement).setPointerCapture(event.pointerId);
        }}
        onPointerMove={(event) => {
          if (drag) setView(panBoardTransform(drag.view, (event.clientX - drag.x) / 2, (event.clientY - drag.y) / 2));
        }}
        onPointerUp={() => setDrag(null)}
      >
        <BoardSvg board={board} view={view} selectedId={selectedId} onSelect={onSelect} />
        <div className="board-controls">
          <button onClick={() => zoom(1.16)} aria-label="Zoom in">
            +
          </button>
          <button onClick={() => zoom(0.86)} aria-label="Zoom out">
            −
          </button>
          <button onClick={() => setView(DEFAULT_BOARD_TRANSFORM)} aria-label="Reset board view">
            ↺
          </button>
          <button onClick={() => setView(DEFAULT_BOARD_TRANSFORM)} aria-label="Fit board to viewport">
            ⛶
          </button>
        </div>
        <div className="map-legend">
          <span><i className="legend-marker verified" /> VERIFIED IDENTITY</span>
          <span><i className="legend-marker candidate" /> CANDIDATE / UNVERIFIED</span>
        </div>
      </div>
    </section>
  );
}
