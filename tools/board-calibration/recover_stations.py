"""
recover_stations.py
===================
Phase 3D.1: Complete Physical Station-Node Recovery Workflow

Implements:
1. Atlas Grid association for all regions of the board.
2. Candidate marker inventory building: preserves the existing 138 raw observations
   and 121 reconciled features, and extends the candidate inventory with newly
   recovered physical markers from registered close-ups and atlas tile inspection.
3. Printed Station Identity Reconciliation: audits verified printed numbers
   (e.g., Station 1 Underground, Station 200, Station 199, landmarks) strictly against
   photographic evidence, maintaining unambiguous status distinction.
4. Completeness matrix for 1-199 plus Marker 200.
5. Generation of all Phase 3D.1 visual artifacts:
   - full_board_recovered_candidates_overlay.png
   - full_board_verified_stations_overlay.png
   - clean_numbered_nodes_board.png
   - unresolved_ambiguous_overlay.png
   - discrepancy_completeness_map.png
"""

import sys
import json
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Tuple

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from landmarks import CURATED_LANDMARKS

# Paths
OUTPUT_DIR = _HERE / "output" / "station_recovery"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FULL_IMG_PATH = _HERE / "output" / "rectified_complete.png"
QUAD_IMG_PATHS = {
    "top-left": _HERE / "output" / "registered_top-left.png",
    "top-right": _HERE / "output" / "registered_top-right.png",
    "bottom-left": _HERE / "output" / "registered_bottom-left.png",
    "bottom-right": _HERE / "output" / "registered_bottom-right.png",
}

RECONCILED_JSON_PATH = _HERE / "output" / "coordinate_extraction" / "reconciled_coordinate_inventory.json"
RAW_JSON_PATH = _HERE / "output" / "coordinate_extraction" / "coordinate_inventory.json"
ATLAS_INDEX_PATH = OUTPUT_DIR / "atlas_index.json"

CANVAS_WIDTH = 1350
CANVAS_HEIGHT = 1000


def load_atlas_tiles() -> List[Dict[str, Any]]:
    if not ATLAS_INDEX_PATH.exists():
        raise FileNotFoundError(f"Missing atlas index at {ATLAS_INDEX_PATH}")
    data = json.loads(ATLAS_INDEX_PATH.read_text(encoding="utf-8"))
    return data["tiles"]


def find_containing_tiles(px: float, py: float, tiles: List[Dict[str, Any]]) -> List[str]:
    containing = []
    for t in tiles:
        x1, y1, x2, y2 = t["bounds_canvas_px"]
        if x1 <= px <= x2 and y1 <= py <= y2:
            containing.append(t["tile_id"])
    return containing


def main():
    print("Executing Phase 3D.1 Station Recovery Pipeline...")

    # 1. Load existing data
    raw_obs = json.loads(RAW_JSON_PATH.read_text(encoding="utf-8"))
    reconciled_data = json.loads(RECONCILED_JSON_PATH.read_text(encoding="utf-8"))
    existing_feats = reconciled_data["features"]
    tiles = load_atlas_tiles()

    print(f"Loaded {len(raw_obs)} baseline raw observations and {len(existing_feats)} provisional features.")

    # Load calibrated images
    img_full = cv2.imread(str(FULL_IMG_PATH))
    quad_imgs = {k: cv2.imread(str(p)) for k, p in QUAD_IMG_PATHS.items()}

    # 2. Recover additional physical station candidates from registered close-ups & full board
    existing_coords = [(f["pixel_x"], f["pixel_y"]) for f in existing_feats]

    def is_near_existing(px, py, thresh=16.0):
        for ex, ey in existing_coords:
            if ((ex - px)**2 + (ey - py)**2)**0.5 < thresh:
                return True
        return False

    additional_candidates = []
    add_id = 1

    # Check registered quads and full
    sources_to_check = ["top-left", "top-right", "bottom-left", "bottom-right", "full"]
    for sname in sources_to_check:
        img = img_full if sname == "full" else quad_imgs[sname]
        valid_mask = ((img[:, :, 0] > 12) | (img[:, :, 1] > 12) | (img[:, :, 2] > 12)).astype(np.uint8) * 255
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Yellow mask (relaxed)
        y_mask = cv2.inRange(hsv, np.array([14, 35, 45]), np.array([38, 255, 255]))
        y_mask = cv2.bitwise_and(y_mask, valid_mask)
        ko = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        kc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        y_clean = cv2.morphologyEx(cv2.morphologyEx(y_mask, cv2.MORPH_OPEN, ko), cv2.MORPH_CLOSE, kc)
        cnts_y, _ = cv2.findContours(y_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts_y:
            area = cv2.contourArea(c)
            if 25.0 <= area <= 450.0:
                x, y, w, h = cv2.boundingRect(c)
                aspect = float(w) / max(h, 1)
                peri = cv2.arcLength(c, True)
                circ = 4.0 * np.pi * (area / (peri * peri)) if peri > 0 else 0
                if 0.48 <= aspect <= 2.2 and circ >= 0.18:
                    M = cv2.moments(c)
                    if M["m00"] > 0:
                        cx = M["m10"] / M["m00"]
                        cy = M["m01"] / M["m00"]
                        if 40 < cx < 1310 and 35 < cy < 965:
                            roi = img[max(0, y):min(1000, y+h), max(0, x):min(1350, x+w)]
                            b, g, r_v = np.mean(roi[:, :, 0]), np.mean(roi[:, :, 1]), np.mean(roi[:, :, 2])
                            purity = (r_v + g) / 2.0 - b
                            if purity >= 32.0 and not is_near_existing(cx, cy, thresh=16.0):
                                # Ensure not close to already added additional candidate
                                if not any(((ac["pixel_x"] - cx)**2 + (ac["pixel_y"] - cy)**2)**0.5 < 16.0 for ac in additional_candidates):
                                    additional_candidates.append({
                                        "category": "yellow",
                                        "source_image": sname,
                                        "pixel_x": round(cx, 2),
                                        "pixel_y": round(cy, 2),
                                        "bbox": [x, y, w, h],
                                        "area": round(area, 1),
                                        "aspect": round(aspect, 2),
                                        "circularity": round(circ, 2),
                                        "purity": round(purity, 1),
                                    })
                                    add_id += 1

    print(f"Recovered {len(additional_candidates)} additional high-confidence physical station candidates.")

    # 3. Assemble Complete Physical Marker Candidate Inventory
    # Start with existing 121 features, then append additional candidates
    master_candidates = []

    for f in existing_feats:
        feat_copy = dict(f)
        feat_copy["containing_atlas_tiles"] = find_containing_tiles(f["pixel_x"], f["pixel_y"], tiles)
        feat_copy["inventory_generation"] = "baseline-phase-3c3"
        master_candidates.append(feat_copy)

    next_feat_id = len(existing_feats) + 1
    for ac in additional_candidates:
        nx = round(ac["pixel_x"] / CANVAS_WIDTH, 6)
        ny = round(ac["pixel_y"] / CANVAS_HEIGHT, 6)
        c_tiles = find_containing_tiles(ac["pixel_x"], ac["pixel_y"], tiles)
        new_feat = {
            "provisional_feature_id": f"FEAT_{next_feat_id:04d}",
            "station_id": None,
            "category": ac["category"],
            "status": "provisional-recovered-candidate",
            "derivation": f"atlas-recovered-{ac['source_image']}",
            "normalized_x": nx,
            "normalized_y": ny,
            "pixel_x": ac["pixel_x"],
            "pixel_y": ac["pixel_y"],
            "primary_source": ac["source_image"],
            "contributing_sources": [ac["source_image"]],
            "contributing_detection_ids": [f"rec_{ac['source_image']}_{next_feat_id:04d}"],
            "spatial_discrepancy_px": 0.0,
            "closeup_observations": [],
            "observation_ambiguous": False,
            "ambiguous": False,
            "ambiguity_reason": "",
            "review_note": f"Recovered via atlas tile inspection from {ac['source_image']}. Area={ac['area']}px, Purity={ac['purity']}.",
            "containing_atlas_tiles": c_tiles,
            "inventory_generation": "recovered-phase-3d1",
        }
        master_candidates.append(new_feat)
        next_feat_id += 1

    print(f"Total Physical Marker Candidates in Inventory: {len(master_candidates)}")

    # 4. Printed Station Identity Reconciliation (Task D & E)
    # Match against verified printed landmarks and visual station markers
    # Station 200 is specifically FEAT_0114 at (1151.8, 938.8)
    # Station 199 is specifically FEAT_0115 at (1146.5, 920.7)
    # Station 1 is specifically FEAT_0094 at (187.9, 56.6)

    # Load curated landmarks
    all_landmarks = {}
    for q_name, llist in CURATED_LANDMARKS.items():
        for lm in llist:
            all_landmarks[lm["station_id"]] = lm

    # Assign station identities from printed evidence
    # Identity assignment must be strictly backed by evidence
    station_identities = {}

    # Explicit high-confidence verified assignments
    # Station 1: FEAT_0094
    station_identities[1] = {
        "station_id": 1,
        "feature_id": "FEAT_0094",
        "category": "red_underground",
        "status": "verified",
        "pixel_x": 187.94, "pixel_y": 56.62,
        "evidence_source": "registered_top-left.png & rectified_complete.png",
        "evidence_basis": "Printed red Underground badge with clear '1' text in Regent's Park / St. John's Wood sector.",
        "confidence": "high"
    }

    # Station 199: FEAT_0115
    station_identities[199] = {
        "station_id": 199,
        "feature_id": "FEAT_0115",
        "category": "yellow",
        "status": "verified",
        "pixel_x": 1146.51, "pixel_y": 920.71,
        "evidence_source": "registered_bottom-right.png",
        "evidence_basis": "Printed yellow station marker with legible '199' text adjacent to Lower Thames / border fold.",
        "confidence": "high"
    }

    # Observed Physical Marker 200 (recorded separately, non-canonical)
    marker_200_record = {
        "observed_marker_id": 200,
        "feature_id": "FEAT_0114",
        "category": "yellow",
        "status": "observed-physical-marker-unresolved-playability",
        "pixel_x": 1151.79, "pixel_y": 938.83,
        "normalized_x": round(1151.79 / CANVAS_WIDTH, 6),
        "normalized_y": round(938.83 / CANVAS_HEIGHT, 6),
        "evidence_source": "registered_bottom-right.png & complete.jpeg",
        "evidence_basis": "Clearly printed yellow badge with visible '200' in lower-right margin. Gameplay status deferred per owner decisions.",
        "confidence": "high-physical-presence"
    }

    # Curated landmark associations:
    # Explicit instruction: Only Stations 1 and 199 are verified from printed evidence.
    # The 4 curated landmarks (Stations 3, 120, 123, 158) are classified as 'candidate_uncertain'
    # because their physical markers are present, but their printed numeric labels are not
    # independently optical-grade legible in the current photography without landmark prior inference.
    UNCERTAIN_LANDMARKS = {
        3: {"sid": 3, "feat_id": "FEAT_0080", "name": "Euston Station approach", "cat": "yellow", "px": 423.65, "py": 40.80},
        120: {"sid": 120, "feat_id": "FEAT_0141", "name": "Kensington Gardens North-West", "cat": "yellow", "px": 42.45, "py": 505.97},
        123: {"sid": 123, "feat_id": "FEAT_0122", "name": "The Serpentine / Hyde Park South", "cat": "yellow", "px": 173.53, "py": 508.46},
        158: {"sid": 158, "feat_id": "FEAT_0018", "name": "Lambeth Road", "cat": "yellow", "px": 560.13, "py": 614.25},
    }

    for sid, u_info in UNCERTAIN_LANDMARKS.items():
        station_identities[sid] = {
            "station_id": sid,
            "feature_id": u_info["feat_id"],
            "category": u_info["cat"],
            "status": "candidate_uncertain",
            "pixel_x": u_info["px"],
            "pixel_y": u_info["py"],
            "evidence_source": "calibrated photography & curated landmark correspondence",
            "evidence_basis": f"Physical marker present at {u_info['name']} ({u_info['feat_id']}); printed numeric text requires higher optical resolution to confirm without landmark prior.",
            "confidence": "candidate_uncertain"
        }

    # Build completeness matrix 1-199
    completeness_matrix = []
    matrix_counts = {
        "verified": 0,
        "candidate_uncertain": 0,
        "missing_from_evidence": 0,
        "conflicting": 0,
        "duplicate": 0
    }

    for sid in range(1, 200):
        if sid in station_identities:
            rec = station_identities[sid]
            completeness_matrix.append(rec)
            matrix_counts[rec["status"]] += 1
        else:
            completeness_matrix.append({
                "station_id": sid,
                "feature_id": None,
                "category": None,
                "status": "missing_from_evidence",
                "pixel_x": None,
                "pixel_y": None,
                "evidence_source": None,
                "evidence_basis": "Not resolved with high-confidence printed text reading in current photographic set.",
                "confidence": "unresolved"
            })
            matrix_counts["missing_from_evidence"] += 1

    print("Completeness Matrix 1-199 Summary:")
    print(f"  Verified Station Identities: {matrix_counts['verified']}")
    print(f"  Candidate Uncertain Station Identities: {matrix_counts['candidate_uncertain']}")
    print(f"  Missing / Unresolved from Current Evidence: {matrix_counts['missing_from_evidence']}")
    print(f"  Observed Marker 200: 1 (Recorded separately)")

    # 5. Save candidate marker inventory JSON
    inv_data = {
        "metadata": {
            "phase": "3D.1",
            "title": "Complete Physical Station-Node Recovery Inventory",
            "working_canvas_dimensions": [CANVAS_WIDTH, CANVAS_HEIGHT],
            "total_physical_candidates": len(master_candidates),
            "baseline_reconciled_features_retained": len(existing_feats),
            "recovered_additional_candidates": len(additional_candidates),
            "target_playable_range": "1-199",
            "marker_200_status": "observed-physical-marker-unresolved-playability",
        },
        "observed_marker_200": marker_200_record,
        "physical_marker_candidates": master_candidates,
    }
    inv_path = OUTPUT_DIR / "candidate_marker_inventory.json"
    inv_path.write_text(json.dumps(inv_data, indent=2), encoding="utf-8")
    print(f"Saved: {inv_path.name}")

    # 6. Save Station Identities and Completeness Matrix JSON
    comp_data = {
        "metadata": {
            "phase": "3D.1",
            "title": "Station Identity & Completeness Matrix 1-199",
            "summary_counts": matrix_counts,
            "additional_physical_markers": [marker_200_record],
        },
        "identities_1_to_199": completeness_matrix,
    }
    comp_path = OUTPUT_DIR / "station_identities_matrix.json"
    comp_path.write_text(json.dumps(comp_data, indent=2), encoding="utf-8")
    print(f"Saved: {comp_path.name}")

    # 7. Render Task F Visual Outputs
    print("Rendering Visual Deliverables...")

    # Overlay 1: Full-board overlay of all recovered physical marker candidates
    ov1 = img_full.copy()
    for f in master_candidates:
        cx, cy = int(round(f["pixel_x"])), int(round(f["pixel_y"]))
        is_new = f.get("inventory_generation") == "recovered-phase-3d1"
        col = (255, 140, 0) if is_new else ((0, 0, 220) if f["category"] == "red_underground" else (0, 220, 0))
        cv2.circle(ov1, (cx, cy), 6, col, -1)
        cv2.circle(ov1, (cx, cy), 8, (0, 0, 0), 1)
        if is_new:
            cv2.drawMarker(ov1, (cx, cy), (255, 255, 255), markerType=cv2.MARKER_CROSS, markerSize=6, thickness=1)

    # Legend ov1
    cv2.rectangle(ov1, (15, 15), (420, 115), (20, 20, 20), -1)
    cv2.rectangle(ov1, (15, 15), (420, 115), (200, 200, 200), 1)
    cv2.putText(ov1, "Phase 3D.1: Recovered Physical Station Candidates", (25, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)
    cv2.circle(ov1, (35, 55), 5, (0, 220, 0), -1)
    cv2.putText(ov1, f"Baseline Yellow Marker ({len([f for f in existing_feats if f['category']=='yellow'])})", (55, 59), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (240, 240, 240), 1)
    cv2.circle(ov1, (35, 75), 5, (0, 0, 220), -1)
    cv2.putText(ov1, f"Baseline Red Underground Marker ({len([f for f in existing_feats if f['category']=='red_underground'])})", (55, 79), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (240, 240, 240), 1)
    cv2.circle(ov1, (35, 95), 5, (255, 140, 0), -1)
    cv2.putText(ov1, f"Phase 3D.1 Newly Recovered Candidates ({len(additional_candidates)})", (55, 99), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (240, 240, 240), 1)

    p_ov1 = OUTPUT_DIR / "full_board_recovered_candidates_overlay.png"
    cv2.imwrite(str(p_ov1), ov1)
    print(f"Saved: {p_ov1.name}")

    # Overlay 2: Full-board overlay with verified and candidate station numbers
    ov2 = img_full.copy()
    dimmed2 = cv2.addWeighted(ov2, 0.85, np.zeros_like(ov2), 0.15, 0)
    for sid, rec in station_identities.items():
        cx, cy = int(round(rec["pixel_x"])), int(round(rec["pixel_y"]))
        is_verified = rec["status"] == "verified"
        col = (0, 255, 255) if is_verified else (255, 180, 0) # Cyan/Yellow for verified, Light Orange/Amber for candidate_uncertain
        cv2.circle(dimmed2, (cx, cy), 10, col, -1)
        cv2.circle(dimmed2, (cx, cy), 10, (0, 0, 0), 1)
        # Text label
        lbl = str(sid)
        t_size = cv2.getTextSize(lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)[0]
        cv2.putText(dimmed2, lbl, (cx - t_size[0]//2, cy + t_size[1]//2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 0), 1)

    # Draw Marker 200 with distinct styling
    cx200, cy200 = int(round(marker_200_record["pixel_x"])), int(round(marker_200_record["pixel_y"]))
    cv2.circle(dimmed2, (cx200, cy200), 11, (0, 140, 255), -1)
    cv2.circle(dimmed2, (cx200, cy200), 11, (255, 255, 255), 1)
    cv2.putText(dimmed2, "200", (cx200 - 10, cy200 + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (0, 0, 0), 1)

    # Legend ov2
    cv2.rectangle(dimmed2, (15, 15), (440, 115), (20, 20, 20), -1)
    cv2.rectangle(dimmed2, (15, 15), (440, 115), (200, 200, 200), 1)
    cv2.putText(dimmed2, "Station Identities Status (Evidence-Backed)", (25, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)
    cv2.circle(dimmed2, (35, 55), 7, (0, 255, 255), -1)
    cv2.putText(dimmed2, f"Verified Station Number ({matrix_counts['verified']} nodes: 1, 199)", (55, 59), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (240, 240, 240), 1)
    cv2.circle(dimmed2, (35, 75), 7, (255, 180, 0), -1)
    cv2.putText(dimmed2, f"Candidate Uncertain ({matrix_counts['candidate_uncertain']} nodes: 3, 120, 123, 158)", (55, 79), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (240, 240, 240), 1)
    cv2.circle(dimmed2, (35, 95), 7, (0, 140, 255), -1)
    cv2.putText(dimmed2, "Observed Physical Marker 200 (Playability Deferred)", (55, 99), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (240, 240, 240), 1)

    p_ov2 = OUTPUT_DIR / "full_board_verified_stations_overlay.png"
    cv2.imwrite(str(p_ov2), dimmed2)
    print(f"Saved: {p_ov2.name}")

    # Overlay 3: Clean board view showing all numbered nodes on parchment
    clean = np.full((CANVAS_HEIGHT, CANVAS_WIDTH, 3), (218, 232, 242), dtype=np.uint8)
    # Neatline
    cv2.rectangle(clean, (10, 10), (CANVAS_WIDTH - 10, CANVAS_HEIGHT - 10), (80, 70, 60), 2)

    # Draw soft Thames guide
    hsv_base = cv2.cvtColor(img_full, cv2.COLOR_BGR2HSV)
    b, g, r = img_full[:, :, 0].astype(float), img_full[:, :, 1].astype(float), img_full[:, :, 2].astype(float)
    water_mask = ((b > 115) & (g > 95) & (b > r + 10) & (hsv_base[:, :, 0] >= 85) & (hsv_base[:, :, 0] <= 125)).astype(np.uint8) * 255
    water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    water_mask = cv2.morphologyEx(water_mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))
    water_cnts, _ = cv2.findContours(water_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for wc in water_cnts:
        if cv2.contourArea(wc) > 1200:
            cv2.drawContours(clean, [wc], -1, (215, 195, 170), -1)

    # Draw stations
    for sid, rec in station_identities.items():
        cx, cy = int(round(rec["pixel_x"])), int(round(rec["pixel_y"]))
        is_underground = rec["category"] == "red_underground"
        is_verified = rec["status"] == "verified"
        if is_underground:
            cv2.rectangle(clean, (cx - 10, cy - 8), (cx + 10, cy + 8), (0, 0, 200), -1)
            cv2.rectangle(clean, (cx - 10, cy - 8), (cx + 10, cy + 8), (40, 40, 40), 1)
            txt_col = (255, 255, 255)
        else:
            badge_col = (20, 195, 235) if is_verified else (0, 160, 230) # Warm Gold if verified, Amber if candidate_uncertain
            cv2.circle(clean, (cx, cy), 9, badge_col, -1)
            cv2.circle(clean, (cx, cy), 9, (40, 40, 40), 1)
            txt_col = (0, 0, 0)
        lbl = str(sid)
        t_size = cv2.getTextSize(lbl, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)[0]
        cv2.putText(clean, lbl, (cx - t_size[0]//2, cy + t_size[1]//2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, txt_col, 1)

    # Draw Marker 200
    cv2.circle(clean, (cx200, cy200), 10, (0, 140, 255), -1)
    cv2.circle(clean, (cx200, cy200), 10, (40, 40, 40), 1)
    cv2.putText(clean, "200", (cx200 - 9, cy200 + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.32, (0, 0, 0), 1)

    # Legend clean
    cv2.rectangle(clean, (15, 15), (450, 135), (245, 250, 252), -1)
    cv2.rectangle(clean, (15, 15), (450, 135), (100, 90, 80), 1)
    cv2.putText(clean, "Clean Numbered Station Nodes (Parchment View)", (25, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (30, 30, 30), 1)
    cv2.circle(clean, (32, 50), 6, (20, 195, 235), -1)
    cv2.putText(clean, "Verified Yellow Station (199)", (48, 54), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (40, 40, 40), 1)
    cv2.rectangle(clean, (26, 64), (38, 74), (0, 0, 200), -1)
    cv2.putText(clean, "Verified Red Underground Station (1)", (48, 72), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (40, 40, 40), 1)
    cv2.circle(clean, (32, 85), 6, (0, 160, 230), -1)
    cv2.putText(clean, "Candidate Uncertain (3, 120, 123, 158)", (48, 88), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (40, 40, 40), 1)
    cv2.circle(clean, (32, 105), 6, (0, 140, 255), -1)
    cv2.putText(clean, "Physical Marker 200 (Observed / Unresolved)", (48, 108), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (40, 40, 40), 1)
    cv2.rectangle(clean, (26, 116), (38, 126), (215, 195, 170), -1)
    cv2.putText(clean, "Thames Water Guide (Contextual Only, Not Canonical)", (48, 124), cv2.FONT_HERSHEY_SIMPLEX, 0.33, (70, 70, 70), 1)

    p_clean = OUTPUT_DIR / "clean_numbered_nodes_board.png"
    cv2.imwrite(str(p_clean), clean)
    print(f"Saved: {p_clean.name}")

    # Overlay 4: Separate unresolved / ambiguous marker overlay
    ov4 = img_full.copy()
    dimmed4 = cv2.addWeighted(ov4, 0.70, np.zeros_like(ov4), 0.30, 0)
    for f in master_candidates:
        if f.get("status") in ("ambiguous", "needs-owner-review", "provisional-recovered-candidate") or f.get("ambiguous"):
            cx, cy = int(round(f["pixel_x"])), int(round(f["pixel_y"]))
            cv2.circle(dimmed4, (cx, cy), 9, (0, 140, 255), 2)
            cv2.drawMarker(dimmed4, (cx, cy), (0, 140, 255), markerType=cv2.MARKER_TILTED_CROSS, markerSize=10, thickness=1)
            lbl = f["provisional_feature_id"]
            cv2.putText(dimmed4, lbl, (cx + 8, cy + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.30, (0, 255, 255), 1)

    cv2.rectangle(dimmed4, (15, 15), (420, 75), (20, 20, 20), -1)
    cv2.rectangle(dimmed4, (15, 15), (420, 75), (200, 200, 200), 1)
    cv2.putText(dimmed4, "Unresolved / Ambiguous Physical Markers", (25, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)
    cv2.circle(dimmed4, (35, 55), 6, (0, 140, 255), 2)
    cv2.putText(dimmed4, "Ambiguous / Review Candidate Marker", (55, 59), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (240, 240, 240), 1)

    p_ov4 = OUTPUT_DIR / "unresolved_ambiguous_overlay.png"
    cv2.imwrite(str(p_ov4), dimmed4)
    print(f"Saved: {p_ov4.name}")

    # Overlay 5: Discrepancy Map showing verified vs unassigned candidate clusters
    ov5 = img_full.copy()
    dimmed5 = cv2.addWeighted(ov5, 0.65, np.zeros_like(ov5), 0.35, 0)

    # Draw verified as green circles
    for sid, rec in station_identities.items():
        cx, cy = int(round(rec["pixel_x"])), int(round(rec["pixel_y"]))
        cv2.circle(dimmed5, (cx, cy), 8, (0, 255, 0), -1)
        cv2.circle(dimmed5, (cx, cy), 8, (0, 0, 0), 1)

    # Draw unassigned physical candidates as purple diamonds
    assigned_feat_ids = set(rec["feature_id"] for rec in station_identities.values())
    for f in master_candidates:
        if f["provisional_feature_id"] not in assigned_feat_ids and f["provisional_feature_id"] != "FEAT_0114":
            cx, cy = int(round(f["pixel_x"])), int(round(f["pixel_y"]))
            cv2.drawMarker(dimmed5, (cx, cy), (255, 0, 255), markerType=cv2.MARKER_DIAMOND, markerSize=10, thickness=2)

    cv2.rectangle(dimmed5, (15, 15), (450, 95), (20, 20, 20), -1)
    cv2.rectangle(dimmed5, (15, 15), (450, 95), (200, 200, 200), 1)
    cv2.putText(dimmed5, "Phase 3D.1 Completeness & Discrepancy Map", (25, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1)
    cv2.circle(dimmed5, (35, 55), 6, (0, 255, 0), -1)
    cv2.putText(dimmed5, f"Verified Station Identity ({matrix_counts['verified']} nodes)", (55, 59), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (240, 240, 240), 1)
    cv2.drawMarker(dimmed5, (35, 75), (255, 0, 255), markerType=cv2.MARKER_DIAMOND, markerSize=8, thickness=2)
    cv2.putText(dimmed5, f"Unassigned Physical Candidate ({len(master_candidates) - len(assigned_feat_ids)} nodes)", (55, 79), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (240, 240, 240), 1)

    p_ov5 = OUTPUT_DIR / "discrepancy_completeness_map.png"
    cv2.imwrite(str(p_ov5), dimmed5)
    print(f"Saved: {p_ov5.name}")

    print("Phase 3D.1 Recovery Script Completed Successfully!")


if __name__ == "__main__":
    main()
