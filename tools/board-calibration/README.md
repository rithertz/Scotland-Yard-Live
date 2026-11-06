# Scotland Yard Live — Board Calibration Tooling (Phase 3C.3-B.1)

## 1. Overview

This directory contains the offline, reproducible Python + OpenCV board calibration foundation for **Scotland Yard Live**.

Phase 3C.3-B.1 conducts an evidence audit and implements independent held-out registration validation:

1. **B1: Source Image Identity & Cryptographic Audit** — Verified dimensions ($1280 \times 892$ for `complete.jpeg`), cryptographic SHA-256 hashes, and orientation mapping. Tamper detection raises immediate exceptions if evidence files are modified.
2. **B2: Global Rectification** — Planar homography mapping the four outer board corners of `complete.jpeg` into a provisional computational working canvas ($1350 \times 1000$, aspect ratio 1.350).
3. **B3: Independent Registration Validation** — Deterministic 75% fitting / 25% held-out validation partition using spatial interleaving. Homographies are fitted strictly on the fitting subset; residuals are independently measured on both subsets.
4. **B4: Geometry, Fold, and Directional Residual Assessment** — Clear separation between image-space quadrilateral proportions, unresolved physical board aspect ratio, and provisional working canvas. Evaluates directional error ($\Delta x$, $\Delta y$, anisotropy) and fold seam proximity.
5. **B5: Enlarged Inspection Visuals** — High-resolution comparison panels covering the central cross-fold, Thames bridges, shared boundary stations, spatial residual distribution, and SE quadrant diagnostics.

> **Scope Boundary:** This tooling establishes the geometric calibration foundation only. It does not extract canonical station coordinates, modify the candidate transport graph, declare Station 200 playable, or alter production runtime packages.

---

## 2. Environment & Prerequisites

- **Python:** 3.10+ (tested and verified on Python 3.14.6 64-bit on Windows).
- **Core Dependencies:**
  - `numpy >= 2.0.0` (verified with NumPy 2.5.4)
  - `opencv-python >= 4.10.0` (verified with OpenCV 5.0.0)

### Virtual Environment Setup

To keep calibration dependencies strictly isolated from the Node.js monorepo and system Python:

```powershell
# From the repository root:
python -m venv tools/board-calibration/.venv

# Activate and install dependencies:
tools/board-calibration/.venv/Scripts/python.exe -m pip install -r tools/board-calibration/requirements.txt
```

---

## 3. Tooling Architecture

```text
tools/board-calibration/
├── .gitignore               # Ignores .venv/ and bytecode caches
├── requirements.txt         # Offline Python dependencies (numpy, opencv-python)
├── config.py                # Expected hashes, dimensions, corners, provisional canvas config
├── inventory.py             # B1: Source image inspection, dimension check, and SHA-256 validation
├── geometry.py              # Homography, points transformation, aspect ratio, residuals, train/val split
├── landmarks.py             # Curated station landmarks for the four quadrants
├── calibrate.py             # B2-B5: Main pipeline execution script
├── test_calibration.py      # Unit test suite (12 tests covering geometry, inventory, residuals, hashes)
└── output/                  # Generated artifacts (reports, JSON datasets, registered PNGs)
    ├── source_inventory.json
    ├── control_points.json
    ├── aspect_ratio_report.json
    ├── registration_residuals.json
    ├── calibration_summary.json
    ├── rectified_complete.png
    ├── registered_top-left.png
    ├── registered_top-right.png
    ├── registered_bottom-left.png
    ├── registered_bottom-right.png
    ├── registration_overlay.png
    └── inspection/          # High-resolution visual inspection panels
        ├── spatial_residuals_map.png
        ├── overlap_central_cross_fold.png
        ├── overlap_thames_bridges.png
        └── overlap_shared_stations.png
```

---

## 4. Verification & Testing

### Running Calibration Pipeline

```powershell
tools/board-calibration/.venv/Scripts/python.exe tools/board-calibration/calibrate.py
```

### Running Unit Test Suite

```powershell
tools/board-calibration/.venv/Scripts/python.exe tools/board-calibration/test_calibration.py
```

All 12 unit tests validate:

- Cryptographic SHA-256 hash integrity across all 5 source photographs.
- Tamper detection raising `ValueError` on mismatched or altered files.
- Control point bounds and global corner homography mapping.
- Exact perspective recovery on synthetic planar quadrilaterals.
- Deterministic, disjoint fitting/held-out validation partition with spatial coverage.
- Directional residual computation ($\Delta x$, $\Delta y$, anisotropy).
- Aspect ratio output schema semantics (distinguishing image-space, unresolved physical, and provisional canvas).
- Fold proximity distance and correlation calculations.

---

## 5. Aspect-Ratio Semantics & Uncertainty

The calibration framework strictly distinguishes three concepts:

1. **Image-Space Quadrilateral Proportions:**
   - Raw 2D Euclidean span measurements in `complete.jpeg`: Width $1155.5\text{ px}$, Height $864.7\text{ px}$.
   - Ratio: $\mathbf{1.336 \pm 0.040}$.
   - Reflects the uncorrected quadrilateral in the photo; does not account for camera pitch or out-of-plane paper curvature.

2. **Estimated Physical Board Aspect Ratio:**
   - Status: **`UNRESOLVED_FROM_CURRENT_PHOTOGRAPHS`**.
   - Pinhole perspective model estimate: $\mathbf{1.226}$ (sensitive to camera pitch and corner grazing at $y=0$).
   - Plausible physical range: $[1.226, 1.376]$.
   - Assumed historical Milton Bradley or European board dimensions must **NOT** be used as proof of this particular physical board. Direct physical measurement with calipers/ruler is required to establish canonical physical dimensions.

3. **Provisional Working Canvas:**
   - Dimensions: $1350 \times 1000\text{ px}$.
   - Aspect Ratio: $\mathbf{1.350}$.
   - Classification: **`PROVISIONAL_COMPUTATIONAL_CHOICE`**.
   - Serves as a convenient orthogonal Cartesian coordinate reference canvas. It is **not** a confirmed physical dimension.

---

## 6. Registration Accuracy Findings

Evaluation using independent 75% fitting and 25% held-out validation subsets:

| Metric                     | Fitting Inliers                           | Independent Held-Out Validation Inliers       |
| :------------------------- | :---------------------------------------- | :-------------------------------------------- |
| **Global Mean Residual**   | $0.000710\text{ norm}$ ($0.96\text{ px}$) | **$0.000792\text{ norm}$ ($1.07\text{ px}$)** |
| **Global Median Residual** | $0.000624\text{ norm}$ ($0.84\text{ px}$) | **$0.000685\text{ norm}$ ($0.92\text{ px}$)** |
| **Global Max Residual**    | $0.002217\text{ norm}$ ($2.99\text{ px}$) | **$0.001931\text{ norm}$ ($2.61\text{ px}$)** |

- **Bottom-Right Registration:** 8 candidate matches in `bottom-right.jpeg` were spurious cross-quadrant false positives in the NW/NE quadrants caused by identical London street symbols. RANSAC rejected 100% of these cross-quadrant matches. Within true SE bounds, inliers cover the full quadrant down to Station 200 with an inlier mean residual of $0.000722\text{ norm}$ (fitting) and $0.001001\text{ norm}$ (validation).
- **Fold Seams:** Residuals within $100\text{ px}$ of the horizontal crease and vertical hinge seam remain under $1.5\text{ px}$ ($0.0011\text{ norm}$), confirming that a single planar homography per photograph is mathematically stable without piecewise warping.
