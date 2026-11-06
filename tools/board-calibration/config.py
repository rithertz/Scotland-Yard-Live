"""
Configuration for Scotland Yard Live board calibration tooling.
Defines evidence paths, reference image specifications, corner control points,
and output directories.
"""

from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parents[2]
# The supplied originals live in this explicit subdirectory.  The legacy
# flat-path copies were removed from the worktree; these files have the exact
# expected dimensions and SHA-256 values and are therefore the authoritative
# inputs without duplicating large photographs.
EVIDENCE_DIR = REPO_ROOT / "docs" / "game" / "evidence" / "board-photos" / "original-references"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"

# Primary evidence filenames
PRIMARY_IMAGES = [
    "complete.jpeg",
    "top-left.jpeg",
    "top-right.jpeg",
    "bottom-left.jpeg",
    "bottom-right.jpeg",
]

# Primary image expected dimensions (width, height)
EXPECTED_DIMENSIONS = {
    "complete.jpeg": (1280, 892),
    "top-left.jpeg": (925, 1280),
    "top-right.jpeg": (885, 1280),
    "bottom-left.jpeg": (914, 1280),
    "bottom-right.jpeg": (1080, 1499),
}

# Source-image control points in complete.jpeg
# In complete.jpeg (1280x892), the board is photographed rotated 180 degrees (upside down).
# The outer border corners are:
# - Physical North-West (canonical top-left in SVG): Bottom-Right in complete.jpeg (x=1202.5, y=867.5)
# - Physical North-East (canonical top-right in SVG): Bottom-Left in complete.jpeg (x=78.5, y=860.5)
# - Physical South-East (canonical bottom-right in SVG): Top-Left in complete.jpeg (x=30.5, y=0.0)
# - Physical South-West (canonical bottom-left in SVG): Top-Right in complete.jpeg (x=1217.5, y=0.0)
COMPLETE_CORNERS_SRC = {
    "physical_nw": (1202.5, 867.5),
    "physical_ne": (78.5, 860.5),
    "physical_se": (30.5, 0.0),
    "physical_sw": (1217.5, 0.0),
}

# Primary image expected SHA-256 cryptographic hashes
EXPECTED_HASHES = {
    "complete.jpeg": "2B1B33BB430F57BD29F7EBE4BEB978BC662C9B5E56DFBFBC0F4D40C8F3264E33",
    "top-left.jpeg": "CF2CA9C1F12AAB41A9B1FA86C9959CE4BE1345442708D8D53C106C7605B68FAC",
    "top-right.jpeg": "3EB783AF350F518AB0DD535E3DE6CD0714D11CE81A953331091526D3876245F5",
    "bottom-left.jpeg": "489525B999DB44E7AF1C98CB22C660FA7A681058AA76FB7EDE150A46EB325719",
    "bottom-right.jpeg": "855AB1D3652F065C468AD101FB5E64B023082FA6BEBECF91153A7D1E0E4A11B1",
}

# Working canvas dimensions for rectified outputs
# PROVISIONAL COMPUTATIONAL CHOICE ONLY:
# An integer orthogonal grid (1350x1000 px, aspect ratio 1.350) selected for computational
# convenience. This must NOT be construed as a confirmed or verified physical board measurement.
# The true physical board aspect ratio remains unresolved from the photographs alone.
CANVAS_WIDTH = 1350
CANVAS_HEIGHT = 1000
CANVAS_ASPECT_RATIO = CANVAS_WIDTH / CANVAS_HEIGHT  # 1.35 (Provisional)
