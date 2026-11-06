# Scotland Yard Live — Phase 3C.3 Evidence Package Manifest

> **Purpose:** Inventory the available source material for the coordinate-reconstruction and bespoke-board work.
> **Status:** Working evidence manifest; verify the live repository paths and hashes before the final model handoff.
> **Core rule:** A source may be visually useful without being authoritative for every claim. Each asset below has a defined evidentiary role.

## 1. Evidence hierarchy

Apply the project's approved authority order. For board reconstruction, use the following more specific evidence handling:

1. **Original physical board photographs** — primary visual evidence for printed layout, visible station markers, visible transport lines, river/landmarks and board boundaries. Photographs may still be incomplete, angled, distorted, reflective or occluded.
2. **Original 1985 Milton Bradley / Funskool India rulebook** — primary textual evidence for rules, setup, ticket mechanics and any explicitly described routes or station references. It does not automatically prove the physical appearance or playable inventory of the photographed board.
3. **Starting-card photograph(s)** — primary evidence only for card values that can be read clearly. Do not extrapolate unreadable cards.
4. **Previously transcribed candidate edge dataset and audit documents** — structured observations and analysis, not canonical truth. Candidate status must be preserved.
5. **Other board photographs / alternate angles** — corroborating evidence, useful for resolving local visibility and overlap. They do not silently override the five-photo evidence set.
6. **Online board images / recreated maps / sample interfaces** — reference only. They are not authoritative for the supplied edition's geometry or topology.
7. **Video and its transcript** — separate roles: the video is a visual-art reference only; the transcript is a gameplay/rules aid only. Neither is board-coordinate evidence.

## 2. Primary board-photo set

The following five files are the designated primary photo set from the completed evidence audit. The filenames below are the repository names under `docs/game/evidence/board-photos/`. Keep these originals unchanged.

| Repository file     | Original dimensions | Intended evidentiary use                                                                                | Known limitations                                                                 |
| ------------------- | ------------------: | ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `complete.jpeg`     |          1280 × 892 | Overall board composition; global layout; approximate relation of major regions; cross-checking overlap | Perspective, resolution and local legibility may limit station/edge transcription |
| `top-left.jpeg`     |          925 × 1280 | Detailed upper-left region; local station markers and route tracing                                     | Partial region; perspective/overlap                                               |
| `top-right.jpeg`    |          885 × 1280 | Detailed upper-right region; local station markers and route tracing                                    | Partial region; perspective/overlap                                               |
| `bottom-left.jpeg`  |          914 × 1280 | Detailed lower-left region; local station markers and route tracing                                     | Partial region; perspective/overlap                                               |
| `bottom-right.jpeg` |         1080 × 1499 | Detailed lower-right region; local station markers and route tracing                                    | Partial region; perspective/overlap                                               |

The five photos overlap imperfectly. Treat them as separate observations until a reproducible registration/calibration process demonstrates how they fit together. Do not assume they form a perfect scan.

## 3. Supporting physical-board photographs

The uploaded context also contains these additional images. Their exact repository destinations must be checked before the final handoff; do not assume every uploaded filename has already been committed.

| Uploaded filename              |  Dimensions | Likely use                                                                         | Evidence caution                                                                                |
| ------------------------------ | ----------: | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `full-1.jpeg`                  | 1152 × 2048 | Alternate full-board photograph; compare overall appearance and visible regions    | Photograph, not a scan; check glare, angle and completeness                                     |
| `full-2.jpeg`                  | 1152 × 2048 | Alternate full-board photograph; corroboration                                     | Same limitations                                                                                |
| `full-3.jpeg`                  | 2160 × 3840 | Higher-resolution alternate full-board photograph; potentially useful local detail | High pixel count does not remove perspective, glare or lens distortion                          |
| `bottom right.jpeg`            | 1152 × 2048 | Additional lower-right detail                                                      | Partial/angled view                                                                             |
| `soctland-yard board pic.jpg`  | 1080 × 1920 | Earlier overall board photograph                                                   | Compare against the designated five-photo set; avoid treating as more authoritative by filename |
| `full-board-online-sample.png` |   760 × 570 | General visual comparison only                                                     | Online/recreated sample; not authoritative for this physical edition                            |
| `full-sample-2.webp`           | 1530 × 1200 | General visual comparison only; may help identify broad layout conventions         | Online/recreated sample; not authoritative for this physical edition                            |

`scotland-yard mrx board.jpg` (899 × 1599) is a photograph of Mr X/logbook-related components, not the board map. Do not use it for board geometry.

## 4. Starting cards

`starting cards.jpeg` (899 × 1599) shows a photograph of the blue starting-location cards.

Use only for card values that are unambiguously legible in the original image. The prior audit established that only 13 of 18 values were safely legible. This image does not justify guessing the remaining five values.

If the repository contains a higher-quality or separately cropped version, compare it, but retain the existing audit finding until all 18 are verified.

## 5. Rulebook

`scotland-yard official rules.pdf` is the supplied 12-page Milton Bradley / Funskool India rulebook.

Prior edition audit findings:

- Identified as the 1985 Milton Bradley / Funskool India edition, product `4500-X2` (rulebook page 12).
- It confirms an 18-card starting-location setup.
- It explicitly describes boat route legs `194–157`, `157–115`, and `115–118`.
- It does not settle whether the playable board inventory contains 199 or 200 stations.
- It does not by itself prove that the photographed board is the exact matching print run; the match is probable, not proven, because the photographed board's copyright/product panel has not been captured clearly.

The rulebook is authoritative for what it explicitly states. Do not infer additional station adjacency from its diagrams or narrative without checking the source and documenting the interpretation.

## 6. Video and transcript — keep their roles separate

### Video: `Video-79477.mp4`

- Duration: approximately 22.6 seconds; vertical video.
- Role: visual-art reference for the application's original art direction.
- The inspected frames show bold scarlet/red fields, black graphic silhouettes, warm off-white/cream paper-like surfaces, rough printed/cut-paper texture, high-contrast editorial composition and short graphic transitions.
- This is a broad stylistic reference, not a literal London illustration reference. Do not claim it supplies London landmarks or board design evidence.
- Use its general visual language in original UI artwork and framing; do not copy exact compositions, artwork, logos or protected assets.
- It provides no evidence about station positions, route topology, rules or board inventory.

### Transcript: `youtube_video_transcipt.txt`

- Role: supplementary gameplay explanation / rules reference.
- Use it to locate explanations and compare against the supplied rulebook.
- Where it differs from the supplied edition's rulebook or explicit user decisions, record the discrepancy rather than silently resolving it.
- It is not a coordinate source or visual-art source.

## 7. Existing structured evidence and audit documents

The final model should inspect the latest repository versions of these files, rather than relying only on this summary:

- `docs/game/BOARD-RECONSTRUCTION.md`
- `docs/game/BOARD-EVIDENCE-REGISTER.md`
- `docs/game/BOARD-COORDINATE-RECONSTRUCTION.md`
- `docs/game/BOARD-TRANSCRIPTION-WORKFLOW.md`
- `docs/game/BOARD-EDITION-IDENTITY.md`
- `docs/game/BOARD-CANONICAL-INVENTORY-DECISION.md`
- `docs/game/BOARD-STARTING-POSITIONS-AUDIT.md`
- `docs/game/BOARD-GRAPH-VERIFICATION.md`
- `docs/game/BOARD-CANONICAL-GRAPH-DECISION.md`
- `docs/game/data/board-edge-candidates-1-200.json`
- Associated candidate schema, validator and tests in the repository.
- `docs/game/PHASE-3C3-COORDINATE-RECONSTRUCTION-BRIEF.md`

These documents contain the current audit trail and provisional candidate graph. They are not interchangeable with the original source images.

## 8. Known unresolved facts — do not promote to canonical

At the last completed graph-verification checkpoint:

- Candidate edge records: 125.
- Verified edges: 0.
- Provisional edges: 121.
- Unresolved boat candidates: 4.
- Candidate transport inventory: taxi 66, bus 33, underground 22, boat 4.
- Nine endpoint pairs have multiple transport observations requiring careful interpretation.
- Five cross-boundary candidates remain provisional.
- Station marker 200 is visible in board evidence, but whether it is a playable station remains unresolved.
- `199–200` remains provisional, not canonical.
- Rulebook-supported boat route legs `194–157`, `157–115`, `115–118` still require physical-board corroboration.
- `108–115` is unsupported by the rulebook evidence examined in the audit.
- Only 13 of 18 starting-card values were safely legible.
- Exact photographed-board / rulebook edition match is probable, not proven.

If the repository audit documents have changed since this checkpoint, report the newer findings and cite the exact source. Do not blindly reuse stale counts.

## 9. Reconstruction method expected from the model

The model should propose and document a reproducible method, not jump straight to hand-authored coordinates.

1. Inspect the primary and supporting photos individually at useful zoom levels.
2. Identify board boundaries, overlap regions, stable landmarks and candidate control points.
3. Assess whether a single photograph, a selected photo, a multi-image mosaic, or a rectified composite is the best coordinate reference.
4. Evaluate perspective correction (for example, a homography where the image geometry supports it) and any necessary lens/rotation corrections.
5. Keep original photos immutable. Store derivatives separately and document each transform and source image.
6. Define a board-local coordinate system and justify its orientation, aspect ratio and units. Normalised coordinates are preferred for scalable SVG rendering, but the model must explain its chosen scheme.
7. Keep **printed marker inventory** separate from **confirmed playable station inventory**. A visible number is not proof that it is playable.
8. Extract station centres with provenance, confidence/uncertainty and a way to review the original image region.
9. Treat route geometry as a separate evidence task. Coordinate reconstruction must not create, infer or canonicalise graph edges.
10. Produce an overlay/reprojection review so the owner can compare extracted coordinates against the original photographs before implementation.

## 10. Final handoff package checklist

Before the strongest-model task begins, ensure the package includes:

- [ ] Consolidated project plan.
- [ ] Phase 3C.3 reconstruction brief.
- [ ] Design-system brief.
- [ ] Motion-component catalogue.
- [ ] Video art-direction reference.
- [ ] Current board evidence register and all board audit/decision documents.
- [ ] Candidate edge JSON, schema, validator and tests.
- [ ] Five primary board photographs, unchanged.
- [ ] Supporting board photos that are present in the repository.
- [ ] Original rulebook PDF.
- [ ] Starting-card photograph.
- [ ] Video file for visual reference, if upload size/context permits.
- [ ] Transcript as a separate rules reference.
- [ ] Current branch and working-tree status supplied by the owner; no agent Git operations.

The first strongest-model deliverable should be an **evidence and calibration proposal**, including identified limitations and a reviewable coordinate-extraction plan. Do not author canonical station coordinates, canonical edges or final board artwork until the proposal and its evidence assumptions have been reviewed and approved.
