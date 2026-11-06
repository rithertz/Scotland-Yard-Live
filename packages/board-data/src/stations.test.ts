import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { validateBoardDataset } from './validate.js';
import type { BoardDataset } from './types.js';

const dataset = JSON.parse(
  readFileSync(new URL('../data/stations.json', import.meta.url), 'utf8'),
) as BoardDataset;

describe('best-effort station reconstruction', () => {
  it('contains all 199 playable stations with normalized coordinates', () => {
    expect(dataset.stations).toHaveLength(199);
    expect(dataset.stations.map((station) => station.id)).toEqual(
      Array.from({ length: 199 }, (_, index) => index + 1),
    );
    expect(dataset.stations.every((station) => station.coordinate)).toBe(true);
    expect(validateBoardDataset(dataset)).toEqual({ valid: true, issues: [] });
  });

  it('keeps marker 200 and transport connections out of the dataset', () => {
    expect(dataset.stations.some((station) => station.id === 200)).toBe(false);
    expect(dataset.connections).toEqual([]);
  });

  it('does not duplicate approximate feature references', () => {
    const featureIds = dataset.stations
      .map((station) => (station as BoardStationWithFeature).featureId)
      .filter((featureId): featureId is string => Boolean(featureId));
    expect(new Set(featureIds).size).toBe(featureIds.length);
  });
});

type BoardStationWithFeature = { featureId?: string };
