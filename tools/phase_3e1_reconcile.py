"""Generate the Phase 3E.1 transport-candidate evidence reconciliation audit."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import cv2

REPO = Path(__file__).resolve().parents[1]
CANDIDATE = REPO / "docs" / "game" / "data" / "board-edge-candidates-1-200.json"
OUT_JSON = REPO / "docs" / "game" / "data" / "phase-3e-1-reconciliation.json"
OUT_MD = REPO / "docs" / "game" / "PHASE-3E-1-EVIDENCE-RECONCILIATION.md"
PHOTO_ROOT = REPO / "docs" / "game" / "evidence" / "board-photos"

SOURCE_MAP = {
    "complete.jpeg": PHOTO_ROOT / "original-references" / "complete.jpeg",
    "top-left.jpeg": PHOTO_ROOT / "original-references" / "top-left.jpeg",
    "top-right.jpeg": PHOTO_ROOT / "original-references" / "top-right.jpeg",
    "bottom-left.jpeg": PHOTO_ROOT / "original-references" / "bottom-left.jpeg",
    "bottom-right.jpeg": PHOTO_ROOT / "original-references" / "bottom-right.jpeg",
}
MULTI_PAIRS = {(11, 22), (13, 14), (14, 15), (102, 115), (105, 107), (127, 133), (133, 140), (156, 157), (105, 108)}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()


def inspect_source(name: str) -> dict[str, Any]:
    path = SOURCE_MAP[name]
    result: dict[str, Any] = {"referenced_name": name, "actual_path": str(path.relative_to(REPO)), "exists": path.exists()}
    if not path.exists():
        result.update({"readable": False, "relevant": False, "sufficient": False, "limitation": "Referenced source was not found."})
        return result
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    result.update({"readable": image is not None, "sha256": sha256(path), "dimensions": [int(image.shape[1]), int(image.shape[0])] if image is not None else None,
                   "relevant": True, "sufficient": False,
                   "limitation": "Source image is readable and region-relevant, but no edge-specific endpoint crop or independent line trace is stored for this candidate."})
    return result


def inspect_actual_evidence_tree() -> dict[str, Any]:
    records = []
    for folder, pattern, role in (("original-references", "*.jpeg", "original board reference"), ("closeups", "*.jpg", "close-up board evidence"), ("high-resolution", "*.jpg", "high-resolution board tile")):
        for path in sorted((PHOTO_ROOT / folder).glob(pattern)):
            image = cv2.imread(str(path), cv2.IMREAD_COLOR)
            records.append({"filename": path.name, "relative_path": str(path.relative_to(REPO)), "role": role, "exists": True,
                            "readable": image is not None, "dimensions": [int(image.shape[1]), int(image.shape[0])] if image is not None else None,
                            "sha256": sha256(path)})
    generated = []
    for path in sorted((REPO / "tools" / "board-calibration" / "output").glob("rectified_complete.png")):
        image = cv2.imread(str(path), cv2.IMREAD_COLOR)
        generated.append({"filename": path.name, "relative_path": str(path.relative_to(REPO)), "role": "derived registered board image", "exists": True, "readable": image is not None, "dimensions": [int(image.shape[1]), int(image.shape[0])] if image is not None else None})
    return {"photographs": records, "derivedImages": generated, "rulebook": {"found": False, "readable": False, "note": "No PDF or other rulebook file was located in the repository tree."}, "projectPlan": {"found": False, "note": "Scotland-Yard-Live-Consolidated-Project-Plan.md was not located in the repository tree."}}


def main() -> None:
    original_bytes = CANDIDATE.read_bytes()
    data = json.loads(original_bytes)
    edges = data["edges"]
    expected_ids = {f"E-{i:03d}" for i in range(1, 126)}
    actual_ids = {edge["edgeId"] for edge in edges}
    assert len(edges) == 125, f"Expected 125 candidates, got {len(edges)}"
    assert len(actual_ids) == 125, "Candidate IDs are not unique"
    assert actual_ids == expected_ids, "Candidate IDs differ from the original E-001..E-125 set"
    assert Counter(edge["transport"] for edge in edges) == Counter({"taxi": 66, "bus": 33, "underground": 22, "boat": 4})
    assert Counter(edge["verificationStatus"] for edge in edges) == Counter({"provisional": 121, "unresolved": 4})
    sources = {name: inspect_source(name) for name in SOURCE_MAP}
    actual_evidence = inspect_actual_evidence_tree()
    station_path = REPO / "packages" / "board-data" / "data" / "stations.json"
    station_bytes = station_path.read_bytes()
    station_data = json.loads(station_bytes)
    station_ids = [station["id"] for station in station_data["stations"]]
    assert len(station_ids) == 199 and station_ids == list(range(1, 200)), "Station dataset must contain IDs 1..199 exactly once"
    assert all(station.get("coordinate") and 0 <= station["coordinate"]["x"] <= 1 and 0 <= station["coordinate"]["y"] <= 1 for station in station_data["stations"]), "Station coordinates must be normalized"
    assert 200 not in station_ids, "Marker 200 must remain outside playable station data"
    station_validation = {"path": str(station_path.relative_to(REPO)), "sha256": hashlib.sha256(station_bytes).hexdigest().upper(), "byteLength": len(station_bytes), "count": len(station_ids), "idsComplete": True, "coordinatesComplete": True, "marker200Excluded": True, "state": station_data["metadata"].get("state")}
    groups: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for edge in edges:
        groups[tuple(sorted((edge["from"], edge["to"])))].append(edge)

    records = []
    for edge in edges:
        pair = tuple(sorted((edge["from"], edge["to"])))
        referenced = [sources[e["file"]] for e in edge.get("evidence", []) if e.get("file") in sources]
        missing_references = [e.get("file") for e in edge.get("evidence", []) if e.get("file") not in sources]
        unresolved = edge["verificationStatus"] == "unresolved"
        classification = "ambiguous-evidence" if unresolved else "partial-evidence"
        if pair in MULTI_PAIRS:
            next_action = "Review this multi-transport endpoint pair in an annotated endpoint crop; independently trace each transport marking."
        elif edge["transport"] == "boat":
            next_action = "Compare a dedicated Thames endpoint crop with rulebook page 10; trace the physical line without relying on route wording."
        elif edge["confidence"] == "low":
            next_action = "Review the cited region at high resolution with both endpoint labels and the complete route segment visible."
        else:
            next_action = "Obtain or inspect an edge-specific crop and reproduce endpoint plus transport-line reading before any promotion."
        records.append({
            "edgeId": edge["edgeId"],
            "from": edge["from"], "to": edge["to"], "transport": edge["transport"],
            "existingConfidence": edge["confidence"], "existingVerificationStatus": edge["verificationStatus"],
            "existingEvidence": edge.get("evidence", []), "approximateImageRegion": edge.get("approximateImageRegion"),
            "sourceInventory": referenced,
            "missingEvidenceReferences": missing_references,
            "endpointAReadable": None, "endpointBReadable": None,
            "connectingRouteActuallyVisible": None, "transportIdentityVisuallySupported": None,
            "reconciliationClassification": classification,
            "evidenceBasis": "The referenced board photo exists, decodes and covers the named region; this audit does not have a stored edge-specific crop or independently reproducible endpoint/line trace.",
            "contradictoryEvidence": False,
            "nextReviewAction": next_action,
            "reviewerNote": edge.get("visualExplanation", "") + (" Existing unresolved status retained; do not resolve by inference." if unresolved else " Candidate remains non-canonical; partial evidence is not verification."),
        })

    counts = {
        "total": len(records),
        "byTransport": dict(Counter(e["transport"] for e in edges)),
        "byExistingStatus": dict(Counter(e["verificationStatus"] for e in edges)),
        "byExistingConfidence": dict(Counter(e["confidence"] for e in edges)),
        "byReconciliation": dict(Counter(r["reconciliationClassification"] for r in records)),
        "withReadableReferencedSources": sum(bool(r["sourceInventory"]) and all(s["readable"] for s in r["sourceInventory"]) for r in records),
        "withDirectVisualEvidence": sum(r["reconciliationClassification"] == "direct-evidence-referenced" for r in records),
        "withMissingOrInsufficientEvidence": sum(r["reconciliationClassification"] in ("missing-evidence", "ambiguous-evidence") or any(not s["sufficient"] for s in r["sourceInventory"]) for r in records),
    }
    unresolved = [r for r in records if r["existingVerificationStatus"] == "unresolved"]
    assert {r["edgeId"] for r in unresolved} == {"E-122", "E-123", "E-124", "E-125"}
    assert {tuple(sorted((r["from"], r["to"]))) for r in records if len(groups[tuple(sorted((r["from"], r["to"])))]) > 1} == MULTI_PAIRS
    assert all(not r["missingEvidenceReferences"] or r["reconciliationClassification"] == "missing-evidence" for r in records)
    assert all(r["sourceInventory"] and all(s["exists"] and s["readable"] for s in r["sourceInventory"]) for r in records)
    multi = {f"{a}-{b}": [{"edgeId": r["edgeId"], "transport": r["transport"], "classification": r["reconciliationClassification"]} for r in records if tuple(sorted((r["from"], r["to"]))) == (a, b)] for a, b in sorted(MULTI_PAIRS)}
    boats = [r for r in records if r["transport"] == "boat"]
    audit = {"phase": "3E.1.1", "candidateFile": str(CANDIDATE.relative_to(REPO)), "candidateSha256": sha256(CANDIDATE), "candidateByteLength": len(original_bytes),
             "sourceInventory": list(sources.values()), "actualEvidenceInventory": actual_evidence, "stationDatasetValidation": station_validation, "summary": counts, "candidates": records, "multiTransportPairs": multi, "unresolvedCandidates": unresolved,
             "boatAssessment": {"rulebookPdfFound": False, "rulebookPage10Inspected": False, "documentedRulebookStatements": [[194, 157], [157, 115], [115, 118]], "candidateRows": boats, "108-115Finding": "No rulebook PDF is available in the repository; historical documentation says page 10 does not support 108-115. The candidate remains unresolved."},
             "station200Dependency": {"candidateId": "E-086", "endpoint": [199, 200], "status": "unresolved-inventory-dependency", "note": "Marker 200 is physically photographed, but playability/edition status remains unresolved."},
             "startingPositionsDependency": {"rulebookCards": 18, "historicallyLegibleValues": 13, "status": "incomplete", "note": "No complete starting-card source is available in this repository; do not infer graph edges from it."}}
    OUT_JSON.write_text(json.dumps(audit, indent=2), encoding="utf-8")

    lines = []
    lines += ["# Phase 3E.1.1 — Audit Integrity and Transport Reconstruction Readiness", "", "## 1. Purpose and scope", "", "This documentation-only audit reconciles the unchanged 125-row non-canonical transport-edge candidate artifact and prepares a practical complete-graph reconstruction workflow. It does not modify candidates, station data, transport data, validators or canonical availability, and it does not begin Phase 3E.2.", "", "The requested `Scotland-Yard-Live-Consolidated-Project-Plan.md` was not found in this checkout; existing board reconstruction and Phase 3D readiness documents were used instead and the absence is recorded below.", "", "## 2. Evidence authority and methodology", "", "Original board photographs and the rulebook would be primary evidence. In this repository, the five cited board photographs are present under `docs/game/evidence/board-photos/original-references/` and decode successfully. The historical candidate references use the basenames `complete.jpeg`, `top-left.jpeg`, `top-right.jpeg`, `bottom-left.jpeg` and `bottom-right.jpeg`; they resolve to those originals. No rulebook PDF is present. No edge-specific endpoint crops are present in the current evidence tree. Therefore the audit distinguishes source accessibility from edge sufficiency and does not treat historical visual explanations as independent verification.", "", "## 3. Actual evidence inventory", ""]
    lines += ["| Referenced source | Actual path | Exists/readable | Dimensions | Edge-sufficient |", "|---|---|---|---:|---|"]
    for s in sources.values(): lines.append(f"| `{s['referenced_name']}` | `{s['actual_path']}` | {s['exists']}/{s['readable']} | `{s.get('dimensions')}` | {s['sufficient']} |")
    lines += ["", f"Actual evidence files: {len(actual_evidence['photographs'])} photographs ({sum(x['readable'] for x in actual_evidence['photographs'])} readable), including 5 original references, 6 close-ups and 16 high-resolution tiles. Derived registered board images: {len(actual_evidence['derivedImages'])}. Rulebook found/readable: {actual_evidence['rulebook']['found']}/{actual_evidence['rulebook']['readable']}.", "", "High-resolution tiles A1–D4, six close-ups and calibrated overlays also exist, but they are not referenced by the 125 candidate rows and no candidate-specific endpoint crop maps them to a row. The rulebook PDF is unavailable in the repository, so page 10 could not be independently opened during this audit.", "", "## 4. Evidence accessibility and quality summary", "", f"The five referenced originals are readable: {counts['withReadableReferencedSources']}/125 candidate rows resolve to readable cited sources. All 125 rows have insufficient edge-specific evidence in the current repository: the source region is available, but endpoint labels, the complete connecting line and transport identity are not recorded as independently reviewable crop-level facts. Four rows are explicitly unresolved and are classified `ambiguous-evidence`; the remaining 121 are `partial-evidence`. No row is classified `direct-evidence-referenced` by this conservative audit.", "", "## 5. Reconciliation classifications", "", "- `direct-evidence-referenced`: not assigned; no edge-specific source was independently sufficient.\n- `partial-evidence`: cited readable board region exists, but the complete candidate observation is not independently established here.\n- `ambiguous-evidence`: source exists but the candidate itself is explicitly unresolved or endpoint/line interpretation is ambiguous.\n- `conflicting-evidence`: none established.\n- `missing-evidence`: none for the five cited photo basenames; rulebook evidence is unavailable separately.\n- `not-reviewed`: none.", "", "## 6. Full candidate-by-candidate reconciliation", "", "The machine-readable companion contains every row exactly once. The table below is the complete audit index.", "", "| ID | Endpoints | Transport | Existing confidence/status | Reconciliation | Source | Next review action |", "|---|---:|---|---|---|---|---|"]
    for r in records:
        src = ", ".join(sorted({x["referenced_name"] for x in r["sourceInventory"]})) or "none"
        lines.append(f"| `{r['edgeId']}` | {r['from']}–{r['to']} | {r['transport']} | {r['existingConfidence']} / {r['existingVerificationStatus']} | {r['reconciliationClassification']} | {src} | {r['nextReviewAction']} |")
    lines += ["", "## 7. Nine multi-transport pair assessments", "", "| Pair | Existing observations | Assessment |", "|---|---|---|"]
    for pair, items in multi.items(): lines.append(f"| `{pair}` | " + ", ".join(f"`{x['edgeId']}` {x['transport']}" for x in items) + " | Co-located multi-modal candidates require endpoint crops and separate transport-line traces; no observation is promoted by coexistence. |")
    lines += ["", "## 8. Four unresolved candidate assessments", "", "| ID | Endpoints/transport | What is known | What remains unresolved |", "|---|---|---|---|"]
    for r in unresolved: lines.append(f"| `{r['edgeId']}` | {r['from']}–{r['to']} / {r['transport']} | Cited readable source region exists; candidate is retained unchanged. | Complete endpoint and line trace; do not resolve by route inference. |")
    lines += ["", "## 9. Boat-route evidence comparison", "", "The repository has no rulebook PDF, so page 10 was not independently inspected. Historical project documentation records rulebook wording for `194–157`, `157–115` and `115–118`; those statements are not reclassified as physical-board verification here. The candidate `108–115` is not supported by the cited historical rulebook statement and remains unresolved. All four boat candidates remain unchanged and non-canonical.", "", "## 10. Station 200 dependency", "", "`E-086` records `199–200` as a provisional taxi candidate. Marker 200 is visibly represented in the physical-board evidence, but the 199-versus-200 playable-inventory decision remains unresolved. This audit neither removes nor promotes `E-086` and does not alter the station dataset.", "", "## 11. Starting-position evidence limitation", "", "Historical documentation records 18 rulebook start cards and 13 safely legible card-face values. The complete source is not available in this repository. The five missing values and their positions remain unresolved; no graph inference is made from starting cards.", "", "## 12. Reconciliation totals and consistency checks", "", f"| Metric | Count |\n|---|---:|\n| Total candidates | {counts['total']} |\n| Taxi | {counts['byTransport']['taxi']} |\n| Bus | {counts['byTransport']['bus']} |\n| Underground | {counts['byTransport']['underground']} |\n| Boat | {counts['byTransport']['boat']} |\n| Existing provisional | {counts['byExistingStatus']['provisional']} |\n| Existing unresolved | {counts['byExistingStatus']['unresolved']} |\n| Partial evidence | {counts['byReconciliation']['partial-evidence']} |\n| Ambiguous evidence | {counts['byReconciliation']['ambiguous-evidence']} |\n| Direct evidence | {counts['byReconciliation'].get('direct-evidence-referenced', 0)} |\n| Readable cited source rows | {counts['withReadableReferencedSources']} |\n| Missing or insufficient evidence | {counts['withMissingOrInsufficientEvidence']} |", "", "Consistency checks: 125 unique candidate IDs accounted for; no unknown IDs; transport totals are 66 taxi, 33 bus, 22 underground and 4 boat; reconciliation totals sum to 125; the original candidate file remains unchanged by this script.", "", "## 13. Practical complete-graph reconstruction strategy", "", "The efficient path to a usable graph is a station-centered crop workflow, not another broad audit:", "", "1. Build one review manifest for stations 1–199 from the existing station coordinates, with a fixed crop radius and overlap margin.\n2. For each station, inspect its incident coloured route lines in the high-resolution A1–D4 tiles, then record each endpoint, transport colour, source tile, source pixel coordinates and registered canvas coordinates in a row-level evidence worksheet.\n3. Reconcile the 125 existing candidates by stable endpoint pair plus transport; preserve the original candidate ID as a linked observation. New connections receive new audit observation IDs, not edits to the candidate file.\n4. Represent duplicate transport modes as separate records keyed by `(minEndpoint,maxEndpoint,transport)`; represent same-pair conflicting readings as separate observations until reviewed.\n5. Use `unresolved`/`candidate-unverified` audit states for unclear endpoints or lines. Never fill a gap from station proximity or expected network structure.\n6. Generate graph invariants after each review batch: IDs 1–199 only, no self-edges, no duplicate same-transport undirected edges, all endpoints resolve, and every accepted edge has a source crop.\n7. Review the nine multi-transport pairs and four boat rows first, then cross-boundary/fold regions, then complete the remaining station-centered queue. Only after a second review should a separate graph integration task produce renderer/game-engine input.", "", "## 14. Station dataset readiness", "", "`packages/board-data/data/stations.json` currently contains 199 unique IDs covering 1–199, all with finite normalized coordinates in bounds. Existing identity, provenance and confidence fields are preserved; marker 200 is excluded. The dataset is explicitly `incomplete-verification` and `bestEffort`, so it is usable as a visual workbench for approximate rendering, but it is not sufficient as canonical gameplay data. Rendering can begin against it only with an explicit approximate-data label and without treating its coordinates or feature associations as verified.", "", "## 15. Frontend board integration readiness", "", "The current frontend uses `DEMO_BOARD_FIXTURE` with synthetic station IDs, positions and routes. A future integration will need to replace that fixture with a board-data adapter, render the 199 normalized station positions over a real/reconstructed board background, load the reviewed transport graph, preserve responsive SVG scaling and pan/zoom, implement station selection and legal-move highlighting from graph adjacency, and render taxi/bus/underground/boat routes with distinct styles. The board-data package currently exports types/validation but does not export the station JSON as canonical; frontend replacement must wait for a separately approved graph/data integration task. No frontend code was changed here.", "", "## 16. Prioritized Phase 3E.2 review queue", "", "1. The nine multi-transport pairs: create endpoint-specific crops that show both labels and independently trace each coloured route.\n2. Boat candidates `E-122`–`E-125`: inspect rulebook page 10 when the source becomes available and compare against dedicated Thames crops.\n3. Low-confidence and unresolved rows, beginning with the four unresolved boat rows and the 22 low-confidence candidates.\n4. `E-086` (`199–200`): resolve the marker-200 edition/inventory decision before treating the endpoint as playable.\n5. Cross-boundary and fold-adjacent candidates: review registered high-resolution tiles only after attaching a row-specific crop and source coordinates.", "", "## 17. Limitations, non-conclusions and owner decisions", "", "This report does not verify any transport edge, does not resolve marker 200, does not complete starting positions and does not create a canonical graph. The absence of a direct classification means only that this audit lacks sufficient row-specific evidence in the repository; it is not a claim that no line is visible in every photograph.", "", "## 18. Phase 3E.1.1 completion statement", "", "Phase 3E.1.1 is complete as an audit-integrity and reconstruction-readiness milestone. All 125 existing candidate observations are accounted for exactly once, the candidate artifact remains unchanged, evidence accessibility and insufficiency are documented, a practical complete-graph strategy is provided, station readiness is assessed, and a prioritized Phase 3E.2 review queue is provided. Phase 3E.2 has not begun."]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert CANDIDATE.read_bytes() == original_bytes
    assert station_path.read_bytes() == station_bytes
    audit["candidateBytePreserved"] = True
    audit["stationDatasetBytePreserved"] = True
    OUT_JSON.write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps({"candidate_sha256": audit["candidateSha256"], "summary": counts}, indent=2))


if __name__ == "__main__":
    main()
