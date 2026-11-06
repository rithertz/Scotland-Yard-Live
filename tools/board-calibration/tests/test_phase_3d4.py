import json
import unittest
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "output" / "station_recovery"


class TestPhase3D4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((OUT / "station_transcription_phase_3d4.json").read_text(encoding="utf-8"))
        cls.audit = json.loads((OUT / "station_transcription_tile_audit_phase_3d4.json").read_text(encoding="utf-8"))

    def test_exact_playable_station_range(self):
        self.assertEqual([s["station_id"] for s in self.data["stations"]], list(range(1, 200)))

    def test_no_duplicate_station_ids(self):
        ids = [s["station_id"] for s in self.data["stations"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_no_duplicate_feature_assignments(self):
        features = [s["feature_id"] for s in self.data["stations"] if s["feature_id"] is not None]
        self.assertEqual(len(features), len(set(features)))

    def test_marker_200_excluded(self):
        self.assertNotIn(200, [s["station_id"] for s in self.data["stations"]])
        self.assertEqual(self.data["marker_200"]["observed_marker_id"], 200)

    def test_verified_provenance(self):
        for station in self.data["stations"]:
            if station["identity_status"] == "verified":
                self.assertIsNotNone(station["feature_id"])
                self.assertTrue(station["supporting_sources"])
                self.assertIsNotNone(station["marker_centre_canvas"])

    def test_tile_audit_covers_all_sources(self):
        self.assertEqual(len(self.audit["tiles"]), 16)
        self.assertTrue(all(tile["status"] == "usable" for tile in self.audit["tiles"]))

    def test_overlay_labels_match_structured_feature_records(self):
        expected = [s["station_id"] for s in self.data["stations"] if s["feature_id"] is not None]
        self.assertEqual(self.data["metadata"]["overlay_numbered_station_ids"], expected)

    def test_read_but_unmapped_is_explicit(self):
        read_but_unmapped = [s for s in self.data["stations"] if s["number_reading_status"] == "read_but_unmapped"]
        self.assertEqual(len(read_but_unmapped), self.data["metadata"]["summary_counts"]["number_reading"]["read_but_unmapped"])
        for station in read_but_unmapped:
            self.assertIsNotNone(station["printed_number"])
            self.assertIsNone(station["feature_id"])


if __name__ == "__main__":
    unittest.main()
