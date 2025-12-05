from typing import List
from ..models import SpeechRequest, SpeechResponse, PronunciationError
from ..providers.asr import transcribe_audio


def analyze_speech(payload: SpeechRequest) -> SpeechResponse:
    transcript = payload.transcript
    if not transcript and payload.audio_url:
        transcript = transcribe_audio(payload.audio_url)
    transcript = transcript or payload.reference_text or "The quick brown fox jumps over the lazy dog."
    reference = payload.reference_text or transcript
    words = reference.split()

    mock_errors: List[PronunciationError] = []
    for idx, word in enumerate(words):
        if word.lower().startswith("th") and idx % 3 == 0:
            mock_errors.append(
                PronunciationError(
                    word=word,
                    expected=word,
                    hint="Lightly place your tongue between your teeth for 'th'.",
                    index=idx,
                )
            )

    accuracy = max(0.65, 1 - (len(mock_errors) * 0.05))
    pace_wpm = 115.0 if len(words) < 40 else 135.0
    coaching_tip = "Great focus—slow slightly to emphasize tricky sounds." if accuracy >= 0.8 else "Try repeating highlighted words; listen to the model audio first."

    return SpeechResponse(
        transcript=transcript,
        accuracy=round(accuracy, 2),
        pace_wpm=round(pace_wpm, 1),
        errors=mock_errors,
        coaching_tip=coaching_tip,
    )
