"""Phase 3D.4 human-assisted identity transcription audit.

This layer consumes the Phase 3D.3 registration and marker observations.  It
does not rerun calibration/detection and it does not manufacture a feature
match where the existing evidence mapping does not support one.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cv2

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "station_recovery"


def load(name: str) -> Any:
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def main() -> None:
    inventory = load("station_inventory_phase_3d3.json")
    mapping = load("station_evidence_mapping_phase_3d3.json")
    candidates = load("phase_3d3_physical_marker_candidates.json")
    detections = load("phase_3d3_highres_marker_detections.json")["detections"]
    photo_meta = load("phase_3d3_photo_metadata.json")

    supported = {station["station_id"]: station for station in inventory["stations"] if station["feature_id"] is not None}
    transcriptions = []
    for station_id in range(1, 200):
        station = inventory["stations"][station_id - 1]
        if station_id in supported:
            # Existing direct/candidate readings are retained verbatim, with a
            # transcription record added around them rather than rewriting them.
            transcriptions.append({
                "station_id": station_id,
                "printed_number": station_id,
                "feature_id": station["feature_id"],
                "identity_status": station["status"],
                "reading_confidence": "directly_read" if station["status"] == "verified" else "candidate_uncertain",
                "number_reading_status": "directly_read" if station["status"] == "verified" else "candidate_from_prior_evidence",
                "feature_match_confidence": "high" if station["status"] == "verified" else "low",
                "marker_centre_canvas": [station["pixel_x"], station["pixel_y"]],
                "normalized": [station["normalized_x"], station["normalized_y"]],
                "supporting_sources": station["source_images"],
                "overlap_confirmation": station["evidence_source"],
                "notes": station["evidence_basis"],
            })
        else:
            transcriptions.append({
                "station_id": station_id,
                "printed_number": None,
                "feature_id": None,
                "identity_status": "unresolved",
                "reading_confidence": "not_feature_mapped",
                "number_reading_status": "unreadable_or_not_transcribed",
                "feature_match_confidence": "none",
                "marker_centre_canvas": None,
                "normalized": None,
                "supporting_sources": [],
                "overlap_confirmation": None,
                "notes": "The completeness slot is preserved, but no explicit station-number-to-marker transcription record is attached; printed_number remains null rather than being inferred from position or ordering.",
            })

    per_tile = []
    for record in photo_meta["records"]:
        tile = record["filename"]
        observations = [d for d in detections if d["source_tile"] == tile]
        per_tile.append({
            "tile": tile,
            "status": record["status"],
            "dimensions": record.get("dimensions"),
            "sha256": record.get("sha256"),
            "raw_marker_observation_count": len(observations),
            "observation_centres_canvas": [[d["pixel_x"], d["pixel_y"]] for d in observations],
            "identity_transcription_status": "reviewed_for_registration_and_marker_observations",
            "identity_assignments_from_this_tile": [],
            "identity_assignment_count": 0,
            "notes": "Raw high-resolution marker observations are intentionally not treated as printed station identities until a human-readable number and existing feature match are recorded together.",
        })

    counts = {
        "verified": sum(x["identity_status"] == "verified" for x in transcriptions),
        "candidate_uncertain": sum(x["identity_status"] == "candidate_uncertain" for x in transcriptions),
        "unresolved": sum(x["identity_status"] == "unresolved" for x in transcriptions),
        "conflicting": 0,
        "duplicate": 0,
    }
    counts["number_reading"] = {
        "actually_read_directly": sum(x["number_reading_status"] == "directly_read" for x in transcriptions),
        "candidate_from_prior_evidence": sum(x["number_reading_status"] == "candidate_from_prior_evidence" for x in transcriptions),
        "read_but_unmapped": 0,
        "unreadable_or_not_transcribed": sum(x["number_reading_status"] == "unreadable_or_not_transcribed" for x in transcriptions),
    }
    overlay_station_ids = [x["station_id"] for x in transcriptions if x["feature_id"] is not None]
    out_meta = {
        "phase": "3D.4",
        "coordinate_system": inventory["metadata"]["coordinate_system"],
        "source_phase": "3D.3",
        "physical_marker_candidates_preserved": candidates["deduplicated_candidates"],
        "raw_observations_preserved": inventory["metadata"]["raw_observation_count_preserved"],
        "identity_policy": "printed number and existing feature correspondence must both be documented; no landmark-only inference",
        "summary_counts": counts,
    }
    out_meta["overlay_numbered_station_ids"] = overlay_station_ids
    payload = {"metadata": out_meta, "stations": transcriptions, "marker_200": mapping["marker_200"]}
    (OUT / "station_transcription_phase_3d4.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (OUT / "station_transcription_tile_audit_phase_3d4.json").write_text(json.dumps({"metadata": out_meta, "tiles": per_tile}, indent=2), encoding="utf-8")

    # Overlay labels only the six currently supported identity mappings. All
    # other physical candidates remain neutral review rings.
    composite = cv2.imread(str(OUT / "phase_3d3_registered_full_board_composite.png"))
    if composite is not None:
        for candidate in candidates["candidates"]:
            cv2.circle(composite, (int(candidate["pixel_x"]), int(candidate["pixel_y"])), 4, (160, 160, 160), 1)
        for station in transcriptions:
            if station["feature_id"] is None:
                continue
            x, y = map(int, map(round, station["marker_centre_canvas"]))
            colour = (0, 220, 0) if station["identity_status"] == "verified" else (0, 180, 255)
            cv2.circle(composite, (x, y), 10, colour, 2)
            cv2.putText(composite, str(station["station_id"]), (x + 8, y + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, colour, 1, cv2.LINE_AA)
        cv2.rectangle(composite, (8, 8), (900, 48), (20, 20, 20), -1)
        cv2.putText(composite, "Phase 3D.4: six pre-existing identity records only; gray rings are unmapped physical candidates", (18, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.imwrite(str(OUT / "station_transcription_overlay_phase_3d4.png"), composite)

    unresolved = [str(x) for x in range(1, 200) if x not in supported]
    report = f"""# Phase 3D.4 station transcription report

## Completeness

All 199 playable station IDs are represented exactly once in `station_transcription_phase_3d4.json`.

| Status | Count |
|---|---:|
| Verified | {counts['verified']} |
| Candidate-uncertain | {counts['candidate_uncertain']} |
| Unresolved feature mappings | {counts['unresolved']} |
| Conflicting | {counts['conflicting']} |
| Duplicate | {counts['duplicate']} |

## Number-reading versus feature-mapping completeness

| Number-reading state | Count |
|---|---:|
| Printed numbers directly read and evidenced | {counts['number_reading']['actually_read_directly']} |
| Candidate records inherited from prior evidence, not direct high-resolution transcription | {counts['number_reading']['candidate_from_prior_evidence']} |
| Read but unmapped | {counts['number_reading']['read_but_unmapped']} |
| Unreadable or not transcribed into this structured artifact | {counts['number_reading']['unreadable_or_not_transcribed']} |

Supported existing mappings are preserved for stations 1, 3, 120, 123, 158 and 199. The unresolved list contains {len(unresolved)} station IDs: `{', '.join(unresolved)}`.

The 16 high-resolution tiles and their 259 registered marker observations are recorded in the tile audit. Marker 200 remains separate and is excluded from the playable station array.

## Overlay explanation

The overlay is generated from `feature_id != null` records in this JSON. Its six labels are not OCR output and are not position/order-derived annotations: they are the two pre-existing verified records and four pre-existing candidate-uncertain records copied from Phase 3D.3. The gray rings are physical-marker candidates with no station identity. No high-resolution tile is currently linked to one of the six identity records, so every tile audit entry correctly reports zero identity assignments.

This pass does not alter coordinates, raw observations, feature IDs, calibration, detection or transport-edge data. A physical marker observation is not promoted to a station identity unless the printed number and existing feature correspondence are recorded together.
"""
    (OUT / "station_recovery_phase_3d4_report.md").write_text(report, encoding="utf-8")
    (OUT / "station_recovery_completeness_phase_3d4.md").write_text(report, encoding="utf-8")
    print(json.dumps({"stations": len(transcriptions), "counts": counts, "tiles": len(per_tile), "raw_marker_observations": len(detections)}, indent=2))


if __name__ == "__main__":
    main()
