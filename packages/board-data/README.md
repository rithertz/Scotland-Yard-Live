# `@scotland-yard-live/board-data`

Pure TypeScript model and validation boundary for the target 1985 Milton Bradley / Funskool Central London board. It has no React, SVG, browser, game-engine, or server dependency.

## Current status

The canonical dataset is deliberately **unavailable**. The package provides the schema, validator, runtime undirected-edge adjacency helper, target-edition metadata, and a small set of directly verified boat-route facts. It does not include candidate stations, coordinates, or transport edges as if they were canonical.

`CANONICAL_DATASET_AVAILABILITY.available` must remain `false` until all 199 station coordinates and the full topology have traceable evidence and pass `validateBoardDataset` with `metadata.state: 'canonical-complete'`.

Read [the board reconstruction specification](../../docs/game/BOARD-RECONSTRUCTION.md) before adding data. That document records required evidence, source licensing, and open discrepancies.

## Commands

```powershell
corepack pnpm --filter @scotland-yard-live/board-data test
corepack pnpm --filter @scotland-yard-live/board-data typecheck
```
