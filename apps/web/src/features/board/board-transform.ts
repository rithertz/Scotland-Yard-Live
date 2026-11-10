import type { ReconstructedBoard } from './types.js';

export type BoardTransform = { scale: number; x: number; y: number };
export const BOARD_ARTWORK_RECT = { x: 0, y: 0, width: 1350, height: 1000 } as const;

export const DEFAULT_BOARD_TRANSFORM: BoardTransform = { scale: 1, x: 0, y: 0 };
export const BOARD_SCALE_LIMITS = { min: 0.72, max: 2.5 } as const;

export function clampBoardScale(scale: number): number {
  return Math.min(BOARD_SCALE_LIMITS.max, Math.max(BOARD_SCALE_LIMITS.min, scale));
}

export function zoomBoardTransform(transform: BoardTransform, factor: number): BoardTransform {
  return { ...transform, scale: clampBoardScale(transform.scale * factor) };
}

export function wheelZoomFactor(deltaY: number): number {
  return deltaY > 0 ? 0.92 : 1.09;
}

export function panBoardTransform(transform: BoardTransform, dx: number, dy: number): BoardTransform {
  return { ...transform, x: transform.x + dx, y: transform.y + dy };
}

export function boardSurfaceTransform(transform: BoardTransform): string {
  return `translate(${transform.x} ${transform.y}) scale(${transform.scale})`;
}

export function boardCoordinateToSurfacePoint(
  board: Pick<ReconstructedBoard, 'width' | 'height'>,
  normalized: { x: number; y: number },
) {
  return { x: normalized.x * board.width, y: normalized.y * board.height };
}
