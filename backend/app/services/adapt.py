from ..models import AdaptationRequest, AdaptationResponse

LEVEL_ORDER = ["A1", "A2", "B1", "B2", "C1"]


<<<<<<< HEAD
=======
def _smooth(curr: float, prev: float | None, alpha: float = 0.6) -> float:
    if prev is None:
        return curr
    return alpha * curr + (1 - alpha) * prev


>>>>>>> 7974fd6 (added all the initial requirements and gitignore for myenv)
def next_level(current: str, accuracy: float, focus: float) -> str:
    if accuracy > 0.85 and focus > 0.55:
        try:
            return LEVEL_ORDER[LEVEL_ORDER.index(current) + 1]
        except (ValueError, IndexError):
            return current
    if accuracy < 0.6 or focus < 0.4:
        try:
            idx = max(0, LEVEL_ORDER.index(current) - 1)
            return LEVEL_ORDER[idx]
        except ValueError:
            return current
    return current


def plan_adjustments(payload: AdaptationRequest) -> AdaptationResponse:
<<<<<<< HEAD
    accuracy = 1 - payload.error_rate
    candidate_level = next_level(payload.current_level, accuracy, payload.focus_score)

    target_speed = 120
    if payload.pace_wpm > 130 and payload.error_rate < 0.1:
        target_speed = 140
    if payload.focus_score < 0.5:
        target_speed = 110

    font_size = 20 if candidate_level in {"A1", "A2"} else 18
    spacing = 1.6 if payload.focus_score < 0.5 else 1.4
    hint_frequency = "often" if payload.error_rate > 0.15 else "contextual"

    rationale = (
        f"Pace {payload.pace_wpm} wpm, errors {payload.error_rate:.2f}, focus {payload.focus_score:.2f}; "
=======
    smooth_focus = _smooth(payload.focus_score, payload.prev_focus_score)
    smooth_pace = _smooth(payload.pace_wpm, payload.prev_pace_wpm)
    smooth_error = _smooth(payload.error_rate, payload.prev_error_rate)

    accuracy = 1 - smooth_error
    candidate_level = next_level(payload.current_level, accuracy, smooth_focus)

    target_speed = 120
    if smooth_pace > 130 and smooth_error < 0.1:
        target_speed = 140
    if smooth_focus < 0.5:
        target_speed = 110

    font_size = 20 if candidate_level in {"A1", "A2"} else 18
    spacing = 1.6 if smooth_focus < 0.5 else 1.4
    hint_frequency = "often" if smooth_error > 0.15 else "contextual"

    rationale = (
        f"Smoothed pace {smooth_pace:.1f} wpm, errors {smooth_error:.2f}, focus {smooth_focus:.2f}; "
>>>>>>> 7974fd6 (added all the initial requirements and gitignore for myenv)
        f"set level {candidate_level}, speed {target_speed} wpm, spacing {spacing}."
    )

    return AdaptationResponse(
        next_level=candidate_level,
        reading_speed_wpm=target_speed,
        font_size_px=font_size,
        spacing_em=round(spacing, 2),
        hint_frequency=hint_frequency,
        rationale=rationale,
    )
