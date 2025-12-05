import base64
from typing import Optional, Tuple

from ..models import AttentionRequest, AttentionResponse
from ..providers.attention import estimate_focus_from_frame


def _decode_frame(frame_base64: Optional[str]) -> Optional[bytes]:
    if not frame_base64:
        return None
    try:
        return base64.b64decode(frame_base64)
    except Exception:
        return None


def analyze_attention(payload: AttentionRequest) -> AttentionResponse:
    frame_bytes = _decode_frame(payload.frame_base64)
    model_estimate: Optional[Tuple[float, float]] = None
    if frame_bytes:
        model_estimate = estimate_focus_from_frame(frame_bytes)

    focus_signal = payload.focus_signal
    blink_rate = payload.blink_rate
    if model_estimate:
        focus_signal, blink_rate = model_estimate

    focus = min(1.0, max(0.0, focus_signal * 0.8 + (1 - blink_rate / 30)))
    fatigue = min(1.0, max(0.0, payload.session_duration_sec / 1800))
    distraction = focus < 0.45 or fatigue > 0.6

    if distraction:
        note = "Looks like focus dipped—take a 2-minute stretch and retry."
    elif fatigue > 0.4:
        note = "Nice work—consider a short break soon."
    else:
        note = "Focus steady—keep the flow going!"

    return AttentionResponse(
        focus_score=round(focus, 2),
        fatigue_score=round(fatigue, 2),
        distraction_flag=distraction,
        note=note,
    )
