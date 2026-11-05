# Physical transport-edge transcription

## Status

This document is the evidence boundary for transport connections. The Phase 3B.2 photographs make route colours locally visible, but no complete edge list has yet passed an endpoint-and-type review. Therefore **zero edges are promoted to verified or provisional transcription records in this milestone**. This is deliberate: a visually plausible line is not enough to establish a canonical connection.

The canonical graph and `packages/board-data/src` are unchanged.

## Transport evidence convention

The physical board distinguishes:

- solid yellow: taxi;
- solid green: bus;
- dashed red: underground.

Boat evidence is handled separately because the Thames route and endpoint discrepancy remain unresolved. A station’s visible service icon is not an edge.

## Current edge counts

| Transport   | Verified | Provisional | Unresolved candidate rows | Canonical added |
| ----------- | -------: | ----------: | ------------------------: | --------------: |
| taxi        |        0 |           0 |                         0 |               0 |
| bus         |        0 |           0 |                         0 |               0 |
| underground |        0 |           0 |                         0 |               0 |
| boat        |        0 |           0 |                         0 |               0 |

No row is entered merely because two visible station markers are geographically close. The next pass must use annotated crops and record each endpoint and transport colour explicitly.

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
