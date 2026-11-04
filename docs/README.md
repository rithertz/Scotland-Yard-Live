# Scotland Yard Live documentation

This directory is the repository’s durable documentation index. It describes the current implementation and separates implemented behavior from planned canonical game work.

## Current foundation

- [Phase 1 bootstrap](PHASE-1-BOOTSTRAP.md) — repository, tooling, local infrastructure, and current foundation status.
- [System overview](architecture/SYSTEM_OVERVIEW.md) — current dependency direction and deferred backend/game-engine work.
- [Architecture decisions](architecture/DECISIONS.md) — recorded infrastructure and architecture choices.
- [Visual identity and experience](frontend/VISUAL-IDENTITY-AND-EXPERIENCE.md) — implemented visual language for the frontend foundation.

## Application documentation

- [Web application README](../apps/web/README.md) — frontend responsibility, structure, commands, interactions, and limitations.

## Planned game documentation

The following areas are required by the consolidated project plan but are not complete in this repository yet:

- Canonical rules specification and verification ledger — planned under `docs/game/`.
- Verified original board reconstruction, graph format, coordinates, and validation — planned under `docs/game/` and the future `packages/board-data/` package.
- Pure game engine and authoritative movement validation — planned under the future `packages/engine/` package.
- Realtime room, player-specific projections, and multiplayer protocol — future server/contracts work.

The current web board is an explicitly synthetic visual fixture. It must not be treated as canonical board data, a verified topology, or multiplayer state.

## Documentation conventions

Documentation should describe observed implementation rather than planned behavior. When a feature is deferred, label it as planned, blocked, or future work. Do not use the excluded Richup UI/UX material as a design reference.
