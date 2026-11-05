# Board coordinate reconstruction

## Status and boundary

This document defines a reproducible preparation workflow. It does not contain coordinates and does not authorize estimated coordinates to be published as canonical. The current images are useful for planning and regional comparison, but not for final calibration.

## Coordinate convention

Use a normalized board-plane coordinate system:

- `x = 0` at the corrected left board boundary and `x = 1` at the corrected right boundary.
- `y = 0` at the corrected top board boundary and `y = 1` at the corrected bottom boundary.
- Origin is top-left; x increases rightward and y increases downward.
- Coordinates represent the visual centre of a numbered station marker, not the centre of its printed transport icon.
- Preserve the source pixel coordinate, normalized coordinate, source image ID, crop/region, and confidence in the evidence worksheet before any canonical promotion.

The final `BoardStation.coordinate` remains optional until verified. The package’s canonical validator requires all coordinates and an approved verification status for `canonical-complete`.

## Image preparation

1. Preserve the original file and record its dimensions, format, orientation, and checksum outside the canonical dataset.
2. Rotate the image so the board’s top edge is horizontal; do not overwrite the original.
3. Identify the four outer board corners and the fold/seam as control features.
4. Crop only after recording the uncropped control points and visible margins.
5. Correct exposure and white balance for inspection only. Never use aggressive sharpening or colour changes as evidence for route type.
6. Keep a full-board working copy plus region crops. Every crop must retain its source image ID and pixel bounds.

The current full-board captures contain glare, shadows/darkness, and perspective, so preparation can improve inspection but cannot recover information that is not resolved in the source pixels.

## Perspective and distortion correction

Use a planar projective transform from the four physical board corners. Record the four source points and the target rectangle dimensions. Check the result against the printed outer frame and long straight border segments.

Do not treat the board fold as a simple camera-plane feature. The fold can create a local discontinuity: use separate left/right residual checks, and do not force stations near the seam to fit a single smooth warp. If the board is visibly bowed, capture a better source rather than introducing a high-order warp without validation.

Lens distortion should be evaluated only when the source capture has sufficient straight architectural or border lines. If correction is applied, record the lens model/parameters and compare station residuals before and after correction.

## Calibration methodology

For each candidate image:

1. Mark the four outer board corners in pixel coordinates.
2. Map those corners to a fixed working rectangle, for example 1,000×1,000 units.
3. Apply the perspective transform to the working image.
4. Mark station centres in the corrected image and store working-pixel coordinates.
5. Divide x by working width and y by working height to obtain normalized values.
6. Record the station ID, source region, reviewer, confidence, and notes.
7. Compare the same station across at least two independent images where coverage overlaps.

The board boundary is the coordinate frame. Do not use the page edge, table edge, river edge, or an inferred grid as the frame.

## Station-centre identification

Use the centre of the numbered marker’s transport-stop symbol. When the number plate is asymmetric or a printed route passes through the marker, record the marker centre by its surrounding outline and note the ambiguity. Do not use the centre of the label glyph alone.

Every station worksheet record should contain:

```text
stationId, sourceImage, region, sourcePixelX, sourcePixelY,
normalizedX, normalizedY, coordinateConfidence,
coordinateStatus, visibleServices, reviewer, notes
```

`visibleServices` is evidence about printed station indicators, not an inferred adjacency list.

## Accuracy and confidence assessment

Use practical error bands, not sub-pixel claims:

- **High:** marker centre is clearly resolved after correction, board boundary is reliable, and a second image/reviewer agrees within the selected tolerance.
- **Medium:** marker is readable and position is usable, but glare, fold, or local perspective leaves a measurable ambiguity; requires independent review.
- **Low:** marker or boundary is blurred/occluded, or the location is estimated from a candidate graph; never promote directly to canonical.

Measure residual error in normalized units and working pixels. Report the maximum and median discrepancy across overlapping images. Set the promotion tolerance after inspecting marker size at the final SVG scale; do not invent a universal tolerance before the high-quality source exists.

## Multi-image alignment

Use printed board corners and stable map landmarks as tie points. Align each image independently to the same board rectangle, then compare station centres only in overlapping regions. Keep the images’ independent measurements; do not average conflicting points into a canonical value without resolving the cause.

For IMG-04 and IMG-07, first establish whether they are duplicates. They look like the same view; a duplicate must not be counted as independent agreement.

## Folds, glare, and occlusion

The visible fold/seam is a source of local geometric error. Flag stations and route junctions close to it, and require an alternate angle or a flat scan. Glare may hide a route colour or number; a sharpened or contrast-boosted version is an inspection aid only and cannot establish an absent fact. If a marker is hidden, record `unresolved`, not an interpolated coordinate.

## Future SVG integration

When coordinates and topology are complete, the future renderer should:

1. Read canonical stations and connections from `@scotland-yard-live/board-data`.
2. Map normalized coordinates to the SVG viewBox without embedding station data in JSX.
3. Keep map artwork, route styling, labels, and Thames geometry in presentation layers.
4. Preserve the existing midnight-ink, brass, crimson, parchment, and blue visual identity.
5. Keep viewport, selection, and synthetic-fixture tests independent from the transcription process.

The synthetic fixture must remain the active web source until the canonical package explicitly reports a complete, validated dataset.

## Limitations

## Phase 3B.2 evidence assessment

`complete.jpeg` provides a coherent landscape orientation, all four visible board edges, and a usable overall frame. `top-left.jpeg`, `top-right.jpeg`, `bottom-left.jpeg`, and `bottom-right.jpeg` provide regional overlap and materially better station-marker detail. This is enough to prepare a calibration pass and to inspect the approximate board boundary.

It is not enough to publish canonical coordinates. The complete image is 1280×892, the regional images are rotated/cropped, and no corner control points or image-registration measurements have been recorded. The visible physical board edge and fold must be distinguished from the camera frame before any normalized station centre is promoted.

The current evidence set therefore supports: consistent board orientation, approximate boundary identification, and future multi-image alignment. It does not support: a verified full-board transform, final station-centre coordinates, or a 1:1 accuracy claim.
