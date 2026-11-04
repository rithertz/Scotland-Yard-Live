# Physical board evidence register

## Status

This is the Phase 3B.1 evidence audit for the locked target: the 1985 Milton Bradley Scotland Yard board manufactured under licence by Funskool (India) Ltd., product code 4500-X2. The physical board is the primary visual authority. This register does not create canonical stations, edges, coordinates, or starting positions.

The repository remains on `feat/board-evidence-audit` with a clean working tree at the start of this audit. The canonical dataset remains unavailable in `@scotland-yard-live/board-data`, and the existing synthetic web board remains active.

## Target-edition identification

The project decision identifies the target as the 1985 Milton Bradley / Funskool India edition, product code 4500-X2. The supplied board photographs are consistent with a Central London Scotland Yard board and visibly show the blue Scotland Yard / A Milton Bradley Game border. They do not show a sufficiently legible copyright panel in the accessible images to independently re-read every identification field.

The close-up image visibly includes station `200`. This is an observed physical-board fact, not a resolution of the project’s locked 1–199 target. It may indicate an edition difference, a modified/reference board, or a reading/identification issue. It remains unresolved.

## Image inventory

Dimensions were read from the image files, not inferred from the rendered chat previews. Aspect ratio is width / height.

| ID     | File                                                                        | Dimensions | Aspect | Classification | Board content and usable evidence                                                                                                                                                                                            |
| ------ | --------------------------------------------------------------------------- | ---------: | -----: | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IMG-01 | `scotland-yard-docs/init-context-docs-planning/soctland-yard board pic.jpg` |  1080×1920 | 0.5625 | C              | Complete board overview. Rotated/portrait capture, perspective distortion, modest resolution, visible fold, and limited station/line legibility. Useful for overall composition and region orientation only.                 |
| IMG-02 | `scotland-yard-docs/photoscans/bottom right.jpeg`                           |  2160×3840 | 0.5625 | B              | Partial lower/right board detail. Oblique close-up with board edge visible. Station labels, route colours, border text, and the apparent `200` are readable. Not complete-board evidence.                                    |
| IMG-03 | `scotland-yard-docs/photoscans/starting cards.jpeg`                         |   899×1599 | 0.5622 | C              | Starting-card spread. Several card values are readable, but cards are cropped/rotated and the full set is not presented as a controlled inventory. Supports card transcription only after a deliberate second pass.          |
| IMG-04 | `scotland-yard-docs/photoscans/full-1.jpeg`                                 |  2160×3840 | 0.5625 | B              | Near-complete board photograph. Oblique/perspective-distorted, with strong central glare, fold/seam, and soft detail in parts of the board. Supports regional cross-checking, not precise whole-board coordinate extraction. |
| IMG-05 | `scotland-yard-docs/photoscans/full-2.jpeg`                                 |  2160×3840 | 0.5625 | B              | Near-complete board photograph from a different crop/orientation. Oblique, dark in places, reflective glare, and fold/seam. Useful for cross-checking central and upper/lower regions.                                       |
| IMG-06 | `scotland-yard-docs/photoscans/full-3.jpeg`                                 |  2160×3840 | 0.5625 | B              | Near-complete board photograph with broad station coverage. Perspective distortion and glare remain; station markers are often visible, but small transport distinctions are not auditable everywhere.                       |
| IMG-07 | `codex-clipboard-75c3c5ae-f414-4f9d-b650-d36ca8549020.jpg`                  |  2160×3840 | 0.5625 | B              | Clipboard copy of the same apparent full-board view as IMG-04. It is a separate accessible file but not independent visual evidence; treat it as a duplicate until provenance is confirmed.                                  |

Classification means suitability for reconstruction, not aesthetic quality: A would support precise transcription, B supports partial transcription with cross-checking, C is contextual/card evidence, and D would be unusable.

## Region-coverage inventory

| Region                             | Available evidence                                  | Coverage result                                                                                                       |
| ---------------------------------- | --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Whole board and outer frame        | IMG-01, IMG-04–IMG-07                               | Broad coverage exists, but no straight-on, glare-free, geometrically reliable master image exists.                    |
| Upper/central city                 | IMG-01, IMG-04–IMG-07                               | Broadly visible; transport lines and small labels are not consistently legible.                                       |
| Central Thames, bridges, and docks | IMG-01, IMG-04–IMG-07                               | Visible; fold, glare, and perspective prevent an auditable boat-line trace.                                           |
| Lower city / southern edge         | IMG-01, IMG-04–IMG-07                               | Broadly visible; lower edge and station detail are softened by angle/glare.                                           |
| Right/lower-right border           | IMG-02, IMG-04–IMG-07                               | Strongest local detail in IMG-02; confirms border styling and apparent `200`, but not the complete station inventory. |
| Starting cards                     | IMG-03                                              | Partial card faces visible. No controlled full spread, card backs, or edition panel.                                  |
| Copyright/product panel            | No sufficiently legible panel in the accessible set | Identification is currently project-supplied, not independently re-read from these pixels.                            |

## Required image-level findings

### Is there a complete, straight-on image?

No. IMG-04–IMG-07 show nearly the full board, but they are handheld perspective photographs. IMG-01 is a lower-resolution overview. None provides a flat board plane with all corners, consistent lighting, and no glare/fold interference.

### Can all station numbers be read?

No, not reliably at one time from one image. Many numbers are visually present in the full-board images, but the perspective and resolution make a complete auditable transcription unsafe. IMG-02 supports local reading only.

### Can taxi, bus, and underground lines be distinguished?

Often locally, yes: the board’s yellow, green, and red route conventions are visible. Not reliably across the full board because glare, blur, fold geometry, and line crossings obscure individual routes. No complete edge list is verified by this register.

### Can boat connections be traced?

The Thames geography and water region are visible, but the supplied photographs do not provide a clean, close, straight-on trace of every boat connection and endpoint. The original rules remain the stronger source for the rule wording; the target-board visual cross-check is unresolved.

### Are board edges and the coordinate frame visible?

The outer board edge is visible in the complete-board photographs, but perspective changes the apparent frame and the physical fold is visible. This is sufficient to design a calibration workflow, not to commit final normalized coordinates.

### Are labels hidden by glare, folds, or pieces?

Yes. IMG-04 has strong central glare; IMG-05/IMG-06 show reflective/dark areas; all complete-board captures include a fold/seam or perspective effects. No pawns materially block the supplied board overview, but small station graphics and route junctions remain difficult to audit.

### Can accurate coordinate extraction be performed?

Not from this set alone. Coordinates can be estimated for a prototype overlay, but the evidence does not support verified canonical coordinates or a claim of 1:1 accuracy.

## Station 200 discrepancy

IMG-02 clearly shows a marker labelled `200` in the visible lower/right region. This conflicts with the locked project target of stations 1–199. The correct interpretation is unresolved: the photograph may represent a related edition, the target may have a different inventory than assumed, or the board/reference may include a non-station notation. The 1–199 project target is therefore retained but not independently confirmed.

No station `200` record has been added to the package. No station inventory has been generated from the photographs.

## Boat-route evidence

The supplied rulebook states the black-ticket river journey in the reviewed page-10 section. The existing board-data package records only the three rules-backed endpoint facts as isolated evidence, not as a complete canonical graph. The physical photographs show the Thames and route styling but do not support a clean, edge-by-edge endpoint audit. Candidate community data is secondary and conflicting, so it is not used to resolve the route.

## Starting-position evidence

IMG-03 contains readable card faces, including several values, but it is a casual spread with cropped cards and no controlled count or edition panel. It can support a future transcription worksheet after each card is re-photographed face-up, numbered in a complete inventory, and cross-checked against the target edition. It does not justify a canonical starting-position dataset or allocation logic.

## Confirmed, unresolved, and unsupported facts

Confirmed for evidence workflow:

- The supplied images depict a Central London Scotland Yard board with the expected transport colour language and Thames geography.
- IMG-02 visibly contains a `200` marker.
- The available image files are all portrait-oriented captures with the dimensions listed above.
- The accessible complete-board images are perspective-distorted and affected by glare and/or a fold.

Unresolved:

- Whether the photographed board is exactly product 4500-X2.
- Whether the target physical edition contains 199 or 200 numbered stations.
- The complete station inventory and every station centre.
- The complete taxi, bus, underground, and boat topology.
- The complete starting-position card set.
- A geometrically accurate board boundary and fold model.

Unsupported and deliberately not claimed:

- A 1:1 reconstruction.
- Canonical coordinates.
- A canonical edge count.
- A verified starting-position dataset.
- Multiplayer or game-engine state.

## Missing physical evidence

The next capture should be a flat, straight-on, high-resolution scan or photograph with:

- the complete board, all four outer corners, and the board fold visible;
- no glare or shadows, even diffuse lighting, and the board lying flat;
- at least 4000 pixels on the long side, preferably a lossless or minimally compressed original;
- a separate legible copyright/product-panel close-up;
- separate close-ups for the Thames/boat route and each dense board quadrant;
- a complete face-up starting-card inventory, one card per image or a high-resolution flat spread with all edges visible.

## Recommended next action

Obtain the straight-on capture described above before transcribing any canonical records. Then run the coordinate-preparation procedure in [BOARD-COORDINATE-RECONSTRUCTION.md](BOARD-COORDINATE-RECONSTRUCTION.md), create evidence-linked worksheet records, and use [BOARD-TRANSCRIPTION-WORKFLOW.md](BOARD-TRANSCRIPTION-WORKFLOW.md) for independent review. Keep `CANONICAL_DATASET_AVAILABILITY.available` set to `false` until the full evidence and validation gates pass.
