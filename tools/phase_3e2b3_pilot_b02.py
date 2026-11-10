"""Record the bounded B-02 pilot while preserving B-01 and later batches."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "docs" / "game" / "data"
WORK = DATA / "phase-3e2b1-reconstruction"

def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

OBSERVATIONS = []
for number, (candidate, from_station, to_station, transport, photograph, confidence, description, uncertainty) in enumerate([
    ("E-012", 11, 22, "taxi", "top-left.jpeg", "medium", "Top-left evidence shows the solid yellow route from readable marker 11 toward readable marker 22.", "The corridor shares nearby green evidence."),
    ("E-013", 12, 23, "taxi", "top-left.jpeg", "medium", "Top-left evidence shows the solid yellow route from marker 12 to marker 23 with the crossing visible.", "Crossing geometry should be confirmed in overlap."),
    ("E-014", 13, 14, "taxi", "top-right.jpeg", "high", "Top-right evidence visibly shows the solid yellow route between markers 13 and 14.", "No route polyline was measured."),
    ("E-015", 14, 15, "taxi", "top-right.jpeg", "high", "Top-right evidence visibly shows the adjacent solid yellow route between markers 14 and 15.", "No route polyline was measured."),
    ("E-016", 15, 16, "taxi", "top-right.jpeg", "medium", "Top-right evidence shows the solid yellow corridor between markers 15 and 16.", "A red route crosses nearby."),
    ("E-017", 16, 29, "taxi", "top-right.jpeg", "medium", "Top-right evidence shows the yellow route continuing from marker 16 toward marker 29.", "Endpoint layering warrants overlap confirmation."),
    ("E-018", 17, 30, "taxi", "top-right.jpeg", "high", "Top-right evidence visibly links markers 17 and 30 with a solid yellow route.", "No route polyline was measured."),
    ("E-019", 18, 31, "taxi", "top-left.jpeg", "high", "Top-left evidence visibly shows the yellow route between markers 18 and 31.", "No route polyline was measured."),
    ("E-020", 19, 32, "taxi", "top-left.jpeg", "high", "Top-left evidence visibly shows the yellow route between markers 19 and 32.", "No route polyline was measured."),
    ("E-021", 20, 33, "taxi", "top-left.jpeg", "medium", "Top-left evidence shows the solid yellow route leaving marker 20 toward marker 33.", "The red crossing is retained as uncertainty."),
    ("E-025", 11, 22, "bus", "top-left.jpeg", "medium", "Top-left evidence shows a green route sharing the 11/22 corridor, distinct from the yellow route.", "Layering at the junction needs overlap confirmation."),
    ("E-026", 13, 14, "bus", "top-right.jpeg", "medium", "Top-right evidence shows a green route alongside the 13/14 yellow corridor.", "The shared corridor is visually crowded."),
    ("E-027", 14, 15, "bus", "top-right.jpeg", "medium", "Top-right evidence shows green transport markings continuing between markers 14 and 15.", "Endpoint service-line separation needs confirmation."),
    ("E-028", 15, 29, "bus", "top-right.jpeg", "medium", "Top-right evidence shows a green route in the 15/29 corridor.", "Line layering at crossings remains uncertain."),
    ("E-033", 13, 46, "underground", "top-left.jpeg", "medium", "Top-left evidence shows the dashed red route continuing from marker 13 toward marker 46.", "The long route should be confirmed by an overlapping view."),
], start=13):
    OBSERVATIONS.append({"observationId": f"OBS-3E2B1-{number:05d}", "from": from_station, "to": to_station, "transport": transport, "sourcePhotograph": f"docs/game/evidence/board-photos/original-references/{photograph}", "sourceCropIds": [f"ST-{from_station:03d}", f"ST-{to_station:03d}"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": description, "reviewer": "human-guided B-02 pilot", "reviewStatus": "reviewed", "confidence": confidence, "uncertainty": [uncertainty], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": [candidate], "duplicateOfObservationId": None})

def main() -> None:
    observations_path = WORK / "new-edge-observations.json"
    ledger = json.loads(observations_path.read_text(encoding="utf-8"))
    batches_path = WORK / "review-batches.json"
    batches_doc = json.loads(batches_path.read_text(encoding="utf-8"))
    batches = batches_doc.get("batches")
    if not isinstance(batches, list):
        raise RuntimeError("Refusing B-02 pilot update: batch metadata is missing or malformed.")
    if any(not isinstance(batch, dict) or not isinstance(batch.get("batchId"), str) for batch in batches):
        raise RuntimeError("Refusing B-02 pilot update: batch metadata is missing or malformed.")
    matching = [batch for batch in batches if isinstance(batch, dict) and batch.get("batchId") in {"B-01", "B-02"}]
    if len(matching) != 2:
        raise RuntimeError("Refusing B-02 pilot update: required B-01/B-02 batch metadata is missing or malformed.")
    b01 = next(batch for batch in matching if batch["batchId"] == "B-01")
    b02 = next(batch for batch in matching if batch["batchId"] == "B-02")
    for batch in (b01, b02):
        if not isinstance(batch.get("newObservationIds"), list) or len(batch["newObservationIds"]) != len(set(batch["newObservationIds"])):
            raise RuntimeError("Refusing B-02 pilot update: required batch observation metadata is missing or malformed.")
    if b01.get("reviewStatus") != "uncertain" or b02.get("reviewStatus") not in {"not-started", "uncertain"}:
        raise RuntimeError("Refusing B-02 pilot update: required batch review status is missing or malformed.")
    b02_ids = set(b02.get("newObservationIds", []))
    b01_ids = set(b01.get("newObservationIds", []))
    if b01_ids & b02_ids:
        raise RuntimeError("Refusing B-02 pilot update: B-01 and B-02 observation ID lists overlap.")
    if not isinstance(ledger.get("observations"), list) or any(not isinstance(observation, dict) or "observationId" not in observation for observation in ledger["observations"]):
        raise RuntimeError("Refusing B-02 pilot update: observation ledger is malformed.")
    ledger_ids = {observation["observationId"] for observation in ledger["observations"]}
    if not b01_ids or not b01_ids <= ledger_ids:
        raise RuntimeError("Refusing B-02 pilot update: B-01 metadata does not match preserved ledger observations.")
    if b02_ids and not b02_ids <= ledger_ids:
        raise RuntimeError("Refusing B-02 pilot update: B-02 metadata references missing ledger observations.")
    later_ids = {observation_id for batch in batches if batch.get("batchId") not in {"B-01", "B-02"} for observation_id in batch.get("newObservationIds", [])}
    if ledger_ids & later_ids:
        raise RuntimeError("Refusing B-02 pilot update: ledger contains observations assigned to a later batch.")
    unrelated = [observation for observation in ledger.get("observations", []) if observation["observationId"] not in b02_ids]
    pilot_ids = {observation["observationId"] for observation in OBSERVATIONS}
    if b02_ids and b02_ids != pilot_ids:
        raise RuntimeError("Refusing B-02 pilot update: existing B-02 metadata does not match the pilot observation set.")
    if {observation["observationId"] for observation in unrelated} & pilot_ids:
        raise RuntimeError("Refusing B-02 pilot update: preserved observation collides with a pilot observation ID.")
    ledger["observations"] = unrelated + OBSERVATIONS
    ledger["notes"] = "B-01 and B-02 pilot observations; later batches remain untouched."
    write(observations_path, ledger)
    b02["reviewStatus"] = "uncertain"
    b02["newObservationIds"] = [observation["observationId"] for observation in OBSERVATIONS]
    b02["reviewNote"] = "B-02 routes were inspected; five overlapping/long-route candidates remain ambiguous or are covered by preserved B-01 observations."
    write(batches_path, batches_doc)
    summary_path = WORK / "reconstruction-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["newObservationCount"] = len(ledger["observations"])
    summary["b02Pilot"] = {"status": "uncertain", "reviewedStations": list(range(11, 21)), "observationIds": b02["newObservationIds"]}
    write(summary_path, summary)
    print(json.dumps({"batch": "B-02", "status": b02["reviewStatus"], "newObservations": len(OBSERVATIONS)}, indent=2))

if __name__ == "__main__":
    main()
