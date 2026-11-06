"""
build_atlas.py
==============
Divides the full calibrated board into an overlapping 5x4 grid (20 tiles)
and generates individual tile crops, index JSON, and a master atlas contact sheet.
"""

import cv2
import numpy as np
import json
from pathlib import Path

_HERE = Path(__file__).resolve().parent
img_full = cv2.imread(str(_HERE / 'output' / 'rectified_complete.png'))
out_dir = _HERE / 'output' / 'station_recovery' / 'atlas_tiles'
out_dir.mkdir(parents=True, exist_ok=True)

rows, cols = 4, 5
tile_w, tile_h = 380, 350
row_names = ['A', 'B', 'C', 'D']

tiles = []
for r_idx in range(rows):
    r_name = row_names[r_idx]
    y1 = int(round(r_idx * (1000 - tile_h) / (rows - 1)))
    y2 = y1 + tile_h
    for c_idx in range(cols):
        tile_id = f"{r_name}{c_idx+1}"
        x1 = int(round(c_idx * (1350 - tile_w) / (cols - 1)))
        x2 = x1 + tile_w

        crop = img_full[y1:y2, x1:x2].copy()
        cv2.imwrite(str(out_dir / f"{tile_id}.png"), crop)
        tiles.append({
            'tile_id': tile_id,
            'row': r_name,
            'col': c_idx + 1,
            'bounds_canvas_px': [x1, y1, x2, y2],
            'bounds_normalized': [round(x1/1350.0, 4), round(y1/1000.0, 4), round(x2/1350.0, 4), round(y2/1000.0, 4)],
            'dimensions': [tile_w, tile_h]
        })

atlas_meta = {
    'grid': {'rows': rows, 'cols': cols, 'total_tiles': len(tiles)},
    'canvas_dimensions': [1350, 1000],
    'tile_dimensions': [tile_w, tile_h],
    'overlap_px': {
        'horizontal': tile_w - int(round((1350 - tile_w)/(cols - 1))),
        'vertical': tile_h - int(round((1000 - tile_h)/(rows - 1)))
    },
    'tiles': tiles
}
index_path = _HERE / 'output' / 'station_recovery' / 'atlas_index.json'
index_path.write_text(json.dumps(atlas_meta, indent=2), encoding='utf-8')
print(f"Generated {len(tiles)} atlas tiles and saved index to {index_path.name}")

# Generate Contact Sheet
sheet = np.full((880, 1200, 3), 30, dtype=np.uint8)
for t in tiles:
    r_idx = ord(t['row']) - ord('A')
    c_idx = t['col'] - 1
    tile_img = cv2.imread(str(out_dir / f"{t['tile_id']}.png"))
    scaled = cv2.resize(tile_img, (236, 216))

    y0 = r_idx * 220 + 2
    x0 = c_idx * 240 + 2
    sheet[y0:y0+216, x0:x0+236] = scaled
    cv2.rectangle(sheet, (x0, y0), (x0+235, y0+215), (0, 200, 255), 1)
    cv2.rectangle(sheet, (x0+2, y0+2), (x0+55, y0+24), (0, 0, 0), -1)
    cv2.putText(sheet, t['tile_id'], (x0+6, y0+18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    b = t['bounds_canvas_px']
    coord_str = f"[{b[0]},{b[1]}]"
    cv2.putText(sheet, coord_str, (x0+6, y0+210), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

sheet_path = _HERE / 'output' / 'station_recovery' / 'atlas_contact_sheet.png'
cv2.imwrite(str(sheet_path), sheet)
print(f"Saved atlas contact sheet to {sheet_path.name}")
