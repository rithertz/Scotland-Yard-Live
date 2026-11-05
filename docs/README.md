# Scotland Yard Live documentation

This directory is the repository’s durable documentation index. It describes the current implementation and separates implemented behavior from planned canonical game work.

## Current foundation

- [Phase 1 bootstrap](PHASE-1-BOOTSTRAP.md) — repository, tooling, local infrastructure, and current foundation status.
- [System overview](architecture/SYSTEM_OVERVIEW.md) — current dependency direction and deferred backend/game-engine work.
- [Architecture decisions](architecture/DECISIONS.md) — recorded infrastructure and architecture choices.
- [Visual identity and experience](frontend/VISUAL-IDENTITY-AND-EXPERIENCE.md) — implemented visual language for the frontend foundation.
- [Board reconstruction](game/BOARD-RECONSTRUCTION.md) — canonical-board data contract, evidence ledger, source comparison, and currently blocked verification work.
- [Physical board evidence register](game/BOARD-EVIDENCE-REGISTER.md) — image inventory, quality classifications, region coverage, and missing evidence.
- [Coordinate reconstruction](game/BOARD-COORDINATE-RECONSTRUCTION.md) — reproducible board-plane calibration and normalized-coordinate method.
- [Transcription workflow](game/BOARD-TRANSCRIPTION-WORKFLOW.md) — evidence-linked station/edge transcription and review gates.
- [Station inventory](game/BOARD-STATION-INVENTORY.md) — physical marker observations from the Phase 3B.2 photographs; not canonical station data.
- [Edition identity audit](game/BOARD-EDITION-IDENTITY.md) — rulebook identity evidence and the unresolved board-to-rulebook match.
- [Canonical inventory decision](game/BOARD-CANONICAL-INVENTORY-DECISION.md) — deferred 199-versus-200 playable-station decision and evidence gates.
- [Starting-position audit](game/BOARD-STARTING-POSITIONS-AUDIT.md) — partial card-face observations and missing evidence for all 18 start positions.
- [Edge transcription](game/BOARD-EDGE-TRANSCRIPTION.md) — transport-line evidence boundary and future endpoint-record format.
- [Edge candidate dataset](game/data/board-edge-candidates-1-200.json) — machine-readable, non-canonical candidate edges and evidence references.
- [Edge human-review queue](game/BOARD-EDGE-HUMAN-REVIEW.md) — prioritized review batches for ambiguous and conflicting observations.
- [Graph verification](game/BOARD-GRAPH-VERIFICATION.md) — Phase 3C.2 audit of the non-canonical 125-row candidate set.
- [Canonical graph decision](game/BOARD-CANONICAL-GRAPH-DECISION.md) — evidence gate decision; no canonical graph has been introduced.
- [Discrepancy ledger](game/BOARD-DISCREPANCY-LEDGER.md) — unresolved station-range, boat-route, starting-card, and calibration decisions.

## Application documentation

- [Web application README](../apps/web/README.md) — frontend responsibility, structure, commands, interactions, and limitations.

## Planned game documentation

The following areas are required by the consolidated project plan but are not complete in this repository yet:

- Canonical rules specification and verification ledger — planned under `docs/game/`.
- Verified original board reconstruction, graph format, coordinates, and validation — data-package infrastructure and provenance are present in `packages/board-data/`; complete target-edition topology and coordinates remain blocked pending evidence.
- Pure game engine and authoritative movement validation — planned under the future `packages/engine/` package.
- Realtime room, player-specific projections, and multiplayer protocol — future server/contracts work.

The current web board is an explicitly synthetic visual fixture. It must not be treated as canonical board data, a verified topology, or multiplayer state.

## Documentation conventions

Documentation should describe observed implementation rather than planned behavior. When a feature is deferred, label it as planned, blocked, or future work. Do not use the excluded Richup UI/UX material as a design reference.
