import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, it } from 'vitest';
import {
  DEFAULT_BOARD_TRANSFORM,
  panBoardTransform,
  zoomBoardTransform,
} from '../board-transform.js';
import { RECONSTRUCTED_BOARD } from '../data/reconstructed-board-data.js';
import { BoardSvg } from './BoardSvg.js';

function renderBoard(selectedId: number | null = null, transform = DEFAULT_BOARD_TRANSFORM) {
  return renderToStaticMarkup(
    <BoardSvg
      board={RECONSTRUCTED_BOARD}
      view={transform}
      selectedId={selectedId}
      onSelect={() => undefined}
    />,
  );
}

function markerIds(markup: string): number[] {
  return [...markup.matchAll(/data-station="(\d+)"/g)].map((match) => Number(match[1]));
}

describe('rendered provisional board SVG', () => {
  it('renders exactly one marker for every station 1–199', () => {
    const ids = markerIds(renderBoard());
    expect(ids).toHaveLength(199);
    expect(new Set(ids).size).toBe(199);
    expect(ids).toEqual(Array.from({ length: 199 }, (_, index) => index + 1));
  });

  it('keeps every marker after selection and shared transform changes', () => {
    const transformed = panBoardTransform(
      zoomBoardTransform(DEFAULT_BOARD_TRANSFORM, 1.6),
      42,
      -18,
    );
    const markup = renderBoard(100, transformed);
    expect(markerIds(markup)).toHaveLength(199);
    expect(markup).toContain('data-board-surface="true"');
    expect(markup).toContain('transform="translate(42 -18) scale(1.6)"');
    expect(markup).toContain('ST-100');
  });

  it('places representative markers inside the logical artwork rectangle', () => {
    for (const id of [1, 2, 93, 100, 140, 185, 198, 199]) {
      const station = RECONSTRUCTED_BOARD.stations.find((candidate) => candidate.id === id);
      expect(station?.position.x).toBeGreaterThanOrEqual(0);
      expect(station?.position.x).toBeLessThanOrEqual(RECONSTRUCTED_BOARD.width);
      expect(station?.position.y).toBeGreaterThanOrEqual(0);
      expect(station?.position.y).toBeLessThanOrEqual(RECONSTRUCTED_BOARD.height);
    }
  });
});
