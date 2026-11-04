# Scotland Yard Live web application

React 19 + Vite player-facing frontend. The current milestone is the visual foundation: a responsive game-room presentation with a synthetic SVG board and local demo interactions. It is not yet a connected multiplayer client or a canonical implementation of the original board.

## Responsibility and boundaries

The web application owns:

- Presentation of the game-room shell, board, personnel dossier, pursuit desk, tickets, and movement record.
- Client-only visual state such as selected station, selected ticket, and board viewport transform.
- Accessible interaction affordances for the current prototype.

It must not own authoritative game state, movement legality, hidden Mr X locations, canonical board data, or server-side validation. Shared wire schemas belong in `packages/contracts` once the realtime boundary is implemented.

## Frontend structure

```text
apps/web/src/
├── App.tsx
├── main.tsx
├── styles.css
└── features/
    ├── board/
    │   ├── components/
    │   │   ├── BoardSvg.tsx
    │   │   └── BoardViewport.tsx
    │   ├── data/
    │   │   ├── demo-board-fixture.test.ts
    │   │   └── demo-board-fixture.ts
    │   └── types.ts
    └── game-room/
        └── components/
            └── GameRoomShell.tsx
```

`GameRoomShell` composes the command bar, personnel dossier, central board, station inspector, pursuit desk, ticket folio, movement record, and responsive case-notes drawer. `BoardViewport` owns local pan/zoom/reset state and passes typed fixture data to `BoardSvg`. `BoardSvg` renders separate cartographic, route, station, pawn, and selection layers.

## Synthetic board boundary

`src/features/board/data/demo-board-fixture.ts` is an explicitly synthetic visual fixture. Its station IDs, positions, and edges exist only to demonstrate rendering and interaction. The fixture is covered by boundary tests in `demo-board-fixture.test.ts` and is not the source of truth for the eventual Milton Bradley 1985 board.

The current milestone makes no claim of 1:1 board accuracy. Canonical station topology, coordinates, transport connections, starting positions, and rule validation remain future work described by the consolidated project plan.

## Current interactions

- Select a synthetic station by click, keyboard focus, Enter, or Space.
- View the selected station’s illustrative location report and clear it with Escape or the clear action.
- Highlight connected demo routes when a station is selected.
- Select a local demo ticket in the pursuit desk.
- Zoom with the board controls, mouse wheel, `+`, and `-`.
- Pan with click-drag or arrow keys while the board is focused.
- Reset the board view with the reset control or `0`.
- Open and close the case-notes drawer at narrower breakpoints.

These interactions update local presentation state only. They do not submit moves, consume real tickets, validate legal destinations, synchronize players, or reveal authoritative game state.

## Run the web app

From the repository root:

```powershell
corepack pnpm --filter @scotland-yard-live/web dev
```

The Vite development server uses `http://127.0.0.1:5173` by default. The root workspace command `corepack pnpm dev` starts the workspace development tasks in parallel when the complete local environment is available.

## Package checks

```powershell
corepack pnpm --filter @scotland-yard-live/web lint
corepack pnpm --filter @scotland-yard-live/web typecheck
corepack pnpm --filter @scotland-yard-live/web test
corepack pnpm --filter @scotland-yard-live/web build
corepack pnpm format:check
```

The repository-wide equivalents are documented in [Phase 1 bootstrap](../../docs/PHASE-1-BOOTSTRAP.md).

## Follow-up work

- Replace the synthetic fixture only after verified canonical board data and validation exist.
- Connect server-filtered room/game projections without placing hidden information in client state.
- Move movement legality and authoritative ticket accounting into the future game engine.
- Add real room lifecycle, realtime synchronization, reconnect handling, and game-state presentation.
