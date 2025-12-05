"""Attention provider hooks (MediaPipe / OpenCV).

These functions are placeholders to integrate real gaze/blink estimation models. They currently
return None so the service layer can fall back to client-provided signals.
"""
from __future__ import annotations
from typing import Optional, Tuple

try:  # Optional dependency
    import cv2  # type: ignore
except ImportError:  # pragma: no cover - optional
    cv2 = None  # type: ignore


def estimate_focus_from_frame(frame_bytes: bytes) -> Optional[Tuple[float, float]]:
    """Return (focus_score, blink_rate) if a model is available; otherwise None."""
    if cv2 is None:
        return None
    # Placeholder: real implementation would decode frame and run eye-aspect-ratio or landmark model
    return None
