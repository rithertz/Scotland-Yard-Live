# Canonical graph decision — Phase 3C.2

Decision: **do not introduce or promote a canonical transport graph.**

Phase 3C.2 selects Option B from the verification brief: the current physical
evidence is insufficient for a verified graph. The 125-row artifact remains a
non-canonical candidate set documented in
[`BOARD-GRAPH-VERIFICATION.md`](BOARD-GRAPH-VERIFICATION.md).

## Reasons

- The audit contains 0 verified, 121 provisional, and 4 unresolved candidate
  rows.
- The photographed board’s exact edition/product identity is probable but not
  directly tied to the supplied rulebook by a readable board panel.
- Marker `200` is physically visible, while the playable 199-versus-200
  inventory remains unresolved.
- Four boat candidates remain unresolved; the rulebook supports three route
  statements, but the photo-to-rulebook edition match and endpoint traces are
  not independently established.
- Nine endpoint pairs have conflicting transport observations.
- Canonical station coordinates and a complete verified starting-position set
  are not available.

## Scope protection

No files under `packages/board-data/src` were changed. No canonical graph,
playable station inventory, coordinate dataset, game rule, frontend behavior,
or server behavior was added or modified.

## Promotion gates for a future decision

1. Tie the physical board to an authoritative edition/product identity.
2. Resolve the station inventory, including the role of marker `200`.
3. Produce endpoint crops and independent review for every candidate row.
4. Resolve all multimodal and boat-route discrepancies.
5. Establish board-plane coordinates and verify the complete station set.
6. Re-run candidate validation and graph invariants before any canonical data
   change.

Until all gates pass, future contributors must preserve the candidate artifact
and discrepancy ledger rather than treating it as playable data.
