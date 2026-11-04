# Canonical board reconstruction

## Status

**Infrastructure and evidence ledger complete; canonical dataset and renderer integration blocked.** The existing web board remains an intentionally synthetic visual fixture. No file in this repository currently claims a 1:1 board reconstruction.

This document governs the safe reconstruction of the target board. It follows the consolidated project plan and supersedes older context-pack proposals that describe custom-map or editor work.

## 1. Target edition

| Field                  | Value                                                                    | Evidence/status                                                                  |
| ---------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------- |
| Target                 | _Scotland Yard_, original Central London board                           | Project decision                                                                 |
| Edition                | 1985 Milton Bradley; manufactured under licence by Funskool (India) Ltd. | Project decision and supplied physical references                                |
| Product code           | 4500-X2                                                                  | Project decision / supplied copyright-panel reference                            |
| Expected station range | 1–199                                                                    | Project decision; not yet independently transcribed from a traceable board image |
| Player maximum         | Six                                                                      | Supplied rules, page 1                                                           |

The physical close-up supplied for this work appears to include a station labelled `200`. This conflicts with the target-edition decision (1–199) and must be resolved from a straight-on image of the copyright panel and complete board before publishing a complete dataset.

## 2. Board-data architecture

`packages/board-data` is the only eventual canonical graph boundary. It is TypeScript-only and intentionally has no dependency on React, Vite, SVG, server state, or the game engine.

```text
physical board + original rules ──> evidence ledger / provenance
                                      │
                                      ▼
                           @scotland-yard-live/board-data
                           stations + undirected connections
                                      │
                            validated directional adjacency
                                      │
                                      ▼
                       future SVG presentation adapter in apps/web
```

The package exposes types, `validateBoardDataset`, `createAdjacency`, `hasSymmetricAdjacency`, edition metadata, and explicit availability state. It exports no candidate graph as canonical. The application must not switch from its synthetic fixture until availability is `true` and the data validates as `canonical-complete`.

## 3. Canonical schemas

- `BoardStation`: integer ID, optional normalized coordinate, coordinate verification status, and optional provenance.
- `TransportConnection`: one undirected edge, stored once with `from < to`; transport is `taxi`, `bus`, `underground`, or `boat`.
- `BoardDataset`: edition metadata, dataset version, normalized coordinate system, completeness state, stations, connections, and source references.

Coordinates use a normalized `0..1` x/y system. They are resolution-independent and only belong to the canonical data once calibrated against a suitable physical-board source. Presentation-only artwork—Thames path, parks, labels, line offsets, marker radii, and route styling—does not belong in this package.

## 4. Validation strategy

For `canonical-complete`, the validator requires exactly 199 unique IDs covering 1–199; finite, in-range coordinates; verified coordinate statuses; valid and ordered endpoints; known endpoints; no self-connections; valid transport values; no duplicate same-transport undirected edges; and verified edge status. Runtime adjacency is derived in both directions from each single stored edge and has an explicit symmetry check.

An incomplete-verification dataset can be used only as a workbench during transcription. It is never a substitute for complete canonical data, and no such dataset is shipped from this package.

## 5. Evidence and provenance

Verification states are deliberately attached to individual records: `verified-from-physical-board`, `verified-from-rulebook`, `cross-checked`, `candidate-unverified`, and `unresolved`. A candidate source cannot silently become canonical.

Direct rulebook evidence: page 10 of the supplied rules describes Mr X’s black-ticket Thames journey as `194–157`, `157–115`, and `115–118`, in either direction. These three facts are recorded in `VERIFIED_BOAT_CONNECTIONS`, but are not used as a partial playable graph.

The supplied photographs establish that a physical Central London board exists and show local route/marker detail, but their perspective, resolution, glare, and partial coverage do not permit auditable calibration of all 199 coordinates or transcription of every connection.

## 6. Candidate comparison and licensing

Candidate repositories were researched for comparison only; no code or dataset has been copied.

| Source                                                                            | Reviewed path / revision                                                     | Contents                                            | Licence / target-edition assessment                                        | Decision           |
| --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------- | ------------------ |
| [thamma/scotlandyard-tool](https://github.com/thamma/scotlandyard-tool)           | `master`, `maps/` (repository view; immutable SHA not exposed during review) | Haskell solver/map material                         | No root `LICENSE` file at the reviewed URL; target edition not established | Research only      |
| [waland1510/yard](https://github.com/waland1510/yard)                             | `main`, `apps/frontend/src/app/game/board-data/connections-data.ts`          | Frontend topology records                           | No root `LICENSE` at the reviewed URL; target edition not established      | Research only      |
| [tim-koehler/ScotlandYard](https://github.com/tim-koehler/ScotlandYard)           | `master`, `ScotlandYard.json`, `LICENSE`                                     | Runtime game-state JSON, not a complete board graph | Apache-2.0; target edition not established                                 | No topology reused |
| [AlexElvers/scotland-yard-data](https://github.com/AlexElvers/scotland-yard-data) | `master`, `stations.txt`, `connections.txt`                                  | 199 stations, coordinates, and transport edges      | No root `LICENSE` visible; candidate data conflicts with the rules         | Research only      |

Remote branch names are recorded because the review surface did not expose immutable resolved commit SHAs. A future audit must record a commit SHA or immutable archive URL before an external source can be used as verification evidence.

## 7. Discrepancy ledger

| Subject            | Candidate/observed values                                                                                                                                              | Evidence                                           | Decision                                                           | Status                                                               | Required action                                                                                           |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------------------------------------ | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Station range      | Project target 1–199; supplied close-up appears to show `200`; waland’s candidate graph includes `199–200`; Alex README notes another version with 200 and missing 108 | Target decision, supplied photo, candidate sources | Do not publish a station list                                      | Unresolved                                                           | Obtain a straight-on complete target-edition board/photo of copyright panel; transcribe IDs independently |
| Thames route       | Rules: 194–157–115–118; Alex: 194–157–115–108                                                                                                                          | Supplied rules p.10; candidate `connections.txt`   | Keep only the rules-backed three-edge fact; reject candidate route | Verified for rules wording; target-board visual still to cross-check | Photograph/scan boat line and target board station labels                                                 |
| General topology   | Community datasets differ and have no proven edition identity; waland inserts negative-numbered river waypoints                                                        | Candidate repositories                             | Do not import or vote by majority                                  | Unresolved                                                           | Edge-by-edge transcription and independent review against target board                                    |
| Coordinates        | Candidate coordinates exist; physical images are oblique/partial                                                                                                       | Candidate stations file; supplied photos           | Do not use candidate coordinates                                   | Unresolved                                                           | Supply a flat, straight-on, high-resolution full-board scan/photo with no glare                           |
| Starting positions | User-supplied start-card photo exists in project context; rules reviewed here do not establish the full set                                                            | Physical reference / rules                         | Keep separate from topology; do not encode allocation logic        | Unresolved                                                           | Independently transcribe all cards and cross-check target edition                                         |

## 8. Coordinate calibration workflow

1. Capture the complete board straight on, with all edges visible, at least 4000 px on the long side, evenly lit, and including the copyright panel.
2. Record source file dimensions, crop, lens/perspective correction, and board-corner control points in the evidence ledger.
3. Calibrate each station center to normalized `0..1` coordinates; retain a per-station provenance reference.
4. Have a second person compare every ID and center against the image.
5. Store only independently checked values as `verified-from-physical-board` or `cross-checked`.
6. Run the validator before allowing renderer integration.

## 9. Future SVG layer architecture

When complete data exists, keep six separate responsibilities:

1. Canonical station/edge data from `@scotland-yard-live/board-data`.
2. A presentation adapter that converts normalized points into the SVG view box.
3. Custom geography artwork (Thames, parks, roads, landmarks, labels).
4. Transport-edge rendering using the established midnight-ink, brass, crimson, parchment, and blue palette.
5. Station markers and transport indicators.
6. Viewport, selection, and later pawn layers.

No graph will be hard-coded in JSX. Existing pan, zoom, reset, keyboard selection, and responsive game-room behavior remain the compatibility baseline. The synthetic fixture remains available for isolated visual regression tests until the active source is explicitly changed.

## 10. Safe update procedure

1. Add a provenance entry and immutable source reference for every new fact.
2. Add records only at their actual verification status; never infer a missing edge or coordinate.
3. Run package tests and full workspace quality checks.
4. Update this ledger with all discrepancies and decisions.
5. Only change `CANONICAL_DATASET_AVAILABILITY` after independent topology and coordinate review, then integrate the renderer in a separate, reviewable change.

## Remaining verification work

- Resolve whether the supplied physical image’s apparent station `200` belongs to the target edition.
- Obtain a high-resolution, front-on image adequate for 199 station centers and every transport line.
- Independently transcribe and verify all taxi, bus, underground, and boat edges.
- Verify the complete starting-position set against the target-edition physical components.
- Record immutable revisions for any future external-source comparison.

Until those steps are complete, the visual foundation is not a canonical or multiplayer Scotland Yard implementation.
