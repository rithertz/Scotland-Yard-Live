"""Independent validation for the Phase 3E.2B.1 workspace."""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "docs" / "game" / "data"
WORK = DATA / "phase-3e2b1-reconstruction"
SUPPORTED_TRANSPORTS = {"taxi", "bus", "underground", "boat"}
REVIEW_STATUSES = {"not-started", "in-progress", "reviewed", "uncertain", "conflicting", "blocked"}


def load(name: str) -> Any:
    return json.loads((WORK / name).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def _schema_validate(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    # The workspace schema uses these instance-validation keywords: type,
    # enum, minLength, pattern, minimum, maximum, required, properties,
    # additionalProperties and items. `$schema` and `title` are schema
    # metadata and do not impose constraints on an instance.
    expected = schema.get("type")
    valid_types = expected if isinstance(expected, list) else [expected] if expected else []
    if valid_types:
        type_ok = any((kind == "object" and isinstance(value, dict)) or (kind == "array" and isinstance(value, list)) or (kind == "string" and isinstance(value, str)) or (kind == "integer" and isinstance(value, int) and not isinstance(value, bool)) or (kind == "null" and value is None) for kind in valid_types)
        assert type_ok, f"{path}: invalid JSON Schema type"
    if "enum" in schema:
        assert value in schema["enum"], f"{path}: value outside enum"
    if isinstance(value, str):
        if "minLength" in schema:
            assert len(value) >= schema["minLength"], f"{path}: string too short"
        if "pattern" in schema:
            assert re.fullmatch(schema["pattern"], value), f"{path}: pattern mismatch"
    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema:
            assert value >= schema["minimum"], f"{path}: below minimum"
        if "maximum" in schema:
            assert value <= schema["maximum"], f"{path}: above maximum"
    if isinstance(value, dict):
        for required in schema.get("required", []):
            assert required in value, f"{path}: missing required field {required}"
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            assert set(value) <= set(properties), f"{path}: unexpected property"
        for key, child in value.items():
            if key in properties:
                _schema_validate(child, properties[key], f"{path}.{key}")
    if isinstance(value, list) and "items" in schema:
        for index, child in enumerate(value):
            _schema_validate(child, schema["items"], f"{path}[{index}]")


def validate_observation_relationships(observations: list[dict[str, Any]], candidates: dict[str, dict[str, Any]], crop_ids: set[str]) -> list[str]:
    schema = json.loads((WORK / "phase-3e2b1-observation.schema.json").read_text(encoding="utf-8"))
    assert schema["additionalProperties"] is False
    seen: set[str] = set()
    for observation in observations:
        _schema_validate(observation, schema)
        observation_id = observation["observationId"]
        assert observation_id not in seen
        seen.add(observation_id)
        assert (REPO / observation["sourcePhotograph"]).is_file()
        assert observation["sourceCropIds"] and all(crop_id in crop_ids for crop_id in observation["sourceCropIds"])
        endpoint_crops = {f"ST-{observation['from']:03d}", f"ST-{observation['to']:03d}"}
        assert endpoint_crops <= set(observation["sourceCropIds"]), "source crops do not cover both observation endpoints"
        related = observation.get("relatedCandidateIds", [])
        assert related and all(candidate_id in candidates for candidate_id in related)
        for candidate_id in related:
            candidate = candidates[candidate_id]
            assert (observation["from"], observation["to"], observation["transport"]) == (candidate["from"], candidate["to"], candidate["transport"])
    ids = {observation["observationId"] for observation in observations}
    graph: dict[str, set[str]] = {observation_id: set() for observation_id in ids}
    for observation in observations:
        source_id = observation["observationId"]
        references = observation.get("supportingObservationIds", []) + observation.get("conflictingObservationIds", [])
        duplicate = observation.get("duplicateOfObservationId")
        if duplicate is not None:
            references.append(duplicate)
        for reference in references:
            assert reference in ids and reference != source_id
            graph[source_id].add(reference)
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> None:
        assert node not in visiting, "cyclic observation relationship"
        if node in visited:
            return
        visiting.add(node)
        for child in graph[node]:
            visit(child)
        visiting.remove(node)
        visited.add(node)
    for node in graph:
        visit(node)
    return sorted(ids)


def validate_batch_isolation(observations: list[dict[str, Any]], batches: list[dict[str, Any]], active_batch_ids: tuple[str, ...] = ("B-01", "B-02")) -> list[str]:
    active_batches = [next(batch for batch in batches if batch["batchId"] == batch_id) for batch_id in active_batch_ids]
    observation_ids = {observation["observationId"] for observation in observations}
    listed_by_batch = []
    for batch in active_batches:
        listed_ids = batch.get("newObservationIds", [])
        assert len(listed_ids) == len(set(listed_ids)), f"{batch['batchId']} contains duplicate observation IDs"
        listed_by_batch.extend(listed_ids)
        assert batch.get("reviewStatus") == "uncertain"
    assert len(listed_by_batch) == len(set(listed_by_batch))
    assert listed_by_batch == sorted(observation_ids), "active batch observation lists must exactly match the ledger"
    for batch in batches:
        if batch["batchId"] not in active_batch_ids:
            assert batch["reviewStatus"] == "not-started"
            assert batch.get("newObservationIds", []) == []
    return sorted(observation_ids)


def validate() -> dict[str, Any]:
    imported_doc = load("candidate-import.json")
    candidates = imported_doc["candidates"]
    source = json.loads((DATA / "board-edge-candidates-1-200.json").read_text(encoding="utf-8"))["edges"]
    batches = load("review-batches.json")["batches"]
    summary = load("reconstruction-summary.json")
    assert len(candidates) == 125
    expected_ids = [f"E-{index:03d}" for index in range(1, 126)]
    assert [edge["edgeId"] for edge in candidates] == expected_ids
    assert len({edge["edgeId"] for edge in candidates}) == 125
    assert candidates == source, "candidate import is not semantically equal to source records"
    assert imported_doc["sourceDatasetSha256"] == sha256(DATA / "board-edge-candidates-1-200.json")

    transport_counts = defaultdict(int)
    pairs: dict[tuple[int, int], set[str]] = defaultdict(set)
    unresolved: list[str] = []
    for edge in candidates:
        endpoints = {edge["from"], edge["to"]}
        if 200 in endpoints:
            assert edge["edgeId"] == "E-086" and endpoints == {199, 200}
        else:
            assert edge["from"] in range(1, 200) and edge["to"] in range(1, 200)
        assert edge["transport"] in SUPPORTED_TRANSPORTS
        transport_counts[edge["transport"]] += 1
        pairs[tuple(sorted((edge["from"], edge["to"])))].add(edge["transport"])
        if edge["verificationStatus"] == "unresolved":
            unresolved.append(edge["edgeId"])
    assert dict(transport_counts) == {"taxi": 66, "bus": 33, "underground": 22, "boat": 4}
    assert sum(len(types) > 1 for types in pairs.values()) == 9
    assert unresolved == ["E-122", "E-123", "E-124", "E-125"]

    assert len(batches) == 20
    covered = [station_id for batch in batches for station_id in batch["stationIds"]]
    assert sorted(covered) == list(range(1, 200)) and len(covered) == len(set(covered)) == 199
    candidate_map = {edge["edgeId"]: edge for edge in candidates}
    for batch in batches:
        stations = batch["stationIds"]
        assert stations == sorted(stations)
        assert len(stations) == len(set(stations))
        assert all(station_id in range(1, 200) for station_id in stations)
        assert len(batch["candidateIds"]) == len(set(batch["candidateIds"]))
        assert all(candidate_id in candidate_map for candidate_id in batch["candidateIds"])
        expected = {edge_id for edge_id, edge in candidate_map.items() if edge["from"] in stations or edge["to"] in stations}
        assert set(batch["candidateIds"]) == expected

    manifest = json.loads((DATA / "phase-3e2a-workspace/station-crop-manifest.json").read_text(encoding="utf-8"))
    observations = load("new-edge-observations.json")["observations"]
    observation_ids = validate_observation_relationships(observations, candidate_map, {record["cropId"] for record in manifest["stations"]})
    assert summary["automaticPromotion"] is False
    assert summary["canonicalDataModified"] is False
    assert summary["marker200CandidateIds"] == ["E-086"]
    protected = {
        "stationsSha256": REPO / "packages/board-data/data/stations.json",
        "candidateDatasetSha256": DATA / "board-edge-candidates-1-200.json",
        "stationReviewQueueSha256": DATA / "phase-3e2a-workspace/station-review-queue.json",
        "edgeObservationsSha256": DATA / "phase-3e2a-workspace/edge-observations.json",
    }
    actual_hashes = {key: sha256(path) for key, path in protected.items()}
    assert summary["protectedInputs"] == actual_hashes
    b01 = next(batch for batch in batches if batch["batchId"] == "B-01")
    b02 = next(batch for batch in batches if batch["batchId"] == "B-02")
    assert all(set(observation.get("relatedCandidateIds", [])) <= (set(b01["candidateIds"]) | set(b02["candidateIds"])) for observation in observations)
    validate_batch_isolation(observations, batches)
    observation_by_id = {observation["observationId"]: observation for observation in observations}
    for batch in (b01, b02):
        for observation_id in batch.get("newObservationIds", []):
            assert set(observation_by_id[observation_id].get("relatedCandidateIds", [])) <= set(batch["candidateIds"])
    assert summary["newObservationCount"] == len(observation_ids)
    return {"candidateCount": 125, "transportCounts": dict(transport_counts), "multiTransportPairs": 9, "unresolvedCandidateIds": unresolved, "newObservationCount": len(observation_ids), "batchCount": 20, "stationCount": 199, "b01Status": b01["reviewStatus"]}


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2))
