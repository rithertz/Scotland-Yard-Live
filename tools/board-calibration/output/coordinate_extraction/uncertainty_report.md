# Uncertainty and Exception Report — Phase 3C.3-C.1

## Multi-Category Detector Parameters

### Yellow Taxi/Bus Badge Configuration:
- HSV lower: [20, 100, 100]
- HSV upper: [30, 255, 255]
- Area range: 30–3000 px²
- Bounding-box minimums: w≥8, h≥6 px
- Aspect range: 0.5–3.5
- Fill ratio minimum: 0.15
- Colour purity threshold: 70.0 ((R+G)/2 - B)

### Red Underground Badge Configuration:
- HSV Range 1: [0, 80, 60] to [9, 255, 255]
- HSV Range 2: [170, 80, 60] to [179, 255, 255]
- Area range: 30–1000 px²
- Bounding-box minimums: w≥10, h≥8 px
- Aspect range: 0.8–2.8
- Fill ratio minimum: 0.2
- Red dominance threshold: 65.0 (R - (G+B)/2)
- Required adjacent symbology: green bus arc or yellow stop

## Detection Statistics Per Image

| Image | Candidates | Accepted Yellow | Accepted Red | Ambiguous | Rejected |
|---|---|---|---|---|---|
| full | 790 | 81 | 13 | 10 | 696 |
| top-left | 97 | 5 | 2 | 0 | 90 |
| top-right | 137 | 8 | 1 | 1 | 128 |
| bottom-left | 197 | 12 | 4 | 1 | 181 |
| bottom-right | 172 | 10 | 2 | 1 | 160 |

## Rejection & Ambiguity Analysis
- **Route Line Segments:** Correctly rejected due to extreme aspect ratios (>3.5 or <0.5) and low fill factors.
- **Parks & River Water:** Rejection of green background by narrow yellow/red hue ranges and colour dominance checks.
- **Building Roofs:** Brownish-red building roofs rejected via strict red purity dominance and adjacent symbology verification.
- **Merged Features:** Candidates > 1200 px² or fill < 0.22 flagged as ambiguous for human review.

Generated: 2026-11-06T11:36:43.404564+00:00