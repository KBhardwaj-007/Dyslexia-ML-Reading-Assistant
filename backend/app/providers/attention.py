"""Attention provider using MediaPipe Face Mesh.

Computes a coarse focus score from gaze alignment and eye openness. Blink rate is approximated
from eye-aspect ratio; without a frame sequence we return a nominal value unless eyes appear closed.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Optional, Tuple

import numpy as np

try:  # Optional dependencies
    import cv2  # type: ignore
    import mediapipe as mp  # type: ignore
except ImportError:  # pragma: no cover - optional
    cv2 = None  # type: ignore
    mp = None  # type: ignore


@lru_cache
def _face_mesh():
    if mp is None:
        return None
    return mp.solutions.face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True)


def _eye_aspect_ratio(landmarks, idxs) -> float:
    p = np.array([(landmarks[i].x, landmarks[i].y) for i in idxs])
    # vertical distances
    vert1 = np.linalg.norm(p[1] - p[5])
    vert2 = np.linalg.norm(p[2] - p[4])
    horiz = np.linalg.norm(p[0] - p[3]) + 1e-6
    return (vert1 + vert2) / (2.0 * horiz)


def _gaze_center(landmarks) -> float:
    # Use iris center vs eye corners to gauge off-center gaze (0 = straight, 1 = far off)
    left_corners = [33, 133]
    left_iris = 468
    lx = landmarks[left_corners[0]].x
    rx = landmarks[left_corners[1]].x
    cx = landmarks[left_iris].x
    span = max(abs(rx - lx), 1e-6)
    offset = abs(cx - (lx + rx) / 2) / span
    return offset


def estimate_focus_from_frame(frame_bytes: bytes) -> Optional[Tuple[float, float]]:
    if cv2 is None or mp is None:
        return None
    mesh = _face_mesh()
    if mesh is None:
        return None

    np_frame = np.frombuffer(frame_bytes, np.uint8)
    img = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)
    if img is None:
        return None

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = mesh.process(img_rgb)
    if not result.multi_face_landmarks:
        return None

    landmarks = result.multi_face_landmarks[0].landmark
    left_eye = [33, 160, 158, 133, 153, 144]  # mediapipe indices
    right_eye = [362, 385, 387, 263, 373, 380]
    ear_left = _eye_aspect_ratio(landmarks, left_eye)
    ear_right = _eye_aspect_ratio(landmarks, right_eye)
    ear = (ear_left + ear_right) / 2

    gaze_offset = _gaze_center(landmarks)

    # Focus heuristic: high when eyes open and gaze near center
    focus = max(0.0, min(1.0, (1 - gaze_offset) * 0.8 + ear * 0.6))

    # Blink rate rough estimate: if eyes nearly closed, flag high blink; else nominal 15
    blink_rate = 30 if ear < 0.18 else 15

    return round(focus, 2), blink_rate
