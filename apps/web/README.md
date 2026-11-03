# Web application

React + Vite player-facing application. The current implementation is a visual bootstrap shell with a small API liveness check.

## Commands

- `pnpm --filter @scotland-yard-live/web dev`
- `pnpm --filter @scotland-yard-live/web build`
- `pnpm --filter @scotland-yard-live/web typecheck`
- `pnpm --filter @scotland-yard-live/web test`

## Boundaries

The web application owns presentation and client-only interaction state. It must not own authoritative game state or receive hidden information that the current player's role is not permitted to see. Shared wire schemas belong in `packages/contracts`.
