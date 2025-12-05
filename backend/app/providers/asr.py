"""ASR provider hooks using Whisper (local) with graceful fallback."""
from __future__ import annotations

from functools import lru_cache
from typing import Optional

try:  # Optional dependency
    import whisper  # type: ignore
except ImportError:  # pragma: no cover - optional
    whisper = None  # type: ignore

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
        result = model.transcribe(audio_path_or_url)
        return result.get("text")
    except Exception:
        return None
