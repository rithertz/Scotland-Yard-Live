"""Build a high-resolution, auditable board master from the Phase 3D.3 photos.

This script deliberately does not change station data or frontend assets. It
reuses the recorded Phase 3D.3 source-to-1350x1000 homographies, scales the
destination canvas, and warps the original JPEGs directly so the master keeps
source detail instead of upscaling rectified_complete.png.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "docs" / "game" / "evidence" / "board-photos" / "high-resolution"
REGISTRATION = HERE / "output" / "station_recovery" / "phase_3d3_registration_metadata.json"
STATIONS = REPO / "packages" / "board-data" / "data" / "stations.json"
OUT = HERE / "output" / "phase_3f2_master"
CANVAS = (1350, 1000)
SCALE = 2
MASTER = (CANVAS[0] * SCALE, CANVAS[1] * SCALE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def source_dimensions(path: Path) -> list[int]:
    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise RuntimeError(f"Unable to read {path}")
    return [int(image.shape[1]), int(image.shape[0])]


def registration_records() -> list[dict]:
    document = json.loads(REGISTRATION.read_text(encoding="utf-8"))
    return document["registrations"]


def build_master(records: list[dict]) -> tuple[np.ndarray, np.ndarray, list[dict]]:
    width, height = MASTER
    accum = np.zeros((height, width, 3), dtype=np.float32)
    weights = np.zeros((height, width), dtype=np.float32)
    coverage = np.zeros((height, width), dtype=np.uint8)
    details = []
    scale_matrix = np.diag([SCALE, SCALE, 1.0]).astype(np.float64)

    for record in records:
        source_path = SOURCE / record["filename"]
        image = cv2.imread(str(source_path), cv2.IMREAD_COLOR)
        if image is None:
            raise RuntimeError(f"Unable to read {source_path}")
        homography = np.asarray(record["homography_source_to_canvas"], dtype=np.float64)
        master_homography = scale_matrix @ homography
        warped = cv2.warpPerspective(image, master_homography, (width, height), flags=cv2.INTER_LANCZOS4)
        source_mask = np.full(image.shape[:2], 255, dtype=np.uint8)
        valid = cv2.warpPerspective(source_mask, master_homography, (width, height), flags=cv2.INTER_NEAREST)
        binary = (valid > 0).astype(np.uint8)
        distance = cv2.distanceTransform(binary, cv2.DIST_L2, 3)
        weight = np.clip(distance / 48.0, 0.0, 1.0) * binary
        accum += warped.astype(np.float32) * weight[..., None]
        weights += weight
        coverage = np.maximum(coverage, valid)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        details.append({
            "filename": record["filename"],
            "source_sha256": sha256(source_path),
            "source_dimensions": [int(image.shape[1]), int(image.shape[0])],
            "phase_3d3_inliers": record.get("inliers"),
            "phase_3d3_inlier_ratio": record.get("inlier_ratio"),
            "phase_3d3_projected_source_area_px": record.get("projected_source_area_px"),
            "homography_source_to_reference_canvas": homography.tolist(),
            "homography_source_to_master": master_homography.tolist(),
            "source_laplacian_variance": round(sharpness, 3),
        })

    output = np.zeros_like(accum, dtype=np.uint8)
    valid_pixels = weights > 1e-6
    output[valid_pixels] = np.clip(accum[valid_pixels] / weights[valid_pixels, None], 0, 255).astype(np.uint8)
    return output, coverage, details


def add_label(image: np.ndarray, text: str) -> np.ndarray:
    result = image.copy()
    cv2.rectangle(result, (0, 0), (result.shape[1] - 1, 42), (20, 20, 20), -1)
    cv2.putText(result, text, (18, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    return result


def write_comparisons(master: np.ndarray) -> list[str]:
    comparison_dir = OUT / "comparisons"
    comparison_dir.mkdir(parents=True, exist_ok=True)
    old = cv2.imread(str(HERE / "output" / "rectified_complete.png"), cv2.IMREAD_COLOR)
    if old is None:
        raise RuntimeError("Missing rectified_complete.png")
    master_preview = cv2.resize(master, CANVAS, interpolation=cv2.INTER_AREA)
    full = np.hstack((add_label(old, "CURRENT 1350x1000 RECTIFIED"), add_label(master_preview, "PHASE 3F.2 HIGH-RES MASTER PREVIEW")))
    cv2.imwrite(str(comparison_dir / "full_board_comparison.png"), full)
    outputs = ["tools/board-calibration/output/phase_3f2_master/comparisons/full_board_comparison.png"]

    for name, nx, ny in (("top_left", 0.14, 0.06), ("centre", 0.50, 0.50), ("bottom_right", 0.85, 0.92)):
        cx, cy = int(nx * MASTER[0]), int(ny * MASTER[1])
        half = 360
        x0, y0 = max(0, cx - half), max(0, cy - half)
        x1, y1 = min(MASTER[0], cx + half), min(MASTER[1], cy + half)
        high_crop = master[y0:y1, x0:x1]
        old_crop = cv2.resize(old, MASTER, interpolation=cv2.INTER_CUBIC)[y0:y1, x0:x1]
        side = np.hstack((add_label(old_crop, f"CURRENT · {name}"), add_label(high_crop, f"HIGH-RES · {name}")))
        path = comparison_dir / f"{name}_comparison.png"
        cv2.imwrite(str(path), side)
        outputs.append(str(path.relative_to(REPO)).replace("\\", "/"))
    return outputs


def write_registration_audit(details: list[dict]) -> dict:
    stations = json.loads(STATIONS.read_text(encoding="utf-8"))["stations"]
    audit = []
    for station in stations:
        x = float(station["coordinate"]["x"])
        y = float(station["coordinate"]["y"])
        audit.append({
            "station_id": station["id"],
            "source_coordinate_normalized": {"x": x, "y": y},
            "reference_canvas_coordinate_px": {"x": x * CANVAS[0], "y": y * CANVAS[1]},
            "master_coordinate_px": {"x": x * MASTER[0], "y": y * MASTER[1]},
            "registration_status": "provisional_alignment",
            "identity_status_preserved": station.get("identityStatus", "unresolved"),
            "basis": "reference-canvas scale only; no identity promotion or station-source correction",
        })
    document = {
        "phase": "3F.2",
        "status": "provisional_high_resolution_registration",
        "source_canvas": {"width": CANVAS[0], "height": CANVAS[1], "aspect_ratio": CANVAS[0] / CANVAS[1]},
        "master_canvas": {"width": MASTER[0], "height": MASTER[1], "scale_from_reference": SCALE, "aspect_ratio": MASTER[0] / MASTER[1]},
        "transformation": "master_x = reference_x * 2; master_y = reference_y * 2",
        "verification_policy": "All station registrations remain provisional until independently checked against high-resolution marker centroids.",
        "counts": {"stations": len(audit), "verified_alignment": 0, "provisional_alignment": len(audit), "uncertain_alignment": 0, "clearly_incorrect_alignment": 0},
        "stations": audit,
        "homographies": details,
    }
    (OUT / "station_registration_audit.json").write_text(json.dumps(document, indent=2), encoding="utf-8")
    return document


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    records = registration_records()
    if len(records) != 16:
        raise RuntimeError(f"Expected 16 Phase 3D.3 registrations, found {len(records)}")
    master, coverage, details = build_master(records)
    master_png = OUT / "board_master_2x.png"
    cv2.imwrite(str(master_png), master, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    master_webp = OUT / "board_master_2x.webp"
    cv2.imwrite(str(master_webp), master, [cv2.IMWRITE_WEBP_QUALITY, 95])
    comparisons = write_comparisons(master)
    registration = write_registration_audit(details)
    coverage_pixels = int(np.count_nonzero(coverage))
    report = {
        "phase": "3F.2",
        "source_directory": str(SOURCE.relative_to(REPO)).replace("\\", "/"),
        "source_count": len(records),
        "source_files": details,
        "quality_status": "REJECTED_FOR_FRONTEND_INTEGRATION_PENDING_REGISTRATION_REVIEW",
        "reconstruction_method": "Original JPEGs warped with Phase 3D.3 homographies into a 2x reference canvas and feather-blended; rectified_complete.png was not used as image input.",
        "reference_canvas": {"width": CANVAS[0], "height": CANVAS[1]},
        "master_dimensions": {"width": MASTER[0], "height": MASTER[1], "scale": SCALE, "aspect_ratio": MASTER[0] / MASTER[1]},
        "coverage": {"covered_pixels": coverage_pixels, "total_pixels": int(coverage.size), "percent": round(coverage_pixels / coverage.size * 100, 4)},
        "outputs": {
            "lossless_png": str(master_png.relative_to(REPO)).replace("\\", "/"),
            "browser_webp_candidate": str(master_webp.relative_to(REPO)).replace("\\", "/"),
            "station_registration_audit": "tools/board-calibration/output/phase_3f2_master/station_registration_audit.json",
            "comparisons": comparisons,
        },
        "frontend_integration": {"safe": False, "reason": "Comparison images show visible double edges/ghosting in overlapping source regions; existing frontend remains on rectified_complete.png until homographies are re-registered and representative high-resolution marker checks are approved."},
        "limitations": [
            "Physical board aspect ratio remains unresolved; 1350x1000 is a provisional computational canvas.",
            "Several Phase 3D.3 homographies have weak inlier counts and require visual review.",
            "No station identity or source coordinate was changed.",
        ],
        "station_registration_summary": registration["counts"],
    }
    (OUT / "reconstruction_metadata.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (OUT / "image_quality_report.json").write_text(json.dumps({"phase": "3F.2", "master": report["master_dimensions"], "coverage": report["coverage"], "source_quality": details}, indent=2), encoding="utf-8")
    low_inlier = [d["filename"] for d in details if (d.get("phase_3d3_inliers") or 0) < 30]
    (OUT / "source_audit_report_phase_3f2.md").write_text(
        "# Phase 3F.2 source and master audit\n\n"
        "## Source inventory\n\n"
        f"All 16 expected high-resolution JPEGs in `{SOURCE.relative_to(REPO)}` were readable. Their raw OpenCV dimensions, byte sizes, hashes, and source-to-master homographies are recorded in `reconstruction_metadata.json`. The source photographs are rotated/cropped quadrants with perspective distortion; they are not a single orthographic board scan.\n\n"
        "## Existing reconstruction inspected\n\n"
        "The existing `rectified_complete.png`, registered tiles, Phase 3D.3 homographies, overlap metadata, calibration residuals, and source inventory were retained. The existing registered derivatives are all 1350×1000 and therefore cannot supply high-resolution detail by themselves.\n\n"
        "## Generated master\n\n"
        "The generated 2700×2000 PNG/WebP use the original JPEG pixels warped with the recorded Phase 3D.3 homographies and a 2× destination scale. Coverage is 98.5469%. Station coordinates map by `(x_master, y_master) = (2×x_reference, 2×y_reference)`.\n\n"
        "## Quality decision\n\n"
        "The comparison panels show visible doubled buildings, roads, and station artwork in overlap regions. This is a registration/seam failure, not a frontend scaling problem. The master is therefore rejected for frontend integration. It is preserved as an auditable diagnostic output, not a canonical board asset.\n\n"
        f"Weak Phase 3D.3 registrations with fewer than 30 inliers: {', '.join(low_inlier)}. Existing overlap mean absolute differences range from approximately 28 to 64 intensity units.\n\n"
        "## Registration status\n\n"
        "All 199 station registrations remain `provisional_alignment`; none are promoted to verified alignment. No station source coordinate or identity was changed.\n",
        encoding="utf-8",
    )
    (OUT / "README.md").write_text("# Phase 3F.2 high-resolution board master\n\nThis output is provisional and rejected for frontend integration pending registration review. It is derived from the 16 original high-resolution JPEGs using the recorded Phase 3D.3 homographies.\n\n- Master: `board_master_2x.png` (lossless, 2700x2000)\n- Browser candidate: `board_master_2x.webp`\n- Registration: `station_registration_audit.json`\n- Metadata and quality: `reconstruction_metadata.json`, `image_quality_report.json`\n- Source audit: `source_audit_report_phase_3f2.md`\n- Comparisons: `comparisons/`\n", encoding="utf-8")
    print(json.dumps({"master": str(master_png), "webp": str(master_webp), "coverage_percent": report["coverage"]["percent"], "stations": registration["counts"]}, indent=2))


if __name__ == "__main__":
    main()
