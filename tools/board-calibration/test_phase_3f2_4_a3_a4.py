import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools/board-calibration/phase_3f2_4_a3_a4.py"
OUTPUT = ROOT / "tools/board-calibration/output/phase_3f2_4_a3_a4"
INPUT = ROOT / "tools/board-calibration/control-point-workbench/workspace/a3-a4-pilot.json"


class Phase3F24Tests(unittest.TestCase):
    def test_outputs_are_reproducible_and_input_is_preserved(self):
        before = INPUT.read_bytes()
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)
        first_report = json.loads((OUTPUT / "registration_report.json").read_text(encoding="utf-8"))
        subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, check=True, capture_output=True, text=True)
        second_report = json.loads((OUTPUT / "registration_report.json").read_text(encoding="utf-8"))
        self.assertEqual(INPUT.read_bytes(), before)
        self.assertEqual(first_report["integrity"]["correspondence_count"], 11)
        self.assertTrue(first_report["integrity"]["all_non_demo"])
        self.assertEqual(first_report["all_points"]["homography"], second_report["all_points"]["homography"])
        self.assertEqual(first_report["all_points"]["threshold_counts"], second_report["all_points"]["threshold_counts"])
        self.assertIn("out_of_bounds_projections", first_report)
        self.assertEqual(len(first_report["outlier_removal_scenario"]["retained_ids"]), 5)
        with (OUTPUT / "point_error_report.csv").open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual([row["id"] for row in rows], [f"CP-{index:03d}" for index in range(1, 12)])
        for filename in ["registration_report.json", "registration_report.md", "point_error_report.csv", "homography.json", "overlay_a3_to_a4.png", "overlay_a4_to_a3.png", "blend.png", "difference.png", "correspondence_visualization.png", "robustness_comparison.png"]:
            self.assertTrue((OUTPUT / filename).exists(), filename)
