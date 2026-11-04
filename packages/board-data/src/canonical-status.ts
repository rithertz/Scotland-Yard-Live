import type { BoardEdition, SourceReference } from './types.js';

export const TARGET_EDITION: BoardEdition = {
  id: 'milton-bradley-funskool-1985-4500-x2',
  name: 'Scotland Yard (1985 Central London board)',
  manufacturer: 'Milton Bradley; manufactured under licence by Funskool (India) Ltd.',
  productCode: '4500-X2',
  stationCount: 199,
};

export const RECONSTRUCTION_SOURCES: readonly SourceReference[] = [
  {
    id: 'supplied-rulebook-page-10',
    description: 'Supplied original rules PDF, page 10: Thames boat-route wording.',
    status: 'verified-from-rulebook',
  },
  {
    id: 'supplied-physical-board-photographs',
    description: 'User-supplied photographs of the Funskool/Milton Bradley board.',
    status: 'verified-from-physical-board',
  },
];

/**
 * There is intentionally no exported canonical board dataset yet. The available
 * photographs are not a traceable source for all 199 coordinates and the
 * candidate graphs conflict with the rulebook's Thames route. Consumers must
 * not silently substitute candidate data for this target edition.
 */
export const CANONICAL_DATASET_AVAILABILITY = {
  available: false,
  state: 'incomplete-verification' as const,
  reason:
    'Topology and coordinates remain incomplete pending a straight-on, high-resolution board source and edge-by-edge verification.',
};

/** Direct rulebook evidence only; not a complete topology and never renderer input. */
export const VERIFIED_BOAT_CONNECTIONS = [
  { from: 115, to: 118 },
  { from: 115, to: 157 },
  { from: 157, to: 194 },
] as const;
