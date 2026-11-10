"""Build the Phase 3E.2B.1 transport-graph reconstruction workspace."""

from __future__ import annotations

import hashlib
import html
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "docs" / "game" / "data"
WORK = DATA / "phase-3e2b1-reconstruction"
CANDIDATES = DATA / "board-edge-candidates-1-200.json"
QUEUE = DATA / "phase-3e2a-workspace" / "station-review-queue.json"
OBSERVATIONS = DATA / "phase-3e2a-workspace" / "edge-observations.json"
STATIONS = REPO / "packages" / "board-data" / "data" / "stations.json"
MANIFEST = DATA / "phase-3e2a-workspace" / "station-crop-manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    candidates_doc = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    queue_doc = json.loads(QUEUE.read_text(encoding="utf-8"))
    old_obs = json.loads(OBSERVATIONS.read_text(encoding="utf-8"))
    stations_doc = json.loads(STATIONS.read_text(encoding="utf-8"))
    manifest_doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    existing_summary_path = WORK / "reconstruction-summary.json"
    existing_summary = json.loads(existing_summary_path.read_text(encoding="utf-8")) if existing_summary_path.exists() else {}
    edges = candidates_doc["edges"]
    station_ids = [station["id"] for station in stations_doc["stations"]]

    # Candidate import preserves the 125 source records semantically. The
    # enclosing JSON is intentionally newly serialized for this workspace.
    candidate_import = {
        "phase": "3E.2B.1",
        "schema": "phase-3e2b1-candidate-import",
        "sourceDataset": "docs/game/data/board-edge-candidates-1-200.json",
        "sourceDatasetSha256": sha256(CANDIDATES),
        "canonicalStatus": "non-canonical",
        "candidates": edges,
    }
    write_json(WORK / "candidate-import.json", candidate_import)

    existing_ledger_path = WORK / "new-edge-observations.json"
    existing_ledger = json.loads(existing_ledger_path.read_text(encoding="utf-8")) if existing_ledger_path.exists() else None
    new_observations = {
        "phase": "3E.2B.1",
        "schema": "phase-3e2b1-new-edge-observations",
        "observationIdPolicy": "OBS-3E2B1-NNNNN, monotonically assigned; never reused",
        "reviewStatusValues": ["not-started", "in-progress", "reviewed", "uncertain", "conflicting", "blocked"],
        "observations": existing_ledger.get("observations", []) if existing_ledger else [],
        "notes": existing_ledger.get("notes", "Empty by design. Human review must add evidence-backed observations; no graph transcription was performed.") if existing_ledger else "Empty by design. Human review must add evidence-backed observations; no graph transcription was performed.",
    }
    write_json(WORK / "new-edge-observations.json", new_observations)

    incident: dict[int, list[str]] = defaultdict(list)
    for edge in edges:
        incident[edge["from"]].append(edge["edgeId"])
        incident[edge["to"]].append(edge["edgeId"])
    queue_by_station = {entry["stationId"]: entry for entry in queue_doc["queue"]}

    # Ten-station batches keep the review manageable while preserving all
    # boundary/fold stations and every incident candidate reference.
    batches = []
    for index, start in enumerate(range(1, 200, 10), start=1):
        station_batch = list(range(start, min(start + 10, 200)))
        candidate_ids = sorted({edge_id for station_id in station_batch for edge_id in incident[station_id]}, key=lambda value: int(value.split("-")[1]))
        priority = []
        for station_id in station_batch:
            entry = queue_by_station[station_id]
            if entry["boundaryCrop"] or entry["foldAdjacent"]:
                priority.append({"stationId": station_id, "boundaryCrop": entry["boundaryCrop"], "foldAdjacent": entry["foldAdjacent"]})
        batches.append({
            "batchId": f"B-{index:02d}",
            "stationIds": station_batch,
            "candidateIds": candidate_ids,
            "priorityStations": priority,
            "reviewStatus": "not-started",
            "newObservationIds": [],
            "reviewRule": "Review all incident candidate routes and any newly discovered routes; station presence alone is not completion.",
        })
    existing_batches_path = WORK / "review-batches.json"
    if existing_batches_path.exists():
        existing_batches = {batch["batchId"]: batch for batch in json.loads(existing_batches_path.read_text(encoding="utf-8"))["batches"]}
        for batch in batches:
            prior = existing_batches.get(batch["batchId"], {})
            for field in ("reviewStatus", "newObservationIds", "reviewNote"):
                if field in prior:
                    batch[field] = prior[field]
    write_json(existing_batches_path, {"phase": "3E.2B.1", "batchSize": 10, "batches": batches})

    # The dashboard is intentionally a static, dependency-free review aid.
    rows = []
    for station_id in station_ids:
        entry = queue_by_station[station_id]
        crop = manifest_doc["stations"][station_id - 1]
        crop_path = (crop.get("sourceCropPath") or crop["registeredCropPath"]).replace("\\", "/")
        target = REPO / crop_path
        relative_crop = os.path.relpath(target, WORK).replace("\\", "/")
        rows.append(f'<tr><td>ST-{station_id:03d}</td><td><code>{html.escape(", ".join(entry["incidentExistingCandidateIds"]) or "—")}</code></td><td><a href="{html.escape(relative_crop, quote=True)}">{html.escape(crop_path)}</a></td><td>not-started</td></tr>')
    dashboard = """<!doctype html><meta charset="utf-8"><title>Scotland Yard Live — Phase 3E.2B.1 review</title>
<style>body{font:14px system-ui;margin:2rem;background:#f7f7f7}table{border-collapse:collapse;background:white}td,th{border:1px solid #ccc;padding:.4rem;text-align:left}input{margin:.5rem 0;padding:.5rem;width:24rem}code{font-size:12px}</style>
<h1>Phase 3E.2B.1 transport review</h1><p><strong>Read-only index.</strong> Crop links and candidate IDs are provided for inspection only. This page does not persist status and is not a graph editor. Record approved review progress and route evidence in the designated JSON workspace in a later approved task. Existing candidate records remain hypotheses.</p><input id="filter" placeholder="Filter station or candidate"><table id="review"><thead><tr><th>Station</th><th>Existing candidates</th><th>Primary crop</th><th>Dashboard status</th></tr></thead><tbody>""" + "\n".join(rows) + """</tbody></table><script>const filter=document.getElementById('filter');filter.oninput=()=>{let q=filter.value.toLowerCase();for(let r of document.querySelectorAll('#review tbody tr'))r.hidden=!r.innerText.toLowerCase().includes(q)}</script>"""
    (WORK / "review-dashboard.html").write_text(dashboard, encoding="utf-8")

    status_counts = defaultdict(int)
    for observation in old_obs["observations"]:
        status_counts[observation["reviewStatus"]] += 1
    transport_counts = defaultdict(int)
    for edge in edges:
        transport_counts[edge["transport"]] += 1
    pairs: dict[tuple[int, int], set[str]] = defaultdict(set)
    for edge in edges:
        pairs[tuple(sorted((edge["from"], edge["to"])))].add(edge["transport"])
    multi_transport_pairs = sum(len(types) > 1 for types in pairs.values())
    unresolved_candidates = sum(edge["verificationStatus"] == "unresolved" for edge in edges)
    marker_200_candidates = [edge["edgeId"] for edge in edges if 200 in (edge["from"], edge["to"])]
    summary = {
        "phase": "3E.2B.1",
        "candidateCount": len(edges),
        "newObservationCount": len(new_observations["observations"]),
        "batchCount": len(batches),
        "stationCoverage": {"supported": station_ids, "coveredByBatches": sorted({station_id for batch in batches for station_id in batch["stationIds"]})},
        "candidateTransportCounts": dict(sorted(transport_counts.items())),
        "existingObservationStatusCounts": dict(sorted(status_counts.items())),
        "multiTransportEndpointPairCount": multi_transport_pairs,
        "unresolvedCandidateCount": unresolved_candidates,
        "marker200CandidateIds": marker_200_candidates,
        "marker200Policy": "preserve existing hypothesis separately; do not resolve or promote in Phase 3E.2B.1",
        "reviewStatusValues": ["not-started", "in-progress", "reviewed", "uncertain", "conflicting", "blocked"],
        "automaticPromotion": False,
        "canonicalDataModified": False,
        "protectedInputs": {
            "stationsSha256": sha256(STATIONS),
            "candidateDatasetSha256": sha256(CANDIDATES),
            "stationReviewQueueSha256": sha256(QUEUE),
            "edgeObservationsSha256": sha256(OBSERVATIONS),
        },
    }
    if "b01Pilot" in existing_summary:
        summary["b01Pilot"] = existing_summary["b01Pilot"]
    write_json(WORK / "reconstruction-summary.json", summary)
    write_json(WORK / "phase-3e2b1-workspace.json", {
        "phase": "3E.2B.1",
        "architecture": {"candidateImport": "candidate-import.json", "newObservations": "new-edge-observations.json", "reviewBatches": "review-batches.json", "dashboard": "review-dashboard.html", "summary": "reconstruction-summary.json"},
        "evidencePolicy": ["No proximity or numbering inference", "Route evidence must show both endpoints and the intervening route", "Coordinate confidence is separate from edge confidence", "Conflicts and duplicates remain visible", "No automatic promotion to canonical data"],
    })
    print(json.dumps({"candidates": len(edges), "newObservations": len(new_observations["observations"]), "batches": len(batches), "stations": len(station_ids), "multiTransportPairs": multi_transport_pairs, "unresolvedCandidates": unresolved_candidates}, indent=2))


if __name__ == "__main__":
    main()
