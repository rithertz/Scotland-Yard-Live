"""Independent pairwise/global registration for Phase 3F.2.1.

The graph is built from SIFT matches between neighboring original JPEGs. The
Phase 3D.3 homographies are used only to place the independently composed graph
into the existing provisional 1350x1000 reference frame; they are not used to
derive pairwise transformations or to select the global tree.
"""

from __future__ import annotations

import json
from pathlib import Path

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SOURCE = REPO / "docs" / "game" / "evidence" / "board-photos" / "high-resolution"
OLD_REGISTRATION = HERE / "output" / "station_recovery" / "phase_3d3_registration_metadata.json"
OUT = HERE / "output" / "phase_3f2_1_registration"
CANVAS = (1350, 1000)
SCALE = 2
MASTER = (CANVAS[0] * SCALE, CANVAS[1] * SCALE)
NAMES = [f"{row}{col}.jpg" for row in "ABCD" for col in range(1, 5)]


def feature_data() -> dict[str, tuple[list, np.ndarray, float, tuple[int, int]]]:
    sift = cv2.SIFT_create(nfeatures=5000)
    data = {}
    for name in NAMES:
        image = cv2.imread(str(SOURCE / name), cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise RuntimeError(f"Cannot read {name}")
        scale = min(1.0, 1600.0 / max(image.shape))
        small = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA) if scale < 1 else image
        keypoints, descriptors = sift.detectAndCompute(small, None)
        data[name] = (keypoints, descriptors, scale, (int(image.shape[1]), int(image.shape[0])))
    return data


def adjacent_pairs() -> list[tuple[str, str]]:
    pairs = []
    for row in "ABCD":
        for col in range(1, 4):
            pairs.append((f"{row}{col}.jpg", f"{row}{col + 1}.jpg"))
    for col in range(1, 5):
        for row in "ABC":
            pairs.append((f"{row}{col}.jpg", f"{chr(ord(row) + 1)}{col}.jpg"))
    return pairs


def match_pair(a: str, b: str, features: dict) -> dict:
    ka, da, sa, _ = features[a]
    kb, db, sb, _ = features[b]
    matcher = cv2.BFMatcher()
    pairs = matcher.knnMatch(da, db, k=2)
    good = [pair[0] for pair in pairs if len(pair) == 2 and pair[0].distance < 0.72 * pair[1].distance]
    src = np.float32([ka[m.queryIdx].pt for m in good]) / sa
    dst = np.float32([kb[m.trainIdx].pt for m in good]) / sb
    H, mask = cv2.findHomography(src, dst, cv2.RANSAC, 6.0) if len(good) >= 8 else (None, None)
    errors = np.array([], dtype=float)
    inlier_points = []
    if H is not None and mask is not None:
        projected = cv2.perspectiveTransform(src.reshape(-1, 1, 2), H).reshape(-1, 2)
        inlier_mask = mask.ravel().astype(bool)
        errors = np.linalg.norm(projected[inlier_mask] - dst[inlier_mask], axis=1)
        inlier_points = src[inlier_mask].tolist()
    inliers = int(len(errors))
    return {
        "a": a,
        "b": b,
        "good_matches": len(good),
        "inliers": inliers,
        "inlier_ratio": round(inliers / max(len(good), 1), 4),
        "mean_reprojection_error_px": round(float(errors.mean()), 4) if inliers else None,
        "median_reprojection_error_px": round(float(np.median(errors)), 4) if inliers else None,
        "max_reprojection_error_px": round(float(errors.max()), 4) if inliers else None,
        "homography_a_to_b": H.tolist() if H is not None else None,
        "inlier_points_a": inlier_points,
        "reliable_for_global_tree": bool(inliers >= 30 and inliers / max(len(good), 1) >= 0.10),
    }


class UnionFind:
    def __init__(self, items: list[str]):
        self.parent = {item: item for item in items}

    def find(self, item: str) -> str:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, a: str, b: str) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[rb] = ra
        return True


def global_tree(edges: list[dict]) -> list[dict]:
    chosen = []
    uf = UnionFind(NAMES)
    ordered = sorted(edges, key=lambda e: (e["reliable_for_global_tree"], e["inliers"], e["inlier_ratio"]), reverse=True)
    for edge in ordered:
        if uf.union(edge["a"], edge["b"]):
            chosen.append(edge)
        if len(chosen) == len(NAMES) - 1:
            break
    if len(chosen) != len(NAMES) - 1:
        raise RuntimeError(f"Neighbor graph did not connect all photos: {len(chosen)} edges")
    return chosen


def compose_transforms(tree: list[dict], anchor: str) -> dict[str, np.ndarray]:
    adjacency: dict[str, list[tuple[str, np.ndarray]]] = {name: [] for name in NAMES}
    for edge in tree:
        H = np.asarray(edge["homography_a_to_b"], dtype=float)
        adjacency[edge["a"]].append((edge["b"], H))
        adjacency[edge["b"]].append((edge["a"], np.linalg.inv(H)))
    transforms = {anchor: np.eye(3, dtype=float)}
    pending = [anchor]
    while pending:
        current = pending.pop(0)
        for neighbor, H_current_to_neighbor in adjacency[current]:
            if neighbor in transforms:
                continue
            transforms[neighbor] = transforms[current] @ np.linalg.inv(H_current_to_neighbor)
            pending.append(neighbor)
    return transforms


def loop_consistency(edges: list[dict], transforms: dict[str, np.ndarray]) -> list[dict]:
    results = []
    for edge in edges:
        H = np.asarray(edge["homography_a_to_b"], dtype=float)
        points = np.asarray(edge["inlier_points_a"], dtype=np.float32)
        if len(points) == 0:
            results.append({"a": edge["a"], "b": edge["b"], "status": "unmeasured"})
            continue
        direct = cv2.perspectiveTransform(points.reshape(-1, 1, 2), H).reshape(-1, 2)
        ga = cv2.perspectiveTransform(points.reshape(-1, 1, 2), transforms[edge["a"]]).reshape(-1, 2)
        gb = cv2.perspectiveTransform(direct.reshape(-1, 1, 2), transforms[edge["b"]]).reshape(-1, 2)
        error = np.linalg.norm(ga - gb, axis=1)
        results.append({"a": edge["a"], "b": edge["b"], "samples": len(error), "mean_loop_error_px": round(float(error.mean()), 4), "median_loop_error_px": round(float(np.median(error)), 4), "max_loop_error_px": round(float(error.max()), 4), "status": "consistent" if float(np.median(error)) < 8 else "inconsistent"})
    return results


def compose_master(transforms: dict[str, np.ndarray], old_metadata: dict) -> tuple[np.ndarray, np.ndarray]:
    anchor = "A1.jpg"
    old_by_name = {record["filename"]: np.asarray(record["homography_source_to_canvas"], dtype=float) for record in old_metadata["registrations"]}
    # Absolute board-frame anchoring is retained only for compatibility with
    # stations.json; all relative source transforms above are independent.
    anchor_to_reference = old_by_name[anchor]
    accum = np.zeros((MASTER[1], MASTER[0], 3), dtype=np.float32)
    weights = np.zeros((MASTER[1], MASTER[0]), dtype=np.float32)
    coverage = np.zeros((MASTER[1], MASTER[0]), dtype=np.uint8)
    for name in NAMES:
        image = cv2.imread(str(SOURCE / name), cv2.IMREAD_COLOR)
        source_mask = np.full(image.shape[:2], 255, dtype=np.uint8)
        source_to_reference = anchor_to_reference @ transforms[name]
        scale_matrix = np.diag([SCALE, SCALE, 1.0]).astype(float)
        H = scale_matrix @ source_to_reference
        warped = cv2.warpPerspective(image, H, MASTER, flags=cv2.INTER_LANCZOS4)
        valid = cv2.warpPerspective(source_mask, H, MASTER, flags=cv2.INTER_NEAREST)
        binary = (valid > 0).astype(np.uint8)
        distance = cv2.distanceTransform(binary, cv2.DIST_L2, 3)
        weight = np.clip(distance / 48.0, 0.0, 1.0) * binary
        accum += warped.astype(np.float32) * weight[..., None]
        weights += weight
        coverage = np.maximum(coverage, valid)
    output = np.zeros_like(accum, dtype=np.uint8)
    valid = weights > 1e-6
    output[valid] = np.clip(accum[valid] / weights[valid, None], 0, 255).astype(np.uint8)
    return output, coverage


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    features = feature_data()
    edges = [match_pair(a, b, features) for a, b in adjacent_pairs()]
    tree = global_tree(edges)
    transforms = compose_transforms(tree, "A1.jpg")
    loops = loop_consistency(edges, transforms)
    old_metadata = json.loads(OLD_REGISTRATION.read_text(encoding="utf-8"))
    master, coverage = compose_master(transforms, old_metadata)
    cv2.imwrite(str(OUT / "board_master_global_2x.png"), master, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    cv2.imwrite(str(OUT / "board_master_global_2x.webp"), master, [cv2.IMWRITE_WEBP_QUALITY, 95])
    per_photo = []
    for name in NAMES:
        incident = [edge for edge in edges if edge["a"] == name or edge["b"] == name]
        per_photo.append({
            "filename": name,
            "source_dimensions": list(features[name][3]),
            "neighbor_edges": len(incident),
            "weak_neighbor_edges": sum(not edge["reliable_for_global_tree"] for edge in incident),
            "global_transform_to_anchor": transforms[name].tolist(),
            "registration_confidence": "high" if all(edge["reliable_for_global_tree"] for edge in incident) else "limited_by_weak_overlap",
        })
    document = {
        "phase": "3F.2.1",
        "status": "independent_global_registration_diagnostic",
        "anchor": "A1.jpg",
        "source_files": NAMES,
        "method": "SIFT features on original JPEGs, Lowe ratio 0.72, pairwise RANSAC homographies on neighboring grid overlaps, maximum-confidence spanning tree, loop consistency audit.",
        "absolute_frame_note": "The existing A1-to-1350x1000 homography is used only to express the independently composed graph in the existing provisional board frame; it is not used for pairwise registration or tree selection.",
        "tree_edges": [{"a": e["a"], "b": e["b"], "inliers": e["inliers"], "mean_reprojection_error_px": e["mean_reprojection_error_px"], "inlier_ratio": e["inlier_ratio"]} for e in tree],
        "per_photo_registration": per_photo,
        "pairwise_edges": edges,
        "loop_consistency": loops,
        "global_transforms_to_anchor": {name: matrix.tolist() for name, matrix in transforms.items()},
        "coverage": {"pixels": int(np.count_nonzero(coverage)), "total": int(coverage.size), "percent": round(float(np.count_nonzero(coverage) / coverage.size * 100), 4)},
        "output": {"png": "tools/board-calibration/output/phase_3f2_1_registration/board_master_global_2x.png", "webp": "tools/board-calibration/output/phase_3f2_1_registration/board_master_global_2x.webp", "dimensions": [MASTER[0], MASTER[1]]},
        "integration_safe": False,
        "integration_reason": "Global diagnostic requires visual seam review and independent absolute-frame validation before frontend use.",
    }
    (OUT / "registration_report.json").write_text(json.dumps(document, indent=2), encoding="utf-8")
    stations = json.loads((REPO / "packages" / "board-data" / "data" / "stations.json").read_text(encoding="utf-8"))["stations"]
    (OUT / "station_registration_diagnostic.json").write_text(json.dumps({
        "phase": "3F.2.1",
        "status": "provisional_compatibility_only",
        "source_canvas": {"width": CANVAS[0], "height": CANVAS[1]},
        "master_canvas": {"width": MASTER[0], "height": MASTER[1]},
        "transformation": "existing reference coordinate × 2; global absolute frame remains dependent on provisional A1 anchor homography",
        "stations": [{"station_id": station["id"], "reference_coordinate": station["coordinate"], "master_coordinate": {"x": station["coordinate"]["x"] * MASTER[0], "y": station["coordinate"]["y"] * MASTER[1]}, "status": "provisional_alignment"} for station in stations],
    }, indent=2), encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Phase 3F.2.1 independent registration diagnostic\n\n"
        "This output uses independent SIFT/RANSAC pairwise homographies between neighboring original JPEGs, a maximum-confidence spanning tree, and loop-consistency measurements. The existing A1-to-reference homography is used only for absolute-frame compatibility.\n\n"
        "The global diagnostic is not frontend-safe: inspect `registration_report.json` for weak edges and inconsistent loops. The generated master is evidence of the current failure mode, not a canonical asset.\n\n"
        "- `registration_report.json` — pairwise matches, tree, loops, and per-photo transforms\n"
        "- `station_registration_diagnostic.json` — unchanged station data expressed in the provisional master frame\n"
        "- `board_master_global_2x.png` / `.webp` — diagnostic composite\n",
        encoding="utf-8",
    )
    print(json.dumps({"tree_edges": len(tree), "inconsistent_loops": sum(loop["status"] == "inconsistent" for loop in loops), "coverage_percent": document["coverage"]["percent"], "integration_safe": False}, indent=2))


if __name__ == "__main__":
    main()
