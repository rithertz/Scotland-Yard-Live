"""
diag_badge_size.py
==================
Measure actual badge pixel dimensions to set correct area/aspect thresholds.
"""
import cv2
import numpy as np
from pathlib import Path

IMG_DIR = Path(__file__).parent / "output"
OUT_DIR = IMG_DIR / "coordinate_extraction"

FULL_PATH = IMG_DIR / "rectified_complete.png"

# Known yellow badge approximate centres (x, y) on 1350x1000 canvas
YELLOW_BADGES = [
    (222, 18),   # stn 2
    (315, 95),   # stn 10
    (210, 125),  # stn 20
    (245, 98),   # stn 21
    (185, 180),  # stn 33
    (410, 35),   # stn 3
    (500, 45),   # stn 4
    (640, 85),   # stn 14
    (720, 150),  # stn 15
    (420, 135),  # stn 23
]

def main():
    img = cv2.imread(str(FULL_PATH))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Use the "slightly broader" threshold that showed good badge detection
    lower = np.array([15, 80, 80], dtype=np.uint8)
    upper = np.array([45, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Total contours from broader mask: {len(contours)}")
    print()

    # For each known badge, find the closest contour centroid and report its dimensions
    print(f"{'StnXY':>12}  {'cnt_cx':>7} {'cnt_cy':>7}  {'dist':>6}  "
          f"{'area':>7}  {'bbox_w':>7} {'bbox_h':>7}  {'aspect':>7}  {'fill':>6}  {'vertices':>8}")
    print("-" * 100)

    for (bx, by) in YELLOW_BADGES:
        best_cnt = None
        best_dist = 999999
        for cnt in contours:
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cx = M["m10"] / M["m00"]
            cy = M["m01"] / M["m00"]
            d = ((cx - bx) ** 2 + (cy - by) ** 2) ** 0.5
            if d < best_dist:
                best_dist = d
                best_cnt = cnt
                best_cx, best_cy = cx, cy
        if best_cnt is None:
            print(f"({bx:4},{by:4})  No contour found")
            continue
        area = cv2.contourArea(best_cnt)
        x, y, w, h = cv2.boundingRect(best_cnt)
        aspect = w / float(h) if h else 0
        fill = area / float(w * h) if (w * h) else 0
        peri = cv2.arcLength(best_cnt, True)
        approx = cv2.approxPolyDP(best_cnt, 0.04 * peri, True)
        print(f"({bx:4},{by:4})  {best_cx:7.1f} {best_cy:7.1f}  {best_dist:6.1f}  "
              f"{area:7.1f}  {w:7d} {h:7d}  {aspect:7.3f}  {fill:6.3f}  {len(approx):8d}")

    print()
    # Overall size distribution for all plausible contours
    areas = []
    widths = []
    heights = []
    aspects = []
    for cnt in contours:
        a = cv2.contourArea(cnt)
        if 50 < a < 15000:
            x, y, w, h = cv2.boundingRect(cnt)
            areas.append(a)
            widths.append(w)
            heights.append(h)
            aspects.append(w / float(h) if h else 0)

    areas = np.array(areas)
    widths = np.array(widths)
    heights = np.array(heights)
    aspects = np.array(aspects)
    print(f"Plausible contour (50<area<15000) count: {len(areas)}")
    print(f"  Area   : p5={np.percentile(areas,5):.0f}  p25={np.percentile(areas,25):.0f}  "
          f"median={np.median(areas):.0f}  p75={np.percentile(areas,75):.0f}  "
          f"p95={np.percentile(areas,95):.0f}  max={areas.max():.0f}")
    print(f"  Width  : p5={np.percentile(widths,5):.0f}  median={np.median(widths):.0f}  "
          f"p95={np.percentile(widths,95):.0f}")
    print(f"  Height : p5={np.percentile(heights,5):.0f}  median={np.median(heights):.0f}  "
          f"p95={np.percentile(heights,95):.0f}")
    print(f"  Aspect : p5={np.percentile(aspects,5):.2f}  median={np.median(aspects):.2f}  "
          f"p95={np.percentile(aspects,95):.2f}")

    # Save a zoomed overlay of contours near known badges
    vis = img.copy()
    for cnt in contours:
        a = cv2.contourArea(cnt)
        if 50 < a < 15000:
            cv2.drawContours(vis, [cnt], -1, (0, 255, 0), 1)
    for (bx, by) in YELLOW_BADGES:
        cv2.circle(vis, (bx, by), 5, (0, 0, 255), -1)
    cv2.imwrite(str(OUT_DIR / "diag_badge_size.png"), vis)
    print(f"\nSaved overlay: {OUT_DIR / 'diag_badge_size.png'}")

if __name__ == "__main__":
    main()
