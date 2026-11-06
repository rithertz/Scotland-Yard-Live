"""
diag_investigate.py
===================
Diagnostic script for Phase 3C.3-C station-marker investigation.

Samples pixel colours at known landmark positions from landmarks.py and
measures the actual HSV ranges of the badge colours.  Run with the venv
Python before tuning any detector thresholds.
"""

import cv2
import numpy as np
from pathlib import Path

IMG_DIR = Path(__file__).parent / "output"
OUT_DIR = IMG_DIR / "coordinate_extraction"
OUT_DIR.mkdir(parents=True, exist_ok=True)

FULL_PATH = IMG_DIR / "rectified_complete.png"

# ---------------------------------------------------------------------------
# Known landmark positions on the 1350x1000 canvas (from landmarks.py)
# Format: (station_id, x, y, badge_color, name)
# Using canonical_approx values – note these are (x, y) pixel coords
LANDMARKS = [
    # yellow badges on full canvas
    (2,   222,  18,  "yellow", "London Zoo / Regent's Park North"),
    (8,   115,  68,  "yellow", "Primrose Hill approach"),
    (10,  315,  95,  "yellow", "Regent's Park East"),
    (18,   80, 105,  "yellow", "Paddington Canal"),
    (20,  210, 125,  "yellow", "Regent's Park Outer Circle West"),
    (21,  245,  98,  "yellow", "Queen Mary's Gardens"),
    (33,  185, 180,  "yellow", "Marylebone Road"),
    (3,   410,  35,  "yellow", "Euston Station approach"),
    (4,   500,  45,  "yellow", "St Pancras Station"),
    (14,  640,  85,  "yellow", "Pentonville Road"),
    (15,  720, 150,  "yellow", "Angel / Islington approach"),
    (23,  420, 135,  "yellow", "University College London"),
    # red badges (underground) for contrast
    (1,   188,  57,  "red",    "Lord's Cricket Ground / St John's Wood"),
    (46,  265, 200,  "red",    "Marylebone / Underground"),
    (13,  555, 112,  "red",    "King's Cross / St Pancras Underground"),
]

def sample_region(img, cx, cy, radius=10):
    """Return all pixels in a square region around (cx, cy)."""
    h, w = img.shape[:2]
    x1 = max(0, cx - radius)
    x2 = min(w, cx + radius + 1)
    y1 = max(0, cy - radius)
    y2 = min(h, cy + radius + 1)
    return img[y1:y2, x1:x2]

def bgr_to_hsv_pixel(b, g, r):
    px = np.uint8([[[b, g, r]]])
    return cv2.cvtColor(px, cv2.COLOR_BGR2HSV)[0][0].tolist()

def main():
    img = cv2.imread(str(FULL_PATH))
    if img is None:
        print(f"ERROR: cannot load {FULL_PATH}")
        return

    h, w = img.shape[:2]
    print(f"Image: {FULL_PATH.name}  shape={w}x{h}")
    print()

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    all_yellow_hues = []
    all_yellow_sats = []
    all_yellow_vals = []
    all_red_hues = []

    print(f"{'Stn':>4}  {'Color':>6}  {'cx':>5} {'cy':>5}  "
          f"{'BGR':^14}  {'HSV':^14}  "
          f"{'region H':^12} {'region S':^12} {'region V':^12}")
    print("-" * 100)

    for (sid, cx, cy, badge_color, name) in LANDMARKS:
        cx, cy = int(cx), int(cy)
        # single pixel
        bgr = img[cy, cx].tolist()
        hsv_px = hsv_img[cy, cx].tolist()
        # region statistics
        region_bgr = sample_region(img, cx, cy, radius=8)
        region_hsv = sample_region(hsv_img, cx, cy, radius=8)
        rh = region_hsv[:, :, 0].flatten()
        rs = region_hsv[:, :, 1].flatten()
        rv = region_hsv[:, :, 2].flatten()
        print(f"{sid:>4}  {badge_color:>6}  {cx:>5} {cy:>5}  "
              f"BGR={bgr}  HSV={hsv_px}  "
              f"H={rh.min()}-{rh.max()}(m={rh.mean():.0f})  "
              f"S={rs.min()}-{rs.max()}(m={rs.mean():.0f})  "
              f"V={rv.min()}-{rv.max()}(m={rv.mean():.0f})  "
              f"  [{name[:35]}]")
        if badge_color == "yellow":
            all_yellow_hues.extend(rh.tolist())
            all_yellow_sats.extend(rs.tolist())
            all_yellow_vals.extend(rv.tolist())
        else:
            all_red_hues.extend(rh.tolist())

    print()
    yh = np.array(all_yellow_hues)
    ys = np.array(all_yellow_sats)
    yv = np.array(all_yellow_vals)
    print("=== YELLOW badge colour summary across all sampled landmarks ===")
    print(f"  Hue  : min={yh.min():.0f}  p5={np.percentile(yh,5):.0f}  "
          f"median={np.median(yh):.0f}  p95={np.percentile(yh,95):.0f}  max={yh.max():.0f}")
    print(f"  Sat  : min={ys.min():.0f}  p5={np.percentile(ys,5):.0f}  "
          f"median={np.median(ys):.0f}  p95={np.percentile(ys,95):.0f}  max={ys.max():.0f}")
    print(f"  Val  : min={yv.min():.0f}  p5={np.percentile(yv,5):.0f}  "
          f"median={np.median(yv):.0f}  p95={np.percentile(yv,95):.0f}  max={yv.max():.0f}")
    print()

    # -----------------------------------------------------------------------
    # Try multiple HSV ranges and count contours
    print("=== Contour counts for candidate HSV thresholds ===")
    test_ranges = [
        ((20, 100, 100), (30, 255, 255),  "original narrow"),
        ((15,  80,  80), (45, 255, 255),  "slightly broader"),
        ((10,  40,  80), (50, 255, 255),  "broad"),
        (( 5,  20,  60), (60, 255, 255),  "very broad"),
        ((10,  30,  60), (45, 220, 220),  "capped sat+val"),
    ]
    for (lo, hi, label) in test_ranges:
        lower = np.array(lo, dtype=np.uint8)
        upper = np.array(hi, dtype=np.uint8)
        mask = cv2.inRange(hsv_img, lower, upper)
        # morphological cleanup
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        # count pixels in mask
        px_count = int(mask.sum() // 255)
        # count contours in plausible size range
        plausible = [c for c in contours
                     if 50 < cv2.contourArea(c) < 10000]
        print(f"  {label:30s}: lo={lo} hi={hi}  "
              f"mask_px={px_count:7d}  all_cnts={len(contours):5d}  "
              f"plausible_cnts={len(plausible):5d}")
        # save diagnostic mask
        fname = f"diag_mask_{label.replace(' ','_')}.png"
        # draw contours on a copy of the image
        vis = img.copy()
        cv2.drawContours(vis, plausible, -1, (0, 255, 0), 2)
        cv2.imwrite(str(OUT_DIR / fname), vis)
    print()

    # -----------------------------------------------------------------------
    # Save HSV channel images for visual inspection
    h_ch = hsv_img[:, :, 0]
    s_ch = hsv_img[:, :, 1]
    v_ch = hsv_img[:, :, 2]
    cv2.imwrite(str(OUT_DIR / "diag_hue.png"),    h_ch)
    cv2.imwrite(str(OUT_DIR / "diag_sat.png"),    s_ch)
    cv2.imwrite(str(OUT_DIR / "diag_val.png"),    v_ch)

    # -----------------------------------------------------------------------
    # Save crops around first few yellow landmarks for visual inspection
    for (sid, cx, cy, badge_color, name) in LANDMARKS[:6]:
        cx, cy = int(cx), int(cy)
        pad = 20
        h_img, w_img = img.shape[:2]
        x1, x2 = max(0, cx-pad), min(w_img, cx+pad)
        y1, y2 = max(0, cy-pad), min(h_img, cy+pad)
        crop = img[y1:y2, x1:x2]
        # scale up 4x for readability
        big = cv2.resize(crop, None, fx=4, fy=4, interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(str(OUT_DIR / f"diag_crop_stn{sid}.png"), big)

    print(f"Diagnostic images written to {OUT_DIR}")
    print("HSV channel images: diag_hue.png  diag_sat.png  diag_val.png")
    print("Landmark crops: diag_crop_stn<id>.png")

if __name__ == "__main__":
    main()
