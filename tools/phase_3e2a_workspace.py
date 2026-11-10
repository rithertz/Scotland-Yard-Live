"""Generate the Phase 3E.2A transport reconstruction review workspace."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

import cv2
import numpy as np

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "game" / "data" / "phase-3e2a-workspace"
CROPS = OUT / "station-crops"
OUT.mkdir(parents=True, exist_ok=True)
CROPS.mkdir(parents=True, exist_ok=True)
BOARD_W, BOARD_H = 1350, 1000
CROP_SIZE = 220
TILE_DIR = REPO / "tools" / "board-calibration" / "output" / "station_recovery" / "phase_3d3_registered_tiles"
REG_META = REPO / "tools" / "board-calibration" / "output" / "station_recovery" / "phase_3d3_registration_metadata.json"
STATION_PATH = REPO / "packages" / "board-data" / "data" / "stations.json"
CANDIDATE_PATH = REPO / "docs" / "game" / "data" / "board-edge-candidates-1-200.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def inside_polygon(point: tuple[float, float], polygon: np.ndarray) -> bool:
    return cv2.pointPolygonTest(polygon.astype(np.float32), point, False) >= 0


def source_inventory() -> list[dict[str, Any]]:
    root = REPO / "docs" / "game" / "evidence" / "board-photos"
    records = []
    for folder, pattern, role in (("original-references", "*.jpeg", "original board photograph"), ("closeups", "*.jpg", "close-up board photograph"), ("high-resolution", "*.jpg", "high-resolution board tile")):
        for path in sorted((root / folder).glob(pattern)):
            image = cv2.imread(str(path), cv2.IMREAD_COLOR)
            records.append({"sourceId": path.name, "path": str(path.relative_to(REPO)), "role": role, "exists": True, "readable": image is not None,
                            "dimensions": [int(image.shape[1]), int(image.shape[0])] if image is not None else None, "sha256": sha256(path)})
    for path in (REPO / "tools" / "board-calibration" / "output").glob("rectified_complete.png"):
        image = cv2.imread(str(path), cv2.IMREAD_COLOR)
        records.append({"sourceId": path.name, "path": str(path.relative_to(REPO)), "role": "derived rectified board reference", "exists": True, "readable": image is not None,
                        "dimensions": [int(image.shape[1]), int(image.shape[0])] if image is not None else None, "sha256": sha256(path)})
    return records


def choose_tile(point: tuple[float, float], registrations: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates = []
    for registration in registrations:
        image = cv2.imread(str(REPO / "tools" / "board-calibration" / "output" / "station_recovery" / "phase_3d3_registered_tiles" / registration["filename"].replace(".jpg", ".png")))
        if image is None:
            continue
        h, w = image.shape[:2]
        H = np.asarray(registration["homography_source_to_canvas"], dtype=np.float64)
        corners = cv2.perspectiveTransform(np.float32([[[0, 0], [w, 0], [w, h], [0, h]]]), H)[0]
        if inside_polygon(point, corners):
            candidates.append((registration["inliers"], registration, H, corners))
    return max(candidates, key=lambda item: item[0])[1] if candidates else None


def perspective_crop(original: np.ndarray, H: np.ndarray, cx: float, cy: float, size: int) -> tuple[np.ndarray, list[float]]:
    half = size / 2
    board_corners = np.float32([[[cx - half, cy - half], [cx + half, cy - half], [cx + half, cy + half], [cx - half, cy + half]]])
    source_corners = cv2.perspectiveTransform(board_corners, np.linalg.inv(H))[0]
    target = np.float32([[0, 0], [size - 1, 0], [size - 1, size - 1], [0, size - 1]])
    transform = cv2.getPerspectiveTransform(source_corners.astype(np.float32), target)
    crop = cv2.warpPerspective(original, transform, (size, size), flags=cv2.INTER_LINEAR)
    return crop, [float(v) for point in source_corners for v in point]


def main() -> None:
    station_bytes = STATION_PATH.read_bytes()
    candidate_bytes = CANDIDATE_PATH.read_bytes()
    station_data = json.loads(station_bytes)
    candidate_data = json.loads(candidate_bytes)
    assert len(station_data["stations"]) == 199
    assert [s["id"] for s in station_data["stations"]] == list(range(1, 200))
    assert len(candidate_data["edges"]) == 125
    registrations = json.loads(REG_META.read_text(encoding="utf-8"))["registrations"]
    edges = candidate_data["edges"]
    incident = {sid: [] for sid in range(1, 200)}
    for edge in edges:
        incident[edge["from"]].append(edge["edgeId"])
        if edge["to"] <= 199:
            incident[edge["to"]].append(edge["edgeId"])

    sources = source_inventory()
    source_by_id = {s["sourceId"]: s for s in sources}
    queue = []
    crop_records = []
    for station in station_data["stations"]:
        sid = station["id"]
        cx = station["coordinate"]["x"] * BOARD_W
        cy = station["coordinate"]["y"] * BOARD_H
        tile = choose_tile((cx, cy), registrations)
        fold = abs(cx - BOARD_W / 2) <= 45 or abs(cy - BOARD_H / 2) <= 45
        boundary = cx < 70 or cy < 70 or cx > BOARD_W - 70 or cy > BOARD_H - 70
        source_tile = tile["filename"] if tile else "rectified_complete.png"
        registered_path = TILE_DIR / source_tile.replace(".jpg", ".png") if tile else REPO / "tools" / "board-calibration" / "output" / "rectified_complete.png"
        registered = cv2.imread(str(registered_path), cv2.IMREAD_COLOR)
        if registered is None:
            raise RuntimeError(f"Missing registered crop source for station {sid}: {registered_path}")
        x1, y1 = max(0, int(round(cx - CROP_SIZE / 2))), max(0, int(round(cy - CROP_SIZE / 2)))
        x2, y2 = min(BOARD_W, x1 + CROP_SIZE), min(BOARD_H, y1 + CROP_SIZE)
        x1, y1 = max(0, x2 - CROP_SIZE), max(0, y2 - CROP_SIZE)
        registered_crop = registered[y1:y2, x1:x2]
        crop_id = f"ST-{sid:03d}"
        registered_name = f"{crop_id}-registered.png"
        cv2.imwrite(str(CROPS / registered_name), registered_crop)
        source_pixel_corners = None
        source_file = None
        source_crop_name = None
        if tile:
            source_file = tile["filename"]
            original_path = REPO / "docs" / "game" / "evidence" / "board-photos" / "high-resolution" / source_file
            original = cv2.imread(str(original_path), cv2.IMREAD_COLOR)
            H = np.asarray(tile["homography_source_to_canvas"], dtype=np.float64)
            source_crop, source_pixel_corners = perspective_crop(original, H, cx, cy, CROP_SIZE)
            source_crop_name = f"{crop_id}-source.png"
            cv2.imwrite(str(CROPS / source_crop_name), source_crop)
        else:
            source_file = "rectified_complete.png"
        crop_records.append({"cropId": crop_id, "stationId": sid, "sourceImage": source_file, "registeredImage": str(registered_path.relative_to(REPO)),
                             "registeredCropPath": str((CROPS / registered_name).relative_to(REPO)), "sourceCropPath": str((CROPS / source_crop_name).relative_to(REPO)) if source_crop_name else None,
                             "registeredCanvasCrop": {"x": x1, "y": y1, "width": x2 - x1, "height": y2 - y1},
                             "sourcePixelCorners": source_pixel_corners, "registeredCanvasCentre": [round(cx, 2), round(cy, 2)],
                             "normalizedCentre": [station["coordinate"]["x"], station["coordinate"]["y"]], "boundaryCrop": boundary, "foldAdjacent": fold,
                             "sourceTransform": "phase_3d3 source-to-1350x1000 homography" if tile else "existing rectified_complete canvas", "sourceSha256": source_by_id.get(source_file, {}).get("sha256")})
        queue.append({"reviewTargetId": crop_id, "stationId": sid, "primaryCropId": crop_id, "incidentExistingCandidateIds": sorted(set(incident[sid])),
                      "boundaryCrop": boundary, "foldAdjacent": fold, "coordinateConfidence": station.get("coordinateStatus", "candidate-unverified"),
                      "reviewStatus": "not-started", "newObservationIds": [], "notes": "Use source crop for line tracing; registered crop provides common-board context."})

    observation_records = []
    for edge in edges:
        observation_records.append({"observationId": f"OBS-CAND-{edge['edgeId']}", "origin": "existing-candidate", "candidateId": edge["edgeId"],
                                    "from": edge["from"], "to": edge["to"], "transport": edge["transport"], "sourceReferences": edge.get("evidence", []),
                                    "endpointScope": "observed-marker-200" if 200 in (edge["from"], edge["to"]) else "playable",
                                    "sourceCropIds": [f"ST-{edge['from']:03d}", f"ST-{edge['to']:03d}"] if edge["to"] <= 199 else [f"ST-{edge['from']:03d}"],
                                    "reviewStatus": "needs-review", "confidence": edge["confidence"], "existingVerificationStatus": edge["verificationStatus"],
                                    "supportingExplanation": edge.get("visualExplanation", ""), "contradictoryObservationIds": [], "notes": "Imported by reference; original candidate JSON remains authoritative and unchanged."})

    manifest = {"phase": "3E.2A", "coordinateSystem": {"canvas": [BOARD_W, BOARD_H], "origin": "top-left", "xDirection": "right", "yDirection": "down", "normalized": "canvas x/1350, y/1000"},
                "cropSizeCanvasPx": CROP_SIZE, "stationCount": 199, "cropCount": len(crop_records), "sources": sources, "registrations": str(REG_META.relative_to(REPO)),
                "stations": crop_records, "sourceHashes": {str(CANDIDATE_PATH.relative_to(REPO)): sha256(CANDIDATE_PATH), str(STATION_PATH.relative_to(REPO)): sha256(STATION_PATH)}}
    (OUT / "station-crop-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (OUT / "station-review-queue.json").write_text(json.dumps({"phase": "3E.2A", "queueCount": len(queue), "queue": queue}, indent=2), encoding="utf-8")
    (OUT / "edge-observations.json").write_text(json.dumps({"phase": "3E.2A", "schema": "phase-3e-2a-edge-observations", "observations": observation_records, "newObservations": []}, indent=2), encoding="utf-8")

    # Contact sheet: station number, crop ID and review flags remain legible.
    thumbs = []
    for crop, item in zip(crop_records, queue):
        image = cv2.imread(str(REPO / crop["registeredCropPath"]))
        image = cv2.resize(image, (120, 120), interpolation=cv2.INTER_AREA)
        cv2.rectangle(image, (0, 0), (119, 119), (255, 255, 255), 1)
        cv2.putText(image, str(crop["stationId"]), (3, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 255), 1, cv2.LINE_AA)
        if crop["boundaryCrop"]: cv2.putText(image, "B", (104, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 140, 255), 1, cv2.LINE_AA)
        if crop["foldAdjacent"]: cv2.putText(image, "F", (92, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 255), 1, cv2.LINE_AA)
        thumbs.append(image)
    rows = []
    for start in range(0, len(thumbs), 12):
        row = thumbs[start:start + 12]
        while len(row) < 12: row.append(np.zeros((120, 120, 3), dtype=np.uint8))
        rows.append(np.hstack(row))
    cv2.imwrite(str(OUT / "station-review-contact-sheet.png"), np.vstack(rows))

    assert len(crop_records) == 199 and {x["stationId"] for x in crop_records} == set(range(1, 200))
    assert len(observation_records) == 125 and {x["candidateId"] for x in observation_records} == {x["edgeId"] for x in edges}
    assert CANDIDATE_PATH.read_bytes() == candidate_bytes and STATION_PATH.read_bytes() == station_bytes
    print(json.dumps({"stations": len(crop_records), "crops": len(crop_records), "sources": len(sources), "candidate_observations": len(observation_records), "new_observations": 0}, indent=2))


if __name__ == "__main__":
    main()
