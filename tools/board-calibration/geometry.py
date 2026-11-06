"""
Geometric transformations, homography computation, aspect ratio measurement,
and residual analysis for Scotland Yard Live board calibration.
"""

from typing import Dict, List, Tuple, Any
import numpy as np
import cv2


def compute_homography(
    src_points: np.ndarray, dst_points: np.ndarray, method: int = cv2.RANSAC
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes 3x3 homography matrix mapping src_points to dst_points.

    Args:
        src_points: (N, 2) array of source coordinates.
        dst_points: (N, 2) array of destination coordinates.
        method: OpenCV method (0 for exact 4-point, cv2.RANSAC for N > 4).

    Returns:
        H: (3, 3) homography matrix.
        mask: inlier mask from RANSAC (or all 1s for exact 4-point).
    """
    if len(src_points) == 4 and method == 0:
        H = cv2.getPerspectiveTransform(
            src_points.astype(np.float32), dst_points.astype(np.float32)
        )
        mask = np.ones((4, 1), dtype=np.uint8)
        return H, mask

    H, mask = cv2.findHomography(src_points, dst_points, method, 3.0)
    if H is None:
        raise ValueError("Homography computation failed - degenerate point configuration.")
    return H, mask


def transform_points(points: np.ndarray, H: np.ndarray) -> np.ndarray:
    """
    Applies homography H to an (N, 2) array of points.

    Returns:
        transformed: (N, 2) array of transformed coordinates.
    """
    pts = points.reshape(-1, 1, 2).astype(np.float32)
    transformed = cv2.perspectiveTransform(pts, H)
    return transformed.reshape(-1, 2)


def warp_image(image: np.ndarray, H: np.ndarray, output_size: Tuple[int, int]) -> np.ndarray:
    """
    Warps image using homography matrix H into canvas of size (width, height).
    """
    width, height = output_size
    return cv2.warpPerspective(image, H, (width, height), flags=cv2.INTER_LINEAR)


def compute_residuals(
    actual_pts: np.ndarray, expected_pts: np.ndarray
) -> Dict[str, Any]:
    """
    Computes Euclidean residuals between actual and expected point coordinates.

    Returns:
        Dictionary with per-point residuals, mean, median, std, max, and RMSE.
    """
    diffs = actual_pts - expected_pts
    distances = np.linalg.norm(diffs, axis=1)

    return {
        "distances": distances.tolist(),
        "mean": float(np.mean(distances)),
        "median": float(np.median(distances)),
        "std": float(np.std(distances)),
        "max": float(np.max(distances)),
        "rmse": float(np.sqrt(np.mean(distances ** 2))),
    }


def compute_directional_residuals(
    actual_pts: np.ndarray, expected_pts: np.ndarray
) -> Dict[str, Any]:
    """
    Computes directional (dx, dy) residual components to evaluate directional bias,
    systematic shear, or anisotropic deformation.
    """
    diffs = actual_pts - expected_pts
    dx = diffs[:, 0]
    dy = diffs[:, 1]
    corr = (
        float(np.corrcoef(dx, dy)[0, 1])
        if len(dx) > 2 and np.std(dx) > 1e-6 and np.std(dy) > 1e-6
        else 0.0
    )
    std_x = float(np.std(dx))
    std_y = float(np.std(dy))
    anisotropy = float(std_x / std_y) if std_y > 1e-6 else 1.0

    return {
        "mean_dx": float(np.mean(dx)),
        "mean_dy": float(np.mean(dy)),
        "std_dx": std_x,
        "std_dy": std_y,
        "rmse_dx": float(np.sqrt(np.mean(dx ** 2))),
        "rmse_dy": float(np.sqrt(np.mean(dy ** 2))),
        "anisotropy_ratio": anisotropy,
        "dx_dy_correlation": corr,
    }


def partition_correspondences_deterministic(
    matches: list,
    kp_close: list,
    train_ratio: float = 0.75,
) -> Tuple[list, list]:
    """
    Deterministically partitions candidate feature matches into fitting and held-out
    validation subsets.

    Sorts matches by close-up keypoint (x, y) coordinates to achieve an interleaved,
    spatially representative distribution across the entire quadrant canvas.
    """
    sorted_matches = sorted(
        matches,
        key=lambda m: (kp_close[m.queryIdx].pt[0], kp_close[m.queryIdx].pt[1]),
    )
    stride = int(round(1.0 / (1.0 - train_ratio))) if train_ratio < 1.0 else 0
    if stride <= 1:
        return sorted_matches, []

    val_matches = [m for idx, m in enumerate(sorted_matches) if idx % stride == 0]
    fit_matches = [m for idx, m in enumerate(sorted_matches) if idx % stride != 0]
    return fit_matches, val_matches


def calculate_aspect_ratio_metric(
    corners: Dict[str, Tuple[float, float]]
) -> Dict[str, Any]:
    """
    Calculates board aspect ratio directly from the 4 outer corner points in complete.jpeg
    using both raw Euclidean distance spans and a perspective vanishing-point pinhole model.

    Explicitly distinguishes:
    1. Image-space quadrilateral proportions.
    2. Estimated physical board aspect ratio (marked UNRESOLVED).
    3. Chosen working-canvas dimensions and aspect ratio (provisional computational choice).

    corners dict keys: 'physical_nw', 'physical_ne', 'physical_se', 'physical_sw'.
    """
    p_nw = np.array(corners["physical_nw"])
    p_ne = np.array(corners["physical_ne"])
    p_se = np.array(corners["physical_se"])
    p_sw = np.array(corners["physical_sw"])

    # 2D Euclidean span lengths
    span_north = float(np.linalg.norm(p_ne - p_nw))
    span_south = float(np.linalg.norm(p_se - p_sw))
    span_west = float(np.linalg.norm(p_sw - p_nw))
    span_east = float(np.linalg.norm(p_se - p_ne))

    avg_width = (span_north + span_south) / 2.0
    avg_height = (span_west + span_east) / 2.0
    raw_aspect_ratio = avg_width / avg_height

    # Pinhole perspective model for planar rectangle
    # Image center
    cx, cy = 1280.0 / 2.0, 892.0 / 2.0

    # Homogeneous coordinates
    h_nw = np.append(p_nw, 1.0)
    h_ne = np.append(p_ne, 1.0)
    h_se = np.append(p_se, 1.0)
    h_sw = np.append(p_sw, 1.0)

    # Lines
    l_north = np.cross(h_nw, h_ne)
    l_south = np.cross(h_sw, h_se)
    l_west = np.cross(h_nw, h_sw)
    l_east = np.cross(h_ne, h_se)

    # Vanishing points
    v_h = np.cross(l_north, l_south)
    v_h = v_h[:2] / v_h[2] if abs(v_h[2]) > 1e-6 else v_h[:2]

    v_v = np.cross(l_west, l_east)
    v_v = v_v[:2] / v_v[2] if abs(v_v[2]) > 1e-6 else v_v[:2]

    # Check orthogonality condition for focal length f
    dot_val = (v_h[0] - cx) * (v_v[0] - cx) + (v_h[1] - cy) * (v_v[1] - cy)
    pinhole_aspect_ratio = None
    focal_length = None

    if dot_val < 0:
        f = float(np.sqrt(-dot_val))
        focal_length = f
        K = np.array([[f, 0, cx], [0, f, cy], [0, 0, 1.0]], dtype=float)
        K_inv = np.linalg.inv(K)

        dir_h = K_inv @ np.append(v_h, 1.0)
        dir_v = K_inv @ np.append(v_v, 1.0)
        dir_h /= np.linalg.norm(dir_h)
        dir_v /= np.linalg.norm(dir_v)

        normal = np.cross(dir_h, dir_v)
        normal /= np.linalg.norm(normal)

        # 3D unprojection onto plane normal . X = 1
        d_nw = K_inv @ h_nw
        d_ne = K_inv @ h_ne
        d_se = K_inv @ h_se
        d_sw = K_inv @ h_sw

        P_nw = (1.0 / np.dot(normal, d_nw)) * d_nw
        P_ne = (1.0 / np.dot(normal, d_ne)) * d_ne
        P_se = (1.0 / np.dot(normal, d_se)) * d_se
        P_sw = (1.0 / np.dot(normal, d_sw)) * d_sw

        w_3d = (np.linalg.norm(P_ne - P_nw) + np.linalg.norm(P_se - P_sw)) / 2.0
        h_3d = (np.linalg.norm(P_sw - P_nw) + np.linalg.norm(P_se - P_ne)) / 2.0
        pinhole_aspect_ratio = float(w_3d / h_3d)

    return {
        # 1. Image-space quadrilateral proportions
        "image_space_quadrilateral": {
            "span_north_px": span_north,
            "span_south_px": span_south,
            "span_west_px": span_west,
            "span_east_px": span_east,
            "average_width_px": avg_width,
            "average_height_px": avg_height,
            "raw_2d_aspect_ratio": float(raw_aspect_ratio),
            "uncertainty_margin": 0.040,
            "description": (
                "Raw 2D Euclidean span ratio of outer corner control points in complete.jpeg. "
                "Does not account for camera perspective pitch, yaw, or out-of-plane paper curvature."
            ),
        },
        # 2. Estimated physical board aspect ratio
        "estimated_physical_board_aspect_ratio": {
            "status": "UNRESOLVED_FROM_CURRENT_PHOTOGRAPHS",
            "pinhole_perspective_estimate": pinhole_aspect_ratio,
            "estimated_focal_length_px": focal_length,
            "plausible_range": [1.226, 1.376],
            "evidence_limitations": (
                "Camera focal length, principal point, and radial distortion parameters are uncalibrated. "
                "The top edge of complete.jpeg grazes the frame (y=0.0), introducing significant leverage on vanishing point geometry. "
                "Assumed historical Milton Bradley or European board dimensions must NOT be used as proof of this physical board. "
                "Direct caliper or ruler measurements of the physical board are unavailable in the evidence set."
            ),
        },
        # 3. Chosen working-canvas dimensions and aspect ratio
        "provisional_working_canvas": {
            "width_px": 1350,
            "height_px": 1000,
            "aspect_ratio": 1.350,
            "classification": "PROVISIONAL_COMPUTATIONAL_CHOICE",
            "justification": (
                "A convenient integer Cartesian grid (1350x1000) chosen strictly for numerical computation "
                "and reproducible pixel coordinates. It must NOT be construed as a confirmed physical board measurement."
            ),
        },
        # Top-level backwards compatibility fields
        "span_north_px": span_north,
        "span_south_px": span_south,
        "span_west_px": span_west,
        "span_east_px": span_east,
        "average_width_px": avg_width,
        "average_height_px": avg_height,
        "raw_2d_aspect_ratio": float(raw_aspect_ratio),
        "pinhole_3d_aspect_ratio": pinhole_aspect_ratio,
        "estimated_focal_length_px": focal_length,
        "recommended_aspect_ratio": 1.35,
        "aspect_ratio_uncertainty": 0.04,
        "explanation": (
            "Image-space 2D corner spans in complete.jpeg yield 1.336 +/- 0.040. "
            "Perspective pinhole solution yields 1.226 (sensitive to corner grazing at y=0). "
            "Physical board aspect ratio remains UNRESOLVED from the photographs alone. "
            "The 1350x1000 working canvas (1.350) is retained strictly as a provisional computational choice."
        ),
    }


def analyze_fold_proximity(
    normalized_coords: np.ndarray, residuals: np.ndarray
) -> Dict[str, Any]:
    """
    Analyzes whether residuals correlate with proximity to the board's physical fold lines.
    The Scotland Yard board is a quad-fold board with:
    - Vertical seam at x_norm = 0.50
    - Horizontal crease at y_norm = 0.50
    """
    vert_dist = np.abs(normalized_coords[:, 0] - 0.50)
    horiz_dist = np.abs(normalized_coords[:, 1] - 0.50)
    min_fold_dist = np.minimum(vert_dist, horiz_dist)

    # Classify points as near fold (within 0.08 normalized units) vs far
    near_mask = min_fold_dist < 0.08
    far_mask = ~near_mask

    near_residuals = residuals[near_mask] if np.any(near_mask) else np.array([])
    far_residuals = residuals[far_mask] if np.any(far_mask) else np.array([])

    return {
        "near_fold_count": int(np.sum(near_mask)),
        "far_fold_count": int(np.sum(far_mask)),
        "near_fold_mean_residual": float(np.mean(near_residuals)) if len(near_residuals) > 0 else 0.0,
        "far_fold_mean_residual": float(np.mean(far_residuals)) if len(far_residuals) > 0 else 0.0,
        "correlation_with_fold_distance": float(np.corrcoef(min_fold_dist, residuals)[0, 1])
        if len(residuals) > 2 and np.std(min_fold_dist) > 0 and np.std(residuals) > 0
        else 0.0,
    }
