import copy
import json
import importlib.util
import re
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DATA = REPO / "docs" / "game" / "data"
WORK = DATA / "phase-3e2b1-reconstruction"
VALIDATOR_SPEC = importlib.util.spec_from_file_location("phase_3e2b1_validate", REPO / "tools" / "phase_3e2b1_validate.py")
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)
PILOT_SPEC = importlib.util.spec_from_file_location("phase_3e2b2_pilot_b01", REPO / "tools" / "phase_3e2b2_pilot_b01.py")
PILOT = importlib.util.module_from_spec(PILOT_SPEC)
PILOT_SPEC.loader.exec_module(PILOT)
PILOT_B02_SPEC = importlib.util.spec_from_file_location("phase_3e2b3_pilot_b02", REPO / "tools" / "phase_3e2b3_pilot_b02.py")
PILOT_B02 = importlib.util.module_from_spec(PILOT_B02_SPEC)
PILOT_B02_SPEC.loader.exec_module(PILOT_B02)


class TestPhase3E2B1Pipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((DATA / "board-edge-candidates-1-200.json").read_text(encoding="utf-8"))["edges"]
        cls.imported = json.loads((WORK / "candidate-import.json").read_text(encoding="utf-8"))["candidates"]
        cls.new = json.loads((WORK / "new-edge-observations.json").read_text(encoding="utf-8"))["observations"]
        cls.batches = json.loads((WORK / "review-batches.json").read_text(encoding="utf-8"))["batches"]
        cls.summary = json.loads((WORK / "reconstruction-summary.json").read_text(encoding="utf-8"))
        cls.schema = json.loads((WORK / "phase-3e2b1-observation.schema.json").read_text(encoding="utf-8"))
        cls.candidate_map = {edge["edgeId"]: edge for edge in cls.imported}
        cls.crop_ids = {record["cropId"] for record in json.loads((DATA / "phase-3e2a-workspace/station-crop-manifest.json").read_text(encoding="utf-8"))["stations"]}

    def test_all_stations_covered_once(self):
        covered = [station_id for batch in self.batches for station_id in batch["stationIds"]]
        self.assertEqual(covered, list(range(1, 200)))

    def test_all_candidates_imported_once_and_unchanged(self):
        self.assertEqual(len(self.imported), 125)
        self.assertEqual([edge["edgeId"] for edge in self.imported], [edge["edgeId"] for edge in self.source])
        self.assertEqual(self.imported, self.source)

    def test_candidate_invariants(self):
        self.assertEqual([edge["edgeId"] for edge in self.imported], [f"E-{i:03d}" for i in range(1, 126)])
        self.assertEqual({edge["transport"] for edge in self.imported}, {"taxi", "bus", "underground", "boat"})
        self.assertEqual({transport: sum(edge["transport"] == transport for edge in self.imported) for transport in ("taxi", "bus", "underground", "boat")}, {"taxi": 66, "bus": 33, "underground": 22, "boat": 4})
        self.assertEqual([edge["edgeId"] for edge in self.imported if edge["verificationStatus"] == "unresolved"], ["E-122", "E-123", "E-124", "E-125"])
        self.assertEqual(self.summary["marker200CandidateIds"], ["E-086"])

    def test_batch_candidate_references_are_complete(self):
        for batch in self.batches:
            expected = {edge["edgeId"] for edge in self.imported if edge["from"] in batch["stationIds"] or edge["to"] in batch["stationIds"]}
            self.assertEqual(set(batch["candidateIds"]), expected)
            self.assertEqual(len(batch["candidateIds"]), len(set(batch["candidateIds"])))

    def test_observations_are_positive_schema_and_relationship_fixtures(self):
        ids = VALIDATOR.validate_observation_relationships(self.new, self.candidate_map, self.crop_ids)
        self.assertEqual(ids, [f"OBS-3E2B1-{i:05d}" for i in range(1, 28)])

    def test_schema_keywords_are_explicitly_covered(self):
        self.assertEqual(set(self.schema), {"$schema", "title", "type", "required", "properties", "additionalProperties"})
        instance_keywords = {"type", "required", "properties", "additionalProperties", "pattern", "minimum", "maximum", "enum", "minLength", "items"}
        nested_keywords = set()
        for definition in self.schema["properties"].values():
            nested_keywords.update(definition)
        self.assertTrue(instance_keywords <= set(self.schema) | nested_keywords)

    def assert_invalid_observation(self, mutate):
        bad = copy.deepcopy(self.new[0])
        mutate(bad)
        with self.assertRaises(AssertionError):
            VALIDATOR.validate_observation_relationships([bad], self.candidate_map, self.crop_ids)

    def test_negative_invalid_transport(self):
        self.assert_invalid_observation(lambda item: item.update(transport="rail"))

    def test_negative_missing_required_field_and_unexpected_property(self):
        self.assert_invalid_observation(lambda item: item.pop("evidenceDescription"))
        self.assert_invalid_observation(lambda item: item.update(unexpected=True))

    def test_negative_incorrect_field_types(self):
        self.assert_invalid_observation(lambda item: item.update({"from": "bad"}))
        self.assert_invalid_observation(lambda item: item.update(sourceCropIds="ST-001"))

    def test_negative_invalid_confidence_and_status(self):
        self.assert_invalid_observation(lambda item: item.update(confidence="certain"))
        self.assert_invalid_observation(lambda item: item.update(reviewStatus="accepted"))

    def test_negative_array_item_and_string_constraints(self):
        self.assert_invalid_observation(lambda item: item.update(sourceCropIds=[7]))
        self.assert_invalid_observation(lambda item: item.update(observationId="OBS-3E2B1-1"))
        self.assert_invalid_observation(lambda item: item.update(evidenceDescription=""))

    def test_negative_invalid_endpoint(self):
        self.assert_invalid_observation(lambda item: item.update(to=200))

    def test_negative_duplicate_id(self):
        bad = copy.deepcopy(self.new[:2])
        bad[1]["observationId"] = bad[0]["observationId"]
        with self.assertRaises(AssertionError):
            VALIDATOR.validate_observation_relationships(bad, self.candidate_map, self.crop_ids)

    def test_negative_missing_crop(self):
        self.assert_invalid_observation(lambda item: item.update(sourceCropIds=["ST-999"]))

    def test_negative_mismatched_candidate(self):
        self.assert_invalid_observation(lambda item: item.update(relatedCandidateIds=["E-002"]))

    def test_negative_self_reference_and_duplicate_reference(self):
        self.assert_invalid_observation(lambda item: item.update(supportingObservationIds=[item["observationId"]]))
        self.assert_invalid_observation(lambda item: item.update(duplicateOfObservationId=item["observationId"]))

    def test_negative_invalid_and_cyclic_relationships(self):
        bad = copy.deepcopy(self.new[:2])
        bad[0]["supportingObservationIds"] = ["OBS-3E2B1-99999"]
        with self.assertRaises(AssertionError):
            VALIDATOR.validate_observation_relationships(bad, self.candidate_map, self.crop_ids)
        cyclic = copy.deepcopy(self.new[:2])
        cyclic[0]["supportingObservationIds"] = [cyclic[1]["observationId"]]
        cyclic[1]["supportingObservationIds"] = [cyclic[0]["observationId"]]
        with self.assertRaises(AssertionError):
            VALIDATOR.validate_observation_relationships(cyclic, self.candidate_map, self.crop_ids)

    def test_negative_endpoint_crop_mapping(self):
        self.assert_invalid_observation(lambda item: item.update(sourceCropIds=["ST-001", "ST-007"]))

    def test_negative_non_active_batch_observation_id(self):
        batches = copy.deepcopy(self.batches)
        next(batch for batch in batches if batch["batchId"] == "B-03")["newObservationIds"] = [self.new[0]["observationId"]]
        with self.assertRaises(AssertionError):
            VALIDATOR.validate_batch_isolation(self.new, batches)

    def test_negative_duplicate_b01_observation_id(self):
        batches = copy.deepcopy(self.batches)
        b01 = next(batch for batch in batches if batch["batchId"] == "B-01")
        b01["newObservationIds"].append(b01["newObservationIds"][0])
        with self.assertRaises(AssertionError):
            VALIDATOR.validate_batch_isolation(self.new, batches)

    def test_pilot_refuses_later_batch_observations(self):
        with tempfile.TemporaryDirectory() as directory:
            original_work = PILOT.WORK
            try:
                PILOT.WORK = Path(directory)
                (PILOT.WORK / "new-edge-observations.json").write_text(json.dumps({"observations": [{"observationId": "OBS-LATER"}]}), encoding="utf-8")
                (PILOT.WORK / "review-batches.json").write_text(json.dumps({"batches": [{"batchId": "B-01", "newObservationIds": []}, {"batchId": "B-02", "newObservationIds": ["OBS-LATER"]}]}), encoding="utf-8")
                (PILOT.WORK / "reconstruction-summary.json").write_text(json.dumps({}), encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, "later batch"):
                    PILOT.main()
            finally:
                PILOT.WORK = original_work

    def test_pilot_preserves_unrelated_observation(self):
        with tempfile.TemporaryDirectory() as directory:
            original_work = PILOT.WORK
            try:
                PILOT.WORK = Path(directory)
                unrelated = {"observationId": "OBS-UNRELATED"}
                (PILOT.WORK / "new-edge-observations.json").write_text(json.dumps({"observations": [unrelated]}), encoding="utf-8")
                (PILOT.WORK / "review-batches.json").write_text(json.dumps({"batches": [{"batchId": "B-01", "reviewStatus": "uncertain", "newObservationIds": [observation["observationId"] for observation in PILOT.OBSERVATIONS]}, {"batchId": "B-02", "reviewStatus": "not-started", "newObservationIds": []}]}), encoding="utf-8")
                (PILOT.WORK / "reconstruction-summary.json").write_text(json.dumps({}), encoding="utf-8")
                PILOT.main()
                result = json.loads((PILOT.WORK / "new-edge-observations.json").read_text(encoding="utf-8"))["observations"]
                result_ids = [observation["observationId"] for observation in result]
                self.assertEqual(result_ids.count("OBS-UNRELATED"), 1)
                for observation in PILOT.OBSERVATIONS:
                    self.assertEqual(result_ids.count(observation["observationId"]), 1)
                batches = json.loads((PILOT.WORK / "review-batches.json").read_text(encoding="utf-8"))["batches"]
                b02 = next(batch for batch in batches if batch["batchId"] == "B-02")
                self.assertEqual(b02["reviewStatus"], "not-started")
                self.assertEqual(b02["newObservationIds"], [])
            finally:
                PILOT.WORK = original_work

    def test_pilot_refuses_preserved_pilot_id_collision(self):
        with tempfile.TemporaryDirectory() as directory:
            original_work = PILOT.WORK
            try:
                PILOT.WORK = Path(directory)
                collision = {"observationId": PILOT.OBSERVATIONS[0]["observationId"]}
                (PILOT.WORK / "new-edge-observations.json").write_text(json.dumps({"observations": [collision]}), encoding="utf-8")
                (PILOT.WORK / "review-batches.json").write_text(json.dumps({"batches": [{"batchId": "B-01", "newObservationIds": []}, {"batchId": "B-02", "reviewStatus": "not-started", "newObservationIds": []}]}), encoding="utf-8")
                (PILOT.WORK / "reconstruction-summary.json").write_text(json.dumps({}), encoding="utf-8")
                with self.assertRaisesRegex(RuntimeError, "collides"):
                    PILOT.main()
            finally:
                PILOT.WORK = original_work

    def _run_b02_fixture(self, ledger_observations, batches, expect_error=None):
        with tempfile.TemporaryDirectory() as directory:
            original_work = PILOT_B02.WORK
            try:
                PILOT_B02.WORK = Path(directory)
                ledger_path = PILOT_B02.WORK / "new-edge-observations.json"
                batches_path = PILOT_B02.WORK / "review-batches.json"
                summary_path = PILOT_B02.WORK / "reconstruction-summary.json"
                ledger_path.write_text(json.dumps({"observations": ledger_observations}), encoding="utf-8")
                batches_path.write_text(json.dumps({"batches": batches}), encoding="utf-8")
                summary_path.write_text(json.dumps({"newObservationCount": len(ledger_observations)}), encoding="utf-8")
                before = {path.name: path.read_bytes() for path in (ledger_path, batches_path, summary_path)}
                if expect_error:
                    with self.assertRaisesRegex(RuntimeError, expect_error):
                        PILOT_B02.main()
                    self.assertEqual(before, {path.name: path.read_bytes() for path in (ledger_path, batches_path, summary_path)})
                    return None
                PILOT_B02.main()
                return {
                    "ledger": json.loads(ledger_path.read_text(encoding="utf-8")),
                    "batches": json.loads(batches_path.read_text(encoding="utf-8"))["batches"],
                }
            finally:
                PILOT_B02.WORK = original_work

    def test_b02_script_preserves_b01_unrelated_and_later_batches(self):
        b01 = copy.deepcopy(self.new[:12])
        b02 = copy.deepcopy(self.new[12:])
        unrelated = {"observationId": "OBS-UNRELATED-B02"}
        batches = [
            {"batchId": "B-01", "reviewStatus": "uncertain", "newObservationIds": [item["observationId"] for item in b01]},
            {"batchId": "B-02", "reviewStatus": "uncertain", "newObservationIds": [item["observationId"] for item in b02]},
        ] + [{"batchId": f"B-{index:02d}", "reviewStatus": "not-started", "newObservationIds": []} for index in range(3, 21)]
        result = self._run_b02_fixture(b01 + b02 + [unrelated], batches)
        result_ids = [item["observationId"] for item in result["ledger"]["observations"]]
        self.assertEqual(result["ledger"]["observations"][:12], b01)
        self.assertEqual(result_ids.count("OBS-UNRELATED-B02"), 1)
        for item in b02:
            self.assertEqual(result_ids.count(item["observationId"]), 1)
        b02_result = next(batch for batch in result["batches"] if batch["batchId"] == "B-02")
        self.assertEqual(b02_result["reviewStatus"], "uncertain")
        self.assertEqual(b02_result["newObservationIds"], [item["observationId"] for item in b02])
        self.assertTrue(all(batch["reviewStatus"] == "not-started" and batch["newObservationIds"] == [] for batch in result["batches"] if int(batch["batchId"][2:]) >= 3))

    def test_b02_script_rerun_does_not_duplicate(self):
        b01 = copy.deepcopy(self.new[:12])
        b02 = copy.deepcopy(self.new[12:])
        batches = [{"batchId": "B-01", "reviewStatus": "uncertain", "newObservationIds": [item["observationId"] for item in b01]}, {"batchId": "B-02", "reviewStatus": "uncertain", "newObservationIds": [item["observationId"] for item in b02]}]
        result = self._run_b02_fixture(b01 + b02, batches)
        result_ids = [item["observationId"] for item in result["ledger"]["observations"]]
        self.assertEqual(len(result_ids), len(set(result_ids)))

    def test_b02_script_refuses_later_collision(self):
        batches = [{"batchId": "B-01", "reviewStatus": "uncertain", "newObservationIds": [item["observationId"] for item in self.new[:12]]}, {"batchId": "B-02", "reviewStatus": "not-started", "newObservationIds": []}, {"batchId": "B-03", "reviewStatus": "not-started", "newObservationIds": ["OBS-LATER"]}]
        self._run_b02_fixture(self.new[:12] + [{"observationId": "OBS-LATER"}], batches, "later batch")

    def test_b02_script_refuses_pilot_collision(self):
        batches = [{"batchId": "B-01", "reviewStatus": "uncertain", "newObservationIds": [item["observationId"] for item in self.new[:12]]}, {"batchId": "B-02", "reviewStatus": "not-started", "newObservationIds": []}]
        self._run_b02_fixture(self.new[:12] + [copy.deepcopy(self.new[12])], batches, "collides")

    def test_b02_script_refuses_b01_id_assigned_to_b02(self):
        batches = [{"batchId": "B-01", "reviewStatus": "uncertain", "newObservationIds": [item["observationId"] for item in self.new[:12]]}, {"batchId": "B-02", "reviewStatus": "not-started", "newObservationIds": [self.new[0]["observationId"]]}]
        self._run_b02_fixture(self.new[:12], batches, "overlap")

    def test_exact_ambiguous_candidates_and_b01_note(self):
        self.assertEqual(["E-022", "E-023", "E-024"], [edge["edgeId"] for edge in self.imported if edge["edgeId"] in {"E-022", "E-023", "E-024"}])
        b01 = next(batch for batch in self.batches if batch["batchId"] == "B-01")
        self.assertEqual(b01["reviewStatus"], "uncertain")
        self.assertIn("three bus candidates", b01["reviewNote"])

    def test_b03_to_b20_not_started(self):
        self.assertTrue(all(batch["reviewStatus"] == "not-started" and batch.get("newObservationIds", []) == [] for batch in self.batches if batch["batchId"] not in {"B-01", "B-02"}))

    def test_b02_observations_are_exactly_listed(self):
        b02 = next(batch for batch in self.batches if batch["batchId"] == "B-02")
        self.assertEqual(b02["reviewStatus"], "uncertain")
        self.assertEqual(b02["newObservationIds"], [f"OBS-3E2B1-{i:05d}" for i in range(13, 28)])

    def test_dashboard_is_read_only_with_links(self):
        dashboard = (WORK / "review-dashboard.html").read_text(encoding="utf-8")
        self.assertIn("Read-only index", dashboard)
        self.assertIn("<a href=", dashboard)
        self.assertNotIn("<select", dashboard)

    def test_observations_are_explicit_and_no_automatic_promotion(self):
        self.assertEqual(len(self.new), 27)
        self.assertEqual([observation["observationId"] for observation in self.new], [f"OBS-3E2B1-{i:05d}" for i in range(1, 28)])
        self.assertFalse(self.summary["automaticPromotion"])
        self.assertFalse(self.summary["canonicalDataModified"])

    def test_batch_generation_is_deterministic(self):
        self.assertEqual(len(self.batches), 20)
        self.assertEqual([batch["batchId"] for batch in self.batches], [f"B-{i:02d}" for i in range(1, 21)])

    def test_existing_multitransport_candidates_are_retained(self):
        pairs = {}
        for edge in self.imported:
            pair = tuple(sorted((edge["from"], edge["to"])))
            pairs.setdefault(pair, set()).add(edge["transport"])
        self.assertGreaterEqual(sum(len(types) > 1 for types in pairs.values()), 1)

    def test_summary_counts(self):
        self.assertEqual(self.summary["candidateCount"], 125)
        self.assertEqual(self.summary["newObservationCount"], 27)
        self.assertEqual(self.summary["batchCount"], 20)


if __name__ == "__main__":
    unittest.main()
