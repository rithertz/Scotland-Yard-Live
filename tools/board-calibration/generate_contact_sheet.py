"""
generate_contact_sheet.py
=========================
Generates a side-by-side contact sheet of all 15 cross-image groups,
showing the label block, the full-board reference crop, and up to two
close-up quadrant crops with crosshairs and metrics.
"""

import cv2
import numpy as np
import json
from pathlib import Path

img_full = cv2.imread('tools/board-calibration/output/rectified_complete.png')
quad_imgs = {
    'top-left': cv2.imread('tools/board-calibration/output/registered_top-left.png'),
    'top-right': cv2.imread('tools/board-calibration/output/registered_top-right.png'),
    'bottom-left': cv2.imread('tools/board-calibration/output/registered_bottom-left.png'),
    'bottom-right': cv2.imread('tools/board-calibration/output/registered_bottom-right.png'),
}

reconciled = json.loads(Path('tools/board-calibration/output/coordinate_extraction/reconciled_coordinate_inventory.json').read_text(encoding='utf-8'))
raw = json.loads(Path('tools/board-calibration/output/coordinate_extraction/coordinate_inventory.json').read_text(encoding='utf-8'))
raw_dict = {r['detection_id']: r for r in raw}

cross_groups = [f for f in reconciled['features'] if len(f['contributing_sources']) > 1]

CROP_SIZE = 120
HALF = CROP_SIZE // 2
ROW_H = 120
LABEL_W = 340
TOTAL_W = LABEL_W + CROP_SIZE * 3
TOTAL_H = ROW_H * len(cross_groups)

sheet = np.full((TOTAL_H, TOTAL_W, 3), 245, dtype=np.uint8)

def get_crop(src_img, cx, cy, marker_color):
    h, w = src_img.shape[:2]
    ix, iy = int(round(cx)), int(round(cy))
    x1, y1 = ix - HALF, iy - HALF
    x2, y2 = x1 + CROP_SIZE, y1 + CROP_SIZE

    pad_left = max(0, -x1)
    pad_top = max(0, -y1)
    pad_right = max(0, x2 - w)
    pad_bottom = max(0, y2 - h)

    sx1, sy1 = max(0, x1), max(0, y1)
    sx2, sy2 = min(w, x2), min(h, y2)

    sub = src_img[sy1:sy2, sx1:sx2].copy()
    if pad_left > 0 or pad_top > 0 or pad_right > 0 or pad_bottom > 0:
        sub = cv2.copyMakeBorder(sub, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=(0,0,0))

    cc = HALF
    cv2.drawMarker(sub, (cc, cc), marker_color, markerType=cv2.MARKER_CROSS, markerSize=12, thickness=1)
    cv2.circle(sub, (cc, cc), 6, marker_color, 1)
    cv2.rectangle(sub, (0, 0), (CROP_SIZE-1, CROP_SIZE-1), (80, 80, 80), 1)
    return sub

for idx, g in enumerate(cross_groups):
    y_start = idx * ROW_H
    fid = g['provisional_feature_id']
    cat = g['category']
    deriv = g['derivation']
    stat = g['status']
    disc = g['spatial_discrepancy_px']
    px, py = g['pixel_x'], g['pixel_y']
    dids = g['contributing_detection_ids']

    cv2.rectangle(sheet, (0, y_start), (LABEL_W, y_start + ROW_H), (235, 238, 240) if idx%2==0 else (245, 248, 250), -1)
    cv2.rectangle(sheet, (0, y_start), (TOTAL_W-1, y_start + ROW_H-1), (180, 180, 180), 1)

    cv2.putText(sheet, f"{fid} ({cat}) - {deriv}", (10, y_start + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.40, (20, 20, 20), 1)
    cv2.putText(sheet, f"Status: {stat} | Disc: {disc:.2f}px", (10, y_start + 42), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (40, 40, 40), 1)
    cv2.putText(sheet, f"Chosen: ({px:.1f}, {py:.1f})", (10, y_start + 62), cv2.FONT_HERSHEY_SIMPLEX, 0.36, (70, 70, 70), 1)

    if len(dids) <= 2:
        cv2.putText(sheet, f"Raw: {dids[0]}, {dids[1]}", (10, y_start + 85), cv2.FONT_HERSHEY_SIMPLEX, 0.34, (90, 40, 0), 1)
    else:
        cv2.putText(sheet, f"Raw: {dids[0]}, {dids[1]},", (10, y_start + 82), cv2.FONT_HERSHEY_SIMPLEX, 0.33, (90, 40, 0), 1)
        cv2.putText(sheet, f"     {dids[2]}", (10, y_start + 98), cv2.FONT_HERSHEY_SIMPLEX, 0.33, (90, 40, 0), 1)

    full_did = [d for d in dids if raw_dict[d]['source_image'] == 'full'][0]
    fr = raw_dict[full_did]
    fx, fy = fr['normalized_x'] * 1350, fr['normalized_y'] * 1000
    crop_f = get_crop(img_full, fx, fy, (0, 0, 255))
    cv2.putText(crop_f, 'Full Ref', (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)
    sheet[y_start:y_start+ROW_H, LABEL_W:LABEL_W+CROP_SIZE] = crop_f

    quad_dids = [d for d in dids if raw_dict[d]['source_image'] != 'full']
    for q_i, q_did in enumerate(quad_dids):
        qr = raw_dict[q_did]
        q_src = qr['source_image']
        qx, qy = qr['normalized_x'] * 1350, qr['normalized_y'] * 1000
        crop_q = get_crop(quad_imgs[q_src], qx, qy, (0, 220, 0))
        cv2.putText(crop_q, f"{q_src}", (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)
        x_pos = LABEL_W + CROP_SIZE * (q_i + 1)
        sheet[y_start:y_start+ROW_H, x_pos:x_pos+CROP_SIZE] = crop_q

    if len(quad_dids) < 2:
        x_pos = LABEL_W + CROP_SIZE * 2
        blank = np.full((ROW_H, CROP_SIZE, 3), 220, dtype=np.uint8)
        cv2.putText(blank, 'N/A (Pair)', (25, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (140, 140, 140), 1)
        cv2.rectangle(blank, (0, 0), (CROP_SIZE-1, CROP_SIZE-1), (180, 180, 180), 1)
        sheet[y_start:y_start+ROW_H, x_pos:x_pos+CROP_SIZE] = blank

out_path = Path('tools/board-calibration/output/coordinate_extraction/cross_image_groups_contact_sheet.png')
cv2.imwrite(str(out_path), sheet)
print('Saved contact sheet to:', out_path)
