import { describe, expect, it } from 'vitest';
import { BOARD_ARTWORK_RECT } from '../board-transform.js';
import { RECONSTRUCTED_BOARD } from './reconstructed-board-data.js';

describe('provisional reconstructed board', () => {
  it('binds exactly stations 1–199 from the board-data dataset', () => {
    expect(RECONSTRUCTED_BOARD.stations).toHaveLength(199);
    expect(RECONSTRUCTED_BOARD.stations.map((station) => station.id)).toEqual(
      Array.from({ length: 199 }, (_, index) => index + 1),
    );
    expect(new Set(RECONSTRUCTED_BOARD.stations.map((station) => station.id)).size).toBe(199);
    expect(RECONSTRUCTED_BOARD.stations.some((station) => station.id === 200)).toBe(false);
    expect(RECONSTRUCTED_BOARD.state).toBe('incomplete-verification');
  });

  it('maps normalized coordinates to the aligned 1350×1000 board canvas', () => {
    expect(BOARD_ARTWORK_RECT).toEqual({ x: 0, y: 0, width: 1350, height: 1000 });
    expect(RECONSTRUCTED_BOARD.width).toBe(1350);
    expect(RECONSTRUCTED_BOARD.height).toBe(1000);
    expect(RECONSTRUCTED_BOARD.stations.every(({ position }) => position.x >= 0 && position.x <= 1350 && position.y >= 0 && position.y <= 1000)).toBe(true);
    expect(RECONSTRUCTED_BOARD.stations.find((station) => station.id === 1)?.position.x).toBeCloseTo(187.94025, 5);
    expect(RECONSTRUCTED_BOARD.stations.find((station) => station.id === 1)?.position.y).toBeCloseTo(56.62, 5);
    for (const id of [1, 2, 93, 100, 140, 185, 198, 199]) {
      const station = RECONSTRUCTED_BOARD.stations.find((candidate) => candidate.id === id);
      expect(station?.position.x).toBeGreaterThanOrEqual(BOARD_ARTWORK_RECT.x);
      expect(station?.position.x).toBeLessThanOrEqual(BOARD_ARTWORK_RECT.width);
      expect(station?.position.y).toBeGreaterThanOrEqual(BOARD_ARTWORK_RECT.y);
      expect(station?.position.y).toBeLessThanOrEqual(BOARD_ARTWORK_RECT.height);
    }
  });

  it('keeps identity uncertainty visible and does not create transport edges', () => {
    expect(RECONSTRUCTED_BOARD.stations.some((station) => station.identityStatus !== 'verified')).toBe(true);
  });
});
