import tempfile
from fastapi import APIRouter, File, UploadFile, Form

from ..models import SpeechRequest, SpeechResponse
from ..services.speech import analyze_speech, analyze_uploaded_speech

router = APIRouter()


@router.post("/analyze", response_model=SpeechResponse)
async def analyze_speech_endpoint(payload: SpeechRequest) -> SpeechResponse:
    return analyze_speech(payload)


@router.post("/upload", response_model=SpeechResponse)
async def analyze_upload(
    file: UploadFile = File(...),
    reference_text: str = Form("")
) -> SpeechResponse:
    """Accept audio file upload, persist temporarily, and run ASR pipeline."""
    suffix = f".{file.filename.split('.')[-1]}" if file.filename else ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        data = await file.read()
        tmp.write(data)
        path = tmp.name
    return analyze_uploaded_speech(path, reference_text or None)
