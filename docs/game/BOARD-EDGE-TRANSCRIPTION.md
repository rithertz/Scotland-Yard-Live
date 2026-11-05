# Physical transport-edge transcription

## Status

This document is the consolidated evidence boundary for transport connections. Phase 3B.3 contains the original 1–100 review set. Phase 3B.4 adds a deliberately partial 101–200 set, cross-boundary observations, and separate unresolved boat-route records. All rows remain **provisional or unresolved visual observations**, not canonical graph data.

The canonical graph and `packages/board-data/src` are unchanged.

Phase 3B.5 mirrors the evidence rows into [`data/board-edge-candidates-1-200.json`](data/board-edge-candidates-1-200.json), validated by [`data/validate-board-edge-candidates.mjs`](data/validate-board-edge-candidates.mjs) against [`data/board-edge-candidates.schema.json`](data/board-edge-candidates.schema.json). That artifact is explicitly non-canonical and non-playable. It does not add station records, coordinates, or movement behavior.

## Transport evidence convention

The physical board distinguishes:

- solid yellow: taxi;
- solid green: bus;
- dashed red: underground.

Boat evidence is handled separately because the Thames route and endpoint discrepancy remain unresolved. A station’s visible service icon is not an edge.

## Current edge counts

| Transport   | Verified | Provisional | Unresolved candidate rows | Canonical added |
| ----------- | -------: | ----------: | ------------------------: | --------------: |
| taxi        |        0 |          66 |                         0 |               0 |
| bus         |        0 |          33 |                         0 |               0 |
| underground |        0 |          22 |                         0 |               0 |
| boat        |        0 |           0 |                         4 |               0 |

The recalculated candidate inventory is 66 taxi, 33 bus, 22 underground, and 4 boat rows: 125 total candidate records. The earlier 134-record summary was inconsistent with the actual tables and is recorded in the discrepancy ledger; no source rows were removed.

Phase 3B.6 reviewed the nine multi-transport endpoint pairs, all 22 low-confidence records, and the five cross-boundary records against the five photographs. The review found no independently traceable basis to promote or delete any candidate. Shared corridors remain possible multi-modal connections; boat records remain unresolved.

No row is entered merely because two visible station markers are geographically close. The next pass must use annotated crops and record each endpoint and transport colour explicitly.

## Provisional edge inventory: stations 1–100

Each row is one undirected physical observation. The source field names the strongest close-up; `complete.jpeg` supplies overall continuity. These are not canonical records and remain provisional until a second reviewer verifies the endpoint trace.

### Taxi — solid yellow

| From |  To | Evidence         | Region              | Confidence | Status      | Visual explanation / follow-up                                                        |
| ---: | --: | ---------------- | ------------------- | ---------- | ----------- | ------------------------------------------------------------------------------------- |
|    1 |   8 | `top-left.jpeg`  | upper-right of crop | medium     | provisional | Solid yellow route leaves marker 1 toward 8; inspect the junction beside 1.           |
|    2 |  10 | `top-left.jpeg`  | park/eastern edge   | high       | provisional | Yellow route visibly joins markers 2 and 10.                                          |
|    2 |  20 | `top-left.jpeg`  | park/western edge   | medium     | provisional | Yellow route appears to leave 2 toward 20; confirm continuation at the park boundary. |
|    3 |   4 | `top-left.jpeg`  | upper-right         | high       | provisional | Short yellow road between the adjacent markers.                                       |
|    4 |  13 | `top-left.jpeg`  | upper-central       | medium     | provisional | Yellow route continues from 4 toward 13; inspect the red route crossing.              |
|    5 |  15 | `top-right.jpeg` | upper-right         | high       | provisional | Yellow route visibly connects the northern 5 marker to 15.                            |
|    6 |   7 | `top-right.jpeg` | upper-right edge    | high       | provisional | Short yellow route between 6 and 7.                                                   |
|    7 |  17 | `top-right.jpeg` | upper-right edge    | high       | provisional | Yellow route continues from 7 to 17.                                                  |
|    8 |  18 | `top-left.jpeg`  | upper-left          | medium     | provisional | Yellow route is visible near the 8/18 corridor; confirm endpoint at 18.               |
|    9 |  20 | `top-left.jpeg`  | upper-central       | high       | provisional | Yellow route from 9 to 20 is visible around the park boundary.                        |
|   10 |  11 | `top-left.jpeg`  | central park edge   | high       | provisional | Short yellow connection between 10 and 11.                                            |
|   11 |  22 | `top-left.jpeg`  | central             | medium     | provisional | Yellow corridor reaches 22; green route shares part of the corridor.                  |
|   12 |  23 | `top-left.jpeg`  | central             | medium     | provisional | Yellow route appears to reach 23; inspect the crossing at 23.                         |
|   13 |  14 | `top-right.jpeg` | upper-central/right | high       | provisional | Yellow route is visible between 13 and 14.                                            |
|   14 |  15 | `top-right.jpeg` | upper-right         | high       | provisional | Yellow route continues between adjacent 14 and 15 markers.                            |
|   15 |  16 | `top-right.jpeg` | upper-right         | medium     | provisional | Yellow route corridor visible; red route also crosses nearby.                         |
|   16 |  29 | `top-right.jpeg` | upper-right/central | medium     | provisional | Yellow route appears to connect 16 and 29; verify marker endpoint.                    |
|   17 |  30 | `top-right.jpeg` | eastern edge        | high       | provisional | Yellow route visibly links 17 and 30.                                                 |
|   18 |  31 | `top-left.jpeg`  | upper-left          | high       | provisional | Yellow route between 18 and 31 is visible.                                            |
|   19 |  32 | `top-left.jpeg`  | upper-left/central  | high       | provisional | Yellow route between 19 and 32 is visible.                                            |
|   20 |  33 | `top-left.jpeg`  | central park edge   | medium     | provisional | Yellow route leaves 20 toward 33; check crossing with red line.                       |

### Bus — solid green

| From |  To | Evidence         | Region              | Confidence | Status      | Visual explanation / follow-up                                                   |
| ---: | --: | ---------------- | ------------------- | ---------- | ----------- | -------------------------------------------------------------------------------- |
|    3 |  11 | `top-left.jpeg`  | upper-central       | medium     | provisional | Green corridor reaches 11; confirm it does not terminate at the nearby crossing. |
|    3 |  12 | `top-left.jpeg`  | upper-central       | medium     | provisional | Green corridor reaches 12; inspect the shared road segment.                      |
|    7 |  42 | `top-right.jpeg` | eastern edge        | medium     | provisional | Green route descends from 7 toward 42; endpoint is near crop boundary.           |
|   11 |  22 | `top-left.jpeg`  | central             | medium     | provisional | Green route shares the 11/22 corridor; separate from yellow evidence.            |
|   13 |  14 | `top-right.jpeg` | upper-central/right | medium     | provisional | Green line is visible alongside the yellow corridor.                             |
|   14 |  15 | `top-right.jpeg` | upper-right         | medium     | provisional | Green line continues between 14 and 15; verify at the station markers.           |
|   15 |  29 | `top-right.jpeg` | upper-right/central | medium     | provisional | Green route crosses the 15/29 corridor; inspect line layering.                   |
|   15 |  41 | `top-right.jpeg` | eastern-central     | low        | provisional | Green route appears to leave 15 toward 41; needs a tighter crop.                 |
|   22 |  23 | `top-left.jpeg`  | central             | medium     | provisional | Green route visibly follows the corridor between 22 and 23.                      |
|   22 |  34 | `top-left.jpeg`  | central park edge   | medium     | provisional | Green route continues from 22 toward 34; check the line split.                   |

### Underground — dashed red

| From |  To | Evidence         | Region             | Confidence | Status      | Visual explanation / follow-up                                                          |
| ---: | --: | ---------------- | ------------------ | ---------- | ----------- | --------------------------------------------------------------------------------------- |
|    1 |  46 | `top-left.jpeg`  | upper-left/central | medium     | provisional | Dashed red route leaves 1 toward the central 46 marker; verify the long diagonal trace. |
|   13 |  46 | `top-left.jpeg`  | central            | medium     | provisional | Dashed red route approaches 46 from the 13 corridor.                                    |
|   13 |  67 | `top-right.jpeg` | central/right      | medium     | provisional | Dashed red route continues from 13 toward 67; crossing near 67 requires review.         |
|   13 |  89 | `top-right.jpeg` | central/right      | low        | provisional | Red route appears to continue toward 89; endpoint is distant and requires annotation.   |
|   46 |  74 | `top-left.jpeg`  | central-left       | medium     | provisional | Dashed red route runs between 46 and 74.                                                |
|   46 |  79 | `top-left.jpeg`  | central            | medium     | provisional | Dashed red route appears to reach 79; inspect overlap with the 46/74 corridor.          |
|   67 |  79 | `top-right.jpeg` | central            | medium     | provisional | Dashed red line is visible between 67 and 79.                                           |
|   67 |  89 | `top-right.jpeg` | central/right      | low        | provisional | Long red corridor appears to connect 67 and 89; requires a close annotated crop.        |
|   79 |  93 | `top-left.jpeg`  | central-left       | medium     | provisional | Dashed red route continues from 79 toward 93.                                           |
|   79 | 100 | `top-left.jpeg`  | lower-central      | low        | provisional | Red line appears to continue toward 100; endpoint is near lower crop boundary.          |

These 41 rows are a first-pass review set, not a claim that the 1–100 graph is complete. The low-confidence rows are retained so a reviewer can confirm or reject them rather than allowing them to disappear silently.

## Boundary audit

The original Phase 3B.3 1–100 set contained no edge whose second endpoint was above 100. Phase 3B.4 now records five provisional cross-boundary candidates below. Additional boundary edges remain unresolved and require explicit inspection.

## Provisional edge inventory: stations 101–200

The following Phase 3B.4 rows are new observations. They use the same evidence standard as the earlier 1–100 rows and are not canonical data. The lower-board close-ups are rotated and contain dense route crossings, so all remain provisional pending annotated-crop review.

### Taxi — solid yellow

| From |  To | Evidence            | Region                     | Confidence | Status      | Visual explanation / follow-up                                                                 |
| ---: | --: | ------------------- | -------------------------- | ---------- | ----------- | ---------------------------------------------------------------------------------------------- |
|  101 | 102 | `top-right.jpeg`    | lower-central/eastern edge | medium     | provisional | Solid yellow route is visible between the adjacent markers; confirm the nearby green corridor. |
|  102 | 115 | `top-right.jpeg`    | river-side lower edge      | medium     | provisional | Yellow route approaches 115; endpoint is close to the crop/river boundary.                     |
|  103 | 104 | `top-right.jpeg`    | lower-left of crop         | high       | provisional | Short yellow connection between the visible markers.                                           |
|  105 | 106 | `top-right.jpeg`    | lower-right                | medium     | provisional | Yellow route continues toward 106; inspect the line split near the edge.                       |
|  105 | 107 | `top-right.jpeg`    | lower-right                | medium     | provisional | Yellow corridor visibly branches toward 107.                                                   |
|  106 | 107 | `top-right.jpeg`    | eastern lower edge         | medium     | provisional | Short yellow route between 106 and 107; confirm marker centres.                                |
|  107 | 108 | `top-right.jpeg`    | lower/eastern edge         | medium     | provisional | Yellow route follows the edge corridor toward 108.                                             |
|  109 | 110 | `bottom-left.jpeg`  | upper section of crop      | high       | provisional | Short yellow route visibly joins 109 and 110.                                                  |
|  110 | 111 | `bottom-left.jpeg`  | upper-central              | medium     | provisional | Yellow line continues from 110 toward 111; red line crosses nearby.                            |
|  111 | 112 | `bottom-left.jpeg`  | upper-central              | medium     | provisional | Yellow corridor between 111 and 112 is visible.                                                |
|  112 | 113 | `bottom-left.jpeg`  | central                    | medium     | provisional | Yellow route reaches 113; inspect the adjacent green route.                                    |
|  113 | 114 | `bottom-left.jpeg`  | central                    | high       | provisional | Short yellow connection between 113 and 114.                                                   |
|  114 | 115 | `top-right.jpeg`    | river-side boundary        | low        | provisional | Yellow line appears to approach 115, but water-side geometry needs an annotated crop.          |
|  115 | 116 | `top-right.jpeg`    | river-side                 | medium     | provisional | Yellow route is visible along the 115/116 corridor.                                            |
|  116 | 117 | `bottom-right.jpeg` | upper-right                | medium     | provisional | Yellow line links 116 and 117; endpoint is near image boundary.                                |
|  117 | 118 | `bottom-right.jpeg` | upper-right                | high       | provisional | Short yellow route between 117 and 118.                                                        |
|  118 | 119 | `bottom-right.jpeg` | right edge                 | medium     | provisional | Yellow route continues from 118 toward 119.                                                    |
|  127 | 133 | `bottom-left.jpeg`  | central-right              | medium     | provisional | Yellow corridor is visible between 127 and 133.                                                |
|  128 | 135 | `bottom-right.jpeg` | upper-right/central        | medium     | provisional | Yellow route reaches 135; inspect the nearby green line.                                       |
|  129 | 130 | `bottom-right.jpeg` | central-right              | high       | provisional | Short yellow connection between 129 and 130.                                                   |
|  133 | 140 | `bottom-left.jpeg`  | central                    | medium     | provisional | Yellow route leaves 133 toward 140; bridge/landmark detail is nearby.                          |
|  140 | 154 | `bottom-left.jpeg`  | central-lower              | medium     | provisional | Yellow corridor visibly continues from 140 toward 154.                                         |
|  154 | 155 | `bottom-left.jpeg`  | lower-central              | high       | provisional | Short yellow route between 154 and 155.                                                        |
|  155 | 156 | `bottom-left.jpeg`  | lower-central              | high       | provisional | Yellow route links 155 and 156.                                                                |
|  156 | 157 | `bottom-left.jpeg`  | Thames-side lower          | medium     | provisional | Yellow route approaches 157; bridge/river lines require review.                                |
|  157 | 158 | `bottom-right.jpeg` | upper-left of crop         | medium     | provisional | Yellow route appears to continue east from 157 toward 158.                                     |
|  158 | 159 | `bottom-right.jpeg` | central                    | medium     | provisional | Yellow corridor reaches 159; inspect the crossing at 159.                                      |
|  159 | 160 | `bottom-right.jpeg` | central-right              | medium     | provisional | Yellow route between 159 and 160 is visible.                                                   |
|  160 | 161 | `bottom-right.jpeg` | lower-right                | high       | provisional | Yellow route links 160 and 161.                                                                |
|  161 | 162 | `bottom-right.jpeg` | lower-right                | medium     | provisional | Yellow route appears to continue from 161 to 162.                                              |
|  162 | 174 | `bottom-right.jpeg` | lower-right edge           | medium     | provisional | Yellow route follows the lower-right corridor.                                                 |
|  163 | 164 | `bottom-left.jpeg`  | lower-left                 | high       | provisional | Short yellow connection between 163 and 164.                                                   |
|  164 | 165 | `bottom-left.jpeg`  | lower-left/central         | medium     | provisional | Yellow route continues from 164 toward 165.                                                    |
|  165 | 166 | `bottom-left.jpeg`  | lower-central              | medium     | provisional | Yellow route visible along the 165/166 corridor.                                               |
|  166 | 167 | `bottom-left.jpeg`  | lower-central              | medium     | provisional | Yellow route appears to join 166 and 167.                                                      |
|  167 | 168 | `bottom-left.jpeg`  | lower-central              | medium     | provisional | Yellow corridor continues toward 168.                                                          |
|  168 | 169 | `bottom-left.jpeg`  | lower-central              | medium     | provisional | Yellow route is visible between 168 and 169.                                                   |
|  169 | 170 | `bottom-right.jpeg` | lower-central              | medium     | provisional | Yellow route approaches 170 near the river crossings.                                          |
|  170 | 171 | `bottom-right.jpeg` | lower-central              | medium     | provisional | Yellow corridor continues between 170 and 171.                                                 |
|  171 | 172 | `bottom-right.jpeg` | lower-right                | medium     | provisional | Yellow route appears to connect 171 and 172.                                                   |
|  172 | 173 | `bottom-right.jpeg` | lower-right                | medium     | provisional | Yellow line continues toward 173.                                                              |
|  173 | 175 | `bottom-right.jpeg` | lower-right edge           | medium     | provisional | Yellow route between 173 and 175 is visible.                                                   |
|  187 | 188 | `bottom-right.jpeg` | lower-left of crop         | high       | provisional | Short yellow route between 187 and 188.                                                        |
|  188 | 199 | `bottom-right.jpeg` | lower edge                 | medium     | provisional | Yellow route follows the lower edge toward 199.                                                |
|  199 | 200 | `bottom-right.jpeg` | lower edge                 | high       | provisional | Yellow line visibly reaches the printed 200 marker; edition status remains unresolved.         |

### Bus — solid green

| From |  To | Evidence            | Region                | Confidence | Status      | Visual explanation / follow-up                                                  |
| ---: | --: | ------------------- | --------------------- | ---------- | ----------- | ------------------------------------------------------------------------------- |
|  102 | 115 | `top-right.jpeg`    | river-side lower edge | low        | provisional | Green line appears to share the corridor; separate it from the yellow route.    |
|  105 | 107 | `top-right.jpeg`    | lower-right           | medium     | provisional | Solid green route is visible alongside the yellow corridor.                     |
|  105 | 108 | `top-right.jpeg`    | lower-right edge      | medium     | provisional | Green route continues from 105 toward 108; endpoint is near the crop edge.      |
|  107 | 161 | `bottom-right.jpeg` | eastern/lower edge    | low        | provisional | Long green corridor appears to continue toward 161; requires a full-crop trace. |
|  108 | 116 | `top-right.jpeg`    | river-side            | medium     | provisional | Green route follows the water-side corridor between 108 and 116.                |
|  109 | 124 | `bottom-left.jpeg`  | central-left          | medium     | provisional | Green line leaves 109 toward 124; inspect the park boundary.                    |
|  111 | 124 | `bottom-left.jpeg`  | central               | low        | provisional | Green route appears to connect 111 and 124; line crossing needs annotation.     |
|  116 | 127 | `bottom-right.jpeg` | upper-central         | medium     | provisional | Green route is visible from 116 toward 127.                                     |
|  116 | 142 | `bottom-right.jpeg` | central               | medium     | provisional | Green corridor continues toward 142.                                            |
|  122 | 123 | `bottom-left.jpeg`  | upper-left            | high       | provisional | Short green route between 122 and 123.                                          |
|  123 | 124 | `bottom-left.jpeg`  | upper-central         | high       | provisional | Green route visibly continues from 123 to 124.                                  |
|  123 | 144 | `bottom-left.jpeg`  | left edge             | medium     | provisional | Green route leaves 123 toward 144; confirm the lower-left continuation.         |
|  123 | 165 | `bottom-left.jpeg`  | central/lower-left    | medium     | provisional | Green corridor appears to reach 165.                                            |
|  124 | 153 | `bottom-left.jpeg`  | central               | medium     | provisional | Green route continues from 124 toward 153.                                      |
|  127 | 133 | `bottom-left.jpeg`  | central-right         | medium     | provisional | Green route shares the 127/133 corridor; separate from taxi.                    |
|  128 | 142 | `bottom-right.jpeg` | central               | medium     | provisional | Green route visibly runs between 128 and 142.                                   |
|  128 | 161 | `bottom-right.jpeg` | central-right         | low        | provisional | Green line appears to continue to 161; endpoint needs a tighter crop.           |
|  133 | 140 | `bottom-left.jpeg`  | central               | medium     | provisional | Green route shares the 133/140 corridor.                                        |
|  140 | 156 | `bottom-left.jpeg`  | central-lower         | medium     | provisional | Green route appears to link 140 and 156.                                        |
|  156 | 157 | `bottom-left.jpeg`  | Thames-side           | medium     | provisional | Green line is visible near 156/157; river crossing needs review.                |

### Underground — dashed red

| From |  To | Evidence            | Region             | Confidence | Status      | Visual explanation / follow-up                                                                    |
| ---: | --: | ------------------- | ------------------ | ---------- | ----------- | ------------------------------------------------------------------------------------------------- |
|  104 | 115 | `top-right.jpeg`    | river-side         | low        | provisional | Dashed red route appears to reach 115; endpoint is close to the water/edge.                       |
|  105 | 108 | `top-right.jpeg`    | lower-right        | low        | provisional | Red route is visible in the corridor but may terminate at a crossing; annotate before acceptance. |
|  111 | 153 | `bottom-left.jpeg`  | central/lower-left | medium     | provisional | Dashed red route visibly runs from 111 toward 153.                                                |
|  111 | 163 | `bottom-left.jpeg`  | lower-left         | medium     | provisional | Red route appears to continue to 163.                                                             |
|  128 | 140 | `bottom-right.jpeg` | central            | medium     | provisional | Dashed red route is visible between 128 and 140.                                                  |
|  128 | 185 | `bottom-right.jpeg` | lower-central      | low        | provisional | Long red route appears to continue toward 185; endpoint is distant.                               |
|  140 | 153 | `bottom-left.jpeg`  | central/lower      | medium     | provisional | Dashed red route visibly crosses the 140/153 corridor.                                            |
|  153 | 163 | `bottom-left.jpeg`  | lower-left/central | medium     | provisional | Red route appears to link 153 and 163.                                                            |
|  153 | 185 | `bottom-left.jpeg`  | lower-central      | low        | provisional | Long red route is visible toward 185; requires overlap review.                                    |
|  185 | 187 | `bottom-right.jpeg` | lower-right        | medium     | provisional | Dashed red route appears to connect 185 and 187.                                                  |

## Cross-boundary candidates

These rows connect the existing 1–100 scope to stations above 100. They were previously listed as audit targets and are now recorded as provisional observations without duplicating the original 1–100 rows.

| From |  To | Transport   | Evidence                              | Confidence | Status      | Notes                                                                                          |
| ---: | --: | ----------- | ------------------------------------- | ---------- | ----------- | ---------------------------------------------------------------------------------------------- |
|   46 | 101 | underground | `top-left.jpeg`, `top-right.jpeg`     | low        | provisional | Long dashed route appears to continue toward 101; endpoint and route split require annotation. |
|   67 | 102 | bus         | `top-right.jpeg`                      | low        | provisional | Green corridor appears to leave 67 toward 102; crossing is difficult to distinguish.           |
|   79 | 110 | underground | `top-left.jpeg`, `bottom-left.jpeg`   | low        | provisional | Red route appears to continue across the image boundary; verify both endpoint markers.         |
|   82 | 101 | bus         | `top-right.jpeg`                      | low        | provisional | Green line may reach 101; endpoint is close to a crossing.                                     |
|   89 | 118 | bus         | `top-right.jpeg`, `bottom-right.jpeg` | low        | provisional | Water-side/eastern route is visible but endpoint trace is not yet conclusive.                  |

## Boat candidates — unresolved and separate

| From |  To | Evidence                              | Confidence | Status     | What the photographs establish / gap                                                                                       |
| ---: | --: | ------------------------------------- | ---------- | ---------- | -------------------------------------------------------------------------------------------------------------------------- |
|  108 | 115 | `top-right.jpeg`, `complete.jpeg`     | low        | unresolved | Thames region and both marker areas are visible, but the black/river line cannot be traced continuously between endpoints. |
|  115 | 118 | `top-right.jpeg`, `bottom-right.jpeg` | low        | unresolved | Water-side markers are visible; endpoint route is obscured by bridge/river geometry.                                       |
|  115 | 157 | `complete.jpeg`, `bottom-left.jpeg`   | low        | unresolved | River and bridges are visible, but no clean endpoint trace is recorded.                                                    |
|  157 | 194 | `bottom-left.jpeg`, `complete.jpeg`   | low        | unresolved | Southern Thames region is visible; the boat line needs a dedicated annotated crop.                                         |

Boat rows are not included in taxi/bus/underground totals and do not enter the canonical package.

## Required record format

Each future observation must have one row with this shape:

| Field                | Requirement                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `from` / `to`        | Numeric station markers visible at both ends; canonical ordering `from < to`.                                      |
| `transport`          | Exactly `taxi`, `bus`, `underground`, or `boat`.                                                                   |
| `evidence`           | Photo filename plus crop/region coordinates or a named annotation.                                                 |
| `confidence`         | High, medium, or low, with the reason.                                                                             |
| `verificationStatus` | Existing package vocabulary only: `verified-from-physical-board`, `cross-checked`, or `unresolved` as appropriate. |
| `notes`              | Crossings, occlusion, fold, glare, route continuation, or reviewer disagreement.                                   |

## Image coverage for the future edge pass

| Region                | Primary image       | Overlap                              | Edge-pass limitation                                                                  |
| --------------------- | ------------------- | ------------------------------------ | ------------------------------------------------------------------------------------- |
| northern/central-left | `top-left.jpeg`     | `complete.jpeg`, `top-right.jpeg`    | Rotated crop; route crossings need annotation.                                        |
| northern/eastern      | `top-right.jpeg`    | `complete.jpeg`, `top-left.jpeg`     | Rotated crop; water/bridge area needs separate boat review.                           |
| southern/western      | `bottom-left.jpeg`  | `complete.jpeg`, `bottom-right.jpeg` | Dense route crossings and Thames lines are visible but not yet endpoint-audited.      |
| southern/eastern      | `bottom-right.jpeg` | `complete.jpeg`, `bottom-left.jpeg`  | `200` is clear; connections touching the lower edge require edition resolution first. |
| overall               | `complete.jpeg`     | all close-ups                        | Useful for line continuity, not sufficient alone for small endpoint/type decisions.   |

## Boat-route investigation boundary

The previous discrepancy includes `108–115`, `115–118`, `115–157`, and `157–194`. The new images show the Thames and multiple water-side stations, but this document does not resolve those candidates. A future boat pass must trace the actual black/river line from visible station marker to visible station marker and record the crop. Rulebook evidence and candidate graphs must remain separate evidence classes.

## Acceptance rule for the next pass

An edge may become `verified-from-physical-board` only when both endpoint markers and the intervening transport line are visible in a source crop, with no unresolved crossing or occlusion. A second reviewer must reproduce the reading. Until then, leave the row absent from canonical data or explicitly unresolved in an annotation worksheet.

## Phase 3C.2 graph audit

The 125-row candidate artifact was audited without changing this evidence
boundary. All 66 taxi, 33 bus, and 22 underground rows remain provisional; all
four boat rows remain unresolved. No candidate is a verified or canonical
transport edge. See [BOARD-GRAPH-VERIFICATION.md](BOARD-GRAPH-VERIFICATION.md)
and [BOARD-CANONICAL-GRAPH-DECISION.md](BOARD-CANONICAL-GRAPH-DECISION.md).
