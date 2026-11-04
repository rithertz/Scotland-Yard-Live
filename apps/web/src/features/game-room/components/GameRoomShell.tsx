import { useState } from 'react';
import { DEMO_BOARD_FIXTURE } from '../../board/data/demo-board-fixture.js';
import { BoardViewport } from '../../board/components/BoardViewport.js';

type Ticket = { name: string; symbol: string; count: number; tone: string };
const tickets: Ticket[] = [
  { name: 'Taxi', symbol: 'T', count: 8, tone: 'taxi' },
  { name: 'Bus', symbol: 'B', count: 3, tone: 'bus' },
  { name: 'Underground', symbol: 'U', count: 4, tone: 'underground' },
  { name: 'Black ticket', symbol: 'X', count: 2, tone: 'black' },
];

export function GameRoomShell() {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [ticket, setTicket] = useState('Taxi');
  const [railOpen, setRailOpen] = useState(false);
  const selectedStation = DEMO_BOARD_FIXTURE.stations.find((station) => station.id === selectedId);
  const selectedRoutes = selectedId
    ? DEMO_BOARD_FIXTURE.edges.filter((edge) => edge.from === selectedId || edge.to === selectedId)
    : [];
  return (
    <main className="room-shell">
      <header className="command-bar">
        <div className="brand-lockup">
          <span className="brand-seal">SY</span>
          <div>
            <strong>
              SCOTLAND YARD <em>LIVE</em>
            </strong>
            <span>METROPOLITAN PURSUIT DIVISION</span>
          </div>
        </div>
        <div className="command-meta">
          <div>
            <span className="meta-label">ROOM</span>
            <b>K7P4</b>
            <button className="copy-button" aria-label="Copy demo room code">
              ⧉
            </button>
          </div>
          <div className="connection">
            <i /> <span>SIMULATED LINK</span>
          </div>
          <div>
            <span className="meta-label">ROUND</span>
            <b>08 / 24</b>
          </div>
          <div>
            <span className="meta-label">PLAYERS</span>
            <b>5 / 6</b>
          </div>
          <button className="icon-button" aria-label="Open room settings">
            ☷
          </button>
        </div>
      </header>
      <div className="room-layout">
        <aside className="left-dossier">
          <div className="dossier-intro">
            <span className="section-kicker">CASE FILE 014</span>
            <h1>The London pursuit</h1>
            <p>Private playtest · visual foundation</p>
          </div>
          <div className="case-rule" />
          <section className="personnel-section">
            <div className="section-heading">
              <span>PERSONNEL</span>
              <small>05 ACTIVE</small>
            </div>
            <div className="personnel-list">
              <Player name="Mr X" detail="Location concealed" color="red" active />
              <Player name="Inspector Hale" detail="Station D4" color="gold" />
              <Player name="Constable Reed" detail="Station C2" color="blue" />
              <Player name="Agent Singh" detail="Awaiting move" color="green" />
            </div>
          </section>
          <div className="left-note">
            <span className="stamp">SIMULATED STATE</span>
            <p>Server-backed room state and rule validation are not connected in this prototype.</p>
          </div>
        </aside>
        <section className="map-column">
          <div className="map-context">
            <span>
              <i className="live-dot" /> LIVE ROOM · DEMO STATE
            </span>
            <span>DRAG TO PAN · WHEEL TO ZOOM</span>
          </div>
          <BoardViewport
            fixture={DEMO_BOARD_FIXTURE}
            selectedId={selectedId}
            onSelect={(id) => setSelectedId(id || null)}
          />
          {selectedStation && (
            <div className="station-inspector">
              <div className="inspector-heading">
                <span className="section-kicker">LOCATION REPORT · ILLUSTRATIVE</span>
                <span className="inspector-state">SELECTED</span>
              </div>
              <div className="inspector-main">
                <strong>{selectedStation.id}</strong>
                <span>{selectedStation.district} district · synthetic node</span>
              </div>
              <div className="inspector-facts">
                <span>
                  <b>{new Set(selectedRoutes.map((route) => route.type)).size}</b> transport types
                </span>
                <span>
                  <b>
                    {selectedId === 'B3' || selectedId === 'C2' || selectedId === 'D4'
                      ? 'OCCUPIED'
                      : 'CLEAR'}
                  </b>{' '}
                  demo occupancy
                </span>
              </div>
              <button onClick={() => setSelectedId(null)}>Clear selection</button>
            </div>
          )}
        </section>
        <aside className={`evidence-rail ${railOpen ? 'open' : ''}`}>
          <button
            className="rail-toggle"
            onClick={() => setRailOpen(!railOpen)}
            aria-expanded={railOpen}
          >
            CASE NOTES <span>{railOpen ? '×' : '＋'}</span>
          </button>
          <div className="rail-content">
            <section className="turn-card">
              <div className="section-heading">
                <span>THE PURSUIT</span>
                <small>TURN 08</small>
              </div>
              <div className="turn-player">
                <span className="turn-avatar">D</span>
                <div>
                  <strong>Inspector Hale</strong>
                  <span>Your move · choose a ticket</span>
                </div>
                <b>02:14</b>
              </div>
              <div className="turn-prompt">
                Select a ticket, then choose an illuminated destination on the board.
              </div>
            </section>
            <section className="folio">
              <div className="section-heading">
                <span>TICKET FOLIO</span>
                <small>DEMO INVENTORY</small>
              </div>
              {tickets.map((item) => (
                <button
                  key={item.name}
                  className={`ticket-row ${ticket === item.name ? 'chosen' : ''}`}
                  onClick={() => setTicket(item.name)}
                >
                  <span className={`ticket-icon ${item.tone}`}>{item.symbol}</span>
                  <span>
                    <strong>{item.name}</strong>
                    <small>{ticket === item.name ? 'SELECTED' : 'AVAILABLE'}</small>
                  </span>
                  <b>{item.count}</b>
                </button>
              ))}
            </section>
            <section className="movement-log">
              <div className="section-heading">
                <span>MOVEMENT RECORD</span>
                <small>PUBLIC LOG</small>
              </div>
              <Log time="07:12" player="Mr X" action="Black ticket · concealed" tone="red" />
              <Log time="06:48" player="Constable Reed" action="Moved to C2" tone="blue" />
              <Log time="06:21" player="Agent Singh" action="Selected bus" tone="green" />
            </section>
          </div>
        </aside>
      </div>
      <footer className="room-footer">
        <span>
          <b>SCOTLAND YARD LIVE</b> / METROPOLITAN CASEFILE
        </span>
        <span>DEMO BOARD DATA IS SYNTHETIC · NO CANONICAL MOVEMENT RULES ACTIVE</span>
      </footer>
    </main>
  );
}
function Player({
  name,
  detail,
  color,
  active,
}: {
  name: string;
  detail: string;
  color: string;
  active?: boolean;
}) {
  return (
    <div className={`player ${active ? 'active' : ''}`}>
      <span className={`player-mark ${color}`}>{name === 'Mr X' ? 'X' : name.slice(0, 1)}</span>
      <span>
        <strong>{name}</strong>
        <small>{detail}</small>
      </span>
      <i className="presence" />
    </div>
  );
}
function Log({
  time,
  player,
  action,
  tone,
}: {
  time: string;
  player: string;
  action: string;
  tone: string;
}) {
  return (
    <div className="log-row">
      <time>{time}</time>
      <span className={`log-pin ${tone}`} />
      <p>
        <strong>{player}</strong>
        <small>{action}</small>
      </p>
    </div>
  );
}
