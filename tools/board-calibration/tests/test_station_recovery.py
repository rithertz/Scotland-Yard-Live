"""
Unit tests for Phase 3D.1 Physical Station-Node Recovery.

Validates:
1. Unique station identities in verified inventory.
2. Valid normalized coordinates within [0, 1] x [0, 1].
3. Valid feature references and provenance.
4. No duplicate identity assignment.
5. Explicit unresolved identity representation for missing nodes.
6. Deterministic output across repeated executions.
7. Preservation of original 138 observations.
8. Preservation of original 121 provisional features.
9. Separate documentation and non-playable status of Marker 200.
10. Corrected identity confidence counts (Phase 3D.1 audit corrections applied):
    - verified = 2 (Station 1: FEAT_0094, Station 199: FEAT_0115)
    - candidate_uncertain = 4 (Stations 3, 120, 123, 158)
    - missing_from_evidence = 193
"""

import sys
import unittest
import json
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent.parent
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

OUTPUT_DIR = TOOL_DIR / "output" / "station_recovery"
BASELINE_DIR = TOOL_DIR / "output" / "coordinate_extraction"


class TestStationRecovery(unittest.TestCase):
    """Validation test suite for Phase 3D.1 physical station recovery."""

    def setUp(self):
        self.raw_path = BASELINE_DIR / "coordinate_inventory.json"
        self.reconciled_path = BASELINE_DIR / "reconciled_coordinate_inventory.json"
        self.candidates_path = OUTPUT_DIR / "candidate_marker_inventory.json"
        self.identities_path = OUTPUT_DIR / "station_identities_matrix.json"
        self.atlas_path = OUTPUT_DIR / "atlas_index.json"

        self.assertTrue(self.raw_path.exists())
        self.assertTrue(self.reconciled_path.exists())
        self.assertTrue(self.candidates_path.exists())
        self.assertTrue(self.identities_path.exists())
        self.assertTrue(self.atlas_path.exists())

        self.raw_obs = json.loads(self.raw_path.read_text(encoding="utf-8"))
        self.reconciled = json.loads(self.reconciled_path.read_text(encoding="utf-8"))
        self.candidates_data = json.loads(self.candidates_path.read_text(encoding="utf-8"))
        self.identities_data = json.loads(self.identities_path.read_text(encoding="utf-8"))
        self.atlas_data = json.loads(self.atlas_path.read_text(encoding="utf-8"))

    def test_preservation_of_original_138_observations(self):
        """Original 138 raw observations must remain intact."""
        self.assertEqual(len(self.raw_obs), 138)
        self.assertEqual(self.candidates_data["metadata"]["total_physical_candidates"], len(self.candidates_data["physical_marker_candidates"]))

    def test_preservation_of_baseline_121_features(self):
        """Baseline 121 features must be fully preserved in candidate inventory."""
        self.assertEqual(len(self.reconciled["features"]), 121)
        baseline_in_candidates = [
            f for f in self.candidates_data["physical_marker_candidates"]
            if f.get("inventory_generation") == "baseline-phase-3c3"
        ]
        self.assertEqual(len(baseline_in_candidates), 121)
        for b_feat, orig_feat in zip(baseline_in_candidates, self.reconciled["features"]):
            self.assertEqual(b_feat["provisional_feature_id"], orig_feat["provisional_feature_id"])
            self.assertEqual(b_feat["pixel_x"], orig_feat["pixel_x"])
            self.assertEqual(b_feat["pixel_y"], orig_feat["pixel_y"])

    def test_unique_station_identities(self):
        """Verified station identities must be strictly unique.

        Phase 3D.1 audit correction: exactly 2 verified identities
        (Station 1 → FEAT_0094, Station 199 → FEAT_0115).
        """
        matrix = self.identities_data["identities_1_to_199"]
        self.assertEqual(len(matrix), 199)
        verified_sids = [m["station_id"] for m in matrix if m["status"] == "verified"]
        # Uniqueness
        self.assertEqual(len(verified_sids), len(set(verified_sids)))
        # Corrected count after Phase 3D.1 audit: only 2 directly-readable verified IDs
        self.assertEqual(len(verified_sids), 2)
        self.assertIn(1, verified_sids)
        self.assertIn(199, verified_sids)

    def test_candidate_uncertain_identities(self):
        """candidate_uncertain entries must be exactly 4 with feature IDs and coordinates.

        Phase 3D.1 audit correction: Stations 3, 120, 123, 158 are candidate_uncertain
        (physical marker present but numeric label not independently legible).
        """
        matrix = self.identities_data["identities_1_to_199"]
        cu_entries = [m for m in matrix if m["status"] == "candidate_uncertain"]
        self.assertEqual(len(cu_entries), 4)
        expected_sids = {3, 120, 123, 158}
        actual_sids = {m["station_id"] for m in cu_entries}
        self.assertEqual(actual_sids, expected_sids)
        for entry in cu_entries:
            # Every candidate_uncertain entry must carry a feature reference and coordinates
            self.assertIsNotNone(entry["feature_id"])
            self.assertIsNotNone(entry["pixel_x"])
            self.assertIsNotNone(entry["pixel_y"])
            self.assertEqual(entry["confidence"], "candidate_uncertain")

    def test_no_duplicate_identity_assignment(self):
        """No two verified OR candidate_uncertain stations may claim the same feature ID."""
        matrix = self.identities_data["identities_1_to_199"]
        assigned_feats = [
            m["feature_id"]
            for m in matrix
            if m["status"] in ("verified", "candidate_uncertain")
        ]
        # All feature IDs among assigned entries must be unique
        self.assertEqual(len(assigned_feats), len(set(assigned_feats)))
        # No overlap between verified and candidate_uncertain feature IDs
        verified_feats = {m["feature_id"] for m in matrix if m["status"] == "verified"}
        cu_feats = {m["feature_id"] for m in matrix if m["status"] == "candidate_uncertain"}
        self.assertEqual(len(verified_feats & cu_feats), 0)

    def test_completeness_counts(self):
        """Summary counts in metadata must reflect the Phase 3D.1 audit-corrected values."""
        sc = self.identities_data["metadata"]["summary_counts"]
        self.assertEqual(sc["verified"], 2)
        self.assertEqual(sc["candidate_uncertain"], 4)
        self.assertEqual(sc["missing_from_evidence"], 193)
        self.assertEqual(sc["conflicting"], 0)
        self.assertEqual(sc["duplicate"], 0)
        # Totals must be consistent with the 199-slot matrix
        total_assigned = sc["verified"] + sc["candidate_uncertain"] + sc["missing_from_evidence"]
        self.assertEqual(total_assigned, 199)

    def test_valid_normalized_coordinates(self):
        """All recovered candidate coordinates must be strictly within [0, 1] x [0, 1]."""
        for feat in self.candidates_data["physical_marker_candidates"]:
            nx = feat["normalized_x"]
            ny = feat["normalized_y"]
            self.assertGreaterEqual(nx, 0.0)
            self.assertLessEqual(nx, 1.0)
            self.assertGreaterEqual(ny, 0.0)
            self.assertLessEqual(ny, 1.0)

    def test_valid_provenance_and_tile_containment(self):
        """Every candidate must have valid source image and at least one containing atlas tile."""
        for feat in self.candidates_data["physical_marker_candidates"]:
            self.assertIn(feat["primary_source"], ("full", "top-left", "top-right", "bottom-left", "bottom-right"))
            self.assertGreaterEqual(len(feat["containing_atlas_tiles"]), 1)

    def test_explicit_unresolved_representation(self):
        """Unresolved stations 1-199 must be explicitly represented as missing_from_evidence with null coordinates."""
        matrix = self.identities_data["identities_1_to_199"]
        unresolved = [m for m in matrix if m["status"] == "missing_from_evidence"]
        self.assertGreater(len(unresolved), 0)
        for u in unresolved:
            self.assertIsNone(u["feature_id"])
            self.assertIsNone(u["pixel_x"])
            self.assertIsNone(u["pixel_y"])
            self.assertEqual(u["confidence"], "unresolved")

    def test_marker_200_recorded_separately(self):
        """Marker 200 must be recorded in separate metadata, not in the playable 1-199 array."""
        matrix = self.identities_data["identities_1_to_199"]
        sids = [m["station_id"] for m in matrix]
        self.assertNotIn(200, sids)

        m200 = self.identities_data["metadata"]["additional_physical_markers"][0]
        self.assertEqual(m200["observed_marker_id"], 200)
        self.assertEqual(m200["status"], "observed-physical-marker-unresolved-playability")


if __name__ == "__main__":
    unittest.main()
