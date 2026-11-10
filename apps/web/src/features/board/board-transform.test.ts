import { describe, expect, it } from 'vitest';
import { boardCoordinateToSurfacePoint, boardSurfaceTransform, DEFAULT_BOARD_TRANSFORM, panBoardTransform, wheelZoomFactor, zoomBoardTransform } from './board-transform.js';

describe('unified board surface transform', () => {
  it('maps normalized coordinates onto the canonical board surface', () => {
    expect(boardCoordinateToSurfacePoint({ width: 1350, height: 1000 }, { x: 0.25, y: 0.75 })).toEqual({ x: 337.5, y: 750 });
  });

  it('uses one transform string for the artwork and station overlay surface', () => {
    const transform = panBoardTransform(zoomBoardTransform(DEFAULT_BOARD_TRANSFORM, 1.5), 24, -12);
    expect(boardSurfaceTransform(transform)).toBe('translate(24 -12) scale(1.5)');
  });

  it('keeps zoom and pan bounded and deterministic across viewport aspect ratios', () => {
    expect(zoomBoardTransform(DEFAULT_BOARD_TRANSFORM, 10).scale).toBe(2.5);
    expect(zoomBoardTransform(DEFAULT_BOARD_TRANSFORM, 0.1).scale).toBe(0.72);
    expect(panBoardTransform(DEFAULT_BOARD_TRANSFORM, 18, -9)).toEqual({ scale: 1, x: 18, y: -9 });
  });

  it('uses the same wheel zoom operation regardless of the event target', () => {
    expect(wheelZoomFactor(-100)).toBe(wheelZoomFactor(-100));
    expect(wheelZoomFactor(100)).toBe(wheelZoomFactor(100));
    expect(wheelZoomFactor(-100)).toBe(1.09);
    expect(wheelZoomFactor(100)).toBe(0.92);
  });
});
