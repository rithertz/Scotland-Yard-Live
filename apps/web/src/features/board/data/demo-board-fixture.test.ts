import { describe, expect, it } from 'vitest';
import { DEMO_BOARD_FIXTURE } from './demo-board-fixture.js';

describe('demo board boundary', () => {
  it('keeps the visual fixture separate from canonical station numbering', () => {
    expect(DEMO_BOARD_FIXTURE.stations).toHaveLength(28);
    expect(DEMO_BOARD_FIXTURE.stations.every((station) => /^[A-E][1-6]$/.test(station.id))).toBe(
      true,
    );
  });

  it('keeps transport edges typed and connected to fixture stations', () => {
    const ids = new Set(DEMO_BOARD_FIXTURE.stations.map((station) => station.id));
    expect(DEMO_BOARD_FIXTURE.edges.length).toBeGreaterThan(40);
    expect(DEMO_BOARD_FIXTURE.edges.every((edge) => ids.has(edge.from) && ids.has(edge.to))).toBe(
      true,
    );
    expect(new Set(DEMO_BOARD_FIXTURE.edges.map((edge) => edge.type))).toEqual(
      new Set(['taxi', 'bus', 'underground']),
    );
  });
});
