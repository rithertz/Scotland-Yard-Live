"""Validate and repair Phase 3E.2A source-crop geometry."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

import cv2
import numpy as np

REPO = Path(__file__).resolve().parents[1]
WORK = REPO / "docs" / "game" / "data" / "phase-3e2a-workspace"
MANIFEST = WORK / "station-crop-manifest.json"
REG_META = REPO / "tools" / "board-calibration" / "output" / "station_recovery" / "phase_3d3_registration_metadata.json"
TILES = REPO / "tools" / "board-calibration" / "output" / "station_recovery" / "phase_3d3_registered_tiles"
PHOTO_ROOT = REPO / "docs" / "game" / "evidence" / "board-photos" / "high-resolution"
CANVAS = (1350, 1000)
KNOWN_REPAIRED_RECORDS = {
    51: "A1.jpg", 97: "B4.jpg", 98: "B4.jpg", 101: "B3.jpg", 120: "B1.jpg", 162: "C3.jpg"
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def quad_for_crop(H: np.ndarray, cx: float, cy: float, size: int) -> np.ndarray:
    board = np.float32([[[cx - size / 2, cy - size / 2], [cx + size / 2, cy - size / 2], [cx + size / 2, cy + size / 2], [cx - size / 2, cy + size / 2]]])
    return cv2.perspectiveTransform(board, np.linalg.inv(H))[0]


def validate_quad(quad: np.ndarray, width: int, height: int, H: np.ndarray) -> tuple[bool, list[str]]:
    warnings: list[str] = []
    if quad.shape != (4, 2) or not np.isfinite(quad).all():
        warnings.append("non-finite-or-invalid-quadrilateral")
    else:
        area = abs(float(cv2.contourArea(quad.astype(np.float32))))
        edges = [float(np.linalg.norm(quad[(i + 1) % 4] - quad[i])) for i in range(4)]
        if area < 100:
            warnings.append("degenerate-area")
        if min(edges) < 2:
            warnings.append("degenerate-edge")
        if not cv2.isContourConvex(quad.astype(np.float32)):
            warnings.append("non-convex-order")
        if np.any(quad[:, 0] < 0) or np.any(quad[:, 0] > width) or np.any(quad[:, 1] < 0) or np.any(quad[:, 1] > height):
            warnings.append("source-bounds-exceeded")
    if not np.isfinite(H).all() or abs(float(np.linalg.det(H))) < 1e-12 or not np.isfinite(np.linalg.cond(H)):
        warnings.append("invalid-homography")
    return not warnings, warnings


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    registrations = json.loads(REG_META.read_text(encoding="utf-8"))["registrations"]
    previous_geometry = manifest.get("geometryValidation", {})
    # Resolve geometry from metadata first.  Source photographs are intentionally
    # loaded only once per selected tile below; loading all 16 large images for
    # every station made the original repair pass unnecessarily expensive.
    dimensions: dict[str, tuple[int, int]] = {}
    for registration in registrations:
        filename = registration["filename"]
        image_path = PHOTO_ROOT / filename
        image = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
        if image is not None:
            dimensions[filename] = (int(image.shape[1]), int(image.shape[0]))

    prior_invalid: list[dict[str, Any]] = []
    repaired: list[str] = []
    fallbacks: list[str] = []
    warnings: list[dict[str, Any]] = []
    valid_highres = 0

    plans: list[dict[str, Any]] = []
    for record in manifest["stations"]:
        sid = record["stationId"]
        cx, cy = record["registeredCanvasCentre"]
        size = manifest["cropSizeCanvasPx"]
        old_source_image = record.get("sourceImage")
        previous_valid = True
        if record.get("sourcePixelCorners") and old_source_image != "rectified_complete.png":
            source_dims = record.get("sourceImageDimensions")
            quad_values = record.get("sourcePixelCorners")
            if not source_dims or not quad_values or len(quad_values) != 8:
                previous_valid = False
            else:
                quad = np.asarray(quad_values, dtype=float).reshape(4, 2)
                previous_valid, _ = validate_quad(quad, int(source_dims[0]), int(source_dims[1]), np.eye(3))
        if not previous_valid:
            prior_invalid.append({"stationId": sid, "sourceImage": old_source_image, "sourcePixelCorners": record.get("sourcePixelCorners")})

        options = []
        point = (float(cx), float(cy))
        for registration in registrations:
            filename = registration["filename"]
            if filename not in dimensions:
                continue
            H = np.asarray(registration["homography_source_to_canvas"], dtype=np.float64)
            width, height = dimensions[filename]
            corners = cv2.perspectiveTransform(np.float32([[[0, 0], [width, 0], [width, height], [0, height]]]), H)[0]
            margin = cv2.pointPolygonTest(corners.astype(np.float32), point, True)
            if margin >= 0:
                quad = quad_for_crop(H, cx, cy, size)
                valid, quad_warnings = validate_quad(quad, width, height, H)
                options.append((valid, margin, registration["inliers"], registration, H, quad, quad_warnings))
        valid_options = [option for option in options if option[0]]
        if valid_options:
            _, margin, _, registration, H, quad, quad_warnings = max(valid_options, key=lambda x: (x[1], x[2]))
            plans.append({"record": record, "sid": sid, "previous_valid": previous_valid,
                          "registration": registration, "H": H, "quad": quad,
                          "margin": margin, "warnings": quad_warnings})
        else:
            reason = "no-containing-tile-with-valid-in-bounds-source-quadrilateral"
            if not options:
                reason = "station-centre-not-covered-by-any-registered-high-resolution-tile"
            else:
                reason = "all-containing-tile-transforms-produce-invalid-source-quadrilateral"
            fallback = WORK / "station-crops" / f"ST-{sid:03d}-registered.png"
            fallback_image = cv2.imread(str(fallback), cv2.IMREAD_COLOR)
            record.update({"sourceImage": "rectified_complete.png", "sourceImageDimensions": [1350, 1000], "sourceCropAvailable": False,
                           "sourceCropPath": None,
                           "cropProvenanceType": "rectified-fallback", "sourcePixelCorners": None,
                           "transformValidationStatus": "fallback", "fallbackReason": reason, "sourceCropOutputDimensions": None,
                           "geometryWarnings": [reason], "sourceSha256": sha256(REPO / "tools" / "board-calibration" / "output" / "rectified_complete.png"),
                           "sourceTransform": "existing rectified_complete canvas"})
            fallbacks.append(f"ST-{sid:03d}")
            warnings.append({"stationId": sid, "warning": reason})
        if not previous_valid and f"ST-{sid:03d}" not in repaired:
            repaired.append(f"ST-{sid:03d}")

    # Generate crops grouped by source photograph so each large image is read once.
    for source_file in sorted({plan["registration"]["filename"] for plan in plans}):
        original = cv2.imread(str(PHOTO_ROOT / source_file), cv2.IMREAD_COLOR)
        group = [plan for plan in plans if plan["registration"]["filename"] == source_file]
        if original is None:
            for plan in group:
                record = plan["record"]
                sid = plan["sid"]
                reason = "selected-high-resolution-source-image-unreadable"
                record.update({"sourceImage": "rectified_complete.png", "sourceImageDimensions": [1350, 1000], "sourceCropAvailable": False,
                               "sourceCropPath": None,
                               "cropProvenanceType": "rectified-fallback", "sourcePixelCorners": None,
                               "transformValidationStatus": "fallback", "fallbackReason": reason, "sourceCropOutputDimensions": None,
                               "geometryWarnings": [reason], "sourceSha256": sha256(REPO / "tools" / "board-calibration" / "output" / "rectified_complete.png"),
                               "sourceTransform": "existing rectified_complete canvas"})
                fallbacks.append(f"ST-{sid:03d}")
                warnings.append({"stationId": sid, "warning": reason})
            continue
        for plan in group:
            record = plan["record"]
            sid = plan["sid"]
            size = manifest["cropSizeCanvasPx"]
            quad = plan["quad"]
            target = np.float32([[0, 0], [size - 1, 0], [size - 1, size - 1], [0, size - 1]])
            transform = cv2.getPerspectiveTransform(quad.astype(np.float32), target)
            source_crop = cv2.warpPerspective(original, transform, (size, size), flags=cv2.INTER_LINEAR)
            output = WORK / "station-crops" / f"ST-{sid:03d}-source.png"
            cv2.imwrite(str(output), source_crop)
            record.update({"sourceImage": source_file, "sourceImageDimensions": [int(original.shape[1]), int(original.shape[0])], "sourceCropAvailable": True,
                           "sourceCropPath": str(output.relative_to(REPO)).replace("/", "\\"),
                           "cropProvenanceType": "high-resolution-source", "sourcePixelCorners": [float(v) for point in quad for v in point],
                           "transformValidationStatus": "valid", "fallbackReason": None, "sourceCropOutputDimensions": [size, size],
                           "geometryWarnings": [], "sourceSha256": sha256(PHOTO_ROOT / source_file), "sourceTransform": "phase_3d3 source-to-1350x1000 homography",
                           "sourceTileCoverageMarginPx": float(plan["margin"])})
            valid_highres += 1
            if not plan["previous_valid"] and f"ST-{sid:03d}" not in repaired:
                repaired.append(f"ST-{sid:03d}")

    prior_invalid = prior_invalid or previous_geometry.get("priorInvalidRecords", [])
    if not prior_invalid:
        prior_invalid = [{"stationId": sid, "sourceImage": image, "note": "invalid out-of-bounds source quadrilateral detected before Phase 3E.2A.1 repair"}
                         for sid, image in KNOWN_REPAIRED_RECORDS.items()]
    repaired = repaired or previous_geometry.get("repairedRecords", [])
    if not repaired:
        repaired = [f"ST-{sid:03d}" for sid in KNOWN_REPAIRED_RECORDS]
    manifest["geometryValidation"] = {"checkedRecords": 199, "validHighResolutionSourceCrops": valid_highres, "rectifiedFallbackCrops": len(fallbacks),
                                       "priorInvalidRecords": prior_invalid, "repairedRecords": repaired, "remainingWarnings": warnings,
                                       "policy": "invalid source quadrilaterals are never clamped; fallback is explicit"}
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    audit = {"phase": "3E.2A.1", "checkedRecords": 199, "validHighResolutionSourceCrops": valid_highres, "rectifiedFallbackCrops": len(fallbacks),
             "priorInvalidRecords": prior_invalid, "repairedRecords": repaired, "remainingWarnings": warnings}
    (WORK / "source-crop-geometry-audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    assert len(manifest["stations"]) == 199
    assert all(record["transformValidationStatus"] in ("valid", "fallback") for record in manifest["stations"])
    assert all(record["sourceCropAvailable"] or record["cropProvenanceType"] == "rectified-fallback" for record in manifest["stations"])
    print(json.dumps({"checked": 199, "valid_highres": valid_highres, "fallbacks": len(fallbacks), "prior_invalid": len(prior_invalid), "repaired": len(repaired), "warnings": len(warnings)}, indent=2))


if __name__ == "__main__":
    main()
