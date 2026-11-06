"""
Unit tests for Scotland Yard Live board calibration tooling (Phase 3C.3-B.1).
Tests source inventory validation, SHA-256 integrity and tamper detection,
control point integrity, homography calculation, synthetic perspective recovery,
fitting/held-out validation separation, directional residuals, and aspect ratio semantics.
"""

import sys
import unittest
from pathlib import Path
import numpy as np
import cv2

TOOL_DIR = Path(__file__).resolve().parent
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from config import (
    EVIDENCE_DIR,
    PRIMARY_IMAGES,
    EXPECTED_DIMENSIONS,
    EXPECTED_HASHES,
    COMPLETE_CORNERS_SRC,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
)
from geometry import (
    compute_homography,
    transform_points,
    compute_residuals,
    compute_directional_residuals,
    partition_correspondences_deterministic,
    calculate_aspect_ratio_metric,
    analyze_fold_proximity,
)
from inventory import get_file_sha256, generate_source_inventory


class TestSourceInventoryAndIntegrity(unittest.TestCase):
    """Validates source image existence, dimensions, and cryptographic SHA-256 integrity."""

    def test_all_primary_images_exist(self):
        for filename in PRIMARY_IMAGES:
            path = EVIDENCE_DIR / filename
            self.assertTrue(path.exists(), f"Image missing: {path}")

    def test_image_dimensions_match(self):
        for filename, (exp_w, exp_h) in EXPECTED_DIMENSIONS.items():
            path = EVIDENCE_DIR / filename
            img = cv2.imread(str(path))
            self.assertIsNotNone(img, f"Failed to decode: {path}")
            h, w, _ = img.shape
            self.assertEqual(w, exp_w, f"Width mismatch for {filename}")
            self.assertEqual(h, exp_h, f"Height mismatch for {filename}")

    def test_sha256_exact_match_against_expected(self):
        for filename, expected_hash in EXPECTED_HASHES.items():
            actual_hash = get_file_sha256(EVIDENCE_DIR / filename)
            self.assertEqual(
                actual_hash,
                expected_hash,
                f"Cryptographic hash mismatch for {filename}! File may have been altered.",
            )

    def test_inventory_generation(self):
        report = generate_source_inventory()
        self.assertEqual(len(report["images"]), 5)
        for item in report["images"]:
            self.assertTrue(item["dimensions_match_expected"])
            self.assertTrue(item["sha256_matches_expected"])
            self.assertIn("sha256", item)
            self.assertIn("board_orientation", item)

    def test_tamper_detection_raises_error(self):
        """Simulates an invalid hash and tests that tamper detection raises ValueError."""
        # Temporarily modify expected hash in test
        corrupt_hashes = dict(EXPECTED_HASHES)
        corrupt_hashes["complete.jpeg"] = "0000000000000000000000000000000000000000000000000000000000000000"

        from unittest.mock import patch
        with patch("inventory.EXPECTED_HASHES", corrupt_hashes):
            with self.assertRaises(ValueError) as ctx:
                generate_source_inventory()
            self.assertIn("Cryptographic hash mismatch", str(ctx.exception))


class TestControlPointsAndHomography(unittest.TestCase):
    """Validates corner control points and homography calculation."""

    def test_control_point_coordinates_within_image_bounds(self):
        w_img, h_img = EXPECTED_DIMENSIONS["complete.jpeg"]
        for key, (x, y) in COMPLETE_CORNERS_SRC.items():
            self.assertGreaterEqual(x, 0.0, f"{key} x < 0")
            self.assertLessEqual(x, w_img, f"{key} x > width")
            self.assertGreaterEqual(y, 0.0, f"{key} y < 0")
            self.assertLessEqual(y, h_img, f"{key} y > height")

    def test_global_homography_exact_corner_mapping(self):
        src_corners = np.array([
            list(COMPLETE_CORNERS_SRC["physical_nw"]),
            list(COMPLETE_CORNERS_SRC["physical_ne"]),
            list(COMPLETE_CORNERS_SRC["physical_se"]),
            list(COMPLETE_CORNERS_SRC["physical_sw"]),
        ], dtype=np.float32)

        dst_corners = np.array([
            [0.0, 0.0],
            [float(CANVAS_WIDTH), 0.0],
            [float(CANVAS_WIDTH), float(CANVAS_HEIGHT)],
            [0.0, float(CANVAS_HEIGHT)],
        ], dtype=np.float32)

        H, _ = compute_homography(src_corners, dst_corners, method=0)
        self.assertEqual(H.shape, (3, 3))
        self.assertNotEqual(np.linalg.det(H), 0.0)

        mapped = transform_points(src_corners, H)
        np.testing.assert_allclose(mapped, dst_corners, atol=1e-3)

    def test_synthetic_perspective_warp_recovery(self):
        """Generates a synthetic known rectangle under perspective, tests exact recovery."""
        true_corners = np.array([[0, 0], [400, 0], [400, 300], [0, 300]], dtype=np.float32)
        distorted_corners = np.array([[45, 12], [420, 25], [395, 290], [20, 280]], dtype=np.float32)

        H_true, _ = compute_homography(distorted_corners, true_corners, method=0)

        xs, ys = np.meshgrid(np.linspace(50, 350, 7), np.linspace(50, 250, 5))
        test_pts = np.vstack([xs.ravel(), ys.ravel()]).T.astype(np.float32)

        H_inv = np.linalg.inv(H_true)
        pts_in_distorted = transform_points(test_pts, H_inv)
        recovered_pts = transform_points(pts_in_distorted, H_true)

        res = compute_residuals(recovered_pts, test_pts)
        self.assertLess(res["max"], 1e-3)
        self.assertLess(res["rmse"], 1e-4)


class TestValidationAndResidualMetrics(unittest.TestCase):
    """Validates fitting vs held-out validation separation, directional residuals, and fold analysis."""

    def test_train_validation_split_disjointness_and_determinism(self):
        class MockKeyPoint:
            def __init__(self, x, y):
                self.pt = (x, y)

        class MockDMatch:
            def __init__(self, qidx, tidx):
                self.queryIdx = qidx
                self.trainIdx = tidx

        # Create 40 mock keypoints distributed across a 2D plane
        kps = [MockKeyPoint(float(i * 10), float(i * 5)) for i in range(40)]
        matches = [MockDMatch(i, i) for i in range(40)]

        fit_m1, val_m1 = partition_correspondences_deterministic(matches, kps, train_ratio=0.75)
        fit_m2, val_m2 = partition_correspondences_deterministic(matches, kps, train_ratio=0.75)

        # Reproducibility
        self.assertEqual([m.queryIdx for m in fit_m1], [m.queryIdx for m in fit_m2])
        self.assertEqual([m.queryIdx for m in val_m1], [m.queryIdx for m in val_m2])

        # Disjointness
        fit_set = set(m.queryIdx for m in fit_m1)
        val_set = set(m.queryIdx for m in val_m1)
        self.assertTrue(fit_set.isdisjoint(val_set))
        self.assertEqual(len(fit_set) + len(val_set), 40)
        self.assertEqual(len(val_m1), 10)  # 25% of 40
        self.assertEqual(len(fit_m1), 30)  # 75% of 40

    def test_directional_residuals_computation(self):
        actual = np.array([[10.0, 10.0], [20.0, 20.0], [30.0, 30.0]])
        expected = np.array([[12.0, 9.0], [22.0, 19.0], [32.0, 29.0]])  # dx = -2, dy = +1

        res_dir = compute_directional_residuals(actual, expected)
        self.assertAlmostEqual(res_dir["mean_dx"], -2.0)
        self.assertAlmostEqual(res_dir["mean_dy"], 1.0)
        self.assertAlmostEqual(res_dir["rmse_dx"], 2.0)
        self.assertAlmostEqual(res_dir["rmse_dy"], 1.0)

    def test_aspect_ratio_distinct_semantics(self):
        """Validates that aspect ratio report distinguishes image-space, physical estimate, and canvas."""
        data = calculate_aspect_ratio_metric(COMPLETE_CORNERS_SRC)

        # 1. Image-space quadrilateral
        self.assertIn("image_space_quadrilateral", data)
        raw_ar = data["image_space_quadrilateral"]["raw_2d_aspect_ratio"]
        self.assertGreater(raw_ar, 1.25)
        self.assertLess(raw_ar, 1.45)
        self.assertEqual(data["image_space_quadrilateral"]["uncertainty_margin"], 0.040)

        # 2. Estimated physical board aspect ratio
        self.assertIn("estimated_physical_board_aspect_ratio", data)
        self.assertEqual(
            data["estimated_physical_board_aspect_ratio"]["status"],
            "UNRESOLVED_FROM_CURRENT_PHOTOGRAPHS",
        )
        self.assertIn("evidence_limitations", data["estimated_physical_board_aspect_ratio"])

        # 3. Provisional working canvas
        self.assertIn("provisional_working_canvas", data)
        self.assertEqual(
            data["provisional_working_canvas"]["classification"],
            "PROVISIONAL_COMPUTATIONAL_CHOICE",
        )
        self.assertEqual(data["provisional_working_canvas"]["aspect_ratio"], 1.350)

    def test_fold_proximity_analysis(self):
        coords = np.array([[0.51, 0.51], [0.52, 0.49], [0.10, 0.10], [0.90, 0.90]])
        residuals = np.array([0.001, 0.001, 0.005, 0.005])

        analysis = analyze_fold_proximity(coords, residuals)
        self.assertEqual(analysis["near_fold_count"], 2)
        self.assertEqual(analysis["far_fold_count"], 2)
        self.assertAlmostEqual(analysis["near_fold_mean_residual"], 0.001)
        self.assertAlmostEqual(analysis["far_fold_mean_residual"], 0.005)


if __name__ == "__main__":
    unittest.main()
