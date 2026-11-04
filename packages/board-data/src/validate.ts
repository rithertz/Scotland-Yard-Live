import { TRANSPORT_TYPES } from './types.js';
import type {
  AdjacencyEntry,
  BoardAdjacency,
  BoardDataset,
  DatasetValidation,
  TransportConnection,
  ValidationIssue,
} from './types.js';

const EXPECTED_STATION_IDS = Array.from({ length: 199 }, (_, index) => index + 1);

export function validateBoardDataset(dataset: BoardDataset): DatasetValidation {
  const issues: ValidationIssue[] = [];
  const stationIds = new Set<number>();

  for (const station of dataset.stations) {
    if (!Number.isInteger(station.id) || station.id < 1 || station.id > 199) {
      issues.push({
        code: 'invalid-station-id',
        message: `Station ID ${String(station.id)} must be an integer from 1 through 199.`,
      });
    }
    if (stationIds.has(station.id)) {
      issues.push({
        code: 'duplicate-station-id',
        message: `Station ID ${station.id} is duplicated.`,
      });
    }
    stationIds.add(station.id);

    if (station.coordinate) {
      const { x, y } = station.coordinate;
      if (!Number.isFinite(x) || !Number.isFinite(y) || x < 0 || x > 1 || y < 0 || y > 1) {
        issues.push({
          code: 'invalid-coordinate',
          message: `Station ${station.id} has an invalid normalized coordinate.`,
        });
      }
    }
  }

  if (dataset.metadata.state === 'canonical-complete') {
    if (dataset.stations.length !== 199) {
      issues.push({
        code: 'incomplete-station-count',
        message: 'A canonical-complete dataset must contain exactly 199 stations.',
      });
    }
    for (const id of EXPECTED_STATION_IDS) {
      if (!stationIds.has(id)) {
        issues.push({ code: 'missing-station-id', message: `Station ID ${id} is missing.` });
      }
    }
    for (const station of dataset.stations) {
      if (!station.coordinate) {
        issues.push({
          code: 'missing-coordinate',
          message: `Station ${station.id} has no coordinate.`,
        });
      }
      if (!['verified-from-physical-board', 'cross-checked'].includes(station.coordinateStatus)) {
        issues.push({
          code: 'incomplete-coordinate-verification',
          message: `Station ${station.id} does not have a verified coordinate status.`,
        });
      }
    }
  }

  const edgeKeys = new Set<string>();
  for (const connection of dataset.connections) {
    validateConnection(connection, stationIds, edgeKeys, issues);
    if (
      dataset.metadata.state === 'canonical-complete' &&
      !isVerified(connection.verificationStatus)
    ) {
      issues.push({
        code: 'incomplete-verification',
        message: `Connection ${connection.from}-${connection.to} (${connection.transport}) is not verified.`,
      });
    }
  }

  return { valid: issues.length === 0, issues };
}

function validateConnection(
  connection: TransportConnection,
  stationIds: ReadonlySet<number>,
  edgeKeys: Set<string>,
  issues: ValidationIssue[],
) {
  if (!Number.isInteger(connection.from) || !Number.isInteger(connection.to)) {
    issues.push({
      code: 'invalid-edge-endpoint',
      message: 'Connection endpoints must be integers.',
    });
  }
  if (!stationIds.has(connection.from) || !stationIds.has(connection.to)) {
    issues.push({
      code: 'unknown-edge-endpoint',
      message: `Connection ${connection.from}-${connection.to} references a station not in this dataset.`,
    });
  }
  if (connection.from === connection.to) {
    issues.push({
      code: 'self-connection',
      message: `Station ${connection.from} cannot connect to itself.`,
    });
  }
  if (connection.from >= connection.to) {
    issues.push({
      code: 'non-canonical-edge-order',
      message: `Connection endpoints must be stored in ascending order: ${connection.from}-${connection.to}.`,
    });
  }
  if (!(TRANSPORT_TYPES as readonly string[]).includes(connection.transport)) {
    issues.push({
      code: 'invalid-transport',
      message: `Connection ${connection.from}-${connection.to} has an invalid transport type.`,
    });
  }
  const key = `${connection.from}:${connection.to}:${connection.transport}`;
  if (edgeKeys.has(key)) {
    issues.push({ code: 'duplicate-edge', message: `Connection ${key} is duplicated.` });
  }
  edgeKeys.add(key);
}

function isVerified(status: TransportConnection['verificationStatus']) {
  return (
    status === 'verified-from-physical-board' ||
    status === 'verified-from-rulebook' ||
    status === 'cross-checked'
  );
}

/** Expands each stored undirected edge into both legal travel directions at runtime. */
export function createAdjacency(
  dataset: Pick<BoardDataset, 'stations' | 'connections'>,
): BoardAdjacency {
  const adjacency = new Map<number, AdjacencyEntry[]>();
  for (const station of dataset.stations) adjacency.set(station.id, []);
  for (const connection of dataset.connections) {
    adjacency
      .get(connection.from)
      ?.push({ stationId: connection.to, transport: connection.transport });
    adjacency
      .get(connection.to)
      ?.push({ stationId: connection.from, transport: connection.transport });
  }
  return adjacency;
}

export function hasSymmetricAdjacency(
  dataset: Pick<BoardDataset, 'stations' | 'connections'>,
): boolean {
  const adjacency = createAdjacency(dataset);
  return dataset.connections.every((connection) => {
    const forward = adjacency.get(connection.from) ?? [];
    const reverse = adjacency.get(connection.to) ?? [];
    return (
      forward.some(
        (entry) => entry.stationId === connection.to && entry.transport === connection.transport,
      ) &&
      reverse.some(
        (entry) => entry.stationId === connection.from && entry.transport === connection.transport,
      )
    );
  });
}
