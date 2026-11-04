/** Types deliberately independent of React, SVG, Vite, and the game engine. */
export const TRANSPORT_TYPES = ['taxi', 'bus', 'underground', 'boat'] as const;
export type TransportType = (typeof TRANSPORT_TYPES)[number];

export const VERIFICATION_STATUSES = [
  'verified-from-physical-board',
  'verified-from-rulebook',
  'cross-checked',
  'candidate-unverified',
  'unresolved',
] as const;
export type VerificationStatus = (typeof VERIFICATION_STATUSES)[number];

export type SourceReference = {
  /** Stable local or remote identifier, e.g. a page number or immutable source URL. */
  id: string;
  description: string;
  status: VerificationStatus;
};

/** Resolution-independent board position, normalized to the closed interval [0, 1]. */
export type NormalizedCoordinate = { x: number; y: number };

export type BoardStation = {
  id: number;
  coordinate?: NormalizedCoordinate;
  coordinateStatus: VerificationStatus;
  provenance?: SourceReference;
};

/** A single undirected transport edge. `from` must be numerically less than `to`. */
export type TransportConnection = {
  from: number;
  to: number;
  transport: TransportType;
  verificationStatus: VerificationStatus;
  provenance?: SourceReference;
};

export type BoardEdition = {
  id: string;
  name: string;
  manufacturer: string;
  productCode: string;
  stationCount: number;
};

export type BoardDatasetState = 'canonical-complete' | 'incomplete-verification';

export type BoardDataset = {
  metadata: {
    edition: BoardEdition;
    datasetVersion: string;
    coordinateSystem: 'normalized-0-to-1';
    state: BoardDatasetState;
    provenance: readonly SourceReference[];
  };
  stations: readonly BoardStation[];
  connections: readonly TransportConnection[];
};

export type ValidationIssue = {
  code:
    | 'invalid-station-id'
    | 'duplicate-station-id'
    | 'missing-station-id'
    | 'incomplete-station-count'
    | 'invalid-coordinate'
    | 'missing-coordinate'
    | 'incomplete-coordinate-verification'
    | 'invalid-edge-endpoint'
    | 'unknown-edge-endpoint'
    | 'self-connection'
    | 'non-canonical-edge-order'
    | 'duplicate-edge'
    | 'invalid-transport'
    | 'incomplete-verification';
  message: string;
};

export type DatasetValidation = { valid: boolean; issues: readonly ValidationIssue[] };

export type AdjacencyEntry = { stationId: number; transport: TransportType };
export type BoardAdjacency = ReadonlyMap<number, readonly AdjacencyEntry[]>;
