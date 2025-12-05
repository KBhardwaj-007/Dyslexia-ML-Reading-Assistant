<<<<<<< HEAD
"""ASR provider hooks.

These functions are structured to let you plug in Whisper (local or API), Google, or Azure.
Currently they return None when the provider is unavailable so the service layer can fall back to heuristics.
"""
from __future__ import annotations
=======
"""ASR provider hooks using Whisper (local) with graceful fallback."""
from __future__ import annotations

from functools import lru_cache
>>>>>>> 7974fd6 (added all the initial requirements and gitignore for myenv)
from typing import Optional

try:  # Optional dependency
    import whisper  # type: ignore
except ImportError:  # pragma: no cover - optional
    whisper = None  # type: ignore

<<<<<<< HEAD

def transcribe_audio(audio_path_or_url: str, model_size: str = "base") -> Optional[str]:
    """Attempt Whisper transcription if library is installed; otherwise return None."""
    if whisper is None:
        return None
    try:
        model = whisper.load_model(model_size)
=======
from ..config import get_settings


@lru_cache
def _load_model(model_size: str = "base"):
    if whisper is None:
        return None
    settings = get_settings()
    return whisper.load_model(model_size, device=settings.device)


def transcribe_audio(audio_path_or_url: str, model_size: str = "base") -> Optional[str]:
    """Transcribe audio via Whisper if available; returns None on failure."""
    settings = get_settings()
    size = settings.whisper_model_size or model_size
    model = _load_model(size)
    if model is None:
        return None
    try:
>>>>>>> 7974fd6 (added all the initial requirements and gitignore for myenv)
        result = model.transcribe(audio_path_or_url)
        return result.get("text")
    except Exception:
        return None
