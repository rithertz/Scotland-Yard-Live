# Phase 3E.2B.2 — B-01 Evidence Review

## Scope and status

B-01 was retrieved from `review-batches.json` and covers stations 1–10 and candidates E-001–E-011, E-022–E-024 and E-032. All ten station targets and all fifteen candidate hypotheses were inspected. B-01 is marked `uncertain` because three bus candidates remain ambiguous and several routes are close to image boundaries or crossings.

## Evidence inspected

- `docs/game/evidence/board-photos/original-references/top-left.jpeg`
- `docs/game/evidence/board-photos/original-references/top-right.jpeg`
- `docs/game/data/phase-3e2a-workspace/station-review-contact-sheet.png`
- Registered station crops ST-001 through ST-010, including direct inspection of ST-001, ST-002, ST-005, ST-006 and ST-007.
- Candidate and crop metadata from `candidate-import.json` and `station-crop-manifest.json`.

The B-01 station source crops are rectified-board fallbacks rather than independent high-resolution source crops. Therefore, route coordinates were left `null` rather than fabricated. The original reference photographs supplied the direct visible route evidence.

## Observations created

Twelve observations were added to `new-edge-observations.json`: `OBS-3E2B1-00001` through `OBS-3E2B1-00012`. They cover E-001 through E-011 and E-032. Each records the source photograph, relevant endpoint crop IDs, evidence description, review status and confidence. No source or registered route polyline was measured, so both coordinate fields remain `null`.

## Reconciliation outcome

- Supported by inspected evidence: E-001–E-011 and E-032.
- Ambiguous: E-022, E-023 and E-024.
- Contradicted: none.
- Not sufficiently inspected: none; the ambiguous assessments reflect inspected but inconclusive evidence.
- Newly discovered connections: none.
- Candidate records changed: none.

## Workflow findings and B-02 improvements

The pilot confirms that station-centered crops are useful for endpoint identity and local route context, but boundary and fold-priority crops need explicit overlap navigation. Before B-02:

1. Add a small overlap-view index for every boundary crop and its neighboring station crops.
2. Prefer high-resolution source crops where available; clearly flag rectified fallbacks during review.
3. Add a route-annotation convention for measured polylines so coordinates can be recorded when source geometry supports them.
4. Keep bus-corridor crossings in an explicit ambiguous state until a second view isolates the endpoint and route.
5. Preserve the read-only dashboard model and record progress only in the approved JSON workspace.

The full graph remains unreconstructed, marker 200 remains unresolved, and no candidate was promoted.
