# Backend (FastAPI)

Prototype API exposing the five core modules: Listen, Observe, Adapt, Assist, and Mentor.

## Install & Run
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Optional `.env` settings:
```
DATABASE_URL=sqlite:///./app.db
WHISPER_MODEL_SIZE=base   # e.g., small, medium
DEVICE=cpu                # or cuda if available
```

API root: http://localhost:8000
Docs: http://localhost:8000/docs

## Endpoints
- `POST /listen/analyze` — mock speech analysis returns transcript accuracy, pace, and error spans.
- `POST /listen/upload` — file upload to Whisper-powered transcription plus scoring.
- `POST /observe/analyze` — attention/fatigue estimation from focus score and blink rate.
- `POST /adapt/plan` — suggests next difficulty, spacing, and TTS speed.
- `POST /assist/assist` — returns mock TTS preview link and highlight spans.
- `POST /mentor/coach` — persona-based motivational feedback and next steps.
- `POST /sessions/log` — persists session summary (accuracy/focus/pace/level) to SQLite.
- `GET /sessions/recent` — list recent session logs.
- `GET /sessions/learner/{name}` — aggregate stats for a learner.

These endpoints use lightweight heuristics; swap in Whisper/MediaPipe/RL models via the service layer when available.

## Model Integrations
- **Whisper (openai-whisper + torch)**: `providers/asr.py` loads a cached Whisper model (default `base`) and `services/speech` will transcribe when `audio_url` is provided or when `/listen/upload` is used. Supply a local file path or upload a file.
- **MediaPipe Face Mesh**: `providers/attention.py` decodes a `frame_base64` image and computes focus score from gaze offset + eye aspect ratio; `services/attention` falls back to client signals if models are missing.

Notes:
- GPU-accelerated PyTorch is recommended for faster Whisper inference; adjust your environment accordingly.
- MediaPipe expects RGB frames; the service converts from BGR after decode.

## Docker
```bash
cd backend
docker build -t dyslexia-assistant-api .
docker run -p 8000:8000 --env-file .env dyslexia-assistant-api
```
