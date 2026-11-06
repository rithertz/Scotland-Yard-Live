# Scotland Yard Live — Phase 3C.3 Reconstruction Brief

> **Status:** Prepared handoff brief; to be reviewed against the live repository before execution
> **Phase:** 3C.3 — Coordinate Reconstruction and Bespoke Canonical-Style Board Rendering
> **Audience:** A fresh, high-capability multimodal reasoning/design model, followed by the implementation agent
> **Repository owner:** User
> **Git authority:** User only
> **Last known project checkpoint:** Phase 3C.2 completed; commit `a32b9c9` on `feat/board-graph-verification` was pushed to origin
> **Important:** This brief supplements the approved project plan and existing visual specification. It does not override verified evidence or authorize guesses.

---

## 1. Purpose of this brief

This document gives a new model enough project context to work on the most demanding part of the Scotland Yard Live board reconstruction without relying on earlier chat history.

The task is not simply to draw a plausible London map. It is to reconstruct the **specific physical Milton Bradley 1985 Scotland Yard board edition supplied by the project owner**, preserving its station layout, relative geography, numbering, transport-route appearance and distinctive Thames/landmark composition.

The result must be visually faithful while keeping a strict boundary between:

- what the physical evidence actually establishes;
- what can be geometrically estimated from photographs;
- what remains uncertain;
- what is only presentation styling;
- what is canonical gameplay data.

The board renderer must never invent gameplay topology. A visually plausible line is not proof of a transport edge.

## 2. Project identity and product context

Scotland Yard Live is a private, live-multiplayer web recreation of the original Scotland Yard board game for the project owner's friends. The first release targets 3–6 players, private rooms and faithful original gameplay. The project is deliberately not a generic London map, custom-map editor or global-scale game platform.

The implementation is an established TypeScript monorepo with React/Vite frontend, server, shared contracts, database and board-data packages. The exact current repository structure, scripts, dependencies and implementation state **must be inspected in the live checkout**; do not rely on old planning snapshots for current code details.

The approved visual direction is bespoke **“Metropolitan Casefile”**: warm paper/parchment, restrained district shading, inked map detail, deep ink/navy, crimson and brass/gold accents, clear transport colours and a polished tactical casefile atmosphere. Do not use Richup.io as a visual reference. Do not copy a later Ravensburger board or unlicensed external board artwork.

## 3. Authority and source hierarchy

Follow this hierarchy:

1. Explicit decisions made by the project owner in the current project conversation.
2. Verified original game rules and physical source materials.
3. The approved `Scotland-Yard-Live-Consolidated-Project-Plan.md`.
4. The current board evidence, reconstruction, graph-verification and visual-experience documents in the repository.
5. Other supplied historical context documents, only when they do not conflict with the above.
6. Model or coding-agent recommendations, which are proposals and never become requirements without owner approval.

If sources conflict, do not silently reconcile them. Record the conflict, identify what evidence would resolve it, and ask the owner when the choice affects canonical data or product behavior.

The consolidated plan contains some historical metadata and early assumptions that may no longer reflect implementation progress. In particular, its original 199-location assumption must not be used to dismiss the later physical evidence showing a printed marker 200. Use the current evidence and audit documents to represent the unresolved inventory honestly.

## 4. Current reconstruction status — read carefully

The following is the last known project state. Verify it against the live repository before relying on it.

### Completed work

- Phase 3A established the visual foundation and a synthetic SVG board viewport, including pan/zoom and selection. The synthetic fixture is explicitly not canonical.
- Phase 3B established the `packages/board-data` foundation, evidence registers, transcription workflow and candidate transport dataset.
- Five higher-coverage physical board photographs were added to `docs/game/evidence/board-photos/`.
- Candidate transport transcription covers 125 candidate records: 66 taxi, 33 bus, 22 underground and 4 boat.
- Phase 3B.6 reviewed ambiguous/multimodal observations but retained uncertainty where evidence did not justify promotion.
- Phase 3C.1 audited edition identity, station inventory and starting positions.
- Phase 3C.2 completed a full transport graph verification audit and chose **Option B: evidence insufficient; no canonical transport graph introduced**.

### Phase 3C.2 result

- Candidate edges: 125.
- Verified: 0.
- Provisional: 121.
- Unresolved: 4 boat candidates.
- Taxi: 66 provisional.
- Bus: 33 provisional.
- Underground: 22 provisional.
- Boat: 4 unresolved.
- Nine endpoint pairs have conflicting transport observations.
- The supplied rulebook supports boat legs `194–157`, `157–115`, and `115–118`, but these have not been physically verified against the photographed board edition.
- `108–115` remains unsupported.
- Station marker 200 is visibly printed on the supplied physical board photos, but whether it is a playable station remains unresolved.
- `199–200` remains provisional and must not be treated as a canonical playable connection.
- The supplied rulebook is identified as 1985 Milton Bradley / Funskool India, product `4500-X2`; the exact match between that rulebook and the photographed board remains probable, not proven.
- Only 13 of the 18 starting-card values were safely legible in the supplied evidence; do not treat a guessed or externally sourced list as canonical.

**Critical consequence:** Phase 3C.3 may reconstruct visual positions of visible markers and board geometry as evidence-qualified visual data, but it must not create a canonical station inventory or canonical transport graph by implication. Do not render a candidate line as an authoritative playable route.

## 5. Required source files to inspect

Before analysis or edits, inspect the current repository versions of at least:

### Project and visual authority

- `Scotland-Yard-Live-Consolidated-Project-Plan.md`
- `SCOTLAND_YARD_LIVE_VISUAL_EXPERIENCE_SPEC.md`
- `docs/README.md`
- `docs/game/BOARD-RECONSTRUCTION.md`

### Evidence and uncertainty

- `docs/game/BOARD-EVIDENCE-REGISTER.md`
- `docs/game/BOARD-COORDINATE-RECONSTRUCTION.md`
- `docs/game/BOARD-TRANSCRIPTION-WORKFLOW.md`
- `docs/game/BOARD-EDITION-IDENTITY.md`
- `docs/game/BOARD-CANONICAL-INVENTORY-DECISION.md`
- `docs/game/BOARD-STARTING-POSITIONS-AUDIT.md`
- `docs/game/BOARD-DISCREPANCY-LEDGER.md`
- `docs/game/BOARD-EDGE-TRANSCRIPTION.md`
- `docs/game/BOARD-EDGE-HUMAN-REVIEW.md`
- `docs/game/BOARD-GRAPH-VERIFICATION.md`
- `docs/game/BOARD-CANONICAL-GRAPH-DECISION.md`

### Data and implementation

- `docs/game/data/board-edge-candidates-1-200.json`
- `docs/game/data/board-edge-candidates.schema.json`
- `docs/game/data/validate-board-edge-candidates.mjs`
- `packages/board-data/` (all current source, tests and README)
- `apps/web/src/features/board/` (current renderer, viewport, fixtures, tests and types)
- Relevant frontend design tokens and styles

### Primary visual evidence

Inspect the five original photographs in:

- `docs/game/evidence/board-photos/complete.jpeg`
- `docs/game/evidence/board-photos/top-left.jpeg`
- `docs/game/evidence/board-photos/top-right.jpeg`
- `docs/game/evidence/board-photos/bottom-left.jpeg`
- `docs/game/evidence/board-photos/bottom-right.jpeg`

Also inspect any additional source images, the original scanned rulebook and relevant evidence assets available in the repository. The five photos are primary evidence; do not replace them with a web image or a later-edition board.

Preserve all original evidence files byte-for-byte. Work on derived copies for rotation, cropping, rectification, contrast or annotation.

## 6. Main objective

Develop a defensible reconstruction of the physical board's **visual geometry and station-marker positions**, and prepare a bespoke SVG board design that can ultimately consume verified board data.

The work should proceed in controlled sub-stages:

### Stage 3C.3-A — Evidence and calibration assessment

1. Inspect all five board photographs at full resolution.
2. Identify the actual printed board boundary and its orientation.
3. Assess overlap between the complete photo and four detail photos.
4. Determine which photos are suitable for global geometry, local detail and cross-checking.
5. Identify perspective distortion, rotation, lens/phone distortion, fold/crease, glare, blur, occlusion and uneven lighting.
6. Determine whether the photos support a reliable projective rectification and whether a single homography is sufficient.
7. Identify stable calibration features: board corners, printed border intersections, grid/landmark anchors, river bends, park boundaries or other unambiguous fixed geometry.
8. Establish a reproducible calibration workflow. Keep raw-image pixel coordinates distinct from rectified-board coordinates and final SVG coordinates.
9. Produce a coverage/quality map showing where station IDs and marker centres are readable versus ambiguous.
10. State clearly whether the evidence is sufficient for complete coordinate extraction. If not, specify exact additional photographs/scans needed.

Do not begin by manually guessing every station coordinate.

### Stage 3C.3-B — Coordinate reconstruction

If evidence quality supports it:

1. Define one stable board coordinate space with an explicit aspect ratio and origin.
2. Define transformations from each source image into the common rectified board plane.
3. Identify station-marker centres, not merely number-label centres.
4. Cross-check each station across overlapping images wherever possible.
5. Record coordinate precision appropriate to the image quality; do not imply false sub-pixel certainty.
6. Store evidence provenance per station or per coordinate batch.
7. Assign confidence/status using an explicit documented rubric.
8. Keep uncertain markers separate from confirmed markers.
9. Treat printed marker 200 as a visible marker whose playable status remains unresolved.
10. Do not fabricate a missing marker, infer a marker from numbering sequence, or force the inventory to 199/200.

A coordinate may be geometrically well located while its playable-station status remains unresolved. Keep these two questions separate.

### Stage 3C.3-C — Bespoke SVG board design

Design the board as a vector reconstruction of the physical board, not a generic basemap.

Use the existing `SCOTLAND_YARD_LIVE_VISUAL_EXPERIENCE_SPEC.md` as the primary visual authority, especially:

- “Metropolitan Casefile” art direction.
- Board as digital reconstruction of the physical board.
- Preserve relative geography and station placement.
- Layered SVG architecture.
- Stable viewBox / coordinate contract.
- Station marker and label separation.
- Transport route styling.
- Pan/zoom and accessible interaction.
- Responsive behavior and visual testing.

Expected SVG scene layers (align with the existing specification and current code rather than duplicating unnecessarily):

1. Board background: paper, board border, subtle districts and geographic context.
2. Street/landmark detail: restrained and subordinate to actual board geometry.
3. Thames/river and bridges.
4. Transport routes: only when their visual source and confidence are clear; candidate/unverified topology must not be presented as canonical playable connectivity.
5. Station markers.
6. Station labels.
7. Move hints and legal-destination highlights (future runtime state, not static canonical content).
8. Pawns (future runtime state, not part of the static board asset).
9. Selection, hover/focus and transient effects.

Do not make decorative detail more visually dominant than station positions and route readability.

### Stage 3C.3-D — Integration proposal

Inspect the existing synthetic SVG renderer and propose the smallest maintainable integration path.

Prefer:

- SVG rendering from structured data rather than hard-coded station markup.
- Clear separation between board geometry, station visual positions, transport graph data and runtime game state.
- A stable viewBox and reusable layers.
- Separate label offsets from station coordinates.
- Accessible station hit targets larger than visible marker circles.
- Zoom/pan transformations applied to the scene as a whole.
- Typed data contracts aligned with the existing `packages/board-data` architecture.

Do not couple the SVG to candidate-edge JSON or treat the renderer as a source of movement legality.

## 7. Coordinate and calibration principles

Use the existing visual specification's normalized coordinate concept or an explicitly justified fixed design-space coordinate system.

A normalized point may be represented conceptually as:

```ts
type BoardPoint = {
  x: number; // 0..1 in the rectified board plane
  y: number; // 0..1 in the rectified board plane
};
```

This is illustrative, not a mandate to change existing public types without inspection.

Required principles:

- Define whether coordinates refer to the outer board border, inner map area or another stable rectangle.
- Define axis orientation and origin.
- Preserve board aspect ratio.
- Record source-image IDs/filenames, calibration transform/version, evidence region and confidence.
- Keep raw pixels, rectified-board coordinates and SVG viewBox coordinates explicitly distinguishable.
- Do not use raw photo pixels as canonical coordinates without perspective correction.
- Do not warp each photo independently in a way that makes overlapping features disagree.
- Do not use label positions as station centres.
- Keep label offsets as presentation metadata.
- Preserve sufficient precision in data; round only for display.
- Quantify expected positional error where possible.
- Validate overlap residuals and landmark residuals.
- Avoid hand-adjusting individual coordinates without documenting why and recording the adjustment.
- Never imply a coordinate is canonical solely because it is stored in a structured file.

A useful data model may distinguish:

- `observedMarker`: a visible printed marker in source evidence;
- `stationIdentity`: whether the marker is confirmed as a playable station;
- `visualPosition`: estimated position in the board plane;
- `positionEvidence`: source and calibration provenance;
- `positionConfidence`: quality of the geometric estimate;
- `inventoryStatus`: confirmed / unresolved / excluded, according to project terminology.

Do not add this model blindly. Inspect existing schemas and propose a compatible extension first.

## 8. Evidence and uncertainty policy

Maintain separate statuses for at least these dimensions:

| Dimension          | Example question                                                                      |
| ------------------ | ------------------------------------------------------------------------------------- |
| Marker visibility  | Is a printed numbered marker visible?                                                 |
| Marker identity    | Can its number be read reliably?                                                      |
| Geometric location | Can its centre be located reliably in the rectified board plane?                      |
| Playable inventory | Is it confirmed as a playable station?                                                |
| Transport topology | Are its incident transport edges verified?                                            |
| Visual styling     | Is the drawn line/shape an evidence-backed reproduction or an illustrative treatment? |

Do not collapse these into one generic confidence field.

For station 200:

- The printed marker is visible in the photographs.
- Its playable status is unresolved.
- Its position may be recorded as an observed visual marker if reliably calibrated.
- It must not be included in a canonical playable station inventory without new evidence and owner approval.
- The provisional `199–200` edge must not be drawn as an authoritative playable connection.

For transport routes:

- Phase 3C.2 found no verified candidate edges.
- Do not convert all 125 candidate records into canonical route paths.
- If visual linework can be traced from the photo, record it as a visual observation with provenance, distinct from a verified graph edge.
- Where a route is obscured or ambiguous, preserve the ambiguity rather than connecting plausible endpoints.

## 9. Additional evidence likely needed

The existing audit documents identify these outstanding evidence needs:

1. A straight-on, high-resolution photograph or scan of the board's copyright/product panel to establish the photographed board's edition identity.
2. A high-resolution close-up of station marker 200 and its incident route markings.
3. A complete, controlled photograph of all 18 starting cards, readable in one or more overlapping images.
4. If the five current photographs do not support reliable global rectification, new flat, straight-on, evenly lit, overlapping board scans/photos with all board corners visible.

The model must inspect the actual assets before deciding what is necessary. Do not ask for new images if the supplied evidence already supports the task. Conversely, do not pretend existing photos are sufficient if they are not.

When requesting new images, specify:

- exact target region;
- camera orientation and distance;
- lighting and glare constraints;
- required resolution/legibility;
- overlap and corner visibility;
- why the image resolves a named uncertainty.

## 10. Visual design constraints

The renderer should preserve the physical board's geography and visual hierarchy while improving legibility for screens.

- It is not a generic London basemap.
- It is not a later Ravensburger edition.
- Do not invent or relocate stations to improve composition.
- Do not simplify away meaningful river bends, bridges, district/park boundaries or relative station clusters.
- Keep route strokes visually differentiated by transport type, consistent with the source board and approved visual spec.
- Preserve station numbering and avoid label collisions through separate label-offset metadata.
- Keep decorative texture low contrast.
- Avoid excessive gradients, glows, glassmorphism or game-dashboard clutter.
- Use the existing project's dark ink/navy, crimson, brass and parchment visual language around the board; the board itself should remain faithful and legible.
- Support reduced motion, keyboard focus, accessible names and usable touch targets.
- Keep the board's aspect ratio stable during responsive scaling.

Do not use external map datasets or third-party board scans as replacements for the supplied physical source. External material may be used only as clearly labeled comparative research if the owner authorizes it.

## 11. Implementation boundaries

Before changing code, inspect the current implementation and determine whether this phase should produce:

- evidence/calibration artifacts only;
- a station visual-coordinate dataset for observed markers;
- a board background/geometry SVG;
- renderer integration using the existing synthetic fixture contract;
- or some combination of these.

The agent must recommend a bounded sequence and explain dependencies before making a broad implementation change.

Strictly out of scope:

- canonical transport graph creation;
- canonical playable station inventory decision;
- canonical starting-position list;
- game-engine rules or legal-move logic;
- multiplayer/server behavior;
- room logic;
- new map editor or user-generated maps;
- deployment, accounts, matchmaking or global scaling;
- arbitrary redesign of unrelated frontend screens.

Do not silently change `packages/board-data` semantics. If a schema change is needed, explain migration and compatibility impact.

## 12. Required deliverables

At minimum, produce a reviewable reconstruction package containing:

1. `docs/game/BOARD-IMAGE-CALIBRATION.md`
   - source image inventory and dimensions;
   - board-boundary identification;
   - image quality and overlap assessment;
   - rectification/calibration method;
   - calibration anchors and residual/error analysis;
   - reproducible procedure and known limitations.

2. `docs/game/BOARD-VISUAL-COORDINATE-REGISTER.md`
   - one row per observed numbered marker;
   - marker identity status;
   - normalized/fixed-space coordinate where supportable;
   - source image provenance;
   - confidence and unresolved notes;
   - explicit handling of marker 200;
   - no inferred playable inventory.

3. A typed, machine-readable visual-coordinate dataset, if evidence supports it.
   - It must remain separate from canonical gameplay graph data.
   - It must carry provenance/status rather than presenting every point as canonical.

4. A bespoke SVG board asset or a documented design proposal if implementation is not yet justified.
   - The SVG must consume structured visual data where practical.
   - No fabricated canonical transport edges.

5. Updated `docs/README.md` and relevant reconstruction/evidence docs.

6. Tests/validators for coordinate data and SVG integration if code/data is introduced.

The model may recommend different filenames if the repository already has equivalent artifacts. Avoid duplicate documentation.

## 13. Testing and validation

If coordinate data is added, test at least:

- coordinate bounds and finite numeric values;
- unique marker identifiers;
- required provenance;
- valid confidence/status combinations;
- separation of marker visibility from playable inventory status;
- station 200 unresolved behavior;
- no accidental promotion into canonical board data;
- stable aspect ratio / viewBox contract;
- no duplicate or missing IDs within the chosen visual-marker inventory;
- deterministic parsing and rendering.

If calibration transformations are implemented, test:

- transform round-trip or expected mapping behavior;
- anchor residual bounds;
- consistency of overlapping source images;
- malformed/degenerate calibration input handling.

If SVG is modified, test:

- correct rendering of supplied visual data;
- separation of labels and marker positions;
- keyboard focus and accessible station names;
- pan/zoom not mutating board data or game state;
- no hidden Mr X or runtime gameplay data leaks into the static board asset.

Run relevant repository checks, based on actual package scripts:

- focused tests;
- format check;
- lint;
- typecheck;
- full test suite;
- build;
- data validators;
- visual/manual comparison;
- `git diff --check` (the coding agent may run read-only Git inspection/check commands only if the owner permits; it must not perform Git mutations).

Do not claim visual fidelity based only on a successful build. Include side-by-side comparisons or documented manual review criteria.

## 14. Work protocol for the high-capability model

This phase should use the strongest available multimodal reasoning/design model because it combines image interpretation, geometric reasoning, uncertainty management and visual-system design.

The model starts with no chat history. It must rely on this brief and the live repository.

Work in gated steps:

### Gate 1 — Context and evidence audit

- Read all required repository documents.
- Inspect all source images and current renderer.
- Produce a concise but substantive state-of-evidence report.
- Identify contradictions and stale documentation.
- Do not edit code or generate coordinates yet.
- State whether the supplied evidence is sufficient for reliable calibration.

Wait for owner review if any material decision is required.

### Gate 2 — Calibration plan and prototype

- Propose the board-plane coordinate system.
- Identify calibration anchors and transformations.
- Demonstrate the method on a small representative region and overlapping photographs.
- Report residuals/error and limitations.
- Do not extrapolate the method to the entire board until the prototype is credible.

### Gate 3 — Full visual-marker coordinate extraction

- Extract only what the evidence supports.
- Cross-check overlaps.
- Preserve uncertain IDs/positions.
- Produce machine-readable data and a human-review register.
- Keep playable-inventory status separate.

### Gate 4 — Board visual design and implementation plan

- Present the proposed SVG composition, layer design, visual treatment and data contract.
- Compare it with the physical board and approved visual specification.
- Identify which linework is decorative, directly observed or graph-backed.
- Obtain owner approval for material design/data decisions before broad implementation.

### Gate 5 — Implementation and verification

- Implement only the approved bounded scope.
- Add tests and validators.
- Run checks and provide visual comparison evidence.
- Stop if implementation would require unsupported topology or inventory assumptions.

The owner may choose to use one model for analysis/design and Codex for implementation. The model must produce artifacts and a precise implementation handoff rather than assume it has permission to change everything.

## 15. Agent and Git permissions

The repository owner performs all Git operations.

The model/agent must not:

- create or delete branches;
- commit or amend commits;
- push;
- merge or rebase;
- force-push;
- alter GitHub settings or branch protection;
- open or merge pull requests;
- deploy;
- modify secrets.

It may inspect the repository, edit approved project files and run local checks within the approved task scope.

Do not run Git commands unless the owner explicitly asks. Never claim a push, commit or merge occurred.

## 16. Required final report

At each gate, report:

- findings and evidence used;
- files inspected;
- files created/modified;
- coordinate/calibration method;
- confidence and limitations;
- unresolved questions;
- test/check commands and actual outcomes;
- visual comparison evidence;
- decisions requiring owner approval;
- recommended next bounded step.

Never report the board as canonical unless station inventory, graph topology and relevant provenance have independently passed their acceptance gates.

## 17. Definition of success for Phase 3C.3

Phase 3C.3 is successful when:

- the physical board's geometry has been reconstructed using a reproducible, documented calibration process;
- observed marker positions are traceable to source evidence;
- uncertain marker identities/positions are explicitly represented;
- station 200 has not been silently declared playable;
- visual data is kept separate from canonical graph and game rules;
- a bespoke SVG design faithfully represents the photographed edition;
- the existing renderer can consume structured visual data without owning gameplay logic;
- the output is reviewable, testable and ready for the later canonical-data integration/acceptance phase;
- any remaining evidence gaps are explicit and actionable.

A partial but honest reconstruction is preferable to a complete-looking board with fabricated coordinates, stations or routes.

---

## Appendix A — Known source-image inventory

The five current project evidence photos were previously recorded with these dimensions and file sizes. Reconfirm against the live repository; do not assume files are unchanged.

| File                | Recorded dimensions | Recorded size |
| ------------------- | ------------------: | ------------: |
| `complete.jpeg`     |          1280 × 892 | 368,710 bytes |
| `top-left.jpeg`     |          925 × 1280 | 331,252 bytes |
| `top-right.jpeg`    |          885 × 1280 | 307,440 bytes |
| `bottom-left.jpeg`  |          914 × 1280 | 324,563 bytes |
| `bottom-right.jpeg` |         1080 × 1499 | 484,705 bytes |

These are the five-photo set committed in the Phase 3B.2 evidence checkpoint. Other older photographs exist in the original context pack and may be useful as secondary corroboration, but the five committed images are the current primary photo set.

## Appendix B — Important distinctions to preserve

- **Visible marker** does not automatically mean **playable station**.
- **Readable station number** does not automatically mean **canonical inventory membership**.
- **Geometrically estimated position** does not automatically mean **canonical coordinate**.
- **Visible route stroke** does not automatically mean **verified transport edge**.
- **Rulebook-supported boat leg** does not automatically prove the photographed board is the exact same printing.
- **SVG linework** does not define movement legality.
- **A visually polished board** does not prove topology or station inventory correctness.
- **A successful test/build** does not prove physical-board fidelity.

The governing principle for this phase is:

**Reconstruct what the evidence shows, preserve what it does not resolve, and never let visual design silently become gameplay truth.**
