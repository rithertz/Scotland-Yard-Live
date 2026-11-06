# `@scotland-yard-live/board-data`

Pure TypeScript model and validation boundary for the target 1985 Milton Bradley / Funskool Central London board. It has no React, SVG, browser, game-engine, or server dependency.

## Current status

The canonical dataset is deliberately **unavailable**. `CANONICAL_DATASET_AVAILABILITY.available` remains `false`.

`data/stations.json` is a best-effort station file: 199 records, normalized coordinates, `metadata.state` of `incomplete-verification`, `bestEffort: true`, and an empty `connections` array. Marker 200 is not in that array. `src/index.ts` does not export the file. `validateBoardDataset` can accept this incomplete-verification file without applying the `canonical-complete` coordinate and edge checks. That result is not canonical promotion.

The package provides the schema, validator, runtime undirected-edge adjacency helper, target-edition metadata, and `VERIFIED_BOAT_CONNECTIONS`. Those three boat facts are rulebook statements. They are not a playable graph and are not renderer input. The 125-row transport candidate artifact lives under `docs/game/data/` and is not part of this package.

`CANONICAL_DATASET_AVAILABILITY.available` must remain `false` until all 199 station coordinates and the full topology have traceable evidence and pass `validateBoardDataset` with `metadata.state: 'canonical-complete'`.

Read [the board reconstruction specification](../../docs/game/BOARD-RECONSTRUCTION.md) and [the Phase 3D closeout](../../docs/game/PHASE-3D-CLOSEOUT-AND-PHASE-3E-READINESS.md) before adding data. Those documents record required evidence, source licensing, and open discrepancies. The web application does not depend on this package; its active board remains the synthetic fixture.

## Commands

```powershell
corepack pnpm --filter @scotland-yard-live/board-data test
corepack pnpm --filter @scotland-yard-live/board-data typecheck
```
