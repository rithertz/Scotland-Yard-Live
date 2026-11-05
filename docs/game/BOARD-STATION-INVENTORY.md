# Physical station-number inventory

## Scope and status semantics

This is a visual inventory of printed station-number markers in the Phase 3B.2 photographs. `verified` means the number is legible as a printed marker in at least one supplied photograph. It does **not** mean that the station belongs to the locked target edition, has verified coordinates, or has verified transport connections. No row in this document is canonical board-data input.

## Inventory result

The overlapping photographs support the complete observed numeric sequence **1 through 200**. No missing or duplicated number was identified in the supplied five-photo set at the level of visible marker numbering. The result is therefore:

| Status                 | Count | Meaning                                                                                                        |
| ---------------------- | ----: | -------------------------------------------------------------------------------------------------------------- |
| verified visual marker |   200 | Printed markers `1–200` are legible in the new photo set, using complete-board context and regional close-ups. |
| provisional            |     0 | No marker was retained only from an ambiguous partial reading.                                                 |
| unresolved             |     0 | No station-number slot was left unresolved in this visual inventory; this does not resolve edition identity.   |

## Traceable coverage table

The range notation below enumerates every observed marker without pretending that the ranges are canonical dataset declarations.

| Observed station IDs | Primary evidence    | Overlap/cross-check                  | Status   | Notes                                                                                                |
| -------------------- | ------------------- | ------------------------------------ | -------- | ---------------------------------------------------------------------------------------------------- |
| `1–114`              | `top-left.jpeg`     | `complete.jpeg`, `top-right.jpeg`    | verified | Northern and central-left coverage; several markers are near crop boundaries but visible in overlap. |
| `4–107`              | `top-right.jpeg`    | `complete.jpeg`, `top-left.jpeg`     | verified | Northern/eastern and central-right coverage.                                                         |
| `113–197`            | `bottom-left.jpeg`  | `complete.jpeg`, `bottom-right.jpeg` | verified | Southern/western coverage including Thames-side region.                                              |
| `113–200`            | `bottom-right.jpeg` | `complete.jpeg`, `bottom-left.jpeg`  | verified | Southern/eastern coverage; `200` is clearly visible near the lower-right board edge.                 |
| `1–200`              | `complete.jpeg`     | all four close-ups                   | verified | Overall sequence and board placement context; lower resolution than the close-ups.                   |

## Station 200 investigation

Station `200` is confirmed as a printed board marker in `bottom-right.jpeg` and is also contextualized by `complete.jpeg`. This is stronger evidence than the earlier close-up alone. It still does not prove that the photographed board is the locked 1985 Milton Bradley / Funskool 4500-X2 edition, nor does it authorize changing the project’s 1–199 target or the `@scotland-yard-live/board-data` validator.

The correct data status is: **physical marker observed; edition inventory unresolved**.

## What this inventory does not establish

- station coordinates;
- station transport services beyond what a future edge pass records independently;
- any adjacency or route endpoint;
- the complete starting-position set;
- whether the physical board is exactly product 4500-X2;
- whether `200` replaces, supplements, or contradicts the project’s expected 1–199 inventory.

## Next review action

Create annotated crops for every station marker and have a second reviewer verify the `1–200` sequence against the physical board and copyright/product panel. Keep the package canonical dataset unavailable until the edition discrepancy is resolved by direct evidence.
