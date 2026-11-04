# Board transcription workflow

## Purpose

This workflow turns physical-board evidence into reviewable worksheets before anything can become canonical data. It is designed for the locked 1985 Milton Bradley / Funskool India target and uses the existing board-data verification states:

`verified-from-physical-board`, `verified-from-rulebook`, `cross-checked`, `candidate-unverified`, and `unresolved`.

No candidate repository, visual guess, interpolated line, or majority vote may silently become canonical.

## Station transcription procedure

1. Confirm the source image is identified, preserved, and calibrated under [BOARD-COORDINATE-RECONSTRUCTION.md](BOARD-COORDINATE-RECONSTRUCTION.md).
2. Work in numeric order, but record unexpected IDs rather than correcting them by assumption.
3. For each visible marker, record station ID, source image/region, pixel centre, normalized centre, confidence, visible transport indicators, reviewer, and notes.
4. If an ID is unreadable, record an unresolved candidate tied to the crop. Do not infer from a nearby candidate dataset.
5. If a marker appears outside the expected 1–199 range, record the observation in the discrepancy ledger. Do not add it to canonical data.
6. Perform a second independent pass from a different image or reviewer.
7. Promote a coordinate only when the physical evidence supports it and the status is explicitly recorded.

Station records describe stops and their visible services. They do not contain the full transport adjacency list.

## Transport-edge transcription procedure

Record each undirected edge once with deterministic endpoint ordering (`from < to`):

```text
fromStation, toStation, transport, sourceImage, region,
verificationStatus, confidence, reviewer, notes
```

Use only `taxi`, `bus`, `underground`, or `boat`. A coloured line must reach both numbered markers in the source evidence before it becomes a candidate edge. Lines crossing, disappearing under glare, or ending in a non-station graphic remain unresolved.

Keep transport types separate. A station’s visible taxi/bus/underground indicators do not prove that every adjacent route supports every indicated transport.

Boat edges require a clear route trace and endpoint confirmation. The rulebook may verify a rule statement, but it does not automatically prove the photographed edition’s exact printed topology.

## Evidence recording

Every claim needs:

- evidence source ID;
- image filename or rulebook page;
- crop/region or page location;
- claim;
- confidence;
- verification status;
- reviewer and date;
- outstanding question or discrepancy link.

For candidate repositories, record repository, branch, exact file path, immutable revision where available, licence status, edition assessment, and whether the information is being used only for comparison. Candidate data must remain `candidate-unverified`.

## Verification process

Use this sequence:

1. Primary visual pass against the physical board.
2. Rulebook cross-check for rule statements and transport semantics.
3. Independent second visual pass.
4. Candidate-source comparison only as a discrepancy detector.
5. Validator run against the assembled worksheet.
6. Review of all unresolved records and edge conflicts.
7. Explicit approval before promotion to canonical-complete.

The validator’s completeness gate requires exactly 199 stations, IDs 1–199, valid coordinates, valid endpoints, no duplicate undirected transport edges, and verified statuses. The gate must fail rather than accepting a partially verified dataset as canonical.

## Conflict resolution

When sources disagree:

1. Preserve every candidate value and its evidence.
2. Prefer direct target-edition physical evidence over community data.
3. Use the original rulebook for rule wording, not as a substitute for a complete board trace.
4. Never resolve a conflict by frequency of agreement alone.
5. Mark the subject `unresolved` until the missing evidence is acquired.
6. Document the decision and required next action in the discrepancy ledger.

The currently documented conflicts include the apparent physical `200`, candidate river/boat route differences, and candidate graphs containing non-station river waypoints.

## Review and approval

A reviewer should be able to open the source crop and reproduce the station centre or edge endpoint. Approval should record:

- source and revision;
- reviewer identity;
- date;
- count of stations and edges reviewed;
- unresolved exceptions;
- validator output;
- whether canonical promotion is authorized.

No web renderer should consume worksheet data merely because it looks visually plausible.

## Dataset validation

Use the package checks:

```powershell
corepack pnpm --filter @scotland-yard-live/board-data test
corepack pnpm --filter @scotland-yard-live/board-data typecheck
```

Then run the repository quality gates. The final dataset must use `metadata.state: 'canonical-complete'` and pass `validateBoardDataset` with no issues. Starting positions remain a separate dataset and must not be mixed into transport topology.

## Avoiding silent guesses

- Do not interpolate a coordinate because a station is missing from a photo.
- Do not add an edge because two community sources agree.
- Do not infer a route type from a station icon alone.
- Do not treat a duplicate photograph as independent confirmation.
- Do not turn an unreadable card into a starting-position value.
- Do not change the target station range to accommodate a candidate source.
- Do not remove an inconvenient discrepancy from the ledger.

When evidence is insufficient, the correct output is an unresolved record and a request for a better photograph or scan.
