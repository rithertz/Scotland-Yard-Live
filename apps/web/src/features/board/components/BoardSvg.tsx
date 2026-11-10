import type { ReconstructedBoard, ReconstructedStation } from '../types.js';
import { boardSurfaceTransform, type BoardTransform } from '../board-transform.js';

export function BoardSvg({ board, view, selectedId, onSelect }: { board: ReconstructedBoard; view: BoardTransform; selectedId: number | null; onSelect: (id: number) => void }) {
  const selected = board.stations.find((station) => station.id === selectedId);
  return (
    <svg className="board-svg" viewBox={`0 0 ${board.width} ${board.height}`} preserveAspectRatio="xMidYMid meet">
      <g data-board-surface transform={boardSurfaceTransform(view)}>
        <image href="/board/rectified_complete.png" x="0" y="0" width={board.width} height={board.height} preserveAspectRatio="xMidYMid meet" />
        {board.stations.map((station) => <StationMarker key={station.id} station={station} selected={station.id === selectedId} onSelect={onSelect} />)}
        {selected && <SelectionCallout station={selected} />}
      </g>
    </svg>
  );
}

function StationMarker({ station, selected, onSelect }: { station: ReconstructedStation; selected: boolean; onSelect: (id: number) => void }) {
  const verified = station.identityStatus === 'verified';
  return (
    <g data-station={station.id} className={`station-marker ${verified ? 'verified' : 'candidate'} ${selected ? 'selected' : ''}`} role="button" tabIndex={0} aria-label={`Select station ${station.id}${verified ? ', verified identity' : ', provisional identity'}`} onClick={(event) => { event.stopPropagation(); onSelect(station.id); }} onKeyDown={(event) => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); onSelect(station.id); } }}>
      <circle className="station-hit" cx={station.position.x} cy={station.position.y} r="18" />
      <circle className="station-ring" cx={station.position.x} cy={station.position.y} r="9" />
      <text x={station.position.x} y={station.position.y + 3.5} textAnchor="middle">{station.id}</text>
    </g>
  );
}

function SelectionCallout({ station }: { station: ReconstructedStation }) {
  const x = Math.min(station.position.x + 16, 1080);
  const y = Math.max(station.position.y - 76, 12);
  return <g className="selection-callout" aria-hidden="true"><path d={`M${station.position.x} ${station.position.y - 10} L${x} ${y + 30}`} /><rect x={x} y={y} width="250" height="58" rx="2" /><text x={x + 12} y={y + 19}>SELECTED STATION</text><text className="callout-id" x={x + 12} y={y + 39}>ST-{String(station.id).padStart(3, '0')} · {station.identityStatus}</text></g>;
}
