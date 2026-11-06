# Phase 3D closeout and Phase 3E readiness

This document closes the documentation for the merged best-effort station reconstruction and states the starting boundary for Phase 3E, transport graph reconstruction. It does not authorize Phase 3E implementation.

This pass inspected the working tree. It did not inspect Git history. The repository owner identifies the merged implementation as `6d67c68` (`feat(board): complete best-effort station reconstruction (#17)` on `main`). Statements below were checked against the files present in the tree.

Related status documents:

- [BOARD-RECONSTRUCTION.md](BOARD-RECONSTRUCTION.md)
- [BOARD-COORDINATE-RECONSTRUCTION.md](BOARD-COORDINATE-RECONSTRUCTION.md)
- [FINAL-PHASE-3D-STATION-RECONSTRUCTION.md](FINAL-PHASE-3D-STATION-RECONSTRUCTION.md)
- [BOARD-GRAPH-VERIFICATION.md](BOARD-GRAPH-VERIFICATION.md)
- [BOARD-CANONICAL-GRAPH-DECISION.md](BOARD-CANONICAL-GRAPH-DECISION.md)

## 1. Phase 3D objective and delivered scope

Phase 3D delivered a best-effort station coordinate dataset for the project target range 1–199. It did not deliver a canonical board, a verified station-number identity for every marker, or a transport graph.

Delivered:

- 199 station records with normalized coordinates.
- Explicit `incomplete-verification` state and `bestEffort: true`.
- Marker 200 left out of the playable station array in that file.
- Empty `connections`.
- Package tests that assert those dataset boundaries. See section 5. This documentation pass did not re-run them.

Not delivered:

- `metadata.state: 'canonical-complete'`.
- A change to `CANONICAL_DATASET_AVAILABILITY`.
- Export of the station file from the package entry point.
- Frontend integration. `apps/web` does not depend on `@scotland-yard-live/board-data` and still renders `apps/web/src/features/board/data/demo-board-fixture.ts`.
- Game engine, rooms, sessions, Socket.IO, or multiplayer behavior. No `packages/engine` package is present. `apps/server` has no Socket.IO dependency. `packages/database/src/schema/index.ts` still exports an empty schema.

## 2. Output files

| File                                                                                       | Purpose                                                                                                             |
| ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| `packages/board-data/data/stations.json`                                                   | Best-effort station records. Not canonical, not playable topology.                                                  |
| `packages/board-data/src/stations.test.ts`                                                 | Assertions on station count, ID range, coordinates, empty connections, excluded marker 200, and unique feature IDs. |
| `docs/game/FINAL-PHASE-3D-STATION-RECONSTRUCTION.md`                                       | Published summary counts for the reconstruction.                                                                    |
| `tools/board-calibration/output/station_recovery/final_station_reconstruction_counts.json` | Machine-readable copy of those summary counts.                                                                      |
| `tools/board-calibration/output/station_recovery/final_station_reconstruction_report.md`   | Same summary in report form.                                                                                        |

`packages/board-data/src/index.ts` exports `canonical-status.ts`, `types.ts`, and `validate.ts` only. Consumers must not import `stations.json` as the canonical dataset.

Earlier calibration and recovery artifacts under `tools/board-calibration/output/` remain reconstruction evidence. They are not a second canonical dataset.

## 3. Dataset counts and verification limits

Counted from `stations.json` during this documentation pass:

| Fact                                     | Value                        |
| ---------------------------------------- | ---------------------------- |
| Records                                  | 199                          |
| IDs                                      | 1 through 199, each once     |
| Records with in-range finite coordinates | 199                          |
| `metadata.state`                         | `incomplete-verification`    |
| `metadata.datasetVersion`                | `3D-final-best-effort-1.0.0` |
| `metadata.coordinateSystem`              | `normalized-0-to-1`          |
| `bestEffort`                             | `true`                       |
| `transportGraphStatus`                   | `unchanged-non-canonical`    |
| `marker200Excluded`                      | `true`                       |
| `connections`                            | `[]`                         |
| Marker 200 present                       | no                           |

`coordinateStatus`:

| Status                         |                Records |
| ------------------------------ | ---------------------: |
| `verified-from-physical-board` | 2 (stations 1 and 199) |
| `candidate-unverified`         |                    197 |

`identityStatus` is an extra field on the JSON records. It is not a `VerificationStatus` in `packages/board-data/src/types.ts`.

| `identityStatus`             |                                                Records |
| ---------------------------- | -----------------------------------------------------: |
| `verified`                   |            2 (stations 1 and 199; feature IDs present) |
| `candidate_uncertain`        | 4 (stations 3, 120, 123, and 158; feature IDs present) |
| `approximate`                |                               36 (feature IDs present) |
| `unmatched-feature-identity` |                                    157 (no feature ID) |

The published summary groups the 4 `candidate_uncertain` records and the 36 `approximate` records as **40 approximate feature associations**, with **2 verified retained associations** and **157 unmatched feature identities**. Use the four-way split when reading individual records. Use the grouped 40 only as the published summary count.

Dataset provenance says six prior identity records were retained: stations 1, 3, 120, 123, 158, and 199. Only 1 and 199 are `verified`. The other four retained identities remain `candidate_uncertain` with `candidate-unverified` coordinates. The 42 feature IDs on the file are unique. The report states that no feature identifiers were fabricated.

`CANONICAL_DATASET_AVAILABILITY` is still:

- `available: false`
- `state: 'incomplete-verification'`
- reason text still says topology and coordinates remain incomplete pending a straight-on high-resolution source and edge-by-edge verification

`validateBoardDataset` checks full coordinate and edge verification only when `metadata.state` is `canonical-complete`. The station test expects `{ valid: true, issues: [] }` for this incomplete file. That expectation is not a canonical-complete result.

## 4. Explicit exclusions

- Marker 200 is not a record in `stations.json`. Physical evidence that a marker 200 is printed remains in the historical audits, including [BOARD-CANONICAL-INVENTORY-DECISION.md](BOARD-CANONICAL-INVENTORY-DECISION.md) and candidate edge `E-086`. Exclusion from the best-effort array does not close the 199-versus-200 decision.
- Transport topology is excluded. `connections` is empty. `VERIFIED_BOAT_CONNECTIONS` in `canonical-status.ts` is unchanged and is not copied into the station file.
- The 125 candidate transport observations were not revised by Phase 3D.
- The synthetic frontend board was not switched to this dataset.
- Game rules, station coordinates, and station identities are reconstruction data, not permission to edit them during Phase 3E without an approved evidence change.

## 5. Tests and checks recorded for the implementation

`packages/board-data/src/stations.test.ts` records three expectations:

1. 199 stations, IDs 1 through 199 in order, every station has a coordinate, and `validateBoardDataset` returns `{ valid: true, issues: [] }`.
2. No station ID 200, and `connections` equals `[]`.
3. Feature IDs that are present are unique.

This documentation pass did not execute Vitest, the package typecheck, or the candidate-edge validator. It did not treat those recorded expectations as freshly observed pass results.

The published reconstruction report and `final_station_reconstruction_counts.json` record the grouped counts in section 3. They do not record a test-runner log.

## 6. Known limitations and risks

- Most station numbers are not independently tied to a feature identity. 157 records are unmatched. Assignment error is an expected limitation named by the reconstruction report.
- 197 coordinates are `candidate-unverified`. Fold and perspective displacement remain named limitations. The original control-point calibration workflow was not what produced this file.
- Two records use `coordinateStatus: 'verified-from-physical-board'` inside an `incomplete-verification` best-effort dataset. Reading those two fields as a canonical board would overstate the file.
- Per-station `provenance` objects use `source`, `method`, and sometimes `basis` or `markerCandidate`. That shape is not `SourceReference` (`id`, `description`, `status`) from `types.ts`. The validator ignores the extra JSON fields.
- Edition manufacturer text differs between files: `canonical-status.ts` uses `Milton Bradley; manufactured under licence by Funskool (India) Ltd.` and `stations.json` uses `Milton Bradley; Funskool`. This pass did not choose one string.
- [BOARD-CANONICAL-INVENTORY-DECISION.md](BOARD-CANONICAL-INVENTORY-DECISION.md) still says, as its own decision consequences, that the canonical package remained unchanged and that coordinates must not be generated from the photographs then under review. That document is a historical deferral. The best-effort file now exists and does not close that deferral. Do not delete the file to make the older consequence sentence true, and do not treat the file as the missing owner decision.
- Calling the 199 records "playable stations" in the reconstruction summary means the project target range stored in the file. It does not mean the canonical playable inventory decision is closed.
- Starting positions remain unresolved. [BOARD-STARTING-POSITIONS-AUDIT.md](BOARD-STARTING-POSITIONS-AUDIT.md) records 18 rulebook start cards and 13 observed card-face values, not a canonical set.

## 7. Phase 3E starting evidence inventory

Use these sources as they are. Do not recreate them.

| Evidence                                                                                                                                                                | What it is                                                                                                                                                          | What it is not                                                                                                                                                                                                   |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [data/board-edge-candidates-1-200.json](data/board-edge-candidates-1-200.json)                                                                                          | 125 candidate observations. Metadata: dataset version `3b5.0.0`, `canonicalStatus: non-canonical`, `playable: false`, observed station range 1–200.                 | A canonical or playable graph.                                                                                                                                                                                   |
| [data/board-edge-candidates.schema.json](data/board-edge-candidates.schema.json) and [data/validate-board-edge-candidates.mjs](data/validate-board-edge-candidates.mjs) | Schema and validator for that candidate artifact. Candidate `verificationStatus` is `provisional` or `unresolved` only.                                             | The board-data `VerificationStatus` union. Do not map `provisional` to `verified-from-physical-board` or to `cross-checked`.                                                                                     |
| [BOARD-GRAPH-VERIFICATION.md](BOARD-GRAPH-VERIFICATION.md)                                                                                                              | Phase 3C.2 audit: 66 taxi, 33 bus, 22 underground, 4 boat; 0 verified, 121 provisional, 4 unresolved. Nine endpoint pairs have more than one transport observation. | A promotion record.                                                                                                                                                                                              |
| [BOARD-CANONICAL-GRAPH-DECISION.md](BOARD-CANONICAL-GRAPH-DECISION.md)                                                                                                  | Decision: do not introduce a canonical transport graph.                                                                                                             | Superseded by the station file. The station file did not revisit this decision.                                                                                                                                  |
| [BOARD-EDGE-TRANSCRIPTION.md](BOARD-EDGE-TRANSCRIPTION.md) and [BOARD-EDGE-HUMAN-REVIEW.md](BOARD-EDGE-HUMAN-REVIEW.md)                                                 | Row-level observations and the review queue.                                                                                                                        | Verified edges.                                                                                                                                                                                                  |
| [BOARD-DISCREPANCY-LEDGER.md](BOARD-DISCREPANCY-LEDGER.md)                                                                                                              | Unresolved station-range, boat, starting-card, coordinate, and graph discrepancies, including the earlier 134-versus-125 count correction.                          | A dataset to normalize away.                                                                                                                                                                                     |
| `VERIFIED_BOAT_CONNECTIONS` in `packages/board-data/src/canonical-status.ts`                                                                                            | Three rulebook statements: 115–118, 115–157, and 157–194. The audit describes the same route as 194–157, 157–115, and 115–118.                                      | A complete boat graph, and not proof of the photographed board's topology. Candidate boat rows `E-122` through `E-125` remain unresolved, including `108–115`, which the cited rulebook page does not establish. |
| `stations.json`                                                                                                                                                         | Coordinate and identity context for stations 1–199.                                                                                                                 | Evidence that two nearby stations are connected, or that a service icon implies an edge.                                                                                                                         |
| [BOARD-EVIDENCE-REGISTER.md](BOARD-EVIDENCE-REGISTER.md) and the photo inventories under `docs/game/evidence/board-photos/`                                             | Image inventory and coverage.                                                                                                                                       | A new transcription.                                                                                                                                                                                             |

The nine multi-transport endpoint pairs recorded by the graph audit are `11–22`, `13–14`, `14–15`, `102–115`, `105–107`, `127–133`, `133–140`, `156–157`, and `105–108`. Preserve each observation.

## 8. Phase 3E scope and proposed stages

Phase 3E is transport graph reconstruction only. An incomplete graph retained because the evidence is insufficient is an acceptable outcome. That outcome is already the Phase 3C.2 decision; Phase 3E may confirm it again.

Station coordinate reconstruction stays separate. Do not "improve" coordinates while verifying edges.

### 3E.1 Evidence reconciliation

Compare the existing 125 candidate rows with the rulebook boat statements, the discrepancy ledger, and the human-review queue. Record which rows already have endpoint-level photo citations and which conflicts are unresolved. Do not create a replacement candidate file.

### 3E.2 Edge verification

Verify existing candidate rows against readable endpoint crops and the intervening transport marking. Add a new observation only when a source crop supports it, and keep it at its actual status. A candidate confidence value (`high`, `medium`, or `low`) is not verification.

### 3E.3 Graph integrity and validation

After any approved evidence edit, run the existing candidate validator and check the graph invariants already used by the project: ordered undirected endpoints, known statuses, preserved unresolved rows, and explicit handling of multi-transport pairs. Do not delete a contradictory row to make the graph simpler.

### 3E.4 Canonical promotion decision

Promotion is a separate decision. It requires the gates in section 9. If they fail, write the decision as insufficient evidence and leave `CANONICAL_DATASET_AVAILABILITY.available` false.

## 9. Gates before canonical gameplay

Candidate data must not enter canonical gameplay unless all of the following are true:

1. `CANONICAL_DATASET_AVAILABILITY.available` is still `false` until an explicit promotion change. This milestone does not authorize that change.
2. The dataset `metadata.state` is `canonical-complete` and `validateBoardDataset` passes the canonical-complete checks, including verified coordinate status and verified edge status.
3. Every promoted edge has traceable endpoint evidence and a `verificationStatus` in the board-data union. `provisional`, candidate confidence, and `candidate-unverified` do not qualify.
4. The 199-versus-200 inventory decision has an explicit owner resolution before any playable graph includes or drops marker 200.
5. Rulebook boat statements are not expanded into unpublished physical edges. `108–115` is not added from a community dataset.
6. The active frontend source remains `demo-board-fixture.ts` until a separate integration change. `apps/web` must not gain a board-data dependency inside an evidence-only edit.
7. Historical unresolved rows and contradictory observations stay in the evidence record even if they are omitted from a future canonical graph.
8. No game-engine or multiplayer behavior is added in order to "use" a partial graph.

## 10. Guardrails

- Do not recreate the 125 candidate edges from scratch.
- Do not treat candidate confidence as verification.
- Do not infer edges from station proximity.
- Do not infer transport types from station service icons.
- Do not use community datasets as canonical truth. [BOARD-RECONSTRUCTION.md](BOARD-RECONSTRUCTION.md) records them as research only.
- Do not automatically promote the three rulebook boat statements into a complete physical graph.
- Preserve unresolved records and contradictory observations.
- Keep station coordinate reconstruction separate from transport graph reconstruction.
- Do not change `CANONICAL_DATASET_AVAILABILITY` to `true`.
- Do not change the active frontend board source.
- Do not implement the game engine or multiplayer behavior in Phase 3E.

## 11. Handoff for the next coding agent

Inspect these files first, in this order:

1. This document.
2. [BOARD-GRAPH-VERIFICATION.md](BOARD-GRAPH-VERIFICATION.md) and [BOARD-CANONICAL-GRAPH-DECISION.md](BOARD-CANONICAL-GRAPH-DECISION.md).
3. [data/board-edge-candidates-1-200.json](data/board-edge-candidates-1-200.json), its schema, and `docs/game/data/validate-board-edge-candidates.mjs`.
4. [BOARD-DISCREPANCY-LEDGER.md](BOARD-DISCREPANCY-LEDGER.md) and [BOARD-EDGE-HUMAN-REVIEW.md](BOARD-EDGE-HUMAN-REVIEW.md).
5. `packages/board-data/src/canonical-status.ts` and `packages/board-data/src/types.ts`.
6. `packages/board-data/data/stations.json` metadata and `packages/board-data/src/stations.test.ts`, as coordinate context only.
7. [BOARD-CANONICAL-INVENTORY-DECISION.md](BOARD-CANONICAL-INVENTORY-DECISION.md), as a historical deferral that the station file did not close.
8. `apps/web/src/features/board/data/demo-board-fixture.ts`, to confirm the active renderer source before any board-data edit.

Do not alter the following without explicit owner approval:

- `packages/board-data/data/stations.json` coordinates, identities, feature IDs, or provenance.
- `docs/game/data/board-edge-candidates-1-200.json`, except through an evidence-reviewed edit that preserves unresolved and conflicting rows.
- `CANONICAL_DATASET_AVAILABILITY` in `packages/board-data/src/canonical-status.ts`.
- The active frontend board source and `apps/web` dependencies.
- Historical audit findings in the existing `docs/game/BOARD-*.md` documents. Add a new status note if a later phase changes current facts; do not rewrite the original finding.
- Game rules, database schema, and package dependencies.

The repository owner performs all Git operations. Do not commit, push, merge, rebase, or switch branches as part of Phase 3E preparation.
