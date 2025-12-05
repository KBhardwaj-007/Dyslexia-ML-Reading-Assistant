from ..models import AssistRequest, AssistResponse, Highlight


def generate_assistance(payload: AssistRequest) -> AssistResponse:
    text = payload.text
    target = payload.target_word or (text.split()[0] if text else "")
    start = text.lower().find(target.lower()) if target else 0
    end = start + len(target) if target else 0

    syllable_splits = [idx for idx, ch in enumerate(text) if ch in {"-", " "}]
    highlights = []
    if start >= 0:
        highlights.append(Highlight(start=start, end=end, color="#ffd166"))

    return AssistResponse(
        tts_preview_url="/static/tts-preview.mp3",
        syllable_splits=syllable_splits,
        highlights=highlights,
        narration_speed=0.9,
    )
