"""
diag_badge_analysis.py
======================
Detailed analysis of badge contour geometry using the original narrow mask
which was shown to detect all badge outlines.
"""
import cv2
import numpy as np
from pathlib import Path
import json

IMG_DIR = Path(__file__).parent / "output"
OUT_DIR = IMG_DIR / "coordinate_extraction"

FULL_PATH = IMG_DIR / "rectified_complete.png"

# Known yellow badge approximate centres (x, y) on 1350x1000 canvas
YELLOW_BADGE_CENTRES = [
    (222, 18, 2),
    (115, 68, 8),
    (315, 95, 10),
    (80, 105, 18),
    (210, 125, 20),
    (245, 98, 21),
    (185, 180, 33),
    (410, 35, 3),
    (500, 45, 4),
    (640, 85, 14),
    (720, 150, 15),
    (420, 135, 23),
    (475, 175, 50),
    (745, 240, 29),
    (675, 195, 41),
]

def contour_stats(cnt):
    area = cv2.contourArea(cnt)
    peri = cv2.arcLength(cnt, True)
    circ = (4 * np.pi * area / peri**2) if peri > 0 else 0
    x, y, w, h = cv2.boundingRect(cnt)
    aspect = w / float(h) if h > 0 else 0
    fill = area / float(w * h) if w * h > 0 else 0
    approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
    return dict(area=area, peri=peri, circ=circ, bbox_w=w, bbox_h=h,
                aspect=aspect, fill=fill, vertices=len(approx))

def main():
    img = cv2.imread(str(FULL_PATH))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Use original narrow mask - this detected ALL badge outlines
    lower = np.array([20, 100, 100], dtype=np.uint8)
    upper = np.array([30, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k3)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k3)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Original narrow mask: {len(contours)} total contours")

    # Find contours closest to known yellow badge centres
    print()
    print("=== Properties of contours closest to known yellow badge centres ===")
    print(f"{'Stn':>4} {'SrcXY':>12}  {'cnt_cx':>7} {'cnt_cy':>7}  {'dist':>6}  "
          f"{'area':>7}  {'w':>5} {'h':>5}  {'aspect':>7}  {'fill':>6}  {'circ':>6}  {'verts':>6}")
    print("-" * 110)

    all_badge_stats = []
    for (bx, by, sid) in YELLOW_BADGE_CENTRES:
        best_cnt = None
        best_dist = 999999
        for cnt in contours:
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cx = M["m10"] / M["m00"]
            cy = M["m01"] / M["m00"]
            d = ((cx - bx)**2 + (cy - by)**2)**0.5
            if d < best_dist:
                best_dist = d
                best_cnt = cnt
                best_cx, best_cy = cx, cy
        if best_cnt is None:
            print(f"{sid:>4} ({bx:4},{by:4})  No contour found")
            continue
        s = contour_stats(best_cnt)
        print(f"{sid:>4} ({bx:4},{by:4})  {best_cx:7.1f} {best_cy:7.1f}  {best_dist:6.1f}  "
              f"{s['area']:7.1f}  {s['bbox_w']:5d} {s['bbox_h']:5d}  "
              f"{s['aspect']:7.3f}  {s['fill']:6.3f}  {s['circ']:6.3f}  {s['vertices']:6d}")
        all_badge_stats.append(s)

    # Distribution of ALL contours by area
    print()
    all_areas = [cv2.contourArea(c) for c in contours]
    print(f"=== All {len(all_areas)} contour area distribution ===")
    all_areas_np = np.array(all_areas)
    for pct in [5, 10, 25, 50, 75, 90, 95]:
        print(f"  p{pct:3d} = {np.percentile(all_areas_np, pct):.1f} px²")
    print(f"  max = {all_areas_np.max():.1f} px²")

    # Classify contours by area bucket and report stats
    print()
    print("=== Contour classification by area bucket ===")
    for lo, hi, label in [(0, 10, "tiny noise"), (10, 80, "small noise"),
                           (80, 400, "original range"), (400, 2000, "larger"),
                           (2000, 10000, "big"), (10000, 999999, "huge")]:
        bucket = [contour_stats(c) for c in contours
                  if lo <= cv2.contourArea(c) < hi]
        if not bucket:
            continue
        aspects = [s["aspect"] for s in bucket]
        circs = [s["circ"] for s in bucket]
        fills = [s["fill"] for s in bucket]
        print(f"  {label:20s} [{lo:6}-{hi:6}]: count={len(bucket):5d}  "
              f"aspect median={np.median(aspects):.2f}  "
              f"circ median={np.median(circs):.3f}  "
              f"fill median={np.median(fills):.3f}")

    # Build a classifier and report how many pass
    print()
    print("=== Classifier test: exclude route lines and noise ===")
    # From visual inspection: badges are roughly square-ish to 2:1 wide,
    # medium area, decent fill ratio. Route lines are very long and thin.
    accepted = []
    rejected_reasons = {}
    for cnt in contours:
        a = cv2.contourArea(cnt)
        s = contour_stats(cnt)
        reason = None
        if a < 30:
            reason = "area<30"
        elif a > 3000:
            reason = "area>3000"
        elif s["aspect"] > 3.5 or s["aspect"] < 0.5:
            reason = f"aspect={s['aspect']:.2f}"
        elif s["fill"] < 0.3:
            reason = f"fill={s['fill']:.2f}"
        elif s["bbox_w"] < 8 or s["bbox_h"] < 6:
            reason = f"bbox-too-small"
        else:
            accepted.append(cnt)
            continue
        rejected_reasons[reason] = rejected_reasons.get(reason, 0) + 1
    print(f"  Accepted: {len(accepted)}")
    print(f"  Rejected: {sum(rejected_reasons.values())}")
    print("  Rejection breakdown:")
    for r, n in sorted(rejected_reasons.items(), key=lambda x: -x[1]):
        print(f"    {r:30s}: {n}")

    # Save classifier output overlay
    vis = img.copy()
    for cnt in accepted:
        cv2.drawContours(vis, [cnt], -1, (0, 255, 0), 2)
        M = cv2.moments(cnt)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.circle(vis, (cx, cy), 3, (0, 200, 0), -1)
    cv2.imwrite(str(OUT_DIR / "diag_classifier_v1.png"), vis)
    print(f"\nSaved: diag_classifier_v1.png")

    # Detailed look at a few accepted contours
    print()
    print("=== Sample accepted contours (first 20) ===")
    print(f"{'cx':>7} {'cy':>7}  {'area':>7}  {'w':>5} {'h':>5}  {'aspect':>7}  {'fill':>6}  {'circ':>6}")
    for cnt in sorted(accepted, key=lambda c: cv2.moments(c)["m01"]/cv2.moments(c)["m00"] if cv2.moments(c)["m00"] else 0)[:20]:
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
        cx = M["m10"] / M["m00"]
        cy = M["m01"] / M["m00"]
        s = contour_stats(cnt)
        print(f"{cx:7.1f} {cy:7.1f}  {s['area']:7.1f}  {s['bbox_w']:5d} {s['bbox_h']:5d}  "
              f"{s['aspect']:7.3f}  {s['fill']:6.3f}  {s['circ']:6.3f}")

if __name__ == "__main__":
    main()
