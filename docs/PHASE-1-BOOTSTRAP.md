# Phase 1 bootstrap

## Implemented foundation

- pnpm workspace and Turborepo task graph
- strict shared TypeScript compiler settings
- React + Vite web shell
- Fastify API with liveness and database-readiness endpoints
- shared Zod response contract
- PostgreSQL 17 via Docker Compose with a named persistent volume
- Drizzle database package and migration baseline
- validated server environment configuration
- ESLint, Prettier, Vitest and GitHub Actions CI

## Local setup

Use Node.js 26 and the repository-pinned pnpm version.

```powershell
Copy-Item .env.example .env
pnpm install
docker compose up -d postgres
pnpm --filter @scotland-yard-live/database db:migrate
pnpm dev
```

The web app is served on `127.0.0.1:5173`; the API listens on `127.0.0.1:4000`.

## Database commands

```powershell
docker compose ps
pnpm --filter @scotland-yard-live/database db:generate
pnpm --filter @scotland-yard-live/database db:migrate
pnpm --filter @scotland-yard-live/database db:studio
```

The current migration is intentionally a no-op infrastructure baseline. Domain tables will be introduced with the room and game domain models rather than inventing them prematurely.

## Health endpoints

- `GET /health/live` reports whether the API process is alive.
- `GET /health/ready` checks whether PostgreSQL is reachable and returns HTTP 503 otherwise.

## Verification

```powershell
pnpm lint
pnpm typecheck
pnpm test
pnpm build
pnpm format:check
```

CI starts PostgreSQL, applies migrations, and runs the same verification pipeline.

## Architectural boundaries

The database package owns the PostgreSQL pool, Drizzle client, schema entry point and migrations. It does not depend on Fastify, React, Socket.IO or the game engine. The server owns lifecycle and health integration. Game rules and game-state persistence remain future work.
