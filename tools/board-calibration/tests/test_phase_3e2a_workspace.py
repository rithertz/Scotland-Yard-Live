import hashlib
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
WORK = REPO / "docs" / "game" / "data" / "phase-3e2a-workspace"


class TestPhase3E2AWorkspace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((WORK / "station-crop-manifest.json").read_text(encoding="utf-8"))
        cls.queue = json.loads((WORK / "station-review-queue.json").read_text(encoding="utf-8"))
        cls.obs = json.loads((WORK / "edge-observations.json").read_text(encoding="utf-8"))
        cls.candidate = REPO / "docs" / "game" / "data" / "board-edge-candidates-1-200.json"
        cls.station = REPO / "packages" / "board-data" / "data" / "stations.json"

    def test_all_stations_have_one_primary_crop(self):
        self.assertEqual(self.manifest["cropCount"], 199)
        self.assertEqual({x["stationId"] for x in self.manifest["stations"]}, set(range(1, 200)))
        self.assertEqual(self.queue["queueCount"], 199)
        self.assertEqual({x["stationId"] for x in self.queue["queue"]}, set(range(1, 200)))

    def test_crop_bounds_and_files(self):
        for crop in self.manifest["stations"]:
            rect = crop["registeredCanvasCrop"]
            self.assertGreaterEqual(rect["x"], 0)
            self.assertGreaterEqual(rect["y"], 0)
            self.assertLessEqual(rect["x"] + rect["width"], 1350)
            self.assertLessEqual(rect["y"] + rect["height"], 1000)
            self.assertTrue((REPO / crop["registeredCropPath"]).exists())
            if crop["sourceCropPath"]:
                self.assertTrue((REPO / crop["sourceCropPath"]).exists())

    def test_source_inventory_is_readable(self):
        self.assertGreaterEqual(len(self.manifest["sources"]), 27)
        self.assertTrue(all(source["exists"] and source["readable"] for source in self.manifest["sources"]))

    def test_existing_candidates_imported_once(self):
        observations = self.obs["observations"]
        self.assertEqual(len(observations), 125)
        self.assertEqual({x["candidateId"] for x in observations}, {f"E-{i:03d}" for i in range(1, 126)})
        self.assertEqual(len({x["observationId"] for x in observations}), 125)

    def test_observation_constraints(self):
        for observation in self.obs["observations"] + self.obs["newObservations"]:
            self.assertGreaterEqual(observation["from"], 1)
            self.assertLessEqual(observation["from"], 200)
            self.assertGreaterEqual(observation["to"], 1)
            self.assertLessEqual(observation["to"], 200)
            if observation["endpointScope"] == "playable":
                self.assertLessEqual(observation["from"], 199)
                self.assertLessEqual(observation["to"], 199)
            else:
                self.assertIn(200, (observation["from"], observation["to"]))
            self.assertIn(observation["transport"], {"taxi", "bus", "underground", "boat"})

    def test_protected_inputs_unchanged(self):
        for path, expected in self.manifest["sourceHashes"].items():
            actual = hashlib.sha256((REPO / path).read_bytes()).hexdigest().upper()
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
