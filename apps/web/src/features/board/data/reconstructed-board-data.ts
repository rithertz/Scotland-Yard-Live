import stationsDocument from '../../../../../../packages/board-data/data/stations.json';
import { BOARD_ARTWORK_RECT, boardCoordinateToSurfacePoint } from '../board-transform.js';
import type { ReconstructedBoard } from '../types.js';

type StationRecord = {
  id: number;
  coordinate: { x: number; y: number };
  coordinateStatus: string;
  identityStatus?: string;
  featureId?: string | null;
};

const source = stationsDocument as unknown as {
  metadata: { state: ReconstructedBoard['state'] };
  stations: StationRecord[];
};

export const RECONSTRUCTED_BOARD: ReconstructedBoard = {
  width: BOARD_ARTWORK_RECT.width,
  height: BOARD_ARTWORK_RECT.height,
  state: source.metadata.state,
  stations: source.stations.map((station) => ({
    id: station.id,
    position: boardCoordinateToSurfacePoint(BOARD_ARTWORK_RECT, station.coordinate),
    coordinateStatus: station.coordinateStatus,
    identityStatus: station.identityStatus ?? 'unresolved',
    featureId: station.featureId ?? null,
  })),
};
