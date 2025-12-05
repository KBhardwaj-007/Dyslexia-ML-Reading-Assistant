from typing import List, Optional
from pydantic import BaseModel, Field


class PronunciationError(BaseModel):
    word: str
    expected: str
    hint: str
    index: int = Field(..., description="Word index in the reference text")


class SpeechRequest(BaseModel):
    reference_text: Optional[str] = Field(None, description="Expected sentence for alignment")
    audio_url: Optional[str] = Field(None, description="URL to uploaded audio clip")
    transcript: Optional[str] = Field(None, description="Client-side ASR transcript if available")


class SpeechResponse(BaseModel):
    transcript: str
    accuracy: float
    pace_wpm: float
    errors: List[PronunciationError]
    coaching_tip: str


class AttentionRequest(BaseModel):
    focus_signal: float = Field(0.7, ge=0, le=1, description="Client-estimated focus score")
    blink_rate: float = Field(15, ge=0, description="Blinks per minute")
    session_duration_sec: float = Field(60, ge=0, description="Length of current reading window")
    frame_base64: Optional[str] = Field(None, description="Optional webcam frame for model-based focus estimation")


class AttentionResponse(BaseModel):
    focus_score: float
    fatigue_score: float
    distraction_flag: bool
    note: str


class AdaptationRequest(BaseModel):
    pace_wpm: float = Field(..., ge=0)
    error_rate: float = Field(..., ge=0, le=1)
    focus_score: float = Field(..., ge=0, le=1)
    current_level: str = Field("A1", description="Content difficulty tag")


class AdaptationResponse(BaseModel):
    next_level: str
    reading_speed_wpm: int
    font_size_px: int
    spacing_em: float
    hint_frequency: str
    rationale: str


class AssistRequest(BaseModel):
    text: str
    target_word: Optional[str] = None


class Highlight(BaseModel):
    start: int
    end: int
    color: str = "#ffd166"


class AssistResponse(BaseModel):
    tts_preview_url: str
    syllable_splits: List[int]
    highlights: List[Highlight]
    narration_speed: float


class MentorRequest(BaseModel):
    learner_name: str = "Reader"
    tone: str = Field("friendly", description="friendly | teacher | calm")
    focus_score: float = 0.7
    accuracy: float = 0.8
    pace_wpm: float = 110.0
    streak_minutes: float = 5.0


class MentorResponse(BaseModel):
    persona: str
    message: str
    summary: List[str]
    next_actions: List[str]


class SessionLogRequest(BaseModel):
    learner_name: str = "Reader"
    accuracy: float
    focus_score: float
    pace_wpm: float
    level: str
    note: str = ""


class SessionLogResponse(SessionLogRequest):
    id: int
    created_at: str