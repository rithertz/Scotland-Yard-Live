import json
import unittest
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent.parent
OUT = TOOL_DIR / "output" / "station_recovery"


class TestPhase3D3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.meta = json.loads((OUT / "phase_3d3_photo_metadata.json").read_text(encoding="utf-8"))
        cls.registration = json.loads((OUT / "phase_3d3_registration_metadata.json").read_text(encoding="utf-8"))
        cls.inventory = json.loads((OUT / "station_inventory_phase_3d3.json").read_text(encoding="utf-8"))
        cls.mapping = json.loads((OUT / "station_evidence_mapping_phase_3d3.json").read_text(encoding="utf-8"))
        cls.candidates = json.loads((OUT / "phase_3d3_physical_marker_candidates.json").read_text(encoding="utf-8"))

    def test_all_sixteen_sources_are_usable(self):
        self.assertEqual(len(self.meta["records"]), 16)
        self.assertTrue(all(record["status"] == "usable" for record in self.meta["records"]))

    def test_all_sources_registered(self):
        self.assertEqual(len(self.registration["registrations"]), 16)
        self.assertTrue(all(record["inliers"] >= 8 for record in self.registration["registrations"]))

    def test_playable_inventory_still_exactly_199(self):
        stations = self.inventory["stations"]
        self.assertEqual([station["station_id"] for station in stations], list(range(1, 200)))
        self.assertNotIn(200, [station["station_id"] for station in stations])

    def test_highres_candidates_are_not_identities(self):
        self.assertGreater(self.candidates["raw_observations"], 0)
        self.assertGreater(self.candidates["deduplicated_candidates"], 0)
        self.assertEqual(self.inventory["metadata"]["phase_3d3"]["identity_policy"], "preserve prior identity status until direct number-to-marker matching is documented")

    def test_phase3d3_preserves_prior_assignments(self):
        assigned = [s for s in self.inventory["stations"] if s["status"] in ("verified", "candidate_uncertain")]
        self.assertEqual({s["station_id"] for s in assigned}, {1, 3, 120, 123, 158, 199})
        self.assertEqual(self.mapping["marker_200"]["observed_marker_id"], 200)


if __name__ == "__main__":
    unittest.main()
