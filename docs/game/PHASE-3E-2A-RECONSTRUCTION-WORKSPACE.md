# Phase 3E.2A — Complete Board Reconstruction Workspace

## Scope

This workspace prepares the complete transport-graph review process. It does not transcribe, promote or canonicalize transport edges. The original 125-row candidate artifact and the 199-station workbench dataset remain unchanged.

## Source inventory

The generated manifest indexes 28 readable sources:

- 5 original-reference board photographs.
- 6 close-up photographs.
- 16 high-resolution A1–D4 photographs.
- 1 derived `rectified_complete.png` reference.

Each source record contains its repository path, dimensions, SHA-256 and role. Original JPEGs are read-only inputs. The rulebook PDF is not present in this checkout and is not substituted.

## Coordinate systems and transformations

| Source                      | Coordinate system                                        | Transformation                                     |
| --------------------------- | -------------------------------------------------------- | -------------------------------------------------- |
| Original photographs        | Source-image pixel coordinates; dimensions vary by file  | Original pixels are preserved; no source overwrite |
| High-resolution tiles       | Source-image pixel coordinates                           | Phase 3D.3 source-to-board homography              |
| Registered/rectified images | 1350×1000 board canvas; origin top-left; x right; y down | Existing Phase 3D.3 registered tile outputs        |
| Station dataset             | Normalized `[0,1]` coordinates                           | `canvas_x = x * 1350`, `canvas_y = y * 1000`       |
| Candidate regions           | Historical prose/photo-region references                 | Not treated as measured coordinates                |

Each station receives one deterministic primary review target. Where a registered high-resolution tile covers the station centre, the workspace also stores a perspective-corrected source crop and its source-image corner coordinates. The registered crop remains available for common-board context.

## Workspace structure

- `station-crop-manifest.json` — 199 crop records, source hashes, canvas centres, source coordinates and boundary/fold flags.
- `station-review-queue.json` — exactly one primary review target per station, incident candidate IDs and review state.
- `station-crops/ST-###-registered.png` — registered board-context crops.
- `station-crops/ST-###-source.png` — perspective-corrected crops from the selected high-resolution original tile where available.
- `station-review-contact-sheet.png` — visual index; `B` marks boundary crops and `F` marks fold-adjacent crops.
- `edge-observations.json` — separate observation workspace containing all 125 existing candidates as `OBS-CAND-E-###`; `newObservations` is empty until human review discovers new connections.
- `phase-3e-2a-edge-observations.schema.json` — observation schema for future discoveries, uncertainty, contradictions and multi-transport duplicates.

## Phase 3E.2A.1 source-crop geometry validation

The source-crop manifest was audited and repaired without changing station positions, candidate observations or transport data. All 199 station records were checked against the selected high-resolution source dimensions, source quadrilateral geometry and Phase 3D.3 homographies.

- 53 records have valid, readable high-resolution source crops.
- 146 records use the explicit `rectified-fallback` provenance type because no containing tile produced a valid in-bounds source quadrilateral.
- 6 pre-existing invalid records were repaired: ST-051, ST-097, ST-098, ST-101, ST-120 and ST-162. ST-101 is no longer labelled as a valid B3 source crop with out-of-bounds coordinates.
- 146 fallback warnings remain. They indicate lack of a valid independent high-resolution crop; they do not invalidate the registered board-context crop or alter station data.
- Valid source records include source image dimensions, in-bounds ordered quadrilateral coordinates, transform status, output dimensions, source SHA-256 and coverage margin. Fallback records have no source quadrilateral or source-crop path and include an explicit reason.
- `source-crop-geometry-audit.json` records the audit counts and repaired-record history. `test_phase_3e2a1_geometry.py` covers IDs, crop readability, geometry, fallback provenance, ST-101 and manifest/audit consistency.

Known limitation: the fallback crop is the existing rectified-board context and must not be treated as an independent high-resolution photograph. Some stations remain outside the usable source quadrilateral of every registered tile under the existing Phase 3D.3 transforms.

## Existing candidate mapping

All 125 candidate IDs `E-001` through `E-125` appear exactly once in `edge-observations.json`. Original endpoints, transport, confidence, verification status, evidence references and explanations are copied as audit fields. Each imported observation links to the endpoint station crop IDs, but this link is a review aid and is not evidence that the edge is correct.

The nine multi-transport pairs and four unresolved candidates remain unchanged. No candidate is promoted, deleted, merged or split.

## Complete-board coverage strategy

Review the queue in station order, inspecting each source crop for every incident taxi, bus, underground and boat line. Record each observation with both endpoint labels, transport identity, source tile/crop and registered coordinates. A station is complete only when its incident lines have been reviewed; station presence or printed service symbols do not substitute for route tracing.

Prioritize fold/boundary stations, the nine multi-transport pairs, the four unresolved boat candidates, cross-boundary candidates and the `199–200` dependency. Use the queue’s `incidentExistingCandidateIds` to reconcile old observations while allowing new observations to be added separately.

## Known limitations

- The station coordinates are best-effort and some are approximate; crops inherit that uncertainty.
- A registered tile may not cover every station centre; fallback crops use the existing rectified board reference and record that limitation.
- Source crops are evidence aids, not canonical route decisions.
- Marker 200 remains outside playable station review IDs.
- Starting-card evidence remains incomplete.
- No transport graph or frontend behavior was changed.

## Regeneration and validation

From the repository root:

```powershell
tools/board-calibration/.venv/Scripts/python.exe tools/phase_3e2a_workspace.py
tools/board-calibration/.venv/Scripts/python.exe -m unittest discover -s tools/board-calibration/tests -p "test_*.py"
node docs/game/data/validate-board-edge-candidates.mjs
```

The generator asserts 199 station crops, 125 imported candidates, valid source files, unique IDs and byte-level preservation of `stations.json` and `board-edge-candidates-1-200.json`.

## Phase 3E.2B next steps

Phase 3E.2B should use this workspace to perform human station-centered route tracing, append new observations, reconcile duplicates and conflicts, and produce a separate reviewed graph proposal. It must keep observations separate from accepted canonical gameplay edges and must not change canonical dataset availability until the graph passes its evidence and validation gates.
