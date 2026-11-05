# Canonical playable station inventory decision

## Decision

The canonical playable station inventory remains **deferred**. The project plan and current board-data contract retain the target range `1–199`, but the photographs provide high-confidence evidence that the physical board visibly prints a marker `200`. The available primary evidence does not establish whether `200` is a playable station in the target edition.

No station 200 record, coordinate, edge, or canonical graph entry has been added.

## 199 versus 200 assessment

| Question                                             | Current finding                                                                                                       | Evidence                                                         | Confidence                                      | Blocks canonical board data?                                                 |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------- |
| Why does the project specify 199?                    | `1–199` is an approved project decision and the current canonical package validator assumes that playable range.      | Consolidated project plan; `packages/board-data/src/validate.ts` | High as a project constraint                    | Yes, until physical evidence is reconciled with the target decision.         |
| Is marker 200 physically printed?                    | Yes. It is clearly visible in the lower-right board photograph and contextualized by the complete board view.         | `bottom-right.jpeg`, `complete.jpeg`; station inventory          | High                                            | Yes, because marker presence conflicts with the current target assumption.   |
| Does 200 look like a normal numbered marker?         | It uses the same general yellow numbered-marker treatment and is adjacent to visible route artwork.                   | `bottom-right.jpeg`                                              | Medium                                          | Yes. Appearance alone does not prove playability.                            |
| Is `199–200` visually connected?                     | A yellow route appears to reach the printed `200` marker and is retained as candidate edge `E-086`.                   | `bottom-right.jpeg`; candidate JSON                              | Medium                                          | Yes. The line is not sufficient to establish target-edition gameplay status. |
| Does the rulebook identify 200 as playable?          | No explicit 199/200 station-count statement or station-200 rule reference was found in the supplied 12-page rulebook. | Rulebook pages 1–12                                              | High for absence in reviewed pages              | Yes.                                                                         |
| Does the board photo prove the exact target edition? | No. The board design is consistent, but the board product/copyright panel is not legible.                             | Five board photographs                                           | Medium for probable match; unresolved for proof | Yes.                                                                         |

## Current inventory boundary

The following statements are kept separate:

- **Printed-marker inventory:** visual evidence records markers through `200`.
- **Candidate evidence inventory:** candidate edges may mention `200` without making it canonical.
- **Canonical playable inventory:** remains the approved `1–199` target but is not yet evidence-closed.

This means the repository must not treat the visual inventory of 200 markers as a 200-node playable graph. Conversely, it must not erase the physical observation of marker 200 merely to satisfy the current package range.

## Consequences

- The canonical board-data package remains unchanged.
- The existing validator's canonical `1–199` assumption remains unchanged pending an explicit edition decision.
- Candidate evidence may continue to represent `200` as a non-canonical observed endpoint.
- Coordinates must not be generated for station 200 or any other station from the current photographs.
- The frontend must continue using its synthetic fixture and must not infer playable station count from the evidence documents.

## Evidence required to close the decision

1. A straight-on, high-resolution photograph of the board copyright/product panel tied to the physical board.
2. A glare-free close-up of marker `200`, its route signals, and every incident route endpoint.
3. A readable complete-board capture showing whether the numbering and route layout treat `200` as a normal station, a printing/reference marker, or an edition-specific addition.
4. If the target edition is confirmed to differ from the project assumption, an explicit owner decision must revise the canonical range before any package validator or graph changes are made.

Until those gates pass, the correct decision is **defer 199-versus-200 canonical inventory resolution**.
