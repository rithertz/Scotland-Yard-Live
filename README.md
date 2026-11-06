# Scotland Yard Live

A real-time multiplayer implementation of the original **Scotland Yard** board game, being built first for private playtesting with friends.

> **Current status:** The infrastructure foundation is implemented, and a best-effort station coordinate reconstruction exists. The canonical transport graph, game engine, and multiplayer gameplay are not available. The web board still uses a synthetic fixture.

## Implementation status

| Area                                                                                       | Status                                                                                                                                        |
| ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Monorepo, React/Vite web shell, Fastify API, shared contracts, PostgreSQL/Drizzle baseline | Implemented                                                                                                                                   |
| Best-effort station coordinates in `packages/board-data/data/stations.json`                | Present. 199 records, `incomplete-verification`, `bestEffort: true`. Not verified gameplay topology                                           |
| Canonical transport graph                                                                  | Not available. `CANONICAL_DATASET_AVAILABILITY.available` remains `false`                                                                     |
| Web board                                                                                  | Synthetic fixture at `apps/web/src/features/board/data/demo-board-fixture.ts`. `apps/web` does not depend on `@scotland-yard-live/board-data` |
| Private rooms, player sessions, Socket.IO, game engine, and gameplay                       | Not implemented                                                                                                                               |

Details and Phase 3E limits are in [docs/game/PHASE-3D-CLOSEOUT-AND-PHASE-3E-READINESS.md](docs/game/PHASE-3D-CLOSEOUT-AND-PHASE-3E-READINESS.md).

## Approved project direction

- **Runtime:** Node.js 26 LTS
- **Language:** TypeScript
- **Package management:** pnpm workspaces with Turborepo
- **Frontend:** React + Vite
- **Backend:** Fastify
- **Realtime transport:** Socket.IO (planned; not implemented yet)
- **Database:** PostgreSQL 17 with Drizzle ORM
- **Validation:** Zod
- **Testing:** Vitest; Playwright is planned
- **CI:** GitHub Actions

The application is designed as a **server-authoritative modular monolith**. The future game engine will be framework-independent and deterministic. In particular, detective clients must never receive concealed Mr X location data.

## Current scope and constraints

- Private rooms for 3–6 players.
- Original Scotland Yard board and verified original rules.
- No public matchmaking or spectators in the initial release.
- Custom maps and Board Studio are out of scope.
- The initial deployment is intended for private playtesting, with low or near-zero operating cost.
- Do not describe a feature as implemented until code and tests demonstrate it.

## Prerequisites

Install the following:

- Node.js `26.13.0` (Node 26)
- Corepack, included with supported Node.js installations
- Docker Desktop with Docker Compose
- Git

The repository pins pnpm `11.9.0` through Corepack.

Check your versions:

```powershell
node --version
corepack --version
docker --version
docker compose version
```

## Local setup

Run these commands from the repository root in PowerShell.

### 1. Configure environment variables

```powershell
Copy-Item .env.example .env
```

The local `.env` file is ignored by Git. Keep real credentials and personal secrets out of the repository.

The development PostgreSQL container maps host port `5433` to container port `5432`. The host-side `DATABASE_URL` should therefore use `localhost:5433`.

### 2. Install dependencies

```powershell
corepack pnpm install
```

### 3. Start PostgreSQL

```powershell
docker compose up -d postgres
docker compose ps
```

Wait until the PostgreSQL service reports `healthy`.

### 4. Apply database migrations

```powershell
corepack pnpm --filter @scotland-yard-live/database db:migrate
```

The current migration is an intentionally minimal infrastructure baseline. Domain tables will be introduced alongside the room and game models rather than being invented prematurely.

### 5. Start the applications

```powershell
corepack pnpm dev
```

Turborepo starts the web and API development processes. If you prefer separate terminals, run:

```powershell
corepack pnpm --filter @scotland-yard-live/server dev
```

and, in another terminal:

```powershell
corepack pnpm --filter @scotland-yard-live/web dev
```

Development URLs:

| Service              | URL                                |
| -------------------- | ---------------------------------- |
| Web application      | http://127.0.0.1:5173              |
| API liveness         | http://127.0.0.1:4000/health/live  |
| API readiness        | http://127.0.0.1:4000/health/ready |
| PostgreSQL from host | `localhost:5433`                   |

The web application is currently a development shell, not a playable game.

## Database commands

```powershell
# Start the database
docker compose up -d postgres

# Check container health
docker compose ps

# Generate a migration after changing the Drizzle schema
corepack pnpm --filter @scotland-yard-live/database db:generate

# Apply pending migrations
corepack pnpm --filter @scotland-yard-live/database db:migrate

# Open Drizzle Studio
corepack pnpm --filter @scotland-yard-live/database db:studio
```

To stop the database container without deleting its data:

```powershell
docker compose stop postgres
```

The named Docker volume preserves local database data across container restarts. Do not remove the volume unless you intentionally want to delete that data.

## Quality checks

Run the repository checks from the root:

```powershell
corepack pnpm format:check
corepack pnpm lint
corepack pnpm typecheck
corepack pnpm test
corepack pnpm build
```

Format files when needed:

```powershell
corepack pnpm format
```

## Repository layout

```text
apps/
  server/       Fastify API and application lifecycle
  web/          React + Vite player-facing web shell and synthetic board
packages/
  board-data/   Board types, validator, canonical-availability gate, best-effort station file
  contracts/    Shared Zod schemas and inferred DTO types
  database/     PostgreSQL pool, Drizzle client, schema and migrations
docs/
  architecture/ Architecture overview and decision register
  frontend/     Visual identity and frontend foundation notes
  game/         Board evidence, audits, reconstruction status, and candidate graph
  PHASE-1-BOOTSTRAP.md
.github/
  workflows/    GitHub Actions CI
docker-compose.yml
```

## Architecture boundaries

- `apps/web` consumes shared contracts and communicates with the API.
- `apps/server` owns HTTP lifecycle, readiness checks, and future realtime integration.
- `packages/contracts` owns shared runtime schemas and DTO types.
- `packages/board-data` owns board types, dataset validation, and the canonical-availability gate. Its best-effort station file is not a canonical graph.
- `packages/database` owns PostgreSQL connectivity, Drizzle schema and migrations.
- The future game engine will be a separate pure domain package. It must not depend on React, Fastify, Socket.IO, or PostgreSQL.

The server is authoritative for all game commands and state transitions. Role-specific views must be constructed server-side so hidden Mr X information cannot leak to detectives.

## CI

GitHub Actions runs the repository verification pipeline on pushes to `main` and pull requests. It provisions PostgreSQL, applies migrations, then runs dependency installation, linting, typechecking, tests, build, and formatting checks.

## Git workflow

The repository uses feature branches for implementation work. The project owner performs all Git commits, pushes, and merges. Automated assistants and coding agents must not create commits or push changes.

## Documentation

- [System overview](docs/architecture/SYSTEM_OVERVIEW.md)
- [Architecture decisions](docs/architecture/DECISIONS.md)
- [Phase 1 bootstrap guide](docs/PHASE-1-BOOTSTRAP.md)
- [Documentation index](docs/README.md)
- [Board reconstruction](docs/game/BOARD-RECONSTRUCTION.md)
- [Phase 3D closeout and Phase 3E readiness](docs/game/PHASE-3D-CLOSEOUT-AND-PHASE-3E-READINESS.md)

The approved consolidated project plan is the product and implementation source of truth.
