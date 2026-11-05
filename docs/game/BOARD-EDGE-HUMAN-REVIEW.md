# Board edge human-review queue

This queue is generated from the Phase 3B.5 candidate dataset in [board-edge-candidates-1-200.json](data/board-edge-candidates-1-200.json). The dataset is an evidence artifact only: it is non-canonical, non-playable, and does not authorize changes to `packages/board-data/src`.

Every item below points to an edge ID and at least one source photograph. Reviewers should inspect the listed crop or region, record the result in a future evidence worksheet, and leave the candidate provisional or unresolved until a second reviewer reproduces the reading.

## Targeted audit findings

The five photographs show several solid yellow/green corridors running together and several dashed red routes crossing them. They support the possibility of genuine multi-modal connections, but the available perspective and resolution do not independently establish every endpoint. The nine transport conflicts therefore remain represented as separate provisional records and are warnings, not automatic errors.

| Endpoint pair | Candidate IDs and transports     | Photograph evidence                           | Current finding                                                                                                                               |
| ------------- | -------------------------------- | --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `11–22`       | `E-012` taxi; `E-025` bus        | `top-left.jpeg`, central corridor             | Yellow and green line markings appear in the same corridor; multi-modal service is plausible, but endpoint continuity needs a crop.           |
| `13–14`       | `E-014` taxi; `E-026` bus        | `top-right.jpeg`, upper-central corridor      | Both colour conventions are visible near the corridor; classification is not disproved, but the crossing needs independent tracing.           |
| `14–15`       | `E-015` taxi; `E-027` bus        | `top-right.jpeg`, upper-right corridor        | Parallel/overlapping yellow and green markings are visually plausible; retain both provisionally.                                             |
| `102–115`     | `E-043` taxi; `E-087` bus        | `top-right.jpeg`, river-side lower edge       | Yellow and green corridors are visible near the water-side route; the endpoint at 115 is not sufficiently isolated.                           |
| `105–107`     | `E-046` taxi; `E-088` bus        | `top-right.jpeg`, lower-right corridor        | Adjacent yellow/green markings are visible; inspect whether both reach the same printed markers.                                              |
| `127–133`     | `E-059` taxi; `E-101` bus        | `bottom-left.jpeg`, central-right bridge area | Shared corridor is visible; bridge and crossing geometry prevent a verified classification.                                                   |
| `133–140`     | `E-062` taxi; `E-104` bus        | `bottom-left.jpeg`, central Thames-side area  | Yellow/green route markings coexist in the region; endpoint tracing remains unresolved.                                                       |
| `156–157`     | `E-066` taxi; `E-106` bus        | `bottom-left.jpeg`, Thames-side lower area    | The route corridor and river crossing are visible, but both service lines need separate endpoint traces.                                      |
| `105–108`     | `E-089` bus; `E-108` underground | `top-right.jpeg`, lower-right corridor        | Green and dashed-red markings appear in the same broad corridor; this may be multi-modal, but the red route is low-confidence and unresolved. |

No conflict is promoted to verified status by this visual pass.

## Batch 1 — low-confidence and boundary observations

Inspect these in one pass because they are most exposed to crop boundaries, distant endpoints, or dense crossings:

| Edge IDs                                    | Priority | Evidence focus                                                                                                  |
| ------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------- |
| `E-029`, `E-035`, `E-039`, `E-041`, `E-054` | High     | `top-left.jpeg` / `top-right.jpeg`; long or distant red routes around the central crossings.                    |
| `E-087`, `E-090`, `E-093`                   | High     | `top-right.jpeg`; water-side and lower-right bus/underground endpoints.                                         |
| `E-103`, `E-107`, `E-108`                   | High     | `bottom-left.jpeg` / `bottom-right.jpeg`; long red or river-adjacent traces.                                    |
| `E-112`, `E-115`, `E-117`                   | High     | `bottom-left.jpeg` / `top-right.jpeg`; Thames-side and endpoint-continuation questions.                         |
| `E-118`, `E-119`, `E-120`, `E-121`          | Critical | `top-left.jpeg`, `top-right.jpeg`, `bottom-left.jpeg`, `bottom-right.jpeg`; all five cross-boundary candidates. |
| `E-122`, `E-123`, `E-124`, `E-125`          | Critical | `complete.jpeg` plus the relevant Thames close-up; unresolved boat candidates.                                  |

### Detailed low-confidence records

All low-confidence records are retained as provisional or unresolved. The listed resolution criterion is the observation a reviewer must be able to reproduce before changing the status.

| Edge ID | Endpoints | Transport   | Evidence / region                                     | Current state     | Resolution criterion                                                            |
| ------- | --------- | ----------- | ----------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------- |
| `E-029` | `15–41`   | bus         | `top-right.jpeg`, eastern-central                     | low / provisional | Trace the green line from both markers without terminating at a crossing.       |
| `E-035` | `13–89`   | underground | `top-right.jpeg`, central/right                       | low / provisional | Confirm the distant 89 endpoint and uninterrupted dashed-red route.             |
| `E-039` | `67–89`   | underground | `top-right.jpeg`, central/right                       | low / provisional | Confirm both endpoints rather than the long red corridor alone.                 |
| `E-041` | `79–100`  | underground | `top-left.jpeg`, lower-central                        | low / provisional | Confirm that the red line reaches 100 rather than ending at the crop boundary.  |
| `E-054` | `114–115` | taxi        | `top-right.jpeg`, river-side boundary                 | low / provisional | Isolate the yellow endpoint at 115 from nearby water-side lines.                |
| `E-087` | `102–115` | bus         | `top-right.jpeg`, river-side lower edge               | low / provisional | Separate green from the yellow corridor and confirm both markers.               |
| `E-090` | `107–161` | bus         | `bottom-right.jpeg`, eastern/lower edge               | low / provisional | Trace the long green corridor to 161 in a full crop.                            |
| `E-093` | `111–124` | bus         | `bottom-left.jpeg`, central                           | low / provisional | Resolve the crossing and confirm the green endpoint at 124.                     |
| `E-103` | `128–161` | bus         | `bottom-right.jpeg`, central-right                    | low / provisional | Confirm that the green line reaches 161, not a nearby route.                    |
| `E-107` | `104–115` | underground | `top-right.jpeg`, river-side                          | low / provisional | Trace the dashed-red line to 115 without water/bridge ambiguity.                |
| `E-108` | `105–108` | underground | `top-right.jpeg`, lower-right                         | low / provisional | Confirm that the dashed-red route reaches both markers.                         |
| `E-112` | `128–185` | underground | `bottom-right.jpeg`, lower-central                    | low / provisional | Confirm the distant 185 endpoint and route continuity.                          |
| `E-115` | `153–185` | underground | `bottom-left.jpeg`, lower-central                     | low / provisional | Use overlap with another crop to confirm the long red route.                    |
| `E-117` | `46–101`  | underground | `top-left.jpeg`, `top-right.jpeg`, cross-boundary     | low / provisional | Match the route across the photographic boundary and confirm station 101.       |
| `E-118` | `67–102`  | bus         | `top-right.jpeg`, cross-boundary                      | low / provisional | Confirm the green line and both endpoints at the boundary region.               |
| `E-119` | `79–110`  | underground | `top-left.jpeg`, `bottom-left.jpeg`, cross-boundary   | low / provisional | Confirm the red route continues across the image boundary.                      |
| `E-120` | `82–101`  | bus         | `top-right.jpeg`, cross-boundary                      | low / provisional | Confirm the green endpoint at 101 rather than a nearby crossing.                |
| `E-121` | `89–118`  | bus         | `top-right.jpeg`, `bottom-right.jpeg`, cross-boundary | low / provisional | Confirm the water-side/eastern route reaches 118.                               |
| `E-122` | `108–115` | boat        | `top-right.jpeg`, `complete.jpeg`, Thames route       | low / unresolved  | Trace a continuous black/river line to both markers.                            |
| `E-123` | `115–118` | boat        | `top-right.jpeg`, `bottom-right.jpeg`, Thames route   | low / unresolved  | Resolve bridge occlusion and confirm the boat endpoints.                        |
| `E-124` | `115–157` | boat        | `complete.jpeg`, `bottom-left.jpeg`, Thames route     | low / unresolved  | Establish a direct physical line, not a rulebook or candidate-source inference. |
| `E-125` | `157–194` | boat        | `bottom-left.jpeg`, `complete.jpeg`, Thames route     | low / unresolved  | Trace the southern Thames route to both markers.                                |

## Batch 2 — shared taxi/bus corridors

These endpoint pairs have both taxi and bus observations. This is a conflict to inspect, not permission to delete one classification:

| Endpoint pair | Edge IDs         | Evidence           |
| ------------- | ---------------- | ------------------ |
| `11–22`       | `E-012`, `E-025` | `top-left.jpeg`    |
| `13–14`       | `E-014`, `E-026` | `top-right.jpeg`   |
| `14–15`       | `E-015`, `E-027` | `top-right.jpeg`   |
| `102–115`     | `E-043`, `E-087` | `top-right.jpeg`   |
| `105–107`     | `E-046`, `E-088` | `top-right.jpeg`   |
| `127–133`     | `E-059`, `E-101` | `bottom-left.jpeg` |
| `133–140`     | `E-062`, `E-104` | `bottom-left.jpeg` |
| `156–157`     | `E-066`, `E-106` | `bottom-left.jpeg` |

## Batch 3 — mixed transport classification

| Endpoint pair | Edge IDs         | Evidence         | Review question                                                        |
| ------------- | ---------------- | ---------------- | ---------------------------------------------------------------------- |
| `105–108`     | `E-089`, `E-108` | `top-right.jpeg` | Separate the green corridor from the dashed red route at the crossing. |

## Batch 4 — station 200 and edition boundary

| Edge ID                   | Evidence            | Review question                                                                                                                                                                                     |
| ------------------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `E-086` (`199–200`, taxi) | `bottom-right.jpeg` | Confirm that the yellow line reaches the printed `200` marker, then resolve the target-edition/product-panel discrepancy. Do not add station 200 to canonical data based on this observation alone. |

## Batch 5 — boat-route discrepancy

| Edge ID | Candidate | Evidence                              | Review question                                                                              |
| ------- | --------- | ------------------------------------- | -------------------------------------------------------------------------------------------- |
| `E-122` | `108–115` | `top-right.jpeg`, `complete.jpeg`     | Can the black/river route be traced continuously to both markers?                            |
| `E-123` | `115–118` | `top-right.jpeg`, `bottom-right.jpeg` | Is the endpoint obscured by bridge geometry?                                                 |
| `E-124` | `115–157` | `complete.jpeg`, `bottom-left.jpeg`   | Does the visible river line connect these markers, or is this only a candidate-source claim? |
| `E-125` | `157–194` | `bottom-left.jpeg`, `complete.jpeg`   | Can the southern Thames line be traced without inference?                                    |

## Review protocol

1. Open every listed photograph and record the crop or approximate pixel region used.
2. Confirm both endpoint markers and the uninterrupted transport line.
3. Record an independent reviewer result without overwriting the original observation.
4. Keep unresolved or conflicting rows in the candidate dataset; never promote them automatically.
5. Only a later, separately approved canonical-data task may change the board-data package.
