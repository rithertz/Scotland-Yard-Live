"""
diag_kernel_sweep.py
====================
Sweep close kernel sizes and fill thresholds to find best parameters for
the repaired detector, measuring acceptance rate against known badge positions.
"""
import cv2
import numpy as np
from pathlib import Path

IMG_DIR = Path(__file__).parent / "output"
OUT_DIR = IMG_DIR / "coordinate_extraction"

FULL_PATH = IMG_DIR / "rectified_complete.png"

# Known yellow badge approximate centres (x, y) on 1350x1000 canvas
YELLOW_BADGE_CENTRES = [
    (222, 18), (115, 68), (315, 95), (80, 105), (210, 125),
    (245, 98), (185, 180), (410, 35), (500, 45), (640, 85),
    (720, 150), (420, 135), (475, 175), (745, 240), (675, 195),
    # Add more from landmarks.py top-right quadrant
    (745, 240), (1025, 50), (1137, 49), (1248, 58), (830, 88),
    (620, 114), (280, 140), (1242, 144), (1279, 160), (955, 164),
]

def try_params(img, hsv, close_k, fill_min, area_min=30, area_max=3000,
               aspect_min=0.5, aspect_max=3.5):
    lo = np.array([20, 100, 100], dtype=np.uint8)
    hi = np.array([30, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lo, hi)
    k_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k_open)
    k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close_k, close_k))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k_close)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    accepted = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if not (area_min <= area <= area_max):
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        if w < 8 or h < 6:
            continue
        aspect = w / float(h) if h else 0
        if not (aspect_min <= aspect <= aspect_max):
            continue
        fill = area / float(w * h) if w * h else 0
        if fill < fill_min:
            continue
        M = cv2.moments(cnt)
        if M["m00"] > 0:
            cx = M["m10"] / M["m00"]
            cy = M["m01"] / M["m00"]
            accepted.append((cx, cy, cnt))

    # Count how many known badge centres are within 20px of an accepted centroid
    hit = 0
    for (bx, by) in YELLOW_BADGE_CENTRES:
        for (cx, cy, _) in accepted:
            if ((cx - bx)**2 + (cy - by)**2)**0.5 < 20:
                hit += 1
                break

    return len(accepted), hit

def main():
    img = cv2.imread(str(FULL_PATH))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    total_known = len(set(YELLOW_BADGE_CENTRES))

    print(f"{'close_k':>8} {'fill_min':>8} {'accepted':>9} {'hits':>5}/{total_known:d}")
    print("-" * 50)

    best = None
    for close_k in [7, 9, 11, 13, 15]:
        for fill_min in [0.20, 0.25, 0.30, 0.35]:
            n_acc, hits = try_params(img, hsv, close_k, fill_min)
            line = f"{close_k:>8d} {fill_min:>8.2f} {n_acc:>9d} {hits:>5d}"
            print(line)
            if best is None or (hits >= best[2] and n_acc <= best[3] + 50):
                best = (close_k, fill_min, hits, n_acc)

    print()
    if best:
        print(f"Best params: close_k={best[0]}, fill_min={best[1]} → "
              f"hits={best[2]}/{total_known}, accepted={best[3]}")

if __name__ == "__main__":
    main()
