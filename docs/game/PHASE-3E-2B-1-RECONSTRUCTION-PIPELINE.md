# Phase 3E.2B.1 — Transport Graph Reconstruction Pipeline

## Status and scope

This phase establishes the evidence workflow only. It does not transcribe the complete graph, promote any edge, change station data, or modify canonical game data.

The pipeline creates a separate workspace at `docs/game/data/phase-3e2b1-reconstruction/`:

- `candidate-import.json` — record-preserving import of all 125 `E-001`–`E-125` candidate records, with the source hash. The imported candidate objects are semantically equal to the source records; the enclosing JSON file is newly serialized for this workspace.
- `new-edge-observations.json` — intentionally empty ledger for human-discovered connections.
- `phase-3e2b1-observation.schema.json` — extensible observation model for route evidence, coordinates, review state, confidence, conflicts and duplicates.
- `review-batches.json` — 20 deterministic ten-station batches covering stations 1–199 exactly once.
- `review-dashboard.html` — dependency-free local review index linking each station to its primary crop and incident candidates.
- `reconstruction-summary.json` — deterministic counts, coverage and protected-input hashes.
- `phase-3e2b1-workspace.json` — architecture and evidence policy.

## Candidate reconciliation

The source candidate objects are imported without field edits. Candidate IDs, endpoints, transport, confidence, verification status, evidence, explanations and unresolved notes remain intact. The nine multi-transport endpoint pairs and four unresolved candidates are retained. These records are candidate hypotheses, not human-reviewed observations, and are never automatically promoted.

## Observation model

Each new observation receives a stable `OBS-3E2B1-NNNNN` ID. A reviewer records both endpoints, transport, source photograph, source crop IDs, route coordinates in source and registered spaces when available, evidence description, reviewer/status, confidence, uncertainty, supporting/conflicting observations, related candidate IDs and duplicate relationships. Missing coordinates are represented as `null`; they are not fabricated.

## Batch review

There are 20 batches of at most ten stations. Each batch lists its stations, all incident existing candidate IDs and boundary/fold priority stations. Coverage means every station has a review target; it does not mean the transport graph is complete. A station is complete only after its incident routes have been reviewed. The batch lifecycle is `not-started`, `in-progress`, `reviewed`, `uncertain`, `conflicting` or `blocked`; candidate presence or crop inspection alone does not mark completion.

Routes crossing crop boundaries should be recorded once with both endpoint stations and linked to every crop needed to show the route. Duplicate observations are retained and linked rather than deleted. Multiple transport types for one endpoint pair remain separate.

## Human workflow

Open `review-dashboard.html` locally, filter to a station or candidate, inspect the linked station crop and registered context, then trace the complete route through overlapping context. The dashboard is read-only: its status text is non-persistent. Record evidence and approved progress in the designated JSON workspace only in a later approved task. Add an observation only when both endpoint identity and intervening route are supported. Do not edit protected Phase 3E.2A queue or observation files.

## Validation

```powershell
tools/board-calibration/.venv/Scripts/python.exe tools/phase_3e2b1_pipeline.py
tools/board-calibration/.venv/Scripts/python.exe tools/phase_3e2b1_validate.py
tools/board-calibration/.venv/Scripts/python.exe -m unittest tools.board-calibration.tests.test_phase_3e2b1_pipeline
tools/board-calibration/.venv/Scripts/python.exe -m unittest discover -s tools/board-calibration/tests -p "test_*.py"
node docs/game/data/validate-board-edge-candidates.mjs
corepack pnpm --filter @scotland-yard-live/board-data test
corepack pnpm --filter @scotland-yard-live/board-data typecheck
```

## Results and limitations

- Candidates imported: 125.
- New observations: 0, as required for a pipeline-only phase.
- Review batches: 20.
- Station coverage: all 199 playable stations; marker 200 remains separate.
- Existing candidate observations remain hypotheses; no canonical graph is produced.
- The dashboard is an index rather than a general-purpose editor and does not write evidence automatically.
- The protected source contains `E-086` (`199–200`). It is preserved unchanged as the sole explicit marker-200 exception; marker 200 remains unresolved and is not included in the 199-station batch coverage. The literal invariant that every imported candidate endpoint is 1–199 is therefore impossible without violating the protected-data and marker-200 constraints.
- The approved consolidated project plan named in the task was not present in this checkout; the available Phase 3E.1 and Phase 3E.2A artifacts were used as the repository-local authority.

## Next phase

Phase 3E.2B.2 may begin human route review and add evidence-backed observations through this separate workspace. It must preserve the protected inputs and must not promote observations to canonical graph data without a later evidence gate.
