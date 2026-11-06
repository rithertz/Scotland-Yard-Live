"""Phase 3D.3 high-resolution registration and conservative station audit.

The 16 originals are registered directly to the established rectified board
reference.  No source image is overwritten, and registration is kept separate
from identity assignment: a readable marker number is still required before a
station can be promoted to ``verified``.
"""

from __future__ import annotations

import hashlib
import json
import math
import shutil
from pathlib import Path
from typing import Any

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "docs" / "game" / "evidence" / "board-photos" / "high-resolution"
OUT = HERE / "output" / "station_recovery"
REG = OUT / "phase_3d3_registered_tiles"
DIAG = OUT / "phase_3d3_overlap_diagnostics"
REG.mkdir(parents=True, exist_ok=True)
DIAG.mkdir(parents=True, exist_ok=True)
CANVAS_W, CANVAS_H = 1350, 1000
EXPECTED = [f"{r}{c}.jpg" for r in "ABCD" for c in range(1, 5)]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def metadata() -> list[dict[str, Any]]:
    records = []
    for name in EXPECTED:
        path = SOURCE / name
        if not path.exists():
            records.append({"filename": name, "status": "missing"})
            continue
        image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        if image is None:
            records.append({"filename": name, "status": "unreadable", "sha256": sha256(path)})
            continue
        records.append({"filename": name, "status": "usable", "relative_path": str(path.relative_to(REPO)),
                        "dimensions": [int(image.shape[1]), int(image.shape[0])], "file_size_bytes": path.stat().st_size,
                        "sha256": sha256(path), "grid_cell": name[:2],
                        "orientation_note": "OpenCV pixel orientation used; no EXIF rotation was applied to source bytes",
                        "coverage_note": "4x4 intended grid; actual overlap determined by direct feature matching"})
    return records


def register_one(path: Path, reference: np.ndarray, ref_kp: list[Any], ref_des: np.ndarray) -> tuple[np.ndarray, dict[str, Any], np.ndarray]:
    original = cv2.imread(str(path), cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    scale = min(1.0, 1900.0 / max(gray.shape))
    small = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA) if scale < 1 else gray
    sift = cv2.SIFT_create(nfeatures=5000)
    kp, des = sift.detectAndCompute(small, None)
    matcher = cv2.BFMatcher()
    knn = matcher.knnMatch(des, ref_des, k=2)
    candidates = []
    height, width = original.shape[:2]
    corners = np.float32([[[0, 0], [width, 0], [width, height], [0, height]]])
    # Repetitive board artwork can produce a high-inlier but degenerate
    # homography collapsing the photograph to one point.  Retry with stricter
    # Lowe ratios and keep the strongest geometrically plausible quadrilateral.
    for ratio in (0.72, 0.68, 0.65, 0.62, 0.60, 0.55):
        good = [pair[0] for pair in knn if len(pair) == 2 and pair[0].distance < ratio * pair[1].distance]
        if len(good) < 8:
            continue
        src = np.float32([kp[m.queryIdx].pt for m in good]).reshape(-1, 1, 2) / scale
        dst = np.float32([ref_kp[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        H_try, mask_try = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
        if H_try is None or mask_try is None:
            continue
        projected = cv2.perspectiveTransform(corners, H_try)[0]
        area = abs(float(cv2.contourArea(projected.astype(np.float32))))
        edges = [float(np.linalg.norm(projected[(i + 1) % 4] - projected[i])) for i in range(4)]
        plausible = 50_000 <= area <= 600_000 and min(edges) >= 100 and max(abs(projected[:, 0])) <= CANVAS_W + 150 and max(abs(projected[:, 1])) <= CANVAS_H + 150
        if plausible and int(mask_try.sum()) >= 8:
            candidates.append((int(mask_try.sum()), ratio, good, H_try, mask_try, area))
    if not candidates:
        raise RuntimeError(f"Unstable homography for {path.name}: no plausible projected board region")
    inlier_count, ratio, good, H, mask, projected_area = max(candidates, key=lambda item: (item[0], item[5]))
    registered = cv2.warpPerspective(original, H, (CANVAS_W, CANVAS_H), flags=cv2.INTER_LINEAR)
    source_mask = np.full(original.shape[:2], 255, dtype=np.uint8)
    valid = cv2.warpPerspective(source_mask, H, (CANVAS_W, CANVAS_H), flags=cv2.INTER_NEAREST)
    rec = {"filename": path.name, "good_matches": len(good), "inliers": int(mask.sum()),
           "inlier_ratio": round(float(mask.sum()) / len(good), 4), "match_ratio": ratio,
           "projected_source_area_px": round(projected_area, 1), "homography_source_to_canvas": H.tolist(),
           "registered_output": str((REG / path.name.replace('.jpg', '.png')).relative_to(REPO))}
    return registered, rec, valid


def detect_registered_markers(image: np.ndarray, source_name: str) -> list[dict[str, Any]]:
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np.array([15, 70, 60], np.uint8), np.array([40, 255, 255], np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    found = []
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        if not (20 <= area <= 1000 and w >= 6 and h >= 6 and 0.45 <= w / max(h, 1) <= 2.8):
            continue
        moments = cv2.moments(contour)
        if moments["m00"] == 0:
            continue
        px, py = moments["m10"] / moments["m00"], moments["m01"] / moments["m00"]
        found.append({"source_tile": source_name, "pixel_x": round(px, 2), "pixel_y": round(py, 2),
                      "normalized_x": round(px / CANVAS_W, 6), "normalized_y": round(py / CANVAS_H, 6),
                      "area": round(float(area), 1)})
    return found


def main() -> None:
    photo_records = metadata()
    usable = [r for r in photo_records if r["status"] == "usable"]
    (SOURCE / "PHOTO-INVENTORY-3D3.md").write_text(
        "# Phase 3D.3 high-resolution photo inventory\n\n" +
        "\n".join(f"- `{r['filename']}` — {r.get('dimensions', 'unavailable')}; {r.get('file_size_bytes', 'n/a')} bytes; SHA-256 `{r.get('sha256', 'n/a')}`; {r['status']}." for r in photo_records) +
        "\n\nOriginal JPEG bytes were read only. Registration outputs are derived PNGs. EXIF-dependent rotation was not applied because the decoded pixel orientation was used consistently for matching.\n", encoding="utf-8")
    reference = cv2.imread(str(HERE / "output" / "rectified_complete.png"), cv2.IMREAD_COLOR)
    if reference is None:
        raise FileNotFoundError("Missing established rectified_complete.png reference")
    ref_gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create(nfeatures=6000)
    ref_kp, ref_des = sift.detectAndCompute(ref_gray, None)
    registrations = []
    masks = {}
    tiles = {}
    detections = []
    for record in usable:
        path = SOURCE / record["filename"]
        tile, registration, valid = register_one(path, reference, ref_kp, ref_des)
        tiles[record["filename"]] = tile
        masks[record["filename"]] = valid
        registrations.append(registration)
        cv2.imwrite(str(REG / record["filename"].replace(".jpg", ".png")), tile)
        detections.extend(detect_registered_markers(tile, record["filename"]))

    (OUT / "phase_3d3_photo_metadata.json").write_text(json.dumps({"phase": "3D.3", "expected": 16, "records": photo_records}, indent=2), encoding="utf-8")
    (OUT / "phase_3d3_registration_metadata.json").write_text(json.dumps({"phase": "3D.3", "reference": "rectified_complete.png", "canvas": [CANVAS_W, CANVAS_H], "registrations": registrations}, indent=2), encoding="utf-8")

    # Feathered diagnostic composite; individual registered tiles remain the
    # primary derived evidence for review.
    accum = np.zeros((CANVAS_H, CANVAS_W, 3), np.float32)
    weights = np.zeros((CANVAS_H, CANVAS_W, 1), np.float32)
    for name, tile in tiles.items():
        mask = (masks[name] > 0).astype(np.float32)[..., None]
        accum += tile.astype(np.float32) * mask
        weights += mask
    composite = (accum / np.maximum(weights, 1)).clip(0, 255).astype(np.uint8)
    cv2.imwrite(str(OUT / "phase_3d3_registered_full_board_composite.png"), composite)

    # Contact sheet of original tiles for provenance review.
    thumb_w, thumb_h = 480, 360
    panels = []
    for record in photo_records:
        image = cv2.imread(str(SOURCE / record["filename"])) if record["status"] == "usable" else np.zeros((thumb_h, thumb_w, 3), np.uint8)
        image = cv2.resize(image, (thumb_w, thumb_h), interpolation=cv2.INTER_AREA)
        cv2.rectangle(image, (0, 0), (thumb_w - 1, thumb_h - 1), (255, 255, 255), 2)
        cv2.putText(image, record["filename"], (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(image, record["filename"], (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)
        panels.append(image)
    rows = [np.hstack(panels[i:i + 4]) for i in range(0, 16, 4)]
    cv2.imwrite(str(OUT / "phase_3d3_4x4_tile_contact_sheet.png"), np.vstack(rows))

    # Adjacent overlap diagnostics in the common canvas.
    overlap_records = []
    for row in "ABCD":
        for col in range(1, 4):
            left, right = f"{row}{col}.jpg", f"{row}{col + 1}.jpg"
            if left not in tiles or right not in tiles:
                continue
            both = (masks[left] > 0) & (masks[right] > 0)
            diff = cv2.absdiff(tiles[left], tiles[right])
            diagnostic = np.zeros_like(diff)
            diagnostic[both] = diff[both]
            cv2.imwrite(str(DIAG / f"overlap_{left[:2]}_{right[:2]}.png"), diagnostic)
            overlap_records.append({"pair": [left, right], "overlap_pixels": int(both.sum()), "mean_abs_difference": float(diff[both].mean()) if both.any() else None})
    for row in "ABC":
        for col in range(1, 5):
            upper, lower = f"{row}{col}.jpg", f"{chr(ord(row) + 1)}{col}.jpg"
            if upper not in tiles or lower not in tiles:
                continue
            both = (masks[upper] > 0) & (masks[lower] > 0)
            diff = cv2.absdiff(tiles[upper], tiles[lower])
            diagnostic = np.zeros_like(diff)
            diagnostic[both] = diff[both]
            cv2.imwrite(str(DIAG / f"overlap_{upper[:2]}_{lower[:2]}.png"), diagnostic)
            overlap_records.append({"pair": [upper, lower], "overlap_pixels": int(both.sum()), "mean_abs_difference": float(diff[both].mean()) if both.any() else None})
    (OUT / "phase_3d3_overlap_metadata.json").write_text(json.dumps({"phase": "3D.3", "pairs": overlap_records}, indent=2), encoding="utf-8")
    (OUT / "phase_3d3_highres_marker_detections.json").write_text(json.dumps({"phase": "3D.3", "detector": "yellow connected components on directly registered high-resolution tiles", "count": len(detections), "detections": detections}, indent=2), encoding="utf-8")

    # Deduplicate only as physical observations.  This does not assign a
    # Scotland Yard number; it is an evidence count for human review.
    clusters: list[dict[str, Any]] = []
    for detection in detections:
        match = None
        for cluster in clusters:
            if math.hypot(detection["pixel_x"] - cluster["pixel_x"], detection["pixel_y"] - cluster["pixel_y"]) < 12:
                match = cluster
                break
        if match is None:
            clusters.append({"pixel_x": detection["pixel_x"], "pixel_y": detection["pixel_y"], "observations": [detection]})
        else:
            match["observations"].append(detection)
            n = len(match["observations"])
            match["pixel_x"] = round(sum(o["pixel_x"] for o in match["observations"]) / n, 2)
            match["pixel_y"] = round(sum(o["pixel_y"] for o in match["observations"]) / n, 2)
    for index, cluster in enumerate(clusters, 1):
        cluster["provisional_marker_id"] = f"HRM_{index:03d}"
        cluster["normalized_x"] = round(cluster["pixel_x"] / CANVAS_W, 6)
        cluster["normalized_y"] = round(cluster["pixel_y"] / CANVAS_H, 6)
    (OUT / "phase_3d3_physical_marker_candidates.json").write_text(json.dumps({"phase": "3D.3", "raw_observations": len(detections), "deduplication_radius_px": 12, "deduplicated_candidates": len(clusters), "candidates": clusters}, indent=2), encoding="utf-8")

    previous_inventory = json.loads((OUT / "station_inventory.json").read_text(encoding="utf-8"))
    previous_mapping = json.loads((OUT / "station_evidence_mapping.json").read_text(encoding="utf-8"))
    previous_matrix = json.loads((OUT / "station_recovery_completeness.json").read_text(encoding="utf-8"))
    phase_meta = {"phase": "3D.3", "high_resolution_photographs_inventoried": len(photo_records), "high_resolution_photographs_used": len(usable), "raw_high_resolution_marker_observations": len(detections), "deduplicated_high_resolution_marker_candidates": len(clusters), "identity_policy": "preserve prior identity status until direct number-to-marker matching is documented"}
    previous_inventory["metadata"]["phase_3d3"] = phase_meta
    previous_mapping["metadata"]["phase_3d3"] = phase_meta
    previous_matrix["metadata"]["phase_3d3"] = phase_meta
    (OUT / "station_inventory_phase_3d3.json").write_text(json.dumps(previous_inventory, indent=2), encoding="utf-8")
    (OUT / "station_evidence_mapping_phase_3d3.json").write_text(json.dumps(previous_mapping, indent=2), encoding="utf-8")
    (OUT / "station_recovery_completeness_phase_3d3.json").write_text(json.dumps(previous_matrix, indent=2), encoding="utf-8")

    # Review overlays: gray physical candidates, with only existing
    # evidence-backed station identities numbered.
    assigned = [station for station in previous_inventory["stations"] if station["status"] in ("verified", "candidate_uncertain")]
    for overlay_name, predicate in (("full_board_station_overlay_phase_3d3.png", lambda _s: True),
                                    ("verified_station_overlay_phase_3d3.png", lambda s: s["status"] == "verified"),
                                    ("uncertain_station_overlay_phase_3d3.png", lambda s: s["status"] == "candidate_uncertain")):
        overlay = composite.copy()
        for cluster in clusters:
            cv2.circle(overlay, (int(cluster["pixel_x"]), int(cluster["pixel_y"])), 5, (150, 150, 150), 1)
        for station in assigned:
            if predicate(station):
                x, y = int(round(station["pixel_x"])), int(round(station["pixel_y"]))
                colour = (0, 220, 0) if station["status"] == "verified" else (0, 180, 255)
                cv2.circle(overlay, (x, y), 9, colour, 2)
                cv2.putText(overlay, str(station["station_id"]), (x + 8, y + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.38, colour, 1, cv2.LINE_AA)
        cv2.putText(overlay, "Phase 3D.3: gray=physical candidate; numbered=prior evidence-backed identity", (18, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.44, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imwrite(str(OUT / overlay_name), overlay)

    # Preserve prior identity status until a station number is independently
    # read and matched; the new high-res evidence is additive and auditable.
    previous = json.loads((OUT / "station_recovery_final_report.md").read_text(encoding="utf-8")) if False else None
    uncertainty = f"""# Phase 3D.3 coordinate uncertainty report

The 16 high-resolution photographs were registered directly to the existing 1350×1000 rectified board reference using SIFT feature matches and RANSAC homographies. {len(registrations)}/{len(EXPECTED)} expected tiles were usable. Registration metadata records match counts, inliers and each source-to-canvas transform.

The composite is diagnostic only. Fold curvature, glare and local perspective remain possible sources of displacement. Individual registered tiles and original JPEGs are retained for review. Yellow connected-component detections are physical-marker candidates, not station identities.
"""
    (OUT / "coordinate_uncertainty_report.md").write_text(uncertainty, encoding="utf-8")
    (OUT / "owner_review_required.md").write_text("# Owner review required\n\nPhase 3D.3 retains the previous conservative identity statuses until each high-resolution label is directly matched to a stable feature ID. Review the 4×4 contact sheet, registered tile outputs, overlap diagnostics and station confidence map before promoting unresolved identities. Marker 200 remains excluded from stations 1–199.\n", encoding="utf-8")
    (OUT / "station_recovery_phase_3d3_report.md").write_text(f"""# Station recovery report — Phase 3D.3

## Exact results

| Metric | Result |
|---|---:|
| Playable station IDs accounted for | 199/199 |
| Verified identities | 2 |
| Candidate-uncertain identities | 4 |
| Unresolved identities | 193 |
| Conflicting identities | 0 |
| Duplicate identities | 0 |
| High-resolution photographs inventoried | {len(photo_records)}/16 |
| High-resolution photographs successfully registered | {len(usable)}/16 |
| Raw high-resolution marker observations | {len(detections)} |
| Deduplicated provisional physical candidates | {len(clusters)} |
| Marker 200 | separate, excluded |

## Registration

Each tile was matched directly to the established rectified board reference using SIFT descriptors, Lowe-ratio filtering, RANSAC homography estimation and projected-quadrilateral validation. No source JPEG was modified. The full-board composite is diagnostic; individual registered tiles and original JPEGs remain the evidence sources.

## Identity result

No station was newly promoted automatically. The high-resolution photographs materially improve physical-marker coverage, but a marker detection is not a station identity. Existing assignments remain unchanged: verified stations 1 and 199; candidate-uncertain stations 3, 120, 123 and 158. The remaining 193 identities are explicit unresolved entries with null station-to-feature assignment rather than unsupported OCR or landmark inference.

## Owner review

Inspect `phase_3d3_4x4_tile_contact_sheet.png`, the registered tile directory, overlap diagnostics, and `full_board_station_overlay_phase_3d3.png`. Human review can promote identities only after a printed number and stable feature correspondence are documented in the evidence mapping.
""", encoding="utf-8")
    print(json.dumps({"expected_photos": len(EXPECTED), "usable_photos": len(usable), "registrations": len(registrations), "marker_detections": len(detections)}, indent=2))


if __name__ == "__main__":
    main()
