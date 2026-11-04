export type TransportType = 'taxi' | 'bus' | 'underground' | 'boat';
export type BoardPoint = { x: number; y: number };
export type DemoStation = { id: string; name: string; position: BoardPoint; district: string };
export type DemoEdge = { from: string; to: string; type: TransportType };
export type BoardFixture = { stations: DemoStation[]; edges: DemoEdge[] };
