# Station recovery report — Phase 3D.3

## Exact results

| Metric | Result |
|---|---:|
| Playable station IDs accounted for | 199/199 |
| Verified identities | 2 |
| Candidate-uncertain identities | 4 |
| Unresolved identities | 193 |
| Conflicting identities | 0 |
| Duplicate identities | 0 |
| High-resolution photographs inventoried | 16/16 |
| High-resolution photographs successfully registered | 16/16 |
| Raw high-resolution marker observations | 259 |
| Deduplicated provisional physical candidates | 202 |
| Marker 200 | separate, excluded |

## Registration

Each tile was matched directly to the established rectified board reference using SIFT descriptors, Lowe-ratio filtering, RANSAC homography estimation and projected-quadrilateral validation. No source JPEG was modified. The full-board composite is diagnostic; individual registered tiles and original JPEGs remain the evidence sources.

## Identity result

No station was newly promoted automatically. The high-resolution photographs materially improve physical-marker coverage, but a marker detection is not a station identity. Existing assignments remain unchanged: verified stations 1 and 199; candidate-uncertain stations 3, 120, 123 and 158. The remaining 193 identities are explicit unresolved entries with null station-to-feature assignment rather than unsupported OCR or landmark inference.

## Owner review

Inspect `phase_3d3_4x4_tile_contact_sheet.png`, the registered tile directory, overlap diagnostics, and `full_board_station_overlay_phase_3d3.png`. Human review can promote identities only after a printed number and stable feature correspondence are documented in the evidence mapping.
