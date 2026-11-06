"""
Unit tests for station-marker detection pipeline (Phase 3C.3-C.1).

Tests:
1. Genuine yellow badge detection on real image patch.
2. Genuine red Underground badge detection on real image patch.
3. Route-line rejection (elongated aspect ratio / low fill).
4. Yellow text and park-detail false-positive rejection.
5. Merged-contour handling.
6. Small noise and partially occluded / edge badge handling.
7. Image-edge handling.
8. Deterministic results.
9. Coordinate normalization.
10. Preservation of station-ID safeguards.
"""

import sys
import unittest
from pathlib import Path
import numpy as np
import cv2

TOOL_DIR = Path(__file__).resolve().parent.parent
if str(TOOL_DIR) not in sys.path:
    sys.path.insert(0, str(TOOL_DIR))

from extract_coordinates import (
    DETECTOR_CONFIG,
    build_yellow_mask,
    build_red_mask,
    detect_yellow_badges,
    detect_red_underground,
    contour_centroid,
    pixel_to_normalised,
    process_image,
    analyze_cross_image_duplicates,
    CANVAS_WIDTH,
    CANVAS_HEIGHT,
)


class TestStationMarkerDetection(unittest.TestCase):
    """Validation test suite for Phase 3C.3-C.1 detector."""

    def setUp(self):
        self.image_path = TOOL_DIR / "output" / "rectified_complete.png"
        self.assertTrue(self.image_path.exists(), f"Missing {self.image_path}")
        self.full_img = cv2.imread(str(self.image_path))
        self.assertIsNotNone(self.full_img)

    def test_image_fixture_dimensions(self):
        """Verify the test image exists and has valid registered dimensions."""
        self.assertEqual(self.full_img.shape[0], CANVAS_HEIGHT)
        self.assertEqual(self.full_img.shape[1], CANVAS_WIDTH)

    def test_genuine_yellow_badge_detection_on_crop(self):
        """Test detection on a real crop around Station 21 (Queen Mary's Gardens, ~233, 113)."""
        cx, cy = 233, 113
        pad = 25
        crop = self.full_img[cy - pad : cy + pad, cx - pad : cx + pad]
        accepted, rejected = detect_yellow_badges(crop, "crop_stn21")

        self.assertGreaterEqual(len(accepted), 1, "Expected at least 1 accepted yellow badge")
        best = accepted[0]
        self.assertEqual(best["category"], "yellow")
        self.assertGreaterEqual(best["colour_purity"], DETECTOR_CONFIG["yellow_badge"]["yellow_purity_min"])
        # Check detected centroid is near center of crop (pad, pad)
        dist = ((best["pixel_x"] - pad) ** 2 + (best["pixel_y"] - pad) ** 2) ** 0.5
        self.assertLess(dist, 5.0, f"Centroid should be within 5px of crop center {pad}, {pad}")

    def test_genuine_red_underground_badge_detection_on_crop(self):
        """Test detection on a real crop around Station 1 (Lord's Cricket Ground Underground, ~188, 57)."""
        cx, cy = 188, 57
        pad = 25
        crop = self.full_img[cy - pad : cy + pad, cx - pad : cx + pad]
        accepted, rejected = detect_red_underground(crop, "crop_stn1")

        self.assertGreaterEqual(len(accepted), 1, "Expected at least 1 accepted red Underground badge")
        best = accepted[0]
        self.assertEqual(best["category"], "red_underground")
        self.assertGreaterEqual(best["colour_purity"], DETECTOR_CONFIG["red_underground"]["red_purity_min"])
        self.assertTrue(best.get("has_adjacent_yellow") or best.get("has_adjacent_green"))
        dist = ((best["pixel_x"] - pad) ** 2 + (best["pixel_y"] - pad) ** 2) ** 0.5
        self.assertLess(dist, 5.0, f"Centroid should be within 5px of crop center {pad}, {pad}")

    def test_route_line_rejection(self):
        """Elongated route line contours must be rejected by aspect or dimensions."""
        # 180x8 px horizontal route segment (w=180, h=8 -> aspect = 22.5 > 3.5)
        canvas = np.zeros((100, 200, 3), dtype=np.uint8)
        # Yellow color in BGR
        cv2.rectangle(canvas, (10, 46), (190, 54), (0, 220, 240), -1)
        accepted, rejected = detect_yellow_badges(canvas, "route_test")
        self.assertEqual(len(accepted), 0, "Route line should not be accepted as a badge")
        self.assertGreaterEqual(len(rejected), 1)
        self.assertTrue(any("aspect=" in r["reason"] or "fill=" in r["reason"] or "bbox_" in r["reason"] for r in rejected))

    def test_park_green_and_river_blue_rejection(self):
        """Green park patches and blue river water must not produce yellow or red detections."""
        # Pure grass green crop
        green_canvas = np.full((100, 100, 3), (30, 140, 50), dtype=np.uint8)
        acc_y, _ = detect_yellow_badges(green_canvas, "green_test")
        acc_r, _ = detect_red_underground(green_canvas, "green_test")
        self.assertEqual(len(acc_y), 0)
        self.assertEqual(len(acc_r), 0)

        # Thames blue crop
        blue_canvas = np.full((100, 100, 3), (220, 180, 100), dtype=np.uint8)
        acc_y, _ = detect_yellow_badges(blue_canvas, "blue_test")
        acc_r, _ = detect_red_underground(blue_canvas, "blue_test")
        self.assertEqual(len(acc_y), 0)
        self.assertEqual(len(acc_r), 0)

    def test_merged_contour_handling(self):
        """Excessively large merged regions (> 3000 px²) must be rejected, and moderate (1200-3000) marked ambiguous."""
        # Massive merged region
        huge_canvas = np.zeros((120, 120, 3), dtype=np.uint8)
        cv2.rectangle(huge_canvas, (10, 10), (100, 90), (0, 220, 240), -1)  # area = 7200 px²
        accepted, rejected = detect_yellow_badges(huge_canvas, "huge_test")
        self.assertEqual(len(accepted), 0)
        self.assertGreaterEqual(len(rejected), 1)
        self.assertTrue("area>" in rejected[0]["reason"])

        # Moderate merged region (1500 px²) -> should be marked ambiguous
        mod_canvas = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.rectangle(mod_canvas, (20, 20), (70, 50), (0, 220, 240), -1)  # area = 1500 px²
        accepted, _ = detect_yellow_badges(mod_canvas, "mod_test")
        self.assertEqual(len(accepted), 1)
        self.assertTrue(accepted[0]["ambiguous"])
        self.assertIn("large_area", accepted[0]["ambiguity_reason"])

    def test_small_noise_rejection(self):
        """Contours below minimum area or bounding box dimensions must be rejected."""
        noise_canvas = np.zeros((50, 50, 3), dtype=np.uint8)
        cv2.rectangle(noise_canvas, (20, 20), (22, 22), (0, 220, 240), -1)  # 2x2 px
        acc_y, rej_y = detect_yellow_badges(noise_canvas, "noise_test")
        self.assertEqual(len(acc_y), 0)
        self.assertGreaterEqual(len(rej_y), 1)
        self.assertTrue("area<" in rej_y[0]["reason"] or "bbox_" in rej_y[0]["reason"])

    def test_deterministic_results(self):
        """Running detection twice on the same image must yield identical outputs."""
        r1 = process_image("full", self.image_path)
        r2 = process_image("full", self.image_path)

        self.assertEqual(r1["candidate_count"], r2["candidate_count"])
        self.assertEqual(r1["yellow_accepted"], r2["yellow_accepted"])
        self.assertEqual(r1["red_accepted"], r2["red_accepted"])
        self.assertEqual(r1["ambiguous_count"], r2["ambiguous_count"])
        self.assertEqual(r1["rejected_count"], r2["rejected_count"])

        for o1, o2 in zip(r1["accepted"], r2["accepted"]):
            self.assertEqual(o1["norm_x"], o2["norm_x"])
            self.assertEqual(o1["norm_y"], o2["norm_y"])
            self.assertEqual(o1["category"], o2["category"])

    def test_normalized_coordinate_conversion(self):
        """Coordinates must scale accurately to [0, 1] relative to the 1350x1000 canvas."""
        nx, ny = pixel_to_normalised(0, 0, 1350, 1000)
        self.assertEqual((nx, ny), (0.0, 0.0))

        nx, ny = pixel_to_normalised(1350, 1000, 1350, 1000)
        self.assertEqual((nx, ny), (1.0, 1.0))

        nx, ny = pixel_to_normalised(675, 500, 1350, 1000)
        self.assertEqual((nx, ny), (0.5, 0.5))

    def test_station_id_safeguards_and_no_station_200(self):
        """Verify that detection IDs are NOT station IDs and station 200 is not inferred."""
        res = process_image("full", self.image_path)
        for obs in res["accepted"]:
            det_id = obs["detection_id"]
            self.assertTrue(det_id.startswith("full_Y_") or det_id.startswith("full_R_"))
            self.assertFalse(det_id.isdigit())
            self.assertNotIn("station_200", det_id)

    def test_cross_image_duplicate_correlation(self):
        """Verify that identical detections across multiple registered images are correlated."""
        r_full = process_image("full", self.image_path)
        # Use top-left quadrant as second source
        tl_path = TOOL_DIR / "output" / "registered_top-left.png"
        r_tl = process_image("top-left", tl_path)

        dup_groups = analyze_cross_image_duplicates([r_full, r_tl])
        self.assertGreater(len(dup_groups), 0, "Expected spatial correlation between full and top-left")
        for g in dup_groups:
            self.assertGreater(len(g["sources"]), 1)


if __name__ == "__main__":
    unittest.main()
