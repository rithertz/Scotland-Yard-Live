"""
Unit tests for visual coordinate reconciliation (Phase 3C.3-C.2).

Validates:
1. Every raw observation remains traceable in reconciled feature records.
2. All station_id fields remain strictly None / null.
3. Reconciliation is deterministic across repeated executions.
4. Unmatched observations are retained and not discarded.
5. Ambiguous observations remain distinguishable.
6. Out-of-bounds coordinates are rejected / clamped.
7. Discrepant / borderline observations are flagged for review rather than blindly merged.
"""

import sys
import unittest
from pathlib import Path
import json

TOOL_DIR = Path(__file__).resolve().parent.parent
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from reconcile_coordinates import (
    reconcile_observations,
    load_raw_inventory,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
    MATCH_THRESHOLD_PX,
)


class TestCoordinateReconciliation(unittest.TestCase):
    """Validation test suite for Phase 3C.3-C.2 reconciliation."""

    def setUp(self):
        self.raw_inv_path = TOOL_DIR / "output" / "coordinate_extraction" / "coordinate_inventory.json"
        self.assertTrue(self.raw_inv_path.exists(), f"Missing {self.raw_inv_path}")
        self.raw_inventory = load_raw_inventory(self.raw_inv_path)
        self.reconciled_features, self.stats = reconcile_observations(self.raw_inventory)

    def test_traceability_of_every_raw_observation(self):
        """Every raw detection ID must appear in exactly one reconciled feature's contributing IDs."""
        all_raw_ids = set(x["detection_id"] for x in self.raw_inventory)
        reconciled_raw_ids = set()

        for feat in self.reconciled_features:
            for did in feat["contributing_detection_ids"]:
                self.assertNotIn(did, reconciled_raw_ids, f"Detection {did} referenced more than once")
                reconciled_raw_ids.add(did)

        self.assertEqual(all_raw_ids, reconciled_raw_ids, "Not all raw observations are traceable in reconciled output")

    def test_no_station_id_assignment(self):
        """All station_id fields must remain strictly None."""
        for feat in self.reconciled_features:
            self.assertIsNone(feat["station_id"], f"Feature {feat['provisional_feature_id']} has non-null station_id")
            # Feature ID must be provisional string, not integer
            self.assertTrue(feat["provisional_feature_id"].startswith("FEAT_"))

    def test_reconciliation_is_deterministic(self):
        """Reconciliation must yield identical results across repeated executions."""
        feats2, stats2 = reconcile_observations(self.raw_inventory)
        self.assertEqual(len(self.reconciled_features), len(feats2))
        self.assertEqual(self.stats, stats2)

        for f1, f2 in zip(self.reconciled_features, feats2):
            self.assertEqual(f1["provisional_feature_id"], f2["provisional_feature_id"])
            self.assertEqual(f1["normalized_x"], f2["normalized_x"])
            self.assertEqual(f1["normalized_y"], f2["normalized_y"])
            self.assertEqual(f1["status"], f2["status"])
            self.assertEqual(f1["contributing_detection_ids"], f2["contributing_detection_ids"])

    def test_unmatched_observations_retained(self):
        """Unmatched full and quadrant observations must be preserved as distinct provisional features."""
        self.assertGreater(self.stats["unmatched_full_features"], 0)
        self.assertGreater(self.stats["unmatched_quad_features"], 0)
        total_expected = (
            self.stats["reconciled_cross_image_features"]
            + self.stats["unmatched_full_features"]
            + self.stats["unmatched_quad_features"]
        )
        self.assertEqual(len(self.reconciled_features), total_expected)

    def test_ambiguous_observations_remain_distinguishable(self):
        """Ambiguous observations must not be silently converted to standard high-confidence detections."""
        ambiguous_feats = [f for f in self.reconciled_features if f["ambiguous"]]
        self.assertGreaterEqual(len(ambiguous_feats), 1)
        for af in ambiguous_feats:
            self.assertIn(af["status"], ("ambiguous", "needs-owner-review"))
            self.assertNotEqual(af["ambiguity_reason"], "")

    def test_coordinates_within_normalized_bounds(self):
        """All reconciled coordinates must fall strictly within [0, 1] x [0, 1]."""
        for feat in self.reconciled_features:
            nx = feat["normalized_x"]
            ny = feat["normalized_y"]
            self.assertGreaterEqual(nx, 0.0)
            self.assertLessEqual(nx, 1.0)
            self.assertGreaterEqual(ny, 0.0)
            self.assertLessEqual(ny, 1.0)
            self.assertAlmostEqual(feat["pixel_x"], nx * CANVAS_WIDTH, places=1)
            self.assertAlmostEqual(feat["pixel_y"], ny * CANVAS_HEIGHT, places=1)

    def test_no_broad_threshold_merging(self):
        """Pairs with discrepancy > MATCH_THRESHOLD_PX (15px) must NOT be merged into a single feature."""
        for feat in self.reconciled_features:
            if len(feat["contributing_sources"]) > 1:
                self.assertLessEqual(
                    feat["spatial_discrepancy_px"],
                    MATCH_THRESHOLD_PX,
                    f"Feature {feat['provisional_feature_id']} was merged despite discrepancy {feat['spatial_discrepancy_px']} > {MATCH_THRESHOLD_PX}px"
                )

    def test_exact_mathematical_accounting_invariants(self):
        """Verify the exact 138 raw observation to 121 feature reconciliation math."""
        # Raw totals
        self.assertEqual(len(self.raw_inventory), 138)
        self.assertEqual(self.stats["total_raw_observations"], 138)
        self.assertEqual(self.stats["full_board_observations"], 94)
        self.assertEqual(self.stats["quadrant_observations"], 44)

        # Category raw counts
        yellow_raw = [x for x in self.raw_inventory if x["category"] == "yellow"]
        red_raw = [x for x in self.raw_inventory if x["category"] == "red_underground"]
        self.assertEqual(len(yellow_raw), 116)
        self.assertEqual(len(red_raw), 22)

        # Feature totals
        self.assertEqual(len(self.reconciled_features), 121)
        self.assertEqual(self.stats["total_reconciled_features"], 121)
        self.assertEqual(self.stats["features_by_category"]["yellow"], 104)
        self.assertEqual(self.stats["features_by_category"]["red_underground"], 17)

        # Multi-image groups
        self.assertEqual(self.stats["reconciled_cross_image_features"], 15)
        self.assertEqual(self.stats["unmatched_full_features"], 79)
        self.assertEqual(self.stats["unmatched_quad_features"], 27)

        # Check group size distributions
        single_obs_feats = [f for f in self.reconciled_features if len(f["contributing_detection_ids"]) == 1]
        pair_obs_feats = [f for f in self.reconciled_features if len(f["contributing_detection_ids"]) == 2]
        triplet_obs_feats = [f for f in self.reconciled_features if len(f["contributing_detection_ids"]) == 3]

        self.assertEqual(len(single_obs_feats), 106)  # 79 full + 27 quad
        self.assertEqual(len(pair_obs_feats), 13)
        self.assertEqual(len(triplet_obs_feats), 2)

        total_accounted_raw = (
            len(single_obs_feats) * 1
            + len(pair_obs_feats) * 2
            + len(triplet_obs_feats) * 3
        )
        self.assertEqual(total_accounted_raw, 138)

        # Check duplicates absorbed: 13*1 + 2*2 = 17
        duplicates_absorbed = len(pair_obs_feats) * 1 + len(triplet_obs_feats) * 2
        self.assertEqual(duplicates_absorbed, 17)
        self.assertEqual(138 - duplicates_absorbed, 121)

    def test_derivation_source_counts(self):
        """Ensure derivation sources match exactly across stats and features."""
        deriv_counts = {"global-reference-derived": 0, "global-reference-verified": 0, "close-up-only": 0}
        for f in self.reconciled_features:
            deriv_counts[f["derivation"]] += 1

        self.assertEqual(self.stats["derivation_sources"], deriv_counts)
        self.assertEqual(deriv_counts["global-reference-derived"], 84)
        self.assertEqual(deriv_counts["global-reference-verified"], 10)
        self.assertEqual(deriv_counts["close-up-only"], 27)
        self.assertEqual(sum(deriv_counts.values()), 121)


if __name__ == "__main__":
    unittest.main()
