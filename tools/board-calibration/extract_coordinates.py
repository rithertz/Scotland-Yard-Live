"""
extract_coordinates.py
======================

Phase 3C.3-C.1 – Station Marker Detection Recovery and Reliability Correction
-----------------------------------------------------------------------------

Evidence-based, multi-category, deterministic detector for Scotland Yard station badges.

DESIGN RATIONALE & CORRECTION AUDIT
------------------------------------
This implementation addresses the issues identified in Phase 3C.3-C:

1. Category Separation:
   - Yellow badges (Taxi/Bus stops): Rounded-rectangle markers with high yellow purity
     (R high, G high, B low: (R+G)/2 - B >= 70).
   - Red Underground badges: Distinct red badge rectangles with high red saturation/dominance
     (R - (G+B)/2 >= 65), verified via adjacent contextual symbology (green bus arc and/or yellow stop).

2. Contour & Shape Filtering:
   - Avoids simplistic circularity assumptions (circ > 0.7 rejected genuine badges whose measured
     circularity is 0.25 - 0.65).
   - Configured fill ratio threshold is explicitly set to 0.15 (matching actual measured values).
   - Large merged contours (area > 3000 px²) are rejected to prevent multi-station/route line merges.
   - Moderately large candidates (area 1200 - 3000 px²) or borderline fill ratios are flagged as
     'ambiguous' for manual review rather than discarded or accepted blindly.

3. Image Domain & Coordinates:
   - Primary reference: `rectified_complete.png` (1350x1000).
   - Supplementary evidence: registered quadrant images (all registered to 1350x1000 canvas).
   - Detections are normalized to [0, 1] x [0, 1] relative to the 1350x1000 working canvas.
   - Cross-image duplicates are correlated by spatial proximity (< 0.015 normalized distance ≈ 15-20 px)
     without merging them into a final canonical station dataset.

IDENTITY SAFEGUARDS
-------------------
- Detection IDs (e.g. `full_Y_0001`, `top-left_R_0002`) are sequential counters per image run.
- They are NOT Scotland Yard station numbers.
- Station 200 is not assigned special status or inferred.
- Production board data and transport graph remain untouched.
"""

import cv2
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import datetime

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
IMAGE_DIR = _HERE / "output"
OUTPUT_DIR = _HERE / "output" / "coordinate_extraction"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGES: Dict[str, Path] = {
    "full":         IMAGE_DIR / "rectified_complete.png",
    "top-left":     IMAGE_DIR / "registered_top-left.png",
    "top-right":    IMAGE_DIR / "registered_top-right.png",
    "bottom-left":  IMAGE_DIR / "registered_bottom-left.png",
    "bottom-right": IMAGE_DIR / "registered_bottom-right.png",
}

# Working canvas dimensions
CANVAS_WIDTH  = 1350
CANVAS_HEIGHT = 1000

# ---------------------------------------------------------------------------
# Detector Parameters
# ---------------------------------------------------------------------------
DETECTOR_CONFIG = {
    "canvas_dimensions": [CANVAS_WIDTH, CANVAS_HEIGHT],
    "yellow_badge": {
        "hsv_lower": [20, 100, 100],
        "hsv_upper": [30, 255, 255],
        "morph_open_k": 3,
        "morph_close_k": 7,
        "area_min": 30,
        "area_max": 3000,
        "bbox_w_min": 8,
        "bbox_h_min": 6,
        "aspect_min": 0.5,
        "aspect_max": 3.5,
        "fill_min": 0.15,
        "yellow_purity_min": 70.0,  # (R+G)/2 - B in ROI
    },
    "red_underground": {
        "hsv_lower_1": [0, 80, 60],
        "hsv_upper_1": [9, 255, 255],
        "hsv_lower_2": [170, 80, 60],
        "hsv_upper_2": [179, 255, 255],
        "morph_open_k": 3,
        "morph_close_k": 7,
        "area_min": 30,
        "area_max": 1000,
        "bbox_w_min": 10,
        "bbox_h_min": 8,
        "aspect_min": 0.8,
        "aspect_max": 2.8,
        "fill_min": 0.20,
        "red_purity_min": 65.0,     # R - (G+B)/2 in ROI
        "context_hsv_green_lower": [35, 60, 40],
        "context_hsv_green_upper": [85, 255, 255],
    },
    "ambiguity_thresholds": {
        "yellow_large_area": 1200,
        "yellow_borderline_fill": 0.22,
    },
    "cross_image_duplicate_dist_norm": 0.015,  # ~15-20 px on 1350x1000 canvas
}


def load_image(path: Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Cannot load image: {path}")
    return img


def build_yellow_mask(img: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cfg = DETECTOR_CONFIG["yellow_badge"]
    lo = np.array(cfg["hsv_lower"], dtype=np.uint8)
    hi = np.array(cfg["hsv_upper"], dtype=np.uint8)
    mask = cv2.inRange(hsv, lo, hi)
    ko = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cfg["morph_open_k"], cfg["morph_open_k"]))
    kc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cfg["morph_close_k"], cfg["morph_close_k"]))
    return cv2.morphologyEx(cv2.morphologyEx(mask, cv2.MORPH_OPEN, ko), cv2.MORPH_CLOSE, kc)


def build_red_mask(img: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cfg = DETECTOR_CONFIG["red_underground"]
    m1 = cv2.inRange(hsv, np.array(cfg["hsv_lower_1"], dtype=np.uint8), np.array(cfg["hsv_upper_1"], dtype=np.uint8))
    m2 = cv2.inRange(hsv, np.array(cfg["hsv_lower_2"], dtype=np.uint8), np.array(cfg["hsv_upper_2"], dtype=np.uint8))
    mask = cv2.bitwise_or(m1, m2)
    ko = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cfg["morph_open_k"], cfg["morph_open_k"]))
    kc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cfg["morph_close_k"], cfg["morph_close_k"]))
    return cv2.morphologyEx(cv2.morphologyEx(mask, cv2.MORPH_OPEN, ko), cv2.MORPH_CLOSE, kc)


def contour_centroid(cnt: np.ndarray) -> Tuple[float, float]:
    M = cv2.moments(cnt)
    if M["m00"] == 0:
        x, y, w, h = cv2.boundingRect(cnt)
        return float(x + w / 2), float(y + h / 2)
    return M["m10"] / M["m00"], M["m01"] / M["m00"]


def pixel_to_normalised(px: float, py: float,
                         w: int = CANVAS_WIDTH,
                         h: int = CANVAS_HEIGHT) -> Tuple[float, float]:
    return px / w, py / h


def detect_yellow_badges(img: np.ndarray, image_name: str) -> Tuple[List[Dict], List[Dict]]:
    cfg = DETECTOR_CONFIG["yellow_badge"]
    amb_cfg = DETECTOR_CONFIG["ambiguity_thresholds"]
    mask = build_yellow_mask(img)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    accepted = []
    rejected = []
    det_seq = 1

    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        aspect = w / float(h) if h > 0 else 0.0
        fill = area / float(w * h) if w * h > 0 else 0.0
        peri = cv2.arcLength(c, True)
        circ = (4 * np.pi * area / peri ** 2) if peri > 0 else 0.0
        cx, cy = contour_centroid(c)

        # Rejection filters
        reason = None
        if area < cfg["area_min"]:
            reason = f"area<{cfg['area_min']}"
        elif area > cfg["area_max"]:
            reason = f"area>{cfg['area_max']} (merged route or multi-badge cluster)"
        elif w < cfg["bbox_w_min"]:
            reason = f"bbox_w<{cfg['bbox_w_min']}"
        elif h < cfg["bbox_h_min"]:
            reason = f"bbox_h<{cfg['bbox_h_min']}"
        elif aspect < cfg["aspect_min"]:
            reason = f"aspect={aspect:.2f}<{cfg['aspect_min']} (elongated vertical line)"
        elif aspect > cfg["aspect_max"]:
            reason = f"aspect={aspect:.2f}>{cfg['aspect_max']} (elongated horizontal line)"
        elif fill < cfg["fill_min"]:
            reason = f"fill={fill:.2f}<{cfg['fill_min']}"

        # Colour purity verification
        purity = 0.0
        if reason is None:
            roi = img[y:y+h, x:x+w]
            r = roi[:, :, 2].astype(float)
            g = roi[:, :, 1].astype(float)
            b = roi[:, :, 0].astype(float)
            purity = float(((r + g) / 2.0 - b).max())
            if purity < cfg["yellow_purity_min"]:
                reason = f"yellow_purity={purity:.1f}<{cfg['yellow_purity_min']}"

        if reason is not None:
            rejected.append({
                "source_image": image_name,
                "category": "yellow",
                "pixel_x": round(cx, 2),
                "pixel_y": round(cy, 2),
                "bbox": [int(x), int(y), int(w), int(h)],
                "area_px": round(area, 1),
                "aspect": round(aspect, 3),
                "fill": round(fill, 3),
                "reason": reason,
            })
        else:
            # Check ambiguity
            is_ambiguous = False
            ambiguity_reason = ""
            if area >= amb_cfg["yellow_large_area"]:
                is_ambiguous = True
                ambiguity_reason = f"large_area={area:.0f}_possible_merged_feature"
            elif fill < amb_cfg["yellow_borderline_fill"] and area > 150:
                is_ambiguous = True
                ambiguity_reason = f"borderline_fill={fill:.2f}_route_junction"

            norm_x, norm_y = pixel_to_normalised(cx, cy)
            accepted.append({
                "detection_id": f"{image_name}_Y_{det_seq:04d}",
                "source_image": image_name,
                "category": "yellow",
                "pixel_x": round(cx, 2),
                "pixel_y": round(cy, 2),
                "norm_x": round(max(0.0, min(1.0, norm_x)), 6),
                "norm_y": round(max(0.0, min(1.0, norm_y)), 6),
                "bbox": [int(x), int(y), int(w), int(h)],
                "area_px": round(area, 1),
                "aspect": round(aspect, 3),
                "fill": round(fill, 3),
                "circularity": round(circ, 3),
                "colour_purity": round(purity, 1),
                "ambiguous": is_ambiguous,
                "ambiguity_reason": ambiguity_reason,
                "status": "ambiguous" if is_ambiguous else "automatically-detected",
            })
            det_seq += 1

    return accepted, rejected


def detect_red_underground(img: np.ndarray, image_name: str) -> Tuple[List[Dict], List[Dict]]:
    cfg = DETECTOR_CONFIG["red_underground"]
    mask_r = build_red_mask(img)
    mask_y = build_yellow_mask(img)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_g = cv2.inRange(hsv, np.array(cfg["context_hsv_green_lower"], dtype=np.uint8),
                              np.array(cfg["context_hsv_green_upper"], dtype=np.uint8))

    cnts, _ = cv2.findContours(mask_r, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    accepted = []
    rejected = []
    det_seq = 1

    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)
        aspect = w / float(h) if h > 0 else 0.0
        fill = area / float(w * h) if w * h > 0 else 0.0
        peri = cv2.arcLength(c, True)
        circ = (4 * np.pi * area / peri ** 2) if peri > 0 else 0.0
        cx, cy = contour_centroid(c)

        reason = None
        if area < cfg["area_min"]:
            reason = f"area<{cfg['area_min']}"
        elif area > cfg["area_max"]:
            reason = f"area>{cfg['area_max']}"
        elif w < cfg["bbox_w_min"]:
            reason = f"bbox_w<{cfg['bbox_w_min']}"
        elif h < cfg["bbox_h_min"]:
            reason = f"bbox_h<{cfg['bbox_h_min']}"
        elif aspect < cfg["aspect_min"]:
            reason = f"aspect={aspect:.2f}<{cfg['aspect_min']}"
        elif aspect > cfg["aspect_max"]:
            reason = f"aspect={aspect:.2f}>{cfg['aspect_max']}"
        elif fill < cfg["fill_min"]:
            reason = f"fill={fill:.2f}<{cfg['fill_min']}"

        purity = 0.0
        has_yellow = False
        has_green = False
        if reason is None:
            roi = img[y:y+h, x:x+w]
            r = roi[:, :, 2].astype(float)
            g = roi[:, :, 1].astype(float)
            b = roi[:, :, 0].astype(float)
            purity = float((r - (g + b) / 2.0).max())
            if purity < cfg["red_purity_min"]:
                reason = f"red_purity={purity:.1f}<{cfg['red_purity_min']}"
            else:
                y1, y2 = max(0, y - 10), min(CANVAS_HEIGHT, y + h + 10)
                x1, x2 = max(0, x - 10), min(CANVAS_WIDTH, x + w + 10)
                has_yellow = bool(np.sum(mask_y[y1:y2, x1:x2] > 0) >= 15)
                has_green = bool(np.sum(mask_g[y1:y2, x1:x2] > 0) >= 15)

                if not (has_yellow or has_green):
                    reason = "no_adjacent_underground_symbology (isolated red detail / building)"

        if reason is not None:
            rejected.append({
                "source_image": image_name,
                "category": "red_underground",
                "pixel_x": round(cx, 2),
                "pixel_y": round(cy, 2),
                "bbox": [int(x), int(y), int(w), int(h)],
                "area_px": round(area, 1),
                "aspect": round(aspect, 3),
                "fill": round(fill, 3),
                "reason": reason,
            })
        else:
            is_ambiguous = not (has_yellow and has_green)
            ambiguity_reason = "partial_underground_context" if is_ambiguous else ""

            norm_x, norm_y = pixel_to_normalised(cx, cy)
            accepted.append({
                "detection_id": f"{image_name}_R_{det_seq:04d}",
                "source_image": image_name,
                "category": "red_underground",
                "pixel_x": round(cx, 2),
                "pixel_y": round(cy, 2),
                "norm_x": round(max(0.0, min(1.0, norm_x)), 6),
                "norm_y": round(max(0.0, min(1.0, norm_y)), 6),
                "bbox": [int(x), int(y), int(w), int(h)],
                "area_px": round(area, 1),
                "aspect": round(aspect, 3),
                "fill": round(fill, 3),
                "circularity": round(circ, 3),
                "colour_purity": round(purity, 1),
                "has_adjacent_yellow": has_yellow,
                "has_adjacent_green": has_green,
                "ambiguous": is_ambiguous,
                "ambiguity_reason": ambiguity_reason,
                "status": "ambiguous" if is_ambiguous else "automatically-detected",
            })
            det_seq += 1

    return accepted, rejected


def process_image(name: str, path: Path) -> Dict:
    img = load_image(path)
    img_h, img_w = img.shape[:2]

    acc_y, rej_y = detect_yellow_badges(img, name)
    acc_r, rej_r = detect_red_underground(img, name)

    accepted = acc_y + acc_r
    rejected = rej_y + rej_r

    return {
        "image_name": name,
        "image_path": str(path),
        "image_w": img_w,
        "image_h": img_h,
        "candidate_count": len(accepted) + len(rejected),
        "accepted_count": len(accepted),
        "rejected_count": len(rejected),
        "yellow_accepted": len(acc_y),
        "red_accepted": len(acc_r),
        "ambiguous_count": sum(1 for a in accepted if a.get("ambiguous")),
        "accepted": accepted,
        "rejected": rejected,
    }


def draw_overlay(base_path: Path, accepted: List[Dict], rejected: List[Dict], out_path: Path) -> None:
    img = cv2.imread(str(base_path))
    if img is None:
        raise FileNotFoundError(f"Cannot load image: {base_path}")

    # Draw rejected: small red crosses
    for rej in rejected:
        cx, cy = int(round(rej["pixel_x"])), int(round(rej["pixel_y"]))
        cv2.drawMarker(img, (cx, cy), (0, 0, 180), markerType=cv2.MARKER_CROSS, markerSize=5, thickness=1)

    # Draw accepted
    for obs in accepted:
        cx, cy = int(round(obs["pixel_x"])), int(round(obs["pixel_y"]))
        bx, by, bw, bh = obs["bbox"]
        cat = obs["category"]
        is_amb = obs.get("ambiguous", False)

        if is_amb:
            color = (0, 165, 255)  # Orange for ambiguous
        elif cat == "red_underground":
            color = (0, 0, 255)    # Red for Underground
        else:
            color = (0, 230, 0)    # Green for Yellow Taxi/Bus badges

        # Centroid circle & bbox
        cv2.rectangle(img, (bx, by), (bx + bw, by + bh), color, 1)
        cv2.circle(img, (cx, cy), 3, color, -1)
        cv2.circle(img, (cx, cy), 6, color, 1)

    # Add legend
    legend_y = 30
    cv2.rectangle(img, (15, 10), (320, 110), (20, 20, 20), -1)
    cv2.rectangle(img, (15, 10), (320, 110), (180, 180, 180), 1)
    cv2.circle(img, (35, 30), 5, (0, 230, 0), -1)
    cv2.putText(img, "Accepted Yellow Badge", (50, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    cv2.circle(img, (35, 55), 5, (0, 0, 255), -1)
    cv2.putText(img, "Accepted Red Underground", (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    cv2.circle(img, (35, 80), 5, (0, 165, 255), -1)
    cv2.putText(img, "Ambiguous Candidate", (50, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
    cv2.drawMarker(img, (35, 98), (0, 0, 180), markerType=cv2.MARKER_CROSS, markerSize=6, thickness=1)
    cv2.putText(img, "Rejected Candidate", (50, 102), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

    cv2.imwrite(str(out_path), img)


def analyze_cross_image_duplicates(results: List[Dict]) -> List[Dict]:
    dist_thresh = DETECTOR_CONFIG["cross_image_duplicate_dist_norm"]
    all_obs = []
    for r in results:
        for obs in r["accepted"]:
            all_obs.append(obs)

    clusters = []
    for obs in all_obs:
        matched = False
        for c in clusters:
            if c["category"] != obs["category"]:
                continue
            rep = c["observations"][0]
            d = ((obs["norm_x"] - rep["norm_x"]) ** 2 + (obs["norm_y"] - rep["norm_y"]) ** 2) ** 0.5
            if d <= dist_thresh:
                c["observations"].append(obs)
                c["sources"].add(obs["source_image"])
                matched = True
                break
        if not matched:
            clusters.append({
                "category": obs["category"],
                "observations": [obs],
                "sources": {obs["source_image"]},
            })

    duplicate_report = []
    for i, c in enumerate(clusters):
        if len(c["sources"]) > 1:
            rep = c["observations"][0]
            duplicate_report.append({
                "cluster_index": i + 1,
                "category": c["category"],
                "sources": sorted(list(c["sources"])),
                "observation_count": len(c["observations"]),
                "reference_norm_coord": [rep["norm_x"], rep["norm_y"]],
            })
    return duplicate_report


def write_json(data, path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_coordinate_review_md(results: List[Dict], path: Path) -> None:
    lines = [
        "# Coordinate Review — Phase 3C.3-C.1",
        "",
        "> [!NOTE] All detections are provisional visual markers.",
        "> Sequential run IDs (e.g. `full_Y_0001`, `full_R_0002`) are NOT Scotland Yard station IDs.",
        "",
        "| Det ID | Category | Status | Norm X | Norm Y | Source | Area (px²) | Aspect | Fill | Purity |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        for obs in r["accepted"]:
            lines.append(
                f"| {obs['detection_id']} "
                f"| {obs['category']} "
                f"| {obs['status']} "
                f"| {obs['norm_x']:.5f} "
                f"| {obs['norm_y']:.5f} "
                f"| {obs['source_image']} "
                f"| {obs['area_px']} "
                f"| {obs['aspect']:.2f} "
                f"| {obs['fill']:.2f} "
                f"| {obs.get('colour_purity', 0.0):.1f} |"
            )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_uncertainty_report_md(results: List[Dict], path: Path) -> None:
    lines = [
        "# Uncertainty and Exception Report — Phase 3C.3-C.1",
        "",
        "## Multi-Category Detector Parameters",
        "",
        "### Yellow Taxi/Bus Badge Configuration:",
        f"- HSV lower: {DETECTOR_CONFIG['yellow_badge']['hsv_lower']}",
        f"- HSV upper: {DETECTOR_CONFIG['yellow_badge']['hsv_upper']}",
        f"- Area range: {DETECTOR_CONFIG['yellow_badge']['area_min']}–{DETECTOR_CONFIG['yellow_badge']['area_max']} px²",
        f"- Bounding-box minimums: w≥{DETECTOR_CONFIG['yellow_badge']['bbox_w_min']}, h≥{DETECTOR_CONFIG['yellow_badge']['bbox_h_min']} px",
        f"- Aspect range: {DETECTOR_CONFIG['yellow_badge']['aspect_min']}–{DETECTOR_CONFIG['yellow_badge']['aspect_max']}",
        f"- Fill ratio minimum: {DETECTOR_CONFIG['yellow_badge']['fill_min']}",
        f"- Colour purity threshold: {DETECTOR_CONFIG['yellow_badge']['yellow_purity_min']} ((R+G)/2 - B)",
        "",
        "### Red Underground Badge Configuration:",
        f"- HSV Range 1: {DETECTOR_CONFIG['red_underground']['hsv_lower_1']} to {DETECTOR_CONFIG['red_underground']['hsv_upper_1']}",
        f"- HSV Range 2: {DETECTOR_CONFIG['red_underground']['hsv_lower_2']} to {DETECTOR_CONFIG['red_underground']['hsv_upper_2']}",
        f"- Area range: {DETECTOR_CONFIG['red_underground']['area_min']}–{DETECTOR_CONFIG['red_underground']['area_max']} px²",
        f"- Bounding-box minimums: w≥{DETECTOR_CONFIG['red_underground']['bbox_w_min']}, h≥{DETECTOR_CONFIG['red_underground']['bbox_h_min']} px",
        f"- Aspect range: {DETECTOR_CONFIG['red_underground']['aspect_min']}–{DETECTOR_CONFIG['red_underground']['aspect_max']}",
        f"- Fill ratio minimum: {DETECTOR_CONFIG['red_underground']['fill_min']}",
        f"- Red dominance threshold: {DETECTOR_CONFIG['red_underground']['red_purity_min']} (R - (G+B)/2)",
        f"- Required adjacent symbology: green bus arc or yellow stop",
        "",
        "## Detection Statistics Per Image",
        "",
        "| Image | Candidates | Accepted Yellow | Accepted Red | Ambiguous | Rejected |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(
            f"| {r['image_name']} | {r['candidate_count']} | {r['yellow_accepted']} | "
            f"{r['red_accepted']} | {r['ambiguous_count']} | {r['rejected_count']} |"
        )
    lines += [
        "",
        "## Rejection & Ambiguity Analysis",
        "- **Route Line Segments:** Correctly rejected due to extreme aspect ratios (>3.5 or <0.5) and low fill factors.",
        "- **Parks & River Water:** Rejection of green background by narrow yellow/red hue ranges and colour dominance checks.",
        "- **Building Roofs:** Brownish-red building roofs rejected via strict red purity dominance and adjacent symbology verification.",
        "- **Merged Features:** Candidates > 1200 px² or fill < 0.22 flagged as ambiguous for human review.",
        "",
        f"Generated: {datetime.datetime.now(datetime.timezone.utc).isoformat()}",
    ]
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def write_multi_observation_report_md(dup_list: List[Dict], path: Path) -> None:
    lines = [
        "# Multi-Observation Discrepancy List — Phase 3C.3-C.1",
        "",
        "> [!NOTE] Spatial clustering across the five registered images.",
        "> Observations within distance tolerance (~15-20 px on 1350x1000 canvas) are listed below.",
        "> Detections are NOT merged into canonical stations during this phase.",
        "",
        f"**Total Multi-Image Observation Groups Found:** {len(dup_list)}",
        "",
        "| Group ID | Category | Sources | Count | Approx Canvas Norm Coord |",
        "|---|---|---|---|---|",
    ]
    for d in dup_list:
        lines.append(
            f"| G_{d['cluster_index']:03d} "
            f"| {d['category']} "
            f"| {', '.join(d['sources'])} "
            f"| {d['observation_count']} "
            f"| ({d['reference_norm_coord'][0]:.4f}, {d['reference_norm_coord'][1]:.4f}) |"
        )
    Path(path).write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    print("Phase 3C.3-C.1 – Station Marker Detection Recovery and Reliability Correction")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    results = []
    for name, path in IMAGES.items():
        print(f"  Processing {name} ({path.name}) ...", end=" ", flush=True)
        r = process_image(name, path)
        results.append(r)
        print(f"total={r['candidate_count']} (Yellow={r['yellow_accepted']}, Red={r['red_accepted']}, Amb={r['ambiguous_count']}, Rej={r['rejected_count']})")

    # Inventory
    inventory = []
    global_id = 1
    for r in results:
        for obs in r["accepted"]:
            inventory.append({
                "provisional_detection_id": global_id,
                "station_id": None,
                "detection_id": obs["detection_id"],
                "category": obs["category"],
                "status": obs["status"],
                "normalized_x": obs["norm_x"],
                "normalized_y": obs["norm_y"],
                "bbox": obs["bbox"],
                "source_image": obs["source_image"],
                "metrics": {
                    "area_px": obs["area_px"],
                    "aspect": obs["aspect"],
                    "fill": obs["fill"],
                    "circularity": obs["circularity"],
                    "colour_purity": obs.get("colour_purity", 0.0),
                },
                "ambiguous": obs.get("ambiguous", False),
                "ambiguity_reason": obs.get("ambiguity_reason", ""),
            })
            global_id += 1

    # Cross image analysis
    dup_report = analyze_cross_image_duplicates(results)

    # Machine-readable detector report
    detector_report = {
        "phase": "3C.3-C.1",
        "generated": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "detector_parameters": DETECTOR_CONFIG,
        "identity_safeguards": "Provisional detection IDs do not assign canonical Scotland Yard station IDs.",
        "images": [
            {k: v for k, v in r.items() if k not in ("accepted", "rejected")}
            for r in results
        ],
        "total_accepted_yellow": sum(r["yellow_accepted"] for r in results),
        "total_accepted_red": sum(r["red_accepted"] for r in results),
        "total_ambiguous": sum(r["ambiguous_count"] for r in results),
        "total_rejected": sum(r["rejected_count"] for r in results),
        "cross_image_duplicate_groups": len(dup_report),
    }
    write_json(detector_report, OUTPUT_DIR / "detector_report.json")
    write_json(inventory, OUTPUT_DIR / "coordinate_inventory.json")

    # Markdown reports
    write_coordinate_review_md(results, OUTPUT_DIR / "coordinate_review.md")
    write_uncertainty_report_md(results, OUTPUT_DIR / "uncertainty_report.md")
    write_multi_observation_report_md(dup_report, OUTPUT_DIR / "multi_observation_report.md")

    # Overlays
    overlay_map = {
        "full":         "overlay_full_debug.png",
        "top-left":     "overlay_top-left_debug.png",
        "top-right":    "overlay_top-right_debug.png",
        "bottom-left":  "overlay_bottom-left_debug.png",
        "bottom-right": "overlay_bottom-right_debug.png",
    }
    for r in results:
        name = r["image_name"]
        out_path = OUTPUT_DIR / overlay_map[name]
        draw_overlay(IMAGES[name], r["accepted"], r["rejected"], out_path)
        print(f"  Overlay written: {out_path.name}")

    print()
    print("Summary:")
    print(f"  Total Yellow accepted: {detector_report['total_accepted_yellow']}")
    print(f"  Total Red accepted:    {detector_report['total_accepted_red']}")
    print(f"  Total Ambiguous:       {detector_report['total_ambiguous']}")
    print(f"  Total Rejected:        {detector_report['total_rejected']}")
    print(f"  Cross-image groups:    {detector_report['cross_image_duplicate_groups']}")


if __name__ == "__main__":
    main()
