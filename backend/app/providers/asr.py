"""ASR provider hooks.

These functions are structured to let you plug in Whisper (local or API), Google, or Azure.
Currently they return None when the provider is unavailable so the service layer can fall back to heuristics.
"""
from __future__ import annotations
from typing import Optional

try:  # Optional dependency
    import whisper  # type: ignore
except ImportError:  # pragma: no cover - optional
    whisper = None  # type: ignore


def transcribe_audio(audio_path_or_url: str, model_size: str = "base") -> Optional[str]:
    """Attempt Whisper transcription if library is installed; otherwise return None."""
    if whisper is None:
        return None
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path_or_url)
        return result.get("text")
    except Exception:
        return None
