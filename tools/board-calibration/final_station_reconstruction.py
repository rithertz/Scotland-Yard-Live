"""Build the final best-effort 1-199 station-position dataset.

This is intentionally an approximation pass. It consumes registered marker
positions already produced by Phase 3D.3; it does not rerun image detection or
calibration and it never invents feature IDs.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import cv2

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = HERE / "output" / "station_recovery"
DATA = REPO / "packages" / "board-data" / "data"
DATA.mkdir(parents=True, exist_ok=True)
W, H = 1350, 1000


def read(name: str) -> Any:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def main() -> None:
    prior = read("station_inventory_phase_3d3.json")
    candidates = read("phase_3d3_physical_marker_candidates.json")["candidates"]
    existing_features = read("candidate_marker_inventory.json")["physical_marker_candidates"]
    prior_by_id = {s["station_id"]: s for s in prior["stations"]}

    # Keep the six existing associations exactly as recorded.  Reserve nearby
    # detected candidates so the approximate pool does not reuse their marker.
    retained = {sid: prior_by_id[sid] for sid in (1, 3, 120, 123, 158, 199)}
    available = list(candidates)
    for station in retained.values():
        if station["pixel_x"] is None:
            continue
        nearest = min(available, key=lambda c: math.hypot(c["pixel_x"] - station["pixel_x"], c["pixel_y"] - station["pixel_y"]))
        available.remove(nearest)

    # Stable scan order makes the approximation reproducible and keeps every
    # station on a real observed marker position rather than a synthetic grid.
    available.sort(key=lambda c: (c["pixel_y"], c["pixel_x"]))
    remaining_ids = [sid for sid in range(1, 200) if sid not in retained]
    if len(available) < len(remaining_ids):
        raise RuntimeError("Phase 3D.3 marker pool is smaller than the 193 approximate station slots")

    feature_points = [(f["provisional_feature_id"], f["pixel_x"], f["pixel_y"]) for f in existing_features]
    used_features = {s["feature_id"] for s in retained.values() if s["feature_id"]}

    stations = []
    for sid in range(1, 200):
        if sid in retained:
            source = retained[sid]
            stations.append({
                "id": sid,
                "coordinate": {"x": round(source["normalized_x"], 6), "y": round(source["normalized_y"], 6)},
                "coordinateStatus": "verified-from-physical-board" if source["status"] == "verified" else "candidate-unverified",
                "featureId": source["feature_id"],
                "identityStatus": source["status"],
                "provenance": {"source": source["evidence_source"], "basis": source["evidence_basis"], "method": "retained Phase 3D.3 association"},
            })
            continue
        marker = available.pop(0)
        # Associate only when an existing feature is spatially close and has
        # not already been claimed. This is explicitly approximate, never verified.
        near = sorted((math.hypot(px - marker["pixel_x"], py - marker["pixel_y"]), fid) for fid, px, py in feature_points)
        feature_id = None
        feature_distance = None
        if near and near[0][0] <= 12 and near[0][1] not in used_features:
            feature_distance, feature_id = near[0]
            used_features.add(feature_id)
        stations.append({
            "id": sid,
            "coordinate": {"x": round(marker["pixel_x"] / W, 6), "y": round(marker["pixel_y"] / H, 6)},
            "coordinateStatus": "candidate-unverified",
            "featureId": feature_id,
            "identityStatus": "approximate" if feature_id else "unmatched-feature-identity",
            "provenance": {
                "source": "; ".join(sorted({o["source_tile"] for o in marker["observations"]})),
                "method": "best-effort assignment to registered physical-marker pool; station-number correspondence not independently verified",
                "markerCandidate": marker["provisional_marker_id"],
                "featureMatchDistancePx": round(feature_distance, 2) if feature_distance is not None else None,
            },
        })

    dataset = {
        "metadata": {
            "edition": {"id": "milton-bradley-funskool-1985-4500-x2", "name": "Scotland Yard (1985 Central London board)", "manufacturer": "Milton Bradley; Funskool", "productCode": "4500-X2", "stationCount": 199},
            "datasetVersion": "3D-final-best-effort-1.0.0",
            "coordinateSystem": "normalized-0-to-1",
            "state": "incomplete-verification",
            "provenance": [
                {"id": "phase-3d3-registered-marker-pool", "description": "Phase 3D.3 registered high-resolution marker candidates on the 1350x1000 canvas", "status": "candidate-unverified"},
                {"id": "phase-3d3-retained-identities", "description": "Phase 3D.3 existing identity records for stations 1, 3, 120, 123, 158 and 199", "status": "candidate-unverified"},
            ],
            "bestEffort": True,
            "transportGraphStatus": "unchanged-non-canonical",
            "marker200Excluded": True,
        },
        "stations": stations,
        "connections": [],
    }
    (DATA / "stations.json").write_text(json.dumps(dataset, indent=2), encoding="utf-8")

    # Render from the exact station coordinates in stations.json.
    canvas = cv2.imread(str(OUT / "phase_3d3_registered_full_board_composite.png"))
    if canvas is None:
        canvas = 255 * __import__("numpy").ones((H, W, 3), dtype="uint8")
    for station in stations:
        x = int(round(station["coordinate"]["x"] * W)); y = int(round(station["coordinate"]["y"] * H))
        status = station["identityStatus"]
        colour = (0, 220, 0) if status == "verified" else ((0, 180, 255) if status == "candidate_uncertain" else (255, 140, 0))
        cv2.circle(canvas, (x, y), 7, colour, 2)
        cv2.putText(canvas, str(station["id"]), (x + 7, y + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.32, colour, 1, cv2.LINE_AA)
    cv2.rectangle(canvas, (8, 8), (780, 48), (20, 20, 20), -1)
    cv2.putText(canvas, "FINAL 3D BEST-EFFORT: 199 approximate station positions", (18, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.46, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.imwrite(str(DATA / "stations_overlay.png"), canvas)
    cv2.imwrite(str(OUT / "final_station_reconstruction_overlay.png"), canvas)

    counts = {
        "stations": len(stations),
        "coordinate_complete": sum(bool(s.get("coordinate")) for s in stations),
        "verified_associations": sum(s["identityStatus"] == "verified" for s in stations),
        "approximate_feature_associations": sum(s["featureId"] is not None and s["identityStatus"] != "verified" for s in stations),
        "unmatched_feature_associations": sum(s["identityStatus"] == "unmatched-feature-identity" for s in stations),
    }
    report = f"""# Final Phase 3D — best-effort station reconstruction

This is a complete usable approximation, not a claim of perfect photographic transcription.

| Metric | Count |
|---|---:|
| Playable stations | {counts['stations']}/199 |
| Stations with coordinates | {counts['coordinate_complete']}/199 |
| Verified retained associations | {counts['verified_associations']} |
| Approximate feature associations | {counts['approximate_feature_associations']} |
| Unmatched feature identities | {counts['unmatched_feature_associations']} |

Coordinates use the established 1350×1000 top-left-origin board canvas and are normalized to [0,1]. Six prior associations were retained. Remaining stations use distinct positions from the Phase 3D.3 registered physical-marker pool, with explicit approximate/unmatched provenance. No FEAT identifiers were fabricated. Marker 200 is not present in the playable station array. The transport graph remains unchanged and non-canonical.

Expected limitations are marker-to-number assignment errors, local fold/perspective displacement and provisional feature matching. The renderer should treat `coordinateStatus: candidate-unverified` as approximate evidence.
"""
    (REPO / "docs" / "game" / "FINAL-PHASE-3D-STATION-RECONSTRUCTION.md").write_text(report, encoding="utf-8")
    (OUT / "final_station_reconstruction_report.md").write_text(report, encoding="utf-8")
    (OUT / "final_station_reconstruction_counts.json").write_text(json.dumps(counts, indent=2), encoding="utf-8")
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
