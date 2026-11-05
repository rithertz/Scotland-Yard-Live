# Board graph verification — Phase 3C.2

Status: **Option B — evidence insufficient; do not promote a canonical graph.**

This audit reviews the non-canonical candidate artifact at
[`data/board-edge-candidates-1-200.json`](data/board-edge-candidates-1-200.json)
against the physical-board evidence and the supplied rulebook. Candidate rows
remain evidence records, not playable graph data.

## Audit totals

| Transport   | Candidate rows | Verified | Provisional | Unresolved |
| ----------- | -------------: | -------: | ----------: | ---------: |
| Taxi        |             66 |        0 |          66 |          0 |
| Bus         |             33 |        0 |          33 |          0 |
| Underground |             22 |        0 |          22 |          0 |
| Boat        |              4 |        0 |           0 |          4 |
| **Total**   |        **125** |    **0** |     **121** |      **4** |

The candidate validator passes the artifact with nine warnings for endpoint
pairs observed with more than one transport type. It does not promote those
rows or establish playability.

## Status sets

- Taxi provisional: `E-001–E-021`, `E-042–E-086`.
- Bus provisional: `E-022–E-031`, `E-087–E-106`, `E-118`, `E-120`, `E-121`.
- Underground provisional: `E-032–E-041`, `E-107–E-117`, `E-119`.
- Boat unresolved: `E-122–E-125`.
- Verified rows: none.

## Conflicting transport observations

These endpoint pairs have separate candidate rows for different transport
types. They are retained as provisional observations until endpoint crops and
independent review resolve the visible line markings:

| Endpoints | Candidate IDs    | Observed types   |
| --------- | ---------------- | ---------------- |
| `11–22`   | `E-012`, `E-025` | taxi, bus        |
| `13–14`   | `E-014`, `E-026` | taxi, bus        |
| `14–15`   | `E-015`, `E-027` | taxi, bus        |
| `102–115` | `E-043`, `E-087` | taxi, bus        |
| `105–107` | `E-046`, `E-088` | taxi, bus        |
| `127–133` | `E-059`, `E-101` | taxi, bus        |
| `133–140` | `E-062`, `E-104` | taxi, bus        |
| `156–157` | `E-066`, `E-106` | taxi, bus        |
| `105–108` | `E-089`, `E-108` | bus, underground |

## Boundary and station-200 audit

The five cross-batch rows are all provisional: `E-117` (`46–101`,
underground), `E-118` (`67–102`, bus), `E-119` (`79–110`, underground),
`E-120` (`82–101`, bus), and `E-121` (`89–118`, bus).

Marker `200` is visibly printed in `bottom-right.jpeg`. The candidate set has
only `E-086` (`199–200`, taxi), and that row is provisional. The photographs
establish a physical marker, not that `200` belongs to the playable station
inventory. No station-200 row is promoted.

## Boat-route findings

The supplied rulebook states the boat route `194–157`, `157–115`, and
`115–118` (page 10). The photographs do not provide a sufficiently clear,
independently reviewed endpoint trace to tie those rulebook statements to the
photographed edition. `108–115` is not established by the cited rulebook page.
All four candidate rows remain unresolved: `E-122` (`108–115`), `E-123`
(`115–118`), `E-124` (`115–157`), and `E-125` (`157–194`).

## Decision gate

No candidate meets the project’s promotion gate: both endpoint markers and the
intervening line must be readable in a source crop, with no unresolved crossing
or occlusion, and a second reviewer must reproduce the reading. Missing board
edition linkage, unresolved station inventory, multimodal conflicts, absent
canonical coordinates, and incomplete starting-position evidence prevent a
canonical graph decision.

The next evidence pass should add straight-on, high-resolution endpoint and
Thames crops, a legible product/copyright panel, independent review notes, and
coordinate control points. Until then, this document is an audit of candidate
evidence only.
