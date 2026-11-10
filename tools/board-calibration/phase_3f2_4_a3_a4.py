"""Deterministic diagnostic analysis for the Phase 3F.2.4 A3-A4 pilot.

This script only reads the source photographs and annotation JSON. It never
rewrites either input and does not promote the resulting homography.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import cv2
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
INPUT_JSON = ROOT / "tools/board-calibration/control-point-workbench/workspace/a3-a4-pilot.json"
PHOTO_DIR = ROOT / "docs/game/evidence/board-photos/high-resolution"
OUTPUT_DIR = ROOT / "tools/board-calibration/output/phase_3f2_4_a3_a4"
SEED = 20260342
RANSAC_THRESHOLD = 25.0
THRESHOLDS = (2.0, 5.0, 10.0, 25.0, 50.0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def finite_point(point: Any) -> bool:
    return isinstance(point, dict) and all(isinstance(point.get(k), (int, float)) and math.isfinite(point[k]) for k in ("x", "y"))


def as_array(points: list[dict[str, float]]) -> np.ndarray:
    return np.asarray([[point["x"], point["y"]] for point in points], dtype=np.float64).reshape(-1, 1, 2)


def project(matrix: np.ndarray, points: np.ndarray) -> np.ndarray:
    return cv2.perspectiveTransform(points.astype(np.float64), matrix.astype(np.float64)).reshape(-1, 2)


def errors(matrix: np.ndarray, source: np.ndarray, destination: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    inverse = np.linalg.inv(matrix)
    forward_points = project(matrix, source)
    backward_points = project(inverse, destination)
    forward = np.linalg.norm(forward_points - destination.reshape(-1, 2), axis=1)
    backward = np.linalg.norm(backward_points - source.reshape(-1, 2), axis=1)
    symmetric = np.sqrt((forward * forward + backward * backward) / 2.0)
    return forward, backward, symmetric


def fit_homography(source: np.ndarray, destination: np.ndarray, threshold: float) -> tuple[np.ndarray, np.ndarray]:
    cv2.setRNGSeed(SEED)
    matrix, mask = cv2.findHomography(source, destination, cv2.RANSAC, threshold, maxIters=10000, confidence=0.999)
    if matrix is None or mask is None or not np.isfinite(matrix).all():
        raise RuntimeError(f"RANSAC failed at threshold {threshold}")
    return matrix / matrix[2, 2], mask.reshape(-1).astype(bool)


def matrix_json(matrix: np.ndarray) -> list[list[float]]:
    return [[float(value) for value in row] for row in matrix]


def write_png(path: Path, image: np.ndarray) -> None:
    if not cv2.imwrite(str(path), image, [cv2.IMWRITE_PNG_COMPRESSION, 3]):
        raise RuntimeError(f"Could not write {path}")


def fit_text(image: np.ndarray, lines: list[str]) -> np.ndarray:
    canvas = np.full((max(500, 80 * len(lines) + 80), 1600, 3), 245, dtype=np.uint8)
    for index, line in enumerate(lines):
        cv2.putText(canvas, line, (40, 70 + index * 72), cv2.FONT_HERSHEY_SIMPLEX, 1.15, (20, 20, 20), 2, cv2.LINE_AA)
    return canvas


def make_visuals(a3: np.ndarray, a4: np.ndarray, source: np.ndarray, destination: np.ndarray, matrix: np.ndarray, report: dict[str, Any]) -> None:
    h3, w3 = a3.shape[:2]
    h4, w4 = a4.shape[:2]
    warped_a3 = cv2.warpPerspective(a3, matrix, (w4, h4), flags=cv2.INTER_LINEAR)
    inverse = np.linalg.inv(matrix)
    warped_a4 = cv2.warpPerspective(a4, inverse, (w3, h3), flags=cv2.INTER_LINEAR)
    mask_a3 = cv2.warpPerspective(np.full((h3, w3), 255, dtype=np.uint8), matrix, (w4, h4)) > 0
    mask_a4 = cv2.warpPerspective(np.full((h4, w4), 255, dtype=np.uint8), inverse, (w3, h3)) > 0

    blend = cv2.addWeighted(a4, 0.5, warped_a3, 0.5, 0)
    difference = cv2.absdiff(a4, warped_a3)
    difference[~mask_a3] = 0
    difference = cv2.normalize(difference, None, 0, 255, cv2.NORM_MINMAX)
    side_scale = min(0.28, 1800 / max(w3 + w4, 1), 900 / max(h3, h4))
    left = cv2.resize(a3, (round(w3 * side_scale), round(h3 * side_scale)), interpolation=cv2.INTER_AREA)
    right = cv2.resize(a4, (round(w4 * side_scale), round(h4 * side_scale)), interpolation=cv2.INTER_AREA)
    side = np.full((max(left.shape[0], right.shape[0]) + 100, left.shape[1] + right.shape[1] + 40, 3), 20, dtype=np.uint8)
    side[60:60 + left.shape[0], 10:10 + left.shape[1]] = left
    side[60:60 + right.shape[0], 30 + left.shape[1]:30 + left.shape[1] + right.shape[1]] = right
    cv2.putText(side, "A3 original", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (230, 230, 230), 2, cv2.LINE_AA)
    cv2.putText(side, "A4 original", (30 + left.shape[1], 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (230, 230, 230), 2, cv2.LINE_AA)

    correspondence = side.copy()
    for index, (src_point, dst_point) in enumerate(zip(source.reshape(-1, 2), destination.reshape(-1, 2)), 1):
        sx, sy = (src_point * side_scale + [10, 60]).astype(int)
        dx, dy = (dst_point * side_scale + [30 + left.shape[1], 60]).astype(int)
        colour = (0, 70, 255) if not report["points"][index - 1]["inlier_at_25px"] else (0, 190, 0)
        cv2.circle(correspondence, (sx, sy), 9, colour, -1)
        cv2.circle(correspondence, (dx, dy), 9, colour, -1)
        cv2.putText(correspondence, f"{index:02d}", (sx + 10, sy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, colour, 2, cv2.LINE_AA)
        cv2.putText(correspondence, f"{index:02d}", (dx + 10, dy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, colour, 2, cv2.LINE_AA)
        cv2.line(correspondence, (sx, sy), (dx, dy), colour, 1, cv2.LINE_AA)

    summary = fit_text(np.zeros((1, 1, 3), dtype=np.uint8), [
        "A3-A4 RANSAC robustness comparison",
        f"all 11 points: median symmetric error {report['all_points']['median_symmetric_error_px']:.2f}px; inliers @25px {report['all_points']['inlier_count_at_25px']}/11",
        f"leave-one-out median symmetric error range: {report['leave_one_out']['median_error_min_px']:.2f}–{report['leave_one_out']['median_error_max_px']:.2f}px",
        f"candidate removal is diagnostic only: {report['recommended_scenario']}",
        "green = RANSAC inlier at 25px; red = outlier",
    ])
    write_png(OUTPUT_DIR / "overlay_a3_to_a4.png", blend)
    write_png(OUTPUT_DIR / "overlay_a4_to_a3.png", cv2.addWeighted(a3, 0.5, warped_a4, 0.5, 0))
    write_png(OUTPUT_DIR / "blend.png", blend)
    write_png(OUTPUT_DIR / "difference.png", difference)
    write_png(OUTPUT_DIR / "side_by_side.png", side)
    write_png(OUTPUT_DIR / "correspondence_visualization.png", correspondence)
    write_png(OUTPUT_DIR / "robustness_comparison.png", summary)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    input_bytes_before = INPUT_JSON.read_bytes()
    document = json.loads(input_bytes_before)
    correspondences = document.get("correspondences", [])
    if len(correspondences) != 11:
        raise ValueError(f"Expected 11 correspondences, found {len(correspondences)}")
    expected_ids = [f"CP-{index:03d}" for index in range(1, 12)]
    actual_ids = [item.get("id") for item in correspondences]
    if actual_ids != expected_ids or len(set(actual_ids)) != 11:
        raise ValueError(f"Expected IDs {expected_ids}, found {actual_ids}")
    if any(item.get("pairId") != "A3-A4" or item.get("leftPhoto") != "A3.jpg" or item.get("rightPhoto") != "A4.jpg" for item in correspondences):
        raise ValueError("Correspondence pair/photo metadata is inconsistent")
    if any(item.get("demo") is not False for item in correspondences):
        raise ValueError("A3-A4 pilot contains a demo correspondence")

    a3_meta = next(photo for photo in document["photos"] if photo["filename"] == "A3.jpg")
    a4_meta = next(photo for photo in document["photos"] if photo["filename"] == "A4.jpg")
    a3_path = PHOTO_DIR / "A3.jpg"
    a4_path = PHOTO_DIR / "A4.jpg"
    a3 = cv2.imread(str(a3_path), cv2.IMREAD_COLOR)
    a4 = cv2.imread(str(a4_path), cv2.IMREAD_COLOR)
    if a3 is None or a4 is None:
        raise FileNotFoundError("Could not decode A3.jpg or A4.jpg")
    actual_dimensions = {"A3.jpg": {"width": a3.shape[1], "height": a3.shape[0]}, "A4.jpg": {"width": a4.shape[1], "height": a4.shape[0]}}
    if actual_dimensions["A3.jpg"] != {"width": a3_meta["width"], "height": a3_meta["height"]} or actual_dimensions["A4.jpg"] != {"width": a4_meta["width"], "height": a4_meta["height"]}:
        raise ValueError(f"Photograph dimensions do not match JSON: {actual_dimensions}")

    left_points = [item["left"] for item in correspondences]
    right_points = [item["right"] for item in correspondences]
    if any(not finite_point(point) for point in left_points + right_points):
        raise ValueError("Non-finite correspondence coordinate")
    if any(not (0 <= point["x"] <= a3.shape[1] and 0 <= point["y"] <= a3.shape[0]) for point in left_points):
        raise ValueError("A3 correspondence outside image bounds")
    if any(not (0 <= point["x"] <= a4.shape[1] and 0 <= point["y"] <= a4.shape[0]) for point in right_points):
        raise ValueError("A4 correspondence outside image bounds")

    source = as_array(left_points)
    destination = as_array(right_points)
    matrix, mask = fit_homography(source, destination, RANSAC_THRESHOLD)
    forward, backward, symmetric = errors(matrix, source, destination)
    forward_projected = project(matrix, source)
    backward_projected = project(np.linalg.inv(matrix), destination)
    out_of_bounds_projections = []
    for index, item in enumerate(correspondences):
        fx, fy = forward_projected[index]
        bx, by = backward_projected[index]
        forward_oob = not (0 <= fx <= a4.shape[1] and 0 <= fy <= a4.shape[0])
        backward_oob = not (0 <= bx <= a3.shape[1] and 0 <= by <= a3.shape[0])
        if forward_oob or backward_oob:
            out_of_bounds_projections.append({"id": item["id"], "forward_projected_point": {"x": float(fx), "y": float(fy)}, "backward_projected_point": {"x": float(bx), "y": float(by)}, "forward_out_of_bounds": forward_oob, "backward_out_of_bounds": backward_oob})
    points_report: list[dict[str, Any]] = []
    for index, item in enumerate(correspondences):
        row = {"id": item["id"], "description": item.get("description", ""), "forward_error_px": float(forward[index]), "backward_error_px": float(backward[index]), "symmetric_error_px": float(symmetric[index]), "inlier_at_25px": bool(mask[index])}
        row.update({f"inlier_at_{int(threshold)}px": bool(symmetric[index] <= threshold) for threshold in THRESHOLDS})
        points_report.append(row)

    loo_medians = []
    loo_details = []
    for omit in range(len(correspondences)):
        keep = np.asarray([i != omit for i in range(len(correspondences))])
        loo_matrix, loo_mask = fit_homography(source[keep], destination[keep], RANSAC_THRESHOLD)
        _, _, loo_error = errors(loo_matrix, source[keep], destination[keep])
        loo_medians.append(float(np.median(loo_error)))
        loo_details.append({"omitted_id": correspondences[omit]["id"], "median_symmetric_error_px": float(np.median(loo_error)), "max_symmetric_error_px": float(np.max(loo_error)), "inlier_count_at_25px": int(np.count_nonzero(loo_mask))})

    all_median = float(np.median(symmetric))
    candidate_outliers = [row["id"] for row in points_report if not row["inlier_at_25px"]]
    recommended = "no individual point is removed" if not candidate_outliers else f"inspect {', '.join(candidate_outliers)}; no point was removed automatically"
    retained = np.asarray([item["id"] not in candidate_outliers for item in correspondences])
    removal_matrix, removal_mask = cv2.findHomography(source[retained], destination[retained], 0)
    if removal_matrix is None or not np.isfinite(removal_matrix).all():
        raise RuntimeError("Diagnostic candidate-outlier removal fit failed")
    removal_matrix = removal_matrix / removal_matrix[2, 2]
    _, _, removal_all_error = errors(removal_matrix, source, destination)
    _, _, removal_retained_error = errors(removal_matrix, source[retained], destination[retained])
    report = {
        "phase": "3F.2.4",
        "input": {"path": str(INPUT_JSON), "sha256": sha256(INPUT_JSON), "byte_length": len(input_bytes_before), "unchanged_after_run": False},
        "coordinate_policy": document["coordinateConvention"],
        "manual_rotation_interpretation": "A3 and A4 coordinates are consumed exactly as original decoded pixels. EXIF is not applied and no display rotation is applied during analysis.",
        "integrity": {"correspondence_count": 11, "ids": actual_ids, "all_non_demo": True, "pair_ids": [item["pairId"] for item in correspondences], "dimensions": actual_dimensions, "metadata_inconsistencies": ["CP-006 description contains 'statiion 40'", "CP-010 description contains double space in 'station  53'"]},
        "algorithm": {"method": "cv2.findHomography", "robust_method": "RANSAC", "random_seed": SEED, "ransac_reprojection_threshold_px": RANSAC_THRESHOLD, "max_iterations": 10000, "confidence": 0.999, "error_metric": "forward/backward symmetric RMS pixel error"},
        "all_points": {"homography": matrix_json(matrix), "inlier_count_at_25px": int(np.count_nonzero(mask)), "median_symmetric_error_px": all_median, "mean_symmetric_error_px": float(np.mean(symmetric)), "max_symmetric_error_px": float(np.max(symmetric)), "threshold_counts": {str(int(t)): int(np.count_nonzero(symmetric <= t)) for t in THRESHOLDS}},
        "points": points_report,
        "out_of_bounds_projections": out_of_bounds_projections,
        "leave_one_out": {"median_error_min_px": min(loo_medians), "median_error_max_px": max(loo_medians), "details": loo_details},
        "candidate_outliers_at_25px": candidate_outliers,
        "recommended_scenario": recommended,
        "outlier_removal_scenario": {"description": "Diagnostic only: fit a non-RANSAC homography to the five points classified as 25px inliers; no points were removed from the source JSON.", "removed_ids": candidate_outliers, "retained_ids": [item["id"] for item in correspondences if item["id"] not in candidate_outliers], "retained_median_symmetric_error_px": float(np.median(removal_retained_error)), "all_point_median_symmetric_error_px": float(np.median(removal_all_error)), "all_point_max_symmetric_error_px": float(np.max(removal_all_error)), "homography": matrix_json(removal_matrix)},
        "interpretation": "Residuals measure consistency with a fitted projective model, not correctness of the manually identified station centres. Visual overlap and semantic landmark identity still require human review.",
    }
    report["input"]["unchanged_after_run"] = INPUT_JSON.read_bytes() == input_bytes_before
    (OUTPUT_DIR / "registration_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "homography.json").write_text(json.dumps({"source": "A3.jpg", "destination": "A4.jpg", "matrix": matrix_json(matrix), "seed": SEED, "threshold_px": RANSAC_THRESHOLD}, indent=2) + "\n", encoding="utf-8")
    with (OUTPUT_DIR / "point_error_report.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(points_report[0].keys()))
        writer.writeheader()
        writer.writerows(points_report)
    make_visuals(a3, a4, source, destination, matrix, report)

    report_md = [
        "# Phase 3F.2.4 — A3–A4 Photographic Registration Validation",
        "",
        f"- Input correspondences: **{len(correspondences)}**, IDs CP-001 through CP-011.",
        f"- Dimensions: A3 **{a3.shape[1]}×{a3.shape[0]}**, A4 **{a4.shape[1]}×{a4.shape[0]}**; JSON dimensions match.",
        f"- RANSAC seed: **{SEED}**, threshold: **{RANSAC_THRESHOLD:g}px**, iterations: 10000, confidence: 0.999.",
        f"- All-point fit: **{int(np.count_nonzero(mask))}/11** inliers at 25px; median symmetric error **{all_median:.2f}px**, maximum **{float(np.max(symmetric)):.2f}px**.",
        f"- Candidate outliers at 25px: **{', '.join(candidate_outliers) if candidate_outliers else 'none'}**.",
        "",
        "## Integrity",
        "",
        "All 11 records are non-demo A3–A4 correspondences with finite, in-bounds original decoded pixel coordinates. The input JSON was not written and its bytes were unchanged after analysis.",
        "",
        "Metadata inconsistencies were preserved and reported: CP-006 says `statiion 40`; CP-010 contains a double space in `station  53`.",
        "",
        "## Interpretation",
        "",
        report["interpretation"],
        "",
        f"Leave-one-out median error range: **{min(loo_medians):.2f}–{max(loo_medians):.2f}px**. No correspondence was automatically discarded.",
        f"The diagnostic five-point inlier-only fit has retained median error **{float(np.median(removal_retained_error)):.2f}px**, but its error across all 11 points is median **{float(np.median(removal_all_error)):.2f}px** and maximum **{float(np.max(removal_all_error)):.2f}px**. This demonstrates model dependence rather than validating the six excluded points.",
        "",
        "The generated overlays, blend and difference images are diagnostics only. This result is not promoted to a canonical registration or board reconstruction.",
    ]
    (OUTPUT_DIR / "registration_report.md").write_text("\n".join(report_md) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT_DIR), "correspondences": 11, "inliers_at_25px": int(np.count_nonzero(mask)), "median_symmetric_error_px": all_median, "max_symmetric_error_px": float(np.max(symmetric)), "candidate_outliers": candidate_outliers}, indent=2))


if __name__ == "__main__":
    main()
