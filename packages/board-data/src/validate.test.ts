import { describe, expect, it } from 'vitest';
import { createAdjacency, hasSymmetricAdjacency, validateBoardDataset } from './validate.js';
import type { BoardDataset, TransportConnection } from './types.js';

function completeTestDataset(): BoardDataset {
  return {
    metadata: {
      edition: {
        id: 'test',
        name: 'test',
        manufacturer: 'test',
        productCode: 'test',
        stationCount: 199,
      },
      datasetVersion: 'test',
      coordinateSystem: 'normalized-0-to-1',
      state: 'canonical-complete',
      provenance: [],
    },
    stations: Array.from({ length: 199 }, (_, index) => ({
      id: index + 1,
      coordinate: { x: index / 198, y: index / 198 },
      coordinateStatus: 'cross-checked',
    })),
    connections: [
      { from: 1, to: 2, transport: 'taxi', verificationStatus: 'cross-checked' },
      { from: 2, to: 3, transport: 'bus', verificationStatus: 'cross-checked' },
    ],
  };
}

describe('validateBoardDataset', () => {
  it('accepts a complete, internally valid test dataset', () => {
    expect(validateBoardDataset(completeTestDataset())).toEqual({ valid: true, issues: [] });
  });

  it('rejects duplicate and missing station IDs for a complete dataset', () => {
    const dataset = completeTestDataset();
    dataset.stations = dataset.stations.slice(1);
    dataset.stations = [...dataset.stations, { ...dataset.stations[0]!, id: 2 }];
    const result = validateBoardDataset(dataset);
    expect(result.issues.map((issue) => issue.code)).toEqual(
      expect.arrayContaining(['duplicate-station-id', 'missing-station-id']),
    );
  });

  it('rejects invalid and unverified coordinates in a complete dataset', () => {
    const dataset = completeTestDataset();
    dataset.stations = [
      { id: 1, coordinate: { x: Number.NaN, y: 2 }, coordinateStatus: 'unresolved' },
      ...dataset.stations.slice(1),
    ];
    const result = validateBoardDataset(dataset);
    expect(result.issues.map((issue) => issue.code)).toEqual(
      expect.arrayContaining(['invalid-coordinate', 'incomplete-coordinate-verification']),
    );
  });

  it('rejects malformed, duplicate, and unknown edges', () => {
    const dataset = completeTestDataset();
    dataset.connections = [
      { from: 2, to: 1, transport: 'taxi', verificationStatus: 'cross-checked' },
      { from: 1, to: 2, transport: 'taxi', verificationStatus: 'cross-checked' },
      { from: 1, to: 2, transport: 'taxi', verificationStatus: 'cross-checked' },
      { from: 1, to: 999, transport: 'boat', verificationStatus: 'cross-checked' },
      { from: 3, to: 3, transport: 'bus', verificationStatus: 'cross-checked' },
      {
        from: 3,
        to: 4,
        transport: 'tram' as TransportConnection['transport'],
        verificationStatus: 'cross-checked',
      },
    ];
    const result = validateBoardDataset(dataset);
    expect(result.issues.map((issue) => issue.code)).toEqual(
      expect.arrayContaining([
        'non-canonical-edge-order',
        'duplicate-edge',
        'unknown-edge-endpoint',
        'self-connection',
        'invalid-transport',
      ]),
    );
  });

  it('creates bidirectional runtime adjacency from one stored undirected edge', () => {
    const dataset = completeTestDataset();
    const adjacency = createAdjacency(dataset);
    expect(adjacency.get(1)).toContainEqual({ stationId: 2, transport: 'taxi' });
    expect(adjacency.get(2)).toContainEqual({ stationId: 1, transport: 'taxi' });
    expect(hasSymmetricAdjacency(dataset)).toBe(true);
  });

  it('will not accept an incomplete dataset as canonical-complete', () => {
    const dataset = completeTestDataset();
    dataset.metadata.state = 'incomplete-verification';
    dataset.stations = dataset.stations.slice(0, 3);
    dataset.connections = [];
    expect(validateBoardDataset(dataset)).toEqual({ valid: true, issues: [] });

    dataset.metadata.state = 'canonical-complete';
    expect(validateBoardDataset(dataset).valid).toBe(false);
  });
});
