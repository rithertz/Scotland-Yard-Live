# Phase 3D.4 station transcription report

## Completeness

All 199 playable station IDs are represented exactly once in `station_transcription_phase_3d4.json`.

| Status | Count |
|---|---:|
| Verified | 2 |
| Candidate-uncertain | 4 |
| Unresolved feature mappings | 193 |
| Conflicting | 0 |
| Duplicate | 0 |

## Number-reading versus feature-mapping completeness

| Number-reading state | Count |
|---|---:|
| Printed numbers directly read and evidenced | 2 |
| Candidate records inherited from prior evidence, not direct high-resolution transcription | 4 |
| Read but unmapped | 0 |
| Unreadable or not transcribed into this structured artifact | 193 |

Supported existing mappings are preserved for stations 1, 3, 120, 123, 158 and 199. The unresolved list contains 193 station IDs: `2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 121, 122, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198`.

The 16 high-resolution tiles and their 259 registered marker observations are recorded in the tile audit. Marker 200 remains separate and is excluded from the playable station array.

## Overlay explanation

The overlay is generated from `feature_id != null` records in this JSON. Its six labels are not OCR output and are not position/order-derived annotations: they are the two pre-existing verified records and four pre-existing candidate-uncertain records copied from Phase 3D.3. The gray rings are physical-marker candidates with no station identity. No high-resolution tile is currently linked to one of the six identity records, so every tile audit entry correctly reports zero identity assignments.

This pass does not alter coordinates, raw observations, feature IDs, calibration, detection or transport-edge data. A physical marker observation is not promoted to a station identity unless the printed number and existing feature correspondence are recorded together.
