# Physical board evidence register

## Status

This register now includes the Phase 3B.2 five-photo set. The locked target remains the 1985 Milton Bradley Scotland Yard board manufactured under licence by Funskool (India) Ltd., product code 4500-X2. The physical board is the primary visual authority. This register does not create canonical stations, edges, coordinates, or starting positions.

The repository is on `feat/board-photo-transcription` for this audit. The canonical dataset remains unavailable in `@scotland-yard-live/board-data`, and the existing synthetic web board remains active.

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

### Phase 3B.2 photographs

| ID     | File                                                | Dimensions | Aspect | Classification | Coverage and limitations                                                                                                                                                                                                                                                            |
| ------ | --------------------------------------------------- | ---------: | -----: | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IMG-08 | `docs/game/evidence/board-photos/complete.jpeg`     |   1280×892 |  1.435 | B              | Complete board and all four outer edges are visible in a landscape capture. Orientation is coherent and substantially better for region coverage than the earlier portrait photos, but the source is still not a calibrated scan; small route junctions need close-up confirmation. |
| IMG-09 | `docs/game/evidence/board-photos/top-left.jpeg`     |   925×1280 |  0.723 | B              | Upper-left/upper-central region, including stations 1–114 and the northern parks/city area. Rotated relative to the board, cropped, and perspective-distorted; strong for station-number and local line inspection.                                                                 |
| IMG-10 | `docs/game/evidence/board-photos/top-right.jpeg`    |   885×1280 |  0.691 | B              | Upper-right/eastern-central region, including stations roughly 4–107 and the eastern river/bridge area. Rotated/cropped; overlaps IMG-09 and IMG-08.                                                                                                                                |
| IMG-11 | `docs/game/evidence/board-photos/bottom-left.jpeg`  |   914×1280 |  0.714 | B              | Lower-left/southwestern region, including stations roughly 113–197 and the western/southern Thames. Rotated/cropped; overlaps IMG-08 and the lower central area.                                                                                                                    |
| IMG-12 | `docs/game/evidence/board-photos/bottom-right.jpeg` |  1080×1499 |  0.720 | B              | Lower-right/southeastern region, including stations roughly 113–200 and the eastern/southern Thames. Rotated/cropped; provides the clearest new confirmation of the printed `200` marker.                                                                                           |

The new set is substantially more useful than the earlier portrait captures. It still does not support a complete, independently reviewed edge transcription: the close-ups are rotated/cropped and the complete view is not high enough resolution to settle every line crossing without ambiguity.

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

`complete.jpeg` is a complete landscape reference with all four board edges visible and a coherent orientation. It is not a calibrated straight-on scan: the board remains photographed on fabric, with mild perspective and insufficient pixel density for final station-centre and edge measurement. The four close-ups provide overlap and detail but are individually rotated/cropped.

### Can all station numbers be read?

The new five-photo set supports a conservative station-number inventory from 1 through 200. The complete image provides sequence context and the four close-ups provide local confirmation. This confirms printed marker observations, not canonical edition inventory or transport connectivity.

### Can taxi, bus, and underground lines be distinguished?

Yes, locally: solid yellow taxi, solid green bus, and dashed red underground markings are visibly distinct in the new close-ups. However, the images do not yet establish every endpoint and line crossing well enough for a complete verified edge list. No canonical edge has been added.

### Can boat connections be traced?

The Thames, bridges, and water-side station markers are substantially clearer in IMG-08 and IMG-11/IMG-12. The photographs establish the geography and visible boat-line context, but not a complete, unambiguous endpoint transcription for all candidate discrepancies. The original rules remain the stronger source for rule wording; target-board edge verification remains unresolved.

### Are board edges and the coordinate frame visible?

Yes, IMG-08 clearly shows the complete outer frame. It is sufficient to define a working board orientation and approximate boundary, but not to commit final normalized coordinates because the image is not a calibrated scan and the close-ups do not yet provide measured control-point overlap.

### Are labels hidden by glare, folds, or pieces?

The new images have no major pawn occlusion. Cropping, rotation, perspective, fabric boundary, and small route crossings remain limitations. The earlier images still have glare/fold issues, but the new `complete.jpeg` is the primary overall reference.

### Can accurate coordinate extraction be performed?

The set supports a consistent orientation and an approximate board boundary. It does not yet support verified canonical coordinates: `complete.jpeg` is only 1280×892 and the close-ups lack recorded corner control points and a controlled calibration target.

## Station 200 discrepancy

IMG-12 clearly shows a printed marker labelled `200` in the lower/right region, and IMG-08 provides whole-board context for the same board. This confirms that `200` is physically present in the newly photographed board. It does not resolve whether the photographed board is the exact locked 4500-X2 target, whether the project’s 1–199 assumption is wrong, or whether an edition/reference discrepancy exists. The 1–199 project target and package validator are retained unchanged pending owner approval based on edition evidence.

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
- The new set contains a complete landscape reference and four overlapping regional close-ups.
- The new set visibly includes station `200`.

Unresolved:

- Whether the photographed board is exactly product 4500-X2.
- Whether the photographed board is exactly product 4500-X2.
- Whether the target physical edition contains 199 or 200 numbered stations.
- The complete station inventory and every station centre.
- The complete taxi, bus, underground, and boat topology.
- The complete starting-position card set.
- A geometrically accurate board boundary and fold model.
- A complete, independently reviewed edge transcription.

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
