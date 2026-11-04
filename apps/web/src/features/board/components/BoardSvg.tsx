import type { BoardFixture, DemoEdge, DemoStation } from '../types.js';
import type { ViewTransform } from './BoardViewport.js';
const colors = { taxi: '#d6a928', bus: '#39846a', underground: '#b94a4b', boat: '#4f86a5' };

export function BoardSvg({
  fixture,
  view,
  selectedId,
  onSelect,
}: {
  fixture: BoardFixture;
  view: ViewTransform;
  selectedId: string | null;
  onSelect: (id: string) => void;
}) {
  const map = new Map(fixture.stations.map((station) => [station.id, station]));
  const station = selectedId ? map.get(selectedId) : undefined;
  const connected = fixture.edges
    .filter((edge) => edge.from === selectedId || edge.to === selectedId)
    .map((edge) => (edge.from === selectedId ? edge.to : edge.from));
  const point = (id: string) => map.get(id)?.position ?? { x: 0, y: 0 };
  return (
    <svg className="board-svg" viewBox="0 0 1000 680" preserveAspectRatio="xMidYMid meet">
      <defs>
        <pattern id="paperGrid" width="28" height="28" patternUnits="userSpaceOnUse">
          <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#8a795b" strokeOpacity=".08" />
        </pattern>
        <filter id="paperNoise">
          <feTurbulence baseFrequency=".8" numOctaves="2" seed="2" result="noise" />
          <feColorMatrix in="noise" type="saturate" values="0" />
          <feComponentTransfer>
            <feFuncA type="table" tableValues="0 .08" />
          </feComponentTransfer>
          <feBlend in="SourceGraphic" mode="multiply" />
        </filter>
      </defs>
      <g transform={`translate(${view.x} ${view.y}) scale(${view.scale})`}>
        <rect width="1000" height="680" fill="#f3ebdd" />
        <path
          d="M0 154 C190 118 275 204 436 161 S746 84 1000 144"
          fill="none"
          stroke="#d3c1a4"
          strokeWidth="94"
          opacity=".28"
        />
        <path
          d="M0 466 C160 420 270 510 412 452 S738 404 1000 474"
          fill="none"
          stroke="#d3c1a4"
          strokeWidth="112"
          opacity=".25"
        />
        <path
          d="M-50 382 C240 345 360 421 512 390 S806 310 1045 350"
          fill="none"
          stroke="#4f86a5"
          strokeOpacity=".2"
          strokeWidth="34"
        />
        <path
          d="M-50 382 C240 345 360 421 512 390 S806 310 1045 350"
          fill="none"
          stroke="#4f86a5"
          strokeOpacity=".65"
          strokeWidth="3"
          strokeDasharray="12 10"
        />
        <rect width="1000" height="680" fill="url(#paperGrid)" filter="url(#paperNoise)" />
        <g className="cartographic-labels" aria-hidden="true">
          <text x="54" y="46">
            NORTHBANK / ILLUSTRATIVE STUDY
          </text>
          <text x="770" y="146">
            EAST END
          </text>
          <text x="58" y="418">
            WEST END
          </text>
          <text x="440" y="446">
            CIVIC QUARTER
          </text>
          <text x="690" y="560">
            SOUTHBANK
          </text>
          <path d="M62 55h118M770 155h70M58 427h82M440 455h126M690 569h100" />
        </g>
        <g className="street-lines">
          <path d="M36 128 245 132 338 72 512 118 701 72 964 122" />
          <path d="M18 282 180 244 354 278 502 232 718 270 974 244" />
          <path d="M38 548 211 518 376 548 561 520 740 548 962 514" />
          <path d="M166 14 184 660" />
          <path d="M440 16 426 660" />
          <path d="M748 14 770 660" />
        </g>
        <g>
          {fixture.edges.map((edge, index) => (
            <TransportEdge
              key={`${edge.from}-${edge.to}-${edge.type}-${index}`}
              edge={edge}
              from={point(edge.from)}
              to={point(edge.to)}
              active={connected.includes(edge.from) || connected.includes(edge.to)}
            />
          ))}
        </g>
        <g>
          {fixture.stations.map((item) => (
            <StationMarker
              key={item.id}
              station={item}
              selected={item.id === selectedId}
              connected={connected.includes(item.id)}
              onSelect={onSelect}
            />
          ))}
        </g>
        <g className="pawn-layer">
          <Pawn x={point('B3').x} y={point('B3').y} color="#b93636" label="X" />
          <Pawn x={point('D4').x} y={point('D4').y} color="#e4a72e" label="D" />
          <Pawn x={point('C2').x} y={point('C2').y} color="#4f86a5" label="D" />
        </g>
        {station && (
          <g className="selection-callout">
            <path
              d={`M${station.position.x} ${station.position.y - 24} L${station.position.x + 22} ${station.position.y - 70} h120`}
            />
            <rect
              x={station.position.x + 142}
              y={station.position.y - 92}
              width="170"
              height="48"
              rx="2"
            />
            <text x={station.position.x + 155} y={station.position.y - 70}>
              SELECTED DESTINATION
            </text>
            <text className="callout-id" x={station.position.x + 155} y={station.position.y - 52}>
              {station.id} · {station.district.toUpperCase()}
            </text>
          </g>
        )}
      </g>
    </svg>
  );
}
function TransportEdge({
  edge,
  from,
  to,
  active,
}: {
  edge: DemoEdge;
  from: { x: number; y: number };
  to: { x: number; y: number };
  active: boolean;
}) {
  return (
    <line
      className={`transport-edge ${edge.type} ${active ? 'active' : ''}`}
      x1={from.x}
      y1={from.y}
      x2={to.x}
      y2={to.y}
      stroke={colors[edge.type]}
    />
  );
}
function StationMarker({
  station,
  selected,
  connected,
  onSelect,
}: {
  station: DemoStation;
  selected: boolean;
  connected: boolean;
  onSelect: (id: string) => void;
}) {
  return (
    <g
      data-station="true"
      className={`station-marker ${selected ? 'selected' : ''} ${connected ? 'connected' : ''}`}
      role="button"
      tabIndex={0}
      aria-label={`Select ${station.name}`}
      onClick={(event) => {
        event.stopPropagation();
        onSelect(station.id);
      }}
      onKeyDown={(event) => {
        if (event.key === 'Enter' || event.key === ' ') onSelect(station.id);
      }}
    >
      <circle className="station-hit" cx={station.position.x} cy={station.position.y} r="22" />
      <circle className="station-ring" cx={station.position.x} cy={station.position.y} r="10" />
      <text x={station.position.x} y={station.position.y + 3.5} textAnchor="middle">
        {station.id}
      </text>
    </g>
  );
}
function Pawn({ x, y, color, label }: { x: number; y: number; color: string; label: string }) {
  return (
    <g className="pawn">
      <circle cx={x + 5} cy={y + 5} r="13" fill="#202a32" opacity=".22" />
      <path
        d={`M${x} ${y - 14} a10 10 0 1 1 0 20 a8 8 0 0 0 -8 8 h16 a8 8 0 0 0 -8 -8`}
        fill={color}
        stroke="#f3ebdd"
        strokeWidth="2"
      />
      <text x={x} y={y + 4} textAnchor="middle">
        {label}
      </text>
    </g>
  );
}
