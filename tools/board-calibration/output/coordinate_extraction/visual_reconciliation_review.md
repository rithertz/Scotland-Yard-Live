# Scotland Yard Live — Phase 3C.3-C.2 Visual Coordinate Reconciliation Review Report

> **Notice:** This document is the formal deliverable for Owner Review under Phase 3C.3-C.2.
> All coordinates and features remain strictly provisional. Station numbering and transport edges are NOT included.

## 1. Mathematical Observation-to-Feature Accounting

Every raw observation across all five calibrated source images is accounted for exactly once in this reconciliation.

### Complete Accounting Invariants:
| Metric | Total | Yellow Badges | Red Underground | Notes / Composition |
|---|---|---|---|---|
| **Raw Observations Ingested** | **138** | **116** | **22** | 94 Full-board + 44 Close-up Quadrants |
| — *Full-Board Observations* | 94 | 81 | 13 | Global reference (`rectified_complete.png`) |
| — *Quadrant Observations* | 44 | 35 | 9 | 7 TL, 9 TR, 16 BL, 12 BR |
| **Observations in Multi-Image Groups** | **32** | **24** | **8** | 13 pairs (26 obs) + 2 triplets (6 obs) |
| **Reconciled Multi-Image Groups** | **15** | **12** | **3** | Resulting cross-image provisional features |
| **Duplicate Observations Absorbed** | **17** | **12** | **5** | Redundant detections reconciled into groups |
| **Unmatched Full-Board Observations** | **79** | **69** | **10** | Sole observation from global reference |
| **Unmatched Close-Up Observations** | **27** | **23** | **4** | Close-up exclusive features |
| **Final Provisional Features** | **121** | **104** | **17** | **Total Features: 138 - 17 = 121** |

> **Mathematical Verification:**
> - Yellow features: $116 - 12 = 104$.
> - Red Underground features: $22 - 5 = 17$.
> - Total provisional features: $104 + 17 = 121$.
> - Grouping breakdown: $106\text{ single-obs features} + 13\text{ pairs} \times 2 + 2\text{ triplets} \times 3 = 106 + 26 + 6 = 138\text{ raw observations}$.

### Verification Status Breakdown:
- **Automatically Detected (High Confidence):** 105
- **Ambiguous (Route Intersection / Merged / Borderline Fill):** 11
- **Needs Owner Review (Discrepancy / Proximity Borderline):** 5

### Coordinate Derivation Method:
- **Global Reference Derived:** 84
- **Global Reference Verified (< 5px discrepancy):** 10
- **Close-up Exclusive:** 27

---

## 2. Review Deliverables & Visual Overlays

1. **Full-Board Review Overlay:**
   - Path: `D:\03_Development\GameDev\Scotland-Yard-Live\tools\board-calibration\output\coordinate_extraction\overlay_reconciled_review.png`
   - Distinguishes Reconciled Yellow, Red Underground, Global Ref Verified, Ambiguous, and Needs-Review markers.
2. **Source Image Underneath View:**
   - Path: `D:\03_Development\GameDev\Scotland-Yard-Live\tools\board-calibration\output\coordinate_extraction\overlay_source_underneath.png`
   - Shows the calibrated board photograph directly beneath markers to assess spatial accuracy, local spacing, and alignment with roads and the Thames.
3. **Clean Marker-Only View:**
   - Path: `D:\03_Development\GameDev\Scotland-Yard-Live\tools\board-calibration\output\coordinate_extraction\overlay_marker_clean.png`
   - Shows clean marker placement on neutral cartographic parchment with continuous Thames watercourse guide and legend.

---

## 3. Questionable Regions and Items Requiring Attention

### A. Items Flagged as `needs-owner-review`:
| Feature ID | Category | Norm Pos (X, Y) | Canvas Pixel | Contrib Dets | Review Note |
|---|---|---|---|---|---|
| `FEAT_0098` | yellow | (0.3034, 0.0583) | (409.6, 58.3) | top-left_Y_0005 | Close-up exclusive marker (top-left). Proximity to nearest full candidate: 22.4px. |
| `FEAT_0100` | yellow | (0.7106, 0.5139) | (959.3, 513.9) | top-right_Y_0002 | Close-up exclusive marker (top-right). Proximity to nearest full candidate: 20.9px. |
| `FEAT_0108` | yellow | (0.5206, 0.6425) | (702.8, 642.5) | bottom-left_Y_0009 | Close-up exclusive marker (bottom-left). Proximity to nearest full candidate: 22.9px. |
| `FEAT_0112` | red_underground | (0.2956, 0.5867) | (399.0, 586.7) | bottom-left_R_0003 | Close-up exclusive marker (bottom-left) in outer quadrant region. |
| `FEAT_0116` | yellow | (0.6870, 0.9252) | (927.4, 925.2) | bottom-right_Y_0003 | Close-up exclusive marker (bottom-right) in outer quadrant region. |

### B. Geographic Sectors with High Ambiguity or Review Need:
1. **South-East Sector (Quadrant 4, Lower Thames / Outer Estuary Sector):**
   - Observation `bottom-right_Y_0001` at canvas pixel `(1151.8, 938.8)` captures an observed physical badge marker near the border/fold.
   - An adjacent marker exhibits dense route convergence; visual inspection confirms clear separation between the two badges.
2. **South Bank Waterfront Sector (Central-South Riverside Sector):**
   - Multiple close-up observations (`bottom-left_Y_0001`, `bottom-left_Y_0002`, `bottom-left_Y_0003`) along the southern river bank provide high-clarity placement where global full-board illumination is darker.
3. **Central Seam Sector (Board Fold Line, X ≈ 650–700):**
   - Features near the central fold seam have minor horizontal residual displacement (~2–6 px). Close-up observations provide stable local placement without introducing distortion.
4. **North-West Sector (Outer Paddington / Marylebone Margin Sector):**
   - Close-up observation `top-left_Y_0005` at pixel `(409.6, 58.3)` is near the northern border, retained as an individual feature for owner review due to proximity to the upper edge.

---

## 4. Identity & Playability Safeguards

- All `station_id` fields are strictly `null`.
- No station numbers have been inferred from detection sequence or physical adjacency.
- Station 200 remains an observed physical badge marker; its gameplay status remains unverified.
- Candidate transport edges remain completely separate and unverified.

Generated: 2026-11-05T22:09:46.163246+00:00