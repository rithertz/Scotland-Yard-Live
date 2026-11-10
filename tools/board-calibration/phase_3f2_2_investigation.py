"""Evidence-only investigation of neighboring high-resolution photo overlaps."""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "docs" / "game" / "evidence" / "board-photos" / "high-resolution"
OUT = HERE / "output" / "phase_3f2_2_registration"
PAIR_DIR = OUT / "pairwise"
WEAK_DIR = OUT / "weak_pairs"
NAMES = [f"{row}{col}.jpg" for row in "ABCD" for col in range(1, 5)]
WEAK_PAIRS = [("B1.jpg", "C1.jpg"), ("A2.jpg", "A3.jpg"), ("B3.jpg", "C3.jpg"), ("B2.jpg", "C2.jpg"), ("C3.jpg", "C4.jpg"), ("D2.jpg", "D3.jpg"), ("D3.jpg", "D4.jpg")]


def pairs() -> list[tuple[str, str]]:
    result = []
    for row in "ABCD":
        for col in range(1, 4):
            result.append((f"{row}{col}.jpg", f"{row}{col + 1}.jpg"))
    for col in range(1, 5):
        for row in "ABC":
            result.append((f"{row}{col}.jpg", f"{chr(ord(row) + 1)}{col}.jpg"))
    return result


def load_image(name: str) -> np.ndarray:
    image = cv2.imread(str(SOURCE / name), cv2.IMREAD_COLOR)
    if image is None:
        raise RuntimeError(f"Unable to read {name}")
    return image


def features(image: np.ndarray, method: str):
    scale = min(1.0, 1600.0 / max(image.shape[:2]))
    small = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA) if scale < 1 else image
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    detector = cv2.SIFT_create(nfeatures=5000) if method == "sift" else cv2.ORB_create(nfeatures=5000, fastThreshold=10)
    keypoints, descriptors = detector.detectAndCompute(gray, None)
    return small, keypoints, descriptors, scale


def estimate(a: str, b: str, method: str = "sift", constrained: bool = False) -> dict:
    image_a = load_image(a)
    image_b = load_image(b)
    small_a, key_a, desc_a, scale_a = features(image_a, method)
    small_b, key_b, desc_b, scale_b = features(image_b, method)
    norm = cv2.NORM_L2 if method == "sift" else cv2.NORM_HAMMING
    matcher = cv2.BFMatcher(norm)
    ratio = 0.70 if method == "sift" else 0.78
    raw = matcher.knnMatch(desc_a, desc_b, k=2)
    good = [pair[0] for pair in raw if len(pair) == 2 and pair[0].distance < ratio * pair[1].distance]
    source_points = np.float32([key_a[m.queryIdx].pt for m in good]) / scale_a
    destination_points = np.float32([key_b[m.trainIdx].pt for m in good]) / scale_b
    H, mask = cv2.findHomography(source_points, destination_points, cv2.RANSAC, 6.0) if len(good) >= 8 else (None, None)
    errors = np.array([], dtype=float)
    inlier_indices: list[int] = []
    if H is not None and mask is not None:
        projected = cv2.perspectiveTransform(source_points.reshape(-1, 1, 2), H).reshape(-1, 2)
        inlier_indices = [i for i, value in enumerate(mask.ravel()) if value]
        errors = np.linalg.norm(projected[inlier_indices] - destination_points[inlier_indices], axis=1)
    spread = None
    if inlier_indices:
        pts = source_points[inlier_indices]
        spread = {"x": [round(float(pts[:, 0].min()), 1), round(float(pts[:, 0].max()), 1)], "y": [round(float(pts[:, 1].min()), 1), round(float(pts[:, 1].max()), 1)]}
    overlap_area = None
    if H is not None:
        try:
            inverse = np.linalg.inv(H)
            corners_b = np.float32([[[0, 0], [image_b.shape[1], 0], [image_b.shape[1], image_b.shape[0]], [0, image_b.shape[0]]]])
            projected_b = cv2.perspectiveTransform(corners_b, inverse)[0].astype(np.float32)
            corners_a = np.float32([[0, 0], [image_a.shape[1], 0], [image_a.shape[1], image_a.shape[0]], [0, image_a.shape[0]]])
            projected_b = cv2.convexHull(projected_b)
            overlap, _ = cv2.intersectConvexConvex(projected_b, corners_a)
            overlap_area = float(overlap)
        except cv2.error:
            overlap_area = None
    return {
        "a": a, "b": b, "method": method, "constrained": constrained,
        "dimensions_a": [int(image_a.shape[1]), int(image_a.shape[0])], "dimensions_b": [int(image_b.shape[1]), int(image_b.shape[0])],
        "keypoints_a": len(key_a), "keypoints_b": len(key_b), "good_matches": len(good), "inliers": len(inlier_indices),
        "inlier_ratio": round(len(inlier_indices) / max(len(good), 1), 4),
        "mean_reprojection_error_px": round(float(errors.mean()), 4) if len(errors) else None,
        "median_reprojection_error_px": round(float(np.median(errors)), 4) if len(errors) else None,
        "max_reprojection_error_px": round(float(errors.max()), 4) if len(errors) else None,
        "estimated_overlap_area_in_a_px": round(overlap_area, 1) if overlap_area is not None else None,
        "inlier_spread_in_a": spread,
        "homography": H.tolist() if H is not None else None,
        "status": "usable_candidate" if len(inlier_indices) >= 30 and len(errors) and float(np.median(errors)) < 5 else "insufficient_or_unreliable",
        "evidence_note": "Numerical match result requires visual correspondence review; repetitive board artwork can produce false inliers.",
    }, (small_a, small_b, key_a, key_b, good, inlier_indices)


def visualization(result: dict, visual_data: tuple, output: Path, max_matches: int = 100) -> None:
    image_a, image_b, key_a, key_b, good, inliers = visual_data
    inlier_set = set(inliers)
    accepted = [match for index, match in enumerate(good) if index in inlier_set][:max_matches]
    rejected = [match for index, match in enumerate(good) if index not in inlier_set][:max_matches]
    first = cv2.drawMatches(image_a, key_a, image_b, key_b, rejected, None, matchColor=(0, 0, 255), singlePointColor=(120, 120, 120), flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    second = cv2.drawMatches(image_a, key_a, image_b, key_b, accepted, None, matchColor=(0, 220, 0), singlePointColor=(120, 120, 120), flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    canvas = np.maximum(first, second)
    cv2.rectangle(canvas, (0, 0), (canvas.shape[1] - 1, 42), (20, 20, 20), -1)
    label = f"{result['a']} ↔ {result['b']} | green=inliers red=rejected | inliers={result['inliers']} median={result['median_reprojection_error_px']}px"
    cv2.putText(canvas, label, (16, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imwrite(str(output), canvas)


def main() -> None:
    PAIR_DIR.mkdir(parents=True, exist_ok=True)
    WEAK_DIR.mkdir(parents=True, exist_ok=True)
    audits = []
    for a, b in pairs():
        result, visual_data = estimate(a, b)
        visualization(result, visual_data, PAIR_DIR / f"{Path(a).stem}_{Path(b).stem}.png")
        if (a, b) in WEAK_PAIRS:
            visualization(result, visual_data, WEAK_DIR / f"{Path(a).stem}_{Path(b).stem}_closeup.png", max_matches=250)
        audits.append(result)
    representative = [("A3.jpg", "A4.jpg"), ("A1.jpg", "A2.jpg"), ("A2.jpg", "A3.jpg")]
    methods = []
    for a, b in representative:
        for method in ("sift", "orb"):
            result, _ = estimate(a, b, method=method)
            methods.append(result)
    data = {
        "phase": "3F.2.2",
        "source_directory": str(SOURCE.relative_to(REPO)).replace("\\", "/"),
        "expected_photos": 16,
        "photos_read": len({name for pair in pairs() for name in pair}),
        "expected_neighbor_pairs": 24,
        "audited_pairs": len(audits),
        "pairs": audits,
        "weak_pair_set": [list(pair) for pair in WEAK_PAIRS],
        "visualization_directory": "tools/board-calibration/output/phase_3f2_2_registration/pairwise",
        "weak_visualization_directory": "tools/board-calibration/output/phase_3f2_2_registration/weak_pairs",
    }
    (OUT / "overlap_audit.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    (OUT / "method_comparison.json").write_text(json.dumps({"phase": "3F.2.2", "representative_pairs": [list(pair) for pair in representative], "results": methods, "selection_policy": "Compare physical correspondence and reprojection error; do not select by match count alone."}, indent=2), encoding="utf-8")
    # Contact sheet references the actual generated pair images.
    thumbs = []
    for audit in audits:
        path = PAIR_DIR / f"{Path(audit['a']).stem}_{Path(audit['b']).stem}.png"
        image = cv2.imread(str(path), cv2.IMREAD_COLOR)
        image = cv2.resize(image, (480, 270), interpolation=cv2.INTER_AREA)
        thumbs.append(image)
    rows = [np.hstack(thumbs[i:i + 4]) for i in range(0, len(thumbs), 4)]
    cv2.imwrite(str(OUT / "all_24_pairs_contact_sheet.png"), np.vstack(rows))
    (OUT / "README.md").write_text("# Phase 3F.2.2 registration-quality investigation\n\nThis is an evidence-only investigation. It audits all 24 neighboring overlaps using original high-resolution JPEGs, writes pairwise SIFT/RANSAC diagnostics, compares SIFT and ORB on representative pairs, and does not create a board master or modify frontend/data.\n\n- `overlap_audit.json` — all 24 pair results\n- `method_comparison.json` — SIFT/ORB comparison\n- `all_24_pairs_contact_sheet.png` — visual overview\n- `pairwise/` — one visualization per pair\n- `weak_pairs/` — enlarged weak-pair visualizations\n", encoding="utf-8")
    print(json.dumps({"photos_read": data["photos_read"], "audited_pairs": len(audits), "usable_candidates": sum(item["status"] == "usable_candidate" for item in audits), "insufficient_or_unreliable": sum(item["status"] != "usable_candidate" for item in audits)}, indent=2))


if __name__ == "__main__":
    main()
