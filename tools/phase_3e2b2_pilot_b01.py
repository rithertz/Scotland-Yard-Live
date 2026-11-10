"""Record the controlled B-01 pilot review without changing source candidates."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "docs" / "game" / "data"
WORK = DATA / "phase-3e2b1-reconstruction"


def write(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


OBSERVATIONS = [
    {"observationId": "OBS-3E2B1-00001", "from": 1, "to": 8, "transport": "taxi", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-left.jpeg", "sourceCropIds": ["ST-001", "ST-008"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "Top-left board photograph visibly shows the solid yellow route leaving marker 1 and reaching marker 8; the registered ST-001 context shows both endpoint markers and the intervening route.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "high", "uncertainty": ["Exact route pixel polyline was not measured from the rotated reference photograph."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-001"], "duplicateOfObservationId": None},
    {"observationId": "OBS-3E2B1-00002", "from": 2, "to": 10, "transport": "taxi", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-left.jpeg", "sourceCropIds": ["ST-002", "ST-010"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "Top-left photograph and registered ST-002 context visibly show the solid yellow route between markers 2 and 10 along the park edge.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "high", "uncertainty": ["Exact route pixel polyline was not measured."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-002"], "duplicateOfObservationId": None},
    {"observationId": "OBS-3E2B1-00003", "from": 2, "to": 20, "transport": "taxi", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-left.jpeg", "sourceCropIds": ["ST-002", "ST-020"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "Top-left photograph visibly shows the solid yellow route from marker 2 toward marker 20 around the western park edge, with both endpoints readable.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "medium", "uncertainty": ["The route continuation is close to the crop boundary in the registered context."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-003"], "duplicateOfObservationId": None},
    {"observationId": "OBS-3E2B1-00004", "from": 3, "to": 4, "transport": "taxi", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-left.jpeg", "sourceCropIds": ["ST-003", "ST-004"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "The short solid yellow road between the readable markers 3 and 4 is visible in the upper-right area of the top-left photograph.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "high", "uncertainty": ["No independent coordinate measurement was made."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-004"], "duplicateOfObservationId": None},
    {"observationId": "OBS-3E2B1-00005", "from": 4, "to": 13, "transport": "taxi", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-left.jpeg", "sourceCropIds": ["ST-004", "ST-013"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "The top-left photograph shows the solid yellow route continuing from readable marker 4 to readable marker 13; the red route crossing is kept separate.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "medium", "uncertainty": ["Crossing geometry warrants confirmation in a tighter high-resolution crop."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-005"], "duplicateOfObservationId": None},
    {"observationId": "OBS-3E2B1-00006", "from": 5, "to": 15, "transport": "taxi", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-right.jpeg", "sourceCropIds": ["ST-005", "ST-015"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "Top-right photograph and the registered ST-005 context visibly show the solid yellow route from marker 5 to marker 15.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "high", "uncertainty": ["Exact route pixel polyline was not measured."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-006"], "duplicateOfObservationId": None},
    {"observationId": "OBS-3E2B1-00007", "from": 6, "to": 7, "transport": "taxi", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-right.jpeg", "sourceCropIds": ["ST-006", "ST-007"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "The top-right photograph shows a short solid yellow connection between readable markers 6 and 7.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "medium", "uncertainty": ["The endpoint area is close to the source-photo edge; overlap confirmation is recommended."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-007"], "duplicateOfObservationId": None},
    {"observationId": "OBS-3E2B1-00008", "from": 7, "to": 17, "transport": "taxi", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-right.jpeg", "sourceCropIds": ["ST-007", "ST-017"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "The top-right photograph visibly shows the solid yellow route continuing from marker 7 to marker 17.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "medium", "uncertainty": ["Endpoint continuation should be checked against an overlapping crop before wider batch review."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-008"], "duplicateOfObservationId": None},
    {"observationId": "OBS-3E2B1-00009", "from": 8, "to": 18, "transport": "taxi", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-left.jpeg", "sourceCropIds": ["ST-008", "ST-018"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "The top-left photograph shows the solid yellow route in the 8/18 corridor with both printed endpoint markers visible.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "medium", "uncertainty": ["The route is near an image boundary and should receive overlap confirmation."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-009"], "duplicateOfObservationId": None},
    {"observationId": "OBS-3E2B1-00010", "from": 9, "to": 20, "transport": "taxi", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-left.jpeg", "sourceCropIds": ["ST-009", "ST-020"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "Top-left photograph visibly shows the solid yellow route from marker 9 toward marker 20 around the park boundary.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "high", "uncertainty": ["Exact route pixel polyline was not measured."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-010"], "duplicateOfObservationId": None},
    {"observationId": "OBS-3E2B1-00011", "from": 10, "to": 11, "transport": "taxi", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-left.jpeg", "sourceCropIds": ["ST-010", "ST-011"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "The short solid yellow connection between readable markers 10 and 11 is visible along the central park edge.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "high", "uncertainty": ["No independent coordinate measurement was made."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-011"], "duplicateOfObservationId": None},
    {"observationId": "OBS-3E2B1-00012", "from": 1, "to": 46, "transport": "underground", "sourcePhotograph": "docs/game/evidence/board-photos/original-references/top-left.jpeg", "sourceCropIds": ["ST-001", "ST-046"], "sourcePixelRouteCoordinates": None, "registeredBoardRouteCoordinates": None, "evidenceDescription": "A dashed red route is visibly traceable from marker 1 toward readable marker 46 in the top-left photograph; it is distinct from the solid yellow route.", "reviewer": "human-guided B-01 pilot", "reviewStatus": "reviewed", "confidence": "medium", "uncertainty": ["The long route crosses several junctions and should be independently checked in an overlapping source view."], "supportingObservationIds": [], "conflictingObservationIds": [], "relatedCandidateIds": ["E-032"], "duplicateOfObservationId": None},
]


def main() -> None:
    observations_path = WORK / "new-edge-observations.json"
    ledger = json.loads(observations_path.read_text(encoding="utf-8"))
    batches_path = WORK / "review-batches.json"
    batches_doc = json.loads(batches_path.read_text(encoding="utf-8"))
    b01 = next(item for item in batches_doc["batches"] if item["batchId"] == "B-01")
    b01_ids = set(b01.get("newObservationIds", []))
    ledger_ids = {observation["observationId"] for observation in ledger.get("observations", [])}
    later_ids = {observation_id for batch in batches_doc["batches"] if batch["batchId"] != "B-01" for observation_id in batch.get("newObservationIds", [])}
    if ledger_ids & later_ids:
        raise RuntimeError("Refusing B-01 pilot update: ledger contains observations assigned to a later batch.")
    unrelated = [observation for observation in ledger.get("observations", []) if observation["observationId"] not in b01_ids]
    pilot_ids = {observation["observationId"] for observation in OBSERVATIONS}
    if {observation["observationId"] for observation in unrelated} & pilot_ids:
        raise RuntimeError("Refusing B-01 pilot update: preserved observation collides with a pilot observation ID.")
    ledger["observations"] = unrelated + OBSERVATIONS
    ledger["notes"] = "B-01 pilot observations only; ambiguous candidates remain in the reconciliation report."
    write(observations_path, ledger)

    batch = b01
    batch["reviewStatus"] = "uncertain"
    batch["newObservationIds"] = [observation["observationId"] for observation in OBSERVATIONS]
    batch["reviewNote"] = "All B-01 candidate routes were inspected; material ambiguity remains for three bus candidates and several boundary continuations."
    write(batches_path, batches_doc)

    summary_path = WORK / "reconstruction-summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["newObservationCount"] = len(OBSERVATIONS)
    summary["b01Pilot"] = {"status": "uncertain", "reviewedStations": list(range(1, 11)), "observationIds": batch["newObservationIds"]}
    write(summary_path, summary)
    print(json.dumps({"batch": "B-01", "status": batch["reviewStatus"], "observations": len(OBSERVATIONS)}, indent=2))


if __name__ == "__main__":
    main()
