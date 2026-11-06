# Final Phase 3D — best-effort station reconstruction

This is a complete usable approximation, not a claim of perfect photographic transcription.

| Metric | Count |
|---|---:|
| Playable stations | 199/199 |
| Stations with coordinates | 199/199 |
| Verified retained associations | 2 |
| Approximate feature associations | 40 |
| Unmatched feature identities | 157 |

Coordinates use the established 1350×1000 top-left-origin board canvas and are normalized to [0,1]. Six prior associations were retained. Remaining stations use distinct positions from the Phase 3D.3 registered physical-marker pool, with explicit approximate/unmatched provenance. No FEAT identifiers were fabricated. Marker 200 is not present in the playable station array. The transport graph remains unchanged and non-canonical.

Expected limitations are marker-to-number assignment errors, local fold/perspective displacement and provisional feature matching. The renderer should treat `coordinateStatus: candidate-unverified` as approximate evidence.
