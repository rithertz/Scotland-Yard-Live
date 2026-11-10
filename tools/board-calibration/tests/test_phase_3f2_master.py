import json
from pathlib import Path

import cv2


REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "tools" / "board-calibration" / "output" / "phase_3f2_master"


def test_phase_3f2_master_artifact_dimensions_and_status():
    metadata = json.loads((OUT / "reconstruction_metadata.json").read_text(encoding="utf-8"))
    assert metadata["source_count"] == 16
    assert metadata["master_dimensions"] == {"width": 2700, "height": 2000, "scale": 2, "aspect_ratio": 1.35}
    assert metadata["quality_status"] == "REJECTED_FOR_FRONTEND_INTEGRATION_PENDING_REGISTRATION_REVIEW"
    assert metadata["frontend_integration"]["safe"] is False


def test_phase_3f2_registration_audit_covers_all_playable_stations():
    audit = json.loads((OUT / "station_registration_audit.json").read_text(encoding="utf-8"))
    stations = audit["stations"]
    assert len(stations) == 199
    assert [station["station_id"] for station in stations] == list(range(1, 200))
    assert audit["transformation"] == "master_x = reference_x * 2; master_y = reference_y * 2"
    assert audit["counts"] == {
        "stations": 199,
        "verified_alignment": 0,
        "provisional_alignment": 199,
        "uncertain_alignment": 0,
        "clearly_incorrect_alignment": 0,
    }


def test_phase_3f2_png_is_actual_high_resolution_output():
    image = cv2.imread(str(OUT / "board_master_2x.png"), cv2.IMREAD_COLOR)
    assert image is not None
    assert image.shape[:2] == (2000, 2700)
