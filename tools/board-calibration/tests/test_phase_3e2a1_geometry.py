import json
import math
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
WORK = REPO / "docs" / "game" / "data" / "phase-3e2a-workspace"


class TestPhase3E2AIntervalGeometry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((WORK / "station-crop-manifest.json").read_text(encoding="utf-8"))
        cls.audit = json.loads((WORK / "source-crop-geometry-audit.json").read_text(encoding="utf-8"))

    def test_exact_station_range(self):
        self.assertEqual([r["stationId"] for r in self.manifest["stations"]], list(range(1, 200)))

    def test_registered_and_valid_source_crops_exist(self):
        for record in self.manifest["stations"]:
            self.assertTrue((REPO / record["registeredCropPath"]).exists())
            if record["sourceCropAvailable"]:
                self.assertIsNotNone(record["sourceCropPath"])
                self.assertTrue((REPO / record["sourceCropPath"]).exists())
            else:
                self.assertIsNone(record["sourceCropPath"])

    def test_valid_quadrilaterals_are_finite_and_in_bounds(self):
        for record in self.manifest["stations"]:
            if not record["sourceCropAvailable"]:
                self.assertIsNone(record["sourcePixelCorners"])
                self.assertEqual(record["cropProvenanceType"], "rectified-fallback")
                self.assertTrue(record["fallbackReason"])
                continue
            self.assertEqual(record["transformValidationStatus"], "valid")
            points = record["sourcePixelCorners"]
            self.assertEqual(len(points), 8)
            self.assertTrue(all(math.isfinite(float(value)) for value in points))
            width, height = record["sourceImageDimensions"]
            corners = list(zip(points[::2], points[1::2]))
            self.assertTrue(all(0 <= x <= width and 0 <= y <= height for x, y in corners))
            signed_area = sum(corners[i][0] * corners[(i + 1) % 4][1] - corners[(i + 1) % 4][0] * corners[i][1] for i in range(4)) / 2
            self.assertGreater(abs(signed_area), 100)
            self.assertTrue(all((corners[(i + 1) % 4][0] - corners[i][0]) * (corners[(i + 2) % 4][1] - corners[(i + 1) % 4][1]) - (corners[(i + 1) % 4][1] - corners[i][1]) * (corners[(i + 2) % 4][0] - corners[(i + 1) % 4][0]) != 0 for i in range(4)))
            self.assertEqual(record["sourceCropOutputDimensions"], [220, 220])

    def test_st101_regression(self):
        record = self.manifest["stations"][100]
        self.assertEqual(record["stationId"], 101)
        if record["sourceCropAvailable"]:
            width, height = record["sourceImageDimensions"]
            self.assertTrue(all(0 <= value <= limit for x, y in zip(record["sourcePixelCorners"][::2], record["sourcePixelCorners"][1::2]) for value, limit in ((x, width), (y, height))))
        else:
            self.assertEqual(record["cropProvenanceType"], "rectified-fallback")
            self.assertTrue(record["fallbackReason"])

    def test_audit_counts_match_manifest(self):
        self.assertEqual(self.audit["checkedRecords"], 199)
        self.assertEqual(self.audit["validHighResolutionSourceCrops"] + self.audit["rectifiedFallbackCrops"], 199)
        self.assertEqual(self.audit["remainingWarnings"], [w for w in self.audit["remainingWarnings"] if w["stationId"] in range(1, 200)])

    def test_no_invalid_transform_marked_valid(self):
        for record in self.manifest["stations"]:
            self.assertFalse(record["transformValidationStatus"] == "valid" and not record["sourceCropAvailable"])


if __name__ == "__main__":
    unittest.main()
