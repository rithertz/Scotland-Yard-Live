import json
import math
import sys
import unittest
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent.parent
OUT = TOOL_DIR / "output" / "station_recovery"
sys.path.insert(0, str(TOOL_DIR))


class TestPhase3D2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads((OUT / "station_inventory.json").read_text(encoding="utf-8"))
        cls.mapping = json.loads((OUT / "station_evidence_mapping.json").read_text(encoding="utf-8"))
        cls.matrix = json.loads((OUT / "station_recovery_completeness.json").read_text(encoding="utf-8"))

    def test_exact_playable_range_once(self):
        ids = [s["station_id"] for s in self.inventory["stations"]]
        self.assertEqual(ids, list(range(1, 200)))

    def test_counts_sum_to_199(self):
        counts = self.inventory["metadata"]["summary_counts"]
        self.assertEqual(sum(counts.values()), 199)

    def test_assignment_integrity(self):
        assigned = [s for s in self.inventory["stations"] if s["status"] in ("verified", "candidate_uncertain")]
        self.assertEqual(len({s["feature_id"] for s in assigned}), len(assigned))
        for station in assigned:
            self.assertIsNotNone(station["source_coordinates"])
            self.assertTrue(all(math.isfinite(float(v)) for v in station["source_coordinates"]["canvas"]))
            self.assertTrue(0 <= station["normalized_x"] <= 1)
            self.assertTrue(0 <= station["normalized_y"] <= 1)

    def test_marker_200_separate(self):
        self.assertNotIn(200, [s["station_id"] for s in self.inventory["stations"]])
        self.assertEqual(self.mapping["marker_200"]["observed_marker_id"], 200)

    def test_missing_is_explicit(self):
        for station in self.matrix["entries"]:
            if station["status"] == "missing_from_evidence":
                self.assertIsNone(station["feature_id"])
                self.assertIsNone(station["pixel_x"])
                self.assertIsNone(station["pixel_y"])


if __name__ == "__main__":
    unittest.main()
