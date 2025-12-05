from fastapi import APIRouter

from ..models import SpeechRequest, SpeechResponse
from ..services.speech import analyze_speech

router = APIRouter()


@router.post("/analyze", response_model=SpeechResponse)
async def analyze_speech_endpoint(payload: SpeechRequest) -> SpeechResponse:
    return analyze_speech(payload)
