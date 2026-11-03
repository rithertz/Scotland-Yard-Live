# API server

Fastify server foundation. The current implementation exposes an HTTP liveness endpoint and structured request logging.

## Commands

- `pnpm --filter @scotland-yard-live/server dev`
- `pnpm --filter @scotland-yard-live/server build`
- `pnpm --filter @scotland-yard-live/server typecheck`
- `pnpm --filter @scotland-yard-live/server test`

## Boundaries

The server is the future authority for room membership, commands, game state, hidden-information projections and persistence. Validate all external input. Do not expose internal game state directly to clients.
