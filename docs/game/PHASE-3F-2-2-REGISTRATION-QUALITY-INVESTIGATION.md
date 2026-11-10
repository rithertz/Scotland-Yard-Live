# Phase 3F.2.2 — Photographic Overlap and Registration Quality Investigation

## Scope and result

This was an evidence-only investigation. The original 16 high-resolution JPEGs were read directly. No new board master was produced or integrated, and no station, transport, candidate, or canonical data was changed.

The neighboring overlap graph contains enough strong matches for many local pairs, but it is not globally reliable. Four pairs were numerically insufficient under the independent SIFT/RANSAC test, and the earlier global graph had nine inconsistent loops. The available evidence is not sufficient to approve a seamless reconstruction.

## Pair audit

The pairwise results below are from the original photographs, not registered derivatives. `usable_candidate` means that the numerical threshold was met; it is not proof that every green match is a true physical correspondence. Full visual diagnostics are in `tools/board-calibration/output/phase_3f2_2_registration/pairwise/`.

| Pair | Good | Inliers | Ratio | Median error px | Estimated overlap px² | Status |
|---|---:|---:|---:|---:|---:|---|
| A1–A2 | 269 | 69 | .2565 | 2.9864 | 11,428,445 | usable candidate |
| A2–A3 | 225 | 7 | .0311 | 1.5799 | 1,451 | insufficient |
| A3–A4 | 358 | 160 | .4469 | 1.9033 | 13,894,833 | usable candidate |
| B1–B2 | 383 | 117 | .3055 | 2.0436 | 7,776,856 | usable candidate |
| B2–B3 | 399 | 105 | .2632 | 2.9484 | 20,251,410 | usable candidate |
| B3–B4 | 513 | 189 | .3684 | 2.6915 | 14,853,218 | usable candidate |
| C1–C2 | 845 | 383 | .4533 | 2.8900 | 15,828,548 | usable candidate |
| C2–C3 | 276 | 41 | .1486 | 2.2559 | 9,968,214 | usable candidate |
| C3–C4 | 647 | 168 | .2597 | 2.3425 | 15,211,848 | usable candidate |
| D1–D2 | 485 | 162 | .3340 | 2.3060 | 16,680,096 | usable candidate |
| D2–D3 | 788 | 356 | .4518 | 2.0081 | 19,036,174 | usable candidate |
| D3–D4 | 1,027 | 489 | .4761 | 3.0376 | 21,875,224 | usable candidate |
| A1–B1 | 434 | 148 | .3410 | 2.8425 | 10,119,357 | usable candidate |
| B1–C1 | 183 | 10 | .0546 | 0.0011 | 1,694,863 | insufficient |
| C1–D1 | 1,501 | 663 | .4417 | 2.8989 | 18,044,094 | usable candidate |
| A2–B2 | 848 | 487 | .5743 | 2.2513 | 20,561,614 | usable candidate |
| B2–C2 | 164 | 15 | .0915 | 1.3213 | 4,321,141 | insufficient |
| C2–D2 | 1,047 | 529 | .5053 | 3.2092 | 25,417,590 | usable candidate |
| A3–B3 | 578 | 307 | .5311 | 2.1910 | 16,100,904 | usable candidate |
| B3–C3 | 126 | 5 | .0397 | 0.2089 | 150 | insufficient |
| C3–D3 | 790 | 427 | .5405 | 1.9696 | 20,940,718 | usable candidate |
| A4–B4 | 443 | 120 | .2709 | 2.4126 | 15,642,720 | usable candidate |
| B4–C4 | 469 | 206 | .4392 | 2.8039 | 17,534,936 | usable candidate |
| C4–D4 | 755 | 330 | .4371 | 2.8287 | 16,512,897 | usable candidate |

Exactly 24 expected pairs were audited and all 16 photographs were read successfully.

## Weak overlaps

- **A2–A3:** only 7 inliers; the estimated overlap collapses to approximately 1,451 px². The accepted points are spatially narrow and do not establish a stable projective relation. Manual control points may help only if a distinctive shared landmark is visible; otherwise another overlap photograph is needed.
- **B1–C1:** 10 inliers with a near-zero residual, which is suspicious rather than reassuring. The points are consistent with a degenerate/repetitive-pattern solution and do not establish adequate spatial coverage.
- **B2–C2:** 15 inliers and low ratio. The pair has some apparent common content but insufficient distinctive support for a reliable homography.
- **B3–C3:** 5 inliers and an estimated overlap of approximately 150 px². This is effectively insufficient evidence.
- **C4 / D3 / D4 region:** individual horizontal overlaps can produce many matches, but the existing global graph still shows loop inconsistency and visible double features. Local match count alone is not enough to approve this region.

The contact sheet and pairwise images show repeated station badges, road lines, river edges, and building textures. Those patterns can generate visually plausible but physically incorrect matches. Green RANSAC inliers must therefore be reviewed against the underlying photographs.

## Method comparison

`method_comparison.json` compares SIFT and ORB on A3–A4, A1–A2, and weak A2–A3. SIFT was stronger on the strong and medium examples. ORB did not rescue A2–A3: it produced only 6 inliers. The method decision is therefore based on correspondence quality and reprojection error, not raw match count. Neither method solves the weak overlaps without additional constraints or evidence.

## Manual control-point feasibility

Manual control points are viable for strong overlaps where the same bridge, river bend, road junction, or distinctive building cluster is clearly visible. They are not viable where the photographs share only repetitive building texture or a narrow ambiguous strip. The proposed annotation format is [PHASE-3F-2-2-MANUAL-CONTROL-POINT-TEMPLATE.json](PHASE-3F-2-2-MANUAL-CONTROL-POINT-TEMPLATE.json). It records photo, pixel coordinate, landmark class, reviewer, and explicit same-landmark confirmation. No control points were fabricated in this phase.

## Recommended next step

Do not run global optimization yet. First obtain human-reviewed control points for the strong/medium overlaps and additional photographs covering A2–A3, B1–C1, B2–C2, and B3–C3 with distinctive shared landmarks. A calibrated camera/lens profile would also help determine whether residual local deformation is lens distortion or board/photo geometry. Until then, the existing low-resolution provisional asset remains the only frontend-safe board image.
